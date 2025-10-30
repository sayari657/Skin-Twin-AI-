/**
 * API Health Check Utility
 * Vérifie que toutes les APIs backend sont accessibles
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';

export interface HealthCheckResult {
  endpoint: string;
  status: 'ok' | 'error' | 'warning';
  statusCode?: number;
  message: string;
}

export const checkApiHealth = async (): Promise<HealthCheckResult[]> => {
  const results: HealthCheckResult[] = [];
  
  const endpoints = [
    { name: 'Test Endpoint', url: '/users/test-no-auth/', method: 'GET' },
    { name: 'Public Testimonials', url: '/users/testimonials/public/', method: 'GET' },
    { name: 'Products', url: '/products/', method: 'GET' },
    { name: 'Chat Suggestions', url: '/chat-ai/suggestions/', method: 'GET' },
  ];

  for (const endpoint of endpoints) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint.url}`, {
        method: endpoint.method,
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok || response.status === 401 || response.status === 403) {
        results.push({
          endpoint: endpoint.name,
          status: 'ok',
          statusCode: response.status,
          message: `✅ ${endpoint.name} accessible (${response.status})`,
        });
      } else {
        results.push({
          endpoint: endpoint.name,
          status: 'warning',
          statusCode: response.status,
          message: `⚠️ ${endpoint.name} returned ${response.status}`,
        });
      }
    } catch (error: any) {
      results.push({
        endpoint: endpoint.name,
        status: 'error',
        message: `❌ ${endpoint.name} inaccessible: ${error.message}`,
      });
    }
  }

  return results;
};

export const logApiHealth = async () => {
  console.log('🔍 Vérification santé API...');
  const results = await checkApiHealth();
  
  results.forEach(result => {
    console.log(result.message);
  });
  
  const allOk = results.every(r => r.status === 'ok');
  if (allOk) {
    console.log('✅ Toutes les APIs sont accessibles');
  } else {
    console.warn('⚠️ Certaines APIs ne sont pas accessibles');
  }
  
  return results;
};

