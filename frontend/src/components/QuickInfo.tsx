import React from 'react';
import { Box, Typography, Chip } from '@mui/material';
import { SkinAnalysis } from '../types';

interface QuickInfoProps {
  analysis: SkinAnalysis;
}

const QuickInfo: React.FC<QuickInfoProps> = ({ analysis }) => {
  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        💧 Infos rapides
      </Typography>
      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        {analysis.skin_type_prediction && (
          <Chip 
            label={`Type: ${analysis.skin_type_prediction}`} 
            color="primary" 
            variant="outlined" 
          />
        )}
        {analysis.skin_type_confidence && (
          <Chip 
            label={`Confiance: ${(analysis.skin_type_confidence * 100).toFixed(1)}%`} 
            color="secondary" 
            variant="outlined" 
          />
        )}
      </Box>
    </Box>
  );
};

export default QuickInfo;

