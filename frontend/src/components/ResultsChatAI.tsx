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
  Button,
  Collapse,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  Send as SendIcon,
  Close as CloseIcon,
  Psychology as AIIcon,
  Person as PersonIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Download as DownloadIcon,
  Fullscreen as FullscreenIcon,
  PictureAsPdf as PdfIcon,
  Remove as MinimizeIcon,
} from '@mui/icons-material';
import { chatService, ChatMessage } from '../services/chatService';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { SkinAnalysis } from '../types';

interface ResultsChatAIProps {
  analysis: SkinAnalysis;
  isOpen?: boolean;
  onOpenChange?: (isOpen: boolean) => void;
}

const ResultsChatAI: React.FC<ResultsChatAIProps> = ({
  analysis,
  isOpen: externalIsOpen,
  onOpenChange,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showReport, setShowReport] = useState(false);
  const [reportContent, setReportContent] = useState<string>('');
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const [reportFullscreenOpen, setReportFullscreenOpen] = useState(false);
  const [downloadMenuAnchor, setDownloadMenuAnchor] = useState<null | HTMLElement>(null);
  const [isMinimized, setIsMinimized] = useState(false);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatRef = useRef<HTMLDivElement>(null);
  const reportRef = useRef<HTMLDivElement>(null);
  const reportFullscreenRef = useRef<HTMLDivElement>(null);

  const currentIsOpen = externalIsOpen !== undefined ? externalIsOpen : isOpen;

  // Auto-scroll vers le bas quand de nouveaux messages arrivent
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Message initial avec contexte de l'analyse
  useEffect(() => {
    if (currentIsOpen && messages.length === 0) {
      const initialMessage: ChatMessage = {
        id: Date.now(),
        role: 'assistant',
        content: `👋 Bonjour ! Je suis votre assistant Skin Twin AI spécialisé dans l'analyse de votre peau.

📊 **Résumé de votre analyse :**
- **Type de peau détecté :** ${analysis.skin_type_prediction || 'Non déterminé'}
- **Confiance :** ${analysis.skin_type_confidence ? (analysis.skin_type_confidence * 100).toFixed(1) : 'N/A'}%

**Problèmes détectés :**
${analysis.acne_detected ? `- ✅ Acné (${analysis.acne_severity || 'N/A'})` : '- ❌ Aucune acné'}
${analysis.wrinkles_detected ? `- ✅ Rides (${analysis.wrinkles_severity || 'N/A'})` : '- ❌ Aucune ride'}
${analysis.dark_spots_detected ? `- ✅ Taches sombres (${analysis.dark_spots_severity || 'N/A'})` : '- ❌ Aucune tache'}
${analysis.redness_detected ? `- ✅ Rougeurs (${analysis.redness_severity || 'N/A'})` : '- ❌ Aucune rougeur'}

💬 **Comment puis-je vous aider ?**
- Posez-moi des questions sur vos résultats
- Demandez-moi de générer un rapport détaillé
- Obtenez des conseils personnalisés pour votre peau`,
        timestamp: new Date().toISOString(),
        tokens_used: 0,
      };
      setMessages([initialMessage]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentIsOpen]);

  const handleOpenChange = (open: boolean) => {
    if (onOpenChange) {
      onOpenChange(open);
    } else {
      setIsOpen(open);
    }
  };

  const buildAnalysisContext = (): string => {
    const context = {
      skin_type: analysis.skin_type_prediction,
      skin_type_confidence: analysis.skin_type_confidence,
      acne: {
        detected: analysis.acne_detected,
        severity: analysis.acne_severity,
        confidence: analysis.acne_confidence,
      },
      wrinkles: {
        detected: analysis.wrinkles_detected,
        severity: analysis.wrinkles_severity,
        confidence: analysis.wrinkles_confidence,
      },
      dark_spots: {
        detected: analysis.dark_spots_detected,
        severity: analysis.dark_spots_severity,
        confidence: analysis.dark_spots_confidence,
      },
      redness: {
        detected: analysis.redness_detected,
        severity: analysis.redness_severity,
        confidence: analysis.redness_confidence,
      },
      analysis_date: analysis.analysis_date,
      processing_time: analysis.processing_time,
    };
    return JSON.stringify(context);
  };

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
    const currentInput = inputText;
    setInputText('');
    setIsLoading(true);

    // Message de chargement
    const typingMsg: ChatMessage = {
      id: Date.now() + 1,
      role: 'assistant',
      content: 'L\'IA analyse votre question...',
      timestamp: new Date().toISOString(),
      tokens_used: 0,
    };
    setMessages(prev => [...prev, typingMsg]);

    try {
      // Construire le contexte système avec les résultats de l'analyse
      const analysisContext = buildAnalysisContext();
      const systemPrompt = `Tu es Skin Twin AI, un assistant dermatologique expert. Tu analyses les résultats d'une analyse de peau et réponds aux questions de l'utilisateur.

CONTEXTE DE L'ANALYSE ACTUELLE:
${analysisContext}

Tu dois :
1. Répondre aux questions sur les résultats de l'analyse
2. Expliquer ce que signifient les détections (acné, rides, taches, rougeurs)
3. Donner des conseils personnalisés basés sur les résultats
4. Proposer des routines de soins adaptées
5. Être précis, professionnel et empathique

Réponds en français de manière claire et détaillée.`;

      const response = await chatService.chatWithAI({
        message: currentInput,
        session_id: undefined,
        include_context: false,
        system: systemPrompt,
        analysis_context: analysisContext,
      });
      
      setMessages(prev => prev.filter(m => m.id !== typingMsg.id));
      const aiMessage: ChatMessage = {
        id: Date.now() + 2,
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp,
        tokens_used: response.tokens_used,
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Erreur lors du chat:', error);
      setMessages(prev => prev.filter(m => m.id !== typingMsg.id));
      const errorMessage: ChatMessage = {
        id: Date.now() + 3,
        role: 'assistant',
        content: '⚠️ Désolé, un problème technique est survenu. Réessayez dans quelques instants.',
        timestamp: new Date().toISOString(),
        tokens_used: 0,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    setIsGeneratingReport(true);
    setShowReport(true);

    try {
      const analysisContext = buildAnalysisContext();
      const reportPrompt = `Génère un rapport détaillé et professionnel sur cette analyse de peau en français. Le rapport doit inclure :

1. **Résumé exécutif** : Vue d'ensemble des résultats
2. **Type de peau** : Analyse détaillée du type détecté
3. **Problèmes détectés** : Description de chaque problème (acné, rides, taches, rougeurs) avec sévérité et confiance
4. **Recommandations** : Conseils personnalisés pour chaque problème
5. **Routine de soins** : Routine matin/soir adaptée
6. **Produits recommandés** : Types de produits à utiliser
7. **Suivi** : Conseils pour le suivi et l'amélioration

CONTEXTE DE L'ANALYSE:
${analysisContext}

Formatte le rapport en Markdown avec des sections claires.`;

      const response = await chatService.chatWithAI({
        message: reportPrompt,
        session_id: undefined,
        include_context: false,
        system: 'Tu es un expert dermatologique qui génère des rapports détaillés et professionnels.',
        analysis_context: analysisContext,
      });

      setReportContent(response.response);
    } catch (error) {
      console.error('Erreur lors de la génération du rapport:', error);
      setReportContent('⚠️ Erreur lors de la génération du rapport. Veuillez réessayer.');
    } finally {
      setIsGeneratingReport(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  // Télécharger le rapport en texte
  const handleDownloadText = () => {
    if (!reportContent) return;
    
    const blob = new Blob([reportContent], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `rapport_analyse_${analysis.id}_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    setDownloadMenuAnchor(null);
  };

  // Télécharger le rapport en PDF
  const handleDownloadPDF = async () => {
    if (!reportContent) return;
    
    // Utiliser la ref du rapport plein écran si disponible, sinon celle du rapport réduit
    const element = reportFullscreenRef.current || reportRef.current;
    if (!element) {
      console.error('Élément du rapport non trouvé');
      handleDownloadText();
      return;
    }
    
    try {
      // Utiliser html2pdf.js pour générer le PDF
      const html2pdf = (await import('html2pdf.js')).default;
      
      const opt = {
        margin: [0.5, 0.5, 0.5, 0.5] as [number, number, number, number],
        filename: `rapport_analyse_${analysis.id}_${new Date().toISOString().split('T')[0]}.pdf`,
        image: { type: 'jpeg' as const, quality: 0.98 },
        html2canvas: { 
          scale: 2,
          useCORS: true,
          logging: false,
        },
        jsPDF: { unit: 'in', format: 'a4', orientation: 'portrait' as const }
      };
      
      await html2pdf().set(opt).from(element).save();
      setDownloadMenuAnchor(null);
    } catch (error) {
      console.error('Erreur lors de la génération du PDF:', error);
      // Fallback: télécharger en texte si html2pdf n'est pas disponible
      handleDownloadText();
    }
  };

  // Ouvrir le rapport en plein écran
  const handleOpenFullscreen = () => {
    setReportFullscreenOpen(true);
    setDownloadMenuAnchor(null);
  };

  if (!currentIsOpen) {
    return (
      <Box sx={{ position: 'fixed', bottom: 24, right: 24, zIndex: 9999 }}>
        <Tooltip title="Ouvrir l'assistant de résultats">
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
      sx={{
        position: 'fixed',
        bottom: 24,
        right: 24,
        width: 450,
        height: isMinimized ? 'auto' : 600,
        maxHeight: isMinimized ? 'none' : '85vh',
        zIndex: 10000,
        display: 'flex',
        flexDirection: 'column',
        borderRadius: 4,
        overflow: 'hidden',
        boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
        border: '1px solid rgba(194, 24, 91, 0.15)',
        backdropFilter: 'blur(16px)',
        background: 'linear-gradient(135deg, #fff5f5 0%, #ffffff 100%)',
      }}
    >
      {/* En-tête */}
      <Box
        sx={{
          p: 2,
          bgcolor: 'primary.main',
          color: 'white',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'linear-gradient(90deg, #C2185B 60%, #E91E63 100%)',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.22)', width: 40, height: 40 }}>
            <AIIcon fontSize="small" />
          </Avatar>
          <Box>
            <Typography variant="subtitle1" fontWeight="bold">
              Assistant Résultats
            </Typography>
            <Typography variant="caption" sx={{ opacity: 0.9 }}>
              Analyse #{analysis.id}
            </Typography>
          </Box>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Tooltip title={isMinimized ? "Agrandir" : "Réduire"}>
            <IconButton
              size="small"
              onClick={() => setIsMinimized(!isMinimized)}
              sx={{ color: 'white' }}
            >
              {isMinimized ? <ExpandMoreIcon /> : <MinimizeIcon />}
            </IconButton>
          </Tooltip>
          <Tooltip title="Fermer">
            <IconButton
              size="small"
              onClick={() => handleOpenChange(false)}
              sx={{ color: 'white' }}
            >
              <CloseIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* Rapport généré */}
      {!isMinimized && (
        <Collapse in={showReport}>
        <Box sx={{ p: 2, bgcolor: 'info.50', borderBottom: '1px solid', borderColor: 'divider' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
            <Typography variant="h6" sx={{ fontSize: '1rem', fontWeight: 'bold' }}>
              📄 Rapport d'Analyse
            </Typography>
            <Box sx={{ display: 'flex', gap: 0.5 }}>
              {reportContent && (
                <>
                  <Tooltip title="Télécharger">
                    <IconButton
                      size="small"
                      onClick={(e) => setDownloadMenuAnchor(e.currentTarget)}
                      sx={{ color: 'primary.main' }}
                    >
                      <DownloadIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Voir en plein écran">
                    <IconButton
                      size="small"
                      onClick={handleOpenFullscreen}
                      sx={{ color: 'primary.main' }}
                    >
                      <FullscreenIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                </>
              )}
              <IconButton size="small" onClick={() => setShowReport(false)}>
                <ExpandLessIcon />
              </IconButton>
            </Box>
          </Box>
          {isGeneratingReport ? (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <CircularProgress size={20} />
              <Typography variant="body2">Génération du rapport...</Typography>
            </Box>
          ) : reportContent ? (
            <Box
              ref={reportRef}
              sx={{
                maxHeight: 200,
                overflow: 'auto',
                p: 1,
                bgcolor: 'white',
                borderRadius: 1,
                border: '1px solid',
                borderColor: 'divider',
              }}
            >
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{reportContent}</ReactMarkdown>
            </Box>
          ) : null}
        </Box>
      </Collapse>
      )}

      {/* Menu de téléchargement */}
      <Menu
        anchorEl={downloadMenuAnchor}
        open={Boolean(downloadMenuAnchor)}
        onClose={() => setDownloadMenuAnchor(null)}
      >
        <MenuItem onClick={handleDownloadText}>
          <ListItemIcon>
            <DownloadIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Télécharger en texte (.txt)</ListItemText>
        </MenuItem>
        <MenuItem onClick={handleDownloadPDF}>
          <ListItemIcon>
            <PdfIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Télécharger en PDF</ListItemText>
        </MenuItem>
      </Menu>

      {/* Dialog plein écran pour le rapport */}
      <Dialog
        open={reportFullscreenOpen}
        onClose={() => setReportFullscreenOpen(false)}
        maxWidth="lg"
        fullWidth
        PaperProps={{
          sx: {
            maxHeight: '90vh',
            height: '90vh',
          }
        }}
      >
        <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h5">📄 Rapport d'Analyse - Analyse #{analysis.id}</Typography>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Tooltip title="Télécharger">
              <IconButton
                size="small"
                onClick={(e) => {
                  setDownloadMenuAnchor(e.currentTarget);
                }}
              >
                <DownloadIcon />
              </IconButton>
            </Tooltip>
            <IconButton size="small" onClick={() => setReportFullscreenOpen(false)}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent sx={{ overflow: 'auto' }}>
          <Box
            ref={reportFullscreenRef}
            sx={{
              p: 3,
              bgcolor: 'white',
              borderRadius: 1,
            }}
          >
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{reportContent}</ReactMarkdown>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setReportFullscreenOpen(false)} variant="contained">
            Fermer
          </Button>
        </DialogActions>
      </Dialog>

      {/* Messages */}
      {!isMinimized && (
        <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
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
                maxWidth: '85%',
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
                  p: 1.5,
                  bgcolor: message.role === 'user' ? 'primary.main' : 'grey.50',
                  color: message.role === 'user' ? 'white' : 'text.primary',
                  borderRadius: 3,
                  wordBreak: 'break-word',
                }}
              >
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {message.content}
                </ReactMarkdown>
              </Paper>
            </Box>
          </Box>
        ))}
        
        {isLoading && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, p: 2 }}>
            <Avatar sx={{ bgcolor: 'secondary.main', width: 32, height: 32 }}>
              <AIIcon fontSize="small" />
            </Avatar>
            <Paper sx={{ px: 2, py: 1, bgcolor: 'info.light', borderRadius: 2 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <CircularProgress size={16} />
                <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
                  L'IA réfléchit...
                </Typography>
              </Box>
            </Paper>
          </Box>
        )}
        
        <div ref={messagesEndRef} />
      </Box>
      )}

      {!isMinimized && <Divider />}

      {/* Zone de saisie */}
      {!isMinimized && (
        <Box sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            placeholder="Posez votre question sur les résultats..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            variant="outlined"
            size="small"
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 3,
                backgroundColor: 'white',
              },
            }}
          />
          <IconButton
            color="primary"
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isLoading}
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
        <Box sx={{ mt: 1.5, display: 'flex', gap: 0.75, flexWrap: 'wrap' }}>
          {[
            'Expliquez mes résultats',
            'Routine de soins recommandée',
            'Que signifie cette détection ?',
            'Générer un rapport complet',
          ].map((suggestion) => (
            <Chip
              key={suggestion}
              label={suggestion}
              size="small"
              onClick={() => setInputText(suggestion)}
              sx={{
                cursor: 'pointer',
                fontSize: '0.75rem',
                bgcolor: '#FCE4EC',
                color: '#C2185B',
                '&:hover': {
                  bgcolor: 'primary.light',
                  color: 'white',
                },
              }}
            />
          ))}
        </Box>
      </Box>
      )}
    </Paper>
  );
};

export default ResultsChatAI;

