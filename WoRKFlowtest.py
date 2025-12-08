# ============================================================
# 💎 Diagnostic Dermatologique — Version Git-Safe
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
YOLO_PATH = "models/modele_skinTwin2.pt"
EFFICIENTNET_PATH = "models/modele_peau.pth"
PREPROC_PATH = "models/Modelefusion_preproc.joblib"
XGB_PATH = "models/context_correction_xgb.joblib"
LABELENC_PATH = "models/context_correction_label_encoder.joblib"
TEST_IMAGE = "C:/Users/ASUS/Downloads/Peau-Grasse.jpg"

# ============================================================
# 🔹 CHARGEMENT DES MODÈLES
# ============================================================
print("⏳ Chargement des modèles...")
device = "cuda" if torch.cuda.is_available() else "cpu"

yolo_model = YOLO(YOLO_PATH)

eff_model = efficientnet_b0(pretrained=False)
num_features = eff_model.classifier[1].in_features
eff_model.classifier[1] = torch.nn.Linear(num_features, 3)
state = torch.load(EFFICIENTNET_PATH, map_location="cpu")
eff_model.load_state_dict(state)
eff_model.eval()

preproc = joblib.load(PREPROC_PATH)
xgb_model = joblib.load(XGB_PATH)
label_enc = joblib.load(LABELENC_PATH) if os.path.exists(LABELENC_PATH) else None

print("✅ Modèles chargés avec succès.\n")

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
    X = transform_eff(img).unsqueeze(0)

    with torch.no_grad():
        logits = eff_model(X)
        probs = F.softmax(logits, dim=1).cpu().numpy().ravel()

    idx = int(np.argmax(probs))
    return skin_labels[idx], probs

# ============================================================
# 🔹 PRÉDICTION XGBOOST FUSION
# ============================================================
def predict_fusion(user_info, yolo_probs, sk_probs_arr, skin_label):
    df = pd.DataFrame([user_info])

    for i, v in enumerate(yolo_probs):
        df[f"tr_p{i}"] = float(v)

    for i, v in enumerate(sk_probs_arr):
        df[f"sk_p{i}"] = float(v)

    df[f"skin_{skin_label}"] = 1.0

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
# 🔹 RAPPORT HUMANISÉ (VERSION SANS API GROQ)
# ============================================================
def generate_human_report(trouble, proba, skin_label, user_info):
    return f"""
### 🧾 Rapport Dermatologique Humanisé

**Diagnostic principal :** {trouble}  
**Confiance :** {proba*100:.1f}%  
**Type de peau :** {skin_label}

---

### ✨ Analyse clinique
Votre peau présente des signes compatibles avec **{trouble}**.  
Ce résultat est cohérent avec votre profil :  
- Âge : {user_info.get('age')}
- Sommeil : {user_info.get('sleep_hours')}h
- Stress : {user_info.get('stress_level')}/10

---

### 🧴 Routine de soin recommandée
- Nettoyage doux matin + soir  
- Hydratant adapté aux peaux **{skin_label.lower()}**  
- Protection solaire SPF50 quotidiennement  

---

### 🧪 Produits conseillés
- La Roche-Posay Effaclar / CeraVe / The Ordinary  
- Sérum Niacinamide 10%  
- Gel nettoyant sans parfum  

---

### 💙 Message de votre dermatologue
Votre peau réagit, mais rien d’alarmant.  
Avec une routine cohérente, vous verrez une amélioration en quelques semaines.  
Gardez confiance : vous êtes sur la bonne voie 🌿.
"""

# ============================================================
# 🔹 PIPELINE COMPLET
# ============================================================
def analyze_and_generate_report(image_path, user_info):
    yolo_probs, detections, annotated = run_yolo(image_path)
    skin_label, sk_probs_arr = run_effnet(image_path)
    label_id, proba = predict_fusion(user_info, yolo_probs, sk_probs_arr, skin_label)

    trouble = trouble_labels[label_id]

    rapport = generate_human_report(trouble, proba, skin_label, user_info)

    print(rapport)

    if annotated is not None:
        plt.imshow(annotated)
        plt.axis("off")
        plt.show()

    return {
        "diagnostic": trouble,
        "confidence": proba,
        "skin_type": skin_label,
        "rapport": rapport
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

result = analyze_and_generate_report(TEST_IMAGE, user_info)
print("✅ Rapport généré.")
