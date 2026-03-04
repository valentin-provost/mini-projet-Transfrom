"""
Tests simples pour valider le pipeline ETL
"""
import pandas as pd
from transform import pipeline_complet, valider_donnees

def test_pipeline():
    """Test du pipeline complet"""
    print("=== TEST DU PIPELINE ===")
    
    # Test 1: Le pipeline s'exécute sans erreur
    try:
        df = pipeline_complet()
        if df is not None:
            print("✓ Test 1 RÉUSSI: Pipeline exécuté sans erreur")
        else:
            print("✗ Test 1 ÉCHOUÉ: Pipeline retourne None")
    except Exception as e:
        print(f"✗ Test 1 ÉCHOUÉ: {e}")
    
    # Test 2: Le fichier de sortie existe
    try:
        df_clean = pd.read_csv('donnees_nettoyees.csv')
        print(f"✓ Test 2 RÉUSSI: Fichier créé avec {len(df_clean)} lignes")
    except:
        print("✗ Test 2 ÉCHOUÉ: Fichier non créé")
    
    # Test 3: Pas de valeurs manquantes dans le résultat
    try:
        if df_clean.isnull().sum().sum() == 0:
            print("✓ Test 3 RÉUSSI: Aucune valeur manquante")
        else:
            print("✗ Test 3 ÉCHOUÉ: Valeurs manquantes présentes")
    except:
        print("✗ Test 3 ÉCHOUÉ: Impossible de vérifier")
    
    # Test 4: Pas de doublons
    try:
        if df_clean.duplicated().sum() == 0:
            print("✓ Test 4 RÉUSSI: Aucun doublon")
        else:
            print("✗ Test 4 ÉCHOUÉ: Doublons présents")
    except:
        print("✗ Test 4 ÉCHOUÉ: Impossible de vérifier")
    
    print("\n=== TESTS TERMINÉS ===")

if __name__ == "__main__":
    test_pipeline()
