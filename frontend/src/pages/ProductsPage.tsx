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
  FormControlLabel as MuiFormControlLabel,
  Checkbox as MuiCheckbox,
} from '@mui/material';
import {
  ArrowBack as BackIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  ShoppingCart as CartIcon,
  Star as StarIcon,
  Save as SaveIcon,
  Psychology as AIIcon,
  Web as WebIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { apiService } from '../services/api';
import { realScrapingService } from '../services/realScrapingService';
import { webScrapingService } from '../services/webScrapingService';
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
  const [scrapingUrl, setScrapingUrl] = useState('');
  const [scrapingQuery, setScrapingQuery] = useState('');
  const [scrapingSource, setScrapingSource] = useState('pharma-shop.tn');
  const [scrapingMaxPages, setScrapingMaxPages] = useState(20);  // Réduire à 20 pages par défaut pour éviter les timeouts
  const [isScraping, setIsScraping] = useState(false);
  const [scrapedProducts, setScrapedProducts] = useState<Product[]>([]);
  const [scrapingProgress, setScrapingProgress] = useState({ current: 0, total: 0 });
  const [autoSave, setAutoSave] = useState(true);  // Sauvegarder automatiquement par défaut
  const [productsStats, setProductsStats] = useState<any>(null);  // Statistiques des produits

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
      
      // Gérer le nouveau format avec stats ou l'ancien format (liste directe)
      const responseData = response.data as any;
      
      if (responseData.products && Array.isArray(responseData.products)) {
        // Nouveau format avec stats
        setProducts(responseData.products);
        setProductsStats(responseData.stats);
        console.log('📊 Statistiques des produits:', responseData.stats);
        if (responseData.stats) {
          console.log(`   - Total: ${responseData.stats.total}`);
          console.log(`   - De la base: ${responseData.stats.from_database}`);
          console.log(`   - Scrapés actifs: ${responseData.stats.scraped_active}`);
          console.log(`   - Scrapés total: ${responseData.stats.scraped_total}`);
          console.log(`   - Scrapés inactifs: ${responseData.stats.scraped_inactive}`);
          
          // Afficher un message si le nombre de produits scrapés ne correspond pas
          if (responseData.stats.scraped_total > 0 && responseData.stats.scraped_active < responseData.stats.scraped_total) {
            console.warn(`⚠️ Attention: ${responseData.stats.scraped_inactive} produits scrapés sont inactifs (is_active=False)`);
          }
        }
      } else if (Array.isArray(responseData)) {
        // Ancien format (liste directe)
        setProducts(responseData);
        setProductsStats(null);
        console.log(`📦 ${responseData.length} produits chargés depuis la base de données`);
      } else {
        console.error('Format de réponse inattendu:', responseData);
        setError('Format de réponse inattendu du serveur');
      }
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

  // Fonction pour scraper des produits depuis le web
  const handleScrapeWeb = async () => {
    if (!scrapingUrl && !scrapingQuery) {
      setSnackbarMessage('Veuillez entrer une URL ou un terme de recherche');
      setSnackbarOpen(true);
      return;
    }

    try {
      setIsScraping(true);
      setError(null);

      const response = await webScrapingService.scrapeWebProducts({
        url: scrapingUrl || undefined,
        search_query: scrapingQuery || undefined,
        source_site: scrapingSource,
        max_pages: scrapingMaxPages,
        auto_save: autoSave,  // Sauvegarder automatiquement
      });

      if (response.success && response.products.length > 0) {
        setScrapedProducts(response.products);
        // Ne pas ajouter directement aux produits, attendre le rechargement depuis la base de données
        
        if (response.total_saved !== undefined) {
          setSnackbarMessage(`✅ ${response.total_saved.toLocaleString()} produits sauvegardés sur ${response.total_found.toLocaleString()} trouvés dans la base de données !`);
        } else {
          setSnackbarMessage(`✅ ${response.total_found.toLocaleString()} produits scrapés avec succès !`);
        }
        setSnackbarOpen(true);
        setScrapingUrl('');
        setScrapingQuery('');
        
        // Recharger les produits depuis la base de données si auto_save était activé
        if (autoSave && response.total_saved) {
          console.log('🔄 Rechargement automatique des produits après scraping avec auto_save...');
          await loadProducts();
        }
      } else {
        // Gérer les erreurs
        const errorMessage = response.error || response.message || 'Aucun produit trouvé';
        setError(errorMessage);
        setSnackbarMessage(`❌ Erreur: ${errorMessage}`);
        setSnackbarOpen(true);
        console.error('Erreur lors du scraping:', errorMessage);
      }
    } catch (err: any) {
      console.error('Erreur lors du scraping:', err);
      const errorMessage = err.response?.data?.error || err.message || 'Erreur lors du scraping web';
      setError(errorMessage);
      setSnackbarMessage(`❌ Erreur: ${errorMessage}`);
      setSnackbarOpen(true);
    } finally {
      setIsScraping(false);
    }
  };

  // Fonction pour sauvegarder les produits scrapés
  const handleSaveScrapedProducts = async () => {
    if (scrapedProducts.length === 0) {
      setSnackbarMessage('Aucun produit à sauvegarder');
      setSnackbarOpen(true);
      return;
    }

    try {
      console.log(`💾 Tentative de sauvegarde de ${scrapedProducts.length} produits...`);
      
      const response = await webScrapingService.saveScrapedProducts(scrapedProducts);
      
      console.log('📥 Réponse de sauvegarde:', response);
      
      // Gérer la réponse améliorée avec updated_products
      const totalSaved = (response.saved_products || 0) + (response.updated_products || 0);
      const skipped = response.skipped_products || 0;
      
      let message = `✅ ${totalSaved.toLocaleString()} produit(s) sauvegardés`;
      if (response.updated_products > 0) {
        message += ` (${(response.saved_products || 0).toLocaleString()} nouveaux, ${response.updated_products.toLocaleString()} mis à jour)`;
      }
      if (skipped > 0) {
        message += `, ${skipped.toLocaleString()} ignoré(s)`;
      }
      
      setSnackbarMessage(message);
      setSnackbarOpen(true);
      setScrapedProducts([]);
      
      // Attendre un peu pour que la base de données soit à jour
      await new Promise(resolve => setTimeout(resolve, 1000)); // Augmenter à 1 seconde
      
      // Recharger les produits depuis la base de données
      console.log('🔄 Rechargement des produits après sauvegarde...');
      await loadProducts();
      
      // Afficher les erreurs s'il y en a
      if (response.errors && response.errors.length > 0) {
        console.warn('⚠️ Erreurs lors de la sauvegarde:', response.errors);
        setSnackbarMessage(`${message}. ⚠️ ${response.errors.length} erreur(s) détectée(s). Vérifiez la console.`);
        setSnackbarOpen(true);
      }
      
      // Vérifier si tous les produits ont été sauvegardés
      if (totalSaved < scrapedProducts.length) {
        console.warn(`⚠️ Seulement ${totalSaved} produits sauvegardés sur ${scrapedProducts.length} tentés`);
      }
    } catch (err: any) {
      console.error('❌ Erreur lors de la sauvegarde:', err);
      const errorMessage = err.response?.data?.error || err.message || 'Erreur lors de la sauvegarde des produits';
      setError(errorMessage);
      setSnackbarMessage(`❌ Erreur: ${errorMessage}`);
      setSnackbarOpen(true);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbarOpen(false);
  };

  // Fonction de recherche
  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      // Si la recherche est vide, recharger tous les produits
      await loadProducts();
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // Recherche dans la base de données locale (pas besoin de recharger depuis le serveur)
      // Les produits sont déjà chargés dans le state 'products'
      const filteredProducts = products.filter(product => {
        const searchLower = searchTerm.toLowerCase();
        return (
          product.name.toLowerCase().includes(searchLower) ||
          product.brand.toLowerCase().includes(searchLower) ||
          (product.description && product.description.toLowerCase().includes(searchLower))
        );
      });
      
      // Ne pas modifier 'products', juste utiliser filteredProducts pour l'affichage
      // Le filtrage se fait déjà dans le render avec filteredProducts
      console.log(`🔍 Recherche "${searchTerm}": ${filteredProducts.length} résultat(s) trouvé(s)`);
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


  // Filtrer les produits selon les critères de recherche
  const filteredProducts = products.filter(product => {
    // Filtre de recherche textuelle (ne s'applique que si searchTerm n'est pas vide)
    const matchesSearch = !searchTerm.trim() || 
      (product.name && product.name.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (product.brand && product.brand.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (product.description && product.description.toLowerCase().includes(searchTerm.toLowerCase()));
    
    // Filtre de catégorie (ne s'applique que si categoryFilter n'est pas vide)
    const matchesCategory = !categoryFilter || product.category === categoryFilter;
    
    // Filtre de type de peau (ne s'applique que si skinTypeFilter n'est pas vide)
    const matchesSkinType = !skinTypeFilter || 
      (product.target_skin_types && Array.isArray(product.target_skin_types) && product.target_skin_types.includes(skinTypeFilter));
    
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

          {/* Statistiques des produits */}
          {productsStats && (
            <Alert 
              severity={productsStats.scraped_total > productsStats.scraped_active ? "warning" : "info"} 
              sx={{ mb: 3 }}
            >
              <Typography variant="body2" fontWeight="bold" gutterBottom>
                📊 Statistiques de la base de données (mises à jour en temps réel) :
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                <Typography variant="body2">
                  • <strong>Total produits affichés :</strong> {productsStats.total.toLocaleString()}
                </Typography>
                {productsStats.from_database > 0 && (
                  <Typography variant="body2">
                    • <strong>Produits de la base de données :</strong> {productsStats.from_database.toLocaleString()}
                  </Typography>
                )}
                <Typography variant="body2">
                  • <strong>Produits scrapés actifs :</strong> {productsStats.scraped_active.toLocaleString()} / {productsStats.scraped_total.toLocaleString()} total
                </Typography>
                {productsStats.scraped_inactive > 0 && (
                  <Typography variant="body2" color="warning.main" sx={{ mt: 1 }}>
                    ⚠️ {productsStats.scraped_inactive.toLocaleString()} produit(s) scrapé(s) sont inactifs (is_active=False)
                  </Typography>
                )}
                {productsStats.scraped_total === 0 && (
                  <Typography variant="body2" color="error.main" sx={{ mt: 1 }}>
                    ❌ Aucun produit scrapé trouvé dans la base de données. Vérifiez que le scraping a bien sauvegardé les produits.
                  </Typography>
                )}
                {productsStats.scraped_active > 0 && (
                  <Typography variant="body2" color="success.main" sx={{ mt: 1, fontWeight: 'bold' }}>
                    ✅ {productsStats.scraped_active.toLocaleString()} produits scrapés disponibles et actifs !
                  </Typography>
                )}
              </Box>
            </Alert>
          )}

          {/* Section Scraping Web */}
          <Card sx={{ mb: 3, bgcolor: '#FFF5F8', border: '2px solid #C2185B' }}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: 600, color: '#C2185B', mb: 2 }}>
                Scraping Web - Scraper des produits depuis Internet
              </Typography>
              
              <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 2, mb: 2 }}>
                <TextField
                  fullWidth
                  label="URL du site (optionnel)"
                  value={scrapingUrl}
                  onChange={(e) => setScrapingUrl(e.target.value)}
                  placeholder="https://www.amazon.fr/s?k=soin+peau"
                  variant="outlined"
                />
                <TextField
                  fullWidth
                  label="Terme de recherche (optionnel)"
                  value={scrapingQuery}
                  onChange={(e) => setScrapingQuery(e.target.value)}
                  placeholder="crème hydratante visage"
                  variant="outlined"
                />
                <FormControl sx={{ minWidth: 150 }}>
                  <InputLabel>Source</InputLabel>
                  <Select
                    value={scrapingSource}
                    onChange={(e) => setScrapingSource(e.target.value)}
                    label="Source"
                  >
                    <MenuItem value="pharma-shop.tn">Pharma-Shop.tn</MenuItem>
                    <MenuItem value="amazon">Amazon</MenuItem>
                    <MenuItem value="sephora">Sephora</MenuItem>
                    <MenuItem value="nocibe">Nocibé</MenuItem>
                    <MenuItem value="unknown">Autre</MenuItem>
                  </Select>
                </FormControl>
                        {scrapingSource === 'pharma-shop.tn' && (
                          <TextField
                            type="number"
                            label="Nombre max de pages"
                            value={scrapingMaxPages}
                            onChange={(e) => setScrapingMaxPages(parseInt(e.target.value) || 1)}
                            inputProps={{ min: 1, max: 100 }}
                            sx={{ minWidth: 150 }}
                            helperText={`Recommandé: 10-20 pages (~${scrapingMaxPages * 24} produits max)`}
                          />
                        )}
              </Box>

              {/* Option de sauvegarde automatique */}
              <Box sx={{ mb: 2 }}>
                <MuiFormControlLabel
                  control={
                    <MuiCheckbox
                      checked={autoSave}
                      onChange={(e) => setAutoSave(e.target.checked)}
                      sx={{ color: '#C2185B' }}
                    />
                  }
                  label="Sauvegarder automatiquement dans la base de données pendant le scraping"
                />
              </Box>

              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Button
                  variant="contained"
                  startIcon={isScraping ? <CircularProgress size={20} color="inherit" /> : undefined}
                  onClick={handleScrapeWeb}
                  disabled={isScraping || (!scrapingUrl && !scrapingQuery)}
                  sx={{
                    bgcolor: '#C2185B',
                    '&:hover': {
                      bgcolor: '#880E4F',
                    },
                  }}
                >
                  {isScraping ? 'Scraping en cours...' : 'Scraper les produits'}
                </Button>
                
                {scrapedProducts.length > 0 && (
                  <Button
                    variant="outlined"
                    startIcon={<SaveIcon />}
                    onClick={handleSaveScrapedProducts}
                    sx={{
                      borderColor: '#C2185B',
                      color: '#C2185B',
                      '&:hover': {
                        borderColor: '#880E4F',
                        bgcolor: '#FFF5F8',
                      },
                    }}
                  >
                    Sauvegarder {scrapedProducts.length} produit(s)
                  </Button>
                )}
              </Box>

                      {isScraping && (
                        <Alert severity="info" sx={{ mt: 2 }}>
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                              <CircularProgress size={20} />
                              <Typography>
                                Scraping en cours... Cela peut prendre plusieurs minutes pour scraper {scrapingMaxPages} page(s).
                              </Typography>
                            </Box>
                            <Typography variant="body2" color="text.secondary">
                              ⏱️ Temps estimé : ~{Math.ceil(scrapingMaxPages * 2)} minutes ({scrapingMaxPages} pages × ~2 min/page)
                              <br />
                              💾 Les produits sont sauvegardés automatiquement au fur et à mesure.
                            </Typography>
                          </Box>
                        </Alert>
                      )}
              
              {scrapedProducts.length > 0 && !isScraping && (
                <Alert severity="success" sx={{ mt: 2 }}>
                  <Typography variant="body2" fontWeight="bold" gutterBottom>
                    ✅ {scrapedProducts.length} produit(s) scrapé(s) avec succès !
                  </Typography>
                  <Typography variant="body2">
                    Cliquez sur "Sauvegarder" pour les ajouter à la base de données.
                    {autoSave && (
                      <span> (Les produits sont déjà sauvegardés automatiquement pendant le scraping)</span>
                    )}
                  </Typography>
                </Alert>
              )}
            </CardContent>
          </Card>

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
          <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
            <Typography variant="h6" gutterBottom>
              📦 Produits ({filteredProducts.length.toLocaleString()} / {products.length.toLocaleString()} total)
            </Typography>
            {products.length > 0 && (
              <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}>
                <Typography variant="body2" color="text.secondary">
                  {products.filter(p => p.source_site).length.toLocaleString()} produit(s) scrapé(s) • {products.filter(p => !p.source_site).length.toLocaleString()} produit(s) de la base
                </Typography>
                <Button
                  variant="outlined"
                  size="small"
                  onClick={loadProducts}
                  startIcon={<RefreshIcon />}
                  sx={{ ml: 'auto' }}
                >
                  Actualiser
                </Button>
              </Box>
            )}
          </Box>
          
          {/* Message si des filtres sont actifs */}
          {(searchTerm.trim() || categoryFilter || skinTypeFilter) && filteredProducts.length < products.length && (
            <Alert severity="info" sx={{ mb: 2 }}>
              <Typography variant="body2">
                {products.length - filteredProducts.length} produit(s) masqué(s) par les filtres actifs.
                <Button 
                  size="small" 
                  onClick={() => {
                    setSearchTerm('');
                    setCategoryFilter('');
                    setSkinTypeFilter('');
                  }}
                  sx={{ ml: 1 }}
                >
                  Réinitialiser les filtres
                </Button>
              </Typography>
            </Alert>
          )}
          
          {/* Message si aucun produit n'est affiché */}
          {products.length === 0 && !loading && (
            <Alert severity="warning" sx={{ mb: 2 }}>
              <Typography variant="body2">
                Aucun produit trouvé dans la base de données. 
                {productsStats?.scraped_inactive > 0 && (
                  <span> Il y a {productsStats.scraped_inactive} produit(s) inactif(s) dans la base de données.</span>
                )}
              </Typography>
            </Alert>
          )}
          
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
                        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                          <Chip
                            label={getCategoryLabel(product.category)}
                            color="primary"
                            size="small"
                          />
                          {product.source_site && (
                            <Chip
                              label={`🌐 ${product.source_site}`}
                              size="small"
                              sx={{
                                bgcolor: '#FFF5F8',
                                color: '#C2185B',
                                border: '1px solid #C2185B',
                                fontSize: '0.7rem',
                              }}
                            />
                          )}
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
                          {product.price.toFixed(2)} {product.source_site === 'pharma-shop.tn' ? 'TND' : '€'}
                          {product.size && (
                            <Typography component="span" variant="body2" color="text.secondary">
                              {' '}/ {product.size}
                            </Typography>
                          )}
                        </Typography>
                      )}
                    </CardContent>
                    
                    <Box sx={{ p: 2, pt: 0, display: 'flex', flexDirection: 'column', gap: 1 }}>
                      {/* Lien vers le produit original si disponible */}
                      {product.url && (
                        <Button
                          variant="text"
                          size="small"
                          href={product.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          sx={{
                            color: '#C2185B',
                            textTransform: 'none',
                            fontSize: '0.75rem',
                            alignSelf: 'flex-start',
                          }}
                        >
                          Voir sur {product.source_site || 'le site'}
                        </Button>
                      )}
                      
                      <Box sx={{ display: 'flex', gap: 1 }}>
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




