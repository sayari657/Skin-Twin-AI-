import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  Web as WebIcon,
  ShoppingCart as CartIcon,
  TrendingUp as TrendingIcon,
} from '@mui/icons-material';

interface ScrapingStatsProps {
  totalProducts: number;
  scrapedProducts: number;
  databaseProducts: number;
  scrapingInProgress: boolean;
  useScrapedProducts: boolean;
}

const ScrapingStats: React.FC<ScrapingStatsProps> = ({
  totalProducts,
  scrapedProducts,
  databaseProducts,
  scrapingInProgress,
  useScrapedProducts,
}) => {
  const scrapedPercentage = totalProducts > 0 ? (scrapedProducts / totalProducts) * 100 : 0;
  const databasePercentage = totalProducts > 0 ? (databaseProducts / totalProducts) * 100 : 0;

  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <WebIcon color="primary" />
          Statistiques de Scraping
        </Typography>

        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
          {/* Produits scrapés */}
          <Box sx={{ flex: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2" color="text.secondary">
                Produits Web
              </Typography>
              <Chip
                label={`${scrapedProducts} produits`}
                color="primary"
                size="small"
              />
            </Box>
            <LinearProgress
              variant="determinate"
              value={scrapedPercentage}
              sx={{ mb: 1, height: 8, borderRadius: 4 }}
            />
            <Typography variant="caption" color="text.secondary">
              {scrapedPercentage.toFixed(1)}% du total
            </Typography>
          </Box>

          {/* Produits base de données */}
          <Box sx={{ flex: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2" color="text.secondary">
                Base de Données
              </Typography>
              <Chip
                label={`${databaseProducts} produits`}
                color="secondary"
                size="small"
              />
            </Box>
            <LinearProgress
              variant="determinate"
              value={databasePercentage}
              color="secondary"
              sx={{ mb: 1, height: 8, borderRadius: 4 }}
            />
            <Typography variant="caption" color="text.secondary">
              {databasePercentage.toFixed(1)}% du total
            </Typography>
          </Box>
        </Box>

        {/* Indicateurs de statut */}
        <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {scrapingInProgress && (
            <Chip
              icon={<WebIcon />}
              label="Web en cours..."
              color="warning"
              variant="outlined"
            />
          )}
          
          {useScrapedProducts ? (
            <Chip
              icon={<WebIcon />}
              label="Mode Web Actif"
              color="primary"
              variant="filled"
            />
          ) : (
            <Chip
              icon={<CartIcon />}
              label="Mode Base de Données"
              color="secondary"
              variant="filled"
            />
          )}

          {totalProducts > 0 && (
            <Chip
              icon={<TrendingIcon />}
              label={`${totalProducts} produits au total`}
              color="success"
              variant="outlined"
            />
          )}
        </Box>

        {/* Informations sur les sources */}
        <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Sources de données:
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            <Chip label="Pharmacie.com" size="small" variant="outlined" />
            <Chip label="Sephora.fr" size="small" variant="outlined" />
            <Chip label="Nocibé.fr" size="small" variant="outlined" />
            <Chip label="Marionnaud.fr" size="small" variant="outlined" />
            <Chip label="Douglas.fr" size="small" variant="outlined" />
            <Chip label="Lookfantastic.fr" size="small" variant="outlined" />
            <Chip label="Feelunique.com" size="small" variant="outlined" />
            <Chip label="Notino.fr" size="small" variant="outlined" />
            <Chip label="Base de données locale" size="small" variant="outlined" />
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ScrapingStats;
