import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Button,
  Card,
  CardContent,
  CardMedia,
  Paper,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  CameraAlt as CameraIcon,
  Psychology as AIIcon,
  ShoppingCart as ProductIcon,
  History as HistoryIcon,
  CheckCircle as CheckIcon,
  Star as StarIcon,
  MedicalServices as MedicalIcon,
  Science as ScienceIcon,
  HealthAndSafety as HealthIcon,
  Biotech as BiotechIcon,
} from '@mui/icons-material';
import UserTestimonials from '../components/UserTestimonials';

const Home: React.FC = () => {
  const features = [
    {
      icon: <MedicalIcon sx={{ fontSize: 48, color: 'primary.main' }} />,
      title: 'Diagnostic Dermatologique IA',
      description: 'Technologie médicale avancée utilisant des modèles CNN et YOLOv8 pour l\'analyse précise de l\'état de votre peau.',
    },
    {
      icon: <ScienceIcon sx={{ fontSize: 48, color: 'secondary.main' }} />,
      title: 'Simulation Thérapeutique',
      description: 'Visualisation scientifique des améliorations potentielles grâce à des simulations GAN médicalement validées.',
    },
    {
      icon: <HealthIcon sx={{ fontSize: 48, color: 'success.main' }} />,
      title: 'Recommandations Cliniques',
      description: 'Prescriptions personnalisées de soins dermatologiques basées sur des données médicales et scientifiques.',
    },
    {
      icon: <BiotechIcon sx={{ fontSize: 48, color: 'info.main' }} />,
      title: 'Suivi Médical Longitudinal',
      description: 'Monitoring professionnel de l\'évolution de votre peau avec des rapports détaillés pour votre dermatologue.',
    },
  ];

  const benefits = [
    'Diagnostic dermatologique précis avec intelligence artificielle',
    'Simulation thérapeutique validée médicalement',
    'Recommandations cliniques personnalisées',
    'Suivi médical longitudinal professionnel',
    'Interface médicale sécurisée et conforme RGPD',
    'Données médicales protégées et confidentielles',
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #87CEEB 0%, #4682B4 100%)',
          color: 'white',
          py: 12,
          textAlign: 'center',
        }}
      >
        <Container maxWidth="lg">
          <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
            🏥 Skin Twin AI
          </Typography>
          <Typography variant="h4" gutterBottom sx={{ mb: 4, opacity: 0.95, fontWeight: 500 }}>
            Plateforme Médicale d'Analyse Dermatologique par IA
          </Typography>
          <Typography variant="h6" sx={{ mb: 6, maxWidth: 700, mx: 'auto', opacity: 0.9, lineHeight: 1.6 }}>
            Solution professionnelle d'analyse dermatologique utilisant l'intelligence artificielle 
            pour le diagnostic, le suivi et les recommandations thérapeutiques personnalisées.
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button
              component={RouterLink}
              to="/register"
              variant="contained"
              size="large"
              sx={{ 
                bgcolor: 'white', 
                color: 'primary.main',
                '&:hover': { bgcolor: 'grey.100' },
                px: 4,
                py: 1.5,
              }}
            >
              Commencer Gratuitement
            </Button>
            <Button
              component={RouterLink}
              to="/login"
              variant="outlined"
              size="large"
              sx={{ 
                borderColor: 'white', 
                color: 'white',
                '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' },
                px: 4,
                py: 1.5,
              }}
            >
              Se Connecter
            </Button>
          </Box>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography variant="h3" component="h2" textAlign="center" gutterBottom sx={{ mb: 6 }}>
          Fonctionnalités Principales
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
          {features.map((feature, index) => (
            <Box sx={{ flex: { xs: '1 1 100%', md: '1 1 calc(50% - 16px)' }, minWidth: 0 }} key={index}>
              <Card sx={{ height: '100%', p: 2 }}>
                <CardContent>
                  <Box sx={{ textAlign: 'center', mb: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h5" component="h3" gutterBottom textAlign="center">
                    {feature.title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary" textAlign="center">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Box>
          ))}
        </Box>
      </Container>

      {/* Benefits Section */}
      <Box sx={{ bgcolor: 'grey.50', py: 8 }}>
        <Container maxWidth="lg">
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 6, alignItems: 'center' }}>
            <Box sx={{ flex: { xs: '1', md: '1' } }}>
              <Typography variant="h3" component="h2" gutterBottom>
                Excellence Médicale et Technologique
              </Typography>
              <Typography variant="h6" color="text.secondary" paragraph>
                Notre plateforme médicale intègre les dernières innovations en intelligence artificielle 
                avec une expertise dermatologique certifiée pour un diagnostic professionnel et précis.
              </Typography>
              <List>
                {benefits.map((benefit, index) => (
                  <ListItem key={index} sx={{ px: 0 }}>
                    <ListItemIcon>
                      <CheckIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText primary={benefit} />
                  </ListItem>
                ))}
              </List>
            </Box>
            <Box sx={{ flex: { xs: '1', md: '1' } }}>
              <Paper
                sx={{
                  p: 6,
                  textAlign: 'center',
                  background: 'linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%)',
                  color: 'white',
                  borderRadius: 3,
                }}
              >
                <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
                  🏥 Accès Professionnel
                </Typography>
                <Typography variant="h6" paragraph sx={{ mb: 4, opacity: 0.9 }}>
                  Rejoignez la communauté médicale qui utilise Skin Twin AI pour des diagnostics dermatologiques précis
                </Typography>
                <Button
                  component={RouterLink}
                  to="/register"
                  variant="contained"
                  size="large"
                  sx={{ 
                    bgcolor: 'white', 
                    color: 'primary.main',
                    '&:hover': { bgcolor: 'grey.100' },
                    px: 6,
                    py: 2,
                    fontSize: '1.1rem',
                    fontWeight: 600,
                  }}
                >
                  Accès Professionnel
                </Button>
              </Paper>
            </Box>
          </Box>
        </Container>
      </Box>

      {/* Testimonials Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography variant="h3" component="h2" textAlign="center" gutterBottom sx={{ mb: 6 }}>
          Témoignages Professionnels
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
          {[
            {
              name: 'Dr. Sarah Martin',
              role: 'Dermatologue',
              content: 'Skin Twin AI a transformé ma pratique clinique. Les analyses IA sont d\'une précision remarquable et complètent parfaitement mon diagnostic.',
              rating: 5,
            },
            {
              name: 'Dr. Marie Leblanc',
              role: 'Dermatologue Esthétique',
              content: 'La simulation thérapeutique permet à mes patients de visualiser les résultats potentiels. Un outil professionnel exceptionnel.',
              rating: 5,
            },
            {
              name: 'Dr. Emma Kowalski',
              role: 'Dermatologue Pédiatrique',
              content: 'Interface médicale intuitive et résultats cliniques fiables. Je recommande cette plateforme à mes confrères.',
              rating: 5,
            },
          ].map((testimonial, index) => (
            <Box sx={{ flex: { xs: '1 1 100%', md: '1 1 calc(33.333% - 16px)' }, minWidth: 0 }} key={index}>
              <Card sx={{ height: '100%', p: 3 }}>
                <CardContent>
                  <Box sx={{ display: 'flex', mb: 2 }}>
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <StarIcon key={i} color="primary" />
                    ))}
                  </Box>
                  <Typography variant="body1" paragraph sx={{ fontStyle: 'italic' }}>
                    "{testimonial.content}"
                  </Typography>
                  <Typography variant="h6" component="h4">
                    {testimonial.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {testimonial.role}
                  </Typography>
                </CardContent>
              </Card>
            </Box>
          ))}
        </Box>
      </Container>

      {/* Section Témoignages Utilisateurs */}
      <UserTestimonials />

      {/* CTA Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          py: 8,
          textAlign: 'center',
        }}
      >
        <Container maxWidth="md">
          <Typography variant="h3" component="h2" gutterBottom>
            Prêt à Transformer Votre Peau ?
          </Typography>
          <Typography variant="h6" paragraph sx={{ mb: 4 }}>
            Rejoignez Skin Twin AI dès aujourd'hui et découvrez le pouvoir de l'IA pour vos soins de la peau.
          </Typography>
          <Button
            component={RouterLink}
            to="/register"
            variant="contained"
            size="large"
            sx={{ 
              bgcolor: 'white', 
              color: 'primary.main',
              '&:hover': { bgcolor: 'grey.100' },
              px: 6,
              py: 2,
              fontSize: '1.1rem',
            }}
          >
            Commencer Maintenant
          </Button>
        </Container>
      </Box>
    </Box>
  );
};

export default Home;




