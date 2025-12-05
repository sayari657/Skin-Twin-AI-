import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Button,
  Alert,
  LinearProgress,
  Card,
  CardContent,
  Chip,
} from '@mui/material';
import { ArrowBack as BackIcon } from '@mui/icons-material';
import { apiService } from '../services/api';
import { SkinAnalysis } from '../types';
import { RecommendationsSection } from '../med';
import { RecommendationCategory } from '../med/types/diagnostic.types';

const RecommendationsPage: React.FC = () => {
  const { analysisId } = useParams<{ analysisId: string }>();
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState<SkinAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<RecommendationCategory[]>([]);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);

  const getSkinTypeLabel = (skinType?: string) => {
    const labels: { [key: string]: string } = {
      'DRY': 'Sèche',
      'OILY': 'Grasse',
      'COMBINATION': 'Mixte',
      'NORMAL': 'Normale',
      'SENSITIVE': 'Sensible',
    };
    return labels[skinType || ''] || 'Non déterminé';
  };

  const getSkinTypeColor = (skinType?: string) => {
    const colors: { [key: string]: string } = {
      'DRY': 'error',
      'OILY': 'warning',
      'COMBINATION': 'info',
      'NORMAL': 'success',
      'SENSITIVE': 'secondary',
    };
    return colors[skinType || ''] || 'default';
  };

  // Charger l'analyse
  useEffect(() => {
    const loadAnalysis = async () => {
      if (!analysisId) return;
      
      try {
        setLoading(true);
        const response = await apiService.getSkinAnalysis(parseInt(analysisId));
        setAnalysis(response.data);
      } catch (err: any) {
        setError('Erreur lors du chargement de l\'analyse');
      } finally {
        setLoading(false);
      }
    };

    loadAnalysis();
  }, [analysisId]);

  // Charger les recommandations
  useEffect(() => {
    const loadRecommendations = async () => {
      if (!analysisId) return;

      setLoadingRecommendations(true);
      try {
        const recResponse = await apiService.getRecommendations(parseInt(analysisId));
        if (recResponse.data && Array.isArray(recResponse.data) && recResponse.data.length > 0) {
          // Transformer les recommandations au format attendu
          type ProductItem = {
            nom: string;
            description_detaillee: string;
            links?: Array<{ title: string; link: string; snippet: string }>;
          };
          const categories: { [key: string]: { [productKey: string]: ProductItem } } = {};

          // Première passe : collecter tous les produits et leurs liens
          recResponse.data.forEach((rec: any) => {
            const product = rec.product || rec;
            const category = product.category || 'Autres';
            const categoryLabel = category === 'CLEANSER' ? 'Nettoyant visage' :
                                 category === 'MOISTURIZER' ? 'Hydratant' :
                                 category === 'SERUM' ? 'Sérum' :
                                 category === 'SUNSCREEN' ? 'Protection solaire' :
                                 category === 'TREATMENT' ? 'Traitement' :
                                 category === 'MASK' ? 'Masque' :
                                 category === 'TONER' ? 'Tonique' :
                                 category === 'EXFOLIANT' ? 'Exfoliant' : 'Autres';

            if (!categories[categoryLabel]) {
              categories[categoryLabel] = {};
            }

            // Créer une clé unique basée sur le nom du produit (normalisé)
            const normalizeProductName = (name: string): string => {
              return name
                .trim()
                .toLowerCase()
                .replace(/\s+/g, ' ')
                .replace(/[^\w\s]/g, '')
                .trim();
            };
            const productName = normalizeProductName(product.name || product.brand || 'Produit');
            const productKey = productName;

            // Si le produit existe déjà, ajouter le lien à la liste existante
            if (categories[categoryLabel][productKey]) {
              const existingProduct = categories[categoryLabel][productKey];
              // Utiliser le champ 'sources' du backend qui contient tous les liens
              const sources = product.sources || [];
              if (product.url && product.source_site) {
                const mainLinkExists = sources.some((s: any) => s.url === product.url);
                if (!mainLinkExists) {
                  sources.push({
                    url: product.url,
                    source_site: product.source_site,
                    price: product.price,
                    description: product.description || product.name || ''
                  });
                }
              }

              const allLinks = sources.map((source: any) => ({
                title: `Acheter sur ${source.source_site}`,
                link: source.url,
                snippet: source.description || product.description || product.name || '',
              }));

              const uniqueLinks = allLinks.filter((link: any, index: number, self: any[]) =>
                index === self.findIndex((l: any) => l.link === link.link)
              );

              existingProduct.links = uniqueLinks.length > 0 ? uniqueLinks : existingProduct.links;
            } else {
              // Créer un nouveau produit
              const sources = product.sources || [];
              if (product.url && product.source_site) {
                const mainLinkExists = sources.some((s: any) => s.url === product.url);
                if (!mainLinkExists) {
                  sources.push({
                    url: product.url,
                    source_site: product.source_site,
                    price: product.price,
                    description: product.description || product.name || ''
                  });
                }
              }

              const links = sources.map((source: any) => ({
                title: `Acheter sur ${source.source_site}`,
                link: source.url,
                snippet: source.description || product.description || product.name || '',
              }));

              categories[categoryLabel][productKey] = {
                nom: product.name || product.brand || 'Produit',
                description_detaillee: product.description || 'Produit recommandé pour votre type de peau',
                links: links.length > 0 ? links : undefined,
              };
            }
          });

          // Convertir les objets en tableaux et trier les liens par site
          const formattedRecommendations = Object.keys(categories).map(cat => ({
            categorie: cat,
            produits: Object.values(categories[cat]).map(product => ({
              ...product,
              links: product.links?.sort((a, b) => a.title.localeCompare(b.title)),
            })),
          }));

          setRecommendations(formattedRecommendations);
        }
      } catch (recError) {
        console.error('Erreur lors du chargement des recommandations:', recError);
        setError('Erreur lors du chargement des recommandations');
      } finally {
        setLoadingRecommendations(false);
      }
    };

    if (analysisId) {
      loadRecommendations();
    }
  }, [analysisId]);

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Chargement des recommandations...
        </Typography>
      </Container>
    );
  }

  if (error || !analysis) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error" sx={{ mb: 3 }}>
          {error || 'Analyse non trouvée'}
        </Alert>
        <Button
          variant="contained"
          startIcon={<BackIcon />}
          onClick={() => navigate('/dashboard')}
        >
          Retour au tableau de bord
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Button
          startIcon={<BackIcon />}
          onClick={() => navigate(`/results/${analysisId}`)}
          sx={{ mb: 2 }}
        >
          Retour aux résultats
        </Button>
        <Typography variant="h4" gutterBottom>
          🛍️ Recommandations personnalisées
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Produits recommandés pour votre analyse du {new Date(analysis.analysis_date).toLocaleDateString('fr-FR')}
        </Typography>
      </Box>

      {/* Résumé de l'analyse */}
      {analysis && (
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              🩺 Diagnostic dermatologique
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mt: 2 }}>
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Type de peau
                </Typography>
                <Chip
                  label={getSkinTypeLabel(analysis.skin_type_prediction)}
                  color={getSkinTypeColor(analysis.skin_type_prediction) as any}
                  sx={{ mt: 0.5 }}
                />
                {analysis.skin_type_confidence && (
                  <Typography variant="caption" color="text.secondary" sx={{ ml: 1 }}>
                    Confiance: {(analysis.skin_type_confidence * 100).toFixed(1)}%
                  </Typography>
                )}
              </Box>
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Problèmes détectés
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 0.5 }}>
                  {analysis.acne_detected && <Chip label="Acné" size="small" color="error" />}
                  {analysis.wrinkles_detected && <Chip label="Rides" size="small" color="warning" />}
                  {analysis.dark_spots_detected && <Chip label="Taches" size="small" color="info" />}
                  {analysis.redness_detected && <Chip label="Rougeurs" size="small" color="error" />}
                  {!analysis.acne_detected && !analysis.wrinkles_detected &&
                   !analysis.dark_spots_detected && !analysis.redness_detected && (
                    <Chip label="Aucun problème majeur" size="small" color="success" />
                  )}
                </Box>
              </Box>
            </Box>
            <Box sx={{ mt: 2 }}>
              <Button
                variant="outlined"
                size="small"
                onClick={() => navigate(`/results/${analysisId}`)}
              >
                Voir le rapport complet
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}

      {/* Message de chargement */}
      {loadingRecommendations && (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
            <LinearProgress sx={{ width: '100%', maxWidth: 400 }} />
            <Typography variant="body2" color="text.secondary">
              Chargement des recommandations...
            </Typography>
          </Box>
        </Box>
      )}

      {/* Recommandations */}
      {recommendations && recommendations.length > 0 ? (
        <RecommendationsSection recommendations={recommendations} />
      ) : !loadingRecommendations ? (
        <Alert severity="info" sx={{ mt: 2 }}>
          Aucune recommandation disponible pour le moment. Les recommandations seront générées prochainement.
        </Alert>
      ) : null}
    </Container>
  );
};

export default RecommendationsPage;
