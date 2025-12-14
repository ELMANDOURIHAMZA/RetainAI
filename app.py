from flask import Flask, render_template, request
import pickle
import numpy as np
import os
from model_generator import generate_and_train
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
try:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model_gemini = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Warning: Failed to initialize Gemini: {e}")
    model_gemini = None

app = Flask(__name__)

# Check for model on startup
if not os.path.exists('model.pkl'):
    generate_and_train()

def load_model():
    with open('model.pkl', 'rb') as f:
        return pickle.load(f)

model = load_model()

@app.route('/')
def dashboard():
    # Simulated KPIs for the dashboard
    kpis = {
        'churn_rate': 15.4,
        'revenue_at_risk': 125000,
        'avg_satisfaction': 4.2
    }
    
    # Simulated data for the chart (Age distribution of churners vs non-churners)
    chart_data = {
        'labels': ['18-25', '26-35', '36-45', '46-60', '60+'],
        'churners': [5, 15, 25, 40, 15],
        'non_churners': [10, 30, 35, 20, 5]
    }
    
    return render_template('dashboard.html', kpis=kpis, chart_data=chart_data)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get data from form
        credit_score = float(request.form['credit_score'])
        age = float(request.form['age'])
        salary = float(request.form['salary'])
        tenure = float(request.form['tenure'])
        
        # Predict
        features = np.array([[credit_score, age, salary, tenure]])
        probability = model.predict_proba(features)[0][1]
        churn_prob_percent = round(probability * 100, 1)
        
    # AI Explanation and Email Generation using Gemini
        try:
            prompt = f"""
            Agis comme un expert en rétention client.
            Un client a les caractéristiques suivantes :
            - Score de crédit : {credit_score}
            - Âge : {age}
            - Salaire estimé : {salary}
            - Ancienneté : {tenure} ans
            
            La probabilité de churn (départ) est de {churn_prob_percent}%.
            
            Tâche 1 : Explique brièvement pourquoi ce client est à risque ou non (en français).
            Tâche 2 : Rédige un email de rétention personnalisé (en français) offrant 20% de réduction.
            
            Sépare la Tâche 1 et la Tâche 2 par la chaîne "|||".
            """
            
            response = model_gemini.generate_content(prompt)
            parts = response.text.split("|||")
            explanation = parts[0].strip()
            email_draft = parts[1].strip() if len(parts) > 1 else "Erreur lors de la génération de l'email."
            
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            # Fallback (Simulated logic)
            explanation = "Le risque est faible."
            if churn_prob_percent > 50:
                reasons = []
                if credit_score < 600: reasons.append("Score de crédit bas")
                if age > 50: reasons.append("Âge élevé")
                if tenure < 3: reasons.append("Faible fidélité")
                explanation = f"Risque élevé détecté principalement dû à : {', '.join(reasons)}."
            
            email_draft = f"""Objet : Une offre spéciale pour vous !

Bonjour,

Nous avons remarqué que vous êtes un client précieux et nous souhaitons vous remercier pour votre fidélité.
Pour vous accompagner, nous avons le plaisir de vous offrir 20% de réduction sur votre prochain abonnement.

N'hésitez pas à nous contacter pour en discuter.

Cordialement,
L'équipe Service Client"""

        return render_template('result.html', 
                               prob=churn_prob_percent, 
                               explanation=explanation, 
                               email=email_draft)
                               
    return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
