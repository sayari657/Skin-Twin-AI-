import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Fab,
  Paper,
  TextField,
  IconButton,
  Typography,
  Avatar,
  Chip,
  Fade,
  Slide,
  Divider,
  CircularProgress,
  Tooltip,
} from '@mui/material';
import {
  Chat as ChatIcon,
  Send as SendIcon,
  Close as CloseIcon,
  DragIndicator as DragIcon,
  Psychology as AIIcon,
  SmartToy as BotIcon,
  Person as PersonIcon,
  Mic as MicIcon,
  MicOff as MicOffIcon,
  RecordVoiceOver as VoiceIcon,
} from '@mui/icons-material';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  isTyping?: boolean;
}

interface ChatFloatingProps {
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

const ChatFloating: React.FC<ChatFloatingProps> = ({
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
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: '👋 Bonjour ! Je suis votre assistant Skin Twin AI. Comment puis-je vous aider avec votre peau aujourd\'hui ?',
      isUser: false,
      timestamp: new Date(),
    },
  ]);

  // Gérer l'état externe
  const currentIsOpen = externalIsOpen !== undefined ? externalIsOpen : isOpen;
  
  const handleOpenChange = (newIsOpen: boolean) => {
    if (externalIsOpen !== undefined) {
      onOpenChange?.(newIsOpen);
    } else {
      setIsOpen(newIsOpen);
    }
  };

  // Ajouter un message initial si fourni
  useEffect(() => {
    if (initialMessage && !messages.find(m => m.text === initialMessage)) {
      const newMessage: Message = {
        id: Date.now().toString(),
        text: initialMessage,
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, newMessage]);
    }
  }, [initialMessage]);

  // Remplir le champ de saisie avec un message
  useEffect(() => {
    if (fillInputWithMessage) {
      setInputText(fillInputWithMessage);
      // Ouvrir le chat automatiquement si un message est fourni
      if (!currentIsOpen) {
        handleOpenChange(true);
      }
      // Ajouter une animation pour attirer l'attention sur le champ de saisie
      setTimeout(() => {
        const inputElement = document.querySelector('input[placeholder="Posez votre question..."]') as HTMLInputElement;
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
  const [inputText, setInputText] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [isTyping, setIsTyping] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState<any>(null);
  const chatRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll vers le bas quand de nouveaux messages arrivent
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialiser la reconnaissance vocale
  useEffect(() => {
    if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      recognitionInstance.continuous = true;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = 'fr-FR';

      recognitionInstance.onstart = () => {
        setIsListening(true);
      };

      recognitionInstance.onresult = (event: any) => {
        let finalTranscript = '';
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }

        if (finalTranscript) {
          setInputText(prev => prev + finalTranscript);
        } else if (interimTranscript) {
          // Afficher le texte en cours de reconnaissance
          setInputText(prev => prev + interimTranscript);
        }
      };

      recognitionInstance.onerror = (event: any) => {
        console.error('Erreur de reconnaissance vocale:', event.error);
        setIsListening(false);
      };

      recognitionInstance.onend = () => {
        setIsListening(false);
      };

      setRecognition(recognitionInstance);
    }
  }, []);

  // Gérer le mode vocal
  useEffect(() => {
    if (isVoiceMode && recognition) {
      if (!isListening) {
        recognition.start();
      }
    } else if (!isVoiceMode && recognition && isListening) {
      recognition.stop();
    }
  }, [isVoiceMode, recognition, isListening]);

  // Réponses IA intelligentes basées sur le projet Skin Twin AI
  const getAIResponse = (userMessage: string): string => {
    const message = userMessage.toLowerCase();
    
    // Réponses sur l'analyse de peau
    if (message.includes('analyse') || message.includes('peau') || message.includes('photo')) {
      return '🔬 Pour analyser votre peau, allez dans "Nouvelle analyse" et prenez une photo de votre visage. Notre IA détectera automatiquement les problèmes comme l\'acné, les rides, les taches et les rougeurs.';
    }
    
    // Réponses sur les produits
    if (message.includes('produit') || message.includes('crème') || message.includes('soin')) {
      return '🛍️ Découvrez nos produits recommandés dans la section "Produits". Ils sont adaptés à votre type de peau et à vos problèmes spécifiques.';
    }
    
    // Réponses sur le type de peau
    if (message.includes('type') || message.includes('grasse') || message.includes('sèche') || message.includes('mixte')) {
      return '🎯 Votre type de peau est déterminé par notre IA lors de l\'analyse. Les types incluent : sèche, grasse, mixte, normale et sensible.';
    }
    
    // Réponses sur les problèmes cutanés
    if (message.includes('acné') || message.includes('bouton') || message.includes('imperfection')) {
      return '🔍 Notre IA peut détecter l\'acné et évaluer sa sévérité. Je recommande des produits non-comédogènes et un nettoyage doux.';
    }
    
    if (message.includes('ride') || message.includes('vieillissement')) {
      return '⏰ Les rides sont détectées par notre IA avec une évaluation de sévérité. Les antioxydants et la protection solaire sont essentiels.';
    }
    
    if (message.includes('tache') || message.includes('pigmentation')) {
      return '🌞 Les taches sombres sont analysées par notre IA. La protection solaire et les ingrédients éclaircissants peuvent aider.';
    }
    
    // Réponses sur l'historique
    if (message.includes('historique') || message.includes('résultat') || message.includes('analyse précédente')) {
      return '📊 Consultez votre historique d\'analyses dans la section "Historique" pour voir l\'évolution de votre peau dans le temps.';
    }
    
    // Réponses sur le profil
    if (message.includes('profil') || message.includes('information') || message.includes('données')) {
      return '👤 Votre profil contient vos informations personnelles et vos préférences. Vous pouvez le modifier dans "Mon Profil".';
    }
    
    // Réponses sur l'IA
    if (message.includes('ia') || message.includes('intelligence') || message.includes('algorithme')) {
      return '🤖 Notre IA utilise des modèles CNN pour la classification et YOLO pour la détection. Elle analyse votre peau avec une précision de 95%.';
    }
    
    // Réponses sur les recommandations
    if (message.includes('conseil') || message.includes('recommandation') || message.includes('aide')) {
      return '💡 Basé sur votre analyse, je peux recommander des produits, des routines de soin et des conseils personnalisés pour votre peau.';
    }
    
    // Réponses générales
    if (message.includes('bonjour') || message.includes('salut') || message.includes('hello')) {
      return '👋 Bonjour ! Je suis là pour vous aider avec tout ce qui concerne votre peau et notre application Skin Twin AI.';
    }
    
    if (message.includes('merci') || message.includes('thanks')) {
      return '😊 De rien ! N\'hésitez pas si vous avez d\'autres questions sur votre peau ou l\'application.';
    }
    
    // Réponse par défaut
    return '🤔 Je comprends votre question. Pouvez-vous être plus spécifique ? Je peux vous aider avec l\'analyse de peau, les produits, votre profil, ou l\'historique.';
  };

  const handleSendMessage = () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    // Garder le message dans le champ de saisie au lieu de le vider
    // setInputText(''); // Commenté pour garder le message
    setIsTyping(true);

    // Simuler le délai de réponse de l'IA
    setTimeout(() => {
      const aiResponse = getAIResponse(inputText);
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: aiResponse,
        isUser: false,
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, aiMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleDragStart = (e: React.MouseEvent) => {
    setIsDragging(true);
    const rect = chatRef.current?.getBoundingClientRect();
    if (rect) {
      setDragOffset({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
      });
    }
  };

  const handleDragMove = (e: MouseEvent) => {
    if (!isDragging) return;
    
    const newPosition = {
      x: e.clientX - dragOffset.x,
      y: e.clientY - dragOffset.y,
    };
    
    // Limiter la position dans les limites de l'écran
    const maxX = window.innerWidth - (isOpen ? 350 : 60);
    const maxY = window.innerHeight - (isOpen ? 500 : 60);
    
    newPosition.x = Math.max(0, Math.min(newPosition.x, maxX));
    newPosition.y = Math.max(0, Math.min(newPosition.y, maxY));
    
    onPositionChange?.(newPosition);
  };

  const handleDragEnd = () => {
    setIsDragging(false);
  };

  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleDragMove);
      document.addEventListener('mouseup', handleDragEnd);
      return () => {
        document.removeEventListener('mousemove', handleDragMove);
        document.removeEventListener('mouseup', handleDragEnd);
      };
    }
  }, [isDragging, dragOffset]);

  return (
    <Box
      ref={chatRef}
      sx={{
        position: 'fixed',
        left: position.x,
        top: position.y,
        zIndex: 1000,
        cursor: isDragging ? 'grabbing' : 'grab',
        userSelect: 'none',
      }}
      className={className}
    >
      {/* Cercle flottant */}
      {!currentIsOpen && (
        <Fade in={!currentIsOpen}>
          <Fab
            color="primary"
            size="large"
            onClick={() => handleOpenChange(true)}
            onMouseDown={handleDragStart}
            sx={{
              background: 'linear-gradient(45deg, #2196F3, #21CBF3)',
              boxShadow: '0 8px 25px rgba(33, 150, 243, 0.3)',
              '&:hover': {
                background: 'linear-gradient(45deg, #1976D2, #1CB5E0)',
                transform: 'scale(1.1)',
              },
              transition: 'all 0.3s ease',
            }}
          >
            <ChatIcon />
          </Fab>
        </Fade>
      )}

      {/* Interface de chat */}
      {currentIsOpen && (
        <Slide direction="up" in={currentIsOpen} mountOnEnter unmountOnExit>
          <Paper
            elevation={8}
            sx={{
              width: 350,
              height: 500,
              display: 'flex',
              flexDirection: 'column',
              borderRadius: 3,
              overflow: 'hidden',
              background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
            }}
          >
            {/* En-tête du chat */}
            <Box
              sx={{
                background: 'linear-gradient(45deg, #2196F3, #21CBF3)',
                color: 'white',
                p: 2,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                cursor: 'grab',
              }}
              onMouseDown={handleDragStart}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)' }}>
                  <BotIcon />
                </Avatar>
                <Box>
                  <Typography variant="subtitle1" fontWeight="bold">
                    Skin Twin AI
                  </Typography>
                  <Typography variant="caption" sx={{ opacity: 0.8 }}>
                    {isVoiceMode ? "Mode vocal activé" : "Assistant intelligent"}
                  </Typography>
                </Box>
              </Box>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <Tooltip title="Déplacer">
                  <DragIcon sx={{ cursor: 'grab', opacity: 0.7 }} />
                </Tooltip>
                <IconButton
                  size="small"
                  onClick={() => handleOpenChange(false)}
                  sx={{ color: 'white' }}
                >
                  <CloseIcon />
                </IconButton>
              </Box>
            </Box>

            {/* Messages */}
            <Box
              sx={{
                flex: 1,
                overflow: 'auto',
                p: 2,
                display: 'flex',
                flexDirection: 'column',
                gap: 1,
              }}
            >
              {messages.map((message) => (
                <Box
                  key={message.id}
                  sx={{
                    display: 'flex',
                    justifyContent: message.isUser ? 'flex-end' : 'flex-start',
                    mb: 1,
                  }}
                >
                  <Box
                    sx={{
                      maxWidth: '80%',
                      p: 1.5,
                      borderRadius: 2,
                      background: message.isUser
                        ? 'linear-gradient(45deg, #2196F3, #21CBF3)'
                        : 'white',
                      color: message.isUser ? 'white' : 'text.primary',
                      boxShadow: 1,
                    }}
                  >
                    <Typography variant="body2">
                      {message.text}
                    </Typography>
                    <Typography
                      variant="caption"
                      sx={{
                        opacity: 0.7,
                        fontSize: '0.7rem',
                        display: 'block',
                        mt: 0.5,
                      }}
                    >
                      {message.timestamp.toLocaleTimeString('fr-FR', {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </Typography>
                  </Box>
                </Box>
              ))}

              {/* Indicateur de frappe */}
              {isTyping && (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                  <Avatar sx={{ width: 24, height: 24, bgcolor: 'grey.300' }}>
                    <BotIcon sx={{ fontSize: 16 }} />
                  </Avatar>
                  <Box sx={{ display: 'flex', gap: 0.5 }}>
                    <CircularProgress size={16} />
                    <Typography variant="caption" color="text.secondary">
                      IA réfléchit...
                    </Typography>
                  </Box>
                </Box>
              )}

              <div ref={messagesEndRef} />
            </Box>

            <Divider />

            {/* Zone de saisie */}
            <Box sx={{ p: 2 }}>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
                <TextField
                  fullWidth
                  multiline
                  maxRows={3}
                  placeholder={isVoiceMode ? "Parlez maintenant... (Mode vocal activé)" : "Posez votre question..."}
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyPress={handleKeyPress}
                  variant="outlined"
                  size="small"
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      borderRadius: 3,
                      backgroundColor: isVoiceMode ? '#e3f2fd' : 'white',
                      borderColor: isVoiceMode ? '#2196F3' : undefined,
                    },
                  }}
                />
                <Tooltip title={isVoiceMode ? "Désactiver le mode vocal" : "Activer le mode vocal"}>
                  <IconButton
                    color={isVoiceMode ? "error" : "primary"}
                    onClick={() => onVoiceModeChange?.(!isVoiceMode)}
                    sx={{
                      bgcolor: isVoiceMode ? 'error.main' : 'primary.main',
                      color: 'white',
                      '&:hover': {
                        bgcolor: isVoiceMode ? 'error.dark' : 'primary.dark',
                      },
                      animation: isListening ? 'pulse 1s infinite' : 'none',
                      '@keyframes pulse': {
                        '0%': { transform: 'scale(1)' },
                        '50%': { transform: 'scale(1.1)' },
                        '100%': { transform: 'scale(1)' },
                      },
                    }}
                  >
                    {isVoiceMode ? <MicOffIcon /> : <MicIcon />}
                  </IconButton>
                </Tooltip>
                <IconButton
                  color="primary"
                  onClick={handleSendMessage}
                  disabled={!inputText.trim()}
                  sx={{
                    bgcolor: 'primary.main',
                    color: 'white',
                    '&:hover': {
                      bgcolor: 'primary.dark',
                    },
                    '&:disabled': {
                      bgcolor: 'grey.300',
                    },
                  }}
                >
                  <SendIcon />
                </IconButton>
              </Box>
              
              {/* Suggestions rapides */}
              <Box sx={{ mt: 1, display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                {['Analyser ma peau', 'Produits recommandés', 'Mon profil'].map((suggestion) => (
                  <Chip
                    key={suggestion}
                    label={suggestion}
                    size="small"
                    onClick={() => setInputText(suggestion)}
                    sx={{
                      fontSize: '0.7rem',
                      height: 24,
                      '&:hover': {
                        bgcolor: 'primary.light',
                        color: 'white',
                      },
                    }}
                  />
                ))}
              </Box>
            </Box>
          </Paper>
        </Slide>
      )}
    </Box>
  );
};

export default ChatFloating;
