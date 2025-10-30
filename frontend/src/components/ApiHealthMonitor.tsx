import React, { useEffect, useState } from 'react';
import { Box, Alert, CircularProgress, Typography, Chip } from '@mui/material';
import { checkApiHealth, HealthCheckResult } from '../utils/apiHealthCheck';

const ApiHealthMonitor: React.FC = () => {
  const [results, setResults] = useState<HealthCheckResult[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkHealth = async () => {
      setLoading(true);
      const healthResults = await checkApiHealth();
      setResults(healthResults);
      setLoading(false);
    };

    checkHealth();
    // Vérifier toutes les 30 secondes
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

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
              bgcolor: result.status === 'ok' ? 'success.light' : result.status === 'error' ? 'error.light' : 'warning.light',
              borderRadius: 1,
            }}
          >
            <Chip
              label={result.status === 'ok' ? 'OK' : result.status === 'error' ? 'ERREUR' : 'ATTENTION'}
              color={result.status === 'ok' ? 'success' : result.status === 'error' ? 'error' : 'warning'}
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

