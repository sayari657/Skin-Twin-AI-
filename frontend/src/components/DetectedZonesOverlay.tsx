import React, { useState, useRef, useEffect } from 'react';
import { Box, Typography, Tooltip } from '@mui/material';
import { SkinAnalysis } from '../types';

interface DetectionBox {
  label: string;
  confidence: number;
  box?: [number, number, number, number]; // [x1, y1, x2, y2]
  severity?: string;
}

interface DetectedZonesOverlayProps {
  imageUrl: string;
  analysis: SkinAnalysis;
  width?: number | string;
  height?: number | string;
}

const DetectedZonesOverlay: React.FC<DetectedZonesOverlayProps> = ({
  imageUrl,
  analysis,
  width = '100%',
  height = 400,
}) => {
  const [imageSize, setImageSize] = useState<{ width: number; height: number } | null>(null);
  const [detections, setDetections] = useState<DetectionBox[]>([]);
  const imageRef = useRef<HTMLImageElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Extraire les détections depuis les données de l'analyse
  useEffect(() => {
    const extractedDetections: DetectionBox[] = [];

    // Vérifier si raw_yolo_results contient des détections avec coordonnées
    if (analysis.raw_yolo_results) {
      try {
        const yoloResults = analysis.raw_yolo_results;
        
        // Nouveau format : raw_yolo_results contient 'detections' (liste avec coordonnées) et 'aggregated' (détections agrégées)
        if (yoloResults.detections && Array.isArray(yoloResults.detections)) {
          yoloResults.detections.forEach((det: any) => {
            if (det.box && Array.isArray(det.box) && det.box.length === 4) {
              extractedDetections.push({
                label: det.label || 'Zone détectée',
                confidence: det.confidence || det.conf || 0,
                box: det.box as [number, number, number, number],
                severity: det.severity,
              });
            }
          });
        }
        
        // Ancien format : si c'est directement un tableau de détections
        if (Array.isArray(yoloResults) && yoloResults.length > 0 && yoloResults[0].box) {
          yoloResults.forEach((det: any) => {
            if (det.box && Array.isArray(det.box) && det.box.length === 4) {
              extractedDetections.push({
                label: det.label || 'Zone détectée',
                confidence: det.confidence || det.conf || 0,
                box: det.box as [number, number, number, number],
                severity: det.severity,
              });
            }
          });
        }
        
        // Vérifier aussi dans raw_cnn_results si les détections y sont stockées
        if (analysis.raw_cnn_results && (analysis.raw_cnn_results as any).detections) {
          const cnnDetections = (analysis.raw_cnn_results as any).detections;
          if (Array.isArray(cnnDetections)) {
            cnnDetections.forEach((det: any) => {
              if (det.box && Array.isArray(det.box) && det.box.length === 4) {
                extractedDetections.push({
                  label: det.label || 'Zone détectée',
                  confidence: det.confidence || det.conf || 0,
                  box: det.box as [number, number, number, number],
                  severity: det.severity,
                });
              }
            });
          }
        }
      } catch (e) {
        console.log('Erreur lors de l\'extraction des détections:', e);
      }
    }

    // Si aucune détection avec coordonnées n'est trouvée, créer des zones approximatives
    // basées sur les problèmes détectés
    if (extractedDetections.length === 0) {
      const problems: Array<{ label: string; detected: boolean; confidence?: number; severity?: string }> = [
        { label: 'Acné', detected: analysis.acne_detected, confidence: analysis.acne_confidence, severity: analysis.acne_severity },
        { label: 'Rides', detected: analysis.wrinkles_detected, confidence: analysis.wrinkles_confidence, severity: analysis.wrinkles_severity },
        { label: 'Taches sombres', detected: analysis.dark_spots_detected, confidence: analysis.dark_spots_confidence, severity: analysis.dark_spots_severity },
        { label: 'Rougeurs', detected: analysis.redness_detected, confidence: analysis.redness_confidence, severity: analysis.redness_severity },
      ];

      problems.forEach((problem, index) => {
        if (problem.detected) {
          // Créer des zones approximatives pour chaque problème détecté
          // Ces zones seront positionnées de manière relative sur l'image
          const zoneWidth = 0.15; // 15% de la largeur de l'image
          const zoneHeight = 0.15; // 15% de la hauteur de l'image
          const margin = 0.1; // 10% de marge
          
          // Positionner les zones à différents endroits du visage
          const positions = [
            [0.2, 0.3], // Joues
            [0.7, 0.3],
            [0.45, 0.2], // Front
            [0.3, 0.5], // Autour des yeux
          ];

          const [relX, relY] = positions[index % positions.length];
          
          extractedDetections.push({
            label: problem.label,
            confidence: problem.confidence || 0.5,
            box: undefined, // Sera calculé en fonction de la taille de l'image
            severity: problem.severity,
            // Stocker les positions relatives pour calculer les coordonnées absolues plus tard
            relativePosition: { x: relX, y: relY, width: zoneWidth, height: zoneHeight },
          } as any);
        }
      });
    }

    setDetections(extractedDetections);
  }, [analysis]);

  // Mettre à jour la taille de l'image quand elle charge
  useEffect(() => {
    const handleImageLoad = () => {
      if (imageRef.current) {
        const img = imageRef.current;
        setImageSize({
          width: img.naturalWidth,
          height: img.naturalHeight,
        });
      }
    };

    const img = imageRef.current;
    if (img) {
      if (img.complete) {
        handleImageLoad();
      } else {
        img.addEventListener('load', handleImageLoad);
        return () => img.removeEventListener('load', handleImageLoad);
      }
    }
  }, [imageUrl]);

  // Calculer les coordonnées des boîtes en fonction de la taille réelle de l'image
  const getBoxCoordinates = (detection: DetectionBox): { x1: number; y1: number; x2: number; y2: number } | null => {
    if (!imageSize || !imageRef.current) return null;

    const img = imageRef.current;
    const displayWidth = img.clientWidth;
    const displayHeight = img.clientHeight;
    const scaleX = displayWidth / imageSize.width;
    const scaleY = displayHeight / imageSize.height;

    if (detection.box) {
      // Utiliser les coordonnées absolues du modèle
      const [x1, y1, x2, y2] = detection.box;
      return {
        x1: x1 * scaleX,
        y1: y1 * scaleY,
        x2: x2 * scaleX,
        y2: y2 * scaleY,
      };
    } else if ((detection as any).relativePosition) {
      // Utiliser les positions relatives pour créer des zones approximatives
      const { x, y, width: relWidth, height: relHeight } = (detection as any).relativePosition;
      return {
        x1: x * displayWidth,
        y1: y * displayHeight,
        x2: (x + relWidth) * displayWidth,
        y2: (y + relHeight) * displayHeight,
      };
    }

    return null;
  };

  const getLabelColor = (label: string): string => {
    const colors: { [key: string]: string } = {
      'Acné': '#FF6B6B',
      'Rides': '#FFA726',
      'Taches sombres': '#AB47BC',
      'Rougeurs': '#EF5350',
      'Eyebags': '#FFB300',
      'Skin': '#4CAF50',
    };
    return colors[label] || '#FF9800';
  };

  const getLabelText = (label: string, confidence: number): string => {
    // Traduire les labels en français si nécessaire
    const translations: { [key: string]: string } = {
      'Acne': 'Acné',
      'Wrinkles': 'Rides',
      'Dark-Spots': 'Taches sombres',
      'Skin-Redness': 'Rougeurs',
      'Eyebags': 'Cernes',
      'Skin': 'Peau',
    };
    
    const translatedLabel = translations[label] || label;
    const percentage = Math.round(confidence * 100);
    return `${translatedLabel} ${percentage}%`;
  };

  return (
    <Box
      ref={containerRef}
      sx={{
        position: 'relative',
        width,
        height,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        bgcolor: 'grey.50',
        borderRadius: 2,
        overflow: 'hidden',
      }}
    >
      <Box
        component="img"
        ref={imageRef}
        src={imageUrl.startsWith('http') ? imageUrl : `http://127.0.0.1:8000${imageUrl}`}
        alt="Image analysée"
        sx={{
          maxWidth: '100%',
          maxHeight: '100%',
          objectFit: 'contain',
          display: 'block',
        }}
        onError={(e) => {
          console.error('Erreur de chargement de l\'image:', e);
        }}
      />
      
      {/* Superposition des zones détectées */}
      {imageSize && detections.length > 0 && (
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            pointerEvents: 'none',
          }}
        >
          {detections.map((detection, index) => {
            const coords = getBoxCoordinates(detection);
            if (!coords) return null;

            const { x1, y1, x2, y2 } = coords;
            const boxWidth = x2 - x1;
            const boxHeight = y2 - y1;
            const labelColor = getLabelColor(detection.label);
            const labelText = getLabelText(detection.label, detection.confidence);

            return (
              <Tooltip
                key={index}
                title={
                  <Box>
                    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                      {detection.label}
                    </Typography>
                    <Typography variant="caption">
                      Confiance: {Math.round(detection.confidence * 100)}%
                    </Typography>
                    {detection.severity && (
                      <Typography variant="caption" sx={{ display: 'block', mt: 0.5 }}>
                        Sévérité: {detection.severity}
                      </Typography>
                    )}
                  </Box>
                }
                arrow
              >
                <Box
                  sx={{
                    position: 'absolute',
                    left: `${(x1 / imageRef.current!.clientWidth) * 100}%`,
                    top: `${(y1 / imageRef.current!.clientHeight) * 100}%`,
                    width: `${(boxWidth / imageRef.current!.clientWidth) * 100}%`,
                    height: `${(boxHeight / imageRef.current!.clientHeight) * 100}%`,
                    border: `2px solid ${labelColor}`,
                    borderRadius: 1,
                    pointerEvents: 'auto',
                    cursor: 'pointer',
                    '&:hover': {
                      borderWidth: 3,
                      boxShadow: `0 0 0 2px ${labelColor}40`,
                    },
                  }}
                >
                  {/* Label au-dessus de la boîte */}
                  <Box
                    sx={{
                      position: 'absolute',
                      top: -24,
                      left: 0,
                      bgcolor: labelColor,
                      color: 'white',
                      px: 1,
                      py: 0.25,
                      borderRadius: 0.5,
                      fontSize: '0.75rem',
                      fontWeight: 'bold',
                      whiteSpace: 'nowrap',
                      boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                      zIndex: 10,
                    }}
                  >
                    {labelText}
                  </Box>
                </Box>
              </Tooltip>
            );
          })}
        </Box>
      )}
    </Box>
  );
};

export default DetectedZonesOverlay;

