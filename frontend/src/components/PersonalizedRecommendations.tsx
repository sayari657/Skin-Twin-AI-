import React from 'react';
import { Box, Typography, Alert } from '@mui/material';
import { SkinAnalysis } from '../types';

interface PersonalizedRecommendationsProps {
  analysis: SkinAnalysis;
}

const PersonalizedRecommendations: React.FC<PersonalizedRecommendationsProps> = ({ analysis }) => {
  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        🛍️ Recommandations personnalisées
      </Typography>
      <Alert severity="info">
        Les recommandations seront générées automatiquement après l'analyse.
      </Alert>
    </Box>
  );
};

export default PersonalizedRecommendations;

