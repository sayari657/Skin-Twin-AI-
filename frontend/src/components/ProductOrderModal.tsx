import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Box,
  Typography,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Divider,
  Chip,
} from '@mui/material';
import {
  ShoppingCart as CartIcon,
  LocalShipping as ShippingIcon,
  Payment as PaymentIcon,
} from '@mui/icons-material';
import { Product } from '../types';

interface ProductOrderModalProps {
  open: boolean;
  onClose: () => void;
  product: Product | null;
}

interface OrderFormData {
  quantity: number;
  fullName: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  postalCode: string;
  country: string;
  paymentMethod: string;
  specialInstructions: string;
}

const ProductOrderModal: React.FC<ProductOrderModalProps> = ({
  open,
  onClose,
  product,
}) => {
  const [formData, setFormData] = useState<OrderFormData>({
    quantity: 1,
    fullName: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    postalCode: '',
    country: 'France',
    paymentMethod: 'card',
    specialInstructions: '',
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleInputChange = (field: keyof OrderFormData) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value,
    }));
  };

  const handleQuantityChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const quantity = parseInt(event.target.value) || 1;
    setFormData(prev => ({
      ...prev,
      quantity: Math.max(1, quantity),
    }));
  };

  const calculateTotal = () => {
    if (!product?.price) return 0;
    return product.price * formData.quantity;
  };

  const handleSubmit = async () => {
    if (!product) return;

    // Validation
    if (!formData.fullName || !formData.email || !formData.address) {
      setError('Veuillez remplir tous les champs obligatoires');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Simuler l'envoi de la commande
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      console.log('Commande créée:', {
        product: product.name,
        quantity: formData.quantity,
        total: calculateTotal(),
        customer: formData,
      });

      setSuccess(true);
      
      // Fermer la modal après 2 secondes
      setTimeout(() => {
        onClose();
        setSuccess(false);
        setFormData({
          quantity: 1,
          fullName: '',
          email: '',
          phone: '',
          address: '',
          city: '',
          postalCode: '',
          country: 'France',
          paymentMethod: 'card',
          specialInstructions: '',
        });
      }, 2000);

    } catch (err) {
      setError('Erreur lors de la création de la commande');
    } finally {
      setLoading(false);
    }
  };

  if (!product) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <CartIcon color="primary" />
          <Typography variant="h6">
            Commander: {product.name}
          </Typography>
        </Box>
      </DialogTitle>

      <DialogContent>
        {success ? (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography variant="h5" color="success.main" gutterBottom>
              ✅ Commande confirmée !
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Votre commande a été enregistrée avec succès. Vous recevrez un email de confirmation.
            </Typography>
          </Box>
        ) : (
          <>
            {/* Résumé du produit */}
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Box sx={{ display: 'flex', gap: 2 }}>
                  {product.image && (
                    <Box
                      component="img"
                      src={product.image}
                      alt={product.name}
                      sx={{
                        width: 80,
                        height: 80,
                        objectFit: 'cover',
                        borderRadius: 1,
                      }}
                    />
                  )}
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="h6" gutterBottom>
                      {product.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {product.brand}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
                      <Chip label={product.category} size="small" color="primary" />
                      {product.target_skin_types.map((type, index) => (
                        <Chip key={index} label={type} size="small" variant="outlined" />
                      ))}
                    </Box>
                    <Typography variant="h6" color="primary">
                      {product.price}€ / {product.size}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            {/* Formulaire de commande */}
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {/* Quantité */}
              <TextField
                label="Quantité"
                type="number"
                value={formData.quantity}
                onChange={handleQuantityChange}
                inputProps={{ min: 1 }}
                sx={{ width: 120 }}
              />

              <Divider />

              {/* Informations personnelles */}
              <Typography variant="h6" gutterBottom>
                <ShippingIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Informations de livraison
              </Typography>

              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  label="Nom complet *"
                  value={formData.fullName}
                  onChange={handleInputChange('fullName')}
                  fullWidth
                />
                <TextField
                  label="Email *"
                  type="email"
                  value={formData.email}
                  onChange={handleInputChange('email')}
                  fullWidth
                />
              </Box>

              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  label="Téléphone"
                  value={formData.phone}
                  onChange={handleInputChange('phone')}
                  fullWidth
                />
                <TextField
                  label="Pays"
                  value={formData.country}
                  onChange={handleInputChange('country')}
                  fullWidth
                />
              </Box>

              <TextField
                label="Adresse *"
                value={formData.address}
                onChange={handleInputChange('address')}
                fullWidth
                multiline
                rows={2}
              />

              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  label="Ville"
                  value={formData.city}
                  onChange={handleInputChange('city')}
                  fullWidth
                />
                <TextField
                  label="Code postal"
                  value={formData.postalCode}
                  onChange={handleInputChange('postalCode')}
                  fullWidth
                />
              </Box>

              <Divider />

              {/* Méthode de paiement */}
              <Typography variant="h6" gutterBottom>
                <PaymentIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Paiement
              </Typography>

              <TextField
                label="Méthode de paiement"
                value={formData.paymentMethod}
                onChange={handleInputChange('paymentMethod')}
                fullWidth
                helperText="Carte bancaire, PayPal, virement bancaire"
              />

              <TextField
                label="Instructions spéciales"
                value={formData.specialInstructions}
                onChange={handleInputChange('specialInstructions')}
                fullWidth
                multiline
                rows={2}
                helperText="Instructions pour la livraison (optionnel)"
              />

              {/* Total */}
              <Box sx={{ 
                p: 2, 
                bgcolor: 'primary.light', 
                borderRadius: 1,
                textAlign: 'center'
              }}>
                <Typography variant="h5" color="primary.contrastText">
                  Total: {calculateTotal().toFixed(2)}€
                </Typography>
                <Typography variant="body2" color="primary.contrastText">
                  {formData.quantity} × {product.price}€
                </Typography>
              </Box>
            </Box>
          </>
        )}
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} disabled={loading}>
          {success ? 'Fermer' : 'Annuler'}
        </Button>
        {!success && (
          <Button
            onClick={handleSubmit}
            variant="contained"
            disabled={loading}
            startIcon={loading ? <CircularProgress size={20} /> : <CartIcon />}
          >
            {loading ? 'Traitement...' : 'Confirmer la commande'}
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default ProductOrderModal;




