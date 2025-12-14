import pandas as pd
import numpy as np
import random

def generate_telco_data(n_samples=7000):
    np.random.seed(42)
    random.seed(42)

    data = {
        'customerID': [f'{random.randint(1000,9999)}-{random.choice(["A","B","C"])}{random.randint(100,999)}' for _ in range(n_samples)],
        'gender': np.random.choice(['Male', 'Female'], n_samples),
        'SeniorCitizen': np.random.choice([0, 1], n_samples, p=[0.84, 0.16]),
        'Partner': np.random.choice(['Yes', 'No'], n_samples),
        'Dependents': np.random.choice(['Yes', 'No'], n_samples),
        'tenure': np.random.randint(0, 73, n_samples),
        'PhoneService': np.random.choice(['Yes', 'No'], n_samples, p=[0.9, 0.1]),
        'MultipleLines': np.random.choice(['Yes', 'No', 'No phone service'], n_samples),
        'InternetService': np.random.choice(['DSL', 'Fiber optic', 'No'], n_samples),
        'OnlineSecurity': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'OnlineBackup': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'DeviceProtection': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'TechSupport': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'StreamingTV': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'StreamingMovies': np.random.choice(['Yes', 'No', 'No internet service'], n_samples),
        'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_samples),
        'PaperlessBilling': np.random.choice(['Yes', 'No'], n_samples),
        'PaymentMethod': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], n_samples),
        'MonthlyCharges': np.round(np.random.uniform(18.25, 118.75, n_samples), 2),
    }

    # TotalCharges is roughly tenure * MonthlyCharges
    data['TotalCharges'] = np.round(data['tenure'] * data['MonthlyCharges'] + np.random.uniform(0, 10, n_samples), 2)
    
    # Introduce some correlation for Churn
    df = pd.DataFrame(data)
    
    def get_churn_prob(row):
        prob = 0.2
        if row['Contract'] == 'Month-to-month': prob += 0.4
        if row['InternetService'] == 'Fiber optic': prob += 0.2
        if row['tenure'] < 12: prob += 0.2
        if row['PaymentMethod'] == 'Electronic check': prob += 0.1
        if row['TechSupport'] == 'No': prob += 0.1
        return min(prob, 0.95)

    churn_probs = df.apply(get_churn_prob, axis=1)
    df['Churn'] = [np.random.choice(['Yes', 'No'], p=[p, 1-p]) for p in churn_probs]

    return df

if __name__ == "__main__":
    df = generate_telco_data()
    df.to_csv('data/telco_churn.csv', index=False)
    print("Synthetic data generated at data/telco_churn.csv")
