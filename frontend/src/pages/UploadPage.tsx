import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, Box, Button, Snackbar, Alert } from '@mui/material';
import UploadForm from '../components/UploadForm';
import AvatarCircleAI from '../components/AvatarCircleAI';
import ChatAI from '../components/ChatAI';
import { SkinAnalysis } from '../types';
import { apiService } from '../services/api';

const UploadPage: React.FC = () => {
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState<SkinAnalysis | null>(null);
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

  const handleAIConversation = () => {
    setIsAITalking(true);
    setAvatarStatus('ai-thinking');
    
    const aiMessage = '🔬 Je suis là pour vous aider avec votre analyse de peau ! Prenez une photo claire de votre visage, de préférence avec un bon éclairage naturel, pour obtenir les meilleurs résultats d\'analyse.';
    
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

  const handleAnalysisComplete = (completedAnalysis: SkinAnalysis) => {
    setAnalysis(completedAnalysis);
    // Rediriger vers la page de résultats après un délai
    setTimeout(() => {
      navigate(`/results/${completedAnalysis.id}`);
    }, 2000);
  };

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
            📸 Analyse de Votre Peau
          </Typography>
        </Box>
      </Box>

      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h6" color="text.secondary" paragraph>
          Uploadez une photo de votre visage pour une analyse complète avec l'IA
        </Typography>
      </Box>

      <UploadForm onAnalysisComplete={handleAnalysisComplete} />

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

export default UploadPage;




