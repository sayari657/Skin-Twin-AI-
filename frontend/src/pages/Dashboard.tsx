import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Avatar,
  LinearProgress,
  Alert,
  TextField,
  Rating,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Snackbar,
  IconButton,
  Divider,
} from '@mui/material';
import {
  CameraAlt as CameraIcon,
  History as HistoryIcon,
  Psychology as AIIcon,
  ShoppingCart as ProductIcon,
  TrendingUp as TrendingIcon,
  CheckCircle as CheckIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Star as StarIcon,
  ThumbUp as ThumbUpIcon,
  Comment as CommentIcon,
  Send as SendIcon,
} from '@mui/icons-material';
import { apiService } from '../services/api';
import { SkinAnalysis, User } from '../types';
import AvatarCircleAI from '../components/AvatarCircleAI';
import ChatAI from '../components/ChatAI';




const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);
  const [recentAnalyses, setRecentAnalyses] = useState<SkinAnalysis[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // États pour la section avis
  const [feedbackDialogOpen, setFeedbackDialogOpen] = useState(false);
  const [feedbackRating, setFeedbackRating] = useState<number>(0);
  const [feedbackComment, setFeedbackComment] = useState('');
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [avatarStatus, setAvatarStatus] = useState<'online' | 'offline' | 'active' | 'story' | 'ai-thinking'>('online');
  const [isAITalking, setIsAITalking] = useState(false);
  const [chatPosition, setChatPosition] = useState({ x: window.innerWidth - 100, y: window.innerHeight - 100 });
  const [chatOpen, setChatOpen] = useState(false);
  const [chatInitialMessage, setChatInitialMessage] = useState<string | undefined>(undefined);
  const [chatFillInput, setChatFillInput] = useState<string | undefined>(undefined);
  const [isVoiceMode, setIsVoiceMode] = useState(false);
  


  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [profileResponse, analysesResponse] = await Promise.all([
        apiService.getProfile(),
        apiService.getUserAnalyses(),
      ]);

      setUser(profileResponse.data);
      setRecentAnalyses(analysesResponse.data.slice(0, 3)); // Dernières 3 analyses
    } catch (err: any) {
      setError('Erreur lors du chargement des données');
    } finally {
      setLoading(false);
    }
  };

  // Fonctions pour la gestion des avis
  const handleOpenFeedbackDialog = () => {
    setFeedbackDialogOpen(true);
  };

  const handleCloseFeedbackDialog = () => {
    setFeedbackDialogOpen(false);
    setFeedbackRating(0);
    setFeedbackComment('');
  };

  const handleSubmitFeedback = async () => {
    if (feedbackRating === 0) {
      setSnackbarMessage('Veuillez donner une note avant de soumettre votre avis');
      setSnackbarOpen(true);
      return;
    }

    try {
      // Appel API pour sauvegarder le témoignage
      await apiService.post('/users/testimonials/', {
        rating: feedbackRating,
        comment: feedbackComment,
        is_public: true
      });

      setFeedbackSubmitted(true);
      setSnackbarMessage('Merci pour votre avis ! Votre témoignage a été sauvegardé et sera visible sur la page d\'accueil.');
      setSnackbarOpen(true);
      handleCloseFeedbackDialog();
      
      // Réinitialiser après 3 secondes
      setTimeout(() => {
        setFeedbackSubmitted(false);
      }, 3000);
    } catch (error: any) {
      console.error('Erreur lors de l\'envoi du témoignage:', error);
      setSnackbarMessage('Erreur lors de l\'envoi de votre avis. Veuillez réessayer.');
      setSnackbarOpen(true);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  // Fonction pour simuler l'IA qui parle
  const handleAIConversation = () => {
    setIsAITalking(true);
    setAvatarStatus('ai-thinking');
    
    // Message de l'IA
    const aiMessage = '🤖 Bonjour ! Je suis votre assistant Skin Twin AI. Je peux vous aider avec l\'analyse de votre peau, vous recommander des produits, ou répondre à vos questions sur les soins. Que souhaitez-vous savoir ?';
    
    // Simuler une conversation IA
    setTimeout(() => {
      setAvatarStatus('active');
      
      // Ouvrir le chat et remplir le champ de saisie
      setChatFillInput(aiMessage);
      setChatOpen(true);
      
      // Activer le mode vocal
      setIsVoiceMode(true);
      
      // Afficher aussi la notification
      setSnackbarMessage('🎤 Mode vocal activé ! Parlez maintenant, votre message sera automatiquement rempli dans le chat.');
      setSnackbarOpen(true);
    }, 2000);

    // Arrêter la conversation après 5 secondes
    setTimeout(() => {
      setIsAITalking(false);
      setAvatarStatus('online');
    }, 5000);
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

  const getIssueSeverity = (detected: boolean, severity?: string) => {
    if (!detected) return null;
    const severityColors: { [key: string]: string } = {
      'LOW': 'success',
      'MODERATE': 'warning',
      'HIGH': 'error',
    };
    return severityColors[severity || ''] || 'default';
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Chargement de votre tableau de bord...
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* En-tête avec Avatar Circle AI */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 3, mb: 4 }}>
        <AvatarCircleAI
          src={user?.profile_picture}
          name={user?.first_name || user?.username || 'Utilisateur'}
          status={avatarStatus}
          size={100}
          showStatus={true}
          showName={true}
          aiEnabled={true}
          isThinking={isAITalking}
          onStatusChange={setAvatarStatus}
        />
        <Box sx={{ flex: 1 }}>
          <Typography variant="h4" gutterBottom>
            👋 Bonjour {user?.first_name || user?.username} !
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
            Votre assistant IA Skin Twin est prêt à vous aider
          </Typography>
          <Button
            variant="contained"
            startIcon={<AIIcon />}
            onClick={handleAIConversation}
            disabled={isAITalking}
            size="medium"
            sx={{
              background: 'linear-gradient(45deg, #2196F3, #21CBF3)',
              '&:hover': {
                background: 'linear-gradient(45deg, #1976D2, #1CB5E0)',
                transform: 'scale(1.05)',
              },
              transition: 'all 0.3s ease',
              boxShadow: '0 4px 15px rgba(33, 150, 243, 0.3)',
            }}
          >
            {isAITalking ? '🤖 IA en réflexion...' : '🎤 Parler à l\'IA (Mode vocal)'}
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
        {/* Actions rapides */}
        <Box sx={{ flex: { xs: '1', md: '2' } }}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🚀 Actions Rapides
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<CameraIcon />}
                  onClick={() => navigate('/upload')}
                  sx={{ py: 2 }}
                >
                  Analyser ma peau
                </Button>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<HistoryIcon />}
                  onClick={() => navigate('/history')}
                  sx={{ py: 2 }}
                >
                  Voir l'historique
                </Button>
              </Box>
            </CardContent>
          </Card>

          {/* Profil utilisateur */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                👤 Votre Profil
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="body2" color="text.secondary">
                      Type de peau
                    </Typography>
                    <Chip
                      label={getSkinTypeLabel(user?.skin_type)}
                      color={getSkinTypeColor(user?.skin_type) as any}
                      size="small"
                    />
                  </Box>
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="body2" color="text.secondary">
                      Âge
                    </Typography>
                    <Typography variant="body1">
                      {user?.age ? `${user.age} ans` : 'Non renseigné'}
                    </Typography>
                  </Box>
                </Box>
                {user?.current_skin_problems && user.current_skin_problems.length > 0 && (
                  <Box>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Problèmes cutanés
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {user.current_skin_problems.map((problem, index) => (
                        <Chip
                          key={index}
                          label={problem.replace('_', ' ')}
                          size="small"
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  </Box>
                )}
              </Box>
            </CardContent>
            <CardActions>
              <Button size="small" onClick={() => navigate('/profile')}>
                Modifier le profil
              </Button>
            </CardActions>
          </Card>
        </Box>

        {/* Statistiques */}
        <Box sx={{ flex: { xs: '1', md: '1' } }}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📊 Statistiques
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <CameraIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Analyses effectuées"
                    secondary={recentAnalyses.length}
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <TrendingIcon color="success" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Progression"
                    secondary="En cours..."
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <ProductIcon color="info" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Produits recommandés"
                    secondary="0"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>

          {/* Objectifs */}
          {user?.skin_goals && user.skin_goals.length > 0 && (
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  🎯 Vos Objectifs
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {user.skin_goals.map((goal, index) => (
                    <Chip
                      key={index}
                      label={goal.replace('_', ' ')}
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}
        </Box>

        {/* Analyses récentes */}
        <Box sx={{ width: '100%' }}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📸 Analyses Récentes
              </Typography>
              {recentAnalyses.length === 0 ? (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <CameraIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h6" color="text.secondary" gutterBottom>
                    Aucune analyse pour le moment
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Commencez par analyser votre peau pour voir vos résultats ici.
                  </Typography>
                  <Button
                    variant="contained"
                    startIcon={<CameraIcon />}
                    onClick={() => navigate('/upload')}
                  >
                    Première analyse
                  </Button>
                </Box>
              ) : (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                  {recentAnalyses.map((analysis) => (
                    <Box sx={{ flex: { xs: '1 1 100%', sm: '1 1 calc(50% - 8px)', md: '1 1 calc(33.333% - 12px)' }, minWidth: 0 }} key={analysis.id}>
                      <Paper sx={{ p: 2, height: '100%' }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <Avatar
                            src={analysis.image}
                            variant="rounded"
                            sx={{ width: 60, height: 60, mr: 2 }}
                          />
                          <Box>
                            <Typography variant="subtitle2">
                              {new Date(analysis.analysis_date).toLocaleDateString('fr-FR')}
                            </Typography>
                            <Chip
                              label={getSkinTypeLabel(analysis.skin_type_prediction)}
                              color={getSkinTypeColor(analysis.skin_type_prediction) as any}
                              size="small"
                            />
                          </Box>
                        </Box>
                        
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2" color="text.secondary" gutterBottom>
                            Problèmes détectés:
                          </Typography>
                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                            {analysis.acne_detected && (
                              <Chip
                                label="Acné"
                                color={getIssueSeverity(analysis.acne_detected, analysis.acne_severity) as any}
                                size="small"
                              />
                            )}
                            {analysis.wrinkles_detected && (
                              <Chip
                                label="Rides"
                                color={getIssueSeverity(analysis.wrinkles_detected, analysis.wrinkles_severity) as any}
                                size="small"
                              />
                            )}
                            {analysis.dark_spots_detected && (
                              <Chip
                                label="Taches"
                                color={getIssueSeverity(analysis.dark_spots_detected, analysis.dark_spots_severity) as any}
                                size="small"
                              />
                            )}
                            {analysis.redness_detected && (
                              <Chip
                                label="Rougeurs"
                                color={getIssueSeverity(analysis.redness_detected, analysis.redness_severity) as any}
                                size="small"
                              />
                            )}
                            {!analysis.acne_detected && !analysis.wrinkles_detected && 
                             !analysis.dark_spots_detected && !analysis.redness_detected && (
                              <Chip
                                label="Aucun problème"
                                color="success"
                                size="small"
                              />
                            )}
                          </Box>
                        </Box>
                        
                        <Button
                          size="small"
                          onClick={() => navigate(`/results/${analysis.id}`)}
                        >
                          Voir les détails
                        </Button>
                      </Paper>
                    </Box>
                  ))}
                </Box>
              )}
            </CardContent>
          </Card>


          {/* Section Avis et Feedback */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6">
                  💬 Votre Avis
                </Typography>
                <IconButton 
                  color="primary" 
                  onClick={handleOpenFeedbackDialog}
                  disabled={feedbackSubmitted}
                >
                  <CommentIcon />
                </IconButton>
              </Box>
              
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Partagez votre expérience avec Skin Twin AI et aidez-nous à améliorer notre service
              </Typography>

              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Button
                  variant="outlined"
                  startIcon={<StarIcon />}
                  onClick={handleOpenFeedbackDialog}
                  disabled={feedbackSubmitted}
                  sx={{ flex: 1, minWidth: 200 }}
                >
                  {feedbackSubmitted ? 'Avis envoyé ✓' : 'Donner mon avis'}
                </Button>
                
                <Button
                  variant="text"
                  startIcon={<ThumbUpIcon />}
                  onClick={() => {
                    setSnackbarMessage('Merci pour votre soutien ! 👍');
                    setSnackbarOpen(true);
                  }}
                  sx={{ flex: 1, minWidth: 150 }}
                >
                  Recommander
                </Button>
              </Box>

              {feedbackSubmitted && (
                <Alert severity="success" sx={{ mt: 2 }}>
                  Merci pour votre avis ! Votre feedback nous aide à améliorer Skin Twin AI.
                </Alert>
              )}
            </CardContent>
          </Card>
        </Box>
      </Box>

      {/* Dialog pour donner son avis */}
      <Dialog 
        open={feedbackDialogOpen} 
        onClose={handleCloseFeedbackDialog}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <StarIcon color="primary" />
            Donner votre avis sur Skin Twin AI
          </Box>
        </DialogTitle>
        
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Notez votre expérience (1 = Très décevant, 5 = Excellent)
            </Typography>
            <Rating
              value={feedbackRating}
              onChange={(event, newValue) => {
                setFeedbackRating(newValue || 0);
              }}
              size="large"
              sx={{ mb: 3 }}
            />
          </Box>

          <TextField
            fullWidth
            multiline
            rows={4}
            label="Votre commentaire (optionnel)"
            placeholder="Dites-nous ce que vous pensez de Skin Twin AI, ce qui vous plaît, ce qui pourrait être amélioré..."
            value={feedbackComment}
            onChange={(e) => setFeedbackComment(e.target.value)}
            variant="outlined"
          />
        </DialogContent>
        
        <DialogActions>
          <Button onClick={handleCloseFeedbackDialog}>
            Annuler
          </Button>
          <Button 
            onClick={handleSubmitFeedback}
            variant="contained"
            startIcon={<SendIcon />}
            disabled={feedbackRating === 0}
          >
            Envoyer l'avis
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar pour les notifications */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={4000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert 
          onClose={handleCloseSnackbar} 
          severity="success" 
          sx={{ width: '100%' }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>

      {/* Chat IA Intelligent */}
      <ChatAI
        position={chatPosition}
        onPositionChange={setChatPosition}
        isOpen={chatOpen}
        onOpenChange={setChatOpen}
        initialMessage={chatInitialMessage}
        fillInputWithMessage={chatFillInput}
        isVoiceMode={isVoiceMode}
        onVoiceModeChange={setIsVoiceMode}
      />
    </Container>
      );
    };

    export default Dashboard;




