"""
Module de Diagnostic Dermatologique - Réutilisable
===================================================

Ce module permet d'utiliser les modèles de diagnostic dermatologique dans n'importe quel projet Python.

Usage:
    from skin_diagnostic import SkinDiagnostic
    
    # Initialiser le système
    diagnostic = SkinDiagnostic(models_dir="models")
    
    # Analyser une image
    result = diagnostic.analyze_image("path/to/image.jpg", user_info={...})
"""

import os
import numpy as np
import pandas as pd
import joblib
import torch
import torch.nn.functional as F
import cv2
from PIL import Image
from ultralytics import YOLO
import torchvision.transforms as transforms
from torchvision.models import efficientnet_b0
from typing import Dict, List, Optional, Tuple


class SkinDiagnostic:
    """
    Classe principale pour le diagnostic dermatologique.
    Charge et utilise tous les modèles nécessaires.
    """
    
    # Labels des troubles de peau
    TROUBLE_LABELS = [
        'Acne', 'Blackheads', 'Dark-Spots', 'Dry-Skin', 'Englarged-Pores',
        'Eyebags', 'Oily-Skin', 'Skin-Redness', 'Whiteheads', 'Wrinkles'
    ]
    
    # Labels des types de peau
    SKIN_LABELS = {0: "Dry", 1: "Normal", 2: "Oily"}
    
    def __init__(self, models_dir: str = "models", device: Optional[str] = None):
        """
        Initialise le système de diagnostic.
        
        Args:
            models_dir: Chemin vers le dossier contenant les modèles
            device: Device PyTorch ('cuda' ou 'cpu'). Si None, détecte automatiquement.
        """
        self.models_dir = models_dir
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        # Chemins des modèles
        self.yolo_path = os.path.join(models_dir, "modéle skinTwin2 .pt")
        self.effnet_path = os.path.join(models_dir, "modele_peau.pth")
        self.preproc_path = os.path.join(models_dir, "Modelefusion_preproc.joblib")
        self.xgb_path = os.path.join(models_dir, "context_correction_xgb.joblib")
        self.label_enc_path = os.path.join(models_dir, "context_correction_label_encoder.joblib")
        
        # Transform pour EfficientNet
        self.transform_eff = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        
        # Modèles (seront chargés lors de l'appel à load_models)
        self.yolo_model = None
        self.eff_model = None
        self.preproc = None
        self.xgb_model = None
        self.label_enc = None
        
        # Charger les modèles
        self.load_models()
    
    def load_models(self):
        """Charge tous les modèles en mémoire."""
        print("⏳ Chargement des modèles...")
        
        # 1. YOLO
        try:
            self.yolo_model = YOLO(self.yolo_path)
            print("✅ YOLO chargé")
        except Exception as e:
            raise Exception(f"Erreur chargement YOLO: {e}")
        
        # 2. EfficientNet
        try:
            self.eff_model = efficientnet_b0(pretrained=False)
            num_features = self.eff_model.classifier[1].in_features
            self.eff_model.classifier[1] = torch.nn.Linear(num_features, 3)
            state = torch.load(self.effnet_path, map_location=self.device)
            self.eff_model.load_state_dict(state)
            self.eff_model.eval()
            self.eff_model.to(self.device)
            print("✅ EfficientNet chargé")
        except Exception as e:
            raise Exception(f"Erreur chargement EfficientNet: {e}")
        
        # 3. Preprocessing
        try:
            self.preproc = joblib.load(self.preproc_path)
            print("✅ Preprocessing chargé")
        except Exception as e:
            raise Exception(f"Erreur chargement Preprocessing: {e}")
        
        # 4. XGBoost
        try:
            self.xgb_model = joblib.load(self.xgb_path)
            print("✅ XGBoost chargé")
        except Exception as e:
            raise Exception(f"Erreur chargement XGBoost: {e}")
        
        # 5. Label Encoder (optionnel)
        try:
            if os.path.exists(self.label_enc_path):
                self.label_enc = joblib.load(self.label_enc_path)
                print("✅ Label Encoder chargé")
            else:
                self.label_enc = None
                print("⚠️  Label Encoder non trouvé (optionnel)")
        except Exception as e:
            self.label_enc = None
            print(f"⚠️  Erreur chargement Label Encoder: {e}")
        
        print("✅ Tous les modèles sont prêts!\n")
    
    def detect_troubles(self, image_path: str, conf_thres: float = 0.1) -> Tuple[np.ndarray, List[Dict], np.ndarray]:
        """
        Détecte les troubles de peau avec YOLO.
        
        Returns:
            probs: Probabilités normalisées pour chaque trouble
            detections: Liste des détections avec coordonnées
            annotated_img: Image annotée avec les détections
        """
        results = self.yolo_model(image_path, conf=conf_thres, verbose=False)
        r = results[0]
        probs = np.zeros(len(self.TROUBLE_LABELS))
        detections = []
        
        # Charger et annoter l'image
        img = cv2.imread(image_path)
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img = None
        
        if hasattr(r, "boxes") and len(r.boxes) > 0:
            for cls_id, conf, box in zip(r.boxes.cls.cpu().numpy().astype(int),
                                         r.boxes.conf.cpu().numpy(),
                                         r.boxes.xyxy.cpu().numpy()):
                if 0 <= cls_id < len(self.TROUBLE_LABELS):
                    probs[cls_id] = max(probs[cls_id], float(conf))
                    detections.append({
                        "label": self.TROUBLE_LABELS[cls_id],
                        "conf": float(conf),
                        "box": box.tolist()
                    })
                    # Annoter l'image
                    if img is not None:
                        x1, y1, x2, y2 = map(int, box)
                        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 165, 0), 2)
                        cv2.putText(img, f"{self.TROUBLE_LABELS[cls_id]} {conf*100:.0f}%",
                                   (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)
        
        if probs.sum() > 0:
            probs /= probs.sum()
        
        return probs, detections, img if img is not None else np.array([])
    
    def classify_skin_type(self, image_path: str) -> Tuple[str, Dict[str, float], np.ndarray]:
        """
        Classe le type de peau avec EfficientNet.
        
        Returns:
            skin_label: Label du type de peau (Dry/Normal/Oily)
            skin_probs_dict: Dictionnaire des probabilités
            sk_probs_arr: Array des probabilités
        """
        img = Image.open(image_path).convert("RGB")
        x = self.transform_eff(img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            logits = self.eff_model(x)
            probs = F.softmax(logits, dim=1).cpu().numpy().ravel()
        idx = int(np.argmax(probs))
        return self.SKIN_LABELS[idx], {self.SKIN_LABELS[i]: float(probs[i]) for i in range(3)}, probs
    
    def predict_fusion(self, user_info: Dict, yolo_probs: np.ndarray, 
                      sk_probs_arr: np.ndarray, skin_label: str) -> Tuple[int, float, np.ndarray]:
        """
        Prédiction finale avec fusion XGBoost.
        
        Returns:
            label_id: ID du label prédit
            proba: Probabilité maximale
            all_probas: Toutes les probabilités
        """
        df = pd.DataFrame([user_info])
        for i, v in enumerate(yolo_probs):
            df[f"tr_p{i}"] = float(v)
        for i, v in enumerate(sk_probs_arr):
            df[f"sk_p{i}"] = float(v)
        
        df["predicted_skin_label_Dry"] = 1.0 if skin_label == "Dry" else 0.0
        df["predicted_skin_label_Normal"] = 1.0 if skin_label == "Normal" else 0.0
        df["predicted_skin_label_Oily"] = 1.0 if skin_label == "Oily" else 0.0
        
        df_encoded = pd.get_dummies(df, drop_first=False)
        expected = self.xgb_model.get_booster().feature_names
        expected = [c.replace('"', '').strip() for c in expected]
        for c in expected:
            if c not in df_encoded.columns:
                df_encoded[c] = 0.0
        df_encoded = df_encoded[[c for c in expected]]
        
        X = df_encoded.values
        y_pred = self.xgb_model.predict(X)
        y_proba = self.xgb_model.predict_proba(X)[0]
        
        label_id = int(y_pred[0])
        proba = float(np.max(y_proba))
        return label_id, proba, y_proba
    
    def analyze_image(self, image_path: str, user_info: Optional[Dict] = None) -> Dict:
        """
        Analyse complète d'une image.
        
        Args:
            image_path: Chemin vers l'image
            user_info: Dictionnaire avec les infos utilisateur (optionnel)
                Exemple: {
                    "age": 25,
                    "gender": "Female",
                    "sleep_hours": 6,
                    "stress_level": 4,
                    "diet_quality": "Average",
                    "smoker": "No",
                    "alcohol_consumption": "No"
                }
        
        Returns:
            Dictionnaire avec tous les résultats
        """
        if user_info is None:
            user_info = {
                "age": 25,
                "gender": "Female",
                "sleep_hours": 7,
                "stress_level": 5,
                "diet_quality": "Average",
                "smoker": "No",
                "alcohol_consumption": "No"
            }
        
        # 1. Détection YOLO
        yolo_probs, detections, annotated_img = self.detect_troubles(image_path)
        
        # 2. Classification type de peau
        skin_label, skin_probs_dict, sk_probs_arr = self.classify_skin_type(image_path)
        
        # 3. Prédiction fusion
        label_id, proba, all_probas = self.predict_fusion(user_info, yolo_probs, sk_probs_arr, skin_label)
        
        # Trouver le diagnostic principal (basé sur YOLO)
        yolo_max_idx = int(np.argmax(yolo_probs))
        yolo_diagnostic = self.TROUBLE_LABELS[yolo_max_idx]
        yolo_confidence = yolo_probs[yolo_max_idx]
        
        # Troubles détectés
        detected_troubles = [self.TROUBLE_LABELS[i] for i, p in enumerate(yolo_probs) if p >= 0.1]
        
        return {
            "image_path": image_path,
            "yolo_diagnostic": yolo_diagnostic,
            "yolo_confidence": float(yolo_confidence),
            "yolo_probs": {self.TROUBLE_LABELS[i]: float(p) for i, p in enumerate(yolo_probs)},
            "detections": detections,
            "annotated_image": annotated_img,
            "skin_type": skin_label,
            "skin_probs": skin_probs_dict,
            "xgb_label_id": int(label_id),
            "xgb_confidence": float(proba),
            "detected_troubles": detected_troubles,
            "user_info": user_info
        }


# Fonction utilitaire pour faciliter l'utilisation
def create_diagnostic(models_dir: str = "models") -> SkinDiagnostic:
    """
    Fonction helper pour créer une instance de SkinDiagnostic.
    
    Usage:
        diagnostic = create_diagnostic("path/to/models")
        result = diagnostic.analyze_image("image.jpg")
    """
    return SkinDiagnostic(models_dir=models_dir)

