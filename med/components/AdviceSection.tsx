// Composant pour afficher les conseils pratiques

import React from 'react';
import { Box, Card, CardContent, Typography, Divider, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

interface AdviceSectionProps {
  conseils: string | string[];
}

const AdviceSection: React.FC<AdviceSectionProps> = ({ conseils }) => {
  // Normaliser les conseils en tableau
  const conseilsList = Array.isArray(conseils) ? conseils : [conseils];

  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', mb: 2 }}>
          💡 Conseils pratiques
        </Typography>

        <Divider sx={{ mb: 2 }} />

        <List>
          {conseilsList.map((conseil, index) => (
            <ListItem key={index} sx={{ pl: 0, py: 1 }}>
              <ListItemIcon sx={{ minWidth: 40 }}>
                <CheckCircleIcon color="success" />
              </ListItemIcon>
              <ListItemText
                primary={conseil}
                primaryTypographyProps={{
                  variant: 'body1',
                  sx: { lineHeight: 1.6 },
                }}
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default AdviceSection;

