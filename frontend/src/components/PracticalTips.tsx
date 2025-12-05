import React from 'react';
import { Box, Typography } from '@mui/material';
import { SkinAnalysis } from '../types';

interface PracticalTipsProps {
  analysis: SkinAnalysis;
}

const PracticalTips: React.FC<PracticalTipsProps> = ({ analysis }) => {
  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        💡 Conseils pratiques
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Conseils pratiques basés sur votre analyse de peau.
      </Typography>
    </Box>
  );
};

export default PracticalTips;

