import pandas as pd
import numpy as np

def load_data(filepath):
    """Loads the dataset from a CSV file."""
    df = pd.read_csv(filepath)
    return df

def clean_data(df):
    """Performs basic data cleaning."""
    # Copy to avoid SettingWithCopyWarning
    df = df.copy()
    
    # TotalCharges is often object type due to empty strings
    if df['TotalCharges'].dtype == 'object':
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # Fill missing values for TotalCharges with 0 or median
    df['TotalCharges'] = df['TotalCharges'].fillna(0)
    
    # Convert SeniorCitizen to object for consistency if needed, or keep as int
    # df['SeniorCitizen'] = df['SeniorCitizen'].astype(str)
    
    # No other missing values expected in the standard dataset, but good to check
    # df = df.dropna()
    
    return df

def preprocess_for_model(df):
    """Preprocesses data for the model (encoding, etc)."""
    # This might be handled by the model pipeline, but we can do some here
    # Drop customerID as it's not predictive
    if 'customerID' in df.columns:
        df = df.drop('customerID', axis=1)
    
    return df
