import React, { useState } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Link,
  Alert,
  Container,
  Card,
  CardContent,
} from '@mui/material';
import {
  InputAdornment,
  IconButton,
} from '@mui/material';
import {
  Person as PersonIcon,
  Email as EmailIcon,
  Lock as LockIcon,
  Visibility,
  VisibilityOff,
} from '@mui/icons-material';
import { apiService } from '../services/api';
import { LoginRequest } from '../types';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<LoginRequest>({
    email: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await apiService.login(formData.email, formData.password);
      const { user, tokens } = response.data;

      // Sauvegarder les tokens immédiatement
      apiService.setAuthTokens(tokens);
      
      // Vérifier que les tokens sont bien sauvegardés
      console.log('Tokens sauvegardés:', {
        access: localStorage.getItem('access_token'),
        refresh: localStorage.getItem('refresh_token')
      });
      
      // Attendre un peu pour s'assurer que les tokens sont bien sauvegardés
      setTimeout(() => {
        // Vérifier l'authentification avec la méthode plus douce
        const isAuth = apiService.hasValidTokens();
        console.log('Utilisateur authentifié:', isAuth);

        if (isAuth) {
          // Rediriger si authentifié
          console.log('Redirection vers dashboard...');
          navigate('/dashboard', { replace: true });
        } else {
          console.error('Échec de l\'authentification après connexion');
          setError('Erreur d\'authentification');
        }
      }, 100);
    } catch (err: any) {
      console.error('Erreur de connexion:', err);
      setError(err.response?.data?.error || 'Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        }}
      >
        <Card sx={{ width: '100%', maxWidth: 400 }}>
          <CardContent sx={{ p: 4 }}>
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Typography variant="h4" gutterBottom sx={{ color: 'primary.main' }}>
                🌟 Skin Twin AI
              </Typography>
              <Typography variant="h6" color="text.secondary">
                Connectez-vous à votre compte
              </Typography>
            </Box>

            {error && (
              <Alert severity="error" sx={{ mb: 3 }}>
                {error}
              </Alert>
            )}

            <Box component="form" onSubmit={handleSubmit}>
              <TextField
                fullWidth
                label="Email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                required
                margin="normal"
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <EmailIcon color="action" />
                    </InputAdornment>
                  ),
                }}
              />

              <TextField
                fullWidth
                label="Mot de passe"
                name="password"
                type={showPassword ? 'text' : 'password'}
                value={formData.password}
                onChange={handleChange}
                required
                margin="normal"
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <LockIcon color="action" />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowPassword(!showPassword)}
                        edge="end"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />

              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={loading}
                sx={{ mt: 3, mb: 2, py: 1.5 }}
              >
                {loading ? 'Connexion...' : 'Se connecter'}
              </Button>

              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="body2" color="text.secondary">
                  Pas encore de compte ?{' '}
                  <Link component={RouterLink} to="/register" underline="hover">
                    Créer un compte
                  </Link>
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default Login;




