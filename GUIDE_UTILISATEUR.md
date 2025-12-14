# 📖 Guide Utilisateur - ChurnGuard AI

Bienvenue sur **ChurnGuard AI** (RetainAI). Ce guide vous accompagnera dans l'utilisation de la plateforme pour réduire le taux de désabonnement de vos clients.

---

## 1. Vue d'Ensemble (Dashboard)

Dès votre connexion, vous accédez au **Tableau de Bord**. C'est votre tour de contrôle.

*   **KPIs en haut** :
    *   **Taux de Churn Prédit** : Le pourcentage de votre base client à risque ce mois-ci.
    *   **Revenu à Risque** : La somme des factures mensuelles des clients à risque.
    *   **Clients Sauvés** : Nombre de clients retenus grâce à vos actions récentes.
*   **Graphiques** : Visualisez la répartition des risques par type de contrat ou méthode de paiement.
*   **Actions Rapides** : Boutons pour lancer une analyse ou voir les alertes récentes.

---

## 2. Gestion des Clients

Rendez-vous dans l'onglet **"Clients"** via le menu latéral.

### Filtrer et Rechercher
*   Utilisez la barre de recherche pour trouver un client par son ID ou Nom.
*   **Filtres Intelligents** : Cliquez sur "Risque Élevé" pour ne voir que les clients prioritaires (Probabilité > 50%).
*   **Tri** : Triez par "Probabilité de Churn (Décroissant)" pour traiter les cas les plus urgents en premier.

### Fiche Client
Cliquez sur un client pour voir son profil détaillé :
*   **Score de Risque** : Une jauge colorée (Vert/Orange/Rouge).
*   **Facteurs Clés** : Pourquoi ce score ? (ex: "Contrat mensuel", "Pas de support technique").
*   **Historique** : Ses dernières interactions et factures.

---

## 3. Lancer une Campagne de Rétention

Une fois les clients à risque identifiés, agissez !

1.  Sélectionnez un ou plusieurs clients dans la liste (cases à cocher).
2.  Cliquez sur le bouton **"Actions"** > **"Envoyer Email de Rétention"**.
3.  **Génération IA** : Une fenêtre s'ouvre avec un brouillon d'email généré par l'IA, adapté au profil du client (ex: offre de fibre optique pour un gros consommateur de données).
4.  **Personnalisation** : Vous pouvez modifier le texte si nécessaire.
5.  **Envoi** : Validez l'envoi. Le statut du client passera à "Contacté".

---

## 4. Analyse de Survie

L'onglet **"Survie"** vous permet de comprendre le cycle de vie à long terme.

*   **Courbe de Kaplan-Meier** : Observez à quel mois précis vos clients ont tendance à partir (ex: chute brutale au 12ème mois).
*   **Comparaison** : Comparez la courbe des clients "Fibre" vs "ADSL" pour voir quel produit fidélise le mieux.
*   **Décision** : Utilisez ces infos pour placer vos offres de fidélité *juste avant* les mois critiques.

---

## 5. Monitoring MLOps

Réservé aux profils techniques, l'onglet **"MLOps"** assure la fiabilité de l'IA.

*   **Précision du Modèle** : Vérifiez que la courbe de précision reste au-dessus de 75%. Si elle baisse, cliquez sur **"Ré-entraîner le modèle"**.
*   **Data Drift** : Surveillez si le profil de vos clients change (ex: arrivée massive de clients plus jeunes), ce qui pourrait fausser les prédictions.

---

## 6. Paramètres

Dans **"Paramètres"**, configurez l'application selon vos besoins :
*   **Seuil de Risque** : Définissez à partir de quel pourcentage (ex: 60%) un client est considéré "À Risque".
*   **API Keys** : Renseignez votre clé OpenAI pour activer la génération d'emails.
*   **Utilisateurs** : Invitez vos collègues analystes.

---

## Besoin d'aide ?
Contactez le support technique via l'icône "?" en bas du menu ou écrivez à `support@retainai.com`.
