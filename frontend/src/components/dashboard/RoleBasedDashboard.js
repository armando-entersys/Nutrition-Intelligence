import React, { useState, useEffect } from 'react';
import axios from 'axios';

const RoleBasedDashboard = ({ currentRole: propCurrentRole, onNavigate }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [dashboardData, setDashboardData] = useState({});
  const [loading, setLoading] = useState(true);

  // Use prop role if provided, otherwise use user's primary role
  const currentRole = propCurrentRole || user?.primary_role;

  // Simulated user data (en una implementación real vendría del contexto de auth)
  const mockUser = {
    id: 1,
    name: "Dra. Sara Gallegos",
    email: "contacto@saragallegos.com",
    website: "https://saragallegos.com/",
    primary_role: "nutritionist",
    secondary_roles: ["patient"],
    all_roles: ["nutritionist", "patient"],
    permissions: [
      "create_meal_plans", "calculate_nutrition", "manage_patients",
      "view_equivalences", "create_recipes", "assign_diets",
      "view_meal_plan", "track_consumption", "rate_recipes", "view_progress"
    ]
  };

  useEffect(() => {
    // Simular carga de datos de usuario
    setTimeout(() => {
      setUser(mockUser);
      setIsAuthenticated(true);
      setLoading(false);
    }, 1000);
  }, []);

  useEffect(() => {
    // Load dashboard data when role changes
    if (currentRole) {
      loadDashboardData(currentRole);
    }
  }, [currentRole]);

  const loadDashboardData = async (role) => {
    // Simular carga de datos específicos por rol
    const data = {
      admin: {
        totalUsers: 234,
        activeNutritionists: 45,
        activePatients: 189,
        systemHealth: "Excellent",
        monthlyCalculations: 1250,
        dailyLogins: 67
      },
      nutritionist: {
        activePatients: 23,
        weeklyPlansCreated: 8,
        pendingReviews: 5,
        avgPatientSatisfaction: 4.7,
        thisWeekConsultations: 12,
        completedPlans: 156
      },
      patient: {
        currentPlan: "Plan de Mantenimiento - Semana 3",
        todayProgress: 78,
        weeklyAdherence: 85,
        favoriteRecipes: 12,
        nextAppointment: "2025-07-25",
        totalEquivalentsToday: 24
      }
    };

    setDashboardData(data[role] || {});
  };

  const hasPermission = (permission) => {
    return user?.permissions?.includes(permission) || false;
  };

  if (loading) {
    return (
      <div style={styles.loadingContainer}>
        <div style={styles.loader}>Cargando dashboard...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div style={styles.authContainer}>
        <h2>Acceso Requerido</h2>
        <p>Por favor inicia sesión para ver tu dashboard personalizado.</p>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      {/* Header con información de usuario */}
      <div style={styles.header}>
        <div style={styles.userInfo}>
          <h1>¡Hola, {user.name}!</h1>
          <p style={styles.userEmail}>{user.email}</p>
        </div>
      </div>

      {/* Dashboard específico por rol */}
      <div style={styles.dashboardContent}>
        {currentRole === 'admin' && <AdminDashboard data={dashboardData} onNavigate={onNavigate} />}
        {currentRole === 'nutritionist' && <NutritionistDashboard data={dashboardData} user={user} onNavigate={onNavigate} />}
        {currentRole === 'patient' && <PatientDashboard data={dashboardData} user={user} onNavigate={onNavigate} />}
      </div>
    </div>
  );
};

// Componente Dashboard para Administrador
const AdminDashboard = ({ data }) => (
  <div style={styles.adminDashboard}>
    <h2>🛠️ Panel de Administración</h2>
    <div style={styles.metricsGrid}>
      <MetricCard 
        title="Total Usuarios" 
        value={data.totalUsers} 
        icon="👥" 
        color="#3498db"
      />
      <MetricCard 
        title="Nutricionistas Activos" 
        value={data.activeNutritionists} 
        icon="🥗" 
        color="#27ae60"
      />
      <MetricCard 
        title="Pacientes Activos" 
        value={data.activePatients} 
        icon="👤" 
        color="#e74c3c"
      />
      <MetricCard 
        title="Salud del Sistema" 
        value={data.systemHealth} 
        icon="⚡" 
        color="#f39c12"
      />
      <MetricCard 
        title="Cálculos Mensuales" 
        value={data.monthlyCalculations} 
        icon="📊" 
        color="#9b59b6"
      />
      <MetricCard 
        title="Logins Hoy" 
        value={data.dailyLogins} 
        icon="🚪" 
        color="#1abc9c"
      />
    </div>
    <div style={styles.adminActions}>
      <button style={styles.actionButton}>Gestionar Usuarios</button>
      <button style={styles.actionButton}>Ver Logs del Sistema</button>
      <button style={styles.actionButton}>Configuración</button>
      <button style={styles.actionButton}>Reportes</button>
    </div>
  </div>
);

// Componente Dashboard para Nutricionista
const NutritionistDashboard = ({ data, user, onNavigate }) => (
  <div style={styles.nutritionistDashboard}>
    <h2>🥗 Dashboard del Nutricionista</h2>
    <div style={styles.metricsGrid}>
      <MetricCard 
        title="Pacientes Activos" 
        value={data.activePatients} 
        icon="👥" 
        color="#3498db"
      />
      <MetricCard 
        title="Planes Creados (Esta Semana)" 
        value={data.weeklyPlansCreated} 
        icon="📋" 
        color="#27ae60"
      />
      <MetricCard 
        title="Revisiones Pendientes" 
        value={data.pendingReviews} 
        icon="⏰" 
        color="#e74c3c"
      />
      <MetricCard 
        title="Satisfacción Promedio" 
        value={`${data.avgPatientSatisfaction}/5`} 
        icon="⭐" 
        color="#f39c12"
      />
      <MetricCard 
        title="Consultas Esta Semana" 
        value={data.thisWeekConsultations} 
        icon="🗓️" 
        color="#9b59b6"
      />
      <MetricCard 
        title="Planes Completados" 
        value={data.completedPlans} 
        icon="✅" 
        color="#1abc9c"
      />
    </div>
    
    <div style={styles.quickActions}>
      <h3>🚀 Acciones Rápidas</h3>
      <div style={styles.actionGrid}>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('calculator')}
        >
          <span style={styles.actionIcon}>📊</span>
          Calcular Requerimientos
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('patients')}
        >
          <span style={styles.actionIcon}>📋</span>
          Crear Plan Semanal
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('patients')}
        >
          <span style={styles.actionIcon}>👤</span>
          Gestionar Pacientes
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('recipes')}
        >
          <span style={styles.actionIcon}>🍽️</span>
          Crear Receta
        </button>
      </div>
    </div>

    {/* Si también es paciente, mostrar acceso rápido */}
    {user.all_roles.includes('patient') && (
      <div style={styles.hybridSection}>
        <h3>🔄 Acceso Híbrido</h3>
        <p>Como también eres paciente, puedes cambiar a tu vista de paciente para gestionar tu propio plan nutricional.</p>
        <button style={styles.hybridButton}>Ver mi Plan como Paciente</button>
      </div>
    )}
  </div>
);

// Componente Dashboard para Paciente  
const PatientDashboard = ({ data, user }) => (
  <div style={styles.patientDashboard}>
    <h2>🌟 Mi Dashboard Nutricional</h2>
    
    <div style={styles.currentPlanCard}>
      <h3>📋 Plan Actual</h3>
      <p style={styles.planName}>{data.currentPlan}</p>
      <div style={styles.progressBar}>
        <div 
          style={{...styles.progressFill, width: `${data.todayProgress}%`}}
        />
      </div>
      <p>Progreso de hoy: {data.todayProgress}%</p>
    </div>

    <div style={styles.metricsGrid}>
      <MetricCard 
        title="Adherencia Semanal" 
        value={`${data.weeklyAdherence}%`} 
        icon="📈" 
        color="#27ae60"
      />
      <MetricCard 
        title="Recetas Favoritas" 
        value={data.favoriteRecipes} 
        icon="❤️" 
        color="#e74c3c"
      />
      <MetricCard 
        title="Próxima Cita" 
        value={data.nextAppointment} 
        icon="📅" 
        color="#3498db"
      />
      <MetricCard 
        title="Equivalentes Hoy" 
        value={data.totalEquivalentsToday} 
        icon="🥗" 
        color="#f39c12"
      />
    </div>

    <div style={styles.quickActions}>
      <h3>🎯 Acciones de Hoy</h3>
      <div style={styles.actionGrid}>
        <button style={styles.quickActionButton}>
          <span style={styles.actionIcon}>✅</span>
          Registrar Comida
        </button>
        <button style={styles.quickActionButton}>
          <span style={styles.actionIcon}>⭐</span>
          Calificar Receta
        </button>
        <button style={styles.quickActionButton}>
          <span style={styles.actionIcon}>📊</span>
          Ver Progreso
        </button>
        <button style={styles.quickActionButton}>
          <span style={styles.actionIcon}>🔄</span>
          Solicitar Cambio
        </button>
      </div>
    </div>

    {/* Si también es nutricionista, mostrar acceso profesional */}
    {user.all_roles.includes('nutritionist') && (
      <div style={styles.hybridSection}>
        <h3>👨‍⚕️ Acceso Profesional</h3>
        <p>Como nutricionista, puedes acceder a las herramientas profesionales para gestionar otros pacientes.</p>
        <button style={styles.hybridButton}>Ir a Vista Profesional</button>
      </div>
    )}
  </div>
);

// Componente reutilizable para métricas
const MetricCard = ({ title, value, icon, color }) => (
  <div style={{...styles.metricCard, borderLeft: `4px solid ${color}`}}>
    <div style={styles.metricHeader}>
      <span style={styles.metricIcon}>{icon}</span>
      <span style={styles.metricTitle}>{title}</span>
    </div>
    <div style={{...styles.metricValue, color}}>{value}</div>
  </div>
);

// Estilos
const styles = {
  container: {
    padding: '20px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif',
    backgroundColor: '#f8f9fa',
    minHeight: '100vh',
  },
  loadingContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '200px',
  },
  loader: {
    color: '#7f8c8d',
    fontSize: '16px',
  },
  authContainer: {
    textAlign: 'center',
    padding: '50px',
    backgroundColor: 'white',
    borderRadius: '10px',
    margin: '50px auto',
    maxWidth: '400px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '30px',
    flexWrap: 'wrap',
  },
  userInfo: {
    flex: 1,
  },
  userEmail: {
    color: '#7f8c8d',
    margin: '5px 0 0 0',
  },
  dashboardContent: {
    marginBottom: '30px',
  },
  metricsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
    marginBottom: '30px',
  },
  metricCard: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
    borderLeft: '4px solid #3498db',
  },
  metricHeader: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '10px',
  },
  metricIcon: {
    fontSize: '20px',
    marginRight: '10px',
  },
  metricTitle: {
    fontSize: '14px',
    color: '#7f8c8d',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  metricValue: {
    fontSize: '28px',
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  quickActions: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '20px',
  },
  actionGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '15px',
    marginTop: '15px',
  },
  quickActionButton: {
    display: 'flex',
    alignItems: 'center',
    padding: '15px 20px',
    backgroundColor: '#f8f9fa',
    border: '2px solid #e9ecef',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
    transition: 'all 0.3s ease',
    ':hover': {
      backgroundColor: '#e9ecef',
      transform: 'translateY(-2px)',
    },
  },
  actionIcon: {
    fontSize: '18px',
    marginRight: '10px',
  },
  adminActions: {
    display: 'flex',
    gap: '15px',
    flexWrap: 'wrap',
    marginTop: '20px',
  },
  actionButton: {
    padding: '12px 24px',
    backgroundColor: '#3498db',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
    transition: 'background-color 0.3s ease',
  },
  currentPlanCard: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '25px',
  },
  planName: {
    fontSize: '18px',
    fontWeight: '600',
    color: '#2c3e50',
    margin: '10px 0',
  },
  progressBar: {
    width: '100%',
    height: '8px',
    backgroundColor: '#e9ecef',
    borderRadius: '4px',
    overflow: 'hidden',
    marginBottom: '10px',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#27ae60',
    transition: 'width 0.3s ease',
  },
  hybridSection: {
    backgroundColor: '#f8f9fa',
    border: '2px dashed #dee2e6',
    padding: '20px',
    borderRadius: '10px',
    marginTop: '25px',
    textAlign: 'center',
  },
  hybridButton: {
    padding: '10px 20px',
    backgroundColor: '#6c5ce7',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
    marginTop: '10px',
  },
};

export default RoleBasedDashboard;