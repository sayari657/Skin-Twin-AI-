import React, { useState } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  Box,
  TextField,
  Button,
  Typography,
  Link,
  Alert,
  Container,
  Card,
  CardContent,
  Stepper,
  Step,
  StepLabel,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox,
  Chip,
  Slider,
  RadioGroup,
  Radio,
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
import { RegisterRequest } from '../types';
import GeolocationButton from './GeolocationButton';

const Signup: React.FC = () => {
  const navigate = useNavigate();
  const [activeStep, setActiveStep] = useState(0);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [formData, setFormData] = useState<RegisterRequest>({
    email: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: '',
    age: undefined,
    gender: undefined,
    location_country: '',
    location_region: '',
    skin_type: undefined,
    diabetes: false,
    hypertension: false,
    blood_disorders: false,
    autoimmune_diseases: false,
    pregnancy: false,
    sun_exposure: undefined,
    sunscreen_usage: undefined,
    diet: undefined,
    hydration: undefined,
    smoking: undefined,
    alcohol: undefined,
    sleep_hours: undefined,
    stress_level: undefined,
    diet_quality: undefined,
    alcohol_consumption: undefined,
    family_dermatological_history: false,
    current_treatments: '',
    current_cosmetics: '',
    known_allergies: '',
    skin_goals: [],
  });

  const steps = [
    'Informations de base',
    'Profil dermatologique',
    'Habitudes de vie',
    'Antécédents médicaux',
    'Objectifs personnels'
  ];

  const skinGoals: string[] = [
    'prevent_acne',
    'reduce_wrinkles',
    'improve_glow',
    'reduce_scars',
    'lighten_spots',
    'hydrate_skin',
    'reduce_redness'
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSelectChange = (name: string, value: any) => {
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleArrayChange = (name: string, value: string) => {
    const currentArray = formData[name as keyof RegisterRequest] as string[];
    const newArray = currentArray.includes(value)
      ? currentArray.filter(item => item !== value)
      : [...currentArray, value];
    
    setFormData({
      ...formData,
      [name]: newArray,
    });
  };

  const handleLocationDetected = (country: string, region: string) => {
    setFormData(prev => ({
      ...prev,
      location_country: country,
      location_region: region
    }));
  };

  const handleNext = () => {
    // Validation basique pour les champs obligatoires seulement
    if (activeStep === 0) {
      if (!formData.email || !formData.password || !formData.password_confirm) {
        setError('Veuillez remplir tous les champs obligatoires');
        return;
      }
      
      // Validation de la confirmation de mot de passe
      if (formData.password !== formData.password_confirm) {
        setError('Les mots de passe ne correspondent pas. Veuillez vérifier votre saisie.');
        return;
      }
      
      // Validation de la longueur du mot de passe
      if (formData.password.length < 8) {
        setError('Le mot de passe doit contenir au moins 8 caractères.');
        return;
      }
    }
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  // Fonction pour nettoyer les données avant l'envoi - version simplifiée
  const cleanFormData = (data: RegisterRequest) => {
    const cleaned: any = {};
    
    // Champs obligatoires
    cleaned.email = data.email;
    cleaned.password = data.password;
    cleaned.password_confirm = data.password_confirm;
    
    // Champs optionnels simples - seulement les champs non-undefined
    if (data.first_name && data.first_name.trim()) cleaned.first_name = data.first_name.trim();
    if (data.last_name && data.last_name.trim()) cleaned.last_name = data.last_name.trim();
    if (data.age !== undefined && data.age !== null && data.age > 0) {
      // Convertir l'âge en nombre si c'est une string
      cleaned.age = typeof data.age === 'string' ? parseInt(data.age, 10) : data.age;
    }
    if (data.gender !== undefined && data.gender !== null) cleaned.gender = data.gender;
    if (data.location_country && data.location_country.trim()) cleaned.location_country = data.location_country;
    if (data.location_region && data.location_region.trim()) cleaned.location_region = data.location_region;
    if (data.skin_type !== undefined && data.skin_type !== null) cleaned.skin_type = data.skin_type;
    
    // Champs booléens avec valeurs par défaut
    cleaned.diabetes = Boolean(data.diabetes);
    cleaned.hypertension = Boolean(data.hypertension);
    cleaned.blood_disorders = Boolean(data.blood_disorders);
    cleaned.autoimmune_diseases = Boolean(data.autoimmune_diseases);
    cleaned.pregnancy = Boolean(data.pregnancy);
    if (data.smoking !== undefined && data.smoking !== null) cleaned.smoking = Boolean(data.smoking);
    if (data.alcohol !== undefined && data.alcohol !== null) cleaned.alcohol = Boolean(data.alcohol);
    cleaned.family_dermatological_history = Boolean(data.family_dermatological_history);
    
    // Champs de style de vie - seulement si définis
    if (data.sun_exposure !== undefined && data.sun_exposure !== null) cleaned.sun_exposure = data.sun_exposure;
    if (data.sunscreen_usage !== undefined && data.sunscreen_usage !== null) cleaned.sunscreen_usage = data.sunscreen_usage;
    if (data.diet !== undefined && data.diet !== null) cleaned.diet = data.diet;
    if (data.hydration !== undefined && data.hydration !== null) cleaned.hydration = data.hydration;
    if (data.sleep_hours !== undefined && data.sleep_hours !== null) cleaned.sleep_hours = data.sleep_hours;
    if (data.stress_level !== undefined && data.stress_level !== null) cleaned.stress_level = data.stress_level;
    if (data.diet_quality !== undefined && data.diet_quality !== null) cleaned.diet_quality = data.diet_quality;
    if (data.alcohol_consumption !== undefined && data.alcohol_consumption !== null) cleaned.alcohol_consumption = data.alcohol_consumption;
    
    // Champs de texte - seulement si non vides
    if (data.current_treatments && data.current_treatments.trim()) cleaned.current_treatments = data.current_treatments;
    if (data.current_cosmetics && data.current_cosmetics.trim()) cleaned.current_cosmetics = data.current_cosmetics;
    if (data.known_allergies && data.known_allergies.trim()) cleaned.known_allergies = data.known_allergies;
    
    // Champs de listes - seulement si non vides
    if (data.skin_goals && Array.isArray(data.skin_goals) && data.skin_goals.length > 0) {
      cleaned.skin_goals = data.skin_goals;
    }
    
    return cleaned;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Validation finale côté frontend - seulement les champs essentiels
    if (!formData.email || !formData.password || !formData.password_confirm) {
      setError('Veuillez remplir tous les champs obligatoires');
      setLoading(false);
      return;
    }

    if (formData.password.length < 8) {
      setError('Le mot de passe doit contenir au moins 8 caractères');
      setLoading(false);
      return;
    }

    if (formData.password !== formData.password_confirm) {
      setError('Les mots de passe ne correspondent pas');
      setLoading(false);
      return;
    }

    try {
      const cleanedData = cleanFormData(formData);
      console.log('Données nettoyées envoyées:', cleanedData);
      
      const response = await apiService.register(cleanedData);
      const { user, tokens } = response.data;

      // Sauvegarder les tokens
      apiService.setAuthTokens(tokens);

      // Rediriger vers le dashboard
      navigate('/dashboard');
    } catch (err: any) {
      console.error('Erreur d\'inscription:', err);
      console.error('Détails de l\'erreur:', err.response?.data);
      
      // Gestion des erreurs spécifiques
      if (err.response?.data?.username) {
        setError('Ce nom d\'utilisateur est déjà utilisé. Veuillez en choisir un autre.');
      } else if (err.response?.data?.email) {
        setError('Cette adresse email est déjà utilisée. Veuillez en choisir une autre.');
      } else if (err.response?.data?.password) {
        setError('Erreur avec le mot de passe: ' + err.response.data.password[0]);
      } else {
        setError(err.response?.data?.error || err.response?.data?.message || 'Erreur lors de la création du compte');
      }
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              * Champs obligatoires - Les autres informations sont optionnelles
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
              <TextField
                fullWidth
                label="Prénom"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <PersonIcon color="action" />
                    </InputAdornment>
                  ),
                }}
              />
              <TextField
                fullWidth
                label="Nom de famille"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <PersonIcon color="action" />
                    </InputAdornment>
                  ),
                }}
              />
            </Box>
            <TextField
              fullWidth
              label="Email *"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              required
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <EmailIcon color="action" />
                  </InputAdornment>
                ),
              }}
            />
            <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
              <TextField
                fullWidth
                label="Mot de passe * (min 8 caractères)"
                name="password"
                type={showPassword ? 'text' : 'password'}
                value={formData.password}
                onChange={handleChange}
                required
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
              <TextField
                fullWidth
                label="Confirmer le mot de passe *"
                name="password_confirm"
                type="password"
                value={formData.password_confirm}
                onChange={handleChange}
                required
                error={formData.password_confirm !== '' && formData.password !== formData.password_confirm}
                helperText={
                  formData.password_confirm !== '' && formData.password !== formData.password_confirm
                    ? 'Les mots de passe ne correspondent pas'
                    : ''
                }
              />
            </Box>
            <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
              <TextField
                fullWidth
                label="Âge"
                name="age"
                type="number"
                value={formData.age || ''}
                onChange={handleChange}
              />
              <FormControl fullWidth>
                <InputLabel>Sexe</InputLabel>
                <Select
                  name="gender"
                  value={formData.gender || ''}
                  onChange={(e) => handleSelectChange('gender', e.target.value)}
                >
                  <MenuItem value="M">Homme</MenuItem>
                  <MenuItem value="F">Femme</MenuItem>
                  <MenuItem value="O">Autre</MenuItem>
                </Select>
              </FormControl>
            </Box>
          </Box>
        );

      case 1:
        return (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Informations optionnelles - Vous pouvez passer à l'étape suivante sans remplir ces champs
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
              <TextField
                fullWidth
                label="Pays"
                name="location_country"
                value={formData.location_country}
                onChange={handleChange}
              />
              <TextField
                fullWidth
                label="Région"
                name="location_region"
                value={formData.location_region}
                onChange={handleChange}
              />
            </Box>
            
            {/* Composant de géolocalisation */}
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
              <GeolocationButton
                onLocationDetected={handleLocationDetected}
                variant="outlined"
                size="medium"
              />
            </Box>
            <FormControl fullWidth>
              <InputLabel>Type de peau</InputLabel>
              <Select
                name="skin_type"
                value={formData.skin_type || ''}
                onChange={(e) => handleSelectChange('skin_type', e.target.value)}
              >
                <MenuItem value="DRY">Sèche</MenuItem>
                <MenuItem value="OILY">Grasse</MenuItem>
                <MenuItem value="COMBINATION">Mixte</MenuItem>
                <MenuItem value="NORMAL">Normale</MenuItem>
                <MenuItem value="SENSITIVE">Sensible</MenuItem>
                <MenuItem value="UNKNOWN">Je ne sais pas</MenuItem>
              </Select>
            </FormControl>
          </Box>
        );

      case 2:
        return (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
              <FormControl fullWidth>
                <InputLabel>Exposition au soleil</InputLabel>
                <Select
                  name="sun_exposure"
                  value={formData.sun_exposure || ''}
                  onChange={(e) => handleSelectChange('sun_exposure', e.target.value)}
                >
                  <MenuItem value="LOW">Faible</MenuItem>
                  <MenuItem value="MODERATE">Modérée</MenuItem>
                  <MenuItem value="HIGH">Élevée</MenuItem>
                </Select>
              </FormControl>
              <FormControl fullWidth>
                <InputLabel>Usage crème solaire</InputLabel>
                <Select
                  name="sunscreen_usage"
                  value={formData.sunscreen_usage || ''}
                  onChange={(e) => handleSelectChange('sunscreen_usage', e.target.value)}
                >
                  <MenuItem value="NEVER">Jamais</MenuItem>
                  <MenuItem value="SOMETIMES">Parfois</MenuItem>
                  <MenuItem value="DAILY">Quotidiennement</MenuItem>
                </Select>
              </FormControl>
            </Box>
            
            <FormControl fullWidth>
              <InputLabel>Fumeur</InputLabel>
              <Select
                name="smoking"
                value={formData.smoking === undefined ? '' : formData.smoking ? 'yes' : 'no'}
                onChange={(e) => handleSelectChange('smoking', e.target.value === 'yes')}
              >
                <MenuItem value="yes">Oui</MenuItem>
                <MenuItem value="no">Non</MenuItem>
              </Select>
            </FormControl>
            
            <Box>
              <Typography gutterBottom sx={{ mb: 2 }}>
                Niveau de stress (1-10)
              </Typography>
              <Slider
                value={formData.stress_level || 5}
                onChange={(e, value) => handleSelectChange('stress_level', value)}
                min={1}
                max={10}
                step={1}
                marks
                valueLabelDisplay="auto"
                sx={{ mt: 2 }}
              />
            </Box>
          </Box>
        );

      case 3:
        return (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ color: 'warning.main', fontWeight: 'bold' }}>
              🏥 Antécédents médicaux
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Ces informations nous aident à personnaliser vos recommandations
            </Typography>
            
            <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(2, 1fr)' }, gap: 2 }}>
              <FormControlLabel
                control={
                  <Checkbox
                    name="diabetes"
                    checked={formData.diabetes}
                    onChange={handleChange}
                  />
                }
                label="Diabète"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    name="hypertension"
                    checked={formData.hypertension}
                    onChange={handleChange}
                  />
                }
                label="Hypertension"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    name="blood_disorders"
                    checked={formData.blood_disorders}
                    onChange={handleChange}
                  />
                }
                label="Troubles sanguins"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    name="autoimmune_diseases"
                    checked={formData.autoimmune_diseases}
                    onChange={handleChange}
                  />
                }
                label="Maladies auto-immunes"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    name="pregnancy"
                    checked={formData.pregnancy}
                    onChange={handleChange}
                  />
                }
                label="Grossesse/Allaitement"
              />
            </Box>
          </Box>
        );

      case 4:
        return (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Objectifs personnels
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {skinGoals.map((goal) => (
                  <Chip
                    key={goal}
                    label={goal.replace('_', ' ')}
                    clickable
                    color={formData.skin_goals?.includes(goal) ? 'primary' : 'default'}
                    onClick={() => handleArrayChange('skin_goals', goal)}
                  />
                ))}
              </Box>
            </Box>
          </Box>
        );

      default:
        return null;
    }
  };

  return (
    <Container maxWidth="md">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          py: 4,
        }}
      >
        <Card sx={{ width: '100%', maxWidth: 600 }}>
          <CardContent sx={{ p: 4 }}>
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Typography variant="h4" gutterBottom sx={{ color: 'primary.main' }}>
                🌟 Skin Twin AI
              </Typography>
              <Typography variant="h6" color="text.secondary">
                Créer votre compte
              </Typography>
            </Box>

            <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
              {steps.map((label) => (
                <Step key={label}>
                  <StepLabel>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>

            {error && (
              <Alert severity="error" sx={{ mb: 3 }}>
                {error}
              </Alert>
            )}

            <Box component="form" onSubmit={handleSubmit}>
              {renderStepContent(activeStep)}

              <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
                <Button
                  disabled={activeStep === 0}
                  onClick={handleBack}
                >
                  Retour
                </Button>

                {activeStep === steps.length - 1 ? (
                  <Button
                    type="submit"
                    variant="contained"
                    disabled={loading}
                  >
                    {loading ? 'Création...' : 'Créer le compte'}
                  </Button>
                ) : (
                  <Button
                    variant="contained"
                    onClick={handleNext}
                  >
                    Suivant
                  </Button>
                )}
              </Box>

              <Box sx={{ textAlign: 'center', mt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Déjà un compte ?{' '}
                  <Link component={RouterLink} to="/login" underline="hover">
                    Se connecter
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

export default Signup;




