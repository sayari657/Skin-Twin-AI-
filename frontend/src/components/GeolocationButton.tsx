import React, { useState } from 'react';
import { Button, CircularProgress, Alert } from '@mui/material';
import { LocationOn, LocationOff } from '@mui/icons-material';

interface GeolocationButtonProps {
  onLocationDetected: (country: string, region: string) => void;
  disabled?: boolean;
  variant?: 'text' | 'outlined' | 'contained';
  size?: 'small' | 'medium' | 'large';
}

const GeolocationButton: React.FC<GeolocationButtonProps> = ({ 
  onLocationDetected, 
  disabled = false,
  variant = 'outlined',
  size = 'medium'
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getLocationFromCoordinates = async (lat: number, lng: number): Promise<{country: string, region: string}> => {
    try {
      // Try Google Maps Geocoding API first if available
      const googleApiKey = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;
      
      if (googleApiKey) {
        const response = await fetch(
          `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lng}&key=${googleApiKey}`
        );
        const data = await response.json();
        
        if (data.status === 'OK' && data.results.length > 0) {
          const result = data.results[0];
          let country = '';
          let region = '';
          
          for (const component of result.address_components) {
            if (component.types.includes('country')) {
              country = component.long_name;
            }
            if (component.types.includes('administrative_area_level_1')) {
              region = component.long_name;
            }
          }
          
          return { country, region };
        }
      }
      
      // Fallback to OpenStreetMap Nominatim
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1`
      );
      const data = await response.json();
      
      if (data && data.address) {
        return {
          country: data.address.country || '',
          region: data.address.state || data.address.region || ''
        };
      }
      
      throw new Error('Impossible de déterminer la localisation');
    } catch (error) {
      console.error('Erreur de géocodage:', error);
      throw new Error('Erreur lors de la récupération des informations de localisation');
    }
  };

  const handleGeolocation = async () => {
    if (!navigator.geolocation) {
      setError('La géolocalisation n\'est pas supportée par ce navigateur');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const position = await new Promise<GeolocationPosition>((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
          resolve,
          reject,
          {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 300000 // 5 minutes
          }
        );
      });

      const { latitude, longitude } = position.coords;
      const location = await getLocationFromCoordinates(latitude, longitude);
      
      onLocationDetected(location.country, location.region);
    } catch (error: any) {
      let errorMessage = 'Erreur lors de la détection de la position';
      
      if (error.code) {
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 'Permission de géolocalisation refusée. Veuillez autoriser l\'accès à votre position.';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = 'Position non disponible. Vérifiez votre connexion internet.';
            break;
          case error.TIMEOUT:
            errorMessage = 'Délai d\'attente dépassé. Veuillez réessayer.';
            break;
        }
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <Button
        variant={variant}
        size={size}
        startIcon={isLoading ? <CircularProgress size={20} /> : <LocationOn />}
        onClick={handleGeolocation}
        disabled={disabled || isLoading}
        sx={{ 
          mb: 2,
          borderColor: '#1976d2',
          color: '#1976d2',
          '&:hover': {
            borderColor: '#1565c0',
            backgroundColor: 'rgba(25, 118, 210, 0.04)'
          }
        }}
      >
        {isLoading ? 'Détection en cours...' : 'Détecter ma position'}
      </Button>
      
      {error && (
        <Alert 
          severity="error" 
          sx={{ mb: 2 }}
          onClose={() => setError(null)}
        >
          {error}
        </Alert>
      )}
    </div>
  );
};

export default GeolocationButton;