# Projet ETL - Nettoyage de Données de Ventes

Ce document présente un pipeline ETL développé pour nettoyer et transformer des données de ventes contenant de nombreuses anomalies.

## Présentation du Projet

Le fichier CSV d'origine contient plusieurs types d'erreurs : valeurs manquantes, enregistrements dupliqués, et valeurs incohérentes. 

L'objectif est de nettoyer ces données pour obtenir un ensemble exploitable et fiable pour l'analyse.

## Traitements Appliqués

### 1. Chargement des Données

Le fichier CSV est chargé avec la bibliothèque pandas. Un aperçu initial est effectué avec `df.head()` pour visualiser la structure des données.

### 2. Analyse des Problèmes

L'analyse a révélé plusieurs anomalies :
- **Valeurs manquantes** : absence de noms de produits, de prix ou de quantités pour certains enregistrements
- **Doublons** : enregistrements de ventes identiques apparaissant plusieurs fois
- **Valeurs incohérentes** : quantités vendues égales à 0, ce qui est illogique

### 3. Suppression des Doublons

La méthode `drop_duplicates()` est utilisée pour éliminer les lignes en double. 

Une validation est ensuite effectuée pour confirmer l'absence de doublons dans le jeu de données.

### 4. Traitement des Valeurs Manquantes

Les lignes contenant des valeurs manquantes sont supprimées avec `dropna()`.

*Note : Le pipeline complet propose des stratégies alternatives pour minimiser la perte de données.*

### 5. Détection et Suppression des Valeurs Aberrantes

La méthode IQR (Interquartile Range) est appliquée pour détecter statistiquement les valeurs aberrantes :
- Calcul des quartiles Q1 et Q3 pour les colonnes `Quantite_vendue` et `Prix_unitaire`
- Définition des bornes : `[Q1 - 1.5×IQR, Q3 + 1.5×IQR]`
- Suppression des valeurs situées en dehors de ces bornes

Cette approche statistique détecte automatiquement les anomalies sans intervention manuelle.

### 6. Transformations des Données

#### Transformation 1 : Ajout d'une Colonne Calculée
Création de la colonne `Montant_total` :
```python
Montant_total = Quantite_vendue × Prix_unitaire
```

Cette colonne permet d'analyser directement le chiffre d'affaires par vente.

#### Transformation 2 : Agrégation par Produit
Calcul de statistiques regroupées par produit :
- Total des quantités vendues
- Montant total généré
- Nombre de ventes

Les résultats sont sauvegardés dans `statistiques_produits.csv`.

### 7. Gestion des Erreurs

Des blocs try-except sont implémentés sur toutes les opérations critiques. Les erreurs sont enregistrées dans `pipeline.log` pour faciliter le débogage, et le programme continue son exécution malgré les erreurs non bloquantes.

### 8. Validation Croisée

Après chaque traitement, une validation est effectuée pour vérifier :
- Le nombre de lignes restantes
- L'absence de valeurs manquantes
- L'absence de doublons

Toutes ces informations sont enregistrées dans les logs.

## Utilisation

### Version de Base (Code Original)

```bash
python transform.py
```

Cette commande exécute le nettoyage de base.

### Version Complète (Avec Toutes les Fonctionnalités)

Pour utiliser le pipeline complet, modifier le fichier `transform.py` à la ligne 96 :

```python
# Commenter cette ligne :
# df_propre = transformer_donnees()

# Décommenter celle-ci :
df_propre = pipeline_complet()
```

Puis exécuter :
```bash
python transform.py
```

### Exécution des Tests

```bash
python test_transform.py
```

Cette commande lance 4 tests automatiques pour valider le bon fonctionnement du pipeline.

## Fichiers Générés

Après l'exécution, les fichiers suivants sont créés :

- **donnees_nettoyees.csv** : données nettoyées et enrichies
- **statistiques_produits.csv** : agrégations par produit
- **pipeline.log** : journal détaillé des opérations

## Tests Implémentés

Quatre tests automatiques vérifient :
1. L'exécution du pipeline sans erreur ✓
2. La création des fichiers de sortie ✓
3. L'absence de valeurs manquantes dans les résultats ✓
4. L'absence de doublons ✓

## Résultats

Les résultats du traitement :
- **Avant** : 66 lignes contenant de nombreux doublons et erreurs
- **Après** : 49 lignes nettoyées et exploitables

Les lignes invalides ont été supprimées, conservant uniquement les données fiables.

## Structure du Projet

- `transform.py` - Script principal du pipeline ETL
- `test_transform.py` - Suite de tests automatiques
- `jeux_de_données.csv` - Données sources (non modifiées)
- `pipeline.log` - Fichier de journalisation
- `README.md` - Cette documentation

## Points Importants

- Le code original est **conservé intact** avec ajout de nouvelles fonctions
- Les nouvelles fonctionnalités sont regroupées dans `pipeline_complet()`
- Il est possible de basculer entre les deux versions facilement
- Le code est commenté pour faciliter la compréhension

---

**Auteurs** : Valentin PROVOST & Bastien RABANE
**Date** : Mars 2026
