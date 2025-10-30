import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
  Alert,
  LinearProgress,
  Divider,
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  Save as SaveIcon,
  Lock as LockIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { apiService } from '../services/api';
import { User } from '../types';
import GeolocationButton from '../components/GeolocationButton';

const ProfilePage: React.FC = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      console.log('ProfilePage - Chargement du profil...');
      
      // Utiliser l'API service pour récupérer les vraies données utilisateur
      const response = await apiService.getProfile();
      console.log('ProfilePage - Données utilisateur récupérées:', response.data);
      
      setUser(response.data);
      setSuccess('Profil chargé avec succès');
    } catch (error: any) {
      console.error('ProfilePage - Erreur lors du chargement du profil:', error);
      setError('Erreur lors du chargement du profil. Veuillez vous reconnecter.');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!user) return;

    try {
      setSaving(true);
      setError(null);
      console.log('ProfilePage - Sauvegarde du profil:', user);
      
      // Utiliser l'API service pour sauvegarder les données
      const response = await apiService.updateProfile(user);
      console.log('ProfilePage - Profil sauvegardé:', response.data);
      
      setUser(response.data);
      setSuccess('Profil mis à jour avec succès !');
    } catch (err: any) {
      console.error('ProfilePage - Erreur lors de la sauvegarde:', err);
      setError('Erreur lors de la mise à jour du profil');
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (field: keyof User, value: any) => {
    if (user) {
      setUser({ ...user, [field]: value });
    }
  };

  const handleLocationDetected = (country: string, region: string) => {
    if (user) {
      setUser(prev => prev ? {
        ...prev,
        location_country: country,
        location_region: region
      } : null);
    }
  };

  const handleDeleteAccount = async () => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer votre compte ? Cette action est irréversible.')) {
      try {
        await apiService.deleteAccount();
        navigate('/');
      } catch (err: any) {
        setError('Erreur lors de la suppression du compte');
      }
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Chargement du profil...
        </Typography>
      </Container>
    );
  }

  if (!user) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error">
          Erreur lors du chargement du profil
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Button
          startIcon={<BackIcon />}
          onClick={() => navigate('/dashboard')}
          sx={{ mb: 2 }}
        >
          Retour
        </Button>
        <Typography variant="h4" gutterBottom>
          👤 Mon Profil
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Gérez vos informations personnelles et vos préférences
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 3 }}>
          {success}
        </Alert>
      )}

      {/* Layout horizontal avec 3 colonnes principales */}
      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', lg: 'repeat(3, 1fr)' }, gap: 3 }}>
        
        {/* Colonne 1: Informations de base */}
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ color: 'primary.main', fontWeight: 'bold' }}>
              👤 Informations de base
            </Typography>
            
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  fullWidth
                  label="Prénom"
                  value={user.first_name || ''}
                  onChange={(e) => handleChange('first_name', e.target.value)}
                  size="small"
                />
                <TextField
                  fullWidth
                  label="Nom"
                  value={user.last_name || ''}
                  onChange={(e) => handleChange('last_name', e.target.value)}
                  size="small"
                />
              </Box>
              
              <TextField
                fullWidth
                label="Email"
                type="email"
                value={user.email}
                onChange={(e) => handleChange('email', e.target.value)}
                size="small"
              />
              
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  fullWidth
                  label="Âge"
                  type="number"
                  value={user.age || ''}
                  onChange={(e) => handleChange('age', parseInt(e.target.value) || undefined)}
                  size="small"
                />
                <FormControl fullWidth size="small">
                  <InputLabel>Sexe</InputLabel>
                  <Select
                    value={user.gender || ''}
                    onChange={(e) => handleChange('gender', e.target.value)}
                  >
                    <MenuItem value="M">Homme</MenuItem>
                    <MenuItem value="F">Femme</MenuItem>
                    <MenuItem value="O">Autre</MenuItem>
                  </Select>
                </FormControl>
              </Box>
            </Box>
          </CardContent>
        </Card>

        {/* Colonne 2: Profil dermatologique */}
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ color: 'secondary.main', fontWeight: 'bold' }}>
              🧴 Profil dermatologique
            </Typography>
            
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <FormControl fullWidth size="small">
                <InputLabel>Type de peau</InputLabel>
                <Select
                  value={user.skin_type || ''}
                  onChange={(e) => handleChange('skin_type', e.target.value)}
                >
                  <MenuItem value="DRY">Sèche</MenuItem>
                  <MenuItem value="OILY">Grasse</MenuItem>
                  <MenuItem value="COMBINATION">Mixte</MenuItem>
                  <MenuItem value="NORMAL">Normale</MenuItem>
                  <MenuItem value="SENSITIVE">Sensible</MenuItem>
                  <MenuItem value="MATURE">Mature</MenuItem>
                </Select>
              </FormControl>
              
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  fullWidth
                  label="Pays"
                  value={user.location_country || ''}
                  onChange={(e) => handleChange('location_country', e.target.value)}
                  size="small"
                />
                <TextField
                  fullWidth
                  label="Région"
                  value={user.location_region || ''}
                  onChange={(e) => handleChange('location_region', e.target.value)}
                  size="small"
                />
              </Box>
              
              <GeolocationButton 
                onLocationDetected={handleLocationDetected}
                size="small"
                variant="outlined"
              />
            </Box>
          </CardContent>
        </Card>

        {/* Colonne 3: Habitudes de vie */}
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ color: 'success.main', fontWeight: 'bold' }}>
              🌞 Habitudes de vie
            </Typography>
            
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <FormControl fullWidth size="small">
                <InputLabel>Exposition au soleil</InputLabel>
                <Select
                  value={user.sun_exposure || ''}
                  onChange={(e) => handleChange('sun_exposure', e.target.value)}
                >
                  <MenuItem value="LOW">Faible</MenuItem>
                  <MenuItem value="MODERATE">Modérée</MenuItem>
                  <MenuItem value="HIGH">Élevée</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth size="small">
                <InputLabel>Usage crème solaire</InputLabel>
                <Select
                  value={user.sunscreen_usage || ''}
                  onChange={(e) => handleChange('sunscreen_usage', e.target.value)}
                >
                  <MenuItem value="NEVER">Jamais</MenuItem>
                  <MenuItem value="SOMETIMES">Parfois</MenuItem>
                  <MenuItem value="DAILY">Quotidiennement</MenuItem>
                </Select>
              </FormControl>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={user.smoking || false}
                      onChange={(e) => handleChange('smoking', e.target.checked)}
                      size="small"
                    />
                  }
                  label="Fumeur"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={user.alcohol || false}
                      onChange={(e) => handleChange('alcohol', e.target.checked)}
                      size="small"
                    />
                  }
                  label="Consommation d'alcool"
                />
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Box>

      {/* Section Antécédents médicaux - Pleine largeur */}
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ color: 'warning.main', fontWeight: 'bold' }}>
            🏥 Antécédents médicaux
          </Typography>
          
          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(2, 1fr)', md: 'repeat(3, 1fr)' }, gap: 2 }}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={user.diabetes || false}
                  onChange={(e) => handleChange('diabetes', e.target.checked)}
                />
              }
              label="Diabète"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={user.hypertension || false}
                  onChange={(e) => handleChange('hypertension', e.target.checked)}
                />
              }
              label="Hypertension"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={user.blood_disorders || false}
                  onChange={(e) => handleChange('blood_disorders', e.target.checked)}
                />
              }
              label="Troubles sanguins"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={user.autoimmune_diseases || false}
                  onChange={(e) => handleChange('autoimmune_diseases', e.target.checked)}
                />
              }
              label="Maladies auto-immunes"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={user.pregnancy || false}
                  onChange={(e) => handleChange('pregnancy', e.target.checked)}
                />
              }
              label="Grossesse/Allaitement"
            />
          </Box>
        </CardContent>
      </Card>

      {/* Actions */}
      <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'space-between', flexWrap: 'wrap' }}>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            startIcon={<SaveIcon />}
            onClick={handleSave}
            disabled={saving}
            sx={{ minWidth: 150 }}
          >
            {saving ? 'Sauvegarde...' : 'Sauvegarder'}
          </Button>
        </Box>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<LockIcon />}
            onClick={() => navigate('/change-password')}
            color="primary"
          >
            Changer le mot de passe
          </Button>
          <Button
            variant="outlined"
            startIcon={<DeleteIcon />}
            onClick={handleDeleteAccount}
            color="error"
          >
            Supprimer le compte
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default ProfilePage;
