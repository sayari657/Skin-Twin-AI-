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
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  Psychology as AIIcon,
  ShoppingCart as ProductIcon,
  History as HistoryIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { apiService } from '../services/api';
import { SkinAnalysis } from '../types';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as ChartTooltip, ResponsiveContainer } from 'recharts';
import { IconButton, Tooltip } from '@mui/material';
import ShareIcon from '@mui/icons-material/Share';

const ResultsPage: React.FC = () => {
  const { analysisId } = useParams<{ analysisId: string }>();
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState<SkinAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [imageDeleted, setImageDeleted] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [shareDialogOpen, setShareDialogOpen] = useState(false);
  const skinHistoryData = [ // Dummy data, replace with your fetched history
    { date: '2024-06-01', acne: 1, rides: 0 },
    { date: '2024-07-01', acne: 2, rides: 1 },
    { date: '2024-08-01', acne: 1, rides: 1 },
    { date: '2024-09-01', acne: 0, rides: 2 },
  ];

  useEffect(() => {
    if (analysisId) {
      loadAnalysis();
    }
  }, [analysisId]);

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
                {analysis.image && !imageDeleted && (
                  <Button
                    variant="outlined"
                    color="error"
                    size="small"
                    startIcon={<DeleteIcon />}
                    onClick={handleDeleteImage}
                    sx={{ ml: 2 }}
                  >
                    Supprimer
                  </Button>
                )}
              </Box>
              {analysis.image && !imageDeleted ? (
                <Box
                  component="img"
                  src={analysis.image.startsWith('http') ? analysis.image : `http://127.0.0.1:8000${analysis.image}`}
                  alt="Image analysée"
                  sx={{
                    width: '100%',
                    height: 300,
                    objectFit: 'cover',
                    borderRadius: 2,
                    mb: 2,
                  }}
                  onError={(e) => {
                    console.error('Erreur de chargement de l\'image:', e);
                    e.currentTarget.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDQwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI0MDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjRjVGNUY1Ii8+CjxwYXRoIGQ9Ik0xNzUgMTUwTDE5NSAxMzBMMjE1IDE1MEwyMzUgMTMwTDI1NSAxNTBWMjAwSDE3NVYxNTBaIiBmaWxsPSIjQ0NDQ0NDIi8+Cjx0ZXh0IHg9IjIwMCIgeT0iMjIwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOTk5IiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiPkltYWdlIG5vbiBkaXNwb25pYmxlPC90ZXh0Pgo8L3N2Zz4=';
                  }}
                />
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
                  startIcon={<HistoryIcon />}
                  onClick={() => navigate('/history')}
                >
                  Sauvegarder dans l'historique
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
      <Box sx={{ width: '100%', mt: 2, height: 240, background: 'linear-gradient(135deg,#e2f7fa 70%,#fafafa 100%)', borderRadius: 2, boxShadow: '0 0 12px #b0e0e630', position:'relative', py:2, px:2 }}>
        <Typography fontWeight="bold" color="primary.dark" sx={{pb:0.5}}>Évolution des problèmes cutanés</Typography>
        <ResponsiveContainer width="100%" height={180}>
          <LineChart data={skinHistoryData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" tick={{ fontSize: 12 }} />
            <YAxis allowDecimals={false}/>
            <ChartTooltip />
            <Line type="monotone" dataKey="acne" stroke="#d32f2f" name="Acné" strokeWidth={2}/>
            <Line type="monotone" dataKey="rides" stroke="#FFB300" name="Rides" strokeWidth={2}/>
          </LineChart>
        </ResponsiveContainer>
        <Tooltip title="Partager">
          <IconButton sx={{ position: 'absolute', right: 4, top:10 }} onClick={()=>setShareDialogOpen(true)}><ShareIcon/></IconButton>
        </Tooltip>
      </Box>
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




