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
  MedicalServices as MedicalIcon,
} from '@mui/icons-material';
import { apiService } from '../services/api';

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [mobileMenuAnchor, setMobileMenuAnchor] = useState<null | HTMLElement>(null);

  const isAuthenticated = apiService.isAuthenticated();
  const isHomePage = location.pathname === '/';
  
  // Debug logs
  console.log('Navbar - État d\'authentification:', {
    isAuthenticated,
    accessToken: localStorage.getItem('access_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    currentPath: location.pathname
  });

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
        console.log('Navbar - Clic sur profil, navigation vers /profile');
        console.log('Navbar - Tokens avant navigation:', {
          accessToken: localStorage.getItem('access_token'),
          refreshToken: localStorage.getItem('refresh_token')
        });
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
      sx={{ 
        bgcolor: isHomePage ? 'transparent' : 'primary.main',
        boxShadow: isHomePage ? 'none' : 1,
      }}
    >
      <Toolbar>
        <Typography
          variant="h6"
          component={RouterLink}
          to="/"
          sx={{
            flexGrow: 1,
            textDecoration: 'none',
            color: 'inherit',
            fontWeight: 'bold',
            fontSize: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: 1,
          }}
        >
          <MedicalIcon sx={{ fontSize: '1.8rem' }} />
          Skin Twin AI
        </Typography>

        {isAuthenticated ? (
          <>
            {/* Desktop Menu */}
            <Box sx={{ display: { xs: 'none', md: 'flex' }, alignItems: 'center', gap: 1 }}>
              {menuItems.map((item) => (
                <Button
                  key={item.path}
                  component={RouterLink}
                  to={item.path}
                  color="inherit"
                  startIcon={item.icon}
                  sx={{
                    color: isHomePage ? 'white' : 'inherit',
                    '&:hover': {
                      bgcolor: isHomePage ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.1)',
                    },
                  }}
                >
                  {item.label}
                </Button>
              ))}
              <IconButton
                size="large"
                edge="end"
                aria-label="compte"
                aria-controls="profile-menu"
                aria-haspopup="true"
                onClick={handleProfileMenuOpen}
                color="inherit"
              >
                <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
                  <AccountCircle />
                </Avatar>
              </IconButton>
            </Box>

            {/* Mobile Menu */}
            <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
              <IconButton
                size="large"
                aria-label="menu"
                aria-controls="mobile-menu"
                aria-haspopup="true"
                onClick={handleMobileMenuOpen}
                color="inherit"
              >
                <MenuIcon />
              </IconButton>
            </Box>
          </>
        ) : (
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              component={RouterLink}
              to="/login"
              color="inherit"
              sx={{
                color: isHomePage ? 'white' : 'inherit',
                borderColor: isHomePage ? 'white' : 'inherit',
                '&:hover': {
                  bgcolor: isHomePage ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.1)',
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
                bgcolor: isHomePage ? 'white' : 'secondary.main',
                color: isHomePage ? 'primary.main' : 'white',
                '&:hover': {
                  bgcolor: isHomePage ? 'grey.100' : 'secondary.dark',
                },
              }}
            >
              S'inscrire
            </Button>
          </Box>
        )}

        {renderMobileMenu}
        {renderProfileMenu}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;




