import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Paper,
  TextField,
  IconButton,
  Typography,
  Avatar,
  Chip,
  CircularProgress,
  Tooltip,
  Divider,
  Slide,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton as ListIconButton,
} from '@mui/material';
import {
  Send as SendIcon,
  Close as CloseIcon,
  DragIndicator as DragIcon,
  Psychology as AIIcon,
  Person as PersonIcon,
  Mic as MicIcon,
  MicOff as MicOffIcon,
  History as HistoryIcon,
  Add as AddIcon,
  Delete as DeleteIcon,
  Lightbulb as LightbulbIcon,
  Remove as MinimizeIcon,
} from '@mui/icons-material';
// import Draggable from 'react-draggable'; // Temporairement désactivé
import { chatService, ChatMessage, ChatSession } from '../services/chatService';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm'; // For GitHub markdown (tables, lists)

interface ChatAIProps {
  position?: { x: number; y: number };
  onPositionChange?: (position: { x: number; y: number }) => void;
  className?: string;
  isOpen?: boolean;
  onOpenChange?: (isOpen: boolean) => void;
  initialMessage?: string;
  fillInputWithMessage?: string;
  isVoiceMode?: boolean;
  onVoiceModeChange?: (isVoiceMode: boolean) => void;
}

const ChatAI: React.FC<ChatAIProps> = ({
  position = { x: window.innerWidth - 100, y: window.innerHeight - 100 },
  onPositionChange,
  className = '',
  isOpen: externalIsOpen,
  onOpenChange,
  initialMessage,
  fillInputWithMessage,
  isVoiceMode = false,
  onVoiceModeChange,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState<any>(null);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null);
  const [showSessions, setShowSessions] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  
  const chatRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const currentIsOpen = externalIsOpen !== undefined ? externalIsOpen : isOpen;

  // Auto-scroll vers le bas quand de nouveaux messages arrivent
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialiser la reconnaissance vocale
  useEffect(() => {
    let SpeechRecognition: any = null;
    
    // Vérifier la disponibilité de l'API de reconnaissance vocale
    if (typeof window !== 'undefined') {
      SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
    }
    
    if (!SpeechRecognition) {
      console.warn('Reconnaissance vocale non supportée par ce navigateur');
      return;
    }

    const recognitionInstance = new SpeechRecognition();
    recognitionInstance.continuous = true;
    recognitionInstance.interimResults = true;
    recognitionInstance.lang = 'fr-FR';
    recognitionInstance.maxAlternatives = 1;

    recognitionInstance.onstart = () => {
      console.log('Reconnaissance vocale démarrée');
      setIsListening(true);
    };

    recognitionInstance.onresult = (event: any) => {
      let finalTranscript = '';
      let interimTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript + ' ';
        } else {
          interimTranscript += transcript;
        }
      }

      if (finalTranscript) {
        // Nettoyer le texte final et l'ajouter
        const cleanedText = finalTranscript.trim();
        setInputText(prev => {
          // Enlever le texte temporaire (interim) et ajouter le texte final
          const withoutInterim = prev.replace(interimTranscript, '');
          return withoutInterim + cleanedText;
        });
      } else if (interimTranscript) {
        // Mettre à jour le texte temporaire
        setInputText(prev => {
          // Enlever l'ancien texte temporaire s'il existe
          const withoutOldInterim = prev.replace(/\[.*?\]/g, '');
          return withoutOldInterim + interimTranscript;
        });
      }
    };

    recognitionInstance.onerror = (event: any) => {
      console.log('Erreur reconnaissance vocale:', event.error);
      
      // Ignorer les erreurs normales
      if (event.error === 'no-speech') {
        // Pas de problème, l'utilisateur n'a simplement pas parlé
        return;
      }
      
      // Erreurs critiques qui nécessitent un arrêt
      if (event.error === 'not-allowed') {
        console.error('Microphone non autorisé. Veuillez autoriser l\'accès au microphone.');
        setIsListening(false);
        if (onVoiceModeChange) {
          onVoiceModeChange(false);
        }
        return;
      }
      
      if (event.error === 'aborted') {
        // Reconnaissance arrêtée manuellement
        setIsListening(false);
        return;
      }
      
      // Pour les autres erreurs, essayer de redémarrer
      if (isVoiceMode && event.error !== 'network') {
        console.log('Tentative de redémarrage de la reconnaissance vocale...');
        setTimeout(() => {
          if (isVoiceMode && recognitionInstance) {
            try {
              recognitionInstance.start();
            } catch (e) {
              console.error('Impossible de redémarrer la reconnaissance:', e);
            }
          }
        }, 1000);
      }
    };

    recognitionInstance.onend = () => {
      console.log('Reconnaissance vocale arrêtée');
      setIsListening(false);
      
      // Redémarrer automatiquement si le mode vocal est toujours activé
      if (isVoiceMode) {
        setTimeout(() => {
          if (isVoiceMode && recognitionInstance) {
            try {
              recognitionInstance.start();
            } catch (e) {
              console.error('Impossible de redémarrer la reconnaissance:', e);
            }
          }
        }, 100);
      }
    };

    setRecognition(recognitionInstance);
    
    // Nettoyer lors du démontage
    return () => {
      if (recognitionInstance) {
        try {
          recognitionInstance.stop();
        } catch (e) {
          // Ignorer les erreurs de nettoyage
        }
      }
    };
  }, []);

  // Gérer le mode vocal
  useEffect(() => {
    if (!recognition) return;
    
    if (isVoiceMode) {
      if (!isListening) {
        try {
          recognition.start();
          console.log('Mode vocal activé - Démarrage de la reconnaissance');
        } catch (error: any) {
          console.error('Erreur lors du démarrage de la reconnaissance:', error);
          // Si déjà démarré, ignorer l'erreur
          if (error.message && !error.message.includes('already started')) {
            setIsListening(false);
            if (onVoiceModeChange) {
              onVoiceModeChange(false);
            }
          }
        }
      }
    } else {
      if (isListening) {
        try {
          recognition.stop();
          console.log('Mode vocal désactivé - Arrêt de la reconnaissance');
        } catch (error) {
          console.error('Erreur lors de l\'arrêt de la reconnaissance:', error);
        }
      }
    }
  }, [isVoiceMode, recognition, isListening, onVoiceModeChange]);

  // Remplir le champ de saisie avec un message
  useEffect(() => {
    if (fillInputWithMessage) {
      setInputText(fillInputWithMessage);
      if (!currentIsOpen) {
        handleOpenChange(true);
      }
      setTimeout(() => {
        const inputElement = document.querySelector('input[placeholder*="Parlez"]') as HTMLInputElement;
        if (inputElement) {
          inputElement.focus();
          inputElement.style.borderColor = '#2196F3';
          inputElement.style.boxShadow = '0 0 10px rgba(33, 150, 243, 0.3)';
          setTimeout(() => {
            inputElement.style.borderColor = '';
            inputElement.style.boxShadow = '';
          }, 2000);
        }
      }, 500);
    }
  }, [fillInputWithMessage, currentIsOpen]);

  // Charger les sessions au montage
  useEffect(() => {
    if (currentIsOpen) {
      loadSessions();
      loadSuggestions();
    }
  }, [currentIsOpen]);

  const handleOpenChange = (open: boolean) => {
    if (onOpenChange) {
      onOpenChange(open);
    } else {
      setIsOpen(open);
    }
  };

  const loadSessions = async () => {
    try {
      const sessionsData = await chatService.getChatSessions();
      setSessions(sessionsData);
    } catch (error) {
      console.error('Erreur lors du chargement des sessions:', error);
    }
  };

  const loadSuggestions = async () => {
    try {
      const suggestionsData = await chatService.getAISuggestions();
      setSuggestions(suggestionsData);
    } catch (error) {
      console.error('Erreur lors du chargement des suggestions:', error);
    }
  };

  const createNewSession = async () => {
    try {
      const newSession = await chatService.createNewSession();
      setCurrentSession(newSession);
      setMessages([]);
      setShowSessions(false);
    } catch (error) {
      console.error('Erreur lors de la création de la session:', error);
    }
  };

  const loadSession = async (sessionId: string) => {
    try {
      const session = await chatService.getChatSession(sessionId);
      setCurrentSession(session);
      setMessages(session.messages);
      setShowSessions(false);
    } catch (error) {
      console.error('Erreur lors du chargement de la session:', error);
    }
  };

  const deleteSession = async (sessionId: string) => {
    try {
      await chatService.deleteChatSession(sessionId);
      await loadSessions();
      if (currentSession?.session_id === sessionId) {
        setCurrentSession(null);
        setMessages([]);
      }
    } catch (error) {
      console.error('Erreur lors de la suppression de la session:', error);
    }
  };

  // Helper for emojis (simple replace, can be improved with an emoji lib)
  const parseEmojis = (text: string) =>
    text.replace(/:([a-z0-9_]+):/g, (_, name) => {
      try {
        return String.fromCodePoint(
          // Simple emoji convert
          name === 'smile' ? 0x1F642 :
          name === 'sad' ? 0x1F641 :
          name === 'fire' ? 0x1F525 : 0x2753 // ?
        );
      } catch {
        return ':' + name + ':';
      }
    });

  // Enhanced send message handler
  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now(),
      role: 'user',
      content: inputText,
      timestamp: new Date().toISOString(),
      tokens_used: 0,
    };
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    // Simulate AI typing with animated ellipsis
    let ellipsis = '.';
    const typingMsg: ChatMessage = {
      id: Date.now() + 2,
      role: 'assistant',
      content: 'L\'IA est en train de répondre',
      timestamp: new Date().toISOString(),
      tokens_used: 0,
    };
    setMessages(prev => [...prev, typingMsg]);
    const interval = setInterval(() => {
      ellipsis = ellipsis.length < 3 ? ellipsis + '.' : '.';
      setMessages(prev => prev.map(msg => msg.id === typingMsg.id ? { ...msg, content: `L'IA est en train de répondre${ellipsis}` } : msg));
    }, 340);

    try {
      const response = await chatService.chatWithAI({
        message: userMessage.content,
        session_id: currentSession?.session_id,
        include_context: true,
      });
      clearInterval(interval);
      setMessages(prev => prev.filter(m => m.id !== typingMsg.id));
      const aiMessage: ChatMessage = {
        id: Date.now() + 3,
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp,
        tokens_used: response.tokens_used,
      };
      setMessages(prev => [...prev, aiMessage]);
      // Suggestion chips based on AI reply keywords
      if (response.response.includes('acné')) setSuggestions(["Soins pour l'acné","Nettoyage doux","Produits non-comédogènes","Voir routine recommandée"]);
      else if (response.response.includes('ride')) setSuggestions(["Produits anti-âge","Protection solaire","Routine anti-rides"]);
      else setSuggestions(["Conseil personnalisé","Recommencer","Voir profil peau"]);
    } catch (error) {
      clearInterval(interval);
      setMessages(prev => prev.filter(m => m.id !== typingMsg.id));
      const errorMessage: ChatMessage = {
        id: Date.now() + 4,
        role: 'assistant',
        content: '⚠️ Désolé, un problème technique est survenu. Réessayez ou contactez le support.',
        timestamp: new Date().toISOString(),
        tokens_used: 0,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  // Gestion du drag avec les événements de souris
  const handleMouseDown = (e: React.MouseEvent) => {
    // Vérifier si le clic est sur l'en-tête ou les éléments de drag
    const target = e.target as HTMLElement;
    if (target.classList.contains('drag-handle') || 
        target.closest('.drag-handle') ||
        target.classList.contains('drag-icon') ||
        target.closest('.drag-icon')) {
      setIsDragging(true);
      setDragOffset({
        x: e.clientX - position.x,
        y: e.clientY - position.y
      });
      e.preventDefault();
    }
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (isDragging) {
      const newX = e.clientX - dragOffset.x;
      const newY = e.clientY - dragOffset.y;
      if (onPositionChange) {
        onPositionChange({ x: newX, y: newY });
      }
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Ajouter les event listeners pour le drag
  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    }
  }, [isDragging, dragOffset, onPositionChange]);

  const handleSuggestionClick = (suggestion: string) => {
    setInputText(suggestion);
    setShowSuggestions(false);
  };

  if (!currentIsOpen) {
    // Bouton flottant réduit quand le chat est fermé - Position fixe en bas à droite
    return (
      <Box
        className={className}
        sx={{
          position: 'fixed',
          bottom: 24,
          right: 24,
          zIndex: 9999,
        }}
      >
        <Tooltip title="Ouvrir l'assistant Skin Twin AI">
          <IconButton
            onClick={() => handleOpenChange(true)}
            sx={{
              width: 64,
              height: 64,
              bgcolor: 'primary.main',
              color: 'white',
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
              '&:hover': {
                bgcolor: 'primary.dark',
                boxShadow: '0 6px 16px rgba(0,0,0,0.2)',
                transform: 'scale(1.05)',
              },
              transition: 'all 0.3s ease',
            }}
          >
            <AIIcon sx={{ fontSize: 32 }} />
          </IconButton>
        </Tooltip>
      </Box>
    );
  }

  return (
    <Paper
      ref={chatRef}
      className={className}
      sx={{
        position: 'fixed',
        bottom: 24,
        right: 24,
        width: isMinimized ? 420 : 420,
        height: isMinimized ? 'auto' : 650,
        maxHeight: isMinimized ? 'auto' : '85vh',
        zIndex: 10000,
        display: 'flex',
        flexDirection: 'column',
        borderRadius: 4,
        overflow: 'hidden',
        boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
        border: '1px solid rgba(33, 150, 243, 0.15)',
        backdropFilter: 'blur(16px)',
        background: 'linear-gradient(135deg,#e3f2fd .9,#f8fafc 100%)',
      }}
    >
        {/* En-tête */}
        <Box
          className="drag-handle"
          onMouseDown={handleMouseDown}
          sx={{
            p: 2.2,
            bgcolor: 'primary.main',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            cursor: isDragging ? 'grabbing' : 'grab',
            userSelect: 'none',
            background: 'linear-gradient(90deg, #2196F3 60%, #21CBF3 100%)',
            boxShadow: '0 2px 18px rgba(33,150,243,.05)',
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.22)', width: 44, height: 44, border: '2.5px solid #87CEEB', boxShadow: '0 2px 8px #b0e0e650' }}>
              <AIIcon fontSize="large" />
            </Avatar>
            <Box>
              <Typography variant="subtitle1" fontWeight="bold">
                Skin Twin AI
              </Typography>
              <Typography variant="caption" sx={{ opacity: 0.8 }}>
                {isVoiceMode ? "Mode vocal activé" : "Assistant IA Intelligent"}
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Tooltip title="Historique des conversations">
              <IconButton
                size="small"
                onClick={() => setShowSessions(true)}
                sx={{ color: 'white' }}
              >
                <HistoryIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Nouvelle conversation">
              <IconButton
                size="small"
                onClick={createNewSession}
                sx={{ color: 'white' }}
              >
                <AddIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Suggestions">
              <IconButton
                size="small"
                onClick={() => setShowSuggestions(!showSuggestions)}
                sx={{ color: 'white' }}
              >
                <LightbulbIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Déplacer">
              <DragIcon className="drag-icon" sx={{ cursor: 'grab', opacity: 0.7 }} />
            </Tooltip>
            <Tooltip title="Réduire">
              <IconButton
                size="small"
                onClick={() => setIsMinimized(!isMinimized)}
                sx={{ color: 'white', '&:hover': { bgcolor: 'rgba(255,255,255,0.1)' } }}
              >
                <MinimizeIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Fermer">
              <IconButton
                size="small"
                onClick={() => handleOpenChange(false)}
                sx={{ color: 'white', '&:hover': { bgcolor: 'rgba(255,255,255,0.1)' } }}
              >
                <CloseIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>

        {/* Messages */}
        {!isMinimized && (
          <Box sx={{ flex: 1, overflow: 'auto', p: 1 }}>
          {messages.length === 0 && (
            <Box sx={{ textAlign: 'center', py: 4, color: 'text.secondary' }}>
              <AIIcon sx={{ fontSize: 48, mb: 2, opacity: 0.5 }} />
              <Typography variant="h6" gutterBottom>
                Bienvenue dans Skin Twin AI
              </Typography>
              <Typography variant="body2">
                Je suis votre assistant dermatologique intelligent. Posez-moi vos questions sur les soins de la peau !
              </Typography>
            </Box>
          )}
          
          {messages.map((message) => (
            <Box
              key={message.id}
              sx={{
                display: 'flex',
                mb: 2,
                justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
              }}
            >
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: 1,
                  maxWidth: '80%',
                  flexDirection: message.role === 'user' ? 'row-reverse' : 'row',
                }}
              >
                <Avatar
                  sx={{
                    bgcolor: message.role === 'user' ? 'primary.main' : 'secondary.main',
                    width: 32,
                    height: 32,
                  }}
                >
                  {message.role === 'user' ? <PersonIcon /> : <AIIcon />}
                </Avatar>
                <Paper
                  sx={{
                    my: 1.2,
                    p: 1.8,
                    bgcolor: message.role === 'user' ? 'primary.main' : 'grey.50',
                    color: message.role === 'user' ? 'white' : 'text.primary',
                    borderRadius: 3.5,
                    wordBreak: 'break-word',
                    fontSize: "1.05rem",
                    filter: message.role === 'user' ? undefined : 'drop-shadow(0 2px 8px #b0e0e690)',
                  }}
                >
                  {/* Use a markdown/emoji parser here in final version! */}
                  <ReactMarkdown remarkPlugins={[remarkGfm]} children={parseEmojis(message.content)} />
                </Paper>
              </Box>
            </Box>
          ))}
          
          {isLoading && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.7, p: 2 }}>
              <Avatar sx={{ bgcolor: 'secondary.main', width: 36, height: 36 }}>
                <AIIcon fontSize="small" />
              </Avatar>
              <Paper sx={{ px: 2.2, py: 1, bgcolor: 'info.light', borderRadius: 2.5, color: 'info.dark' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.2 }}>
                  <CircularProgress size={20} thickness={6} sx={{ mr: 1 }}/>
                  <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
                    L'IA réfléchit...<span className="blinking-dot">•</span>
                  </Typography>
                </Box>
              </Paper>
              <style>{`.blinking-dot { animation: blink 1.2s infinite; } @keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0;} }`}</style>
            </Box>
          )}
          
          <div ref={messagesEndRef} />
        </Box>
        )}

        {!isMinimized && (
          <>
            <Divider />

            {/* Zone de saisie */}
            <Box sx={{ p: 2.5 }}>
          <Box sx={{ display: 'flex', gap: 1.5, alignItems: 'flex-end' }}>
            <TextField
              fullWidth
              multiline
              maxRows={4}
              placeholder={isVoiceMode ? "Parlez maintenant... (Mode vocal activé)" : "Posez votre question à l'IA..."}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              variant="outlined"
              size="small"
              inputProps={{ 'aria-label': 'Zone de saisie du message' }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 3.5,
                  backgroundColor: isVoiceMode ? '#c5eafc' : 'white',
                  borderColor: isVoiceMode ? '#21CBF3' : undefined,
                },
              }}
            />
            {/* Voice button animation improved */}
            <Tooltip title={isVoiceMode ? "Désactiver le mode vocal" : "Activer le mode vocal"}>
              <IconButton
                color={isVoiceMode ? "error" : "primary"}
                aria-label={isVoiceMode ? "Désactiver le mode vocal" : "Activer le mode vocal"}
                onClick={async () => {
                  // Demander l'autorisation du microphone si nécessaire
                  if (!isVoiceMode && ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
                    try {
                      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                      stream.getTracks().forEach(track => track.stop()); // Arrêter immédiatement, on voulait juste vérifier l'autorisation
                      onVoiceModeChange?.(!isVoiceMode);
                    } catch (error: any) {
                      console.error('Erreur d\'accès au microphone:', error);
                      alert('Veuillez autoriser l\'accès au microphone dans les paramètres de votre navigateur pour utiliser le mode vocal.');
                    }
                  } else {
                    onVoiceModeChange?.(!isVoiceMode);
                  }
                }}
                sx={{
                  bgcolor: isVoiceMode ? 'error.main' : 'primary.main',
                  color: 'white',
                  boxShadow: isListening ? '0 0 8px #2196F3' : undefined,
                  '&:hover': {
                    bgcolor: isVoiceMode ? 'error.dark' : 'primary.dark',
                  },
                  animation: isListening ? 'pulse 1.2s infinite' : 'none',
                  '@keyframes pulse': {
                    '0%': { transform: 'scale(1)' },
                    '50%': { transform: 'scale(1.09)' },
                    '100%': { transform: 'scale(1)' },
                  },
                }}
              >
                {isVoiceMode ? <MicOffIcon /> : <MicIcon />}
              </IconButton>
            </Tooltip>
            <IconButton
              color="primary"
              aria-label="Envoyer le message"
              onClick={handleSendMessage}
              disabled={!inputText.trim() || isLoading}
              sx={{
                bgcolor: 'primary.main',
                color: 'white',
                '&:hover': {
                  bgcolor: 'primary.dark',
                },
                '&:disabled': {
                  bgcolor: 'grey.200',
                },
              }}
            >
              <SendIcon />
            </IconButton>
          </Box>
          {/* Animate suggestion chips */}
          {showSuggestions && suggestions.length > 0 && (
            <Box sx={{ mt: 1.6, display: 'flex', gap: 0.75, flexWrap: 'wrap' }}>
              {suggestions.slice(0, 4).map((suggestion, index) => (
                <Chip
                  key={index}
                  label={suggestion}
                  size="small"
                  onClick={() => handleSuggestionClick(suggestion)}
                  sx={{
                    cursor: 'pointer',
                    transition: '0.18s',
                    fontWeight: 600,
                    bgcolor: '#E1F5FE',
                    color: '#1976D2',
                    '&:hover': {
                      bgcolor: 'primary.light',
                      color: 'white',
                      transform: 'scale(1.10)',
                    },
                  }}
                />
              ))}
            </Box>
          )}
        </Box>
        </>
        )}
      </Paper>
  );
};

export default ChatAI;
