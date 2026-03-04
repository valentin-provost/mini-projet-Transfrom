import pandas as pd
import logging

# Configuration du logging (journalisation des erreurs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

def transformer_donnees():
    fichier_csv = 'jeux_de_données.csv'
    df = pd.read_csv(fichier_csv, sep=',')

    print(df.head())

    print(df.isnull().sum())

    nb_doublons = df.duplicated().sum()
    print(nb_doublons)
    
    df = df.drop_duplicates()

    df = df.dropna()
    
    print(f"Taille finale du jeu de données : {df.shape[0]} lignes et {df.shape[1]} colonnes.")

    print(df.head())

    return df


# ===== NOUVELLES FONCTIONNALITÉS AJOUTÉES =====

def valider_donnees(df, etape):
    """Validation croisée : vérifie la qualité après chaque traitement"""
    logging.info(f"--- Validation après {etape} ---")
    logging.info(f"Lignes: {len(df)}, Valeurs manquantes: {df.isnull().sum().sum()}, Doublons: {df.duplicated().sum()}")


def traiter_valeurs_aberrantes(df):
    """Supprime les valeurs aberrantes avec la méthode IQR (Interquartile Range)"""
    try:
        logging.info("--- Traitement des valeurs aberrantes (méthode IQR) ---")
        taille_avant = len(df)
        
        for col in ['Quantite_vendue', 'Prix_unitaire']:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            borne_inf = Q1 - 1.5 * IQR
            borne_sup = Q3 + 1.5 * IQR
            
            df = df[(df[col] >= borne_inf) & (df[col] <= borne_sup)]
        
        taille_apres = len(df)
        logging.info(f"✓ {taille_avant - taille_apres} valeurs aberrantes supprimées")
        
        return df
    except Exception as e:
        logging.error(f"Erreur traitement aberrantes: {e}")
        return df


def appliquer_transformations(df):
    """Applique 2 transformations : ajout colonnes + agrégation"""
    try:
        # Transformation 1 : Ajout de colonne Montant_total
        df['Montant_total'] = df['Quantite_vendue'] * df['Prix_unitaire']
        logging.info("✓ Colonne Montant_total ajoutée")
        
        # Transformation 2 : Agrégation par produit
        stats = df.groupby('Nom_produit').agg({
            'Quantite_vendue': 'sum',
            'Montant_total': 'sum'
        })
        stats.to_csv('statistiques_produits.csv')
        logging.info("✓ Statistiques produits sauvegardées")
        
        return df
    except Exception as e:
        logging.error(f"Erreur transformations: {e}")
        return df


def pipeline_complet():
    """Pipeline ETL avec gestion d'erreurs et validation"""
    try:
        logging.info("=== DÉMARRAGE PIPELINE ETL ===")
        
        # Extraction
        df = pd.read_csv('jeux_de_données.csv')
        logging.info(f"✓ Données chargées: {len(df)} lignes")
        
        # Nettoyage doublons
        df = df.drop_duplicates()
        valider_donnees(df, "suppression doublons")
        
        # Nettoyage valeurs manquantes
        df = df.dropna()
        valider_donnees(df, "suppression valeurs manquantes")
        
        # Traitement des valeurs aberrantes
        df = traiter_valeurs_aberrantes(df)
        valider_donnees(df, "traitement valeurs aberrantes")
        
        # Transformations
        df = appliquer_transformations(df)
        valider_donnees(df, "transformations")
        
        # Sauvegarde
        df.to_csv('donnees_nettoyees.csv', index=False)
        logging.info("✓ Données sauvegardées: donnees_nettoyees.csv")
        
        logging.info("=== PIPELINE TERMINÉ ===")
        return df
        
    except FileNotFoundError:
        logging.error("Fichier non trouvé")
        return None
    except Exception as e:
        logging.error(f"Erreur pipeline: {e}")
        return None


if __name__ == "__main__":
    # Choix: utiliser la fonction originale ou le pipeline complet
    
    # Version originale
    df_propre = transformer_donnees()
    
    # OU version avec nouvelles fonctionnalités (décommenter pour utiliser)
    # df_propre = pipeline_complet()