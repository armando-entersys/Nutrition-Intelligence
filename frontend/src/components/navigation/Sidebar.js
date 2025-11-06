import React, { useState } from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  IconButton,
  Box,
  Typography,
  Avatar,
  Divider,
  Select,
  MenuItem,
  FormControl,
  Chip,
  Tooltip,
  Badge,
  useTheme,
  Collapse,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Restaurant as RestaurantIcon,
  MenuBook as MenuBookIcon,
  SwapHoriz as SwapHorizIcon,
  People as PeopleIcon,
  Calculate as CalculateIcon,
  QrCodeScanner as QrCodeScannerIcon,
  FolderOpen as FolderOpenIcon,
  Fastfood as FastfoodIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  Person as PersonIcon,
  MedicalServices as MedicalServicesIcon,
  Settings as SettingsIcon,
  Language as LanguageIcon,
  CameraAlt as CameraAltIcon,
  EmojiEvents as EmojiEventsIcon,
  Chat as ChatIcon,
  ExpandLess,
  ExpandMore,
  AdminPanelSettings as AdminPanelSettingsIcon,
  Security as SecurityIcon,
  ViewModule as ViewModuleIcon,
  Assignment as AssignmentIcon,
  BarChart as BarChartIcon,
  Storage as StorageIcon,
  EventNote as EventNoteIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';

const MotionBox = motion(Box);
const MotionListItemButton = motion(ListItemButton);

const Sidebar = ({ currentView, setCurrentView, isCollapsed, toggleSidebar, currentRole, setCurrentRole, userRoles, isMobile, mobileDrawerOpen, setMobileDrawerOpen, currentUser }) => {
  const theme = useTheme();
  const [expandedGroups, setExpandedGroups] = useState({ tools: true, features: true });

  // Get user's full name
  const getUserDisplayName = () => {
    if (!currentUser) return 'Usuario';

    const firstName = currentUser.first_name || '';
    const lastName = currentUser.last_name || '';

    if (firstName && lastName) {
      return `${firstName} ${lastName}`;
    }

    return currentUser.username || currentUser.email || 'Usuario';
  };

  const userDisplayName = getUserDisplayName();

  const navigationGroups = [
    {
      id: 'main',
      label: 'Principal',
      items: [
        { id: 'dashboard', icon: DashboardIcon, label: 'Dashboard', description: 'Panel principal', color: theme.palette.primary.main },
      ]
    },
    {
      id: 'patient-care',
      label: 'Atención al Paciente',
      items: [
        { id: 'expediente', icon: FolderOpenIcon, label: 'Expediente Clínico', description: 'Expediente completo', roles: ['nutritionist', 'admin'], color: '#9C27B0', badge: 2 },
        { id: 'dietas', icon: FastfoodIcon, label: 'Dietas Dinámicas', description: 'Generador con IA', roles: ['nutritionist', 'admin'], color: '#FF6B35' },
        { id: 'patients', icon: PeopleIcon, label: 'Pacientes', description: 'Gestión de pacientes', roles: ['nutritionist', 'admin'], color: theme.palette.info.main, badge: 5 },
      ]
    },
    {
      id: 'database',
      label: 'Base de Datos',
      items: [
        { id: 'foods', icon: RestaurantIcon, label: 'Alimentos', description: 'Base de datos', roles: ['nutritionist', 'admin'], color: theme.palette.success.main },
        { id: 'recipes', icon: MenuBookIcon, label: 'Recetas', description: 'Recetas y menús', roles: ['nutritionist', 'admin'], color: theme.palette.secondary.main },
        { id: 'equivalences', icon: SwapHorizIcon, label: 'Equivalencias', description: 'Sistema SMAE', roles: ['nutritionist', 'admin'], color: theme.palette.tertiary.main },
      ]
    },
    {
      id: 'ai-tools',
      label: 'Herramientas IA',
      items: [
        { id: 'analisis-fotos', icon: CameraAltIcon, label: 'Análisis de Fotos', description: 'Identifica platillos', roles: ['nutritionist', 'patient', 'admin'], color: '#667eea', badge: 'NEW' },
        { id: 'chat-ia', icon: ChatIcon, label: 'Chat Nutriólogo IA', description: 'Asistente 24/7', roles: ['nutritionist', 'patient', 'admin'], color: '#9C27B0' },
        { id: 'scanner', icon: QrCodeScannerIcon, label: 'Escáner NOM-051', description: 'Escaneo de etiquetas', roles: ['nutritionist', 'patient', 'admin'], color: '#2196F3' },
      ]
    },
    {
      id: 'other',
      label: 'Otras Herramientas',
      items: [
        { id: 'recordatorio', icon: EventNoteIcon, label: 'Recordatorio 24 Horas', description: 'Registro de comidas', roles: ['nutritionist', 'patient', 'admin'], color: '#00BCD4' },
        { id: 'gamificacion', icon: EmojiEventsIcon, label: 'Gamificación', description: 'Logros y recompensas', roles: ['nutritionist', 'patient', 'admin'], color: '#FFD700' },
        { id: 'calculator', icon: CalculateIcon, label: 'Calculadora', description: 'Herramientas de cálculo', roles: ['nutritionist', 'admin'], color: theme.palette.warning.main },
      ]
    },
    {
      id: 'administration',
      label: 'Administración',
      items: [
        { id: 'admin-users', icon: AdminPanelSettingsIcon, label: 'Usuarios', description: 'Gestionar usuarios', roles: ['admin'], color: '#e74c3c' },
        { id: 'admin-roles', icon: SecurityIcon, label: 'Roles y Permisos', description: 'Configurar accesos', roles: ['admin'], color: '#9b59b6', badge: 'NEW' },
        { id: 'admin-views', icon: ViewModuleIcon, label: 'Vistas por Rol', description: 'Configurar vistas', roles: ['admin'], color: '#3498db' },
        { id: 'admin-reports', icon: BarChartIcon, label: 'Reportes', description: 'Analítica del sistema', roles: ['admin'], color: '#27ae60' },
        { id: 'admin-logs', icon: AssignmentIcon, label: 'Logs del Sistema', description: 'Auditoría y logs', roles: ['admin'], color: '#f39c12' },
        { id: 'admin-database', icon: StorageIcon, label: 'Base de Datos', description: 'Mantenimiento BD', roles: ['admin'], color: '#34495e' },
        { id: 'admin-settings', icon: SettingsIcon, label: 'Configuración', description: 'Ajustes del sistema', roles: ['admin'], color: '#95a5a6' },
        { id: 'testing-dashboard', icon: AssignmentIcon, label: 'Dashboard de Pruebas', description: 'Sistema de testing E2E', roles: ['admin'], color: '#16a085', badge: 'QA' },
      ]
    },
  ];

  const roleLabels = {
    nutritionist: { label: 'Nutricionista', icon: <MedicalServicesIcon /> },
    patient: { label: 'Paciente', icon: <PersonIcon /> },
    admin: { label: 'Admin', icon: <SettingsIcon /> }
  };

  const handleRoleChange = (newRole) => {
    console.log('🔄 Sidebar - handleRoleChange called:', {
      newRole,
      previousRole: currentRole,
      timestamp: new Date().toISOString()
    });
    setCurrentRole(newRole);
    setCurrentView('dashboard');
    console.log('✅ Sidebar - State update called');
  };

  const toggleGroup = (groupId) => {
    setExpandedGroups(prev => ({
      ...prev,
      [groupId]: !prev[groupId]
    }));
  };

  // Filter navigation items based on current role
  const filterItemsByRole = (items) => {
    return items.filter(item => !item.roles || item.roles.includes(currentRole));
  };

  const renderNavItem = (item, index, groupIndex) => {
    const isActive = currentView === item.id;
    const IconComponent = item.icon;
    const shouldCollapse = isCollapsed && !isMobile; // Never collapse in mobile

    const navButton = (
      <MotionListItemButton
        key={item.id}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{
          duration: 0.3,
          delay: (groupIndex * 0.1) + (index * 0.03),
          type: "spring",
          stiffness: 200
        }}
        onClick={() => {
          setCurrentView(item.id);
          if (isMobile) {
            setMobileDrawerOpen(false);
          }
        }}
        sx={{
          borderRadius: 2,
          mx: 1,
          mb: 0.5,
          minHeight: 56,
          position: 'relative',
          overflow: 'hidden',
          bgcolor: isActive ? 'rgba(76, 175, 80, 0.15)' : 'transparent',
          borderLeft: isActive ? `4px solid ${item.color}` : '4px solid transparent',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: isActive
              ? `linear-gradient(90deg, ${item.color}15 0%, transparent 100%)`
              : 'transparent',
            transition: 'all 0.3s',
          },
          '&:hover': {
            bgcolor: isActive ? 'rgba(76, 175, 80, 0.25)' : 'rgba(255, 255, 255, 0.08)',
            transform: 'translateX(4px)',
            boxShadow: isActive ? `0 4px 16px ${item.color}40` : '0 2px 8px rgba(0,0,0,0.1)',
            '&::before': {
              background: `linear-gradient(90deg, ${item.color}25 0%, transparent 100%)`,
            },
          },
          '&:active': {
            transform: 'translateX(2px) scale(0.98)',
          },
        }}
        aria-label={item.label}
      >
        <ListItemIcon
          sx={{
            minWidth: shouldCollapse ? 'auto' : 48,
            justifyContent: 'center',
            color: isActive ? item.color : 'rgba(255, 255, 255, 0.7)',
            transition: 'all 0.3s',
          }}
        >
          {item.badge ? (
            <Badge
              badgeContent={item.badge}
              color={typeof item.badge === 'string' ? 'error' : 'primary'}
              sx={{
                '& .MuiBadge-badge': {
                  fontSize: '0.65rem',
                  height: 18,
                  minWidth: 18,
                  fontWeight: 700,
                }
              }}
            >
              <IconComponent sx={{ fontSize: shouldCollapse ? 28 : 24 }} />
            </Badge>
          ) : (
            <IconComponent sx={{ fontSize: shouldCollapse ? 28 : 24 }} />
          )}
        </ListItemIcon>
        {!shouldCollapse && (
          <ListItemText
            primary={item.label}
            secondary={item.description}
            primaryTypographyProps={{
              fontWeight: isActive ? 600 : 500,
              color: isActive ? 'white' : 'rgba(255, 255, 255, 0.9)',
              fontSize: '0.95rem',
              noWrap: true,
            }}
            secondaryTypographyProps={{
              color: 'rgba(255, 255, 255, 0.6)',
              fontSize: '0.75rem',
              noWrap: true,
            }}
          />
        )}
      </MotionListItemButton>
    );

    // Wrap with Tooltip when collapsed (desktop only)
    if (shouldCollapse) {
      return (
        <Tooltip
          key={item.id}
          title={
            <Box>
              <Typography variant="body2" fontWeight="600">{item.label}</Typography>
              <Typography variant="caption" color="inherit" sx={{ opacity: 0.8 }}>
                {item.description}
              </Typography>
            </Box>
          }
          placement="right"
          arrow
          enterDelay={200}
          sx={{
            '& .MuiTooltip-tooltip': {
              bgcolor: 'rgba(0, 0, 0, 0.9)',
              backdropFilter: 'blur(10px)',
              border: `1px solid ${item.color}40`,
              boxShadow: `0 4px 20px ${item.color}20`,
            }
          }}
        >
          {navButton}
        </Tooltip>
      );
    }

    return navButton;
  };

  const drawerContent = (
    <>
      {/* Header */}
      <MotionBox
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: (isCollapsed && !isMobile) ? 'center' : 'space-between',
          p: 2,
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          minHeight: 80,
          background: 'rgba(255, 255, 255, 0.02)',
        }}
      >
        {(!isCollapsed || isMobile) && (
          <MotionBox
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
            sx={{ display: 'flex', alignItems: 'center', gap: 1 }}
          >
            <RestaurantIcon sx={{ color: theme.palette.primary.light, fontSize: 32 }} />
            <Typography
              variant="h6"
              sx={{
                fontWeight: 700,
                background: 'linear-gradient(135deg, #4CAF50 0%, #81C784 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                fontSize: '1.1rem',
              }}
            >
              Nutrition
            </Typography>
          </MotionBox>
        )}
        {!isMobile && (
          <Tooltip title={isCollapsed ? "Expandir menú" : "Contraer menú"} placement="right" arrow>
            <IconButton
              onClick={toggleSidebar}
              sx={{
                color: 'white',
                bgcolor: 'rgba(255, 255, 255, 0.1)',
                minWidth: 40,
                minHeight: 40,
                '&:hover': {
                  bgcolor: theme.palette.primary.main,
                  transform: 'scale(1.1) rotate(180deg)',
                  boxShadow: `0 4px 12px ${theme.palette.primary.main}60`,
                },
                transition: 'all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)',
              }}
              aria-label={isCollapsed ? "Expandir menú lateral" : "Contraer menú lateral"}
            >
              {isCollapsed ? <ChevronRightIcon /> : <ChevronLeftIcon />}
            </IconButton>
          </Tooltip>
        )}
      </MotionBox>

      {/* Navigation Groups */}
      <Box sx={{ flex: 1, py: 2, px: 1 }}>
        {navigationGroups.map((group, groupIndex) => {
          const filteredItems = filterItemsByRole(group.items);
          if (filteredItems.length === 0) return null;

          return (
            <Box key={group.id} sx={{ mb: 2 }}>
              {/* Group Header */}
              {(!isCollapsed || isMobile) && (
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    px: 2,
                    py: 1,
                    cursor: 'pointer',
                    '&:hover': {
                      '& .group-label': {
                        color: 'rgba(255, 255, 255, 1)',
                      }
                    }
                  }}
                  onClick={() => toggleGroup(group.id)}
                >
                  <Typography
                    className="group-label"
                    variant="caption"
                    sx={{
                      color: 'rgba(255, 255, 255, 0.5)',
                      fontWeight: 700,
                      textTransform: 'uppercase',
                      letterSpacing: '0.1em',
                      fontSize: '0.7rem',
                      transition: 'color 0.3s',
                    }}
                  >
                    {group.label}
                  </Typography>
                  <IconButton size="small" sx={{ color: 'rgba(255, 255, 255, 0.3)', width: 20, height: 20 }}>
                    {expandedGroups[group.id] ? <ExpandLess sx={{ fontSize: 16 }} /> : <ExpandMore sx={{ fontSize: 16 }} />}
                  </IconButton>
                </Box>
              )}

              {/* Group Items */}
              <Collapse in={expandedGroups[group.id]} timeout="auto">
                <List sx={{ py: 0 }}>
                  {filteredItems.map((item, index) => (
                    <ListItem key={item.id} disablePadding sx={{ mb: 0.5 }}>
                      {renderNavItem(item, index, groupIndex)}
                    </ListItem>
                  ))}
                </List>
              </Collapse>

              {/* Divider between groups */}
              {groupIndex < navigationGroups.length - 1 && (
                <Divider sx={{ my: 1, mx: 2, borderColor: 'rgba(255, 255, 255, 0.05)' }} />
              )}
            </Box>
          );
        })}
      </Box>

      <Divider sx={{ borderColor: 'rgba(255, 255, 255, 0.1)' }} />

      {/* Role Selector */}
      {(!isCollapsed || isMobile) && userRoles && userRoles.length > 1 && (
        <MotionBox
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          sx={{ p: 2 }}
        >
          <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.6)', mb: 1, display: 'block' }}>
            Cambiar Vista
          </Typography>
          <FormControl fullWidth size="small">
            <Select
              value={currentRole}
              onChange={(e) => handleRoleChange(e.target.value)}
              sx={{
                color: 'white',
                bgcolor: 'rgba(255, 255, 255, 0.08)',
                borderRadius: 2,
                transition: 'all 0.3s',
                '& .MuiOutlinedInput-notchedOutline': {
                  borderColor: 'rgba(76, 175, 80, 0.3)',
                },
                '&:hover': {
                  bgcolor: 'rgba(255, 255, 255, 0.12)',
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: theme.palette.primary.light,
                  },
                },
                '& .MuiSvgIcon-root': {
                  color: 'white',
                },
              }}
            >
              {userRoles.map(role => (
                <MenuItem key={role} value={role}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    {roleLabels[role].icon}
                    {roleLabels[role].label}
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </MotionBox>
      )}

      {/* Footer */}
      <AnimatePresence>
        {(!isCollapsed || isMobile) && (
          <MotionBox
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            transition={{ duration: 0.5 }}
            sx={{
              p: 2,
              borderTop: '1px solid rgba(255, 255, 255, 0.1)',
              background: 'rgba(255, 255, 255, 0.02)',
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 1.5 }}>
              <Avatar
                sx={{
                  width: 44,
                  height: 44,
                  bgcolor: theme.palette.primary.main,
                  boxShadow: `0 4px 12px ${theme.palette.primary.main}60`,
                  border: '2px solid rgba(255, 255, 255, 0.1)',
                }}
              >
                <PersonIcon />
              </Avatar>
              <Box sx={{ flex: 1, overflow: 'hidden' }}>
                <Typography variant="body2" fontWeight={600} color="white" sx={{ lineHeight: 1.2 }} noWrap>
                  {userDisplayName}
                </Typography>
                <Chip
                  label={roleLabels[currentRole]?.label || 'Nutricionista'}
                  size="small"
                  icon={roleLabels[currentRole]?.icon}
                  sx={{
                    mt: 0.5,
                    height: 20,
                    fontSize: '0.7rem',
                    bgcolor: 'rgba(76, 175, 80, 0.2)',
                    color: theme.palette.primary.light,
                    '& .MuiChip-icon': {
                      color: theme.palette.primary.light,
                      fontSize: '0.9rem',
                    },
                  }}
                />
              </Box>
            </Box>
            <Box
              component="a"
              href="https://saragallegos.com/"
              target="_blank"
              rel="noopener noreferrer"
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 1,
                p: 1,
                borderRadius: 2,
                bgcolor: 'rgba(255, 255, 255, 0.05)',
                color: 'rgba(255, 255, 255, 0.8)',
                textDecoration: 'none',
                fontSize: '0.85rem',
                transition: 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
                '&:hover': {
                  bgcolor: theme.palette.primary.main,
                  color: 'white',
                  transform: 'translateY(-2px)',
                  boxShadow: `0 4px 12px ${theme.palette.primary.main}60`,
                },
              }}
            >
              <LanguageIcon sx={{ fontSize: 18 }} />
              saragallegos.com
            </Box>
          </MotionBox>
        )}
      </AnimatePresence>

      {/* Collapsed mode - Footer */}
      {isCollapsed && !isMobile && (
        <Box sx={{ p: 1, borderTop: '1px solid rgba(255, 255, 255, 0.1)' }}>
          <Tooltip title={userDisplayName} placement="right" arrow>
            <Avatar
              sx={{
                width: 48,
                height: 48,
                bgcolor: theme.palette.primary.main,
                boxShadow: `0 4px 12px ${theme.palette.primary.main}60`,
                border: '2px solid rgba(255, 255, 255, 0.1)',
                cursor: 'pointer',
                mx: 'auto',
                '&:hover': {
                  transform: 'scale(1.1)',
                  boxShadow: `0 6px 16px ${theme.palette.primary.main}80`,
                },
                transition: 'all 0.3s',
              }}
            >
              <PersonIcon />
            </Avatar>
          </Tooltip>
        </Box>
      )}
    </>
  );

  const drawerStyles = {
    width: isMobile ? 280 : (isCollapsed ? 80 : 240),
    flexShrink: 0,
    '& .MuiDrawer-paper': {
      width: isMobile ? 280 : (isCollapsed ? 80 : 240),
      boxSizing: 'border-box',
      background: 'linear-gradient(180deg, #1e293b 0%, #0f172a 100%)',
      backdropFilter: 'blur(20px)',
      color: 'white',
      borderRight: '1px solid rgba(255, 255, 255, 0.05)',
      boxShadow: '4px 0 24px rgba(0, 0, 0, 0.3)',
      transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.easeInOut,
        duration: theme.transitions.duration.standard,
      }),
      overflow: 'hidden',
      overflowY: 'auto',
      // Custom scrollbar
      '&::-webkit-scrollbar': {
        width: 6,
      },
      '&::-webkit-scrollbar-track': {
        bgcolor: 'rgba(255, 255, 255, 0.05)',
      },
      '&::-webkit-scrollbar-thumb': {
        bgcolor: 'rgba(255, 255, 255, 0.2)',
        borderRadius: 3,
        '&:hover': {
          bgcolor: 'rgba(255, 255, 255, 0.3)',
        },
      },
    },
  };

  return (
    <>
      {/* Mobile Drawer (Temporary) */}
      {isMobile ? (
        <Drawer
          variant="temporary"
          open={mobileDrawerOpen}
          onClose={() => setMobileDrawerOpen(false)}
          ModalProps={{
            keepMounted: true, // Better mobile performance
          }}
          sx={drawerStyles}
          PaperProps={{ role: "navigation" }}
        >
          {drawerContent}
        </Drawer>
      ) : (
        /* Desktop Drawer (Permanent) */
        <Drawer
          variant="permanent"
          sx={drawerStyles}
          PaperProps={{ role: "navigation" }}
        >
          {drawerContent}
        </Drawer>
      )}
    </>
  );
};

export default Sidebar;
