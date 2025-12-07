import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import cv2
import numpy as np
import io

st.set_page_config(page_title="Transformation Peau 3 Mois", layout="wide")
st.title("📊 Transformation Peau - Progression 3 Mois")

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Paramètres de Transformation")
    filter_type = st.radio("Intensité du filtre", ["Léger", "Moyen", "Fort", "Extrême"])
    st.divider()
    st.subheader("Ajustements")
    
    # Main controls
    skin_smoothness = st.slider("🔹 Lissage peau", 0.0, 1.0, 0.65, step=0.1)
    defect_reduction = st.slider("💊 Réduction défauts", 0.0, 1.0, 0.6, step=0.1)
    brightness = st.slider("☀️ Luminosité", 0.0, 1.0, 0.55, step=0.1)
    glow = st.slider("✨ Éclat", 0.0, 1.0, 0.5, step=0.1)

# Filter parameters
FILTER_PARAMS = {
    "Léger": {"bilateral": 1, "bright": 1.06, "contrast": 1.04},
    "Moyen": {"bilateral": 2, "bright": 1.12, "contrast": 1.08},
    "Fort": {"bilateral": 3, "bright": 1.18, "contrast": 1.12},
    "Extrême": {"bilateral": 4, "bright": 1.26, "contrast": 1.18}
}

def apply_beauty_filter(img_cv, intensity_percent, params):
    """Apply beauty filter with controllable intensity"""
    img_result = img_cv.copy()
    intensity = intensity_percent / 100.0
    
    # Healing - very gentle
    img_healed = cv2.bilateralFilter(img_cv, 7, 60, 60)
    blend_heal = intensity * 0.2
    img_result = cv2.addWeighted(img_cv, 1 - blend_heal, img_healed, blend_heal, 0)
    
    # Smoothing - light
    for _ in range(max(1, int(params["bilateral"] * intensity))):
        d = int(5 + intensity * 4)
        if d % 2 == 0:
            d += 1
        img_result = cv2.bilateralFilter(img_result, d, 60, 60)
    
    # Blur blend
    img_blur = cv2.GaussianBlur(img_result, (5, 5), 0)
    alpha = 0.85 - intensity * 0.1
    img_result = cv2.addWeighted(img_result, alpha, img_blur, 1 - alpha, 0)
    
    return img_result

def enhance_to_pil(img_cv, brightness_val, intensity_percent):
    """Convert to PIL and enhance"""
    img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    intensity = intensity_percent / 100.0
    
    # Brightness
    bright_factor = 1.08 + brightness_val * 0.12 * intensity
    img_pil = ImageEnhance.Brightness(img_pil).enhance(bright_factor)
    
    # Contrast
    contrast_factor = 1.06 + brightness_val * 0.08 * intensity
    img_pil = ImageEnhance.Contrast(img_pil).enhance(contrast_factor)
    
    # Color
    color_factor = 1.0 + brightness_val * 0.08 * intensity
    img_pil = ImageEnhance.Color(img_pil).enhance(color_factor)
    
    # Glow
    if brightness_val > 0:
        img_glow = img_pil.filter(ImageFilter.GaussianBlur(radius=5))
        glow_blend = brightness_val * 0.2 * intensity
        img_pil = Image.blend(img_pil, img_glow, glow_blend)
    
    return img_pil

def create_3month_progression(img_original, filter_type, smoothness, defects, brightness_val, glow_val):
    """Create 3-month transformation progression"""
    params = FILTER_PARAMS[filter_type]
    img_cv = cv2.cvtColor(np.array(img_original), cv2.COLOR_RGB2BGR)
    
    # AVANT - Original (0%)
    img_avant = img_original.copy()
    
    # 1 MOIS - 33% de transformation
    img_1m_cv = apply_beauty_filter(img_cv, 33, params)
    img_1m = enhance_to_pil(img_1m_cv, brightness_val * 0.7, 33)
    
    # 2 MOIS - 66% de transformation
    img_2m_cv = apply_beauty_filter(img_cv, 66, params)
    img_2m = enhance_to_pil(img_2m_cv, brightness_val * 0.85, 66)
    
    # 3 MOIS - 100% de transformation
    img_3m_cv = apply_beauty_filter(img_cv, 100, params)
    img_3m = enhance_to_pil(img_3m_cv, brightness_val, 100)
    
    return img_avant, img_1m, img_2m, img_3m

def create_progression_image(img_avant, img_1m, img_2m, img_3m):
    """Create side-by-side progression image"""
    # Resize all to same size
    size = (280, 320)
    img_avant_r = img_avant.resize(size)
    img_1m_r = img_1m.resize(size)
    img_2m_r = img_2m.resize(size)
    img_3m_r = img_3m.resize(size)
    
    # Create canvas (4 images + margins)
    margin = 10
    total_width = size[0] * 4 + margin * 5
    total_height = size[1] + 60
    
    canvas = Image.new('RGB', (total_width, total_height), color=(30, 30, 30))
    
    # Paste images
    canvas.paste(img_avant_r, (margin, 40))
    canvas.paste(img_1m_r, (margin + size[0] + margin, 40))
    canvas.paste(img_2m_r, (margin + (size[0] + margin) * 2, 40))
    canvas.paste(img_3m_r, (margin + (size[0] + margin) * 3, 40))
    
    # Add labels
    draw = ImageDraw.Draw(canvas)
    labels = ["AVANT", "1 MOIS", "2 MOIS", "3 MOIS"]
    x_positions = [margin + size[0]//3, margin + size[0] + margin + size[0]//3,
                   margin + (size[0] + margin) * 2 + size[0]//3,
                   margin + (size[0] + margin) * 3 + size[0]//3]
    
    for label, x in zip(labels, x_positions):
        draw.text((x - 20, 10), label, fill=(255, 200, 100))
    
    return canvas

# Main application
uploaded_file = st.file_uploader("📸 Téléchargez votre photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img_original = Image.open(uploaded_file).convert("RGB")
    
    if st.button("🎯 Voir Progression 3 Mois", use_container_width=True):
        with st.spinner("⏳ Calcul de la progression..."):
            img_avant, img_1m, img_2m, img_3m = create_3month_progression(
                img_original,
                filter_type,
                skin_smoothness,
                defect_reduction,
                brightness,
                glow
            )
        
        st.success("✅ Progression générée!")
        
        # Display progression
        st.subheader("📊 Transformation Progressive (3 Mois)")
        progression_img = create_progression_image(img_avant, img_1m, img_2m, img_3m)
        st.image(progression_img, use_column_width=True)
        
        st.divider()
        
        # Show detailed before/after for each month
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("1️⃣ 1 Mois")
            comparison_1m = Image.new('RGB', (600, 300), color=(40, 40, 40))
            img_a = img_original.resize((280, 280))
            img_b = img_1m.resize((280, 280))
            comparison_1m.paste(img_a, (10, 10))
            comparison_1m.paste(img_b, (310, 10))
            draw = ImageDraw.Draw(comparison_1m)
            draw.text((80, 265), "AVANT", fill=(255, 255, 255))
            draw.text((350, 265), "1 MOIS", fill=(255, 200, 100))
            st.image(comparison_1m)
        
        with col2:
            st.subheader("2️⃣ 2 Mois")
            comparison_2m = Image.new('RGB', (600, 300), color=(40, 40, 40))
            img_a = img_original.resize((280, 280))
            img_b = img_2m.resize((280, 280))
            comparison_2m.paste(img_a, (10, 10))
            comparison_2m.paste(img_b, (310, 10))
            draw = ImageDraw.Draw(comparison_2m)
            draw.text((80, 265), "AVANT", fill=(255, 255, 255))
            draw.text((350, 265), "2 MOIS", fill=(255, 200, 100))
            st.image(comparison_2m)
        
        with col3:
            st.subheader("3️⃣ 3 Mois")
            comparison_3m = Image.new('RGB', (600, 300), color=(40, 40, 40))
            img_a = img_original.resize((280, 280))
            img_b = img_3m.resize((280, 280))
            comparison_3m.paste(img_a, (10, 10))
            comparison_3m.paste(img_b, (310, 10))
            draw = ImageDraw.Draw(comparison_3m)
            draw.text((80, 265), "AVANT", fill=(255, 255, 255))
            draw.text((350, 265), "3 MOIS", fill=(255, 200, 100))
            st.image(comparison_3m)
        
        st.divider()
        
        # Download options
        st.subheader("📥 Télécharger")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            buf = io.BytesIO()
            img_1m.save(buf, format="PNG", quality=95)
            buf.seek(0)
            st.download_button(
                label="1 Mois",
                data=buf.getvalue(),
                file_name="1_mois.png",
                mime="image/png",
                use_container_width=True
            )
        
        with col2:
            buf = io.BytesIO()
            img_2m.save(buf, format="PNG", quality=95)
            buf.seek(0)
            st.download_button(
                label="2 Mois",
                data=buf.getvalue(),
                file_name="2_mois.png",
                mime="image/png",
                use_container_width=True
            )
        
        with col3:
            buf = io.BytesIO()
            img_3m.save(buf, format="PNG", quality=95)
            buf.seek(0)
            st.download_button(
                label="3 Mois",
                data=buf.getvalue(),
                file_name="3_mois.png",
                mime="image/png",
                use_container_width=True
            )
        
        with col4:
            buf = io.BytesIO()
            progression_img.save(buf, format="PNG", quality=95)
            buf.seek(0)
            st.download_button(
                label="Progression",
                data=buf.getvalue(),
                file_name="progression_3mois.png",
                mime="image/png",
                use_container_width=True
            )

else:
    st.info("👆 Téléchargez une photo pour voir votre transformation")

st.divider()
st.markdown("""
### 📈 Comment ça fonctionne:

La progression montre comment votre peau s'améliore graduellement:

**AVANT** - Votre état initial
- Texture originale
- Défauts visibles
- Éclat naturel

**1 MOIS** - Premières améliorations (33%)
- Peau légèrement plus lisse
- Premiers défauts atténués
- Légèrement plus lumineux

**2 MOIS** - Amélioration significative (66%)
- Peau visiblement lissée
- Défauts considérablement réduits
- Beaucoup plus éclatant

**3 MOIS** - Transformation complète (100%)
- Peau très lisse et raffinée
- Défauts éliminés
- Très lumineux et éclatant

### 💡 Conseils:
- Ajustez les sliders pour voir différentes intensités
- Comparez les images pour voir la progression
- Téléchargez chaque étape pour votre suivi personnel
""")