# 🚀 ChurnGuard AI : Plateforme de Rétention Client Prédictive

> **Transformez vos données en stratégies de fidélisation grâce à l'Intelligence Artificielle.**

---

## 1. 🎯 Vision du Projet
**ChurnGuard AI** (commercialisé sous le nom *RetainAI*) est une solution SaaS B2B conçue pour aider les entreprises à anticiper et réduire le taux d'attrition (churn) de leurs clients. 

Contrairement aux outils d'analytique traditionnels qui ne font que *constater* les départs, ChurnGuard AI utilise le **Machine Learning** pour *prédire* quels clients sont à risque et l'**IA Générative** pour proposer des actions correctives immédiates et personnalisées.

---

## 2. 💡 Problématique & Solution

### Le Problème
*   Acquérir un nouveau client coûte **5 à 25 fois plus cher** que de fidéliser un client existant.
*   Les entreprises réagissent souvent trop tard, une fois que le client a déjà résilié.
*   Les données clients sont dispersées (CRM, ERP, Support) et sous-exploitées.

### La Solution ChurnGuard AI
Une plateforme unifiée qui :
1.  **Centralise** les données (ETL Connectors).
2.  **Analyse** les comportements pour détecter les signaux faibles de départ (ML Random Forest).
3.  **Agit** en générant des campagnes de rétention ciblées (GenAI).
4.  **Surveille** la performance des modèles dans le temps (MLOps).

---

## 3. ✨ Fonctionnalités Clés

### 📊 Dashboard Exécutif
*   **KPIs Temps Réel** : Taux de churn global, Revenu à risque, CLV (Customer Lifetime Value).
*   **Visualisation** : Graphiques interactifs de la répartition des risques.

### 🧠 Prédiction & Scoring (Le Cœur du Système)
*   **Scoring Individuel** : Chaque client reçoit un score de risque (0-100%) et un label (Actif / Risque Élevé).
*   **Segmentation IA** : Identification automatique des "Personas" (ex: "Sensible au Prix", "Tech Reliant").
*   **Facteurs Explicatifs** : Transparence sur *pourquoi* un client est à risque (ex: "Facture en hausse", "Appels support fréquents").

### ⚡ Actions de Rétention (GenAI)
*   **Génération d'Emails** : Rédaction automatique d'emails de reconquête personnalisés via LLM, adaptés au profil du client.
*   **Campagnes Marketing** : Gestion de campagnes multi-canaux (Email, SMS) avec suivi du ROI et des clients sauvés.

### 📈 Analytique Avancée
*   **Analyse de Survie** : Courbes de Kaplan-Meier pour identifier les "moments de vérité" (ex: décrochage massif au 14ème mois).
*   **Comparaison de Cohortes** : Analyse Fibre vs ADSL, ou par type de contrat.

### 🛠️ MLOps & Data Engineering
*   **Data Connectors** : Ingestion fluide depuis CSV, SQL Server, Salesforce.
*   **Monitoring de Modèle** : Détection de "Data Drift" (dérive des données) et alertes de performance.
*   **Ré-entraînement** : Pipeline automatisé pour maintenir la précision du modèle.

---

## 4. 🏗️ Architecture Technique

Le projet repose sur une stack moderne, robuste et évolutive :

*   **Backend** : Python (Flask) - Pour sa flexibilité et son écosystème Data Science riche.
*   **Base de Données** : SQLAlchemy (ORM) avec SQLite (Dev) / PostgreSQL (Prod).
*   **Frontend** : 
    *   **HTML5 / Tailwind CSS** : Pour un design moderne, responsive et "Pixel Perfect".
    *   **Alpine.js & HTMX** : Pour une interactivité dynamique sans la lourdeur d'un framework SPA (React/Vue).
    *   **Chart.js** : Pour les visualisations de données avancées.
*   **Intelligence Artificielle** :
    *   **Scikit-Learn** : Algorithmes de classification (Random Forest, XGBoost).
    *   **Pandas/Numpy** : Manipulation et traitement des données.
    *   **OpenAI API (Optionnel)** : Pour la génération de contenu textuel.

---

## 5. 📱 Flux Utilisateur (User Journey)

1.  **Connexion** : L'analyste se connecte au portail sécurisé.
2.  **Observation** : Il remarque une alerte sur le Dashboard (ex: "Pic de risque détecté sur le segment Fibre").
3.  **Investigation** : Il navigue vers la page **Clients**, filtre par "Risque Élevé" et "Fibre".
4.  **Analyse** : Il consulte la fiche d'un client critique, voit les facteurs de risque (ex: "3 appels au support ce mois-ci").
5.  **Action** : Il clique sur "Générer Email". L'IA propose une offre de remise. Il valide et l'envoie.
6.  **Suivi** : Dans la page **Campagnes**, il suit le taux d'ouverture et voit que le client est repassé en statut "Retained".

---

## 6. 💼 Impact Business & ROI

L'utilisation de ChurnGuard AI permet de :
*   **Réduire le Churn** de 15% à 30% dès la première année.
*   **Augmenter la CLV** (Customer Lifetime Value) en prolongeant la durée de vie des clients.
*   **Optimiser les Coûts** en ciblant uniquement les clients qui ont besoin d'une intervention (pas de remises inutiles).
*   **Gagner du Temps** grâce l'automatisation des tâches d'analyse et de rédaction.

---

> *ChurnGuard AI n'est pas seulement un outil de prédiction, c'est un moteur de croissance durable pour votre entreprise.*
