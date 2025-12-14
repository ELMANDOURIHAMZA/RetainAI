import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = 'data/churn_history.db'

def init_db():
    """Initializes the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            customer_data TEXT,
            churn_probability REAL,
            risk_level TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_prediction(customer_data, probability, risk_level):
    """Saves a prediction to the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Convert customer data to string representation for simplicity
    # In a real app, you'd have columns for each feature
    data_str = str(customer_data)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('''
        INSERT INTO predictions (date, customer_data, churn_probability, risk_level)
        VALUES (?, ?, ?, ?)
    ''', (date_str, data_str, probability, risk_level))
    
    conn.commit()
    conn.close()

def get_history():
    """Retrieves prediction history."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM predictions ORDER BY date DESC", conn)
    conn.close()
    return df
