import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  Paper,
  Chip,
} from '@mui/material';
import {
  CameraAlt as CameraIcon,
  Videocam as VideoIcon,
  ArrowDownward as ArrowDownIcon,
} from '@mui/icons-material';
import UserTestimonials from '../components/UserTestimonials';

const Home: React.FC = () => {
  return (
    <Box sx={{ bgcolor: '#F5F5F0', minHeight: '100vh' }}>
      {/* Hero Section - SKIN-TWIN Branding */}
      <Container maxWidth="lg" sx={{ py: { xs: 6, md: 10 }, textAlign: 'center' }}>
        <Box sx={{ mb: 4 }}>
          <Typography 
            variant="h1" 
            component="h1" 
            gutterBottom 
            sx={{ 
              fontWeight: 700,
              fontSize: { xs: '2.5rem', md: '4rem' },
              mb: 2,
              letterSpacing: '-0.03em',
            }}
          >
            <Box
              component="span"
              sx={{
                color: '#D4A574', // Beige
                fontWeight: 400,
              }}
            >
              SKIN-
            </Box>
            <Box
              component="span"
              sx={{
                color: '#C2185B', // Dark Pink
                fontWeight: 700,
              }}
            >
              TWIN
            </Box>
          </Typography>
          <Typography 
            variant="h2" 
            component="h2"
            sx={{ 
              fontWeight: 600,
              fontSize: { xs: '1.5rem', md: '2rem' },
              color: '#212121',
              mb: 3,
            }}
          >
            Diagnostic Intelligent de la Peau par IA
          </Typography>
        </Box>
        <Typography 
          variant="body1" 
          sx={{ 
            maxWidth: 800,
            mx: 'auto',
            fontSize: { xs: '1rem', md: '1.2rem' },
            color: '#424242',
            lineHeight: 1.8,
            mb: 6,
          }}
        >
          Découvrez votre jumeau de peau grâce à notre technologie d'intelligence artificielle avancée. 
          Analysez votre peau en profondeur, identifiez les problèmes cutanés et recevez des recommandations personnalisées pour une routine de soins adaptée.
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap', mb: 8 }}>
          <Button
            component={RouterLink}
            to="/upload"
            variant="contained"
            size="large"
            startIcon={<CameraIcon />}
            sx={{
              bgcolor: '#C2185B',
              color: 'white',
              px: 4,
              py: 1.5,
              fontSize: '1.1rem',
              fontWeight: 600,
              textTransform: 'none',
              borderRadius: 3,
              boxShadow: '0 4px 12px rgba(194,24,91,0.3)',
              '&:hover': {
                bgcolor: '#880E4F',
                boxShadow: '0 6px 16px rgba(194,24,91,0.4)',
                transform: 'translateY(-2px)',
              },
              transition: 'all 0.3s ease',
            }}
          >
            Analyser ma Peau
          </Button>
          <Button
            component={RouterLink}
            to="/register"
            variant="outlined"
            size="large"
            sx={{
              borderColor: '#C2185B',
              borderWidth: 2,
              color: '#C2185B',
              px: 4,
              py: 1.5,
              fontSize: '1.1rem',
              fontWeight: 600,
              textTransform: 'none',
              borderRadius: 3,
              bgcolor: 'white',
              '&:hover': {
                borderColor: '#880E4F',
                bgcolor: '#FFF5F8',
                transform: 'translateY(-2px)',
              },
              transition: 'all 0.3s ease',
            }}
          >
            Créer un Compte
          </Button>
        </Box>
      </Container>

      {/* Main Analysis Section */}
      <Container maxWidth="lg" sx={{ py: 6, mb: 8 }}>
        <Box sx={{ 
          bgcolor: 'white', 
          borderRadius: 4, 
          p: { xs: 3, md: 6 },
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
        }}>
          <Typography 
            variant="h3" 
            component="h2"
            textAlign="center"
            sx={{ 
              fontWeight: 700,
              fontSize: { xs: '1.75rem', md: '2.5rem' },
              color: '#212121',
              mb: 1,
            }}
          >
            Comment ça fonctionne ?
          </Typography>
          <Typography 
            variant="body1" 
            textAlign="center"
            sx={{ 
              color: '#757575',
              fontSize: '1.1rem',
              mb: 6,
              maxWidth: 600,
              mx: 'auto',
            }}
          >
            Trois étapes simples pour obtenir votre analyse de peau personnalisée
          </Typography>

          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' }, gap: 4, mb: 6 }}>
            {[
              {
                step: '1',
                title: 'Téléchargez votre photo',
                description: 'Prenez une photo de votre visage ou utilisez votre caméra pour une analyse en direct',
                icon: <CameraIcon sx={{ fontSize: 48, color: '#C2185B' }} />,
              },
              {
                step: '2',
                title: 'Analyse par IA',
                description: 'Notre intelligence artificielle analyse votre peau et détecte les problèmes cutanés',
                icon: <VideoIcon sx={{ fontSize: 48, color: '#D4A574' }} />,
              },
              {
                step: '3',
                title: 'Résultats personnalisés',
                description: 'Recevez un rapport détaillé avec des recommandations adaptées à votre type de peau',
                icon: <ArrowDownIcon sx={{ fontSize: 48, color: '#C2185B' }} />,
              },
            ].map((item, index) => (
              <Card 
                key={index}
                sx={{ 
                  p: 3,
                  borderRadius: 3,
                  textAlign: 'center',
                  border: '1px solid rgba(194,24,91,0.1)',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    boxShadow: '0 8px 24px rgba(194,24,91,0.15)',
                    transform: 'translateY(-4px)',
                  },
                }}
              >
                <Box sx={{ mb: 2 }}>
                  {item.icon}
                </Box>
                <Chip 
                  label={item.step} 
                  sx={{ 
                    bgcolor: '#C2185B', 
                    color: 'white',
                    fontWeight: 700,
                    mb: 2,
                  }} 
                />
                <Typography 
                  variant="h6" 
                  sx={{ 
                    fontWeight: 600,
                    color: '#212121',
                    mb: 1.5,
                  }}
                >
                  {item.title}
                </Typography>
                <Typography 
                  variant="body2" 
                  color="text.secondary"
                  sx={{ lineHeight: 1.6 }}
                >
                  {item.description}
                </Typography>
              </Card>
            ))}
          </Box>

          <Box sx={{ textAlign: 'center' }}>
            <Button
              component={RouterLink}
              to="/upload"
              variant="contained"
              size="large"
              startIcon={<CameraIcon />}
              sx={{
                bgcolor: '#C2185B',
                color: 'white',
                px: 6,
                py: 2,
                fontSize: '1.1rem',
                fontWeight: 600,
                textTransform: 'none',
                borderRadius: 3,
                boxShadow: '0 4px 12px rgba(194,24,91,0.3)',
                '&:hover': {
                  bgcolor: '#880E4F',
                  boxShadow: '0 6px 16px rgba(194,24,91,0.4)',
                },
              }}
            >
              Commencer l'Analyse
            </Button>
          </Box>
        </Box>
      </Container>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography 
          variant="h2" 
          component="h2" 
          textAlign="center" 
          gutterBottom 
          sx={{ 
            mb: 2,
            fontWeight: 700,
            fontSize: { xs: '2rem', md: '2.5rem' },
            color: '#212121',
          }}
        >
          Pourquoi choisir SKIN-TWIN ?
        </Typography>
        <Typography 
          variant="body1" 
          textAlign="center"
          sx={{ 
            color: '#757575',
            fontSize: '1.1rem',
            mb: 6,
            maxWidth: 700,
            mx: 'auto',
          }}
        >
          Une technologie de pointe pour une analyse complète et précise de votre peau
        </Typography>
        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(2, 1fr)', md: 'repeat(4, 1fr)' }, gap: 4 }}>
          {[
            {
              title: 'Détection Avancée',
              description: 'Identification précise de multiples problèmes cutanés grâce à notre IA avancée.',
            },
            {
              title: 'Analyse Précise',
              description: 'Technologie HD pour une analyse détaillée zone par zone de votre peau.',
            },
            {
              title: 'Recommandations Personnalisées',
              description: 'Routine de soins adaptée à votre type de peau et vos besoins spécifiques.',
            },
            {
              title: 'Rapports Détaillés',
              description: 'Rapports complets avec visualisation des zones détectées et conseils personnalisés.',
            },
          ].map((feature, index) => (
            <Box key={index}>
              <Card 
                sx={{ 
                  height: '100%',
                  p: 3,
                  borderRadius: 3,
                  bgcolor: 'white',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
                  border: '1px solid rgba(194,24,91,0.1)',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    boxShadow: '0 8px 24px rgba(194,24,91,0.15)',
                    transform: 'translateY(-4px)',
                    borderColor: '#C2185B',
                  },
                }}
              >
                <CardContent sx={{ p: 0 }}>
                  <Typography 
                    variant="h6" 
                    component="h3" 
                    gutterBottom
                    sx={{ 
                      fontWeight: 600,
                      color: '#212121',
                      mb: 2,
                    }}
                  >
                    {feature.title}
                  </Typography>
                  <Typography 
                    variant="body2" 
                    color="text.secondary"
                    sx={{ lineHeight: 1.6 }}
                  >
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Box>
          ))}
        </Box>
      </Container>

      {/* Testimonials Section */}
      <UserTestimonials />

      {/* Bottom CTA Section */}
      <Box sx={{ bgcolor: 'white', py: 10, mt: 8, borderTop: '1px solid rgba(0,0,0,0.05)' }}>
        <Container maxWidth="lg">
          <Box 
            sx={{ 
              textAlign: 'center',
              maxWidth: 800,
              mx: 'auto',
            }}
          >
            <Typography 
              variant="h3" 
              component="h2"
              sx={{ 
                fontWeight: 700,
                fontSize: { xs: '1.75rem', md: '2.5rem' },
                color: '#212121',
                mb: 3,
              }}
            >
              Prêt à découvrir votre jumeau de peau ?
            </Typography>
            <Typography 
              variant="body1" 
              sx={{ 
                fontSize: '1.1rem',
                color: '#424242',
                mb: 4,
                lineHeight: 1.8,
              }}
            >
              Rejoignez SKIN-TWIN aujourd'hui et obtenez une analyse complète de votre peau avec des recommandations personnalisées pour une routine de soins adaptée.
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
              <Button
                component={RouterLink}
                to="/register"
                variant="contained"
                size="large"
                sx={{
                  bgcolor: '#C2185B',
                  color: 'white',
                  px: 6,
                  py: 2,
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  textTransform: 'none',
                  borderRadius: 3,
                  boxShadow: '0 4px 12px rgba(194,24,91,0.3)',
                  '&:hover': {
                    bgcolor: '#880E4F',
                    boxShadow: '0 6px 16px rgba(194,24,91,0.4)',
                  },
                }}
              >
                Commencer Maintenant
              </Button>
              <Button
                component={RouterLink}
                to="/upload"
                variant="outlined"
                size="large"
                sx={{
                  borderColor: '#C2185B',
                  borderWidth: 2,
                  color: '#C2185B',
                  px: 6,
                  py: 2,
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  textTransform: 'none',
                  borderRadius: 3,
                  bgcolor: 'white',
                  '&:hover': {
                    borderColor: '#880E4F',
                    bgcolor: '#FFF5F8',
                  },
                }}
              >
                Essayer Gratuitement
              </Button>
            </Box>
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

export default Home;
