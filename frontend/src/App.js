import React, { useState, useEffect } from 'react';
import axios from 'axios';
import EquivalenceVisualizer from './components/equivalences/EquivalenceVisualizer';
import EquivalencesBrowser from './components/equivalences/EquivalencesBrowser';
import RealTimeMonitor from './components/dashboard/RealTimeMonitor';
import RoleBasedDashboard from './components/dashboard/RoleBasedDashboard';
import RecipeBrowser from './components/recipes/RecipeBrowser';
import RecipesBrowser from './components/recipes/RecipesBrowser';
import FoodsBrowser from './components/foods/FoodsBrowser';
import PatientsBrowser from './components/patients/PatientsBrowser';
import NutritionCalculator from './components/calculator/NutritionCalculator';
import Sidebar from './components/navigation/Sidebar';
import Breadcrumbs from './components/common/Breadcrumbs';
import { ToastProvider } from './components/common/Toast';
import NotificationsPanel from './components/common/NotificationsPanel';
import GlobalSearch from './components/common/GlobalSearch';
import { API_BASE_URL, API_ENDPOINTS } from './config/api';

function App() {
  const [backendStatus, setBackendStatus] = useState('Conectando...');
  const [apiData, setApiData] = useState(null);
  const [currentView, setCurrentView] = useState('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [showGlobalSearch, setShowGlobalSearch] = useState(false);
  const [currentRole, setCurrentRole] = useState('nutritionist'); // nutritionist, patient, admin

  // Mock user for testing (in real app, this would come from authentication)
  const mockUser = {
    id: 1,
    username: "Dra. Sara Gallegos",
    email: "contacto@saragallegos.com",
    website: "https://saragallegos.com/",
    roles: ['nutritionist', 'patient'], // User can have multiple roles
    token: "mock-jwt-token" // In real app, this would be a real JWT
  };

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
          const response = await axios.get(`${API_BASE_URL}/`);
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

  const getViewTitle = () => {
    const titles = {
      dashboard: 'Dashboard',
      foods: 'Alimentos',
      recipes: 'Recetas',
      equivalences: 'Equivalencias',
      patients: 'Pacientes',
      calculator: 'Calculadora'
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
    // Si el rol es paciente, siempre mostrar el dashboard de paciente
    if (currentRole === 'patient') {
      return (
        <div style={styles.viewContainer}>
          <RoleBasedDashboard currentRole="patient" onNavigate={setCurrentView} />
        </div>
      );
    }

    // Vistas para nutricionista/admin
    switch (currentView) {
      case 'foods':
        return (
          <div style={styles.viewContainer}>
            <FoodsBrowser />
          </div>
        );

      case 'recipes':
        return (
          <div style={styles.viewContainer}>
            <RecipesBrowser />
          </div>
        );

      case 'equivalences':
        return (
          <div style={styles.viewContainer}>
            <EquivalencesBrowser />
          </div>
        );

      case 'patients':
        return (
          <div style={styles.viewContainer}>
            <PatientsBrowser />
          </div>
        );

      case 'calculator':
        return (
          <div style={styles.viewContainer}>
            <NutritionCalculator />
          </div>
        );

      case 'dashboard':
      default:
        return (
          <div style={styles.viewContainer}>
            <div style={styles.statusCard}>
              <h2>Estado del Sistema</h2>
              <div style={styles.statusItem}>
                <span>🌐 Frontend:</span>
                <span style={{color: '#27ae60'}}>✅ Activo</span>
              </div>
              <div style={styles.statusItem}>
                <span>🔧 Backend:</span>
                <span style={{color: backendStatus.includes('✅') ? '#27ae60' : '#e74c3c'}}>
                  {backendStatus}
                </span>
              </div>
              <div style={styles.statusItem}>
                <span>🗄️ PostgreSQL:</span>
                <span style={{color: '#27ae60'}}>✅ Activo (puerto 5432)</span>
              </div>
              <div style={styles.statusItem}>
                <span>🔴 Redis:</span>
                <span style={{color: '#27ae60'}}>✅ Activo (puerto 6379)</span>
              </div>
              <div style={styles.statusItem}>
                <span>📦 MinIO:</span>
                <span style={{color: '#27ae60'}}>✅ Activo (puertos 9000/9001)</span>
              </div>
            </div>

            <div style={styles.linksCard}>
              <h2>Enlaces de Administración</h2>
              <div style={styles.linkGrid}>
                <a href={API_ENDPOINTS.DOCS} style={styles.link} target="_blank" rel="noopener noreferrer">
                  📚 API Docs (FastAPI)
                </a>
                <a href="http://localhost:9001" style={styles.link} target="_blank" rel="noopener noreferrer">
                  🗂️ MinIO Console
                </a>
                <a href="http://localhost:5050" style={styles.link} target="_blank" rel="noopener noreferrer">
                  🐘 PgAdmin
                </a>
              </div>
            </div>

            <div style={styles.monitorCard}>
              <RealTimeMonitor />
            </div>

            <div style={styles.rolesCard}>
              <RoleBasedDashboard onNavigate={setCurrentView} />
            </div>

            {apiData && (
              <div style={styles.dataCard}>
                <h2>Respuesta del Backend</h2>
                <pre style={styles.preData}>
                  {JSON.stringify(apiData, null, 2)}
                </pre>
              </div>
            )}
          </div>
        );
    }
  };

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  return (
    <ToastProvider>
      <div style={styles.appContainer}>
        <Sidebar
          currentView={currentView}
          setCurrentView={setCurrentView}
          isCollapsed={sidebarCollapsed}
          toggleSidebar={toggleSidebar}
          currentRole={currentRole}
          setCurrentRole={setCurrentRole}
          userRoles={mockUser.roles}
        />

        <div style={{
          ...styles.mainContent,
          marginLeft: sidebarCollapsed ? '80px' : '280px',
        }}>
          <header style={styles.header}>
            <div style={styles.headerTop}>
              <div style={styles.headerLeft}>
                <div style={styles.logoContainer}>
                  <span style={styles.logoIcon}>🥗</span>
                  <div>
                    <h1 style={styles.title}>Nutrition Intelligence</h1>
                    <p style={styles.subtitle}>Plataforma de Inteligencia Nutricional</p>
                  </div>
                </div>
              </div>
              <div style={styles.headerActions}>
                <div style={{ position: 'relative' }}>
                  <button
                    onClick={() => setShowNotifications(!showNotifications)}
                    style={{
                      ...styles.iconButton,
                      backgroundColor: showNotifications ? '#ebf5fb' : 'transparent'
                    }}
                    title="Notificaciones"
                  >
                    🔔
                    <span style={styles.badge}>3</span>
                  </button>
                  {showNotifications && (
                    <NotificationsPanel
                      onClose={() => setShowNotifications(false)}
                      onNavigate={(view) => setCurrentView(view)}
                    />
                  )}
                </div>
                <div style={styles.userInfo}>
                  <span style={styles.userName}>👤 {mockUser.username}</span>
                </div>
              </div>
            </div>
          </header>

          <Breadcrumbs items={getBreadcrumbs()} />

          <main style={styles.main}>
            {renderCurrentView()}
          </main>
        </div>

        <GlobalSearch
          isOpen={showGlobalSearch}
          onClose={() => setShowGlobalSearch(false)}
          onNavigate={handleSearchNavigate}
        />
      </div>
    </ToastProvider>
  );
}

const styles = {
  appContainer: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif',
    minHeight: '100vh',
    backgroundColor: '#f8f9fa',
    display: 'flex',
  },
  mainContent: {
    flex: 1,
    transition: 'margin-left 0.3s ease',
    minHeight: '100vh',
    backgroundColor: '#f8f9fa',
  },
  container: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif',
    minHeight: '100vh',
    backgroundColor: '#f8f9fa',
    padding: '20px',
  },
  headerContent: {
    textAlign: 'center',
  },
  header: {
    padding: '20px 30px',
    background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.07), 0 1px 3px rgba(0, 0, 0, 0.06)',
    borderBottom: '1px solid rgba(52, 152, 219, 0.1)',
    position: 'sticky',
    top: 0,
    zIndex: 100,
    backdropFilter: 'blur(10px)',
  },
  headerTop: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerLeft: {
    flex: 1,
  },
  logoContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
  },
  logoIcon: {
    fontSize: '48px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '64px',
    height: '64px',
    background: 'linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%)',
    borderRadius: '16px',
    boxShadow: '0 4px 12px rgba(52, 152, 219, 0.15)',
    border: '2px solid rgba(52, 152, 219, 0.1)',
  },
  headerActions: {
    display: 'flex',
    alignItems: 'center',
    gap: '20px',
  },
  iconButton: {
    position: 'relative',
    background: 'white',
    border: '2px solid #f8f9fa',
    fontSize: '20px',
    cursor: 'pointer',
    padding: '10px',
    borderRadius: '12px',
    transition: 'all 0.2s ease',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
  },
  badge: {
    position: 'absolute',
    top: '2px',
    right: '2px',
    backgroundColor: '#e74c3c',
    color: 'white',
    borderRadius: '50%',
    width: '18px',
    height: '18px',
    fontSize: '11px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: '600',
  },
  userInfo: {
    padding: '10px 20px',
    background: 'linear-gradient(135deg, #3498db 0%, #2980b9 100%)',
    borderRadius: '12px',
    border: 'none',
    boxShadow: '0 4px 6px rgba(52, 152, 219, 0.3)',
  },
  userName: {
    fontSize: '14px',
    color: 'white',
    fontWeight: '600',
  },
  title: {
    fontSize: '1.75rem',
    background: 'linear-gradient(135deg, #2c3e50 0%, #3498db 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
    margin: 0,
    marginBottom: '4px',
    fontWeight: '700',
    letterSpacing: '-0.5px',
    lineHeight: '1.2',
  },
  subtitle: {
    fontSize: '0.875rem',
    color: '#7f8c8d',
    margin: 0,
    fontWeight: '400',
    lineHeight: '1.4',
  },
  main: {
    maxWidth: '1200px',
    margin: '0 auto',
    display: 'grid',
    gap: '30px',
    gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
  },
  statusCard: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  },
  statusItem: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '10px 0',
    borderBottom: '1px solid #ecf0f1',
  },
  linksCard: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  },
  linkGrid: {
    display: 'grid',
    gap: '15px',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
  },
  link: {
    display: 'block',
    padding: '15px',
    backgroundColor: '#3498db',
    color: 'white',
    textDecoration: 'none',
    borderRadius: '8px',
    textAlign: 'center',
    transition: 'background-color 0.3s ease',
  },
  dataCard: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    gridColumn: '1 / -1',
  },
  equivalencesCard: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    gridColumn: '1 / -1',
  },
  monitorCard: {
    backgroundColor: '#f8f9fa',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    gridColumn: '1 / -1',
  },
  rolesCard: {
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    gridColumn: '1 / -1',
    padding: '0',
  },
  preData: {
    backgroundColor: '#2c3e50',
    color: '#ecf0f1',
    padding: '20px',
    borderRadius: '8px',
    overflow: 'auto',
    fontSize: '14px',
  },
  viewContainer: {
    width: '100%',
  },
  contentCard: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    gridColumn: '1 / -1',
  },
  featureGrid: {
    display: 'grid',
    gap: '20px',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    marginTop: '30px',
  },
  featureCard: {
    backgroundColor: '#f8f9fa',
    padding: '20px',
    borderRadius: '8px',
    border: '1px solid #e9ecef',
    textAlign: 'center',
    transition: 'transform 0.2s ease, box-shadow 0.2s ease',
    cursor: 'pointer',
  },
};

export default App;