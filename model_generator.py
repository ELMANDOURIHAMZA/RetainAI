import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

MODEL_PATH = 'model.pkl'

def generate_and_train():
    print("Génération du dataset synthétique...")
    np.random.seed(42)
    n_samples = 1000
    
    # Features: CreditScore, Age, EstimatedSalary, Tenure
    data = {
        'CreditScore': np.random.randint(350, 850, n_samples),
        'Age': np.random.randint(18, 92, n_samples),
        'EstimatedSalary': np.random.uniform(20000, 150000, n_samples),
        'Tenure': np.random.randint(0, 10, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Target: Churn (Synthetic logic)
    # Higher age, lower credit score, lower tenure -> higher churn risk
    def churn_logic(row):
        score = 0
        if row['CreditScore'] < 500: score += 3
        if row['Age'] > 50: score += 2
        if row['Tenure'] < 2: score += 2
        if row['EstimatedSalary'] < 40000: score += 1
        
        # Random noise
        prob = (score / 8) + np.random.normal(0, 0.1)
        return 1 if prob > 0.5 else 0

    df['Churn'] = df.apply(churn_logic, axis=1)
    
    print("Entraînement du modèle RandomForest...")
    X = df.drop('Churn', axis=1)
    y = df['Churn']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print(f"Score du modèle: {model.score(X_test, y_test):.2f}")
    
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Modèle sauvegardé sous {MODEL_PATH}")

if __name__ == "__main__":
    generate_and_train()
