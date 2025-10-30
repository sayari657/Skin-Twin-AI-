import React, { useState, useCallback } from 'react';
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
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  PhotoCamera as CameraIcon,
  CheckCircle as CheckIcon,
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

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Typography variant="h4" gutterBottom align="center" sx={{ mb: 4 }}>
        📸 Analyse de Votre Peau
      </Typography>

      {!preview ? (
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
      ) : (
        <Card>
          <CardMedia
            component="img"
            height="400"
            image={preview}
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
    </Box>
  );
};

export default UploadForm;




