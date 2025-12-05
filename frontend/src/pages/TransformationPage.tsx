import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Slider,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  FormLabel,
  LinearProgress,
  Alert,
  Divider,
  IconButton,
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import { apiService } from '../services/api';
import { SkinAnalysis } from '../types';

const TransformationPage: React.FC = () => {
  const { analysisId } = useParams<{ analysisId: string }>();
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState<SkinAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Parameters - Adjusted defaults for natural results
  const [filterType, setFilterType] = useState<string>('Moyen');
  const [skinSmoothness, setSkinSmoothness] = useState<number>(0.50);
  const [defectReduction, setDefectReduction] = useState<number>(0.50);
  const [brightness, setBrightness] = useState<number>(0.40);
  const [glow, setGlow] = useState<number>(0.35);
  
  // Generated images (base64 from backend)
  const [imgAvant, setImgAvant] = useState<string | null>(null);
  const [img1Mois, setImg1Mois] = useState<string | null>(null);
  const [img2Mois, setImg2Mois] = useState<string | null>(null);
  const [img3Mois, setImg3Mois] = useState<string | null>(null);
  const [progressionImage, setProgressionImage] = useState<string | null>(null);
  
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    loadAnalysis();
  }, [analysisId]);

  const loadAnalysis = async () => {
    try {
      setLoading(true);
      if (!analysisId) {
        setError('ID d\'analyse manquant');
        return;
      }
      const response = await apiService.getSkinAnalysis(parseInt(analysisId));
      setAnalysis(response.data);
      
      // Set original image URL for display
      const imageUrl = response.data.image.startsWith('http') 
        ? response.data.image 
        : `http://127.0.0.1:8000${response.data.image}`;
      setImgAvant(imageUrl);
    } catch (err: any) {
      setError('Erreur lors du chargement de l\'analyse');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Create 3-month progression using backend API
  const createProgression = async () => {
    if (!analysis || !analysisId) return;
    
    setProcessing(true);
    setError(null);
    
    try {
      const response = await apiService.createTransformation(
        parseInt(analysisId),
        filterType,
        skinSmoothness,
        defectReduction,
        brightness,
        glow
      );
      
      const { avant, '1_mois': img1M, '2_mois': img2M, '3_mois': img3M } = response.data;
      
      setImgAvant(avant);
      setImg1Mois(img1M);
      setImg2Mois(img2M);
      setImg3Mois(img3M);
      
      // Create progression image
      createProgressionImage(avant, img1M, img2M, img3M);
      
    } catch (err: any) {
      console.error('Erreur lors de la création de la transformation:', err);
      setError(err.response?.data?.error || 'Erreur lors de la création de la transformation');
    } finally {
      setProcessing(false);
    }
  };

  // Create side-by-side progression image
  const createProgressionImage = (
    avant: string,
    img1M: string,
    img2M: string,
    img3M: string
  ) => {
    if (!canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    const size = { width: 280, height: 320 };
    const margin = 10;
    const totalWidth = size.width * 4 + margin * 5;
    const totalHeight = size.height + 60;
    
    canvas.width = totalWidth;
    canvas.height = totalHeight;
    
    // Dark background
    ctx.fillStyle = '#1e1e1e';
    ctx.fillRect(0, 0, totalWidth, totalHeight);
    
    // Load and draw images
    const images = [
      { src: avant, label: 'AVANT' },
      { src: img1M, label: '1 MOIS' },
      { src: img2M, label: '2 MOIS' },
      { src: img3M, label: '3 MOIS' },
    ];
    
    let loaded = 0;
    images.forEach((imgData, index) => {
      const img = new Image();
      img.onload = () => {
        try {
          const x = margin + (size.width + margin) * index;
          const y = 40;
          
          ctx.drawImage(img, x, y, size.width, size.height);
          
          // Draw label
          ctx.fillStyle = '#ffc864';
          ctx.font = 'bold 16px Arial';
          ctx.textAlign = 'center';
          ctx.fillText(imgData.label, x + size.width / 2, 25);
          
          loaded++;
          if (loaded === images.length) {
            // Try to export
            try {
              const dataUrl = canvas.toDataURL('image/png');
              setProgressionImage(dataUrl);
            } catch (exportError) {
              console.error('Error exporting progression image:', exportError);
            }
          }
        } catch (drawError) {
          console.error('Error drawing image:', drawError);
        }
      };
      img.onerror = () => {
        console.error('Failed to load image:', imgData.label);
      };
      img.src = imgData.src;
    });
  };

  // Download image
  const downloadImage = (imageSrc: string, filename: string) => {
    const link = document.createElement('a');
    link.href = imageSrc;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Chargement de l'analyse...
        </Typography>
      </Container>
    );
  }

  if (error || !analysis) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error">{error || 'Analyse non trouvée'}</Alert>
        <Button startIcon={<BackIcon />} onClick={() => navigate(-1)} sx={{ mt: 2 }}>
          Retour
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
        <IconButton onClick={() => navigate(-1)} sx={{ mr: 2 }}>
          <BackIcon />
        </IconButton>
        <Typography variant="h4" component="h1">
          📊 Transformation Peau - Progression 3 Mois
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '300px 1fr' }, gap: 3 }}>
        {/* Sidebar - Parameters */}
        <Box>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                ⚙️ Paramètres de Transformation
              </Typography>
              
              <FormControl component="fieldset" sx={{ mb: 3 }}>
                <FormLabel component="legend">Intensité du filtre</FormLabel>
                <RadioGroup
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                >
                  <FormControlLabel value="Léger" control={<Radio />} label="Léger" />
                  <FormControlLabel value="Moyen" control={<Radio />} label="Moyen" />
                  <FormControlLabel value="Fort" control={<Radio />} label="Fort" />
                  <FormControlLabel value="Extrême" control={<Radio />} label="Extrême" />
                </RadioGroup>
              </FormControl>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="subtitle2" gutterBottom>
                Ajustements
              </Typography>
              
              <Box sx={{ mb: 3 }}>
                <Typography gutterBottom>🔹 Lissage peau</Typography>
                <Slider
                  value={skinSmoothness}
                  onChange={(_, value) => setSkinSmoothness(value as number)}
                  min={0}
                  max={1}
                  step={0.1}
                  marks
                />
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <Typography gutterBottom>💊 Réduction défauts</Typography>
                <Slider
                  value={defectReduction}
                  onChange={(_, value) => setDefectReduction(value as number)}
                  min={0}
                  max={1}
                  step={0.1}
                  marks
                />
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <Typography gutterBottom>☀️ Luminosité</Typography>
                <Slider
                  value={brightness}
                  onChange={(_, value) => setBrightness(value as number)}
                  min={0}
                  max={1}
                  step={0.1}
                  marks
                />
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <Typography gutterBottom>✨ Éclat</Typography>
                <Slider
                  value={glow}
                  onChange={(_, value) => setGlow(value as number)}
                  min={0}
                  max={1}
                  step={0.1}
                  marks
                />
              </Box>
              
              <Button
                variant="contained"
                fullWidth
                onClick={createProgression}
                disabled={processing || !analysis}
                sx={{ mt: 2 }}
              >
                {processing ? '⏳ Calcul en cours...' : '🎯 Voir Progression 3 Mois'}
              </Button>
            </CardContent>
          </Card>
        </Box>

        {/* Main Content */}
        <Box>
          {processing && <LinearProgress sx={{ mb: 2 }} />}
          
          {/* Image originale */}
          {analysis && (
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  📸 Image Originale
                </Typography>
                <Box sx={{ textAlign: 'center' }}>
                  <img
                    src={analysis.image.startsWith('http') ? analysis.image : `http://127.0.0.1:8000${analysis.image}`}
                    alt="Image originale"
                    style={{ maxWidth: '100%', height: 'auto', borderRadius: '8px' }}
                    onError={(e) => {
                      console.error('Erreur de chargement de l\'image:', e);
                      setError('Erreur lors du chargement de l\'image');
                    }}
                  />
                </Box>
              </CardContent>
            </Card>
          )}
          
          {progressionImage && (
            <>
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    📊 Transformation Progressive (3 Mois)
                  </Typography>
                  <Box sx={{ textAlign: 'center' }}>
                    <img
                      src={progressionImage}
                      alt="Progression 3 mois"
                      style={{ maxWidth: '100%', height: 'auto' }}
                    />
                  </Box>
                </CardContent>
              </Card>
              
              <Divider sx={{ my: 3 }} />
              
              {/* Detailed comparisons */}
              <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' }, gap: 2, mb: 3 }}>
                <Box>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        1️⃣ 1 Mois
                      </Typography>
                      {imgAvant && img1Mois && (
                        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="caption" display="block" textAlign="center">
                              AVANT
                            </Typography>
                            <img
                              src={imgAvant}
                              alt="Avant"
                              style={{ width: '100%', height: 'auto' }}
                            />
                          </Box>
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="caption" display="block" textAlign="center" color="primary">
                              1 MOIS
                            </Typography>
                            <img
                              src={img1Mois}
                              alt="1 Mois"
                              style={{ width: '100%', height: 'auto' }}
                            />
                          </Box>
                        </Box>
                      )}
                      {img1Mois && (
                        <Button
                          fullWidth
                          variant="outlined"
                          startIcon={<DownloadIcon />}
                          onClick={() => downloadImage(img1Mois, '1_mois.png')}
                        >
                          Télécharger
                        </Button>
                      )}
                    </CardContent>
                  </Card>
                </Box>
                
                <Box>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        2️⃣ 2 Mois
                      </Typography>
                      {imgAvant && img2Mois && (
                        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="caption" display="block" textAlign="center">
                              AVANT
                            </Typography>
                            <img
                              src={imgAvant}
                              alt="Avant"
                              style={{ width: '100%', height: 'auto' }}
                            />
                          </Box>
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="caption" display="block" textAlign="center" color="primary">
                              2 MOIS
                            </Typography>
                            <img
                              src={img2Mois}
                              alt="2 Mois"
                              style={{ width: '100%', height: 'auto' }}
                            />
                          </Box>
                        </Box>
                      )}
                      {img2Mois && (
                        <Button
                          fullWidth
                          variant="outlined"
                          startIcon={<DownloadIcon />}
                          onClick={() => downloadImage(img2Mois, '2_mois.png')}
                        >
                          Télécharger
                        </Button>
                      )}
                    </CardContent>
                  </Card>
                </Box>
                
                <Box>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        3️⃣ 3 Mois
                      </Typography>
                      {imgAvant && img3Mois && (
                        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="caption" display="block" textAlign="center">
                              AVANT
                            </Typography>
                            <img
                              src={imgAvant}
                              alt="Avant"
                              style={{ width: '100%', height: 'auto' }}
                            />
                          </Box>
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="caption" display="block" textAlign="center" color="primary">
                              3 MOIS
                            </Typography>
                            <img
                              src={img3Mois}
                              alt="3 Mois"
                              style={{ width: '100%', height: 'auto' }}
                            />
                          </Box>
                        </Box>
                      )}
                      {img3Mois && (
                        <Button
                          fullWidth
                          variant="outlined"
                          startIcon={<DownloadIcon />}
                          onClick={() => downloadImage(img3Mois, '3_mois.png')}
                        >
                          Télécharger
                        </Button>
                      )}
                    </CardContent>
                  </Card>
                </Box>
              </Box>
              
              {progressionImage && (
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      📥 Télécharger la progression complète
                    </Typography>
                    <Button
                      variant="contained"
                      startIcon={<DownloadIcon />}
                      onClick={() => downloadImage(progressionImage, 'progression_3mois.png')}
                    >
                      Télécharger Progression
                    </Button>
                  </CardContent>
                </Card>
              )}
            </>
          )}
          
          {!progressionImage && !processing && (
            <Card>
              <CardContent>
                <Typography variant="body1" textAlign="center" color="text.secondary">
                  👆 Ajustez les paramètres et cliquez sur "Voir Progression 3 Mois" pour générer la transformation
                </Typography>
              </CardContent>
            </Card>
          )}
        </Box>
      </Box>
      
      {/* Hidden canvas for progression image creation */}
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </Container>
  );
};

export default TransformationPage;
