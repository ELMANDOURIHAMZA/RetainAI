# 🛡️ ChurnGuard AI (RetainAI)

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000.svg?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**ChurnGuard AI** est une plateforme SaaS B2B de rétention client prédictive. Elle utilise l'apprentissage automatique (Machine Learning) pour identifier les clients à risque de désabonnement (churn) et l'IA générative pour automatiser les actions de fidélisation.

---

## 🚀 Fonctionnalités Principales

- **🔮 Prédiction de Churn** : Algorithme Random Forest pour scorer la probabilité de départ de chaque client.
- **📊 Dashboard Analytique** : KPIs en temps réel, segmentation des risques et analyse de survie (Kaplan-Meier).
- **⚡ Actions Automatisées** : Génération d'emails de rétention personnalisés via IA et gestion de campagnes.
- **🔌 Data Connectors** : Ingestion de données depuis CSV, SQL, et APIs tierces.
- **🛠️ MLOps Monitoring** : Surveillance de la performance du modèle et détection de dérive (Drift).

---

## 🛠️ Stack Technique

- **Backend** : Python, Flask, SQLAlchemy.
- **Frontend** : HTML5, TailwindCSS, Alpine.js, HTMX, Chart.js.
- **Data Science** : Pandas, Scikit-learn, Numpy.
- **Base de Données** : SQLite (Développement) / PostgreSQL (Production).

---

## 📦 Installation & Démarrage

### Prérequis
- Python 3.9 ou supérieur
- Git

### 1. Cloner le projet
```bash
git clone https://github.com/votre-username/churnguard-ai.git
cd churnguard-ai
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Initialiser la Base de Données
Le projet inclut un script de "seeding" pour générer des données de démonstration.
```bash
python seed_data.py
```

### 5. Lancer l'application
```bash
python run.py
```
Accédez à l'application sur : `http://localhost:5000`

**Identifiants de démo :**
- Email : `admin@retainai.com`
- Mot de passe : `admin`

---

## 📂 Structure du Projet

```
ChurnGuard AI/
├── app/
│   ├── blueprints/      # Routes et contrôleurs (Dashboard, Auth, API)
│   ├── services/        # Logique métier (AI, ML, Email)
│   ├── static/          # Assets (CSS, JS, Images)
│   ├── templates/       # Vues HTML (Jinja2)
│   └── models.py        # Modèles de base de données
├── models/              # Fichiers .pkl des modèles entraînés
├── migrations/          # Scripts de migration BDD
├── config.py            # Configuration de l'application
├── run.py               # Point d'entrée
└── requirements.txt     # Dépendances Python
```

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Veuillez lire `CONTRIBUTING.md` pour les détails sur notre code de conduite et le processus de soumission de pull requests.

---

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
