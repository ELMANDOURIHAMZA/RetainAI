import os
import openai

def draft_retention_email(customer_name, risk_score, shap_reasons):
    """
    Generates a retention email using OpenAI API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Mock response if no key
    if not api_key:
        return f"""Objet : Parlons de votre abonnement

Bonjour {customer_name},

J'espère que vous allez bien.

Je remarquais que votre contrat arrive à une étape clé. Nous tenons beaucoup à votre fidélité.
Concernant vos charges mensuelles, nous avons de nouvelles offres qui pourraient vous intéresser.

Seriez-vous disponible pour un court échange ?

Cordialement,
Votre Responsable Client"""

    client = openai.OpenAI(api_key=api_key)
    
    reasons_text = ", ".join(shap_reasons)
    
    prompt = f"""
    Tu es un expert en succès client (Customer Success Manager) empathique et professionnel.
    Contexte : Le client {customer_name} est identifié comme "À Risque Élevé" (Score : {risk_score*100:.1f}%).
    Diagnostic (Basé sur les données) : {reasons_text}.
    
    Tâche : Rédige un email de rétention court (max 150 mots).
    Stratégie :
    - Ne mentionne pas explicitement "nos algorithmes ont vu que...".
    - Au lieu de cela, demande proactivement si tout va bien concernant les points identifiés.
    - Propose une solution spécifique.
    - Ton : Serviable, humain, non intrusif.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erreur lors de la génération : {str(e)}"
