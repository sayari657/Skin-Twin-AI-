import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Chip,
  Alert,
  LinearProgress,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Tabs,
  Tab,
} from '@mui/material';
import ResultsChatAI from '../components/ResultsChatAI';
import AnalysisReport from '../components/AnalysisReport';
import DetectedZonesOverlay from '../components/DetectedZonesOverlay';
import {
  ArrowBack as BackIcon,
  Psychology as AIIcon,
  ShoppingCart as ProductIcon,
  Timeline as TimelineIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { apiService } from '../services/api';
import { SkinAnalysis } from '../types';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as ChartTooltip, ResponsiveContainer } from 'recharts';
import { IconButton, Tooltip } from '@mui/material';
import ShareIcon from '@mui/icons-material/Share';
import ZoomInIcon from '@mui/icons-material/ZoomIn';
import CloseIcon from '@mui/icons-material/Close';

// Imports des composants med/
import { QuickInfo, DiagnosticSection, AdviceSection } from '../med';
import { DiagnosisResult, QuickInfo as QuickInfoType, DiagnosticData } from '../med/types/diagnostic.types';

const ResultsPage: React.FC = () => {
  const { analysisId } = useParams<{ analysisId: string }>();
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState<SkinAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [imageDeleted, setImageDeleted] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [shareDialogOpen, setShareDialogOpen] = useState(false);
  const [showAnnotatedImage, setShowAnnotatedImage] = useState(true); // Afficher l'image annotée par défaut
  const [imageViewerOpen, setImageViewerOpen] = useState(false);
  const [imageViewerTab, setImageViewerTab] = useState(0);
  const [allAnalyses, setAllAnalyses] = useState<SkinAnalysis[]>([]);
  const [skinHistoryData, setSkinHistoryData] = useState<Array<{date: string, acne: number, rides: number, taches: number, rougeurs: number}>>([]);
  const [diagnosisData, setDiagnosisData] = useState<DiagnosisResult | null>(null);
  const [loadingDiagnosis, setLoadingDiagnosis] = useState(false);

  // Fonction pour convertir la sévérité en valeur numérique
  const severityToNumber = (severity?: string, detected?: boolean): number => {
    if (!detected) return 0;
    switch (severity) {
      case 'LOW': return 1;
      case 'MODERATE': return 2;
      case 'HIGH': return 3;
      default: return detected ? 1 : 0;
    }
  };

  // Fonction pour transformer les analyses en données pour le graphique
  const transformAnalysesToChartData = (analyses: SkinAnalysis[]) => {
    return analyses
      .sort((a, b) => new Date(a.analysis_date).getTime() - new Date(b.analysis_date).getTime())
      .map(analysis => {
        const date = new Date(analysis.analysis_date);
        const formattedDate = date.toISOString().split('T')[0]; // Format YYYY-MM-DD
        
        return {
          date: formattedDate,
          acne: severityToNumber(analysis.acne_severity, analysis.acne_detected),
          rides: severityToNumber(analysis.wrinkles_severity, analysis.wrinkles_detected),
          taches: severityToNumber(analysis.dark_spots_severity, analysis.dark_spots_detected),
          rougeurs: severityToNumber(analysis.redness_severity, analysis.redness_detected),
        };
      });
  };

  // Charger toutes les analyses de l'utilisateur pour le graphique
  const loadAllAnalyses = async () => {
    try {
      const response = await apiService.getUserAnalyses();
      const analyses = response.data;
      setAllAnalyses(analyses);
      
      // Transformer les données pour le graphique
      const chartData = transformAnalysesToChartData(analyses);
      setSkinHistoryData(chartData);
    } catch (err: any) {
      console.error('Erreur lors du chargement de l\'historique:', err);
      // En cas d'erreur, utiliser des données vides
      setSkinHistoryData([]);
    }
  };

  useEffect(() => {
    if (analysisId) {
      loadAnalysis();
    }
  }, [analysisId]);

  // Charger l'historique des analyses pour le graphique
  useEffect(() => {
    loadAllAnalyses();
  }, []);

  // Mettre à jour le graphique quand une nouvelle analyse est chargée
  useEffect(() => {
    if (analysis && allAnalyses.length > 0) {
      // Vérifier si l'analyse actuelle est déjà dans la liste
      const exists = allAnalyses.some(a => a.id === analysis.id);
      if (!exists) {
        // Recharger toutes les analyses pour inclure la nouvelle
        loadAllAnalyses();
      }
    }
  }, [analysis]);

  const loadAnalysis = async () => {
    try {
      setLoading(true);
      const response = await apiService.getSkinAnalysis(parseInt(analysisId!));
      console.log('Données de l\'analyse:', response.data);
      console.log('URL de l\'image:', response.data.image);
      setAnalysis(response.data);
    } catch (err: any) {
      setError('Erreur lors du chargement de l\'analyse');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteImage = () => {
    setDeleteDialogOpen(true);
  };

  const handleConfirmDelete = () => {
    setImageDeleted(true);
    setDeleteDialogOpen(false);
    // Optionnel : appeler une API pour supprimer l'image du serveur
    console.log('Image supprimée par l\'utilisateur');
  };

  const handleCancelDelete = () => {
    setDeleteDialogOpen(false);
  };

  const handleRestoreImage = () => {
    setImageDeleted(false);
    console.log('Image restaurée par l\'utilisateur');
  };

  const getSkinTypeColor = (skinType?: string) => {
    const colors: { [key: string]: string } = {
      'DRY': 'error',
      'OILY': 'warning',
      'COMBINATION': 'info',
      'NORMAL': 'success',
      'SENSITIVE': 'secondary',
    };
    return colors[skinType || ''] || 'default';
  };

  const getSkinTypeLabel = (skinType?: string) => {
    const labels: { [key: string]: string } = {
      'DRY': 'Sèche',
      'OILY': 'Grasse',
      'COMBINATION': 'Mixte',
      'NORMAL': 'Normale',
      'SENSITIVE': 'Sensible',
    };
    return labels[skinType || ''] || 'Non déterminé';
  };

  const getSeverityColor = (severity?: string) => {
    const colors: { [key: string]: string } = {
      'LOW': 'success',
      'MODERATE': 'warning',
      'HIGH': 'error',
    };
    return colors[severity || ''] || 'default';
  };

  // Fonction pour transformer SkinAnalysis en DiagnosisResult pour les composants med/
  const transformToDiagnosisResult = (analysis: SkinAnalysis): DiagnosisResult => {
    // Construire la liste des troubles détectés
    const detectedTroubles: Array<{ name: string; confidence: number; severity?: 'LOW' | 'MODERATE' | 'HIGH' }> = [];
    
    if (analysis.acne_detected) {
      detectedTroubles.push({
        name: 'Acné',
        confidence: analysis.acne_confidence || 0.1,
        severity: (analysis.acne_severity as 'LOW' | 'MODERATE' | 'HIGH') || 'LOW',
      });
    }
    if (analysis.wrinkles_detected) {
      detectedTroubles.push({
        name: 'Rides',
        confidence: analysis.wrinkles_confidence || 0.1,
        severity: (analysis.wrinkles_severity as 'LOW' | 'MODERATE' | 'HIGH') || 'LOW',
      });
    }
    if (analysis.dark_spots_detected) {
      detectedTroubles.push({
        name: 'Taches sombres',
        confidence: analysis.dark_spots_confidence || 0.1,
        severity: (analysis.dark_spots_severity as 'LOW' | 'MODERATE' | 'HIGH') || 'LOW',
      });
    }
    if (analysis.redness_detected) {
      detectedTroubles.push({
        name: 'Rougeurs',
        confidence: analysis.redness_confidence || 0.1,
        severity: (analysis.redness_severity as 'LOW' | 'MODERATE' | 'HIGH') || 'LOW',
      });
    }

    // Mapper le type de peau
    const skinTypeMap: { [key: string]: 'Dry' | 'Normal' | 'Oily' } = {
      'DRY': 'Dry',
      'NORMAL': 'Normal',
      'OILY': 'Oily',
      'COMBINATION': 'Normal', // Fallback
      'SENSITIVE': 'Normal', // Fallback
    };
    const skinType = skinTypeMap[analysis.skin_type_prediction || 'NORMAL'] || 'Normal';

    // Construire le texte du diagnostic
    const problemsList = detectedTroubles.map(t => t.name).join(', ') || 'Aucun problème majeur';
    const diagnosticText = `L'examen dermatologique révèle une peau de type ${getSkinTypeLabel(analysis.skin_type_prediction)} avec une confiance de ${((analysis.skin_type_confidence || 0) * 100).toFixed(1)}%. ${problemsList !== 'Aucun problème majeur' ? `Les problèmes suivants ont été détectés : ${problemsList}.` : 'Votre peau semble en bonne santé générale.'} ${analysis.skin_type_confidence && analysis.skin_type_confidence > 0.9 ? 'La qualité de votre peau est excellente.' : 'Quelques améliorations peuvent être apportées avec les bons produits.'}`;

    // Construire les conseils pratiques
    const conseils: string[] = [];
    if (analysis.acne_detected) {
      conseils.push('Utiliser un nettoyant doux matin et soir pour réduire l\'acné');
      conseils.push('Éviter de toucher le visage avec les mains sales');
    }
    if (analysis.wrinkles_detected) {
      conseils.push('Appliquer une crème hydratante riche en acide hyaluronique');
      conseils.push('Protéger la peau du soleil avec un écran solaire SPF 30+');
    }
    if (analysis.dark_spots_detected) {
      conseils.push('Utiliser des produits contenant de la vitamine C pour éclaircir les taches');
      conseils.push('Éviter l\'exposition excessive au soleil');
    }
    if (conseils.length === 0) {
      conseils.push('Maintenir une routine de soins quotidienne');
      conseils.push('Boire suffisamment d\'eau pour hydrater la peau');
      conseils.push('Dormir au moins 7-8 heures par nuit');
    }

    // Construire les recommandations (sera rempli par l'API si disponible)
    const recommendations: Array<{ categorie: string; produits: Array<{ nom: string; description_detaillee: string; links?: Array<{ title: string; link: string; snippet: string }> }> }> = [];

    return {
      quickInfo: {
        skinType: {
          type: skinType,
          confidence: analysis.skin_type_confidence || 0.5,
        },
        confidence: analysis.skin_type_confidence || 0.5,
        detectedTroubles,
      },
      diagnostic: {
        diagnostic: diagnosticText,
        skinType: getSkinTypeLabel(analysis.skin_type_prediction),
        problems: detectedTroubles.map(t => t.name),
      },
      conseils_pratiques: conseils,
      recommendations,
      annotated_image: analysis.annotated_image,
      diagnosis_id: analysis.id,
      created_at: analysis.analysis_date,
    };
  };

  // Charger les recommandations depuis l'API
  useEffect(() => {
    const loadRecommendations = async () => {
      if (!analysis) return;
      
      setLoadingDiagnosis(true);
      try {
        // Transformer les données existantes
        const diagnosisResult = transformToDiagnosisResult(analysis);
        
        // Essayer de charger les recommandations depuis l'API
        try {
          const recResponse = await apiService.getRecommendations(analysis.id);
          if (recResponse.data && Array.isArray(recResponse.data) && recResponse.data.length > 0) {
            // Transformer les recommandations au format attendu
            type ProductItem = {
              nom: string;
              description_detaillee: string;
              links?: Array<{ title: string; link: string; snippet: string }>;
            };
            const categories: { [key: string]: { [productKey: string]: ProductItem } } = {};
            
            // Première passe : collecter tous les produits et leurs liens
            recResponse.data.forEach((rec: any) => {
              const product = rec.product || rec;
              const category = product.category || 'Autres';
              const categoryLabel = category === 'CLEANSER' ? 'Nettoyant visage' :
                                   category === 'MOISTURIZER' ? 'Hydratant' :
                                   category === 'SERUM' ? 'Sérum' :
                                   category === 'SUNSCREEN' ? 'Protection solaire' :
                                   category === 'TREATMENT' ? 'Traitement' :
                                   category === 'MASK' ? 'Masque' :
                                   category === 'TONER' ? 'Tonique' :
                                   category === 'EXFOLIANT' ? 'Exfoliant' : 'Autres';
              
              if (!categories[categoryLabel]) {
                categories[categoryLabel] = {};
              }
              
              // Créer une clé unique basée sur le nom du produit (normalisé)
              // Normaliser : enlever espaces multiples, caractères spéciaux, convertir en minuscules
              const normalizeProductName = (name: string): string => {
                return name
                  .trim()
                  .toLowerCase()
                  .replace(/\s+/g, ' ') // Remplacer espaces multiples par un seul
                  .replace(/[^\w\s]/g, '') // Enlever caractères spéciaux
                  .trim();
              };
              const productName = normalizeProductName(product.name || product.brand || 'Produit');
              const productKey = productName;
              
              // Si le produit existe déjà, ajouter le lien à la liste existante
              if (categories[categoryLabel][productKey]) {
                const existingProduct = categories[categoryLabel][productKey];
                // Utiliser le champ 'sources' du backend qui contient tous les liens
                const sources = product.sources || [];
                if (product.url && product.source_site) {
                  // Ajouter aussi le lien principal si pas déjà dans sources
                  const mainLinkExists = sources.some((s: any) => s.url === product.url);
                  if (!mainLinkExists) {
                    sources.push({
                      url: product.url,
                      source_site: product.source_site,
                      price: product.price,
                      description: product.description || product.name || ''
                    });
                  }
                }
                
                // Convertir sources en format links pour l'affichage
                const allLinks = sources.map((source: any) => ({
                  title: `Acheter sur ${source.source_site}`,
                  link: source.url,
                  snippet: source.description || product.description || product.name || '',
                }));
                
                // Éviter les doublons de liens
                const uniqueLinks = allLinks.filter((link: any, index: number, self: any[]) =>
                  index === self.findIndex((l: any) => l.link === link.link)
                );
                
                existingProduct.links = uniqueLinks.length > 0 ? uniqueLinks : existingProduct.links;
              } else {
                // Créer un nouveau produit
                // Utiliser le champ 'sources' du backend qui contient tous les liens
                const sources = product.sources || [];
                if (product.url && product.source_site) {
                  // Ajouter le lien principal si pas déjà dans sources
                  const mainLinkExists = sources.some((s: any) => s.url === product.url);
                  if (!mainLinkExists) {
                    sources.push({
                      url: product.url,
                      source_site: product.source_site,
                      price: product.price,
                      description: product.description || product.name || ''
                    });
                  }
                }
                
                // Convertir sources en format links pour l'affichage
                const links = sources.map((source: any) => ({
                  title: `Acheter sur ${source.source_site}`,
                  link: source.url,
                  snippet: source.description || product.description || product.name || '',
                }));
                
                categories[categoryLabel][productKey] = {
                  nom: product.name || product.brand || 'Produit',
                  description_detaillee: product.description || 'Produit recommandé pour votre type de peau',
                  links: links.length > 0 ? links : undefined,
                };
              }
            });
            
            // Convertir les objets en tableaux et trier les liens par site
            diagnosisResult.recommendations = Object.keys(categories).map(cat => ({
              categorie: cat,
              produits: Object.values(categories[cat]).map(product => ({
                ...product,
                // Trier les liens par nom de site pour une meilleure présentation
                links: product.links?.sort((a, b) => a.title.localeCompare(b.title)),
              })),
            }));
          }
        } catch (recError) {
          console.log('Recommandations non disponibles:', recError);
        }
        
        setDiagnosisData(diagnosisResult);
      } catch (err) {
        console.error('Erreur lors du chargement des données:', err);
      } finally {
        setLoadingDiagnosis(false);
      }
    };

    if (analysis) {
      loadRecommendations();
    }
  }, [analysis]);

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Chargement des résultats...
        </Typography>
      </Container>
    );
  }

  if (error || !analysis) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error || 'Analyse non trouvée'}
        </Alert>
        <Button
          variant="contained"
          startIcon={<BackIcon />}
          onClick={() => navigate('/dashboard')}
        >
          Retour au tableau de bord
        </Button>
      </Container>
    );
  }

  return (
    <>
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* DASHBOARD SUMMARY ADDED */}
      <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap', mb: 3 }}>
        <Card sx={{ minWidth: 220, background: 'linear-gradient(90deg, #b0e0e6,#2196f3 80%)', color: '#191970', boxShadow: '0 2px 14px #b0e0e655', borderRadius: 4 }}>
          <CardContent>
            <Typography variant="h6">Type de Peau</Typography>
            <Typography variant="h5" fontWeight="bold" sx={{ letterSpacing: 1 }}>{getSkinTypeLabel(analysis.skin_type_prediction)}</Typography>
            {analysis.skin_type_confidence && (
              <Typography variant="body2" color="#2292A4">Confiance: {(analysis.skin_type_confidence * 100).toFixed(1)}%</Typography>
            )}
          </CardContent>
        </Card>
        <Card sx={{ minWidth: 220, background: 'linear-gradient(90deg, #ffe082,#f57c00 90%)', color: '#4f2e00', boxShadow: '0 2px 14px #ffd18055', borderRadius: 4 }}>
          <CardContent>
            <Typography variant="h6">Problèmes détectés</Typography>
            <Typography variant="h5" fontWeight="bold" sx={{ letterSpacing: 1 }}>{[
            analysis.acne_detected ? 'Acné' : '',
            analysis.wrinkles_detected ? 'Rides' : '',
            analysis.dark_spots_detected ? 'Taches' : '',
            analysis.redness_detected ? 'Rougeurs' : ''
          ].filter(Boolean).join(', ') || 'Aucun'}</Typography>
          </CardContent>
        </Card>
        <Card sx={{ minWidth: 220, background: 'linear-gradient(90deg, #e8f5e9,#81c784 90%)', color: '#1b5e20', boxShadow: '0 2px 14px #a5d6a755', borderRadius: 4 }}>
          <CardContent>
            <Typography variant="h6">Date</Typography>
            <Typography variant="h5" fontWeight="bold">{new Date(analysis.analysis_date).toLocaleDateString('fr-FR')}</Typography>
          </CardContent>
        </Card>
      </Box>
      <Paper sx={{ p: 3, my: 2, background: 'linear-gradient(120deg,#e3f2fd 70%,#fafafa 100%)', borderRadius: 3, boxShadow: '0 2px 14px #b0e0e625' }}>
        <Typography variant="h6" fontWeight={700} sx={{ mb: 0.5, color: 'primary.dark' }}>
          ➤ Résumé IA
        </Typography>
        <Typography variant="body1" sx={{ lineHeight: 1.8, color: '#333' }}>
            {[
              analysis.acne_detected && `Acné (${getSeverityColor(analysis.acne_severity)})`,
              analysis.wrinkles_detected && `Rides (${getSeverityColor(analysis.wrinkles_severity)})`,
              analysis.dark_spots_detected && `Taches`,
              analysis.redness_detected && `Rougeurs`,
            ].filter(Boolean).join(', ') || 'Aucun problème majeur détecté.'}
          <br/>
          {analysis.skin_type_prediction && `Type de peau: ${getSkinTypeLabel(analysis.skin_type_prediction)}.`}
          {analysis.skin_type_confidence && ` (Confiance: ${(analysis.skin_type_confidence*100).toFixed(1)}%)`}
        </Typography>
      </Paper>
      <Box sx={{ mb: 4 }}>
        <Button
          startIcon={<BackIcon />}
          onClick={() => navigate('/dashboard')}
          sx={{ mb: 2 }}
        >
          Retour
        </Button>
        <Typography variant="h4" gutterBottom>
          📊 Résultats de l'Analyse
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Analyse effectuée le {new Date(analysis.analysis_date).toLocaleDateString('fr-FR')}
        </Typography>
      </Box>

      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
        {/* Image et type de peau */}
        <Box sx={{ flex: { xs: '1', md: '1' } }}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  📸 Image Analysée
                </Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  {analysis.annotated_image && (
                    <Button
                      variant={showAnnotatedImage ? "contained" : "outlined"}
                      size="small"
                      onClick={() => setShowAnnotatedImage(true)}
                      sx={{ fontSize: '0.75rem' }}
                    >
                      Zones détectées
                    </Button>
                  )}
                  <Button
                    variant={!showAnnotatedImage ? "contained" : "outlined"}
                    size="small"
                    onClick={() => setShowAnnotatedImage(false)}
                    sx={{ fontSize: '0.75rem' }}
                  >
                    Originale
                  </Button>
                  {analysis.image && !imageDeleted && (
                    <Button
                      variant="outlined"
                      color="error"
                      size="small"
                      startIcon={<DeleteIcon />}
                      onClick={handleDeleteImage}
                      sx={{ ml: 1 }}
                    >
                      Supprimer
                    </Button>
                  )}
                </Box>
              </Box>
              {analysis.image && !imageDeleted ? (
                <>
                  {showAnnotatedImage ? (
                    <>
                      <DetectedZonesOverlay
                        imageUrl={analysis.image}
                        analysis={analysis}
                        width="100%"
                        height={400}
                      />
                      <Box sx={{ mb: 2, p: 1.5, bgcolor: 'info.50', borderRadius: 1, mt: 2 }}>
                        <Typography variant="body2" color="info.dark" sx={{ fontWeight: 500 }}>
                          🔍 Zones détectées par l'IA :
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                          Les rectangles colorés indiquent les zones où des problèmes de peau ont été détectés. 
                          Survolez les zones pour voir plus de détails. Le pourcentage affiché représente le niveau de confiance de la détection.
                        </Typography>
                      </Box>
                    </>
                  ) : (
                    <Box
                      component="img"
                      src={analysis.image.startsWith('http') ? analysis.image : `http://127.0.0.1:8000${analysis.image}`}
                      alt="Image originale"
                      sx={{
                        width: '100%',
                        height: 400,
                        objectFit: 'contain',
                        borderRadius: 2,
                        mb: 2,
                        bgcolor: 'grey.50',
                      }}
                      onError={(e) => {
                        console.error('Erreur de chargement de l\'image:', e);
                        e.currentTarget.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDQwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI0MDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjRjVGNUY1Ii8+CjxwYXRoIGQ9Ik0xNzUgMTUwTDE5NSAxMzBMMjE1IDE1MEwyMzUgMTMwTDI1NSAxNTBWMjAwSDE3NVYxNTBaIiBmaWxsPSIjQ0NDQ0NDIi8+Cjx0ZXh0IHg9IjIwMCIgeT0iMjIwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOTk5IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiPkltYWdlIG5vbiBkaXNwb25pYmxlPC90ZXh0Pgo8L3N2Zz4=';
                      }}
                    />
                  )}
                </>
              ) : imageDeleted ? (
                <Box
                  sx={{
                    width: '100%',
                    height: 300,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    bgcolor: 'error.50',
                    borderRadius: 2,
                    mb: 2,
                    flexDirection: 'column',
                    gap: 2,
                    border: '2px dashed',
                    borderColor: 'error.main',
                  }}
                >
                  <DeleteIcon sx={{ fontSize: 48, color: 'error.main' }} />
                  <Typography variant="h6" color="error.main">
                    🗑️ Image supprimée
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    L'image a été supprimée par l'utilisateur
                  </Typography>
                  <Button
                    variant="outlined"
                    color="primary"
                    size="small"
                    onClick={handleRestoreImage}
                    sx={{ mt: 1 }}
                  >
                    Restaurer l'image
                  </Button>
                </Box>
              ) : (
                <Box
                  sx={{
                    width: '100%',
                    height: 300,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    bgcolor: 'grey.100',
                    borderRadius: 2,
                    mb: 2,
                    flexDirection: 'column',
                    gap: 2,
                  }}
                >
                  <Typography variant="h6" color="text.secondary">
                    📷 Aucune image disponible
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    L'image de l'analyse n'a pas pu être chargée
                  </Typography>
                </Box>
              )}
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Typography variant="body1">
                  <strong>Type de peau:</strong>
                </Typography>
                <Chip
                  label={getSkinTypeLabel(analysis.skin_type_prediction)}
                  color={getSkinTypeColor(analysis.skin_type_prediction) as any}
                />
                {analysis.skin_type_confidence && (
                  <Typography variant="body2" color="text.secondary">
                    ({(analysis.skin_type_confidence * 100).toFixed(1)}% de confiance)
                  </Typography>
                )}
              </Box>
              
              {/* Bouton pour afficher les images en grand format */}
              {analysis.image && !imageDeleted && (
                <Button
                  variant="outlined"
                  fullWidth
                  startIcon={<ZoomInIcon />}
                  onClick={() => setImageViewerOpen(true)}
                  sx={{ mt: 2 }}
                >
                  Voir les images en grand format
                </Button>
              )}
            </CardContent>
          </Card>
        </Box>

        {/* Détections */}
        <Box sx={{ flex: { xs: '1', md: '1' } }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🔍 Problèmes Détectés
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                {analysis.acne_detected && (
                  <Paper sx={{ p: 2, bgcolor: 'error.50' }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="body1">
                        <strong>Acné détectée</strong>
                      </Typography>
                      <Chip
                        label={analysis.acne_severity}
                        color={getSeverityColor(analysis.acne_severity) as any}
                        size="small"
                      />
                    </Box>
                    {analysis.acne_confidence && (
                      <Typography variant="body2" color="text.secondary">
                        Confiance: {(analysis.acne_confidence * 100).toFixed(1)}%
                      </Typography>
                    )}
                  </Paper>
                )}

                {analysis.wrinkles_detected && (
                  <Paper sx={{ p: 2, bgcolor: 'warning.50' }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="body1">
                        <strong>Rides détectées</strong>
                      </Typography>
                      <Chip
                        label={analysis.wrinkles_severity}
                        color={getSeverityColor(analysis.wrinkles_severity) as any}
                        size="small"
                      />
                    </Box>
                    {analysis.wrinkles_confidence && (
                      <Typography variant="body2" color="text.secondary">
                        Confiance: {(analysis.wrinkles_confidence * 100).toFixed(1)}%
                      </Typography>
                    )}
                  </Paper>
                )}

                {analysis.dark_spots_detected && (
                  <Paper sx={{ p: 2, bgcolor: 'info.50' }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="body1">
                        <strong>Taches sombres détectées</strong>
                      </Typography>
                      <Chip
                        label={analysis.dark_spots_severity}
                        color={getSeverityColor(analysis.dark_spots_severity) as any}
                        size="small"
                      />
                    </Box>
                    {analysis.dark_spots_confidence && (
                      <Typography variant="body2" color="text.secondary">
                        Confiance: {(analysis.dark_spots_confidence * 100).toFixed(1)}%
                      </Typography>
                    )}
                  </Paper>
                )}

                {analysis.redness_detected && (
                  <Paper sx={{ p: 2, bgcolor: 'error.50' }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="body1">
                        <strong>Rougeurs détectées</strong>
                      </Typography>
                      <Chip
                        label={analysis.redness_severity}
                        color={getSeverityColor(analysis.redness_severity) as any}
                        size="small"
                      />
                    </Box>
                    {analysis.redness_confidence && (
                      <Typography variant="body2" color="text.secondary">
                        Confiance: {(analysis.redness_confidence * 100).toFixed(1)}%
                      </Typography>
                    )}
                  </Paper>
                )}

                {!analysis.acne_detected && !analysis.wrinkles_detected && 
                 !analysis.dark_spots_detected && !analysis.redness_detected && (
                  <Paper sx={{ p: 2, bgcolor: 'success.50' }}>
                    <Typography variant="body1" color="success.main">
                      <strong>✅ Aucun problème majeur détecté</strong>
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Votre peau semble en bonne santé !
                    </Typography>
                  </Paper>
                )}
              </Box>
            </CardContent>
          </Card>
        </Box>

        {/* Actions */}
        <Box sx={{ flex: '1' }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🚀 Actions Recommandées
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Button
                  variant="contained"
                  startIcon={<AIIcon />}
                  onClick={() => navigate(`/simulation/${analysis.id}`)}
                >
                  Voir la simulation IA
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<ProductIcon />}
                  onClick={() => navigate(`/recommendations/${analysis.id}`)}
                >
                  Produits recommandés
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<TimelineIcon />}
                  onClick={() => navigate(`/transformation/${analysis.id}`)}
                >
                  Voir l'Évolution Après Traitement
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Box>
        </Box>
      </Container>

      {/* Dialog de confirmation de suppression */}
      <Dialog
        open={deleteDialogOpen}
        onClose={handleCancelDelete}
        aria-labelledby="delete-dialog-title"
        aria-describedby="delete-dialog-description"
      >
        <DialogTitle id="delete-dialog-title">
          🗑️ Supprimer l'image
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="delete-dialog-description">
            Êtes-vous sûr de vouloir supprimer cette image ? Cette action est irréversible.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCancelDelete} color="primary">
            Annuler
          </Button>
          <Button onClick={handleConfirmDelete} color="error" variant="contained">
            Oui, supprimer
          </Button>
        </DialogActions>
      </Dialog>

      {/* Modal pour afficher les images en grand format */}
      <Dialog
        open={imageViewerOpen}
        onClose={() => setImageViewerOpen(false)}
        maxWidth="lg"
        fullWidth
        PaperProps={{
          sx: {
            maxHeight: '90vh',
            height: '90vh',
          }
        }}
      >
        <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', pb: 1 }}>
          <Typography variant="h6">Images de l'analyse</Typography>
          <IconButton onClick={() => setImageViewerOpen(false)} size="small">
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent sx={{ p: 0, display: 'flex', flexDirection: 'column', height: '100%' }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs
              value={imageViewerTab}
              onChange={(e, newValue) => setImageViewerTab(newValue)}
              sx={{ px: 2 }}
            >
              {analysis.annotated_image && (
                <Tab label="Zones détectées" />
              )}
              <Tab label="Image originale" />
            </Tabs>
          </Box>
          <Box sx={{ flex: 1, overflow: 'auto', p: 2, display: 'flex', justifyContent: 'center', alignItems: 'center', bgcolor: 'grey.50' }}>
            {(() => {
              const hasAnnotated = analysis.annotated_image;
              // Si l'image annotée existe et qu'on est sur l'onglet 0, afficher l'image annotée
              // Sinon, afficher l'image originale
              const showAnnotated = hasAnnotated && imageViewerTab === 0;
              
              return showAnnotated ? (
                <Box
                  component="img"
                  src={analysis.annotated_image!.startsWith('http') ? analysis.annotated_image! : `http://127.0.0.1:8000${analysis.annotated_image}`}
                  alt="Image avec zones détectées"
                  sx={{
                    maxWidth: '100%',
                    maxHeight: 'calc(90vh - 120px)',
                    objectFit: 'contain',
                    borderRadius: 2,
                    boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                  }}
                  onError={(e) => {
                    console.error('Erreur de chargement de l\'image annotée:', e);
                  }}
                />
              ) : (
                <Box
                  component="img"
                  src={analysis.image.startsWith('http') ? analysis.image : `http://127.0.0.1:8000${analysis.image}`}
                  alt="Image originale"
                  sx={{
                    maxWidth: '100%',
                    maxHeight: 'calc(90vh - 120px)',
                    objectFit: 'contain',
                    borderRadius: 2,
                    boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                  }}
                  onError={(e) => {
                    console.error('Erreur de chargement de l\'image:', e);
                  }}
                />
              );
            })()}
          </Box>
        </DialogContent>
        <DialogActions sx={{ px: 2, py: 1 }}>
          <Button onClick={() => setImageViewerOpen(false)} variant="contained">
            Fermer
          </Button>
        </DialogActions>
      </Dialog>

      {/* Composants med/ - Sections détaillées */}
      {diagnosisData && !loadingDiagnosis && (
        <>
          {/* 💧 Infos rapides */}
          <Box sx={{ mt: 4 }}>
            <QuickInfo data={diagnosisData.quickInfo} />
          </Box>

          {/* 🩺 Diagnostic dermatologique */}
          <Box sx={{ mt: 2 }}>
            <DiagnosticSection data={diagnosisData.diagnostic} />
          </Box>

          {/* 💡 Conseils pratiques */}
          <Box sx={{ mt: 2 }}>
            <AdviceSection conseils={diagnosisData.conseils_pratiques} />
          </Box>
        </>
      )}

      {/* Message de chargement pour les composants med/ */}
      {loadingDiagnosis && (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4, mt: 4 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
            <LinearProgress sx={{ width: '100%', maxWidth: 400 }} />
            <Typography variant="body2" color="text.secondary">
              Chargement des recommandations détaillées...
            </Typography>
          </Box>
        </Box>
      )}

      {/* Rapport d'Analyse */}
      {analysis && <AnalysisReport analysis={analysis} />}

      {/* Évolution des problèmes cutanés */}
      <Box sx={{ width: '100%', mt: 2, height: 240, background: 'linear-gradient(135deg,#e2f7fa 70%,#fafafa 100%)', borderRadius: 2, boxShadow: '0 0 12px #b0e0e630', position:'relative', py:2, px:2 }}>
        <Typography fontWeight="bold" color="primary.dark" sx={{pb:0.5}}>Évolution des problèmes cutanés</Typography>
        {skinHistoryData.length > 0 ? (
          <ResponsiveContainer width="100%" height={180}>
            <LineChart data={skinHistoryData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }} 
                tickFormatter={(value) => {
                  const date = new Date(value);
                  return date.toLocaleDateString('fr-FR', { month: 'short', day: 'numeric' });
                }}
              />
              <YAxis allowDecimals={false} domain={[0, 3]}/>
              <ChartTooltip 
                labelFormatter={(value) => {
                  const date = new Date(value);
                  return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
                }}
              />
              <Line type="monotone" dataKey="acne" stroke="#d32f2f" name="Acné" strokeWidth={2} dot={{ r: 4 }} />
              <Line type="monotone" dataKey="rides" stroke="#FFB300" name="Rides" strokeWidth={2} dot={{ r: 4 }} />
              <Line type="monotone" dataKey="taches" stroke="#9C27B0" name="Taches" strokeWidth={2} dot={{ r: 4 }} />
              <Line type="monotone" dataKey="rougeurs" stroke="#F44336" name="Rougeurs" strokeWidth={2} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: 180 }}>
            <Typography variant="body2" color="text.secondary">
              Aucune donnée historique disponible. Effectuez plusieurs analyses pour voir l'évolution.
            </Typography>
          </Box>
        )}
        <Tooltip title="Partager">
          <IconButton sx={{ position: 'absolute', right: 4, top:10 }} onClick={()=>setShareDialogOpen(true)}><ShareIcon/></IconButton>
        </Tooltip>
      </Box>

      {/* Assistant Chat pour les résultats */}
      {analysis && <ResultsChatAI analysis={analysis} />}
      <Dialog open={shareDialogOpen} onClose={()=>setShareDialogOpen(false)}>
        <DialogTitle>Partager votre analyse</DialogTitle>
        <DialogContent>
          <Typography>Copiez le lien ou partagez sur vos réseaux sociaux ! (Fonctionnalité à intégrer)</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={()=>setShareDialogOpen(false)}>Fermer</Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

  export default ResultsPage;




