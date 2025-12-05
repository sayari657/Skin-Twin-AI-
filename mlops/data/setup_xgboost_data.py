"""
Script pour configurer les données XGBoost
"""
import shutil
import os
from pathlib import Path

def setup_xgboost_data(source_path=None):
    """Copie le fichier CSV XGBoost vers le dossier data"""
    # Chemin par défaut (peut être modifié via variable d'environnement)
    if source_path is None:
        source_path = os.getenv(
            'XGBOOST_CSV_PATH',
            r"C:\Users\Mohamed\Downloads\changement\fusion_features_wiki.csv"
        )
    
    source_path = Path(source_path)
    target_path = Path(__file__).parent.parent.parent / "data" / "raw" / "fusion_features_wiki.csv"
    
    # Créer le dossier de destination si nécessaire
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    if source_path.exists():
        try:
            shutil.copy2(source_path, target_path)
            print(f"✅ Fichier CSV copié avec succès!")
            print(f"📁 Source: {source_path}")
            print(f"📁 Destination: {target_path}")
            return str(target_path)
        except Exception as e:
            print(f"❌ Erreur lors de la copie: {str(e)}")
            raise
    else:
        print(f"⚠️  Le fichier source n'existe pas: {source_path}")
        print(f"💡 Veuillez vérifier le chemin et réessayer")
        print(f"💡 Vous pouvez définir la variable d'environnement XGBOOST_CSV_PATH")
        return None

if __name__ == "__main__":
    import sys
    source = sys.argv[1] if len(sys.argv) > 1 else None
    setup_xgboost_data(source)

