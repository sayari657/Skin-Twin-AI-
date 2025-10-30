import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  Card,
  CardContent,
  CardMedia,
  IconButton,
  Chip,
  Divider,
  Alert,
  TextField,
  Badge,
} from '@mui/material';
import {
  ShoppingCart as CartIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  Remove as RemoveIcon,
  Clear as ClearIcon,
  ShoppingBag as BagIcon,
} from '@mui/icons-material';
import { cartService, Cart, CartItem } from '../services/cartService';
import { Product } from '../types';

interface CartModalProps {
  open: boolean;
  onClose: () => void;
}

const CartModal: React.FC<CartModalProps> = ({ open, onClose }) => {
  const [cart, setCart] = useState<Cart>(cartService.getCart());
  const [loading, setLoading] = useState(false);

  // Mettre à jour le panier quand la modal s'ouvre
  useEffect(() => {
    if (open) {
      setCart(cartService.getCart());
    }
  }, [open]);

  // Mettre à jour la quantité d'un produit
  const handleQuantityChange = (productId: number, newQuantity: number) => {
    const updatedCart = cartService.updateQuantity(productId, newQuantity);
    setCart(updatedCart);
  };

  // Supprimer un produit du panier
  const handleRemoveItem = (productId: number) => {
    const updatedCart = cartService.removeFromCart(productId);
    setCart(updatedCart);
  };

  // Vider le panier
  const handleClearCart = () => {
    const updatedCart = cartService.clearCart();
    setCart(updatedCart);
  };

  // Obtenir les statistiques du panier
  const stats = cartService.getCartStats();

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <CartIcon color="primary" />
          <Typography variant="h6">
            Mon Panier ({stats.totalItems} articles)
          </Typography>
          {stats.totalItems > 0 && (
            <Chip
              label={`${stats.totalPrice.toFixed(2)}€`}
              color="primary"
              size="small"
            />
          )}
        </Box>
      </DialogTitle>

      <DialogContent>
        {cart.items.length === 0 ? (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <BagIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" color="text.secondary" gutterBottom>
              Votre panier est vide
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Ajoutez des produits de soins de la peau à votre panier
            </Typography>
          </Box>
        ) : (
          <>
            {/* Statistiques du panier */}
            <Box sx={{ mb: 3, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
              <Typography variant="h6" gutterBottom>
                📊 Résumé du panier
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Chip label={`${stats.uniqueProducts} produits uniques`} size="small" />
                <Chip label={`${stats.scrapedProducts} web`} size="small" color="primary" />
                <Chip label={`${stats.databaseProducts} base de données`} size="small" color="secondary" />
              </Box>
            </Box>

            {/* Liste des produits */}
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {cart.items.map((item: CartItem) => (
                <Card key={item.product.id} sx={{ display: 'flex' }}>
                  {/* Image du produit */}
                  {item.product.image && (
                    <CardMedia
                      component="img"
                      sx={{ width: 100, height: 100, objectFit: 'cover' }}
                      image={item.product.image}
                      alt={item.product.name}
                    />
                  )}

                  <CardContent sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                    {/* En-tête du produit */}
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                      <Box>
                        <Typography variant="h6" component="h3" gutterBottom>
                          {item.product.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          {item.product.brand}
                        </Typography>
                      </Box>
                      <Box sx={{ display: 'flex', gap: 1 }}>
                        <Chip
                          label={item.source === 'scraped' ? '🌐 Web' : '📦 BDD'}
                          size="small"
                          color={item.source === 'scraped' ? 'primary' : 'secondary'}
                          variant="outlined"
                        />
                        <IconButton
                          onClick={() => handleRemoveItem(item.product.id)}
                          color="error"
                          size="small"
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Box>
                    </Box>

                    {/* Prix et quantité */}
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 'auto' }}>
                      <Typography variant="h6" color="primary">
                        {(item.product.price || 0) * item.quantity}€
                      </Typography>
                      
                      {/* Contrôles de quantité */}
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <IconButton
                          onClick={() => handleQuantityChange(item.product.id, item.quantity - 1)}
                          disabled={item.quantity <= 1}
                          size="small"
                        >
                          <RemoveIcon />
                        </IconButton>
                        
                        <TextField
                          value={item.quantity}
                          onChange={(e) => {
                            const newQuantity = parseInt(e.target.value) || 1;
                            handleQuantityChange(item.product.id, newQuantity);
                          }}
                          inputProps={{ 
                            min: 1, 
                            style: { textAlign: 'center', width: '60px' } 
                          }}
                          size="small"
                          type="number"
                        />
                        
                        <IconButton
                          onClick={() => handleQuantityChange(item.product.id, item.quantity + 1)}
                          size="small"
                        >
                          <AddIcon />
                        </IconButton>
                      </Box>
                    </Box>

                    {/* Informations supplémentaires */}
                    <Box sx={{ mt: 1 }}>
                      <Typography variant="caption" color="text.secondary">
                        Prix unitaire: {item.product.price}€
                      </Typography>
                      {item.product.size && (
                        <Typography variant="caption" color="text.secondary" sx={{ ml: 2 }}>
                          Taille: {item.product.size}
                        </Typography>
                      )}
                    </Box>
                  </CardContent>
                </Card>
              ))}
            </Box>

            <Divider sx={{ my: 3 }} />

            {/* Total du panier */}
            <Box sx={{ 
              p: 2, 
              bgcolor: 'primary.light', 
              borderRadius: 1,
              textAlign: 'center'
            }}>
              <Typography variant="h5" color="primary.contrastText" gutterBottom>
                Total: {stats.totalPrice.toFixed(2)}€
              </Typography>
              <Typography variant="body2" color="primary.contrastText">
                {stats.totalItems} articles • {stats.uniqueProducts} produits uniques
              </Typography>
            </Box>
          </>
        )}
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>
          {cart.items.length === 0 ? 'Fermer' : 'Continuer mes achats'}
        </Button>
        
        {cart.items.length > 0 && (
          <>
            <Button
              onClick={handleClearCart}
              color="error"
              startIcon={<ClearIcon />}
            >
              Vider le panier
            </Button>
            <Button
              variant="contained"
              startIcon={<CartIcon />}
              onClick={() => {
                // TODO: Implémenter le processus de commande
                console.log('Commande en cours...', cart);
                alert('Fonctionnalité de commande en cours de développement !');
              }}
            >
              Commander ({stats.totalPrice.toFixed(2)}€)
            </Button>
          </>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default CartModal;
