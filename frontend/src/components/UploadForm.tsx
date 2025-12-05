import React, { useState, useCallback, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Box,
  Paper,
  Typography,
  Button,
  LinearProgress,
  Alert,
  Card,
  CardContent,
  CardMedia,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  PhotoCamera as CameraIcon,
  CheckCircle as CheckIcon,
  Videocam as VideocamIcon,
  Close as CloseIcon,
  CameraAlt as CameraAltIcon,
} from '@mui/icons-material';
import { SkinAnalysis } from '../types';
import { apiService } from '../services/api';

interface UploadFormProps {
  onAnalysisComplete: (analysis: SkinAnalysis) => void;
}

const UploadForm: React.FC<UploadFormProps> = ({ onAnalysisComplete }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<SkinAnalysis | null>(null);
  const [cameraOpen, setCameraOpen] = useState(false);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const videoRef = React.useRef<HTMLVideoElement>(null);
  const canvasRef = React.useRef<HTMLCanvasElement>(null);
  const metadataHandlerRef = React.useRef<(() => void) | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setError(null);
      setPreview(URL.createObjectURL(file));
      setAnalysis(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const handleUpload = async () => {
    if (!preview) return;

    setUploading(true);
    setUploadProgress(0);
    setError(null);

    try {
      // Simuler le progrès
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 10;
        });
      }, 200);

      // Récupérer le fichier depuis la preview
      const response = await fetch(preview);
      const blob = await response.blob();
      const file = new File([blob], 'skin_analysis.jpg', { type: 'image/jpeg' });

      const result = await apiService.uploadSkinAnalysis(file);
      setAnalysis(result.data);
      onAnalysisComplete(result.data);

      clearInterval(progressInterval);
      setUploadProgress(100);

    } catch (err: any) {
      setError(err.response?.data?.error || 'Erreur lors de l\'analyse de l\'image');
    } finally {
      setUploading(false);
    }
  };

  const resetUpload = () => {
    setPreview(null);
    setAnalysis(null);
    setError(null);
    setUploadProgress(0);
  };

  // Ouvrir la caméra
  const handleOpenCamera = async () => {
    try {
      setError(null);
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user' }, // Caméra frontale
        audio: false,
      });
      setStream(mediaStream);
      setCameraOpen(true);
    } catch (err: any) {
      const errorMessage = err.name === 'NotAllowedError' 
        ? 'Accès à la caméra refusé. Veuillez autoriser l\'accès à la caméra dans les paramètres de votre navigateur.'
        : err.name === 'NotFoundError'
        ? 'Aucune caméra trouvée sur votre appareil.'
        : 'Impossible d\'accéder à la caméra. Veuillez vérifier vos paramètres.';
      setError(errorMessage);
      console.error('Erreur d\'accès à la caméra:', err);
      setCameraOpen(false);
    }
  };

  // Fermer la caméra
  const handleCloseCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setCameraOpen(false);
  };

  // Connecter le stream vidéo à l'élément video
  useEffect(() => {
    if (stream && cameraOpen) {
      console.log('Stream disponible, connexion à la vidéo...');
      
      // Vérifier que le stream est toujours actif
      const videoTrack = stream.getVideoTracks()[0];
      if (!videoTrack || videoTrack.readyState !== 'live') {
        console.warn('Stream vidéo pas actif:', videoTrack?.readyState);
        return;
      }
      
      // Attendre que le Dialog soit complètement monté et que le videoRef soit disponible
      const timer = setTimeout(() => {
        const video = videoRef.current;
        if (video && stream) {
          console.log('Assignation du stream à la vidéo');
          
          // S'assurer que le stream n'est pas déjà assigné
          if (video.srcObject !== stream) {
            video.srcObject = stream;
          }
          
          // Attendre que les métadonnées soient chargées
          const handleLoadedMetadata = () => {
            console.log('Métadonnées chargées, démarrage de la lecture');
            if (video) {
              video.play().catch(err => {
                console.error('Erreur lors de la lecture de la vidéo:', err);
              });
            }
          };
          
          // Nettoyer l'ancien listener s'il existe
          if (metadataHandlerRef.current) {
            video.removeEventListener('loadedmetadata', metadataHandlerRef.current);
          }
          
          metadataHandlerRef.current = handleLoadedMetadata;
          video.addEventListener('loadedmetadata', handleLoadedMetadata);
          
          // Vérifier si la vidéo peut déjà jouer
          if (video.readyState >= 2) {
            console.log('Vidéo déjà prête, démarrage immédiat');
            video.play().catch(err => {
              console.error('Erreur lors de la lecture immédiate:', err);
            });
          } else {
            // Forcer la lecture immédiatement aussi
            video.play().catch(err => {
              console.error('Erreur lors de la lecture immédiate:', err);
            });
          }
        } else {
          console.warn('videoRef.current n\'est pas disponible');
        }
      }, 500); // Augmenté à 500ms pour être sûr
      
      return () => {
        clearTimeout(timer);
        const video = videoRef.current;
        if (video && metadataHandlerRef.current) {
          video.removeEventListener('loadedmetadata', metadataHandlerRef.current);
          metadataHandlerRef.current = null;
        }
      };
    }
  }, [stream, cameraOpen]);

  // Capturer la photo depuis la caméra
  const handleCapturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const context = canvas.getContext('2d');

      if (context && video.videoWidth > 0 && video.videoHeight > 0) {
        // Définir la taille du canvas à la taille de la vidéo
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Dessiner l'image de la vidéo sur le canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convertir le canvas en blob puis en File
        canvas.toBlob((blob) => {
          if (blob) {
            const file = new File([blob], 'camera_capture.jpg', { type: 'image/jpeg' });
            const previewUrl = URL.createObjectURL(file);
            setPreview(previewUrl);
            handleCloseCamera();
          }
        }, 'image/jpeg', 0.95);
      }
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Typography variant="h4" gutterBottom align="center" sx={{ mb: 4 }}>
        📸 Analyse de Votre Peau
      </Typography>

      {!preview ? (
        <>
          <Paper
            {...getRootProps()}
            sx={{
              p: 4,
              textAlign: 'center',
              border: '2px dashed',
              borderColor: isDragActive ? 'primary.main' : 'grey.300',
              backgroundColor: isDragActive ? 'primary.50' : 'background.paper',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              '&:hover': {
                borderColor: 'primary.main',
                backgroundColor: 'primary.50',
              },
            }}
          >
            <input {...getInputProps()} />
            <UploadIcon sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              {isDragActive ? 'Déposez votre image ici' : 'Glissez-déposez votre image ou cliquez pour sélectionner'}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Formats acceptés: JPEG, PNG (max 10MB)
            </Typography>
            <Button
              variant="outlined"
              startIcon={<CameraIcon />}
              sx={{ mt: 1 }}
            >
              Choisir une image
            </Button>
          </Paper>
          
          {/* Bouton séparé pour la caméra */}
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
            <Button
              variant="contained"
              startIcon={<VideocamIcon />}
              onClick={(e) => {
                e.stopPropagation();
                handleOpenCamera();
              }}
              sx={{ 
                bgcolor: 'primary.main',
                px: 4,
                py: 1.5,
                fontSize: '1rem',
                '&:hover': {
                  bgcolor: 'primary.dark',
                },
              }}
            >
              Prendre une photo avec la caméra
            </Button>
          </Box>
        </>
      ) : (
        <Card>
          <CardMedia
            component="img"
            height="400"
            image={preview || undefined}
            alt="Aperçu de l'image"
            sx={{ objectFit: 'cover' }}
          />
          <CardContent>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            {uploading && (
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" gutterBottom>
                  Analyse en cours... {uploadProgress}%
                </Typography>
                <LinearProgress variant="determinate" value={uploadProgress} />
              </Box>
            )}

            {analysis && (
              <Alert severity="success" sx={{ mb: 2 }} icon={<CheckIcon />}>
                Analyse terminée avec succès !
              </Alert>
            )}

            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
              {!analysis && (
                <Button
                  variant="contained"
                  onClick={handleUpload}
                  disabled={uploading}
                  startIcon={<UploadIcon />}
                >
                  {uploading ? 'Analyse en cours...' : 'Analyser la peau'}
                </Button>
              )}
              
              <Button
                variant="outlined"
                onClick={resetUpload}
                disabled={uploading}
              >
                Nouvelle image
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}

      {analysis && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6" gutterBottom>
            Résultats de l'analyse
          </Typography>
          <Paper sx={{ p: 2 }}>
            <Typography variant="body1">
              <strong>Type de peau détecté:</strong> {analysis.skin_type_prediction || 'Non déterminé'}
            </Typography>
            {analysis.skin_type_confidence && (
              <Typography variant="body2" color="text.secondary">
                Confiance: {(analysis.skin_type_confidence * 100).toFixed(1)}%
              </Typography>
            )}
            
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Problèmes détectés:
              </Typography>
              {analysis.acne_detected && (
                <Typography variant="body2" color="error">
                  • Acné ({analysis.acne_severity})
                </Typography>
              )}
              {analysis.wrinkles_detected && (
                <Typography variant="body2" color="warning.main">
                  • Rides ({analysis.wrinkles_severity})
                </Typography>
              )}
              {analysis.dark_spots_detected && (
                <Typography variant="body2" color="info.main">
                  • Taches sombres ({analysis.dark_spots_severity})
                </Typography>
              )}
              {analysis.redness_detected && (
                <Typography variant="body2" color="error">
                  • Rougeurs ({analysis.redness_severity})
                </Typography>
              )}
              {!analysis.acne_detected && !analysis.wrinkles_detected && 
               !analysis.dark_spots_detected && !analysis.redness_detected && (
                <Typography variant="body2" color="success.main">
                  Aucun problème majeur détecté
                </Typography>
              )}
            </Box>
          </Paper>
        </Box>
      )}

      {/* Dialog pour la caméra */}
      <Dialog
        open={cameraOpen}
        onClose={handleCloseCamera}
        maxWidth="md"
        fullWidth
        disableEnforceFocus
        disableAutoFocus
        disableRestoreFocus
        TransitionProps={{
          onEntered: () => {
            // Une fois le Dialog complètement monté, assigner le stream
            if (stream && videoRef.current) {
              console.log('Dialog monté, assignation du stream via onEntered');
              const video = videoRef.current;
              if (video.srcObject !== stream) {
                video.srcObject = stream;
              }
              video.play().catch(err => {
                console.error('Erreur de lecture dans onEntered:', err);
              });
            }
          }
        }}
        PaperProps={{
          sx: {
            bgcolor: 'black',
          }
        }}
      >
        <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: 'white' }}>
          Prendre une photo
          <IconButton onClick={handleCloseCamera} sx={{ color: 'white' }}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent sx={{ p: 0, position: 'relative', display: 'flex', justifyContent: 'center', bgcolor: 'black', minHeight: '400px' }}>
          <Box sx={{ position: 'relative', width: '100%', maxHeight: '70vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            {!stream ? (
              <Box sx={{ textAlign: 'center', color: 'white', p: 4 }}>
                <Typography variant="h6" gutterBottom>
                  Chargement de la caméra...
                </Typography>
                <Typography variant="body2">
                  Veuillez autoriser l'accès à la caméra
                </Typography>
              </Box>
            ) : (
              <>
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  style={{
                    width: '100%',
                    height: 'auto',
                    maxHeight: '70vh',
                    objectFit: 'contain',
                    display: 'block',
                    backgroundColor: '#000',
                  }}
                  onLoadedMetadata={() => {
                    console.log('onLoadedMetadata déclenché');
                    if (videoRef.current) {
                      videoRef.current.play().catch(err => {
                        console.error('Erreur de lecture dans onLoadedMetadata:', err);
                      });
                    }
                  }}
                  onCanPlay={() => {
                    console.log('onCanPlay déclenché - vidéo prête');
                    if (videoRef.current) {
                      console.log('Dimensions vidéo:', videoRef.current.videoWidth, 'x', videoRef.current.videoHeight);
                      console.log('Stream actif:', videoRef.current.srcObject ? 'Oui' : 'Non');
                      videoRef.current.play().catch(err => {
                        console.error('Erreur de lecture dans onCanPlay:', err);
                      });
                    }
                  }}
                  onPlay={() => {
                    console.log('✅ Vidéo en cours de lecture!');
                  }}
                  onError={(e) => {
                    console.error('Erreur vidéo:', e);
                  }}
                />
                <canvas ref={canvasRef} style={{ display: 'none' }} />
              </>
            )}
          </Box>
        </DialogContent>
        <DialogActions sx={{ justifyContent: 'center', pb: 3, bgcolor: 'black' }}>
          <Button
            variant="contained"
            startIcon={<CameraAltIcon />}
            onClick={handleCapturePhoto}
            sx={{
              bgcolor: 'primary.main',
              color: 'white',
              px: 4,
              py: 1.5,
              fontSize: '1.1rem',
              '&:hover': {
                bgcolor: 'primary.dark',
              },
            }}
          >
            Capturer la photo
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default UploadForm;




