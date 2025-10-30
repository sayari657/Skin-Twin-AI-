import React, { useState, useEffect } from 'react';
import {
  Box,
  Avatar,
  Typography,
  Tooltip,
  Chip,
  Fade,
  Zoom,
  CircularProgress,
} from '@mui/material';
import {
  Circle as CircleIcon,
  Chat as ChatIcon,
  Wifi as WifiIcon,
  WifiOff as WifiOffIcon,
  Psychology as AIIcon,
  AutoAwesome as SparkleIcon,
} from '@mui/icons-material';

export type AvatarStatus = 'online' | 'offline' | 'active' | 'story' | 'ai-thinking';

interface AvatarCircleAIProps {
  src?: string;
  alt?: string;
  name?: string;
  status?: AvatarStatus;
  size?: number;
  showStatus?: boolean;
  showName?: boolean;
  aiEnabled?: boolean;
  isThinking?: boolean;
  onStatusChange?: (status: AvatarStatus) => void;
  className?: string;
}

const AvatarCircleAI: React.FC<AvatarCircleAIProps> = ({
  src,
  alt = 'Avatar',
  name = 'Utilisateur',
  status = 'offline',
  size = 80,
  showStatus = true,
  showName = true,
  aiEnabled = true,
  isThinking = false,
  onStatusChange,
  className = '',
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const [pulseAnimation, setPulseAnimation] = useState(false);

  // Animation de pulsation pour les statuts actifs
  useEffect(() => {
    if (status === 'active' || status === 'story' || isThinking) {
      const interval = setInterval(() => {
        setPulseAnimation(prev => !prev);
      }, 2000);
      return () => clearInterval(interval);
    }
  }, [status, isThinking]);

  // Couleurs et styles selon le statut
  const getStatusConfig = () => {
    switch (status) {
      case 'online':
        return {
          color: '#4CAF50',
          icon: <WifiIcon sx={{ fontSize: 12 }} />,
          label: 'En ligne',
          animation: 'pulse-green',
        };
      case 'offline':
        return {
          color: '#9E9E9E',
          icon: <WifiOffIcon sx={{ fontSize: 12 }} />,
          label: 'Hors ligne',
          animation: 'none',
        };
      case 'active':
        return {
          color: '#2196F3',
          icon: <ChatIcon sx={{ fontSize: 12 }} />,
          label: 'En conversation',
          animation: 'pulse-blue',
        };
      case 'story':
        return {
          color: 'linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4)',
          icon: <SparkleIcon sx={{ fontSize: 12 }} />,
          label: 'Story récente',
          animation: 'gradient-rotate',
        };
      case 'ai-thinking':
        return {
          color: '#9C27B0',
          icon: <AIIcon sx={{ fontSize: 12 }} />,
          label: 'IA en réflexion',
          animation: 'ai-pulse',
        };
      default:
        return {
          color: '#9E9E9E',
          icon: <WifiOffIcon sx={{ fontSize: 12 }} />,
          label: 'Hors ligne',
          animation: 'none',
        };
    }
  };

  const statusConfig = getStatusConfig();

  // Styles CSS pour les animations
  const getAnimationStyles = () => {
    const baseStyles = {
      position: 'relative',
      display: 'inline-block',
      cursor: 'pointer',
      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
      transform: isHovered ? 'scale(1.05)' : 'scale(1)',
    };

    const ringStyles = {
      position: 'absolute',
      top: -4,
      left: -4,
      right: -4,
      bottom: -4,
      borderRadius: '50%',
      border: `3px solid ${statusConfig.color}`,
      transition: 'all 0.3s ease',
    };

    // Animations spécifiques
    let animationStyles = {};
    switch (statusConfig.animation) {
      case 'pulse-green':
        animationStyles = {
          ...ringStyles,
          animation: 'pulse-green 2s infinite',
          boxShadow: '0 0 20px rgba(76, 175, 80, 0.3)',
        };
        break;
      case 'pulse-blue':
        animationStyles = {
          ...ringStyles,
          animation: 'pulse-blue 1.5s infinite',
          boxShadow: '0 0 20px rgba(33, 150, 243, 0.4)',
        };
        break;
      case 'gradient-rotate':
        animationStyles = {
          ...ringStyles,
          background: 'linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4)',
          backgroundSize: '400% 400%',
          animation: 'gradient-rotate 3s ease infinite',
          border: 'none',
        };
        break;
      case 'ai-pulse':
        animationStyles = {
          ...ringStyles,
          animation: 'ai-pulse 1s infinite',
          boxShadow: '0 0 25px rgba(156, 39, 176, 0.5)',
        };
        break;
      default:
        animationStyles = ringStyles;
    }

    return { baseStyles, ringStyles: animationStyles };
  };

  const { baseStyles, ringStyles } = getAnimationStyles();

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 1,
        position: 'relative',
      }}
      className={className}
    >
      {/* Avatar avec anneau animé */}
      <Box
        sx={baseStyles}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {/* Anneau de statut */}
        {showStatus && (
          <Box sx={ringStyles} />
        )}

        {/* Avatar principal */}
        <Avatar
          src={src}
          alt={alt}
          sx={{
            width: size,
            height: size,
            border: '3px solid white',
            boxShadow: isHovered 
              ? '0 8px 25px rgba(0,0,0,0.15)' 
              : '0 4px 15px rgba(0,0,0,0.1)',
            transition: 'all 0.3s ease',
            position: 'relative',
            zIndex: 2,
          }}
        >
          {!src && name.charAt(0).toUpperCase()}
        </Avatar>

        {/* Indicateur de statut (petit cercle) */}
        {showStatus && (
          <Box
            sx={{
              position: 'absolute',
              bottom: 2,
              right: 2,
              width: 20,
              height: 20,
              borderRadius: '50%',
              backgroundColor: statusConfig.color,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              border: '2px solid white',
              zIndex: 3,
              ...(statusConfig.animation !== 'none' && {
                animation: `${statusConfig.animation} 2s infinite`,
              }),
            }}
          >
            {isThinking ? (
              <CircularProgress size={10} sx={{ color: 'white' }} />
            ) : (
              statusConfig.icon
            )}
          </Box>
        )}

        {/* Effet de brillance au survol */}
        {isHovered && (
          <Fade in={isHovered}>
            <Box
              sx={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                borderRadius: '50%',
                background: 'radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%)',
                zIndex: 1,
              }}
            />
          </Fade>
        )}
      </Box>

      {/* Nom de l'utilisateur */}
      {showName && (
        <Zoom in={true} timeout={500}>
          <Typography
            variant="caption"
            sx={{
              fontWeight: 600,
              color: 'text.primary',
              textAlign: 'center',
              maxWidth: size + 20,
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
            }}
          >
            {name}
          </Typography>
        </Zoom>
      )}

      {/* Chip de statut avec tooltip */}
      {showStatus && (
        <Tooltip title={statusConfig.label} arrow>
          <Chip
            icon={statusConfig.icon}
            label={statusConfig.label}
            size="small"
            sx={{
              backgroundColor: statusConfig.color,
              color: 'white',
              fontSize: '0.7rem',
              height: 20,
              '& .MuiChip-icon': {
                color: 'white',
                fontSize: '0.8rem',
              },
              ...(statusConfig.animation !== 'none' && {
                animation: `${statusConfig.animation} 2s infinite`,
              }),
            }}
          />
        </Tooltip>
      )}

      {/* Styles CSS pour les animations - injectés via useEffect */}
      <style dangerouslySetInnerHTML={{
        __html: `
          @keyframes pulse-green {
            0%, 100% { 
              transform: scale(1);
              opacity: 1;
            }
            50% { 
              transform: scale(1.1);
              opacity: 0.7;
            }
          }

          @keyframes pulse-blue {
            0%, 100% { 
              transform: scale(1);
              opacity: 1;
            }
            50% { 
              transform: scale(1.15);
              opacity: 0.6;
            }
          }

          @keyframes gradient-rotate {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
          }

          @keyframes ai-pulse {
            0%, 100% { 
              transform: scale(1);
              opacity: 1;
            }
            50% { 
              transform: scale(1.2);
              opacity: 0.5;
            }
          }
        `
      }} />
    </Box>
  );
};

export default AvatarCircleAI;
