import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ThemeProvider, CssBaseline, useMediaQuery, useTheme } from '@mui/material';
import { Box, AppBar, Toolbar, Card, CardContent, Typography, IconButton, Badge, Avatar, Chip, Grid, Link as MuiLink, Button } from '@mui/material';
import {
  Notifications as NotificationsIcon,
  Restaurant as RestaurantIcon,
  Menu as MenuIcon,
  AdminPanelSettings as AdminPanelSettingsIcon,
  Security as SecurityIcon,
  ViewModule as ViewModuleIcon,
  BarChart as BarChartIcon,
  Assignment as AssignmentIcon,
  Storage as StorageIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import theme from './theme/theme';
import EquivalencesBrowser from './components/equivalences/EquivalencesBrowser';
import RealTimeMonitor from './components/dashboard/RealTimeMonitor';
import RoleBasedDashboard from './components/dashboard/RoleBasedDashboard';
import RecipesBrowser from './components/recipes/RecipesBrowser';
import FoodsBrowser from './components/foods/FoodsBrowser';
import PatientsBrowser from './components/patients/PatientsBrowser';
import NutritionCalculator from './components/calculator/NutritionCalculator';
import EscanerNOM051 from './components/scanner/EscanerNOM051';
import ExpedienteClinico from './components/expediente/ExpedienteClinico';
import GeneradorDietas from './components/dietas/GeneradorDietas';
import CalculadoraRequerimientos from './components/dietas/CalculadoraRequerimientos';
import AnalizadorFotosMejorado from './components/analisis-fotos/AnalizadorFotosMejorado';
import GamificacionMexicana from './components/gamificacion/GamificacionMexicana';
import ChatNutriologoIA from './components/chat-ia/ChatNutriologoIA';
import Recordatorio24Horas from './components/recordatorio/Recordatorio24Horas';
import AdminPlaceholder from './components/admin/AdminPlaceholder';
import TestingDashboard from './components/testing/TestingDashboard';
import Sidebar from './components/navigation/Sidebar';
import Breadcrumbs from './components/common/Breadcrumbs';
import { ToastProvider } from './components/common/Toast';
import NotificationsPanel from './components/common/NotificationsPanel';
import GlobalSearch from './components/common/GlobalSearch';
import HelpButton from './components/common/HelpButton';
import WelcomeTour from './components/common/WelcomeTour';
import { API_BASE_URL, API_ENDPOINTS } from './config/api';
import authService from './services/authService';

// Motion components for animations
const MotionBox = motion(Box);
const MotionCard = motion(Card);

function MainApp() {
  const appTheme = useTheme();
  const isMobile = useMediaQuery(appTheme.breakpoints.down('md'));
  const navigate = useNavigate();
  const [backendStatus, setBackendStatus] = useState('Conectando...');
  const [apiData, setApiData] = useState(null);
  const [currentView, setCurrentView] = useState('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [showGlobalSearch, setShowGlobalSearch] = useState(false);
  // Get current user from token
  const currentUser = authService.getCurrentUser();

  // Determine user's available roles from their data
  const getUserRoles = () => {
    if (!currentUser) return ['nutritionist']; // Default fallback

    const roles = [];

    // Add primary role
    if (currentUser.primary_role) {
      roles.push(currentUser.primary_role.toLowerCase());
    }

    // Add secondary roles if they exist
    if (currentUser.secondary_roles && Array.isArray(currentUser.secondary_roles)) {
      currentUser.secondary_roles.forEach(role => {
        const roleLower = role.toLowerCase();
        if (!roles.includes(roleLower)) {
          roles.push(roleLower);
        }
      });
    }

    return roles.length > 0 ? roles : ['nutritionist']; // Default fallback
  };

  const userRoles = getUserRoles();
  const [currentRole, setCurrentRole] = useState(userRoles[0]); // Set to user's primary role

  // Debug: Monitor currentRole changes
  useEffect(() => {
    console.log('🔔 MainApp - currentRole changed to:', currentRole, {
      currentView,
      timestamp: new Date().toISOString()
    });
  }, [currentRole]);

  // Debug: Monitor currentView changes
  useEffect(() => {
    console.log('📍 MainApp - currentView changed to:', currentView, {
      currentRole,
      timestamp: new Date().toISOString()
    });
  }, [currentView]);

  useEffect(() => {
    // Probar conexión con el backend
    const checkBackend = async () => {
      try {
        console.log('Connecting to:', API_ENDPOINTS.HEALTH);
        const response = await axios.get(API_ENDPOINTS.HEALTH);
        setBackendStatus('✅ Backend Conectado');
        setApiData(response.data);
      } catch (error) {
        console.error('Health endpoint failed:', error.message);
        try {
          // Probar ruta alternativa
          console.log('Trying base URL:', `${API_BASE_URL}/`);
          await axios.get(`${API_BASE_URL}/`);
          setBackendStatus('✅ Backend Conectado (ruta /)');
          setApiData({ message: 'Backend activo pero sin endpoint /health' });
        } catch (err) {
          console.error('Base URL failed:', err.message);
          setBackendStatus(`❌ Backend no disponible (${API_BASE_URL})`);
        }
      }
    };

    checkBackend();
  }, []);

  // Ctrl+K para búsqueda global
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        setShowGlobalSearch(true);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleLogout = () => {
    authService.logout();
    navigate('/auth/login');
  };

  const getViewTitle = () => {
    const titles = {
      dashboard: 'Dashboard',
      foods: 'Alimentos',
      recipes: 'Recetas',
      equivalences: 'Equivalencias',
      patients: 'Pacientes',
      calculator: 'Calculadora',
      scanner: 'Escáner NOM-051',
      expediente: 'Expediente Clínico',
      dietas: 'Dietas Dinámicas',
      recordatorio: 'Recordatorio 24 Horas',
      'calculadora-requerimientos': 'Calculadora de Requerimientos',
      'analisis-fotos': 'Análisis de Fotos IA',
      gamificacion: 'Gamificación Mexicana',
      'chat-ia': 'Chat Nutriólogo Virtual',
      'admin-users': 'Gestión de Usuarios',
      'admin-roles': 'Roles y Permisos',
      'admin-views': 'Vistas por Rol',
      'admin-reports': 'Reportes del Sistema',
      'admin-logs': 'Logs del Sistema',
      'admin-database': 'Base de Datos',
      'admin-settings': 'Configuración del Sistema',
      'testing-dashboard': 'Dashboard de Pruebas'
    };
    return titles[currentView] || 'Dashboard';
  };

  const getBreadcrumbs = () => {
    return [
      { label: 'Dashboard', onClick: () => setCurrentView('dashboard') },
      ...(currentView !== 'dashboard' ? [{ label: getViewTitle() }] : [])
    ];
  };

  const handleSearchNavigate = (item) => {
    if (item.type === 'section') {
      setCurrentView(item.id);
    } else {
      // Para pacientes, alimentos, recetas - navegar a la sección correspondiente
      const sectionMap = {
        patient: 'patients',
        food: 'foods',
        recipe: 'recipes'
      };
      setCurrentView(sectionMap[item.type]);
      // Aquí podríamos también seleccionar el item específico
    }
  };

  const renderCurrentView = () => {
    // Vistas disponibles para todos los roles
    switch (currentView) {
      // Vistas restringidas a nutricionista/admin
      case 'foods':
        if (currentRole === 'patient') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <Box sx={{ width: '100%' }}>
            <FoodsBrowser />
          </Box>
        );

      case 'recipes':
        return (
          <Box sx={{ width: '100%' }}>
            <RecipesBrowser />
          </Box>
        );

      case 'equivalences':
        if (currentRole === 'patient') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <Box sx={{ width: '100%' }}>
            <EquivalencesBrowser />
          </Box>
        );

      case 'patients':
        if (currentRole === 'patient') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <Box sx={{ width: '100%' }}>
            <PatientsBrowser />
          </Box>
        );

      case 'calculator':
        if (currentRole === 'patient') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <Box sx={{ width: '100%' }}>
            <NutritionCalculator />
          </Box>
        );

      case 'scanner':
        return (
          <Box sx={{ width: '100%' }}>
            <EscanerNOM051 />
          </Box>
        );

      case 'expediente':
        if (currentRole === 'patient') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <Box sx={{ width: '100%' }}>
            <ExpedienteClinico />
          </Box>
        );

      case 'recordatorio':
        return (
          <Box sx={{ width: '100%' }}>
            <Recordatorio24Horas />
          </Box>
        );

      case 'dietas':
        if (currentRole === 'patient') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <Box sx={{ width: '100%' }}>
            <GeneradorDietas />
          </Box>
        );

      case 'calculadora-requerimientos':
        if (currentRole === 'patient') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <Box sx={{ width: '100%' }}>
            <CalculadoraRequerimientos />
          </Box>
        );

      case 'analisis-fotos':
        return (
          <Box sx={{ width: '100%' }}>
            <AnalizadorFotosMejorado />
          </Box>
        );

      case 'gamificacion':
        return (
          <Box sx={{ width: '100%' }}>
            <GamificacionMexicana />
          </Box>
        );

      case 'chat-ia':
        return (
          <Box sx={{ width: '100%' }}>
            <ChatNutriologoIA />
          </Box>
        );

      case 'admin-users':
        if (currentRole !== 'admin') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <AdminPlaceholder
            title="Gestión de Usuarios"
            description="Administra usuarios del sistema, crea nuevos usuarios, asigna roles y permisos"
            icon={AdminPanelSettingsIcon}
            features={[
              'Crear y editar usuarios',
              'Asignar roles (Admin, Nutricionista, Paciente)',
              'Gestionar permisos individuales',
              'Ver historial de accesos',
              'Activar/desactivar usuarios',
              'Resetear contraseñas'
            ]}
            onBack={() => setCurrentView('dashboard')}
          />
        );

      case 'admin-roles':
        if (currentRole !== 'admin') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <AdminPlaceholder
            title="Roles y Permisos"
            description="Configura roles del sistema y sus permisos asociados"
            icon={SecurityIcon}
            features={[
              'Crear roles personalizados',
              'Asignar permisos granulares',
              'Definir acceso a vistas',
              'Configurar restricciones por rol',
              'Auditoría de cambios en permisos',
              'Templates de roles predefinidos'
            ]}
            onBack={() => setCurrentView('dashboard')}
          />
        );

      case 'admin-views':
        if (currentRole !== 'admin') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <AdminPlaceholder
            title="Vistas por Rol"
            description="Configura qué vistas y funcionalidades están disponibles para cada rol"
            icon={ViewModuleIcon}
            features={[
              'Habilitar/deshabilitar vistas por rol',
              'Configurar menú de navegación',
              'Personalizar dashboard por rol',
              'Vista previa de interfaz por rol',
              'Exportar configuraciones',
              'Importar templates'
            ]}
            onBack={() => setCurrentView('dashboard')}
          />
        );

      case 'admin-reports':
        if (currentRole !== 'admin') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <AdminPlaceholder
            title="Reportes del Sistema"
            description="Genera y visualiza reportes de uso, actividad y rendimiento del sistema"
            icon={BarChartIcon}
            features={[
              'Reportes de uso por usuario',
              'Estadísticas de planes generados',
              'Métricas de rendimiento',
              'Análisis de consultas IA',
              'Exportación a PDF/Excel',
              'Reportes programados'
            ]}
            onBack={() => setCurrentView('dashboard')}
          />
        );

      case 'admin-logs':
        if (currentRole !== 'admin') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <AdminPlaceholder
            title="Logs del Sistema"
            description="Visualiza y analiza logs de actividad, errores y auditoría del sistema"
            icon={AssignmentIcon}
            features={[
              'Visor de logs en tiempo real',
              'Filtrado por tipo y nivel',
              'Búsqueda avanzada en logs',
              'Exportación de logs',
              'Alertas automáticas',
              'Rotación de logs configurable'
            ]}
            onBack={() => setCurrentView('dashboard')}
          />
        );

      case 'admin-database':
        if (currentRole !== 'admin') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <AdminPlaceholder
            title="Gestión de Base de Datos"
            description="Herramientas de mantenimiento y administración de la base de datos"
            icon={StorageIcon}
            features={[
              'Backup y restauración',
              'Optimización de tablas',
              'Estadísticas de uso',
              'Limpieza de datos obsoletos',
              'Migraciones de esquema',
              'Monitoreo de rendimiento'
            ]}
            onBack={() => setCurrentView('dashboard')}
          />
        );

      case 'admin-settings':
        if (currentRole !== 'admin') {
          setCurrentView('dashboard');
          return null;
        }
        return (
          <AdminPlaceholder
            title="Configuración del Sistema"
            description="Ajustes generales y configuración avanzada del sistema"
            icon={SettingsIcon}
            features={[
              'Configuración general',
              'Parámetros de API',
              'Integraciones externas',
              'Notificaciones del sistema',
              'Personalización de marca',
              'Variables de entorno'
            ]}
            onBack={() => setCurrentView('dashboard')}
          />
        );

      case 'testing-dashboard':
        return (
          <Box sx={{ width: '100%' }}>
            <TestingDashboard />
          </Box>
        );

      case 'dashboard':
      default:
        return (
          <Box sx={{ width: '100%' }}>
            <Grid container spacing={3}>
              {/* System Status Card - SOLO ADMIN */}
              {currentRole === 'admin' && (
                <Grid item xs={12} md={6}>
                  <MotionCard
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    elevation={2}
                  >
                    <CardContent>
                      <Typography variant="h5" gutterBottom color="primary" fontWeight={600}>
                        Estado del Sistema
                      </Typography>
                      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 1, borderBottom: 1, borderColor: 'divider' }}>
                          <Typography variant="body1">🌐 Frontend:</Typography>
                          <Chip label="Activo" color="success" size="small" />
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 1, borderBottom: 1, borderColor: 'divider' }}>
                          <Typography variant="body1">🔧 Backend:</Typography>
                          <Chip
                            label={backendStatus}
                            color={backendStatus.includes('✅') ? 'success' : 'error'}
                            size="small"
                          />
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 1, borderBottom: 1, borderColor: 'divider' }}>
                          <Typography variant="body1">🗄️ PostgreSQL:</Typography>
                          <Chip label="Activo (puerto 5432)" color="success" size="small" />
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 1, borderBottom: 1, borderColor: 'divider' }}>
                          <Typography variant="body1">🔴 Redis:</Typography>
                          <Chip label="Activo (puerto 6379)" color="success" size="small" />
                        </Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', py: 1 }}>
                          <Typography variant="body1">📦 MinIO:</Typography>
                          <Chip label="Activo (puertos 9000/9001)" color="success" size="small" />
                        </Box>
                      </Box>
                    </CardContent>
                  </MotionCard>
                </Grid>
              )}

              {/* Admin Links Card - SOLO ADMIN */}
              {currentRole === 'admin' && (
                <Grid item xs={12} md={6}>
                <MotionCard
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.1 }}
                  elevation={2}
                >
                  <CardContent>
                    <Typography variant="h5" gutterBottom color="primary" fontWeight={600}>
                      Enlaces de Administración
                    </Typography>
                    <Grid container spacing={2} sx={{ mt: 1 }}>
                      <Grid item xs={12}>
                        <MuiLink
                          href={API_ENDPOINTS.DOCS}
                          target="_blank"
                          rel="noopener noreferrer"
                          sx={{ textDecoration: 'none' }}
                        >
                          <Card
                            sx={{
                              bgcolor: 'primary.main',
                              color: 'white',
                              transition: 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
                              '&:hover': {
                                transform: 'translateY(-4px)',
                                boxShadow: 6
                              }
                            }}
                          >
                            <CardContent sx={{ textAlign: 'center', py: 2 }}>
                              <Typography variant="body1" fontWeight={500}>
                                📚 API Docs (FastAPI)
                              </Typography>
                            </CardContent>
                          </Card>
                        </MuiLink>
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <MuiLink
                          href="http://localhost:9001"
                          target="_blank"
                          rel="noopener noreferrer"
                          sx={{ textDecoration: 'none' }}
                        >
                          <Card
                            sx={{
                              bgcolor: 'secondary.main',
                              color: 'white',
                              transition: 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
                              '&:hover': {
                                transform: 'translateY(-4px)',
                                boxShadow: 6
                              }
                            }}
                          >
                            <CardContent sx={{ textAlign: 'center', py: 2 }}>
                              <Typography variant="body1" fontWeight={500}>
                                🗂️ MinIO Console
                              </Typography>
                            </CardContent>
                          </Card>
                        </MuiLink>
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <MuiLink
                          href="http://localhost:5050"
                          target="_blank"
                          rel="noopener noreferrer"
                          sx={{ textDecoration: 'none' }}
                        >
                          <Card
                            sx={{
                              bgcolor: 'tertiary.main',
                              color: 'white',
                              transition: 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
                              '&:hover': {
                                transform: 'translateY(-4px)',
                                boxShadow: 6
                              }
                            }}
                          >
                            <CardContent sx={{ textAlign: 'center', py: 2 }}>
                              <Typography variant="body1" fontWeight={500}>
                                🐘 PgAdmin
                              </Typography>
                            </CardContent>
                          </Card>
                        </MuiLink>
                      </Grid>
                    </Grid>
                  </CardContent>
                </MotionCard>
              </Grid>
              )}

              {/* Real-Time Monitor - SOLO ADMIN */}
              {currentRole === 'admin' && (
                <Grid item xs={12}>
                  <MotionCard
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                    elevation={2}
                    sx={{ bgcolor: 'grey.50' }}
                  >
                    <RealTimeMonitor />
                  </MotionCard>
                </Grid>
              )}

              {/* Role-Based Dashboard */}
              <Grid item xs={12}>
                <MotionCard
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.3 }}
                  elevation={2}
                >
                  <RoleBasedDashboard currentRole={currentRole} onNavigate={setCurrentView} />
                </MotionCard>
              </Grid>

              {/* Backend Response - SOLO ADMIN */}
              {currentRole === 'admin' && apiData && (
                <Grid item xs={12}>
                  <MotionCard
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: 0.4 }}
                    elevation={2}
                  >
                    <CardContent>
                      <Typography variant="h5" gutterBottom color="primary" fontWeight={600}>
                        Respuesta del Backend
                      </Typography>
                      <Box
                        component="pre"
                        sx={{
                          bgcolor: 'grey.900',
                          color: 'grey.100',
                          p: 3,
                          borderRadius: 2,
                          overflow: 'auto',
                          fontSize: '0.875rem',
                          mt: 2
                        }}
                      >
                        {JSON.stringify(apiData, null, 2)}
                      </Box>
                    </CardContent>
                  </MotionCard>
                </Grid>
              )}
            </Grid>
          </Box>
        );
    }
  };

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ToastProvider>
        <Box
          sx={{
            display: 'flex',
            minHeight: '100vh',
            bgcolor: 'background.default',
          }}
        >
          <Sidebar
            currentView={currentView}
            setCurrentView={setCurrentView}
            isCollapsed={sidebarCollapsed}
            toggleSidebar={toggleSidebar}
            currentRole={currentRole}
            setCurrentRole={setCurrentRole}
            userRoles={userRoles}
            isMobile={isMobile}
            mobileDrawerOpen={mobileDrawerOpen}
            setMobileDrawerOpen={setMobileDrawerOpen}
          />

          <Box
            component="main"
            sx={{
              flex: 1,
              ml: '0 !important',
              pl: '0 !important',
              pr: '0 !important',
              transition: 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
              minHeight: '100vh',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            {/* App Bar Header */}
            <AppBar
              position="sticky"
              elevation={0}
              sx={{
                bgcolor: 'background.paper',
                borderBottom: 1,
                borderColor: 'divider',
                backdropFilter: 'blur(10px)',
              }}
            >
              <Toolbar sx={{ py: 1.5, px: { xs: 1, sm: 2, md: 3 } }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flex: 1 }}>
                  {/* Hamburger Menu for Mobile */}
                  {isMobile && (
                    <IconButton
                      edge="start"
                      color="inherit"
                      aria-label="Abrir menú"
                      onClick={() => setMobileDrawerOpen(true)}
                      sx={{
                        minWidth: 48,
                        minHeight: 48,
                        color: 'primary.main',
                      }}
                    >
                      <MenuIcon />
                    </IconButton>
                  )}

                  {/* Logo */}
                  <MotionBox
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 0.5 }}
                    sx={{
                      width: { xs: 48, md: 64 },
                      height: { xs: 48, md: 64 },
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      bgcolor: 'primary.light',
                      borderRadius: 3,
                      boxShadow: 2,
                    }}
                  >
                    <RestaurantIcon sx={{ fontSize: { xs: 32, md: 40 }, color: 'primary.dark' }} />
                  </MotionBox>

                  {/* Title and Subtitle */}
                  <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
                    <Typography
                      variant="h4"
                      sx={{
                        background: 'linear-gradient(135deg, #2c3e50 0%, #3498db 100%)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        backgroundClip: 'text',
                        fontWeight: 700,
                        letterSpacing: '-0.5px',
                        lineHeight: 1.2,
                        fontSize: { sm: '1.5rem', md: '2.125rem' },
                      }}
                    >
                      Nutrition Intelligence
                    </Typography>
                    <Typography variant="body2" color="text.secondary" fontWeight={400} sx={{ display: { xs: 'none', md: 'block' } }}>
                      Plataforma de Inteligencia Nutricional
                    </Typography>
                  </Box>
                </Box>

                {/* Header Actions */}
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  {/* Notifications */}
                  <Box sx={{ position: 'relative' }}>
                    <IconButton
                      onClick={() => setShowNotifications(!showNotifications)}
                      sx={{
                        bgcolor: showNotifications ? 'action.selected' : 'transparent',
                        transition: 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
                        minWidth: 48,
                        minHeight: 48,
                        '&:hover': {
                          transform: 'scale(1.1)',
                        },
                      }}
                      aria-label="Abrir notificaciones (3 nuevas)"
                      title="Notificaciones"
                    >
                      <Badge badgeContent={3} color="error">
                        <NotificationsIcon />
                      </Badge>
                    </IconButton>
                    {showNotifications && (
                      <NotificationsPanel
                        onClose={() => setShowNotifications(false)}
                        onNavigate={(view) => setCurrentView(view)}
                      />
                    )}
                  </Box>

                  {/* Help Button */}
                  <HelpButton />

                  {/* User Info */}
                  <Chip
                    avatar={<Avatar sx={{ width: { xs: 28, md: 32 }, height: { xs: 28, md: 32 } }}>👤</Avatar>}
                    label={currentUser?.username || 'Usuario'}
                    color="primary"
                    sx={{
                      px: { xs: 0.5, md: 1 },
                      height: { xs: 40, md: 44 },
                      fontSize: { xs: '0.75rem', md: '0.875rem' },
                      fontWeight: 600,
                      boxShadow: 2,
                      transition: 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
                      '&:hover': {
                        transform: 'translateY(-2px)',
                        boxShadow: 4,
                      },
                      display: { xs: 'none', sm: 'flex' },
                    }}
                  />

                  {/* Logout Button */}
                  <Button
                    variant="outlined"
                    color="error"
                    startIcon={<LogoutIcon />}
                    onClick={handleLogout}
                    sx={{
                      display: { xs: 'none', md: 'flex' }
                    }}
                  >
                    Salir
                  </Button>
                  <IconButton
                    color="error"
                    onClick={handleLogout}
                    sx={{
                      display: { xs: 'flex', md: 'none' }
                    }}
                    title="Cerrar sesión"
                  >
                    <LogoutIcon />
                  </IconButton>
                </Box>
              </Toolbar>
            </AppBar>

            {/* Breadcrumbs */}
            <Box sx={{ px: { xs: 2, md: 2 }, pt: 2 }}>
              <Breadcrumbs items={getBreadcrumbs()} />
            </Box>

            {/* Main Content */}
            <Box
              sx={{
                py: { xs: 2, sm: 3, md: 4 },
                px: { xs: 2, md: 2 },
                flex: 1,
                maxWidth: '100%',
              }}
            >
              {renderCurrentView()}
            </Box>
          </Box>

          <GlobalSearch
            isOpen={showGlobalSearch}
            onClose={() => setShowGlobalSearch(false)}
            onNavigate={handleSearchNavigate}
          />

          {/* Welcome Tour for new users */}
          <WelcomeTour />
        </Box>
      </ToastProvider>
    </ThemeProvider>
  );
}

export default MainApp;
