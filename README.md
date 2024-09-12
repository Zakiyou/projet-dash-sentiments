

## Description du Projet

Ce projet se compose de deux parties principales : une analyse des sentiments réalisée dans un Jupyter Notebook et un tableau de bord interactif créé avec Dash pour visualiser les résultats de cette analyse.

### Partie 1 : Analyse avec Jupyter Notebook

**Objectif :**
- Nettoyer et classer les commentaires en sentiments positifs, négatifs et neutres.
- Effectuer une analyse descriptive des données avant classification.

**Étapes réalisées :**
1. **Installation des bibliothèques nécessaires :**
   - `textblob_fr` pour l'analyse des sentiments en français.
   - `nltk` pour la tokenisation des textes.
   - `spacy` pour la gestion des mots vides et des expressions en français.
   - `matplotlib` pour la visualisation des données.

2. **Chargement et Nettoyage des Données :**
   - Suppression des colonnes inutiles.
   - Conversion des commentaires en minuscules.
   - Suppression des lignes contenant des commentaires vides.
   - Tokenisation et filtrage des commentaires pour enlever les mots vides.

3. **Classification des Commentaires :**
   - Utilisation de `textblob` pour classer les commentaires en sentiments positifs, négatifs ou neutres.
   - Ajout des résultats de classification dans les données.

4. **Visualisation :**
   - Création de graphiques pour visualiser le nombre de commentaires par année et par insurance.
   - Utilisation de `seaborn` et `matplotlib` pour les graphiques et annotations.

**Packages requis :**
- `textblob_fr`
- `nltk`
- `spacy`
- `plotly`
- `matplotlib`
- `seaborn`

### Partie 2 : Tableau de Bord Interactif avec Dash

**Objectif :**
- Créer un tableau de bord interactif pour visualiser les statistiques et les sentiments des commentaires.

**Fonctionnalités :**
1. **Statistiques :**
   - Total des commentaires de façon général et total par insurance.
   - Répartition des commentaires par insurance et par année.
   - Répartition des sentiments par insurance.

2. **Visualisation Interactives :**
   - Graphiques pour le nombre de commentaires par année et par insurance.
   - Graphiques pour la distribution des sentiments par insurance.

3. **Interface :**
   - Utilisation de `dash` et `dash_bootstrap_components` pour le design du tableau de bord.
   - Onglets pour naviguer entre l'accueil, les commentaires et les sentiments.
   - Pagination pour les cartes affichant les statistiques.

**Packages requis :**
- `dash`
- `dash_bootstrap_components`
- `pandas`
- `plotly`


## Installation

pip install -r requirements.txt

Le fichier `requirements.txt` doit contenir les bibliothèques suivantes :

textblob_fr

nltk

spacy

plotly

matplotlib

seaborn

dash

dash_bootstrap_components

pandas
