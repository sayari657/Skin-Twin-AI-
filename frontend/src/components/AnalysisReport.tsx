import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Typography,
  IconButton,
  CircularProgress,
  Tooltip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  Paper,
} from '@mui/material';
import {
  Description as ReportIcon,
  Download as DownloadIcon,
  Fullscreen as FullscreenIcon,
  PictureAsPdf as PdfIcon,
} from '@mui/icons-material';
import { chatService } from '../services/chatService';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { SkinAnalysis } from '../types';

interface AnalysisReportProps {
  analysis: SkinAnalysis;
}

const AnalysisReport: React.FC<AnalysisReportProps> = ({ analysis }) => {
  const [reportContent, setReportContent] = useState<string>('');
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const [reportFullscreenOpen, setReportFullscreenOpen] = useState(false);
  const [downloadMenuAnchor, setDownloadMenuAnchor] = useState<null | HTMLElement>(null);
  
  const reportRef = useRef<HTMLDivElement>(null);
  const reportFullscreenRef = useRef<HTMLDivElement>(null);

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

  const handleGenerateReport = async () => {
    setIsGeneratingReport(true);

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

  // Générer automatiquement le rapport au chargement du composant
  useEffect(() => {
    if (analysis && !reportContent && !isGeneratingReport) {
      handleGenerateReport();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [analysis?.id]);

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

  const handleDownloadPDF = async () => {
    if (!reportContent) return;
    
    const element = reportFullscreenRef.current || reportRef.current;
    if (!element) {
      console.error('Élément du rapport non trouvé');
      handleDownloadText();
      return;
    }
    
    try {
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
    } catch (error) {
      console.error('Erreur lors de la génération du PDF:', error);
      handleDownloadText();
    }
  };

  const handleOpenFullscreen = () => {
    setReportFullscreenOpen(true);
    setDownloadMenuAnchor(null);
  };

  return (
    <>
      <Paper 
        sx={{ 
          width: '100%', 
          mt: 2, 
          p: 2, 
          bgcolor: 'info.50', 
          borderRadius: 2, 
          boxShadow: '0 0 12px rgba(0,0,0,0.1)' 
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Typography variant="h6" sx={{ fontSize: '1.1rem', fontWeight: 'bold', color: 'primary.dark' }}>
            📄 Rapport d'Analyse
          </Typography>
          <Box sx={{ display: 'flex', gap: 1 }}>
            {reportContent && (
              <>
                <Tooltip title="Télécharger">
                  <IconButton
                    size="small"
                    onClick={(e) => setDownloadMenuAnchor(e.currentTarget)}
                    sx={{ color: 'primary.main' }}
                  >
                    <DownloadIcon />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Voir en plein écran">
                  <IconButton
                    size="small"
                    onClick={handleOpenFullscreen}
                    sx={{ color: 'primary.main' }}
                  >
                    <FullscreenIcon />
                  </IconButton>
                </Tooltip>
              </>
            )}
          </Box>
        </Box>

        {isGeneratingReport ? (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, py: 2 }}>
            <CircularProgress size={20} />
            <Typography variant="body2">Génération du rapport...</Typography>
          </Box>
        ) : reportContent ? (
          <Box
            ref={reportRef}
            sx={{
              p: 2,
              bgcolor: 'white',
              borderRadius: 1,
              border: '1px solid',
              borderColor: 'divider',
              mt: 1,
            }}
          >
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{reportContent}</ReactMarkdown>
          </Box>
        ) : null}
      </Paper>

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
            <Tooltip title="Fermer">
              <IconButton
                size="small"
                onClick={() => setReportFullscreenOpen(false)}
              >
                <FullscreenIcon />
              </IconButton>
            </Tooltip>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Box
            ref={reportFullscreenRef}
            sx={{
              p: 2,
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
    </>
  );
};

export default AnalysisReport;

