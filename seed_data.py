import pandas as pd
import numpy as np
from app import create_app
from app.models import db, Tenant, User, Customer, Subscription
import uuid
import os

def generate_synthetic_csv():
    # Deprecated: We use the real dataset now
    pass

def seed_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # 1. Create Tenant
        tenant = Tenant.query.filter_by(name="Demo Corp").first()
        if not tenant:
            tenant = Tenant(name="Demo Corp", api_key="demo-key-123")
            db.session.add(tenant)
            db.session.commit()
            print("Tenant 'Demo Corp' créé.")
            
        # 2. Create Admin User
        user = User.query.filter_by(email="admin@demo.com").first()
        if not user:
            user = User(tenant_id=tenant.id, email="admin@demo.com", role="admin")
            user.set_password("admin123")
            db.session.add(user)
            db.session.commit()
            print("User Admin créé.")
        else:
            # Update password for existing user to ensure it works with new auth system
            user.set_password("admin123")
            db.session.commit()
            print("Mot de passe Admin mis à jour.")

        # 3. Clear existing data
        print("Nettoyage des anciennes données...")
        try:
            num_subs = db.session.query(Subscription).delete()
            num_cust = db.session.query(Customer).delete()
            db.session.commit()
            print(f"Supprimé: {num_cust} clients, {num_subs} abonnements.")
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors du nettoyage: {e}")

        # 4. Ingest CSV
        if not os.path.exists('Telco-Customer-Churn.csv'):
            print("ERREUR: Le fichier 'Telco-Customer-Churn.csv' est manquant.")
            return
            
        df = pd.read_csv('Telco-Customer-Churn.csv')
        
        import random
        from datetime import datetime, timedelta
        from app.models import RiskHistory

        count = 0
        for _, row in df.iterrows():
            # Check if exists
            if Customer.query.filter_by(external_id=row['customerID']).first():
                continue
            
            # Persona Logic (Simplified)
            persona = "Standard"
            if float(row['MonthlyCharges']) > 90:
                persona = "Premium / Exigeant"
            elif row['Contract'] == "Month-to-month":
                persona = "Volatile / Sensible au Prix"
            elif row['TechSupport'] == "No":
                persona = "Frustré Technique"
            elif int(row['tenure']) > 48:
                persona = "Fidèle / Ambassadeur"

            cust = Customer(
                tenant_id=tenant.id,
                external_id=row['customerID'],
                gender=row['gender'],
                senior_citizen=bool(row['SeniorCitizen']),
                partner=True if row['Partner'] == 'Yes' else False,
                dependents=True if row['Dependents'] == 'Yes' else False,
                churn_label=True if row['Churn'] == 'Yes' else False,
                persona=persona,
                ab_test_group=random.choice(['A', 'B'])
            )
            db.session.add(cust)
            db.session.flush() # Get ID
            
            sub = Subscription(
                customer_id=cust.id,
                phone_service=True if row['PhoneService'] == 'Yes' else False,
                multiple_lines=True if row['MultipleLines'] == 'Yes' else False,
                internet_service=row['InternetService'],
                online_security=True if row['OnlineSecurity'] == 'Yes' else False,
                device_protection=True if row['DeviceProtection'] == 'Yes' else False,
                tech_support=True if row['TechSupport'] == 'Yes' else False,
                streaming_tv=True if row['StreamingTV'] == 'Yes' else False,
                streaming_movies=True if row['StreamingMovies'] == 'Yes' else False,
                contract=row['Contract'],
                paperless_billing=True if row['PaperlessBilling'] == 'Yes' else False,
                payment_method=row['PaymentMethod'],
                monthly_charges=float(row['MonthlyCharges']),
                total_charges=float(row['TotalCharges']) if row['TotalCharges'] != ' ' else 0.0,
                tenure=int(row['tenure'])
            )
            db.session.add(sub)

            # Generate Mock Risk History (Last 6 months)
            base_risk = 0.8 if cust.churn_label else 0.2
            for i in range(6):
                # Risk fluctuates slightly
                risk = base_risk + random.uniform(-0.1, 0.1)
                risk = max(0.0, min(1.0, risk))
                
                history = RiskHistory(
                    customer_id=cust.id,
                    risk_score=risk,
                    recorded_at=datetime.utcnow() - timedelta(days=30 * (5-i))
                )
                db.session.add(history)

            count += 1
            
        db.session.commit()
        print(f"{count} clients importés avec historique et personas.")

if __name__ == "__main__":
    seed_database()
