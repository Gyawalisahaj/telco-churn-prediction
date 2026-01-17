import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense, BatchNormalization, Dropout

# Import your Pydantic model from predmodel.py
from src.predmodel import CustomerData 

# 1. Initialize FastAPI
app = FastAPI(
    title="Nepal Telco Churn API",
    description="Deep Learning API to predict customer churn in the Nepalese Telecom sector."
)

# 2. Load trained objects
try:
    model = load_model("model/Churnpred_ann.keras")
    scaler = joblib.load("model/scaler.pkl")
    train_columns = joblib.load("model/train_columns.pkl")
    print("✅ System: Model and Scaler loaded successfully!")
except Exception as e:
    print(f"⚠️ System: Model loading failed. Using fallback model.")
    print(f"Error: {e}")
    # Create fallback model
    model = Sequential([
        Dense(32, activation='relu', input_shape=(17,)),
        BatchNormalization(),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    # Load scaler and columns
    scaler = joblib.load("model/scaler.pkl")
    train_columns = joblib.load("model/train_columns.pkl")
    print("✅ System: Fallback model and Scaler loaded successfully!")

# 3. Prediction Helper Function
def run_prediction(data: CustomerData):
    # Create an empty dataframe with 17 columns (initialized to 0)
    input_df = pd.DataFrame(0, index=[0], columns=train_columns)

    # Map raw input from Pydantic model to DataFrame
    input_df["gender"] = 1 if data.gender.upper() == "M" else 0
    input_df["age"] = data.age
    input_df["num_dependents"] = data.num_dependents
    input_df["estimated_salary"] = data.estimated_salary
    input_df["calls_made"] = data.calls_made
    input_df["sms_sent"] = data.sms_sent
    input_df["data_used"] = data.data_used
    input_df["tenure_months"] = data.tenure_months

    # Handle One-Hot Encoding for Nepal Provinces and Providers
    if f"province_{data.province}" in input_df.columns:
        input_df[f"province_{data.province}"] = 1
    if f"provider_nepal_{data.provider}" in input_df.columns:
        input_df[f"provider_nepal_{data.provider}"] = 1

    # Scale only the numeric columns
    cols_to_scale = [
        "age", "estimated_salary", "calls_made", 
        "sms_sent", "data_used", "tenure_months", "num_dependents"
    ]
    input_df[cols_to_scale] = scaler.transform(input_df[cols_to_scale])

    # Perform Prediction
    prediction_prob = float(model.predict(input_df.values, verbose=0)[0][0])
    
    # Determine Status and Risk
    status = "CHURN" if prediction_prob > 0.5 else "STAY"
    risk = "LOW" if prediction_prob < 0.3 else "MEDIUM" if prediction_prob < 0.6 else "HIGH"

    return {
        "customer_name": data.name,
        "churn_prediction": status,
        "churn_probability": round(prediction_prob * 100, 2),
        "risk_level": risk
    }

# 4. API Endpoints
@app.get("/")
def read_root():
    return {"status": "API is active", "project": "Nepal Telco Churn Prediction"}

@app.post("/predict")
def predict_churn(data: CustomerData):
    """
    Accepts customer data and returns Churn Probability and Risk Level.
    """
    return run_prediction(data)