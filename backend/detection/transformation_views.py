from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import SkinAnalysis
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64
import logging

logger = logging.getLogger(__name__)

# Filter parameters - Balanced for natural results
FILTER_PARAMS = {
    "Léger": {"bilateral": 1, "bright": 1.04, "contrast": 1.03},
    "Moyen": {"bilateral": 2, "bright": 1.08, "contrast": 1.06},
    "Fort": {"bilateral": 3, "bright": 1.12, "contrast": 1.09},
    "Extrême": {"bilateral": 4, "bright": 1.16, "contrast": 1.12}
}


def reduce_redness_and_acne(img_cv, intensity_percent, defect_reduction):
    """Specifically reduce redness and acne spots - Progressive and natural"""
    intensity = intensity_percent / 100.0
    if defect_reduction <= 0 or intensity <= 0:
        return img_cv
    
    img_result = img_cv.copy()
    
    # Convert to LAB color space for better skin tone processing
    lab = cv2.cvtColor(img_result, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Create mask for red areas (acne, redness) - progressive threshold
    threshold = 130 + (intensity * 10)  # Progressive: 130 -> 140
    _, red_mask = cv2.threshold(a, int(threshold), 255, cv2.THRESH_BINARY)
    red_mask = cv2.GaussianBlur(red_mask, (13, 13), 0) / 255.0
    
    # Progressive reduction - natural and visible
    reduction_factor = intensity * defect_reduction * (0.3 + intensity * 0.3)
    a_reduced = a.copy().astype(np.float32)
    a_reduced = a_reduced - (a_reduced - 128) * red_mask * reduction_factor
    a_reduced = np.clip(a_reduced, 0, 255).astype(np.uint8)
    
    # Smooth out the transitions - moderate
    smoothing_strength = int(9 + intensity * 6)
    a_reduced = cv2.bilateralFilter(a_reduced, smoothing_strength, 70, 70)
    
    # Merge back
    lab = cv2.merge([l, a_reduced, b])
    img_result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Conservative inpainting for severe cases only
    if intensity > 0.5 and defect_reduction > 0.4:
        gray = cv2.cvtColor(img_result, cv2.COLOR_BGR2GRAY)
        _, spots = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel_size = int(3 + intensity * 4)
        spots = cv2.morphologyEx(spots, cv2.MORPH_CLOSE, np.ones((kernel_size, kernel_size), np.uint8))
        
        if np.sum(spots > 0) > 0:
            inpaint_radius = int(2 + intensity * 3)
            max_spots_area = img_result.shape[0] * img_result.shape[1] * (0.03 + intensity * 0.05)
            if np.sum(spots > 0) < max_spots_area:
                img_result = cv2.inpaint(img_result, spots, inpaint_radius, cv2.INPAINT_TELEA)
    
    return img_result


def apply_beauty_filter(img_cv, intensity_percent, params, smoothness=0.65, defect_reduction=0.6):
    """Apply soft beauty filter with natural skin preservation - CORRECTED VERSION"""
    intensity = intensity_percent / 100.0
    img_result = img_cv.copy()
    
    # First, reduce redness and acne specifically
    img_result = reduce_redness_and_acne(img_result, intensity_percent, defect_reduction)
    
    # 1) Soft bilateral smoothing - ONE PASS ONLY (not multiple loops)
    img_smooth = cv2.bilateralFilter(img_result, 9, 40, 40)
    
    # Blend soft smoothing - very gentle
    smooth_blend = 0.15 * intensity * smoothness
    img_result = cv2.addWeighted(img_result, 1 - smooth_blend, img_smooth, smooth_blend, 0)
    
    # 2) Very light blur for evening tones - CORRECTED alpha
    img_blur = cv2.GaussianBlur(img_result, (3, 3), 0)  # Small kernel (3x3)
    alpha = 0.97 - intensity * 0.03  # CORRECTED: Much softer (was 0.85 - intensity * 0.1)
    img_result = cv2.addWeighted(img_result, alpha, img_blur, 1 - alpha, 0)
    
    return img_result


def enhance_to_pil(img_cv, brightness_val, intensity_percent, glow_val=0.5):
    """Convert to PIL and enhance - Natural and balanced"""
    img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    intensity = intensity_percent / 100.0
    
    # Balanced brightness - avoid overexposure
    bright_factor = 1.05 + brightness_val * 0.10 * intensity
    img_pil = ImageEnhance.Brightness(img_pil).enhance(bright_factor)
    
    # Balanced contrast - subtle improvement
    contrast_factor = 1.04 + brightness_val * 0.08 * intensity
    img_pil = ImageEnhance.Contrast(img_pil).enhance(contrast_factor)
    
    # Balanced color saturation - keep natural tones
    color_factor = 1.0 + brightness_val * 0.06 * intensity
    img_pil = ImageEnhance.Color(img_pil).enhance(color_factor)
    
    # CORRECTED: Very subtle glow effect - avoid excessive blur
    if glow_val > 0 and brightness_val > 0:
        img_glow = img_pil.filter(ImageFilter.GaussianBlur(radius=3))  # Small radius
        glow_blend = glow_val * 0.07 * intensity  # CORRECTED: Much reduced (was 0.2)
        img_pil = Image.blend(img_pil, img_glow, glow_blend)
    
    # Sharpening to maintain clarity and prevent blur
    from PIL import ImageFilter as PILFilter
    if intensity > 0.2:
        # Subtle sharpening to maintain detail
        img_pil = img_pil.filter(PILFilter.UnsharpMask(radius=1, percent=100 + int(intensity * 30), threshold=3))
    
    return img_pil


def create_3month_progression(img_original, filter_type, smoothness, defects, brightness_val, glow_val):
    """Create 3-month transformation progression - Natural and realistic"""
    params = FILTER_PARAMS[filter_type]
    img_cv = cv2.cvtColor(np.array(img_original), cv2.COLOR_RGB2BGR)
    
    # AVANT - Original (0%)
    img_avant = img_original.copy()
    
    # CORRECTED INTENSITIES: 20%, 40%, 60% (instead of 33%, 66%, 100%)
    # 1 MOIS - 20% de transformation (subtle visible improvement)
    img_1m_cv = apply_beauty_filter(img_cv, 20, params, smoothness, defects)
    img_1m = enhance_to_pil(img_1m_cv, brightness_val * 0.70, 20, glow_val * 0.50)
    
    # 2 MOIS - 40% de transformation (moderate improvement)
    img_2m_cv = apply_beauty_filter(img_cv, 40, params, smoothness, defects)
    img_2m = enhance_to_pil(img_2m_cv, brightness_val * 0.85, 40, glow_val * 0.70)
    
    # 3 MOIS - 60% de transformation (significant but natural improvement)
    img_3m_cv = apply_beauty_filter(img_cv, 60, params, smoothness, defects)
    # Cap brightness to avoid overexposure
    capped_brightness = min(brightness_val, 0.85)
    capped_glow = min(glow_val, 0.75)
    img_3m = enhance_to_pil(img_3m_cv, capped_brightness, 60, capped_glow)
    
    return img_avant, img_1m, img_2m, img_3m


def pil_to_base64(img_pil):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    img_pil.save(buffered, format="PNG", quality=95)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_transformation(request, analysis_id):
    """Create skin transformation progression"""
    try:
        # Get analysis
        analysis = get_object_or_404(SkinAnalysis, id=analysis_id, user=request.user)
        
        # Get parameters from request
        filter_type = request.data.get('filter_type', 'Moyen')
        skin_smoothness = float(request.data.get('skin_smoothness', 0.50))
        defect_reduction = float(request.data.get('defect_reduction', 0.50))
        brightness = float(request.data.get('brightness', 0.40))
        glow = float(request.data.get('glow', 0.35))
        
        # Validate filter_type
        if filter_type not in FILTER_PARAMS:
            return Response(
                {'error': 'Type de filtre invalide'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Load original image
        img_path = analysis.image.path
        img_original = Image.open(img_path).convert("RGB")
        
        # Create progression
        img_avant, img_1m, img_2m, img_3m = create_3month_progression(
            img_original,
            filter_type,
            skin_smoothness,
            defect_reduction,
            brightness,
            glow
        )
        
        # Convert to base64 for frontend
        return Response({
            'avant': pil_to_base64(img_avant),
            '1_mois': pil_to_base64(img_1m),
            '2_mois': pil_to_base64(img_2m),
            '3_mois': pil_to_base64(img_3m),
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f'Error creating transformation: {str(e)}', exc_info=True)
        return Response(
            {'error': f'Erreur lors de la création de la transformation: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
