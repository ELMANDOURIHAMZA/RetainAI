import google.generativeai as genai
import os

def generate_churn_insight(customer_data):
    """
    Generates insights using Google Gemini Pro.
    """
    # Hardcoded key as requested by user
    api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyCT7BuxHeo0DryjWBQbp7-NxQe7_xu_kFE")
    
    if not api_key:
        return {
            "explanation": "Clé API Google manquante. Configuration requise.",
            "email": "Veuillez configurer la clé API pour générer l'email."
        }

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        Tu es un expert senior en rétention client pour une entreprise de télécommunications.
        
        Analyse le profil client suivant :
        - Ancienneté : {customer_data['tenure']} mois
        - Contrat : {customer_data['contract']}
        - Charges Mensuelles : ${customer_data['monthly_charges']}
        - Internet : {customer_data['internet_service']}
        - Support Technique : {'Oui' if customer_data['tech_support'] else 'Non'}
        - Probabilité de Churn calculée : {customer_data['churn_prob']}%
        
        Tâche 1 : Explique en 2 phrases pourquoi ce client est à risque.
        Tâche 2 : Rédige un email court et empathique proposant une offre spécifique pour le retenir.
        
        Format de réponse attendu (JSON pur sans markdown) :
        {{
            "explanation": "...",
            "email": "..."
        }}
        """
        
        response = model.generate_content(prompt)
        
        # Simple parsing
        import json
        text = response.text.replace('```json', '').replace('```', '')
        return json.loads(text)
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        # Fallback Logic (Smart Simulation)
        tenure = customer_data['tenure']
        contract = customer_data['contract']
        monthly = customer_data['monthly_charges']
        churn_prob = customer_data['churn_prob']
        
        # 1. Dynamic Explanation
        reasons = []
        if contract == "Month-to-month": reasons.append("son contrat mensuel sans engagement")
        if monthly > 80: reasons.append(f"ses factures élevées (${monthly}/mois)")
        if tenure < 6: reasons.append("sa faible ancienneté")
        if not customer_data['tech_support']: reasons.append("l'absence de support technique")
        
        reason_str = " et ".join(reasons[:2]) if reasons else "son profil de consommation"
        fallback_explanation = f"Risque de {churn_prob}% identifié. Le client est volatile principalement à cause de {reason_str}."

        # 2. Dynamic Email
        subject = "Une offre spéciale pour vous !"
        intro = "Bonjour,"
        
        if tenure > 24:
            intro = f"Bonjour,\n\nCela fait déjà {tenure} mois que vous nous faites confiance, et nous vous en remercions sincèrement."
            offer = "Pour vous remercier de votre fidélité, nous vous offrons 2 mois d'abonnement gratuits si vous prolongez votre aventure avec nous."
        elif monthly > 90:
            intro = "Bonjour,\n\nNous savons que vos factures récentes ont été élevées."
            offer = "Nous pouvons réduire votre facture mensuelle de 20% dès le mois prochain en optimisant votre forfait."
        else:
            intro = "Bonjour,\n\nNous espérons que vous appréciez nos services."
            offer = "Nous avons une offre exclusive : profitez de l'option 'Support Premium' offerte pendant 6 mois."

        fallback_email = f"""Objet : {subject}

{intro}

{offer}

N'hésitez pas à nous contacter pour activer cet avantage.

Cordialement,
L'équipe Service Client"""

        return {
            "explanation": fallback_explanation,
            "email": fallback_email
        }
