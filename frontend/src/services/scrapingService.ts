import { Product } from '../types';

// Interface pour les données scrapées
interface ScrapedProduct {
  name: string;
  brand: string;
  price: number;
  image: string;
  url: string;
  description: string;
  category: string;
  target_skin_types: string[];
  target_issues: string[];
}

// Sites de scraping pour les produits de soins de la peau
const SCRAPING_SOURCES = {
  // Pharmacies françaises
  PHARMACIE: {
    name: 'Pharmacie',
    baseUrl: 'https://www.pharmacie.com',
    searchUrl: 'https://www.pharmacie.com/search?q=',
    selectors: {
      product: '.product-item',
      name: '.product-name',
      price: '.price',
      image: '.product-image img',
      link: 'a'
    }
  },
  // Sephora
  SEPHORA: {
    name: 'Sephora',
    baseUrl: 'https://www.sephora.fr',
    searchUrl: 'https://www.sephora.fr/search?keyword=',
    selectors: {
      product: '.product-tile',
      name: '.product-name',
      price: '.price',
      image: '.product-image img',
      link: 'a'
    }
  },
  // Nocibé
  NOCIBE: {
    name: 'Nocibé',
    baseUrl: 'https://www.nocibe.fr',
    searchUrl: 'https://www.nocibe.fr/recherche?q=',
    selectors: {
      product: '.product-card',
      name: '.product-title',
      price: '.price',
      image: '.product-image img',
      link: 'a'
    }
  },
  // Marionnaud
  MARIONNAUD: {
    name: 'Marionnaud',
    baseUrl: 'https://www.marionnaud.fr',
    searchUrl: 'https://www.marionnaud.fr/recherche?q=',
    selectors: {
      product: '.product-item',
      name: '.product-name',
      price: '.price',
      image: '.product-image img',
      link: 'a'
    }
  },
  // Douglas
  DOUGLAS: {
    name: 'Douglas',
    baseUrl: 'https://www.douglas.fr',
    searchUrl: 'https://www.douglas.fr/recherche?q=',
    selectors: {
      product: '.product-tile',
      name: '.product-title',
      price: '.price',
      image: '.product-image img',
      link: 'a'
    }
  },
  // Lookfantastic
  LOOKFANTASTIC: {
    name: 'Lookfantastic',
    baseUrl: 'https://www.lookfantastic.fr',
    searchUrl: 'https://www.lookfantastic.fr/search?q=',
    selectors: {
      product: '.product-item',
      name: '.product-name',
      price: '.price',
      image: '.product-image img',
      link: 'a'
    }
  },
  // Feelunique
  FEELUNIQUE: {
    name: 'Feelunique',
    baseUrl: 'https://www.feelunique.com',
    searchUrl: 'https://www.feelunique.com/search?q=',
    selectors: {
      product: '.product-card',
      name: '.product-title',
      price: '.price',
      image: '.product-image img',
      link: 'a'
    }
  },
  // Notino
  NOTINO: {
    name: 'Notino',
    baseUrl: 'https://www.notino.fr',
    searchUrl: 'https://www.notino.fr/recherche?q=',
    selectors: {
      product: '.product-item',
      name: '.product-name',
      price: '.price',
      image: '.product-image img',
      link: 'a'
    }
  }
};

class ScrapingService {
  private baseURL = 'http://127.0.0.1:8000/api';

  // Mots-clés de recherche pour les produits de soins de la peau
  private getSearchKeywords(): string[] {
    return [
      'nettoyant visage',
      'crème hydratante',
      'sérum anti-âge',
      'crème solaire',
      'masque visage',
      'tonique',
      'exfoliant',
      'soin anti-acné',
      'soin anti-rides',
      'soin peau sensible',
      'soin peau sèche',
      'soin peau grasse',
      'soin peau mixte'
    ];
  }

  // Catégoriser les produits selon les mots-clés
  private categorizeProduct(name: string, description: string): string {
    const text = (name + ' ' + description).toLowerCase();
    
    if (text.includes('nettoyant') || text.includes('cleanser') || text.includes('gel nettoyant')) {
      return 'CLEANSER';
    }
    if (text.includes('hydratant') || text.includes('moisturizer') || text.includes('crème')) {
      return 'MOISTURIZER';
    }
    if (text.includes('sérum') || text.includes('serum')) {
      return 'SERUM';
    }
    if (text.includes('solaire') || text.includes('sunscreen') || text.includes('spf')) {
      return 'SUNSCREEN';
    }
    if (text.includes('masque') || text.includes('mask')) {
      return 'MASK';
    }
    if (text.includes('tonique') || text.includes('toner')) {
      return 'TONER';
    }
    if (text.includes('exfoliant') || text.includes('scrub')) {
      return 'EXFOLIANT';
    }
    if (text.includes('traitement') || text.includes('treatment') || text.includes('soin')) {
      return 'TREATMENT';
    }
    
    return 'TREATMENT'; // Par défaut
  }

  // Déterminer les types de peau ciblés
  private getTargetSkinTypes(name: string, description: string): string[] {
    const text = (name + ' ' + description).toLowerCase();
    const skinTypes: string[] = [];
    
    if (text.includes('sensible') || text.includes('sensitive')) {
      skinTypes.push('SENSITIVE');
    }
    if (text.includes('sèche') || text.includes('dry')) {
      skinTypes.push('DRY');
    }
    if (text.includes('grasse') || text.includes('oily')) {
      skinTypes.push('OILY');
    }
    if (text.includes('mixte') || text.includes('combination')) {
      skinTypes.push('COMBINATION');
    }
    if (text.includes('normale') || text.includes('normal')) {
      skinTypes.push('NORMAL');
    }
    
    // Si aucun type spécifique, on assume que c'est pour tous les types
    if (skinTypes.length === 0) {
      skinTypes.push('NORMAL', 'DRY', 'OILY', 'COMBINATION', 'SENSITIVE');
    }
    
    return skinTypes;
  }

  // Déterminer les problèmes ciblés
  private getTargetIssues(name: string, description: string): string[] {
    const text = (name + ' ' + description).toLowerCase();
    const issues: string[] = [];
    
    if (text.includes('acné') || text.includes('acne') || text.includes('bouton')) {
      issues.push('acne');
    }
    if (text.includes('ride') || text.includes('anti-âge') || text.includes('anti-age')) {
      issues.push('wrinkles');
    }
    if (text.includes('tache') || text.includes('pigmentation') || text.includes('tâche')) {
      issues.push('dark_spots');
    }
    if (text.includes('rougeur') || text.includes('irritation') || text.includes('sensible')) {
      issues.push('redness');
    }
    if (text.includes('hydratation') || text.includes('sèche') || text.includes('dry')) {
      issues.push('dryness');
    }
    if (text.includes('brillance') || text.includes('grasse') || text.includes('oily')) {
      issues.push('oiliness');
    }
    
    return issues;
  }

  // Simuler le scraping (en réalité, cela nécessiterait un backend avec des outils comme Puppeteer ou Scrapy)
  private async simulateScraping(): Promise<ScrapedProduct[]> {
    // Données simulées de produits de soins de la peau
    const mockProducts: ScrapedProduct[] = [
      {
        name: 'Nettoyant Doux La Roche-Posay',
        brand: 'La Roche-Posay',
        price: 12.50,
        image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop',
        url: 'https://www.laroche-posay.fr/nettoyant-doux',
        description: 'Nettoyant doux pour tous types de peau, même les plus sensibles',
        category: 'CLEANSER',
        target_skin_types: ['SENSITIVE', 'NORMAL'],
        target_issues: ['redness']
      },
      {
        name: 'Crème Hydratante Vichy Aqualia',
        brand: 'Vichy',
        price: 18.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.vichy.fr/creme-hydratante-aqualia',
        description: 'Crème hydratante 24h pour peaux sèches et déshydratées',
        category: 'MOISTURIZER',
        target_skin_types: ['DRY', 'NORMAL'],
        target_issues: ['dryness']
      },
      {
        name: 'Sérum Anti-Âge L\'Oréal Revitalift',
        brand: 'L\'Oréal Paris',
        price: 24.99,
        image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=300&h=300&fit=crop',
        url: 'https://www.loreal-paris.fr/serum-anti-age-revitalift',
        description: 'Sérum anti-rides avec acide hyaluronique et vitamine C',
        category: 'SERUM',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: ['wrinkles', 'dark_spots']
      },
      {
        name: 'Crème Solaire Anthelios La Roche-Posay',
        brand: 'La Roche-Posay',
        price: 16.50,
        image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop',
        url: 'https://www.laroche-posay.fr/creme-solaire-anthelios',
        description: 'Protection solaire SPF 50+ pour peaux sensibles',
        category: 'SUNSCREEN',
        target_skin_types: ['SENSITIVE', 'NORMAL', 'DRY', 'OILY', 'COMBINATION'],
        target_issues: []
      },
      {
        name: 'Masque Purifiant Vichy Normaderm',
        brand: 'Vichy',
        price: 15.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.vichy.fr/masque-purifiant-normaderm',
        description: 'Masque purifiant pour peaux grasses et mixtes',
        category: 'MASK',
        target_skin_types: ['OILY', 'COMBINATION'],
        target_issues: ['oiliness', 'acne']
      },
      {
        name: 'Tonique Purifiant Bioderma Sébium',
        brand: 'Bioderma',
        price: 11.90,
        image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=300&h=300&fit=crop',
        url: 'https://www.bioderma.fr/tonique-purifiant-sebium',
        description: 'Tonique purifiant pour peaux grasses et mixtes',
        category: 'TONER',
        target_skin_types: ['OILY', 'COMBINATION'],
        target_issues: ['oiliness', 'acne']
      },
      {
        name: 'Exfoliant Doux Nuxe Reve de Miel',
        brand: 'Nuxe',
        price: 19.50,
        image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop',
        url: 'https://www.nuxe.fr/exfoliant-doux-reve-de-miel',
        description: 'Exfoliant doux au miel pour tous types de peau',
        category: 'EXFOLIANT',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: []
      },
      {
        name: 'Sérum Anti-Taches Eucerin Even Brighter',
        brand: 'Eucerin',
        price: 22.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.eucerin.fr/serum-anti-taches-even-brighter',
        description: 'Sérum anti-taches avec acide glycolique',
        category: 'SERUM',
        target_skin_types: ['NORMAL', 'COMBINATION'],
        target_issues: ['dark_spots']
      },
      // Nouveaux produits de différents sites
      {
        name: 'Gel Nettoyant Avène Cleanance',
        brand: 'Avène',
        price: 14.90,
        image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop',
        url: 'https://www.marionnaud.fr/gel-nettoyant-avene-cleanance',
        description: 'Gel nettoyant pour peaux grasses et mixtes',
        category: 'CLEANSER',
        target_skin_types: ['OILY', 'COMBINATION'],
        target_issues: ['acne', 'oiliness']
      },
      {
        name: 'Crème Hydratante Clinique Dramatically Different',
        brand: 'Clinique',
        price: 32.00,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.douglas.fr/creme-hydratante-clinique',
        description: 'Crème hydratante pour tous types de peau',
        category: 'MOISTURIZER',
        target_skin_types: ['NORMAL', 'DRY', 'OILY', 'COMBINATION'],
        target_issues: ['dryness']
      },
      {
        name: 'Sérum Vitamine C The Ordinary',
        brand: 'The Ordinary',
        price: 8.90,
        image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=300&h=300&fit=crop',
        url: 'https://www.lookfantastic.fr/serum-vitamine-c-the-ordinary',
        description: 'Sérum vitamine C pour éclaircir le teint',
        category: 'SERUM',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: ['dark_spots', 'wrinkles']
      },
      {
        name: 'Crème Solaire ISDIN Fotoprotector',
        brand: 'ISDIN',
        price: 28.50,
        image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop',
        url: 'https://www.feelunique.com/creme-solaire-isdin',
        description: 'Crème solaire haute protection SPF 50+',
        category: 'SUNSCREEN',
        target_skin_types: ['SENSITIVE', 'NORMAL', 'DRY', 'OILY', 'COMBINATION'],
        target_issues: []
      },
      {
        name: 'Masque Hydratant Caudalie Vinoperfect',
        brand: 'Caudalie',
        price: 25.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.notino.fr/masque-hydratant-caudalie',
        description: 'Masque hydratant au raisin pour tous types de peau',
        category: 'MASK',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: ['dryness']
      },
      {
        name: 'Tonique Équilibrant Clarins Toning Lotion',
        brand: 'Clarins',
        price: 22.00,
        image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=300&h=300&fit=crop',
        url: 'https://www.sephora.fr/tonique-clarins',
        description: 'Tonique équilibrant pour tous types de peau',
        category: 'TONER',
        target_skin_types: ['NORMAL', 'DRY', 'OILY', 'COMBINATION'],
        target_issues: []
      },
      {
        name: 'Gommage Doux L\'Occitane Almond',
        brand: 'L\'Occitane',
        price: 18.50,
        image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop',
        url: 'https://www.nocibe.fr/gommage-loccitane-almond',
        description: 'Gommage doux à l\'amande pour tous types de peau',
        category: 'EXFOLIANT',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: []
      },
      {
        name: 'Sérum Anti-Âge Estée Lauder Advanced Night Repair',
        brand: 'Estée Lauder',
        price: 89.00,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.douglas.fr/serum-anti-age-estee-lauder',
        description: 'Sérum anti-âge de nuit pour tous types de peau',
        category: 'SERUM',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: ['wrinkles', 'dark_spots']
      }
    ];

    // Simuler un délai de scraping
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return mockProducts;
  }

  // Convertir les données scrapées en format Product
  private convertToProduct(scrapedProduct: ScrapedProduct, index: number): Product {
    return {
      id: index + 1000, // ID temporaire pour les produits scrapés
      name: scrapedProduct.name,
      brand: scrapedProduct.brand,
      category: scrapedProduct.category as any,
      description: scrapedProduct.description,
      ingredients: 'Ingrédients non disponibles (produit externe)',
      price: scrapedProduct.price,
      size: '50ml', // Taille par défaut
      target_skin_types: scrapedProduct.target_skin_types,
      target_issues: scrapedProduct.target_issues,
      image: scrapedProduct.image,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      is_active: true,
      // Ajouter l'URL du produit pour redirection
      url: scrapedProduct.url
    } as Product & { url: string };
  }

  // Méthode principale pour récupérer les produits scrapés
  async getScrapedProducts(): Promise<Product[]> {
    try {
      console.log('🕷️ Début du scraping des produits de soins de la peau...');
      
      // Simuler le scraping
      const scrapedProducts = await this.simulateScraping();
      
      // Convertir en format Product
      const products = scrapedProducts.map((scraped, index) => 
        this.convertToProduct(scraped, index)
      );
      
      console.log(`✅ ${products.length} produits scrapés avec succès`);
      return products;
      
    } catch (error) {
      console.error('❌ Erreur lors du scraping:', error);
      throw new Error('Impossible de récupérer les produits scrapés');
    }
  }

  // Méthode pour rechercher des produits spécifiques
  async searchProducts(query: string): Promise<Product[]> {
    try {
      console.log(`🔍 Recherche de produits pour: "${query}"`);
      
      // Simuler la recherche
      const allProducts = await this.getScrapedProducts();
      
      // Filtrer selon la requête
      const filteredProducts = allProducts.filter(product => 
        product.name.toLowerCase().includes(query.toLowerCase()) ||
        product.brand.toLowerCase().includes(query.toLowerCase()) ||
        product.description.toLowerCase().includes(query.toLowerCase())
      );
      
      console.log(`✅ ${filteredProducts.length} produits trouvés pour "${query}"`);
      return filteredProducts;
      
    } catch (error) {
      console.error('❌ Erreur lors de la recherche:', error);
      throw new Error('Impossible de rechercher les produits');
    }
  }

  // Méthode pour obtenir les produits par catégorie
  async getProductsByCategory(category: string): Promise<Product[]> {
    try {
      console.log(`📂 Récupération des produits de catégorie: ${category}`);
      
      const allProducts = await this.getScrapedProducts();
      const filteredProducts = allProducts.filter(product => 
        product.category === category
      );
      
      console.log(`✅ ${filteredProducts.length} produits trouvés pour la catégorie ${category}`);
      return filteredProducts;
      
    } catch (error) {
      console.error('❌ Erreur lors du filtrage par catégorie:', error);
      throw new Error('Impossible de filtrer les produits par catégorie');
    }
  }
}

export const scrapingService = new ScrapingService();
export default scrapingService;
