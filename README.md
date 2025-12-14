# RetainAI

RetainAI est une application web visant à analyser et prédire le churn client, avec un dashboard métier, des scripts d'entraînement ML et des utilities pour importer et traiter des données.

---

## Fonctionnalités

- Scores de churn individuels (Random Forest)
- Dashboard de KPIs et segmentation
- Import CSV et préprocessing basique
- Scripts d'entraînement et de seed data
- Export et versioning simple des modèles

---

## Stack technique

- Python 3.9+
- Flask
- pandas / numpy
- scikit-learn
- SQLite (dev) / PostgreSQL (prod)
- Jinja2, TailwindCSS, Chart.js

---

## Démarrage rapide

1. Cloner le dépôt :

```bash
git clone https://github.com/ELMANDOURIHAMZA/RetainAI.git
cd RetainAI
```

2. (Optionnel) Créer et activer un environnement virtuel :

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. (Optionnel) Générer des données de démonstration :

```bash
python seed_data.py
```

5. Lancer l'application :

```bash
python run.py
```

L'application sera disponible sur `http://localhost:5000`.

---

## Structure principale

- `app/` — application Flask (routes, blueprints, services)
- `models/` — modèles ML et métadonnées
- `data/` — jeux de données (ex : Telco-Customer-Churn.csv)
- `model_generator.py` — script d'entraînement
- `seed_data.py` — génération de données de démonstration
- `run.py` / `app.py` — points d'entrée
- `requirements.txt` — dépendances

---

## Contribution

Les contributions sont bienvenues : ouvrez une issue ou une pull request. Respectez PEP8 et préférez des commits clairs et tests simples pour les nouveaux modules.

---

## Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE`.

---

## Auteur

HAMZA EL MANDOURI — https://github.com/ELMANDOURIHAMZA

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
