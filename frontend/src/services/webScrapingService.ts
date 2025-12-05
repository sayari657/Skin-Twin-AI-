import axios from 'axios';
import { Product } from '../types';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api';

export interface ScrapeWebRequest {
  url?: string;
  search_query?: string;
  source_site?: string;
  max_pages?: number;
  auto_save?: boolean;  // Sauvegarder automatiquement dans la base de données
}

export interface ScrapeWebResponse {
  success: boolean;
  products: Product[];
  total_found: number;
  total_saved?: number;  // Nombre de produits sauvegardés
  url?: string;
  error?: string;
  message?: string;  // Message de confirmation
}

class WebScrapingService {
  private api = axios.create({
    baseURL: BASE_URL,
    timeout: 900000,  // 15 minutes pour le scraping de plusieurs pages (100 pages * 1.5s = 2.5 min minimum + traitement)
    headers: {
      'Content-Type': 'application/json',
    },
  });

  async scrapeWebProducts(request: ScrapeWebRequest): Promise<ScrapeWebResponse> {
    try {
      const response = await this.api.post<ScrapeWebResponse>(
        '/scraped-products/scrape-web/',
        request
      );
      return response.data;
    } catch (error: any) {
      console.error('Erreur lors du scraping web:', error);
      
      // Gérer différents types d'erreurs
      let errorMessage = 'Erreur lors du scraping web';
      
      if (error.code === 'ECONNABORTED') {
        errorMessage = 'Timeout: Le scraping prend trop de temps. Essayez de réduire le nombre de pages.';
      } else if (error.response?.data?.error) {
        errorMessage = error.response.data.error;
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      return {
        success: false,
        products: [],
        total_found: 0,
        url: request.url || '',
        error: errorMessage,
      };
    }
  }

  async saveScrapedProducts(products: Product[]): Promise<any> {
    try {
      console.log(`📤 Envoi de ${products.length} produits au backend pour sauvegarde...`);
      
      const productsToSave = products.map(p => ({
        name: p.name,
        brand: p.brand,
        description: p.description || p.name,
        ingredients: p.ingredients || '',
        price: p.price || 0,
        size: p.size,
        category: p.category,
        target_skin_types: p.target_skin_types || ['NORMAL'],
        target_issues: p.target_issues || [],
        image: p.image,
        url: p.url,
        source_site: (p as any).source_site || 'pharma-shop.tn',
        source_url: (p as any).source_url,
      }));
      
      console.log(`📦 Données préparées pour ${productsToSave.length} produits`);
      console.log(`   Exemple de produit:`, productsToSave[0]);
      
      const response = await this.api.post('/scraped-products/save-products/', {
        products: productsToSave,
      });
      
      console.log(`✅ Réponse reçue:`, response.data);
      return response.data;
    } catch (error: any) {
      console.error('❌ Erreur lors de la sauvegarde:', error);
      if (error.response) {
        console.error('   Détails de l\'erreur:', error.response.data);
      }
      throw error;
    }
  }
}

export const webScrapingService = new WebScrapingService();

