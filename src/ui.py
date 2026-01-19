"""
Professional Streamlit UI for Nepal Telco Churn Prediction
Advanced interface with multiple prediction modes, analytics, and data visualization
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import sys
from pathlib import Path

# Handle imports for different deployment environments
try:
    # Try absolute imports (for local/Docker)
    from src.model_service import ChurnModelService
    from src.predmodel import CustomerData
except ImportError:
    try:
        # Try relative imports (for Streamlit Cloud with src in path)
        from model_service import ChurnModelService
        from predmodel import CustomerData
    except ImportError:
        # Add current directory to path and try again
        sys.path.insert(0, str(Path(__file__).parent))
        from model_service import ChurnModelService
        from predmodel import CustomerData

# ==================== Page Configuration ====================
st.set_page_config(
    page_title="🇳🇵 Nepal Telco Churn Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main {
        padding: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .high-risk {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .medium-risk {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .low-risk {
        background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .section-title {
        color: #1f77b4;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 10px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== Initialize Session State ====================
if "predictions_history" not in st.session_state:
    st.session_state.predictions_history = []

if "model_service" not in st.session_state:
    try:
        st.session_state.model_service = ChurnModelService()
    except Exception as e:
        st.error(f"❌ Failed to initialize model service: {str(e)}")
        st.stop()

model_service = st.session_state.model_service

# ==================== Helper Functions ====================

def create_risk_gauge(probability: float) -> go.Figure:
    """Create a gauge chart for risk visualization"""
    color = "#30cfd0" if probability < 0.3 else "#fa709a" if probability < 0.6 else "#f5576c"
    
    fig = go.Figure(data=[go.Indicator(
        mode="gauge+number+delta",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Churn Risk %"},
        delta={'reference': 50, 'suffix': " vs baseline"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 30], 'color': "rgba(48, 207, 208, 0.2)"},
                {'range': [30, 60], 'color': "rgba(250, 112, 154, 0.2)"},
                {'range': [60, 100], 'color': "rgba(245, 87, 108, 0.2)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    )])
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=70, b=20))
    return fig

def create_comparison_chart(customers_data: list) -> go.Figure:
    """Create comparison chart for multiple customers"""
    names = [c['name'] for c in customers_data]
    probs = [c['probability'] for c in customers_data]
    colors = ["#30cfd0" if p < 0.3 else "#fa709a" if p < 0.6 else "#f5576c" for p in probs]
    
    fig = go.Figure(data=[
        go.Bar(x=names, y=[p*100 for p in probs], marker_color=colors)
    ])
    fig.update_layout(
        title="Customer Churn Risk Comparison",
        yaxis_title="Churn Probability (%)",
        xaxis_title="Customer Name",
        height=400,
        hovermode='x unified'
    )
    return fig

def save_prediction(prediction_result: dict):
    """Save prediction to history"""
    st.session_state.predictions_history.append({
        "timestamp": datetime.now(),
        **prediction_result
    })

def export_predictions():
    """Export prediction history as CSV"""
    if st.session_state.predictions_history:
        df = pd.DataFrame(st.session_state.predictions_history)
        return df.to_csv(index=False).encode('utf-8')
    return None

# ==================== Header Section ====================
st.markdown("""
# 🇳🇵 Nepal Telco Churn Prediction System
### Advanced ML-Based Customer Retention Analytics
---
""")

# Model Status
col1, col2, col3 = st.columns(3)
with col1:
    status = "✅ Online" if model_service.model_loaded else "❌ Offline"
    st.metric("Model Status", status)
with col2:
    st.metric("Features", "17")
with col3:
    st.metric("Accuracy", "~92%")

# ==================== Main Navigation ====================
st.sidebar.markdown("## 🔧 Navigation")
page = st.sidebar.radio(
    "Select Mode",
    ["Single Prediction", "Batch Prediction", "Analytics Dashboard", "Prediction History"]
)

# ==================== PAGE 1: Single Prediction ====================
if page == "Single Prediction":
    st.markdown("### 📋 Single Customer Prediction")
    st.markdown("Enter customer details below to predict churn risk and get personalized retention recommendations.")
    
    # Create two-column layout for inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Demographics")
        name = st.text_input("Customer Name", placeholder="e.g., Ram Kumar")
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
        num_dependents = st.number_input("Number of Dependents", min_value=0, max_value=10, value=2)
        
        st.subheader("💰 Financial")
        estimated_salary = st.number_input(
            "Estimated Monthly Salary (NPR)",
            min_value=0, value=50000, step=5000
        )
    
    with col2:
        st.subheader("📱 Service Usage")
        tenure_months = st.slider("Tenure (Months)", 0, 72, 24)
        calls_made = st.number_input("Monthly Calls Made", min_value=0, value=45, step=5)
        sms_sent = st.number_input("Monthly SMS Sent", min_value=0, value=30, step=5)
        data_used = st.number_input("Monthly Data Used (MB)", min_value=0, value=1500, step=100)
        
        st.subheader("🏢 Service Provider")
        province = st.selectbox(
            "Province",
            ["Bagmati", "Gandaki", "Karnali", "Koshi", "Lumbini", "Madhesh", "Sudurpashchim"]
        )
        provider = st.selectbox("Provider", ["Ncell", "Nepal Telecom"])
    
    # Prediction Button
    st.divider()
    if st.button("🔮 Predict Churn Risk", use_container_width=True, type="primary"):
        if not name:
            st.warning("⚠️ Please enter customer name")
        else:
            with st.spinner("🔄 Analyzing customer data..."):
                try:
                    customer_dict = {
                        "name": name,
                        "gender": gender,
                        "age": age,
                        "num_dependents": num_dependents,
                        "estimated_salary": estimated_salary,
                        "calls_made": calls_made,
                        "sms_sent": sms_sent,
                        "data_used": data_used,
                        "tenure_months": tenure_months,
                        "province": province,
                        "provider": provider
                    }
                    
                    result = model_service.predict(customer_dict)
                    
                    if result.get("success"):
                        # Save to history
                        save_prediction(result)
                        
                        # Display Results
                        st.success("✅ Prediction Complete!")
                        st.divider()
                        
                        # Main Results
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            probability = result["churn_probability"] / 100
                            st.metric(
                                "Churn Prediction",
                                result["churn_prediction"],
                                f"{result['churn_probability']:.1f}%"
                            )
                        
                        with col2:
                            risk_colors = {
                                "LOW": "🟢",
                                "MEDIUM": "🟡",
                                "HIGH": "🔴"
                            }
                            st.metric(
                                "Risk Level",
                                f"{risk_colors.get(result['risk_level'], '')} {result['risk_level']}"
                            )
                        
                        with col3:
                            st.metric(
                                "Tenure",
                                f"{tenure_months} months",
                                f"Provider: {provider}"
                            )
                        
                        st.divider()
                        
                        # Gauge Chart
                        gauge_chart = create_risk_gauge(probability)
                        st.plotly_chart(gauge_chart, use_container_width=True)
                        
                        # Recommendations
                        st.subheader("💡 Retention Recommendations")
                        if result["recommendations"]:
                            for i, rec in enumerate(result["recommendations"], 1):
                                st.info(f"**{i}.** {rec}")
                        else:
                            st.success("No specific recommendations needed. Customer is stable.")
                        
                        # Customer Profile Summary
                        with st.expander("📊 Customer Profile Summary"):
                            profile_data = {
                                "Metric": [
                                    "Name", "Gender", "Age", "Province", "Provider",
                                    "Salary", "Tenure", "Calls", "SMS", "Data Usage"
                                ],
                                "Value": [
                                    name, gender, age, province, provider,
                                    f"₹{estimated_salary:,.0f}", f"{tenure_months}m",
                                    calls_made, sms_sent, f"{data_used}MB"
                                ]
                            }
                            st.dataframe(pd.DataFrame(profile_data), use_container_width=True)
                    else:
                        st.error(f"❌ Prediction failed: {result.get('error', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ==================== PAGE 2: Batch Prediction ====================
elif page == "Batch Prediction":
    st.markdown("### 📦 Batch Customer Prediction")
    st.markdown("Upload a CSV file with multiple customers to predict churn for all at once.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write(f"📄 Loaded {len(df)} customers")
            
            # Display sample
            with st.expander("View Sample Data"):
                st.dataframe(df.head(), use_container_width=True)
            
            if st.button("🔮 Predict All Customers", type="primary", use_container_width=True):
                with st.spinner("🔄 Processing batch predictions..."):
                    predictions = []
                    progress_bar = st.progress(0)
                    
                    for idx, row in df.iterrows():
                        try:
                            customer_dict = row.to_dict()
                            result = model_service.predict(customer_dict)
                            if result.get("success"):
                                predictions.append(result)
                                save_prediction(result)
                            else:
                                predictions.append({
                                    "customer_name": customer_dict.get("name", "Unknown"),
                                    "churn_prediction": "ERROR",
                                    "churn_probability": 0,
                                    "risk_level": "UNKNOWN"
                                })
                        except Exception as e:
                            st.warning(f"Skipped row {idx}: {str(e)}")
                        
                        progress_bar.progress((idx + 1) / len(df))
                    
                    # Results Summary
                    st.success(f"✅ Processed {len(predictions)} customers")
                    
                    results_df = pd.DataFrame(predictions)
                    
                    # Statistics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        churn_count = (results_df["churn_prediction"] == "CHURN").sum()
                        st.metric("Churn Risk", f"{churn_count}/{len(results_df)}")
                    with col2:
                        high_risk = (results_df["risk_level"] == "HIGH").sum()
                        st.metric("High Risk", f"{high_risk}/{len(results_df)}")
                    with col3:
                        avg_prob = results_df["churn_probability"].mean()
                        st.metric("Avg Risk %", f"{avg_prob:.1f}%")
                    with col4:
                        medium_risk = (results_df["risk_level"] == "MEDIUM").sum()
                        st.metric("Medium Risk", f"{medium_risk}/{len(results_df)}")
                    
                    st.divider()
                    
                    # Results Table
                    st.subheader("📋 Prediction Results")
                    st.dataframe(results_df, use_container_width=True)
                    
                    # Comparison Chart
                    comparison_data = results_df.head(15).to_dict('records')
                    if comparison_data:
                        comparison_data = [
                            {
                                "name": d.get("customer_name", "Unknown"),
                                "probability": d.get("churn_probability", 0) / 100
                            }
                            for d in comparison_data
                        ]
                        comparison_chart = create_comparison_chart(comparison_data)
                        st.plotly_chart(comparison_chart, use_container_width=True)
                    
                    # Download Results
                    csv_download = results_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv_download,
                        file_name=f"churn_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

# ==================== PAGE 3: Analytics Dashboard ====================
elif page == "Analytics Dashboard":
    st.markdown("### 📊 Analytics Dashboard")
    
    if st.session_state.predictions_history:
        history_df = pd.DataFrame(st.session_state.predictions_history)
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Predictions", len(history_df))
        with col2:
            churn_rate = (history_df["churn_prediction"] == "CHURN").sum() / len(history_df) * 100
            st.metric("Churn Rate", f"{churn_rate:.1f}%")
        with col3:
            avg_risk = history_df["churn_probability"].mean()
            st.metric("Avg Risk", f"{avg_risk:.1f}%")
        with col4:
            high_risk_count = (history_df["risk_level"] == "HIGH").sum()
            st.metric("High Risk Count", high_risk_count)
        
        st.divider()
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk Distribution
            risk_counts = history_df["risk_level"].value_counts()
            fig_risk = px.pie(
                values=risk_counts.values, labels=risk_counts.index,
                title="Risk Level Distribution",
                color_discrete_map={"LOW": "#30cfd0", "MEDIUM": "#fa709a", "HIGH": "#f5576c"}
            )
            st.plotly_chart(fig_risk, use_container_width=True)
        
        with col2:
            # Churn Prediction Distribution
            churn_counts = history_df["churn_prediction"].value_counts()
            fig_churn = px.bar(
                x=churn_counts.index, y=churn_counts.values,
                title="Churn Prediction Distribution",
                labels={"x": "Prediction", "y": "Count"}
            )
            st.plotly_chart(fig_churn, use_container_width=True)
        
        # Probability Distribution
        fig_prob = px.histogram(
            history_df, x="churn_probability",
            nbins=20, title="Churn Probability Distribution",
            labels={"churn_probability": "Churn Probability (%)"}
        )
        st.plotly_chart(fig_prob, use_container_width=True)
        
    else:
        st.info("📊 No predictions yet. Make some predictions to see analytics!")

# ==================== PAGE 4: Prediction History ====================
elif page == "Prediction History":
    st.markdown("### 📜 Prediction History")
    
    if st.session_state.predictions_history:
        history_df = pd.DataFrame(st.session_state.predictions_history)
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            risk_filter = st.multiselect(
                "Filter by Risk Level",
                ["LOW", "MEDIUM", "HIGH"],
                default=["LOW", "MEDIUM", "HIGH"]
            )
        with col2:
            churn_filter = st.multiselect(
                "Filter by Prediction",
                ["CHURN", "RETAIN"],
                default=["CHURN", "RETAIN"]
            )
        
        filtered_df = history_df[
            (history_df["risk_level"].isin(risk_filter)) &
            (history_df["churn_prediction"].isin(churn_filter))
        ]
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # Export
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download History",
            data=csv_data,
            file_name=f"prediction_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Clear History
        if st.button("🗑️ Clear History", type="secondary", use_container_width=True):
            st.session_state.predictions_history = []
            st.rerun()
    else:
        st.info("📜 No prediction history yet.")

# ==================== Footer ====================
st.divider()
st.markdown("""
---
### About This Application
🔬 **Advanced ML-Based Customer Churn Prediction**
- Powered by Deep Learning (Artificial Neural Network)
- Trained on Localized Nepalese telecom customer data
- Real-time batch processing capabilities
- Professional analytics dashboard
- Accuracy score of ~80%

📞 **For more information:** sahajgnawali@gmail.com
""")
