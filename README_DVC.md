# 📦 Configuration DVC pour Skin-Twin-AI

## 📋 Vue d'ensemble

Ce projet utilise DVC (Data Version Control) pour gérer les datasets et modèles de machine learning.

## 🔧 Configuration des données

### 1. Dataset Kaggle - Détection de troubles du visage

Le dataset est téléchargé automatiquement depuis Kaggle via `kagglehub` :

```python
import kagglehub
path = kagglehub.dataset_download("safabenammor/datasetam")
```

**Chemin DVC** : `data/raw/face_trouble_dataset`

**Script** : `mlops/data/download_kaggle_dataset.py`

### 2. Données XGBoost

Le fichier CSV pour le modèle XGBoost est copié depuis :

**Source** : `C:\Users\Mohamed\Downloads\changement\fusion_features_wiki.csv`

**Destination DVC** : `data/raw/fusion_features_wiki.csv`

**Script** : `mlops/data/setup_xgboost_data.py`

**Note** : Vous pouvez modifier le chemin source en définissant la variable d'environnement :
```bash
export XGBOOST_CSV_PATH="/chemin/vers/fusion_features_wiki.csv"
```

## 🚀 Utilisation

### Télécharger les données

```bash
# Télécharger le dataset Kaggle
dvc repro download_kaggle_dataset

# Configurer les données XGBoost
dvc repro setup_xgboost_data

# Ou exécuter les scripts directement
python mlops/data/download_kaggle_dataset.py
python mlops/data/setup_xgboost_data.py
```

### Pipeline complet

```bash
# Exécuter tout le pipeline DVC
dvc repro

# Ou étape par étape
dvc repro download_kaggle_dataset
dvc repro setup_xgboost_data
dvc repro prepare_data
dvc repro train
```

## 📁 Structure des données

```
data/
├── raw/
│   ├── face_trouble_dataset/     # Dataset Kaggle (téléchargé)
│   └── fusion_features_wiki.csv  # Données XGBoost (copié)
└── processed/                    # Données préprocessées
```

## 🔐 Configuration Kaggle

Pour utiliser `kagglehub`, vous devez configurer vos credentials Kaggle :

1. Créer un compte Kaggle
2. Télécharger votre fichier `kaggle.json` depuis les paramètres de votre compte
3. Le placer dans `~/.kaggle/kaggle.json` (Linux/Mac) ou `C:\Users\<username>\.kaggle\kaggle.json` (Windows)

Ou utiliser les variables d'environnement :
```bash
export KAGGLE_USERNAME="votre_username"
export KAGGLE_KEY="votre_api_key="votre_api_key"
```

## 📝 Notes

- Les stages `download_kaggle_dataset` et `setup_xgboost_data` ont `always_changed: true` car ils dépendent de sources externes
- Les fichiers sont versionnés avec DVC dans `dvc_storage/`
- Utilisez `dvc pull` pour récupérer les données versionnées
- Utilisez `dvc push` pour pousser les données vers le remote

