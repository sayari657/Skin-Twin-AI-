"""
Script de vérification pour le package "model skin"
Vérifie que tous les fichiers nécessaires sont présents
"""

import os
import sys

# Fix encoding pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def verify_package():
    """Vérifie que le package est complet"""
    print("="*60)
    print("🔍 VÉRIFICATION DU PACKAGE 'model skin'")
    print("="*60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Fichiers requis
    required_files = {
        "skin_diagnostic.py": "Module Python principal",
        "requirements.txt": "Dépendances Python",
        "models/modéle skinTwin2 .pt": "Modèle YOLO",
        "models/modele_peau.pth": "Modèle EfficientNet",
        "models/Modelefusion_preproc.joblib": "Preprocessing",
        "models/context_correction_xgb.joblib": "Modèle XGBoost",
        "models/context_correction_label_encoder.joblib": "Label Encoder"
    }
    
    all_ok = True
    print("\n📋 Vérification des fichiers...\n")
    
    for file_path, description in required_files.items():
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            size_mb = size / (1024 * 1024)
            print(f"✅ {description:35s} : {file_path:50s} ({size_mb:.2f} MB)")
        else:
            print(f"❌ {description:35s} : {file_path:50s} - MANQUANT!")
            all_ok = False
    
    print("\n" + "="*60)
    if all_ok:
        print("✅ TOUS LES FICHIERS SONT PRÉSENTS!")
        print("✅ Le package est complet et prêt à être utilisé!")
        print("\n💡 Prochaine étape:")
        print("   1. Copiez ce dossier dans votre projet")
        print("   2. Installez les dépendances: pip install -r requirements.txt")
        print("   3. Utilisez: from skin_diagnostic import SkinDiagnostic")
    else:
        print("❌ CERTAINS FICHIERS MANQUENT!")
        print("❌ Le package est incomplet!")
    
    print("="*60)
    return all_ok

if __name__ == "__main__":
    verify_package()

