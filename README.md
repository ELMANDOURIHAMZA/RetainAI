# 🎯 RetainAI - Plateforme de Prédiction et Rétention Client

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![pandas](https://img.shields.io/badge/pandas-1.3+-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)](#)

**Auteur:** HAMZA EL MANDOURI | **Version:** 1.0.0

</div>

---

## 📋 Table des matières

- [À propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture Technique](#-architecture-technique)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du Projet](#-structure-du-projet)
- [API Documentation](#-api-documentation)
- [Modèles ML](#-modèles-ml)
- [Dépannage](#-dépannage)
- [Contribution](#-contribution)
- [Licence](#-licence)

---

## 🎯 À propos

**RetainAI** est une plateforme intelligente de rétention client basée sur le Machine Learning et l'IA générative. Elle aide les entreprises B2B à :

- 🔍 **Identifier** les clients à risque de churn avec précision
- 📊 **Analyser** les patterns de désabonnement via des KPIs avancés
- ⚡ **Automatiser** les campagnes de rétention personnalisées
- 📈 **Optimiser** la valeur client à long terme

L'outil combine des techniques de ML classiques (Random Forest, Logistic Regression) avec des capacités d'IA générative pour créer des stratégies de rétention data-driven.

---

## ✨ Fonctionnalités Principales

### 🔮 Prédiction de Churn
- **Modèle Random Forest** entraîné sur données télécommunications
- Prédiction individualisée pour chaque client
- Score de probabilité de désabonnement (0-100%)
- Explainabilité des prédictions

### 📊 Dashboard Analytique
- **KPIs en temps réel** : churn rate, revenue at risk, lifetime value
- **Segmentation** : risque élevé, moyen, faible
- **Analyse de survie** : courbes Kaplan-Meier
- **Heatmaps** et visualisations interactives (Chart.js)

### 🤖 Campagnes de Rétention
- Génération d'emails personnalisés via API LLM
- Templates adaptatifs selon le segment client
- Historique des actions et suivi des conversions
- Gestion des campagnes multi-canaux

### 🔌 Connecteurs de Données
- Import CSV avec validation
- Connexions SQL (PostgreSQL, MySQL)
- APIs tierces (CRM, ERP)
- Synchronisation planifiée

### 🛡️ Authentification & Sécurité
- Système d'authentification multi-niveaux
- Reset de mot de passe par email
- Rôles utilisateurs (Admin, Analyst, Viewer)
- Protection CSRF et validation entrées

### 📈 MLOps & Monitoring
- Suivi performance du modèle
- Détection de drift de données
- Logs d'entraînement détaillés
- Versioning des modèles

---

## 🛠️ Architecture Technique

### Backend
```
Framework     : Flask 2.0+
ORM           : SQLAlchemy
Authentication: Flask-Login, Flask-Bcrypt
Email         : Flask-Mail
```

### Data Science
```
ML            : scikit-learn (Random Forest, Logistic Regression)
Data          : Pandas, NumPy, SciPy
Visualisation : Matplotlib, Seaborn (backend)
Statistiques  : Kaplan-Meier Estimator
```

### Frontend
```
Template      : Jinja2
Styling       : TailwindCSS
JS Framework  : Alpine.js, HTMX
Graphiques    : Chart.js
```

### Database
```
Développement : SQLite
Production    : PostgreSQL
Migrations    : Flask-Migrate
```

---

## 📦 Installation

### Prérequis
- **Python 3.9+** (3.11 recommandé)
- **Git**
- **pip** (gestionnaire de paquets Python)
- Optionnel : **PostgreSQL** pour production

### 1️⃣ Cloner le repository

```bash
git clone https://github.com/ELMANDOURIHAMZA/RetainAI.git
cd RetainAI
```

### 2️⃣ Créer un environnement virtuel

**Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux :**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

**Verification :**
```bash
pip list
```

### 4️⃣ Configuration de l'environnement

Créer un fichier `.env` à la racine :

```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///app.db
```

### 5️⃣ Initialiser la base de données

```bash
# Générer les données de démo
python seed_data.py

# Créer les tables
python
>>> from app import create_app
>>> app = create_app()
>>> with app.app_context():
...     from app.models import db
...     db.create_all()
>>> exit()
```

### 6️⃣ Entraîner le modèle ML (optionnel)

```bash
python model_generator.py
```

### 7️⃣ Lancer l'application

```bash
python run.py
```

L'application est accessible à : **http://localhost:5000**

---

## 🚀 Utilisation

### Identifiants de Démonstration
```
Email    : admin@retainai.com
Password : admin
```

### Flux Principal
1. **Login** → Authentification utilisateur
2. **Dashboard** → Vue d'ensemble des KPIs
3. **Clients** → Liste et détails des clients avec score churn
4. **Modèles** → Performance et métriques ML
5. **Campagnes** → Création et suivi des actions
6. **Paramètres** → Configuration utilisateur

### Cas d'Usage Principaux

#### 📊 Analyser le Churn
```
Dashboard → Voir le churn rate global
Clients → Trier par "Churn Score" décroissant
Survival → Visualiser la courbe Kaplan-Meier
```

#### 🎯 Créer une Campagne
```
Campagnes → "Nouvelle Campagne"
Sélectionner segment (ex: risque > 70%)
Générer emails via IA
Valider et lancer
```

#### 📈 Évaluer le Modèle
```
MLOps → Voir les métriques d'entraînement
Confusion Matrix, ROC-AUC, Precision-Recall
Déterminer si réentraînement nécessaire
```

---

## 📂 Structure du Projet

```
RetainAI/
│
├── app/                          # Application principale
│   ├── __init__.py              # Factory pattern Flask
│   ├── models.py                # Modèles SQLAlchemy (User, Client, Campaign...)
│   │
│   ├── blueprints/              # Modules Flask (séparation des routes)
│   │   ├── auth.py              # Login, Register, Logout, Password Reset
│   │   └── dashboard.py         # Routes du dashboard (Dashboard, Clients, Modèles, etc.)
│   │
│   ├── services/                # Logique métier (découplée des routes)
│   │   ├── ml_service.py        # Prédictions, entraînement modèles
│   │   ├── ai_service.py        # Génération contenu via LLM
│   │   ├── data_service.py      # Gestion données (import, nettoyage)
│   │   └── llm_service.py       # Intégration APIs LLM (OpenAI, etc.)
│   │
│   ├── static/                  # Assets statiques
│   │   ├── css/
│   │   │   └── style.css        # Styles TailwindCSS
│   │   ├── js/
│   │   │   └── main.js          # Scripts Alpine.js et HTMX
│   │   └── uploads/             # Fichiers uploadés (CSV, etc.)
│   │
│   └── templates/               # Fichiers Jinja2
│       ├── layouts/
│       │   └── base.html        # Template de base (header, nav, footer)
│       ├── auth/
│       │   ├── login.html
│       │   ├── register.html
│       │   ├── forgot_password.html
│       │   └── reset_password.html
│       └── dashboard/
│           ├── index.html       # Dashboard principal
│           ├── clients.html     # Liste clients avec scores
│           ├── models.html      # Performance ML
│           ├── campaigns.html   # Gestion campagnes
│           ├── survival.html    # Analyse de survie
│           ├── connectors.html  # Connecteurs données
│           ├── mlops.html       # Monitoring modèle
│           ├── settings.html    # Préférences utilisateur
│           ├── profile.html     # Profil utilisateur
│           └── partials/        # Composants réutilisables (notifications, etc.)
│
├── models/                      # Modèles ML entraînés
│   ├── model_metadata.json      # Métadonnées (version, date, scores)
│   └── model.pkl               # Modèle Random Forest sérialisé
│
├── data/                        # Données brutes
│   └── Telco-Customer-Churn.csv # Dataset d'entraînement
│
├── config.py                    # Configuration (Dev, Prod, Test)
├── run.py                       # Point d'entrée principal
├── app.py                       # Fichier principal Flask
├── seed_data.py                 # Génération données de démo
├── model_generator.py           # Script entraînement modèle
├── trigger_training.py          # API pour réentraînement
├── list_models.py              # Utilitaire lister modèles
├── requirements.txt            # Dépendances Python
└── .gitignore                  # Fichiers à ignorer Git
```

---

## 🔗 API Documentation

### Authentification

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "admin@retainai.com",
  "password": "admin"
}

Response 200:
{
  "message": "Login successful",
  "user_id": 1,
  "email": "admin@retainai.com"
}
```

#### Register
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "confirm_password": "secure_password"
}
```

### Dashboard

#### Récupérer les KPIs
```http
GET /dashboard/kpis

Response 200:
{
  "total_clients": 7043,
  "churn_rate": 26.5,
  "at_risk_count": 1837,
  "avg_churn_score": 42.3,
  "lifetime_value": 2547.89
}
```

#### Lister les clients
```http
GET /dashboard/clients?sort=churn_score&order=desc&limit=50

Response 200:
{
  "clients": [
    {
      "id": 123,
      "name": "John Doe",
      "email": "john@example.com",
      "churn_score": 0.87,
      "lifetime_value": 1250.50,
      "contract_type": "month-to-month"
    }
  ],
  "total": 7043
}
```

### Campagnes

#### Créer une campagne
```http
POST /dashboard/campaigns
Content-Type: application/json

{
  "name": "Retention Q4 2024",
  "segment_filter": {"churn_score_min": 0.7},
  "email_template": "retention_v1",
  "scheduled_at": "2024-12-15T10:00:00"
}
```

---

## 🤖 Modèles ML

### Pipeline d'Entraînement

```
1. Ingestion (CSV)
   ↓
2. Nettoyage & Preprocessing
   - Imputations valeurs manquantes
   - Encodage variables catégoriques
   - Normalisation features numériques
   ↓
3. Feature Engineering
   - Dérivation nouvelles variables
   - Sélection features (SelectKBest)
   ↓
4. Entraînement modèles
   - Random Forest (modèle principal)
   - Logistic Regression (baseline)
   - Evaluation K-Fold cross-validation
   ↓
5. Tuning Hyperparamètres
   - GridSearchCV
   ↓
6. Évaluation finale
   - Confusion Matrix
   - ROC-AUC, Precision-Recall
   - Calibration courbes
   ↓
7. Sauvegarde (pickle)
```

### Performances Actuelles

| Métrique | Valeur |
|----------|--------|
| Accuracy | 81.4% |
| ROC-AUC | 0.845 |
| Precision (Churn) | 0.743 |
| Recall (Churn) | 0.692 |
| F1-Score | 0.716 |

### Features Principales

1. **Tenure** : Ancienneté client (mois)
2. **Monthly Charges** : Frais mensuels
3. **Total Charges** : Total dépensé
4. **Contract Type** : Type contrat (mois, 1an, 2ans)
5. **Internet Service** : Service internet (DSL, Fiber, None)
6. **Online Security** : Service sécurité online
7. **Tech Support** : Support technique
8. **Streaming Services** : Services streaming

### Réentraîner le Modèle

```bash
# Réentraîner localement
python model_generator.py

# Via API
curl -X POST http://localhost:5000/api/trigger-training \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## ⚙️ Configuration Avancée

### Variables d'Environnement

```env
# Flask
FLASK_APP=app.py
FLASK_ENV=development|production
FLASK_DEBUG=0|1
SECRET_KEY=generate-with-secrets.token_hex(32)

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/retainai

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# LLM API
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# Security
JWT_SECRET_KEY=generate-with-secrets.token_hex(32)
JWT_ALGORITHM=HS256
SESSION_TIMEOUT=3600
```

### Fichier config.py

```python
class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', 3600))
```

---

## 🆘 Dépannage

### Problème : "ModuleNotFoundError: No module named 'flask'"
**Solution :**
```bash
pip install -r requirements.txt
# Vérifier activation venv
which python  # macOS/Linux
where python  # Windows
```

### Problème : "DatabaseError: No such table"
**Solution :**
```bash
# Recréer la base
rm app.db
python seed_data.py
```

### Problème : "Email not sent"
**Solution :**
1. Vérifier variables `MAIL_*` dans `.env`
2. Utiliser "App Password" pour Gmail
3. Vérifier configuration SMTP en logs

### Problème : Modèle ne prédit pas correctement
**Solution :**
1. Vérifier données d'entraînement (distribution)
2. Réentraîner : `python model_generator.py`
3. Consulter `models/model_metadata.json` pour métriques

### Logs Utiles
```bash
# Logs Flask
tail -f logs/app.log

# Debug mode
export FLASK_DEBUG=1
python run.py
```

---

## 🤝 Contribution

Les contributions sont bienvenues ! Pour contribuer :

1. **Fork** le repository
2. **Créer une branche** : `git checkout -b feature/ma-fonctionnalite`
3. **Commit** : `git commit -m "Add feature: ..."`
4. **Push** : `git push origin feature/ma-fonctionnalite`
5. **Pull Request** : Décrire les changements

### Standards de Code
- Utiliser **PEP 8** pour Python
- Ajouter des **docstrings** aux fonctions
- Couvrir avec des **tests unitaires**
- Formatter avec **Black**

---

## 📚 Ressources & Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [TailwindCSS](https://tailwindcss.com/)

Voir aussi : [DOCUMENTATION_TECHNIQUE.md](DOCUMENTATION_TECHNIQUE.md) et [GUIDE_UTILISATEUR.md](GUIDE_UTILISATEUR.md)

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir [LICENSE](LICENSE) pour plus de détails.

---

## 👨‍💻 Auteur

**HAMZA EL MANDOURI**

- 📧 Email : hamza.elmandouri@example.com
- 💼 LinkedIn : [LinkedIn Profile]
- 🐙 GitHub : [@ELMANDOURIHAMZA](https://github.com/ELMANDOURIHAMZA)
- 📱 Portfolio : [Votre Portfolio]

---

## 🙏 Remerciements

Merci à toutes les librairies open-source utilisées dans ce projet :
- Flask Team
- scikit-learn Contributors
- Pandas Team
- Tailwind Labs

---

<div align="center">

**⭐ Si ce projet vous a été utile, n'hésitez pas à le star sur GitHub !**

Made with ❤️ by HAMZA EL MANDOURI

</div>
