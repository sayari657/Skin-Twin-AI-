import { Product } from '../types';

// Interface pour les éléments du panier
export interface CartItem {
  product: Product;
  quantity: number;
  addedAt: string;
  source: 'scraped' | 'database';
}

// Interface pour le panier
export interface Cart {
  items: CartItem[];
  totalItems: number;
  totalPrice: number;
  lastUpdated: string;
}

class CartService {
  private readonly CART_STORAGE_KEY = 'skin_twin_cart';

  // Récupérer le panier depuis le localStorage
  private getCartFromStorage(): Cart {
    try {
      const cartData = localStorage.getItem(this.CART_STORAGE_KEY);
      if (cartData) {
        return JSON.parse(cartData);
      }
    } catch (error) {
      console.error('Erreur lors de la récupération du panier:', error);
    }
    
    return {
      items: [],
      totalItems: 0,
      totalPrice: 0,
      lastUpdated: new Date().toISOString()
    };
  }

  // Sauvegarder le panier dans le localStorage
  private saveCartToStorage(cart: Cart): void {
    try {
      localStorage.setItem(this.CART_STORAGE_KEY, JSON.stringify(cart));
    } catch (error) {
      console.error('Erreur lors de la sauvegarde du panier:', error);
    }
  }

  // Calculer le total du panier
  private calculateCartTotals(cart: Cart): Cart {
    const totalItems = cart.items.reduce((sum, item) => sum + item.quantity, 0);
    const totalPrice = cart.items.reduce((sum, item) => {
      return sum + (item.product.price || 0) * item.quantity;
    }, 0);

    return {
      ...cart,
      totalItems,
      totalPrice: Math.round(totalPrice * 100) / 100, // Arrondir à 2 décimales
      lastUpdated: new Date().toISOString()
    };
  }

  // Récupérer le panier actuel
  getCart(): Cart {
    return this.getCartFromStorage();
  }

  // Ajouter un produit au panier
  addToCart(product: Product, quantity: number = 1, source: 'scraped' | 'database' = 'scraped'): Cart {
    const cart = this.getCartFromStorage();
    
    // Vérifier si le produit existe déjà dans le panier
    const existingItemIndex = cart.items.findIndex(
      item => item.product.id === product.id
    );

    if (existingItemIndex !== -1) {
      // Mettre à jour la quantité si le produit existe déjà
      cart.items[existingItemIndex].quantity += quantity;
    } else {
      // Ajouter un nouvel élément au panier
      const newItem: CartItem = {
        product,
        quantity,
        addedAt: new Date().toISOString(),
        source
      };
      cart.items.push(newItem);
    }

    // Recalculer les totaux et sauvegarder
    const updatedCart = this.calculateCartTotals(cart);
    this.saveCartToStorage(updatedCart);
    
    console.log(`✅ Produit ajouté au panier: ${product.name} (x${quantity})`);
    return updatedCart;
  }

  // Supprimer un produit du panier
  removeFromCart(productId: number): Cart {
    const cart = this.getCartFromStorage();
    cart.items = cart.items.filter(item => item.product.id !== productId);
    
    const updatedCart = this.calculateCartTotals(cart);
    this.saveCartToStorage(updatedCart);
    
    console.log(`🗑️ Produit supprimé du panier: ID ${productId}`);
    return updatedCart;
  }

  // Mettre à jour la quantité d'un produit
  updateQuantity(productId: number, newQuantity: number): Cart {
    const cart = this.getCartFromStorage();
    const itemIndex = cart.items.findIndex(item => item.product.id === productId);
    
    if (itemIndex !== -1) {
      if (newQuantity <= 0) {
        // Supprimer l'élément si la quantité est 0 ou négative
        cart.items.splice(itemIndex, 1);
      } else {
        // Mettre à jour la quantité
        cart.items[itemIndex].quantity = newQuantity;
      }
    }

    const updatedCart = this.calculateCartTotals(cart);
    this.saveCartToStorage(updatedCart);
    
    console.log(`📝 Quantité mise à jour: ID ${productId} → ${newQuantity}`);
    return updatedCart;
  }

  // Vider le panier
  clearCart(): Cart {
    const emptyCart: Cart = {
      items: [],
      totalItems: 0,
      totalPrice: 0,
      lastUpdated: new Date().toISOString()
    };
    
    this.saveCartToStorage(emptyCart);
    console.log('🧹 Panier vidé');
    return emptyCart;
  }

  // Vérifier si un produit est dans le panier
  isInCart(productId: number): boolean {
    const cart = this.getCartFromStorage();
    return cart.items.some(item => item.product.id === productId);
  }

  // Obtenir la quantité d'un produit dans le panier
  getProductQuantity(productId: number): number {
    const cart = this.getCartFromStorage();
    const item = cart.items.find(item => item.product.id === productId);
    return item ? item.quantity : 0;
  }

  // Obtenir les statistiques du panier
  getCartStats(): {
    totalItems: number;
    totalPrice: number;
    uniqueProducts: number;
    scrapedProducts: number;
    databaseProducts: number;
  } {
    const cart = this.getCartFromStorage();
    
    const scrapedProducts = cart.items.filter(item => item.source === 'scraped').length;
    const databaseProducts = cart.items.filter(item => item.source === 'database').length;
    
    return {
      totalItems: cart.totalItems,
      totalPrice: cart.totalPrice,
      uniqueProducts: cart.items.length,
      scrapedProducts,
      databaseProducts
    };
  }

  // Exporter le panier (pour sauvegarde ou partage)
  exportCart(): string {
    const cart = this.getCartFromStorage();
    return JSON.stringify(cart, null, 2);
  }

  // Importer un panier (pour restauration)
  importCart(cartData: string): boolean {
    try {
      const cart = JSON.parse(cartData);
      this.saveCartToStorage(cart);
      console.log('📥 Panier importé avec succès');
      return true;
    } catch (error) {
      console.error('❌ Erreur lors de l\'import du panier:', error);
      return false;
    }
  }

  // Obtenir les produits les plus ajoutés
  getMostAddedProducts(limit: number = 5): Array<{product: Product, totalQuantity: number}> {
    const cart = this.getCartFromStorage();
    
    // Grouper par produit et sommer les quantités
    const productMap = new Map<number, {product: Product, totalQuantity: number}>();
    
    cart.items.forEach(item => {
      const existing = productMap.get(item.product.id);
      if (existing) {
        existing.totalQuantity += item.quantity;
      } else {
        productMap.set(item.product.id, {
          product: item.product,
          totalQuantity: item.quantity
        });
      }
    });

    // Trier par quantité totale et retourner les premiers
    return Array.from(productMap.values())
      .sort((a, b) => b.totalQuantity - a.totalQuantity)
      .slice(0, limit);
  }

  // Obtenir les produits récemment ajoutés
  getRecentlyAddedProducts(limit: number = 5): CartItem[] {
    const cart = this.getCartFromStorage();
    return cart.items
      .sort((a, b) => new Date(b.addedAt).getTime() - new Date(a.addedAt).getTime())
      .slice(0, limit);
  }
}

export const cartService = new CartService();
export default cartService;




