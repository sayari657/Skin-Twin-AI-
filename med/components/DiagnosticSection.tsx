// Composant pour afficher le diagnostic dermatologique

import React from 'react';
import { Box, Card, CardContent, Typography, Divider, List, ListItem, ListItemText } from '@mui/material';
import { DiagnosticData } from '../types/diagnostic.types';

interface DiagnosticSectionProps {
  data: DiagnosticData;
}

const DiagnosticSection: React.FC<DiagnosticSectionProps> = ({ data }) => {
  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', mb: 2 }}>
          🩺 Diagnostic dermatologique
        </Typography>

        <Divider sx={{ mb: 2 }} />

        {/* Texte du diagnostic */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="body1" sx={{ lineHeight: 1.8, textAlign: 'justify' }}>
            {data.diagnostic}
          </Typography>
        </Box>

        {/* Type de peau */}
        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
            Type de peau :
          </Typography>
          <Typography variant="body1" color="primary">
            {data.skinType}
          </Typography>
        </Box>

        {/* Problèmes détectés */}
        <Box>
          <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
            Problèmes détectés :
          </Typography>
          {data.problems && data.problems.length > 0 ? (
            <List dense>
              {data.problems.map((problem, index) => (
                <ListItem key={index} sx={{ pl: 0 }}>
                  <ListItemText
                    primary={problem}
                    primaryTypographyProps={{
                      variant: 'body2',
                    }}
                  />
                </ListItem>
              ))}
            </List>
          ) : (
            <Typography variant="body2" color="text.secondary">
              Aucun problème détecté
            </Typography>
          )}
        </Box>
      </CardContent>
    </Card>
  );
};

export default DiagnosticSection;

