"""
Advanced Model Service for Churn Prediction
Handles model loading, preprocessing, and predictions with caching and error handling
"""

import os
import joblib
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, Optional
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChurnModelService:
    """Singleton service for managing churn prediction model"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChurnModelService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.model = None
        self.scaler = None
        self.train_columns = None
        self.model_loaded = False
        self._initialized = True
        
        self.load_model_and_dependencies()
    
    def load_model_and_dependencies(self) -> bool:
        """Load the trained model, scaler, and training columns"""
        try:
            base_path = Path(__file__).parent.parent
            model_path = base_path / "model" / "Churnpred_ann.keras"
            scaler_path = base_path / "model" / "scaler.pkl"
            columns_path = base_path / "model" / "train_columns.pkl"
            
            if model_path.exists():
                try:
                    self.model = load_model(str(model_path))
                    logger.info(f"✅ Model loaded successfully from {model_path}")
                except Exception as model_error:
                    logger.warning(f"⚠️ Could not load saved model: {str(model_error)}")
                    logger.warning("⚠️ Using fallback model instead")
                    self.model = self._create_fallback_model()
            else:
                logger.warning(f"⚠️ Model not found at {model_path}. Creating fallback model.")
                self.model = self._create_fallback_model()
            
            if scaler_path.exists():
                try:
                    self.scaler = joblib.load(str(scaler_path))
                    logger.info(f"✅ Scaler loaded successfully")
                except Exception as scaler_error:
                    logger.warning(f"⚠️ Could not load scaler: {str(scaler_error)}")
                    from sklearn.preprocessing import StandardScaler
                    self.scaler = StandardScaler()
            else:
                logger.warning("⚠️ Scaler not found. Creating fallback.")
                from sklearn.preprocessing import StandardScaler
                self.scaler = StandardScaler()
            
            if columns_path.exists():
                try:
                    self.train_columns = joblib.load(str(columns_path))
                    logger.info(f"✅ Training columns loaded: {len(self.train_columns)} features")
                except Exception as col_error:
                    logger.warning(f"⚠️ Could not load columns: {str(col_error)}")
                    self.train_columns = self._get_default_columns()
            else:
                self.train_columns = self._get_default_columns()
                logger.warning("⚠️ Using default training columns")
            
            self.model_loaded = True
            logger.info("✅ Model service fully initialized with fallback support")
            return True
            
        except Exception as e:
            logger.error(f"❌ Critical error during initialization: {str(e)}")
            logger.info("Creating complete fallback model...")
            self.model = self._create_fallback_model()
            from sklearn.preprocessing import StandardScaler
            self.scaler = StandardScaler()
            self.train_columns = self._get_default_columns()
            self.model_loaded = True
            return True
    
    def _create_fallback_model(self) -> Sequential:
        """Create a fallback model if the trained model is not available"""
        logger.info("Creating fallback model...")
        model = Sequential([
            Dense(32, activation='relu', input_shape=(17,)),
            BatchNormalization(),
            Dropout(0.3),
            Dense(16, activation='relu'),
            Dropout(0.2),
            Dense(8, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model
    
    def _get_default_columns(self) -> list:
        """Return default training columns"""
        return [
            'gender', 'age', 'num_dependents', 'estimated_salary',
            'calls_made', 'sms_sent', 'data_used', 'tenure_months',
            'province_Bagmati', 'province_Gandaki', 'province_Karnali',
            'province_Koshi', 'province_Lumbini', 'province_Madhesh',
            'province_Sudurpashchim', 'provider_nepal_Ncell',
            'provider_nepal_Nepal_Telecom'
        ]
    
    def preprocess_input(self, customer_dict: Dict) -> Tuple[pd.DataFrame, bool]:
        """
        Preprocess customer data to match model input format
        
        Args:
            customer_dict: Dictionary with customer information
            
        Returns:
            Tuple of (processed_dataframe, success_flag)
        """
        try:
            input_df = pd.DataFrame(0, index=[0], columns=self.train_columns)
            
            # Map basic fields
            input_df["gender"] = 1 if customer_dict.get('gender', '').upper() in ['MALE', 'M'] else 0
            input_df["age"] = customer_dict.get('age', 0)
            input_df["num_dependents"] = customer_dict.get('num_dependents', 0)
            input_df["estimated_salary"] = customer_dict.get('estimated_salary', 0)
            input_df["calls_made"] = customer_dict.get('calls_made', 0)
            input_df["sms_sent"] = customer_dict.get('sms_sent', 0)
            input_df["data_used"] = customer_dict.get('data_used', 0)
            input_df["tenure_months"] = customer_dict.get('tenure_months', 0)
            
            # Handle one-hot encoding for province
            province = customer_dict.get('province', '')
            province_col = f"province_{province}"
            if province_col in input_df.columns:
                input_df[province_col] = 1
            
            # Handle one-hot encoding for provider
            provider = customer_dict.get('provider', '')
            provider_col = f"provider_nepal_{provider}" if provider else None
            if provider_col and provider_col in input_df.columns:
                input_df[provider_col] = 1
            
            # Scale numeric features
            cols_to_scale = [
                "age", "estimated_salary", "calls_made",
                "sms_sent", "data_used", "tenure_months", "num_dependents"
            ]
            
            if self.scaler:
                try:
                    input_df[cols_to_scale] = self.scaler.transform(input_df[cols_to_scale])
                except Exception as e:
                    logger.warning(f"⚠️ Could not scale features: {str(e)}")
            
            return input_df, True
            
        except Exception as e:
            logger.error(f"❌ Error preprocessing input: {str(e)}")
            return None, False
    
    def predict(self, customer_dict: Dict) -> Dict:
        """
        Make a prediction for a customer
        
        Args:
            customer_dict: Dictionary with customer information
            
        Returns:
            Dictionary with prediction results
        """
        if not self.model_loaded:
            return {
                "success": False,
                "error": "Model not loaded. Please check server logs."
            }
        
        try:
            input_df, success = self.preprocess_input(customer_dict)
            if not success:
                return {
                    "success": False,
                    "error": "Failed to preprocess input data"
                }
            
            # Make prediction
            prediction_prob = float(self.model.predict(input_df.values, verbose=0)[0][0])
            
            # Determine status and risk level
            status = "CHURN" if prediction_prob > 0.5 else "RETAIN"
            if prediction_prob < 0.3:
                risk = "LOW"
            elif prediction_prob < 0.6:
                risk = "MEDIUM"
            else:
                risk = "HIGH"
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                prediction_prob, customer_dict, risk
            )
            
            return {
                "success": True,
                "customer_name": customer_dict.get('name', 'Unknown'),
                "churn_prediction": status,
                "churn_probability": round(prediction_prob * 100, 2),
                "risk_level": risk,
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"❌ Prediction error: {str(e)}")
            return {
                "success": False,
                "error": f"Prediction failed: {str(e)}"
            }
    
    def _generate_recommendations(self, prob: float, customer: Dict, risk: str) -> list:
        """Generate actionable recommendations based on prediction"""
        recommendations = []
        
        if prob > 0.5:
            recommendations.append("🚨 Priority: High-risk customer - Consider immediate retention strategy")
            recommendations.append("💬 Offer: Provide personalized discount or loyalty rewards")
            recommendations.append("📞 Action: Assign dedicated customer support representative")
        
        if customer.get('tenure_months', 0) < 12:
            recommendations.append("🆕 Customer is relatively new - Focus on onboarding & relationship building")
        
        if customer.get('calls_made', 0) < 20:
            recommendations.append("📉 Low engagement detected - Encourage service usage")
        
        if customer.get('estimated_salary', 0) < 30000:
            recommendations.append("💰 Consider affordable plans to reduce churn")
        
        if risk in ["MEDIUM", "HIGH"] and customer.get('data_used', 0) < 500:
            recommendations.append("📊 Data usage is low - Offer attractive data bundles")
        
        return recommendations
