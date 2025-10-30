import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { AuthTokens, User, SkinAnalysis, Product, Recommendation, GANSimulation } from '../types';

class ApiService {
  private api: AxiosInstance;
  private baseURL: string;

  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';
    this.api = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Intercepteur pour ajouter le token d'authentification
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Intercepteur pour gérer les erreurs de réponse
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        // Éviter les boucles infinies pour les endpoints de refresh et login
        if (error.response?.status === 401 && 
            !originalRequest._retry && 
            !originalRequest.url?.includes('/token/refresh/') &&
            !originalRequest.url?.includes('/users/login/')) {
          originalRequest._retry = true;

          try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
              console.log('Tentative de rafraîchissement du token...');
              const response = await this.refreshToken(refreshToken);
              const { access } = response.data;
              localStorage.setItem('access_token', access);
              originalRequest.headers.Authorization = `Bearer ${access}`;
              console.log('Token rafraîchi avec succès');
              return this.api(originalRequest);
            } else {
              console.log('Pas de refresh token disponible');
            }
          } catch (refreshError) {
            console.error('Échec du rafraîchissement du token:', refreshError);
            // Ne pas déconnecter immédiatement, laisser l'utilisateur essayer de nouveau
            console.log('Token refresh failed, but not logging out immediately');
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // Méthodes d'authentification
  async login(email: string, password: string): Promise<AxiosResponse<{ user: User; tokens: AuthTokens }>> {
    console.log('API Service - Tentative de connexion:', { email, baseURL: this.baseURL });
    // Envoie le champ username attendu par le backend
    const response = await axios.post(`${this.baseURL}/users/login/`, { username: email, password }, {
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });
    console.log('API Service - Connexion réussie:', response.status);
    return response;
  }

  async register(userData: any): Promise<AxiosResponse<{ user: User; tokens: AuthTokens }>> {
    console.log('Données envoyées au backend:', userData);
    // Utiliser une requête directe sans intercepteur pour éviter l'ajout automatique du token
    const response = await axios.post(`${this.baseURL}/users/register/`, userData, {
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });
    return response;
  }

  async logout(): Promise<AxiosResponse<void>> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      try {
        await this.api.post('/users/logout/', { refresh: refreshToken });
      } catch (error) {
        console.error('Erreur lors de la déconnexion:', error);
      }
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    return Promise.resolve({} as AxiosResponse<void>);
  }

  async refreshToken(refreshToken: string): Promise<AxiosResponse<{ access: string }>> {
    // Utiliser une requête directe sans intercepteur pour éviter les boucles
    const response = await axios.post(`${this.baseURL}/token/refresh/`, { refresh: refreshToken }, {
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });
    return response;
  }

  async getProfile(): Promise<AxiosResponse<User>> {
    // Utiliser l'endpoint de profil simple qui ne nécessite pas d'authentification JWT
    const userId = this.getUserIdFromToken();
    if (!userId) {
      throw new Error('Utilisateur non authentifié');
    }
    return this.api.get(`/users/profile-simple/?user_id=${userId}`);
  }

  private getUserIdFromToken(): number | null {
    const token = localStorage.getItem('access_token');
    if (!token) {
      console.log('API Service - Pas de token d\'accès trouvé');
      return null;
    }
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      console.log('API Service - Token payload:', payload);
      // Le token JWT peut contenir user_id, user_id, ou id
      const userId = payload.user_id || payload.id || null;
      console.log('API Service - User ID extrait:', userId);
      return userId;
    } catch (error) {
      console.error('API Service - Erreur lors du décodage du token:', error);
      return null;
    }
  }

  async updateProfile(userData: Partial<User>): Promise<AxiosResponse<User>> {
    return this.api.patch('/users/profile/', userData);
  }

  async changePassword(oldPassword: string, newPassword: string): Promise<AxiosResponse<{ message: string }>> {
    return this.api.post('/users/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
      new_password_confirm: newPassword,
    });
  }

  // Méthodes pour l'analyse de peau
  async uploadSkinAnalysis(image: File): Promise<AxiosResponse<SkinAnalysis>> {
    const formData = new FormData();
    formData.append('image', image);
    return this.api.post('/detection/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  async getSkinAnalysis(analysisId: number): Promise<AxiosResponse<SkinAnalysis>> {
    return this.api.get(`/detection/analysis/${analysisId}/`);
  }

  async getUserAnalyses(): Promise<AxiosResponse<SkinAnalysis[]>> {
    // Solution temporaire : utiliser l'endpoint principal avec user_id
    const userId = this.getUserIdFromToken();
    if (!userId) {
      throw new Error('Utilisateur non authentifié');
    }
    return this.api.get(`/detection/analyses/?user_id=${userId}`);
  }

  async deleteSkinAnalysis(analysisId: number): Promise<AxiosResponse<void>> {
    return this.api.delete(`/detection/analysis/${analysisId}/delete/`);
  }

  // Méthodes pour les recommandations
  async getRecommendations(analysisId: number): Promise<AxiosResponse<Recommendation[]>> {
    return this.api.get(`/recommendations/analysis/${analysisId}/`);
  }

  async getProducts(): Promise<AxiosResponse<Product[]>> {
    return this.api.get('/products/');
  }

  async getProduct(productId: number): Promise<AxiosResponse<Product>> {
    return this.api.get(`/products/${productId}/`);
  }

  // Méthodes pour les simulations GAN
  async createGANSimulation(analysisId: number, simulationType: string): Promise<AxiosResponse<GANSimulation>> {
    return this.api.post('/gan/simulate/', {
      analysis_id: analysisId,
      simulation_type: simulationType,
    });
  }

  async getGANSimulation(simulationId: number): Promise<AxiosResponse<GANSimulation>> {
    return this.api.get(`/gan/simulation/${simulationId}/`);
  }

  async getUserGANSimulations(): Promise<AxiosResponse<GANSimulation[]>> {
    return this.api.get('/gan/simulations/');
  }

  // Méthodes pour l'historique
  async getHistory(): Promise<AxiosResponse<any[]>> {
    return this.api.get('/history/');
  }

  // Méthodes utilitaires
  async deleteAccount(): Promise<AxiosResponse<void>> {
    return this.api.delete('/users/delete-account/');
  }

  setAuthTokens(tokens: AuthTokens): void {
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
  }

  isAuthenticated(): boolean {
    const token = localStorage.getItem('access_token');
    if (!token) {
      console.log('API Service - Pas de token d\'accès');
      return false;
    }
    
    try {
      // Vérifier si le token JWT est valide (pas expiré)
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Math.floor(Date.now() / 1000);
      
      if (payload.exp && payload.exp < currentTime) {
        console.log('API Service - Token expiré, tentative de rafraîchissement...');
        // Ne pas supprimer immédiatement, laisser l'intercepteur gérer le refresh
        return false;
      }
      
      console.log('API Service - Token valide');
      return true;
    } catch (error) {
      console.log('API Service - Token invalide, mais on ne le supprime pas immédiatement:', error);
      // Ne pas supprimer les tokens immédiatement, laisser l'intercepteur gérer
      return false;
    }
  }

  // Méthode plus douce pour vérifier l'authentification
  hasValidTokens(): boolean {
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!accessToken || !refreshToken) {
      return false;
    }
    
    try {
      // Vérifier seulement si le token d'accès existe et n'est pas expiré
      const payload = JSON.parse(atob(accessToken.split('.')[1]));
      const currentTime = Math.floor(Date.now() / 1000);
      
      // Ajouter une marge de 5 minutes pour éviter les problèmes de timing
      return payload.exp && payload.exp > (currentTime + 300);
    } catch (error) {
      return false;
    }
  }

  getAuthHeaders(): { Authorization: string } | {} {
    const token = localStorage.getItem('access_token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  }

  // Generic HTTP methods
  async get(url: string, config?: any): Promise<AxiosResponse<any>> {
    return this.api.get(url, config);
  }

  async post(url: string, data?: any, config?: any): Promise<AxiosResponse<any>> {
    return this.api.post(url, data, config);
  }

  async put(url: string, data?: any, config?: any): Promise<AxiosResponse<any>> {
    return this.api.put(url, data, config);
  }

  async patch(url: string, data?: any, config?: any): Promise<AxiosResponse<any>> {
    return this.api.patch(url, data, config);
  }

  async delete(url: string, config?: any): Promise<AxiosResponse<any>> {
    return this.api.delete(url, config);
  }
}

export const apiService = new ApiService();
export default apiService;




