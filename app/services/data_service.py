import pandas as pd
from app.models import db, Customer
import random

def process_csv(file_stream):
    """
    Ingests a CSV file and updates the Customer table.
    """
    try:
        df = pd.read_csv(file_stream)
        
        # Basic cleaning
        if 'TotalCharges' in df.columns:
             df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
        
        count = 0
        for _, row in df.iterrows():
            # Upsert logic
            cust_id = str(row.get('customerID', f"UNK-{random.randint(1000,9999)}"))
            
            customer = Customer.query.filter_by(customer_id_str=cust_id).first()
            if not customer:
                customer = Customer(customer_id_str=cust_id)
                db.session.add(customer)
            
            customer.tenure = int(row.get('tenure', 0))
            customer.monthly_charges = float(row.get('MonthlyCharges', 0.0))
            customer.total_charges = float(row.get('TotalCharges', 0.0))
            customer.contract_type = row.get('Contract', 'Month-to-month')
            
            count += 1
        
        db.session.commit()
        return count, None
    except Exception as e:
        db.session.rollback()
        return 0, str(e)

def generate_mock_data(n=50):
    """Generates mock data if no CSV is present."""
    for i in range(n):
        cust_id = f"C-{1000+i}"
        if not Customer.query.filter_by(customer_id_str=cust_id).first():
            c = Customer(
                customer_id_str=cust_id,
                tenure=random.randint(1, 72),
                monthly_charges=random.uniform(20, 120),
                total_charges=random.uniform(100, 8000),
                contract_type=random.choice(['Month-to-month', 'One year', 'Two year']),
                churn_score=random.random() # Random score for demo
            )
            # Mock SHAP
            if c.churn_score > 0.5:
                c.shap_factors = {
                    "reasons": [
                        "Prix mensuel élevé (+45%)",
                        "Faible ancienneté (+20%)"
                    ]
                }
            db.session.add(c)
    db.session.commit()
