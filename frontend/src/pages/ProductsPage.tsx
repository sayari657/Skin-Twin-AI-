import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Chip,
  Alert,
  LinearProgress,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CardMedia,
  Rating,
  CircularProgress,
  Snackbar,
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  ShoppingCart as CartIcon,
  Star as StarIcon,
  Save as SaveIcon,
  Psychology as AIIcon,
} from '@mui/icons-material';
import { apiService } from '../services/api';
import { realScrapingService } from '../services/realScrapingService';
import { Product } from '../types';
import ProductOrderModal from '../components/ProductOrderModal';
import CartModal from '../components/CartModal';
import AvatarCircleAI from '../components/AvatarCircleAI';
import ChatAI from '../components/ChatAI';
import { cartService } from '../services/cartService';

const ProductsPage: React.FC = () => {
  const navigate = useNavigate();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [skinTypeFilter, setSkinTypeFilter] = useState('');
  const [orderModalOpen, setOrderModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [cartModalOpen, setCartModalOpen] = useState(false);
  const [cartItemsCount, setCartItemsCount] = useState(0);
  const [user, setUser] = useState<any>(null);
  const [avatarStatus, setAvatarStatus] = useState<'online' | 'offline' | 'active' | 'story' | 'ai-thinking'>('online');
  const [isAITalking, setIsAITalking] = useState(false);
  const [chatPosition, setChatPosition] = useState({ x: window.innerWidth - 100, y: window.innerHeight - 100 });
  const [chatOpen, setChatOpen] = useState(false);
  const [chatInitialMessage, setChatInitialMessage] = useState<string | undefined>(undefined);
  const [chatFillInput, setChatFillInput] = useState<string | undefined>(undefined);
  const [isVoiceMode, setIsVoiceMode] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');

  useEffect(() => {
    loadProducts();
    updateCartCount();
    loadUserProfile();
  }, []);

  const loadUserProfile = async () => {
    try {
      const response = await apiService.getProfile();
      setUser(response.data);
    } catch (error) {
      console.error('Erreur lors du chargement du profil:', error);
    }
  };

  // Mettre à jour le compteur du panier
  const updateCartCount = () => {
    const cart = cartService.getCart();
    setCartItemsCount(cart.totalItems);
  };

  const loadProducts = async () => {
    try {
      setLoading(true);
      setError(null);
      
      console.log('📦 Chargement des produits de la base de données...');
      const response = await apiService.getProducts();
      setProducts(response.data);
    } catch (err: any) {
      console.error('Erreur lors du chargement des produits:', err);
      setError('Erreur lors du chargement des produits');
    } finally {
      setLoading(false);
    }
  };

  const getCategoryLabel = (category: string) => {
    const labels: { [key: string]: string } = {
      'CLEANSER': 'Nettoyant',
      'MOISTURIZER': 'Hydratant',
      'SERUM': 'Sérum',
      'SUNSCREEN': 'Crème solaire',
      'TREATMENT': 'Traitement',
      'MASK': 'Masque',
      'TONER': 'Tonique',
      'EXFOLIANT': 'Exfoliant',
    };
    return labels[category] || category;
  };

  const getSkinTypeLabel = (skinType: string) => {
    const labels: { [key: string]: string } = {
      'DRY': 'Sèche',
      'OILY': 'Grasse',
      'COMBINATION': 'Mixte',
      'NORMAL': 'Normale',
      'SENSITIVE': 'Sensible',
    };
    return labels[skinType] || skinType;
  };

  const handleAIConversation = () => {
    setIsAITalking(true);
    setAvatarStatus('ai-thinking');
    
    const aiMessage = '🛍️ Je peux vous aider à trouver les meilleurs produits pour votre peau ! Dites-moi votre type de peau (sèche, grasse, mixte, normale, sensible) et vos problèmes spécifiques (acné, rides, taches, etc.) pour des recommandations personnalisées.';
    
    setTimeout(() => {
      setAvatarStatus('active');
      setChatFillInput(aiMessage);
      setChatOpen(true);
      setIsVoiceMode(true);
      setSnackbarMessage('🎤 Mode vocal activé ! Parlez maintenant, votre message sera automatiquement rempli dans le chat.');
      setSnackbarOpen(true);
    }, 2000);

    setTimeout(() => {
      setIsAITalking(false);
      setAvatarStatus('online');
    }, 5000);
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  // Fonction de recherche
  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      await loadProducts();
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // Recherche dans la base de données locale
      const response = await apiService.getProducts();
      const filteredProducts = response.data.filter(product =>
        product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.brand.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setProducts(filteredProducts);
    } catch (err: any) {
      console.error('Erreur lors de la recherche:', err);
      setError('Erreur lors de la recherche');
    } finally {
      setLoading(false);
    }
  };


  // Fonction pour ouvrir la modal de commande
  const handleOrderProduct = (product: Product) => {
    setSelectedProduct(product);
    setOrderModalOpen(true);
  };

  // Fonction pour fermer la modal de commande
  const handleCloseOrderModal = () => {
    setOrderModalOpen(false);
    setSelectedProduct(null);
  };

  // Fonction pour ajouter un produit au panier
  const handleAddToCart = (product: Product) => {
    const source = 'database';
    cartService.addToCart(product, 1, source);
    updateCartCount();
    console.log(`🛒 Produit ajouté au panier: ${product.name}`);
  };

  // Fonction pour ouvrir la modal du panier
  const handleOpenCart = () => {
    setCartModalOpen(true);
  };

  // Fonction pour fermer la modal du panier
  const handleCloseCart = () => {
    setCartModalOpen(false);
    updateCartCount(); // Mettre à jour le compteur après fermeture
  };


  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.brand.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = !categoryFilter || product.category === categoryFilter;
    const matchesSkinType = !skinTypeFilter || product.target_skin_types.includes(skinTypeFilter);
    
    return matchesSearch && matchesCategory && matchesSkinType;
  });

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2, textAlign: 'center' }}>
          Chargement des produits...
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* En-tête avec Avatar Circle AI */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 3, mb: 4 }}>
        <AvatarCircleAI
          src={user?.profile_picture}
          name={user?.first_name || user?.username || 'Utilisateur'}
          status={avatarStatus}
          size={100}
          showStatus={true}
          showName={true}
          aiEnabled={true}
          isThinking={isAITalking}
          onStatusChange={setAvatarStatus}
        />
        <Box sx={{ flex: 1 }}>
          <Button
            startIcon={<BackIcon />}
            onClick={() => navigate('/dashboard')}
            sx={{ mb: 2 }}
          >
            Retour
          </Button>
          <Typography variant="h4" gutterBottom>
            🛍️ Produits Recommandés
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
            Votre assistant IA Skin Twin peut vous recommander les meilleurs produits
          </Typography>
          <Button
            variant="contained"
            startIcon={<AIIcon />}
            onClick={handleAIConversation}
            disabled={isAITalking}
            size="medium"
            sx={{
              background: 'linear-gradient(45deg, #2196F3, #21CBF3)',
              '&:hover': {
                background: 'linear-gradient(45deg, #1976D2, #1CB5E0)',
                transform: 'scale(1.05)',
              },
              transition: 'all 0.3s ease',
              boxShadow: '0 4px 15px rgba(33, 150, 243, 0.3)',
            }}
          >
            {isAITalking ? '🤖 IA en réflexion...' : '🎤 Parler à l\'IA (Mode vocal)'}
          </Button>
        </Box>
      </Box>
        

          {/* Bouton du panier */}
          <Box sx={{ mt: 2, display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
            <Button
              variant="outlined"
              onClick={handleOpenCart}
              startIcon={<CartIcon />}
              sx={{ position: 'relative' }}
            >
              Panier
              {cartItemsCount > 0 && (
                <Chip
                  label={cartItemsCount}
                  size="small"
                  color="primary"
                  sx={{ 
                    position: 'absolute', 
                    top: -8, 
                    right: -8,
                    minWidth: 20,
                    height: 20,
                    fontSize: '0.75rem'
                  }}
                />
              )}
            </Button>
          </Box>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}


          {/* Filtres */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🔍 Filtres
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 2, alignItems: 'center' }}>
                <Box sx={{ flex: { xs: '1', sm: '1' } }}>
                  <TextField
                    fullWidth
                    label="Rechercher"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                    InputProps={{
                      startAdornment: <SearchIcon color="action" />,
                    }}
                  />
                </Box>
                <Button
                  variant="contained"
                  onClick={handleSearch}
                  startIcon={<SearchIcon />}
                  sx={{ ml: 1 }}
                >
                  Rechercher
                </Button>
                <Box sx={{ flex: { xs: '1', sm: '1' } }}>
                  <FormControl fullWidth>
                    <InputLabel>Catégorie</InputLabel>
                    <Select
                      value={categoryFilter}
                      onChange={(e) => setCategoryFilter(e.target.value)}
                    >
                      <MenuItem value="">Toutes les catégories</MenuItem>
                      <MenuItem value="CLEANSER">Nettoyant</MenuItem>
                      <MenuItem value="MOISTURIZER">Hydratant</MenuItem>
                      <MenuItem value="SERUM">Sérum</MenuItem>
                      <MenuItem value="SUNSCREEN">Crème solaire</MenuItem>
                      <MenuItem value="TREATMENT">Traitement</MenuItem>
                      <MenuItem value="MASK">Masque</MenuItem>
                      <MenuItem value="TONER">Tonique</MenuItem>
                      <MenuItem value="EXFOLIANT">Exfoliant</MenuItem>
                    </Select>
                  </FormControl>
                </Box>
                <Box sx={{ flex: { xs: '1', sm: '1' } }}>
                  <FormControl fullWidth>
                    <InputLabel>Type de peau</InputLabel>
                    <Select
                      value={skinTypeFilter}
                      onChange={(e) => setSkinTypeFilter(e.target.value)}
                    >
                      <MenuItem value="">Tous les types</MenuItem>
                      <MenuItem value="DRY">Sèche</MenuItem>
                      <MenuItem value="OILY">Grasse</MenuItem>
                      <MenuItem value="COMBINATION">Mixte</MenuItem>
                      <MenuItem value="NORMAL">Normale</MenuItem>
                      <MenuItem value="SENSITIVE">Sensible</MenuItem>
                    </Select>
                  </FormControl>
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Produits */}
          {filteredProducts.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 8 }}>
              <CartIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
              <Typography variant="h6" color="text.secondary" gutterBottom>
                Aucun produit trouvé
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Essayez de modifier vos filtres de recherche.
              </Typography>
            </Box>
          ) : (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
              {filteredProducts.map((product) => (
                <Box sx={{ flex: { xs: '1 1 100%', sm: '1 1 calc(50% - 12px)', md: '1 1 calc(33.333% - 16px)' }, minWidth: 0 }} key={product.id}>
                  <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                    {product.image && (
                      <CardMedia
                        component="img"
                        height="200"
                        image={product.image}
                        alt={product.name}
                        sx={{ objectFit: 'cover' }}
                      />
                    )}
                    <CardContent sx={{ flexGrow: 1 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                        <Typography variant="h6" component="h3" gutterBottom>
                          {product.name}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          <Chip
                            label={getCategoryLabel(product.category)}
                            color="primary"
                            size="small"
                          />
                        </Box>
                      </Box>
                      
                      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                        {product.brand}
                      </Typography>

                      <Typography variant="body2" color="text.secondary" paragraph>
                        {product.description.length > 100 
                          ? `${product.description.substring(0, 100)}...` 
                          : product.description
                        }
                      </Typography>

                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Types de peau:
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                          {product.target_skin_types.map((skinType, index) => (
                            <Chip
                              key={index}
                              label={getSkinTypeLabel(skinType)}
                              size="small"
                              variant="outlined"
                            />
                          ))}
                        </Box>
                      </Box>

                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Problèmes ciblés:
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                          {product.target_issues.map((issue, index) => (
                            <Chip
                              key={index}
                              label={issue.replace('_', ' ')}
                              size="small"
                              color="secondary"
                              variant="outlined"
                            />
                          ))}
                        </Box>
                      </Box>

                      {product.price && (
                        <Typography variant="h6" color="primary" gutterBottom>
                          {product.price}€
                          {product.size && (
                            <Typography component="span" variant="body2" color="text.secondary">
                              {' '}/ {product.size}
                            </Typography>
                          )}
                        </Typography>
                      )}
                    </CardContent>
                    
                    <Box sx={{ p: 2, pt: 0, display: 'flex', gap: 1 }}>
                      {/* Bouton d'ajout au panier */}
                      <Button
                        variant="outlined"
                        startIcon={<CartIcon />}
                        onClick={() => handleAddToCart(product)}
                        sx={{ flex: 1 }}
                      >
                        Ajouter au panier
                      </Button>
                      
                      {/* Bouton d'achat/commande */}
                      <Button
                        variant="contained"
                        onClick={() => {
                          if ((product as any).url) {
                            // Pour les produits scrapés, rediriger vers l'URL externe
                            window.open((product as any).url, '_blank');
                          } else {
                            // Pour les produits de la base de données, ouvrir la modal de commande
                            handleOrderProduct(product);
                          }
                        }}
                        sx={{ flex: 1 }}
                      >
                        {(product as any).url ? '🛒 Acheter' : '🛒 Commander'}
                      </Button>
                    </Box>
                  </Card>
                </Box>
              ))}
            </Box>
          )}

          {/* Modal de commande */}
          <ProductOrderModal
            open={orderModalOpen}
            onClose={handleCloseOrderModal}
            product={selectedProduct}
          />

          {/* Modal du panier */}
          <CartModal
            open={cartModalOpen}
            onClose={handleCloseCart}
          />


      {/* Snackbar pour les notifications */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={4000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert 
          onClose={handleCloseSnackbar} 
          severity="success" 
          sx={{ width: '100%' }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>

      {/* Chat IA Intelligent */}
      <ChatAI
        position={chatPosition}
        onPositionChange={setChatPosition}
        isOpen={chatOpen}
        onOpenChange={setChatOpen}
        initialMessage={chatInitialMessage}
        fillInputWithMessage={chatFillInput}
        isVoiceMode={isVoiceMode}
        onVoiceModeChange={setIsVoiceMode}
      />
    </Container>
  );
};

export default ProductsPage;




