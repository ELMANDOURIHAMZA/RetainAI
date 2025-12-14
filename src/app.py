from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
import json
import plotly
import plotly.express as px
from utils.data_loader import load_data, clean_data
from utils.model_trainer import train_model, save_model, load_model
from utils.llm_helper import generate_retention_email
from utils.db_manager import init_db, save_prediction, get_history
import shap

app = Flask(__name__)

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize DB
if not os.path.exists('data/churn_history.db'):
    init_db()

# Load demo data if available
def get_demo_data():
    if os.path.exists('data/telco_churn.csv'):
        return load_data('data/telco_churn.csv')
    return None

@app.route('/')
def dashboard():
    df = get_demo_data()
    stats = {}
    graphs = {}
    
    if df is not None:
        # KPIs
        churn_rate = df['Churn'].value_counts(normalize=True).get('Yes', 0) * 100
        avg_charges = df['MonthlyCharges'].mean()
        total_customers = len(df)
        risk_count = int(total_customers * churn_rate/100)
        
        stats = {
            'churn_rate': round(churn_rate, 1),
            'avg_charges': round(avg_charges, 2),
            'total_customers': total_customers,
            'risk_count': risk_count
        }
        
        # Graphs
        # 1. Churn Distribution
        fig_churn = px.pie(df, names='Churn', hole=0.4, color_discrete_sequence=['#4CAF50', '#FF5252'])
        graphs['churn_dist'] = json.dumps(fig_churn, cls=plotly.utils.PlotlyJSONEncoder)
        
        # 2. Contract vs Churn
        fig_contract = px.histogram(df, x='Contract', color='Churn', barmode='group', color_discrete_sequence=['#4CAF50', '#FF5252'])
        graphs['contract'] = json.dumps(fig_contract, cls=plotly.utils.PlotlyJSONEncoder)
        
    return render_template('dashboard.html', stats=stats, graphs=graphs)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})
            
        try:
            new_data = pd.read_csv(file)
            if os.path.exists('models/churn_model.pkl'):
                model = load_model()
                processed_data = clean_data(new_data)
                
                probs = model.predict_proba(processed_data)[:, 1]
                new_data['Churn_Probability'] = probs
                new_data['Risk_Level'] = pd.cut(probs, bins=[0, 0.3, 0.7, 1.0], labels=['Faible', 'Moyen', 'Élevé'])
                
                # Save to DB (limit to 50 for performance)
                for i, row in new_data.head(50).iterrows():
                    save_prediction(row.to_dict(), row['Churn_Probability'], row['Risk_Level'])
                
                return jsonify({
                    'success': True,
                    'data': new_data.head(20).to_dict(orient='records')
                })
            else:
                return jsonify({'error': 'Model not trained'})
        except Exception as e:
            return jsonify({'error': str(e)})
            
    return render_template('predict.html')

@app.route('/train', methods=['POST'])
def train():
    df = get_demo_data()
    if df is not None:
        try:
            model, auc, report, _, _ = train_model(clean_data(df))
            save_model(model)
            return jsonify({'success': True, 'auc': auc, 'report': report})
        except Exception as e:
            return jsonify({'error': str(e)})
    return jsonify({'error': 'No data available'})

@app.route('/explain')
def explain():
    df = get_demo_data()
    customers = []
    if df is not None:
        customers = df.head(100).to_dict(orient='records')
        # Add index to dict for selection
        for idx, c in enumerate(customers):
            c['index'] = idx
            
    return render_template('explain.html', customers=customers)

@app.route('/api/explain/<int:customer_idx>')
def api_explain(customer_idx):
    df = get_demo_data()
    if df is not None and os.path.exists('models/churn_model.pkl'):
        try:
            model = load_model()
            X = clean_data(df).drop('Churn', axis=1)
            
            preprocessor = model.named_steps['preprocessor']
            classifier = model.named_steps['classifier']
            
            row = X.iloc[[customer_idx]]
            row_transformed = preprocessor.transform(row)
            
            explainer = shap.TreeExplainer(classifier)
            shap_values = explainer.shap_values(row_transformed)
            
            # Get feature names (simplified)
            # In a real scenario, we'd map these back to original features
            feature_names = [f"Feature {i}" for i in range(shap_values[0].shape[0])]
            
            return jsonify({
                'base_value': float(explainer.expected_value),
                'values': shap_values[0].tolist(),
                'feature_names': feature_names
            })
        except Exception as e:
            return jsonify({'error': str(e)})
    return jsonify({'error': 'Model or data missing'})

@app.route('/retention', methods=['GET', 'POST'])
def retention():
    if request.method == 'POST':
        data = request.json
        email = generate_retention_email(
            data.get('name'), 
            data.get('reasons'), 
            data.get('api_key')
        )
        return jsonify({'email': email})
    return render_template('retention.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
