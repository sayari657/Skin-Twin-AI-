import React, { useEffect, useState } from 'react';
import { Box, Alert, CircularProgress, Typography, Chip } from '@mui/material';
import { checkApiHealth, HealthCheckResult } from '../utils/apiHealthCheck';

const ApiHealthMonitor: React.FC = () => {
  const [results, setResults] = useState<HealthCheckResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [visible, setVisible] = useState(true); // 👈 contrôle d'affichage
  const [showCompletionMessage, setShowCompletionMessage] = useState(false); // 👈 contrôle du message de fin

  useEffect(() => {
    const checkHealth = async () => {
      setLoading(true);
      const healthResults = await checkApiHealth();
      setResults(healthResults);
      setLoading(false);
    };

    // Vérification initiale
    checkHealth();

    // Vérification toutes les 30 secondes
    const interval = setInterval(checkHealth, 30000);

    // 👇 Masquer le composant après 5 secondes
    const timeout = setTimeout(() => {
      setVisible(false);
      setShowCompletionMessage(true);
    }, 5000);

    return () => {
      clearInterval(interval);
      clearTimeout(timeout);
    };
  }, []);

  // 👇 Gérer la disparition du message de fin après 5 secondes
  useEffect(() => {
    if (showCompletionMessage) {
      const completionTimeout = setTimeout(() => {
        setShowCompletionMessage(false);
      }, 5000);

      return () => {
        clearTimeout(completionTimeout);
      };
    }
  }, [showCompletionMessage]);

  // Si le message de fin est affiché
  if (showCompletionMessage) {
    return (
      <Box sx={{ p: 2 }}>
        <Alert severity="info">
          ⏳ Vérification terminée — le module d'état des APIs est maintenant caché.
        </Alert>
      </Box>
    );
  }

  // Si plus visible et le message de fin n'est plus affiché, ne rien retourner
  if (!visible) {
    return null;
  }

  if (loading) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, p: 2 }}>
        <CircularProgress size={20} />
        <Typography variant="body2">Vérification des APIs...</Typography>
      </Box>
    );
  }

  const allOk = results.every(r => r.status === 'ok');
  const hasErrors = results.some(r => r.status === 'error');

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        🔍 État des APIs Backend
      </Typography>
      
      {allOk ? (
        <Alert severity="success" sx={{ mb: 2 }}>
          ✅ Toutes les APIs sont accessibles
        </Alert>
      ) : hasErrors ? (
        <Alert severity="error" sx={{ mb: 2 }}>
          ❌ Certaines APIs ne sont pas accessibles
        </Alert>
      ) : (
        <Alert severity="warning" sx={{ mb: 2 }}>
          ⚠️ Certaines APIs nécessitent une attention
        </Alert>
      )}

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
        {results.map((result, index) => (
          <Box
            key={index}
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              p: 1,
              bgcolor:
                result.status === 'ok'
                  ? 'success.light'
                  : result.status === 'error'
                  ? 'error.light'
                  : 'warning.light',
              borderRadius: 1,
            }}
          >
            <Chip
              label={
                result.status === 'ok'
                  ? 'OK'
                  : result.status === 'error'
                  ? 'ERREUR'
                  : 'ATTENTION'
              }
              color={
                result.status === 'ok'
                  ? 'success'
                  : result.status === 'error'
                  ? 'error'
                  : 'warning'
              }
              size="small"
            />
            <Typography variant="body2">{result.endpoint}</Typography>
            {result.statusCode && (
              <Typography variant="caption" color="text.secondary">
                ({result.statusCode})
              </Typography>
            )}
          </Box>
        ))}
      </Box>
    </Box>
  );
};

export default ApiHealthMonitor;
