from app import create_app
from app.services.ml_service import train_model
from app.models import Tenant

app = create_app()
with app.app_context():
    tenant = Tenant.query.first()
    if tenant:
        print(f"Entraînement pour le tenant: {tenant.name}")
        success, message = train_model(tenant.id)
        print(f"Résultat: {message}")
    else:
        print("Erreur: Aucun tenant trouvé.")
