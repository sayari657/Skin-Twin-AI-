# ============================================================
# 💎 Diagnostic Dermatologique — Version Nettoyée
# ============================================================

import os
import numpy as np
import pandas as pd
import joblib
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from ultralytics import YOLO
import torchvision.transforms as transforms
from torchvision.models import efficientnet_b0

# ============================================================
# ⚙️ CONFIGURATION
# ============================================================
YOLO_PATH = "models/modèle_skinTwin2.pt"
EFFICIENTNET_PATH = "models/modele_peau.pth"
PREPROC_PATH = "models/Modelefusion_preproc.joblib"
XGB_PATH = "models/context_correction_xgb.joblib"

TEST_IMAGE = "C:/Users/ASUS/Downloads/Peau-Grasse.jpg"

# ============================================================
# 🔹 CHARGEMENT DES MODÈLES
# ============================================================
print("⏳ Chargement des modèles...")

device = "cuda" if torch.cuda.is_available() else "cpu"

# YOLO
yolo_model = YOLO(YOLO_PATH)

# EfficientNet
eff_model = efficientnet_b0(pretrained=False)
num_features = eff_model.classifier[1].in_features
eff_model.classifier[1] = torch.nn.Linear(num_features, 3)

state = torch.load(EFFICIENTNET_PATH, map_location="cpu")
eff_model.load_state_dict(state)
eff_model.eval()

# Préprocesseur & XGBoost
preproc = joblib.load(PREPROC_PATH)
xgb_model = joblib.load(XGB_PATH)

print("✅ Modèles chargés.\n")

# ============================================================
# 🔹 LABELS
# ============================================================
trouble_labels = [
    'Acne', 'Blackheads', 'Dark-Spots', 'Dry-Skin', 'Englarged-Pores',
    'Eyebags', 'Oily-Skin', 'Skin-Redness', 'Whiteheads', 'Wrinkles'
]

skin_labels = {0: "Dry", 1: "Normal", 2: "Oily"}

transform_eff = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# ============================================================
# 🔹 DÉTECTION YOLO
# ============================================================
def run_yolo(image_path, conf_thres=0.1):
    results = yolo_model(image_path, conf=conf_thres, verbose=False)
    r = results[0]

    probs = np.zeros(len(trouble_labels))
    detections = []

    if hasattr(r, "boxes") and len(r.boxes) > 0:
        for cls_id, conf, box in zip(
            r.boxes.cls.cpu().numpy().astype(int),
            r.boxes.conf.cpu().numpy(),
            r.boxes.xyxy.cpu().numpy()
        ):

            if 0 <= cls_id < len(trouble_labels):
                probs[cls_id] = max(probs[cls_id], float(conf))
                detections.append({
                    "label": trouble_labels[cls_id],
                    "conf": float(conf),
                    "box": box.tolist()
                })

    if probs.sum() > 0:
        probs /= probs.sum()

    # Image annotée
    img = cv2.imread(image_path)
    if img is not None:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        for d in detections:
            x1, y1, x2, y2 = map(int, d["box"])
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 165, 0), 2)
            cv2.putText(img, f"{d['label']} {d['conf']*100:.0f}%",
                        (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)

    return probs, detections, img

# ============================================================
# 🔹 TYPE DE PEAU
# ============================================================
def run_effnet(image_path):
    img = Image.open(image_path).convert("RGB")
    x = transform_eff(img).unsqueeze(0)

    with torch.no_grad():
        logits = eff_model(x)
        probs = F.softmax(logits, dim=1).cpu().numpy().ravel()

    idx = int(np.argmax(probs))
    return skin_labels[idx], probs

# ============================================================
# 🔹 PRÉDICTION XGBOOST FUSION
# ============================================================
def predict_fusion(user_info, yolo_probs, sk_probs_arr, skin_label):

    df = pd.DataFrame([user_info])

    # Ajouter probs YOLO
    for i, v in enumerate(yolo_probs):
        df[f"tr_p{i}"] = float(v)

    # Ajouter probs EfficientNet
    for i, v in enumerate(sk_probs_arr):
        df[f"sk_p{i}"] = float(v)

    # Ajouter type de peau (one hot)
    df["predicted_skin_label_Dry"] = 1.0 if skin_label == "Dry" else 0.0
    df["predicted_skin_label_Normal"] = 1.0 if skin_label == "Normal" else 0.0
    df["predicted_skin_label_Oily"] = 1.0 if skin_label == "Oily" else 0.0

    # Alignement
    df = pd.get_dummies(df, drop_first=False)
    expected = xgb_model.get_booster().feature_names

    for col in expected:
        if col not in df.columns:
            df[col] = 0

    df = df[expected]

    y_pred = xgb_model.predict(df.values)
    y_proba = xgb_model.predict_proba(df.values)[0]

    label_id = int(y_pred[0])
    proba = float(np.max(y_proba))

    return label_id, proba

# ============================================================
# 🔹 PIPELINE COMPLET
# ============================================================
def analyze(image_path, user_info):

    yolo_probs, detections, annotated = run_yolo(image_path)
    skin_label, sk_probs_arr = run_effnet(image_path)
    label_id, proba = predict_fusion(user_info, yolo_probs, sk_probs_arr, skin_label)

    diagnostic = trouble_labels[label_id]

    print("\n🩺 Diagnostic :", diagnostic)
    print("💧 Type de peau :", skin_label)
    print("📊 Confiance :", f"{proba*100:.1f}%")
    print("⚡ Symptômes détectés :", [trouble_labels[i] for i, p in enumerate(yolo_probs) if p >= 0.1])

    if annotated is not None:
        plt.figure(figsize=(6, 6))
        plt.imshow(annotated)
        plt.axis("off")
        plt.title(f"{diagnostic} — {skin_label}")
        plt.show()

    return {
        "diagnostic": diagnostic,
        "confidence": proba,
        "skin_type": skin_label
    }

# ============================================================
# 🔹 TEST
# ============================================================
user_info = {
    "age": 25,
    "gender": "Female",
    "sleep_hours": 6,
    "stress_level": 4,
    "diet_quality": "Average",
    "smoker": "No",
    "alcohol_consumption": "No"
}

result = analyze(TEST_IMAGE, user_info)
print("\n✅ Analyse terminée.")
