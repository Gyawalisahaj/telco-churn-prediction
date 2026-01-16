import joblib
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pickle
import pandas as pd
import numpy as np

def predict_customer_churn(name, gender, age, num_dependent, salary, calls, sms, data, province, tenure, provider):
    input_df = pd.DataFrame(0, index=[0], columns=train_columns)
    

    input_df['gender'] = 1 if gender.upper() == 'M' else 0
    input_df['age'] = age
    input_df['num_dependents'] = num_dependent
    input_df['estimated_salary'] = salary
    input_df['calls_made'] = calls
    input_df['sms_sent'] = sms
    input_df['data_used'] = data
    input_df['tenure_months'] = tenure
    

    if f"province_{province}" in input_df.columns:
        input_df[f"province_{province}"] = 1
    if f"provider_nepal_{provider}" in input_df.columns:
        input_df[f"provider_nepal_{provider}"] = 1


    cols_to_scale = ['age', 'estimated_salary', 'calls_made', 'sms_sent', 'data_used', 'tenure_months', 'num_dependents']
    

    input_df[cols_to_scale] = scaler.transform(input_df[cols_to_scale])


    prediction_prob = model.predict(input_df.values, verbose=0)[0][0]
    
    status = "CHURN" if prediction_prob > 0.5 else "STAY"
    if prediction_prob < 0.3:
          risk_level = "LOW"
    elif 0.3 <= prediction_prob < 0.6:
          risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    

    print(f"\n{'='*30}")
    print(f" CUSTOMER ANALYSIS: {name.upper()}")
    print(f"{'='*30}")
    print(f" Prediction: {status}")
    print(f" Probability: {prediction_prob:.2%}")
    print(f" Risk Level: {risk_level}")
    print(f"{'='*30}\n")
    
    return status

# --- TEST ---
predict_customer_churn("Aayush", "M", 25, 2, 45000, 15, 5, 100, "Bagmati", 12, "Ncell")