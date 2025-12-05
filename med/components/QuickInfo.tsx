// Composant pour afficher les infos rapides (Type de peau, Confiance, Troubles détectés)

import React from 'react';
import { Box, Card, CardContent, Typography, Chip, Grid } from '@mui/material';
import { QuickInfo as QuickInfoType } from '../types/diagnostic.types';

interface QuickInfoProps {
  data: QuickInfoType;
}

const QuickInfo: React.FC<QuickInfoProps> = ({ data }) => {
  const { skinType, confidence, detectedTroubles } = data;

  const getSkinTypeColor = (type: string) => {
    switch (type) {
      case 'Dry':
        return '#FFB74D'; // Orange
      case 'Normal':
        return '#66BB6A'; // Vert
      case 'Oily':
        return '#42A5F5'; // Bleu
      default:
        return '#9E9E9E'; // Gris
    }
  };

  const getSeverityColor = (severity?: string) => {
    switch (severity) {
      case 'HIGH':
        return '#F44336'; // Rouge
      case 'MODERATE':
        return '#FF9800'; // Orange
      case 'LOW':
        return '#4CAF50'; // Vert
      default:
        return '#FFD700'; // Or
    }
  };

  return (
    <Card sx={{ mb: 3, backgroundColor: '#f5f5f5' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ mb: 2, fontWeight: 'bold' }}>
          💧 Infos rapides
        </Typography>

        <Grid container spacing={2}>
          {/* Type de peau */}
          <Grid item xs={12} sm={6}>
            <Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Type de peau
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Chip
                  label={skinType.type}
                  sx={{
                    backgroundColor: getSkinTypeColor(skinType.type),
                    color: 'white',
                    fontWeight: 'bold',
                    fontSize: '0.9rem',
                  }}
                />
              </Box>
            </Box>
          </Grid>

          {/* Confiance */}
          <Grid item xs={12} sm={6}>
            <Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Confiance
              </Typography>
              <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#1976d2' }}>
                {(confidence * 100).toFixed(1)}%
              </Typography>
            </Box>
          </Grid>

          {/* Troubles détectés */}
          <Grid item xs={12}>
            <Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                ⚡ Troubles détectés :
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
                {detectedTroubles.length > 0 ? (
                  detectedTroubles.map((trouble, index) => (
                    <Chip
                      key={index}
                      label={trouble.name}
                      sx={{
                        backgroundColor: getSeverityColor(trouble.severity),
                        color: 'white',
                        fontWeight: 'medium',
                        fontSize: '0.85rem',
                      }}
                    />
                  ))
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    Aucun trouble significatif détecté
                  </Typography>
                )}
              </Box>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default QuickInfo;

