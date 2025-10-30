// Configuration pour la géolocalisation
export const GEOLOCATION_CONFIG = {
  // Clé API Google Maps (optionnel - le composant fonctionne aussi sans)
  GOOGLE_MAPS_API_KEY: process.env.REACT_APP_GOOGLE_MAPS_API_KEY || '',
  
  // Options de géolocalisation
  GEOLOCATION_OPTIONS: {
    enableHighAccuracy: true,
    timeout: 10000,
    maximumAge: 300000, // 5 minutes
  },
  
  // URLs des services de géocodage
  GOOGLE_GEOCODING_URL: 'https://maps.googleapis.com/maps/api/geocode/json',
  NOMINATIM_URL: 'https://nominatim.openstreetmap.org/reverse',
};

// Fonction pour obtenir la clé API Google Maps
export const getGoogleMapsApiKey = (): string => {
  return GEOLOCATION_CONFIG.GOOGLE_MAPS_API_KEY;
};

// Fonction pour vérifier si Google Maps est disponible
export const isGoogleMapsAvailable = (): boolean => {
  return !!GEOLOCATION_CONFIG.GOOGLE_MAPS_API_KEY;
};






