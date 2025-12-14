import openai

def generate_retention_email(customer_name, churn_factors, api_key, model="gpt-3.5-turbo"):
    """Generates a retention email using OpenAI API."""
    
    if not api_key:
        return "Veuillez entrer une clé API OpenAI pour générer l'email."
    
    client = openai.OpenAI(api_key=api_key)
    
    factors_text = "\n".join([f"- {factor}" for factor in churn_factors])
    
    prompt = f"""
    Tu es un expert en marketing et relation client. Rédige un email de rétention personnalisé pour un client nommé "{customer_name}".
    
    Le client risque de partir pour les raisons suivantes :
    {factors_text}
    
    L'email doit être :
    1. Empathique et professionnel.
    2. Proposer une solution ou une offre concrète liée aux problèmes identifiés (invente une offre réaliste, ex: réduction, rendez-vous technique).
    3. Court et percutant.
    
    Sujet de l'email : [Génère un sujet accrocheur]
    Corps de l'email :
    """
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Tu es un assistant marketing utile."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erreur lors de la génération : {str(e)}"
