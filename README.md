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
## RetainAI — Récapitulatif Professionnel

**Auteur :** HAMZA EL MANDOURI

---

## Résumé (pour recruteurs)

RetainAI est une application web full-stack développée en Python/Flask, conçue pour aider les entreprises à identifier les clients à risque de churn et à piloter des actions de rétention. Le projet montre des compétences en :

- Développement backend (API et architecture Flask)
- Intégration de pipelines ML simples (préprocessing, entraînement, sérialisation)
- Conception d'interfaces et visualisations (Jinja2, Chart.js)
- Pratiques de MLOps et gestion de modèles
- Gestion de projet et documentation technique

Ce repository est un bon exemple pour un profil de Data Analyst / Junior Python Developer cherchant à démontrer capacité à produire une solution complète de bout en bout.

---

## Points forts à mettre en avant dans un CV / entretien

- Architecture claire et découplée (`app/`, `services/`, `models/`).
- Pipeline de données et modèle Random Forest reproductible.
- Visualisations interactives dans le dashboard pour KPI et segmentation.
- Utilisation de bonnes pratiques : modularité, fichiers de configuration et scripts utilitaires.
- Livraison prête à être dockerisée ou déployée sur un PaaS.

---

## Stack technique

- Langage : Python 3.9+
- Framework : Flask
- Data : Pandas, NumPy, scikit-learn
- DB : SQLite (dev) / PostgreSQL (prod)
- Frontend : Jinja2, TailwindCSS, Chart.js, Alpine.js
- Tests / Qualité : (prévoir pytest, flake8, black)

---

## Fichiers & dossiers clés

- `app/` — Application Flask (routes, blueprints, services)
- `models/` — Modèles ML et métadonnées
- `data/` — Jeu de données (ex : Telco-Customer-Churn.csv)
- `model_generator.py` — Script d'entraînement
- `seed_data.py` — Script pour données de démonstration
- `run.py` / `app.py` — Entrées de l'application
- `requirements.txt` — Dépendances

---

## Comment présenter ce projet à un recruteur

1. Contexte : expliquer le problème business (churn) et l'impact financier possible.
2. Votre rôle : lister les tâches réalisées (ex : nettoyage, feature engineering, entraînement, déploiement minimal).
3. Résultats : mentionner métriques (ROC-AUC / précision) si disponibles et actions produites (emails, segments).
4. Améliorations possibles : monitoring, tests, CI/CD, déploiement dockerisé, baselines supplémentaires.

---

## Licence

Ce projet est distribué sous licence MIT. Voir `LICENSE` pour détails.

---

## Auteur

**HAMZA EL MANDOURI** — hamza.elmandouri@example.com — https://github.com/ELMANDOURIHAMZA

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
