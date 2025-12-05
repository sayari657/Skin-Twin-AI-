// Composant principal qui combine tous les composants de résultats

import React from 'react';
import { Box, Container, CircularProgress, Alert } from '@mui/material';
import { DiagnosisResult } from '../types/diagnostic.types';
import QuickInfo from './QuickInfo';
import DiagnosticSection from './DiagnosticSection';
import AdviceSection from './AdviceSection';
import RecommendationsSection from './RecommendationsSection';

interface DiagnosisResultsProps {
  data: DiagnosisResult | null;
  loading?: boolean;
  error?: string | null;
}

const DiagnosisResults: React.FC<DiagnosisResultsProps> = ({ data, loading, error }) => {
  if (loading) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
          <CircularProgress size={60} />
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg">
        <Alert severity="error" sx={{ mt: 3 }}>
          {error}
        </Alert>
      </Container>
    );
  }

  if (!data) {
    return (
      <Container maxWidth="lg">
        <Alert severity="info" sx={{ mt: 3 }}>
          Aucune donnée de diagnostic disponible.
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Infos rapides */}
      <QuickInfo data={data.quickInfo} />

      {/* Diagnostic */}
      <DiagnosticSection data={data.diagnostic} />

      {/* Conseils pratiques */}
      <AdviceSection conseils={data.conseils_pratiques} />

      {/* Recommandations */}
      <RecommendationsSection recommendations={data.recommendations} />
    </Container>
  );
};

export default DiagnosisResults;

