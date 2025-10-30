import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
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
  Avatar,
  IconButton,
  Snackbar,
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  Visibility as ViewIcon,
  Delete as DeleteIcon,
  CameraAlt as CameraIcon,
  Psychology as AIIcon,
} from '@mui/icons-material';
import { apiService } from '../services/api';
import { SkinAnalysis } from '../types';
import AvatarCircleAI from '../components/AvatarCircleAI';
import ChatAI from '../components/ChatAI';

const HistoryPage: React.FC = () => {
  const navigate = useNavigate();
  const [analyses, setAnalyses] = useState<SkinAnalysis[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [user, setUser] = useState<any>(null);
  const [avatarStatus, setAvatarStatus] = useState<'online' | 'offline' | 'active' | 'story' | 'ai-thinking'>('online');
  const [isAITalking, setIsAITalking] = useState(false);
  const [chatPosition, setChatPosition] = useState({ x: window.innerWidth - 100, y: window.innerHeight - 100 });
  const [chatOpen, setChatOpen] = useState(false);
  const [chatInitialMessage, setChatInitialMessage] = useState<string | undefined>(undefined);
  const [chatFillInput, setChatFillInput] = useState<string | undefined>(undefined);
  const [isVoiceMode, setIsVoiceMode] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');

  useEffect(() => {
    loadAnalyses();
    loadUserProfile();
  }, []);

  const loadUserProfile = async () => {
    try {
      const response = await apiService.getProfile();
      setUser(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement du profil:', error);
    }
  };

  const loadAnalyses = async () => {
    try {
      setLoading(true);
      const response = await apiService.getUserAnalyses();
      setAnalyses(response.data);
    } catch (err: any) {
      setError('Erreur lors du chargement de l\'historique');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAnalysis = async (analysisId: number) => {
    try {
      await apiService.deleteSkinAnalysis(analysisId);
      setAnalyses(analyses.filter(a => a.id !== analysisId));
    } catch (err: any) {
      console.error('Erreur lors de la suppression:', err);
    }
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

  const handleAIConversation = () => {
    setIsAITalking(true);
    setAvatarStatus('ai-thinking');
    
    const aiMessage = '📚 Je peux vous aider à analyser votre historique de peau ! Je peux vous expliquer l\'évolution de vos analyses dans le temps, identifier les tendances, et vous donner des conseils personnalisés basés sur vos résultats précédents.';
    
    setTimeout(() => {
      setAvatarStatus('active');
      setChatFillInput(aiMessage);
      setChatOpen(true);
      setIsVoiceMode(true);
      setSnackbarMessage('🎤 Mode vocal activé ! Parlez maintenant, votre message sera automatiquement rempli dans le chat.');
      setSnackbarOpen(true);
    }, 2000);

    setTimeout(() => {
      setIsAITalking(false);
      setAvatarStatus('online');
    }, 5000);
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Chargement de l'historique...
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
          <Button
            startIcon={<BackIcon />}
            onClick={() => navigate('/dashboard')}
            sx={{ mb: 2 }}
          >
            Retour
          </Button>
          <Typography variant="h4" gutterBottom>
            📚 Historique des Analyses
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
            Votre assistant IA Skin Twin peut analyser l'évolution de votre peau
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

      {analyses.length === 0 ? (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <CameraIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            Aucune analyse dans l'historique
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
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
          {analyses.map((analysis) => (
            <Box sx={{ flex: { xs: '1 1 100%', sm: '1 1 calc(50% - 12px)', md: '1 1 calc(33.333% - 16px)' }, minWidth: 0 }} key={analysis.id}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Avatar
                      src={analysis.image}
                      variant="rounded"
                      sx={{ width: 60, height: 60, mr: 2 }}
                    />
                    <Box sx={{ flexGrow: 1 }}>
                      <Typography variant="subtitle1" gutterBottom>
                        {new Date(analysis.analysis_date).toLocaleDateString('fr-FR')}
                      </Typography>
                      <Chip
                        label={getSkinTypeLabel(analysis.skin_type_prediction)}
                        color={getSkinTypeColor(analysis.skin_type_prediction) as any}
                        size="small"
                      />
                    </Box>
                    <IconButton
                      size="small"
                      onClick={() => handleDeleteAnalysis(analysis.id)}
                      color="error"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Box>

                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Problèmes détectés:
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {analysis.acne_detected && (
                        <Chip label="Acné" color="error" size="small" />
                      )}
                      {analysis.wrinkles_detected && (
                        <Chip label="Rides" color="warning" size="small" />
                      )}
                      {analysis.dark_spots_detected && (
                        <Chip label="Taches" color="info" size="small" />
                      )}
                      {analysis.redness_detected && (
                        <Chip label="Rougeurs" color="error" size="small" />
                      )}
                      {!analysis.acne_detected && !analysis.wrinkles_detected && 
                       !analysis.dark_spots_detected && !analysis.redness_detected && (
                        <Chip label="Aucun problème" color="success" size="small" />
                      )}
                    </Box>
                  </Box>

                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Button
                      size="small"
                      variant="contained"
                      startIcon={<ViewIcon />}
                      onClick={() => navigate(`/results/${analysis.id}`)}
                      sx={{ flexGrow: 1 }}
                    >
                      Voir
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Box>
          ))}
        </Box>
      )}

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

export default HistoryPage;




