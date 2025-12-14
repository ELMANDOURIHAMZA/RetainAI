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
- [Utilisation](#-utilisation)
- [Structure du Projet](#-structure-du-projet)
- [API Documentation](#-api-documentation)
- [Modèles ML](#-modèles-ml)
- [Contribution](#-contribution)
└── .gitignore                  # Fichiers à ignorer Git
```

---

## 🤝 Contribution
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
