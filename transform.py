import pandas as pd

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

if __name__ == "__main__":
    df_propre = transformer_donnees()