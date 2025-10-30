import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import { apiService } from '../services/api';
import { CircularProgress, Box } from '@mui/material';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuth = () => {
      // Utiliser la méthode plus douce pour vérifier l'authentification
      const authStatus = apiService.hasValidTokens();
      console.log('ProtectedRoute - Vérification authentification:', {
        isAuthenticated: authStatus,
        accessToken: localStorage.getItem('access_token'),
        refreshToken: localStorage.getItem('refresh_token')
      });
      
      setIsAuthenticated(authStatus);
      setIsLoading(false);
    };

    // Délai plus long pour s'assurer que les tokens sont bien sauvegardés
    const timer = setTimeout(checkAuth, 200);
    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!isAuthenticated) {
    console.log('ProtectedRoute - Redirection vers login');
    return <Navigate to="/login" replace />;
  }

  console.log('ProtectedRoute - Accès autorisé');
  return <>{children}</>;
};

export default ProtectedRoute;




