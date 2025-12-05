"""
Script pour télécharger le dataset Kaggle pour la détection de troubles du visage
"""
import kagglehub
import os
import shutil
from pathlib import Path

def download_face_trouble_dataset():
    """Télécharge le dataset Kaggle pour la détection de troubles du visage"""
    try:
        print("📥 Téléchargement du dataset Kaggle...")
        
        # Download latest version
        kaggle_path = kagglehub.dataset_download("safabenammor/datasetam")
        
        print(f"✅ Dataset téléchargé avec succès depuis Kaggle!")
        print(f"📁 Chemin Kaggle: {kaggle_path}")
        
        # Chemin de destination dans le projet
        data_raw_path = Path(__file__).parent.parent.parent / "data" / "raw" / "face_trouble_dataset"
        data_raw_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Si le chemin Kaggle est différent, copier les fichiers
        if str(kaggle_path) != str(data_raw_path):
            if data_raw_path.exists():
                print(f"⚠️  Le dossier {data_raw_path} existe déjà")
                print(f"💡 Suppression de l'ancien dossier...")
                if data_raw_path.is_symlink():
                    data_raw_path.unlink()
                else:
                    shutil.rmtree(data_raw_path)
            
            # Copier le contenu du dataset Kaggle vers data/raw
            print(f"📋 Copie des fichiers vers {data_raw_path}...")
            shutil.copytree(kaggle_path, data_raw_path)
            print(f"✅ Fichiers copiés avec succès!")
        
        print(f"📁 Chemin final du dataset: {data_raw_path}")
        return str(data_raw_path)
        
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement du dataset: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    download_face_trouble_dataset()

