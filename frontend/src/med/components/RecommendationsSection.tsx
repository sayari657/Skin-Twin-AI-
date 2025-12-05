// Composant pour afficher les recommandations personnalisées de produits

import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Divider,
  Paper,
  Link,
  Chip,
} from '@mui/material';
import { RecommendationCategory } from '../types/diagnostic.types';

interface RecommendationsSectionProps {
  recommendations: RecommendationCategory[];
}

const RecommendationsSection: React.FC<RecommendationsSectionProps> = ({ recommendations }) => {
  if (!recommendations || recommendations.length === 0) {
    return (
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
            🛍️ Recommandations personnalisées
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Aucune recommandation disponible pour le moment.
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', mb: 2 }}>
          🛍️ Recommandations personnalisées
        </Typography>

        <Divider sx={{ mb: 3 }} />

        {recommendations.map((category, categoryIndex) => (
          <Box key={categoryIndex} sx={{ mb: 4 }}>
            {/* Titre de la catégorie */}
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', mb: 2, color: '#1976d2' }}>
              🧴 {category.categorie}
            </Typography>

            {/* Grille de produits */}
            <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' }, gap: 3 }}>
              {category.produits.map((produit, produitIndex) => (
                <Paper
                  key={produitIndex}
                  elevation={2}
                  sx={{
                    p: 2,
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    transition: 'transform 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: 4,
                    },
                  }}
                >
                  {/* Nom du produit */}
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', mb: 1 }}>
                    🧴 {produit.nom}
                  </Typography>

                  {/* Description */}
                  <Typography
                    variant="body2"
                    sx={{
                      mb: 2,
                      flexGrow: 1,
                      lineHeight: 1.6,
                      color: 'text.secondary',
                    }}
                  >
                    {produit.description_detaillee}
                  </Typography>

                  {/* Liens d'achat */}
                  {produit.links && produit.links.length > 0 && (
                    <Box sx={{ mt: 'auto' }}>
                      <Typography variant="caption" color="text.secondary" gutterBottom>
                        Où acheter :
                      </Typography>
                      {produit.links.map((link, linkIndex) => (
                        <Box key={linkIndex} sx={{ mb: 1 }}>
                          {link.link ? (
                            <Link
                              href={link.link}
                              target="_blank"
                              rel="noopener noreferrer"
                              sx={{
                                display: 'block',
                                textDecoration: 'none',
                                '&:hover': {
                                  textDecoration: 'underline',
                                },
                              }}
                            >
                              <Chip
                                label={`🔗 ${link.title}`}
                                size="small"
                                clickable
                                sx={{
                                  mb: 0.5,
                                  maxWidth: '100%',
                                  '& .MuiChip-label': {
                                    overflow: 'hidden',
                                    textOverflow: 'ellipsis',
                                  },
                                }}
                              />
                              {link.snippet && (
                                <Typography
                                  variant="caption"
                                  color="text.secondary"
                                  sx={{
                                    display: 'block',
                                    mt: 0.5,
                                    fontSize: '0.7rem',
                                  }}
                                >
                                  {link.snippet.substring(0, 100)}...
                                </Typography>
                              )}
                            </Link>
                          ) : (
                            <Typography variant="caption" color="text.secondary">
                              {link.title}
                            </Typography>
                          )}
                        </Box>
                      ))}
                    </Box>
                  )}
                </Paper>
              ))}
            </Box>

            {categoryIndex < recommendations.length - 1 && (
              <Divider sx={{ mt: 4, mb: 2 }} />
            )}
          </Box>
        ))}
      </CardContent>
    </Card>
  );
};

export default RecommendationsSection;

