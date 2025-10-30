import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

class ScrapedProductsApiService {
  private baseURL = `${API_BASE_URL}/scraped-products`;

  // Récupérer tous les produits scrapés
  async getScrapedProducts(params?: {
    category?: string;
    brand?: string;
    search?: string;
    min_price?: number;
    max_price?: number;
  }) {
    try {
      const response = await axios.get(`${this.baseURL}/products/`, { params });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des produits scrapés:', error);
      throw error;
    }
  }

  // Rechercher des produits scrapés
  async searchProducts(query: string, category?: string, brand?: string) {
    try {
      const params: any = { q: query };
      if (category) params.category = category;
      if (brand) params.brand = brand;
      
      const response = await axios.get(`${this.baseURL}/products/search/`, { params });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la recherche de produits scrapés:', error);
      throw error;
    }
  }

  // Récupérer un produit scrapé par ID
  async getScrapedProduct(id: number) {
    try {
      const response = await axios.get(`${this.baseURL}/products/${id}/`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération du produit scrapé:', error);
      throw error;
    }
  }

  // Créer un nouveau produit scrapé
  async createScrapedProduct(productData: any) {
    try {
      const response = await axios.post(`${this.baseURL}/products/`, productData);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la création du produit scrapé:', error);
      throw error;
    }
  }

  // Sauvegarder plusieurs produits scrapés
  async saveScrapedProducts(products: any[], sessionId?: number) {
    try {
      const response = await axios.post(`${this.baseURL}/save-products/`, {
        products,
        session_id: sessionId
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la sauvegarde des produits scrapés:', error);
      throw error;
    }
  }

  // Démarrer une nouvelle session de scraping
  async startScrapingSession(sessionName: string, sourceSites: string[]) {
    try {
      const response = await axios.post(`${this.baseURL}/start-session/`, {
        session_name: sessionName,
        source_sites: sourceSites
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors du démarrage de la session de scraping:', error);
      throw error;
    }
  }

  // Récupérer les statistiques de scraping
  async getScrapingStats() {
    try {
      const response = await axios.get(`${this.baseURL}/stats/`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des statistiques:', error);
      throw error;
    }
  }

  // Récupérer les sessions de scraping
  async getScrapingSessions() {
    try {
      const response = await axios.get(`${this.baseURL}/sessions/`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des sessions:', error);
      throw error;
    }
  }

  // Récupérer une session de scraping par ID
  async getScrapingSession(id: number) {
    try {
      const response = await axios.get(`${this.baseURL}/sessions/${id}/`);
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération de la session:', error);
      throw error;
    }
  }
}

export const scrapedProductsApiService = new ScrapedProductsApiService();
export default scrapedProductsApiService;




