import pandas as pd
import numpy as np



def stateLocalize(df: pd.DataFrame, state:str):
    state_localization = {
    'Karnataka': 'Bagmati', 'Maharashtra': 'Bagmati', 'Tamil Nadu': 'Bagmati', 
    'Telangana': 'Bagmati', 'Delhi': 'Bagmati', 'Goa': 'Bagmati',
    
    'Bihar': 'Madhesh', 'Uttar Pradesh': 'Madhesh', 'Andhra Pradesh': 'Madhesh',
    
    # Koshi Province 
    'West Bengal': 'Koshi', 'Sikkim': 'Koshi', 'Arunachal Pradesh': 'Koshi', 
    'Assam': 'Koshi', 'Nagaland': 'Koshi', 'Manipur': 'Koshi',
    
    # Gandaki Province 
    'Punjab': 'Gandaki', 'Haryana': 'Gandaki', 'Gujarat': 'Gandaki', 'Tripura': 'Gandaki',
    
    # Lumbini Province 
    'Rajasthan': 'Lumbini', 'Madhya Pradesh': 'Lumbini', 'Chhattisgarh': 'Lumbini', 'Odisha': 'Lumbini',
    
    # Karnali Province 
    'Mizoram': 'Karnali', 'Himachal Pradesh': 'Karnali', 'Meghalaya': 'Karnali',
    
    # Sudurpashchim Province 
    'Uttarakhand': 'Sudurpashchim', 'Jharkhand': 'Sudurpashchim', 'Kerala': 'Sudurpashchim'
    }
    df['province'] = df['state'].map(state_localization)
    return df


def providerLocalize(df: pd.DataFrame, provider:str):
    provider_mapping = {
    'Airtel': 'Ncell',
    'Reliance Jio': 'Ncell',
    'BSNL': 'Nepal Telecom (NTC)',
    'Vodafone': 'Nepal Telecom (NTC)'
   }
    df['provider_nepal'] = df['telecom_partner'].replace(provider_mapping)
    return df

def det_outlier(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5*IQR
    upper = Q3 + 1.5*IQR
    list1 = df[(df[col] < lower) | (df[col] > upper)]
    print('list:',list1)
    return list1

def data_Clean(df):
    df = df[df.calls_made >= 0 ]
    df = df[df.sms_sent >= 0 ]
    df = df[df.data_used >= 0 ]
    df = df.drop(['telecom_partner', 'state','city','pincode'], axis=1)
    return df

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = stateLocalize(df, 'state')
    df = providerLocalize(df, 'telecom_partner')
    df = data_Clean(df)
    return df


