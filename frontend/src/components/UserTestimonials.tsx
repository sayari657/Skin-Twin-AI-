import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Avatar,
  Rating,
  CircularProgress,
  Alert,
  Chip,
} from '@mui/material';
import {
  Star as StarIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import { apiService } from '../services/api';
import axios from 'axios';

interface Testimonial {
  id: number;
  user_username: string;
  user_first_name: string;
  user_last_name: string;
  rating: number;
  comment: string;
  created_at: string;
}

const UserTestimonials: React.FC = () => {
  const [testimonials, setTestimonials] = useState<Testimonial[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTestimonials();
  }, []);

  const loadTestimonials = async () => {
    try {
      setLoading(true);
      // Appel direct sans headers d'authentification
      const response = await axios.get(
        (process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api') + '/users/testimonials/public/'
      );
      setTestimonials(response.data.testimonials || []);
    } catch (error) {
      console.error('Erreur lors du chargement des témoignages:', error);
      setError('Impossible de charger les témoignages');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getInitials = (firstName: string, lastName: string) => {
    return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase();
  };

  if (loading) {
    return (
      <Box sx={{ py: 8, textAlign: 'center' }}>
        <CircularProgress />
        <Typography variant="body1" sx={{ mt: 2 }}>
          Chargement des témoignages...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ py: 8 }}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  if (testimonials.length === 0) {
    return (
      <Box sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h6" color="text.secondary">
          Aucun témoignage disponible pour le moment
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ py: 8, bgcolor: 'grey.50' }}>
      <Container maxWidth="lg">
        <Box sx={{ textAlign: 'center', mb: 6 }}>
          <Typography variant="h3" component="h2" gutterBottom>
            💬 Témoignages Utilisateurs
          </Typography>
          <Typography variant="h6" color="text.secondary" paragraph>
            Découvrez ce que nos utilisateurs pensent de Skin Twin AI
          </Typography>
        </Box>

        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: { 
            xs: '1fr', 
            md: 'repeat(2, 1fr)', 
            lg: 'repeat(3, 1fr)' 
          }, 
          gap: 3 
        }}>
          {testimonials.slice(0, 6).map((testimonial) => (
            <Card 
              key={testimonial.id}
              sx={{ 
                height: '100%', 
                display: 'flex', 
                flexDirection: 'column',
                transition: 'transform 0.2s ease-in-out',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 3,
                }
              }}
            >
              <CardContent sx={{ flexGrow: 1, p: 3 }}>
                {/* En-tête avec avatar et nom */}
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar 
                    sx={{ 
                      bgcolor: 'primary.main', 
                      mr: 2,
                      width: 48,
                      height: 48,
                      fontSize: '1.2rem'
                    }}
                  >
                    {getInitials(testimonial.user_first_name, testimonial.user_last_name)}
                  </Avatar>
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography variant="h6" component="h3">
                      {testimonial.user_first_name} {testimonial.user_last_name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      @{testimonial.user_username}
                    </Typography>
                  </Box>
                </Box>

                {/* Note avec étoiles */}
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Rating 
                    value={testimonial.rating} 
                    readOnly 
                    size="small"
                    sx={{ mr: 1 }}
                  />
                  <Chip
                    label={`${testimonial.rating}/5`}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                </Box>

                {/* Commentaire */}
                {testimonial.comment && (
                  <Typography 
                    variant="body1" 
                    sx={{ 
                      mb: 2,
                      fontStyle: 'italic',
                      lineHeight: 1.6
                    }}
                  >
                    "{testimonial.comment}"
                  </Typography>
                )}

                {/* Date */}
                <Typography variant="caption" color="text.secondary">
                  {formatDate(testimonial.created_at)}
                </Typography>
              </CardContent>
            </Card>
          ))}
        </Box>

        {/* Statistiques */}
        {testimonials.length > 0 && (
          <Box sx={{ mt: 6, textAlign: 'center' }}>
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 4, flexWrap: 'wrap' }}>
              <Box>
                <Typography variant="h4" color="primary.main" fontWeight="bold">
                  {testimonials.length}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Témoignages
                </Typography>
              </Box>
              <Box>
                <Typography variant="h4" color="primary.main" fontWeight="bold">
                  {(testimonials.reduce((sum, t) => sum + t.rating, 0) / testimonials.length).toFixed(1)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Note moyenne
                </Typography>
              </Box>
              <Box>
                <Typography variant="h4" color="primary.main" fontWeight="bold">
                  {Math.round((testimonials.filter(t => t.rating >= 4).length / testimonials.length) * 100)}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Recommandent
                </Typography>
              </Box>
            </Box>
          </Box>
        )}
      </Container>
    </Box>
  );
};

export default UserTestimonials;
