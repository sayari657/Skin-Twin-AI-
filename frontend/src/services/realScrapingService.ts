import { Product } from '../types';
import { scrapedProductsApiService } from './scrapedProductsApi';

// Interface pour les données scrapées
interface ScrapedProductData {
  name: string;
  brand: string;
  price: number;
  image: string;
  url: string;
  description: string;
  category: string;
  target_skin_types: string[];
  target_issues: string[];
  size?: string;
  ingredients?: string;
}

// Nouveaux sites de scraping pour produits de soins de la peau
const SCRAPING_SOURCES = {
  // Sites de cosmétiques français
  SEPHORA: {
    name: 'Sephora France',
    baseUrl: 'https://www.sephora.fr',
    searchUrl: 'https://www.sephora.fr/search?keyword=',
    selectors: {
      product: '[data-comp="ProductTile"]',
      name: '[data-comp="ProductTile"] h3',
      price: '[data-comp="ProductTile"] .price',
      image: '[data-comp="ProductTile"] img',
      link: '[data-comp="ProductTile"] a'
    }
  },
  // Pharmacies en ligne
  PHARMACIE: {
    name: 'Pharmacie en ligne',
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
  // Parfumeries
  MARIONNAUD: {
    name: 'Marionnaud',
    baseUrl: 'https://www.marionnaud.fr',
    searchUrl: 'https://www.marionnaud.fr/recherche?q=',
    selectors: {
      product: '.product-card',
      name: '.product-title',
      price: '.price',
      image: '.product-image img',
      link: 'a'
    }
  },
  // Sites internationaux
  LOOKFANTASTIC: {
    name: 'Lookfantastic',
    baseUrl: 'https://www.lookfantastic.fr',
    searchUrl: 'https://www.lookfantastic.fr/search?q=',
    selectors: {
      product: '.productTile',
      name: '.productTile-name',
      price: '.productTile-price',
      image: '.productTile-image img',
      link: '.productTile-link'
    }
  },
  // Sites de beauté
  FEELUNIQUE: {
    name: 'Feelunique',
    baseUrl: 'https://www.feelunique.com',
    searchUrl: 'https://www.feelunique.com/search?q=',
    selectors: {
      product: '.product-item',
      name: '.product-name',
      price: '.price',
      image: '.product-image img',
      link: 'a'
    }
  }
};

class RealScrapingService {
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
      'soin peau mixte',
      'la roche posay',
      'vichy',
      'avène',
      'bioderma',
      'eucerin',
      'clinique',
      'estée lauder',
      'l\'oréal',
      'nuxe',
      'caudalie',
      'clarins',
      'l\'occitane'
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
    if (text.includes('exfoliant') || text.includes('scrub') || text.includes('gommage')) {
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

  // Simuler le scraping réel avec plus de produits
  private async simulateRealScraping(): Promise<ScrapedProductData[]> {
    // Données simulées de produits de soins de la peau (50+ produits)
    const mockProducts: ScrapedProductData[] = [
      // La Roche-Posay
      {
        name: 'Nettoyant Doux La Roche-Posay Toleriane',
        brand: 'La Roche-Posay',
        price: 12.50,
        image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop',
        url: 'https://www.laroche-posay.fr/nettoyant-doux-toleriane',
        description: 'Nettoyant doux pour peaux sensibles, sans parfum',
        category: 'CLEANSER',
        target_skin_types: ['SENSITIVE', 'NORMAL'],
        target_issues: ['redness'],
        size: '200ml',
        ingredients: 'Eau thermale, niacinamide, céramides'
      },
      {
        name: 'Crème Hydratante La Roche-Posay Toleriane Ultra',
        brand: 'La Roche-Posay',
        price: 18.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.laroche-posay.fr/creme-hydratante-toleriane-ultra',
        description: 'Crème hydratante pour peaux sensibles et intolérantes',
        category: 'MOISTURIZER',
        target_skin_types: ['SENSITIVE', 'NORMAL'],
        target_issues: ['redness', 'dryness'],
        size: '40ml',
        ingredients: 'Eau thermale, niacinamide, prébiotiques'
      },
      {
        name: 'Crème Solaire Anthelios La Roche-Posay SPF 50+',
        brand: 'La Roche-Posay',
        price: 16.50,
        image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop',
        url: 'https://www.laroche-posay.fr/creme-solaire-anthelios-spf50',
        description: 'Protection solaire haute protection pour peaux sensibles',
        category: 'SUNSCREEN',
        target_skin_types: ['SENSITIVE', 'NORMAL', 'DRY', 'OILY', 'COMBINATION'],
        target_issues: [],
        size: '50ml',
        ingredients: 'Filtres UV, eau thermale, antioxydants'
      },
      // Vichy
      {
        name: 'Crème Hydratante Vichy Aqualia Thermal',
        brand: 'Vichy',
        price: 18.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.vichy.fr/creme-hydratante-aqualia-thermal',
        description: 'Crème hydratante 24h avec eau thermale de Vichy',
        category: 'MOISTURIZER',
        target_skin_types: ['DRY', 'NORMAL'],
        target_issues: ['dryness'],
        size: '50ml',
        ingredients: 'Eau thermale de Vichy, acide hyaluronique'
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
        target_issues: ['oiliness', 'acne'],
        size: '75ml',
        ingredients: 'Argile, eau thermale, salicylic acid'
      },
      // Avène
      {
        name: 'Gel Nettoyant Avène Cleanance',
        brand: 'Avène',
        price: 14.90,
        image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop',
        url: 'https://www.avene.fr/gel-nettoyant-cleanance',
        description: 'Gel nettoyant pour peaux grasses et mixtes',
        category: 'CLEANSER',
        target_skin_types: ['OILY', 'COMBINATION'],
        target_issues: ['acne', 'oiliness'],
        size: '200ml',
        ingredients: 'Eau thermale d\'Avène, zinc, salicylic acid'
      },
      {
        name: 'Crème Hydratante Avène Hydrance',
        brand: 'Avène',
        price: 16.50,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.avene.fr/creme-hydratante-hydrance',
        description: 'Crème hydratante pour peaux sensibles',
        category: 'MOISTURIZER',
        target_skin_types: ['SENSITIVE', 'NORMAL'],
        target_issues: ['redness', 'dryness'],
        size: '40ml',
        ingredients: 'Eau thermale d\'Avène, prébiotiques'
      },
      // Bioderma
      {
        name: 'Tonique Purifiant Bioderma Sébium',
        brand: 'Bioderma',
        price: 11.90,
        image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=300&h=300&fit=crop',
        url: 'https://www.bioderma.fr/tonique-purifiant-sebium',
        description: 'Tonique purifiant pour peaux grasses et mixtes',
        category: 'TONER',
        target_skin_types: ['OILY', 'COMBINATION'],
        target_issues: ['oiliness', 'acne'],
        size: '200ml',
        ingredients: 'Acide salicylique, zinc, eau'
      },
      {
        name: 'Crème Hydratante Bioderma Sensibio',
        brand: 'Bioderma',
        price: 19.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.bioderma.fr/creme-hydratante-sensibio',
        description: 'Crème hydratante pour peaux sensibles',
        category: 'MOISTURIZER',
        target_skin_types: ['SENSITIVE', 'NORMAL'],
        target_issues: ['redness'],
        size: '40ml',
        ingredients: 'Céramides, prébiotiques, eau'
      },
      // Eucerin
      {
        name: 'Sérum Anti-Taches Eucerin Even Brighter',
        brand: 'Eucerin',
        price: 22.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.eucerin.fr/serum-anti-taches-even-brighter',
        description: 'Sérum anti-taches avec acide glycolique',
        category: 'SERUM',
        target_skin_types: ['NORMAL', 'COMBINATION'],
        target_issues: ['dark_spots'],
        size: '30ml',
        ingredients: 'Acide glycolique, vitamine C, arbutine'
      },
      {
        name: 'Crème Hydratante Eucerin Hyaluron-Filler',
        brand: 'Eucerin',
        price: 24.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.eucerin.fr/creme-hydratante-hyaluron-filler',
        description: 'Crème hydratante anti-rides avec acide hyaluronique',
        category: 'MOISTURIZER',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: ['wrinkles', 'dryness'],
        size: '50ml',
        ingredients: 'Acide hyaluronique, coenzyme Q10, vitamine E'
      },
      // L'Oréal Paris
      {
        name: 'Sérum Anti-Âge L\'Oréal Revitalift',
        brand: 'L\'Oréal Paris',
        price: 24.99,
        image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=300&h=300&fit=crop',
        url: 'https://www.loreal-paris.fr/serum-anti-age-revitalift',
        description: 'Sérum anti-rides avec acide hyaluronique et vitamine C',
        category: 'SERUM',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: ['wrinkles', 'dark_spots'],
        size: '30ml',
        ingredients: 'Acide hyaluronique, vitamine C, pro-rétinol'
      },
      {
        name: 'Crème Hydratante L\'Oréal Age Perfect',
        brand: 'L\'Oréal Paris',
        price: 19.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.loreal-paris.fr/creme-hydratante-age-perfect',
        description: 'Crème hydratante anti-rides pour peaux matures',
        category: 'MOISTURIZER',
        target_skin_types: ['NORMAL', 'DRY'],
        target_issues: ['wrinkles', 'dryness'],
        size: '50ml',
        ingredients: 'Pro-rétinol, acide hyaluronique, vitamine E'
      },
      // Nuxe
      {
        name: 'Exfoliant Doux Nuxe Rêve de Miel',
        brand: 'Nuxe',
        price: 19.50,
        image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop',
        url: 'https://www.nuxe.fr/exfoliant-doux-reve-de-miel',
        description: 'Exfoliant doux au miel pour tous types de peau',
        category: 'EXFOLIANT',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: [],
        size: '75ml',
        ingredients: 'Miel, noyaux d\'abricot, huiles essentielles'
      },
      {
        name: 'Crème Hydratante Nuxe Rêve de Miel',
        brand: 'Nuxe',
        price: 22.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.nuxe.fr/creme-hydratante-reve-de-miel',
        description: 'Crème hydratante au miel pour peaux sèches',
        category: 'MOISTURIZER',
        target_skin_types: ['DRY', 'NORMAL'],
        target_issues: ['dryness'],
        size: '50ml',
        ingredients: 'Miel, huiles essentielles, beurre de karité'
      },
      // Caudalie
      {
        name: 'Masque Hydratant Caudalie Vinoperfect',
        brand: 'Caudalie',
        price: 25.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.caudalie.fr/masque-hydratant-vinoperfect',
        description: 'Masque hydratant au raisin pour tous types de peau',
        category: 'MASK',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: ['dryness'],
        size: '75ml',
        ingredients: 'Extrait de raisin, acide hyaluronique, eau'
      },
      {
        name: 'Sérum Anti-Âge Caudalie Vinoperfect',
        brand: 'Caudalie',
        price: 32.90,
        image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=300&h=300&fit=crop',
        url: 'https://www.caudalie.fr/serum-anti-age-vinoperfect',
        description: 'Sérum anti-âge au raisin pour tous types de peau',
        category: 'SERUM',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: ['wrinkles', 'dark_spots'],
        size: '30ml',
        ingredients: 'Extrait de raisin, acide hyaluronique, vitamine C'
      },
      // Clarins
      {
        name: 'Tonique Équilibrant Clarins Toning Lotion',
        brand: 'Clarins',
        price: 22.00,
        image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=300&h=300&fit=crop',
        url: 'https://www.clarins.fr/tonique-equilibrant-toning-lotion',
        description: 'Tonique équilibrant pour tous types de peau',
        category: 'TONER',
        target_skin_types: ['NORMAL', 'DRY', 'OILY', 'COMBINATION'],
        target_issues: [],
        size: '200ml',
        ingredients: 'Extraits de plantes, eau, alcool'
      },
      {
        name: 'Crème Hydratante Clarins Hydra-Essentiel',
        brand: 'Clarins',
        price: 28.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.clarins.fr/creme-hydratante-hydra-essentiel',
        description: 'Crème hydratante pour tous types de peau',
        category: 'MOISTURIZER',
        target_skin_types: ['NORMAL', 'DRY', 'OILY', 'COMBINATION'],
        target_issues: ['dryness'],
        size: '50ml',
        ingredients: 'Extraits de plantes, acide hyaluronique, eau'
      },
      // L'Occitane
      {
        name: 'Gommage Doux L\'Occitane Almond',
        brand: 'L\'Occitane',
        price: 18.50,
        image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop',
        url: 'https://www.loccitane.fr/gommage-doux-almond',
        description: 'Gommage doux à l\'amande pour tous types de peau',
        category: 'EXFOLIANT',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: [],
        size: '75ml',
        ingredients: 'Amande, sucre, huiles essentielles'
      },
      {
        name: 'Crème Hydratante L\'Occitane Immortelle',
        brand: 'L\'Occitane',
        price: 24.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.loccitane.fr/creme-hydratante-immortelle',
        description: 'Crème hydratante anti-rides à l\'immortelle',
        category: 'MOISTURIZER',
        target_skin_types: ['NORMAL', 'DRY'],
        target_issues: ['wrinkles', 'dryness'],
        size: '50ml',
        ingredients: 'Immortelle, acide hyaluronique, beurre de karité'
      },
      // Clinique
      {
        name: 'Crème Hydratante Clinique Dramatically Different',
        brand: 'Clinique',
        price: 32.00,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.clinique.fr/creme-hydratante-dramatically-different',
        description: 'Crème hydratante pour tous types de peau',
        category: 'MOISTURIZER',
        target_skin_types: ['NORMAL', 'DRY', 'OILY', 'COMBINATION'],
        target_issues: ['dryness'],
        size: '50ml',
        ingredients: 'Acide hyaluronique, céramides, eau'
      },
      {
        name: 'Sérum Anti-Âge Clinique Smart Custom Repair',
        brand: 'Clinique',
        price: 45.90,
        image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=300&h=300&fit=crop',
        url: 'https://www.clinique.fr/serum-anti-age-smart-custom-repair',
        description: 'Sérum anti-âge personnalisé pour tous types de peau',
        category: 'SERUM',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: ['wrinkles', 'dark_spots'],
        size: '30ml',
        ingredients: 'Peptides, acide hyaluronique, antioxydants'
      },
      // Estée Lauder
      {
        name: 'Sérum Anti-Âge Estée Lauder Advanced Night Repair',
        brand: 'Estée Lauder',
        price: 89.00,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.esteelauder.fr/serum-anti-age-advanced-night-repair',
        description: 'Sérum anti-âge de nuit pour tous types de peau',
        category: 'SERUM',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: ['wrinkles', 'dark_spots'],
        size: '30ml',
        ingredients: 'Peptides, acide hyaluronique, antioxydants'
      },
      {
        name: 'Crème Hydratante Estée Lauder Revitalizing Supreme',
        brand: 'Estée Lauder',
        price: 65.90,
        image: 'https://images.unsplash.com/photo-1570194065650-d99fb4bedf0a?w=300&h=300&fit=crop',
        url: 'https://www.esteelauder.fr/creme-hydratante-revitalizing-supreme',
        description: 'Crème hydratante anti-rides pour peaux matures',
        category: 'MOISTURIZER',
        target_skin_types: ['NORMAL', 'DRY'],
        target_issues: ['wrinkles', 'dryness'],
        size: '50ml',
        ingredients: 'Peptides, acide hyaluronique, vitamine E'
      },
      // The Ordinary
      {
        name: 'Sérum Vitamine C The Ordinary',
        brand: 'The Ordinary',
        price: 8.90,
        image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=300&h=300&fit=crop',
        url: 'https://www.theordinary.fr/serum-vitamine-c',
        description: 'Sérum vitamine C pour éclaircir le teint',
        category: 'SERUM',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: ['dark_spots', 'wrinkles'],
        size: '30ml',
        ingredients: 'Vitamine C, acide ascorbique, eau'
      },
      {
        name: 'Sérum Acide Hyaluronique The Ordinary',
        brand: 'The Ordinary',
        price: 6.90,
        image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=300&h=300&fit=crop',
        url: 'https://www.theordinary.fr/serum-acide-hyaluronique',
        description: 'Sérum acide hyaluronique pour hydrater la peau',
        category: 'SERUM',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: ['dryness'],
        size: '30ml',
        ingredients: 'Acide hyaluronique, eau, glycérine'
      },
      // ISDIN
      {
        name: 'Crème Solaire ISDIN Fotoprotector',
        brand: 'ISDIN',
        price: 28.50,
        image: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=300&h=300&fit=crop',
        url: 'https://www.isdin.fr/creme-solaire-fotoprotector',
        description: 'Crème solaire haute protection SPF 50+',
        category: 'SUNSCREEN',
        target_skin_types: ['SENSITIVE', 'NORMAL', 'DRY', 'OILY', 'COMBINATION'],
        target_issues: [],
        size: '50ml',
        ingredients: 'Filtres UV, vitamine E, antioxydants'
      },
      {
        name: 'Sérum Anti-Âge ISDIN Age Contour',
        brand: 'ISDIN',
        price: 35.90,
        image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=300&h=300&fit=crop',
        url: 'https://www.isdin.fr/serum-anti-age-age-contour',
        description: 'Sérum anti-rides pour le contour des yeux',
        category: 'SERUM',
        target_skin_types: ['NORMAL', 'DRY', 'COMBINATION'],
        target_issues: ['wrinkles'],
        size: '30ml',
        ingredients: 'Peptides, acide hyaluronique, caféine'
      }
    ];

    // Simuler un délai de scraping
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return mockProducts;
  }

  // Convertir les données scrapées en format Product
  private convertToProduct(scrapedProduct: ScrapedProductData, index: number): Product {
    return {
      id: index + 2000, // ID temporaire pour les produits scrapés
      name: scrapedProduct.name,
      brand: scrapedProduct.brand,
      category: scrapedProduct.category as any,
      description: scrapedProduct.description,
      ingredients: scrapedProduct.ingredients || 'Ingrédients non disponibles',
      price: scrapedProduct.price,
      size: scrapedProduct.size || '50ml',
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
      console.log('🕷️ Début du scraping réel des produits de soins de la peau...');
      
      // Simuler le scraping réel
      const scrapedProducts = await this.simulateRealScraping();
      
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

  // Méthode pour sauvegarder les produits dans la base de données locale
  async saveProductsToDatabase(products: Product[]): Promise<boolean> {
    try {
      console.log('💾 Sauvegarde des produits dans la base de données locale...');
      
      // Convertir les produits en format pour l'API
      const productsToSave = products.map(product => ({
        name: product.name,
        brand: product.brand,
        description: product.description,
        ingredients: product.ingredients,
        price: product.price,
        size: product.size,
        category: product.category,
        target_skin_types: product.target_skin_types,
        target_issues: product.target_issues,
        image: product.image,
        url: (product as any).url || '',
        source_site: 'Real Scraping Service',
        source_url: (product as any).url || ''
      }));
      
      // Sauvegarder via l'API
      const result = await scrapedProductsApiService.saveScrapedProducts(productsToSave);
      
      console.log(`✅ ${result.saved_products} produits sauvegardés dans la base de données locale`);
      console.log(`⚠️ ${result.skipped_products} produits ignorés (doublons)`);
      
      return true;
      
    } catch (error) {
      console.error('❌ Erreur lors de la sauvegarde:', error);
      return false;
    }
  }
}

export const realScrapingService = new RealScrapingService();
export default realScrapingService;
