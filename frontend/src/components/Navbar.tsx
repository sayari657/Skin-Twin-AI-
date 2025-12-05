import React, { useState } from 'react';
import { Link as RouterLink, useNavigate, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Box,
  Avatar,
  Divider,
  Container,
} from '@mui/material';
import {
  Menu as MenuIcon,
  AccountCircle,
  Dashboard as DashboardIcon,
  CameraAlt as CameraIcon,
  History as HistoryIcon,
  Person as PersonIcon,
  ShoppingCart as ProductIcon,
  Logout as LogoutIcon,
  Home as HomeIcon,
  Search as SearchIcon,
  Language as LanguageIcon,
} from '@mui/icons-material';
import { apiService } from '../services/api';

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [mobileMenuAnchor, setMobileMenuAnchor] = useState<null | HTMLElement>(null);

  const isAuthenticated = apiService.isAuthenticated();
  const isHomePage = location.pathname === '/';

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMobileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setMobileMenuAnchor(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setMobileMenuAnchor(null);
  };

  const handleLogout = async () => {
    await apiService.logout();
    navigate('/');
    handleMenuClose();
  };

  const menuItems = [
    { label: 'Tableau de bord', path: '/dashboard', icon: <DashboardIcon /> },
    { label: 'Analyser ma peau', path: '/upload', icon: <CameraIcon /> },
    { label: 'Historique', path: '/history', icon: <HistoryIcon /> },
    { label: 'Produits', path: '/products', icon: <ProductIcon /> },
  ];

  const renderMobileMenu = (
    <Menu
      anchorEl={mobileMenuAnchor}
      anchorOrigin={{
        vertical: 'top',
        horizontal: 'right',
      }}
      keepMounted
      transformOrigin={{
        vertical: 'top',
        horizontal: 'right',
      }}
      open={Boolean(mobileMenuAnchor)}
      onClose={handleMenuClose}
    >
      {isAuthenticated ? [
        ...menuItems.map((item) => (
          <MenuItem
            key={item.path}
            onClick={() => {
              navigate(item.path);
              handleMenuClose();
            }}
          >
            {item.icon}
            <Box sx={{ ml: 1 }}>{item.label}</Box>
          </MenuItem>
        )),
        <Divider key="divider" />,
        <MenuItem key="profile" onClick={handleProfileMenuOpen}>
          <PersonIcon />
          <Box sx={{ ml: 1 }}>Profil</Box>
        </MenuItem>,
        <MenuItem key="logout" onClick={handleLogout}>
          <LogoutIcon />
          <Box sx={{ ml: 1 }}>Déconnexion</Box>
        </MenuItem>
      ] : [
        <MenuItem key="login" onClick={() => navigate('/login')}>
          Se connecter
        </MenuItem>,
        <MenuItem key="register" onClick={() => navigate('/register')}>
          S'inscrire
        </MenuItem>
      ]}
    </Menu>
  );

  const renderProfileMenu = (
    <Menu
      anchorEl={anchorEl}
      anchorOrigin={{
        vertical: 'top',
        horizontal: 'right',
      }}
      keepMounted
      transformOrigin={{
        vertical: 'top',
        horizontal: 'right',
      }}
      open={Boolean(anchorEl)}
      onClose={handleMenuClose}
    >
      <MenuItem onClick={() => { 
        navigate('/profile'); 
        handleMenuClose(); 
      }}>
        <PersonIcon sx={{ mr: 1 }} />
        Mon profil
      </MenuItem>
      <MenuItem onClick={handleLogout}>
        <LogoutIcon sx={{ mr: 1 }} />
        Déconnexion
      </MenuItem>
    </Menu>
  );

  return (
    <AppBar 
      position="static" 
      elevation={0}
      sx={{ 
        bgcolor: '#424242', // Gris foncé
        borderBottom: '1px solid rgba(255,255,255,0.1)',
        boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
      }}
    >
      <Container maxWidth="lg">
        <Toolbar sx={{ py: 2, px: 0 }}>
          {/* Logo */}
          <Typography
            variant="h6"
            component={RouterLink}
            to="/"
            sx={{
              textDecoration: 'none',
              fontWeight: 700,
              fontSize: '1.5rem',
              display: 'flex',
              alignItems: 'center',
              mr: 4,
              color: '#FFFFFF',
            }}
          >
            <Box
              component="span"
              sx={{
                color: '#D4A574', // Beige
                fontWeight: 400,
              }}
            >
              SKIN-
            </Box>
            <Box
              component="span"
              sx={{
                color: '#FFFFFF',
                fontWeight: 700,
              }}
            >
              TWIN
            </Box>
          </Typography>

          {/* Main Navigation - Desktop */}
          {isAuthenticated && (
            <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1, flexGrow: 1 }}>
              {menuItems.map((item) => (
                <Button
                  key={item.path}
                  component={RouterLink}
                  to={item.path}
                  sx={{
                    color: '#FFFFFF',
                    fontWeight: 500,
                    fontSize: '0.95rem',
                    textTransform: 'none',
                    '&:hover': {
                      bgcolor: 'rgba(255,255,255,0.1)',
                      color: '#D4A574', // Beige au survol
                    },
                  }}
                >
                  {item.label}
                </Button>
              ))}
            </Box>
          )}

          {/* Utility Links - Desktop */}
          <Box sx={{ display: { xs: 'none', md: 'flex' }, alignItems: 'center', gap: 2, ml: 'auto' }}>
            <IconButton
              size="small"
              sx={{
                color: '#FFFFFF',
                '&:hover': {
                  bgcolor: 'rgba(255,255,255,0.1)',
                },
              }}
            >
              <SearchIcon />
            </IconButton>
            
            {!isAuthenticated ? (
              <>
                <Button
                  component={RouterLink}
                  to="/login"
                  sx={{
                    color: '#FFFFFF',
                    fontWeight: 500,
                    textTransform: 'none',
                    '&:hover': {
                      bgcolor: 'rgba(255,255,255,0.1)',
                    },
                  }}
                >
                  Se connecter
                </Button>
                <Button
                  component={RouterLink}
                  to="/register"
                  variant="contained"
                  sx={{
                    bgcolor: '#C2185B', // Rose foncée
                    color: 'white',
                    fontWeight: 500,
                    textTransform: 'none',
                    px: 3,
                    display: 'none', // Rendu invisible
                    '&:hover': {
                      bgcolor: '#880E4F',
                    },
                  }}
                >
                  CONTACTS BUSINESS
                </Button>
              </>
            ) : (
              <>
                <IconButton
                  size="large"
                  edge="end"
                  aria-label="compte"
                  aria-controls="profile-menu"
                  aria-haspopup="true"
                  onClick={handleProfileMenuOpen}
                  sx={{ color: '#FFFFFF' }}
                >
                  <Avatar sx={{ width: 32, height: 32, bgcolor: '#C2185B' }}>
                    <AccountCircle />
                  </Avatar>
                </IconButton>
              </>
            )}
            
            <IconButton
              size="small"
              sx={{
                color: '#FFFFFF',
                display: 'none', // Rendu invisible
                '&:hover': {
                  bgcolor: 'rgba(255,255,255,0.1)',
                },
              }}
            >
              <LanguageIcon />
            </IconButton>
            <Typography variant="body2" sx={{ color: '#FFFFFF', fontSize: '0.875rem', display: 'none' }}>
              Français
            </Typography>
          </Box>

          {/* Mobile Menu */}
          <Box sx={{ display: { xs: 'flex', md: 'none' }, ml: 'auto' }}>
            <IconButton
              size="large"
              aria-label="menu"
              aria-controls="mobile-menu"
              aria-haspopup="true"
              onClick={handleMobileMenuOpen}
              sx={{ color: '#FFFFFF' }}
            >
              <MenuIcon />
            </IconButton>
          </Box>

          {renderMobileMenu}
          {renderProfileMenu}
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;
