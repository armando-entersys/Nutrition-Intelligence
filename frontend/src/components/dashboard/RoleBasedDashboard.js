import React, { useState, useEffect } from 'react';
import axios from 'axios';
import authService from '../../services/authService';
import dashboardService from '../../services/dashboardService';

const RoleBasedDashboard = ({ currentRole: propCurrentRole, onNavigate }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [dashboardData, setDashboardData] = useState({});
  const [loading, setLoading] = useState(true);

  // Use prop role if provided, otherwise use user's primary role
  const currentRole = propCurrentRole || user?.primary_role;

  // Debug logging
  console.log('🔍 RoleBasedDashboard Debug:', {
    propCurrentRole,
    userPrimaryRole: user?.primary_role,
    finalCurrentRole: currentRole,
    user: user,
    timestamp: new Date().toISOString()
  });

  useEffect(() => {
    // Load real user data from authentication service
    try {
      const currentUser = authService.getCurrentUser();
      const isAuth = authService.isAuthenticated();

      if (currentUser && isAuth) {
        // Format user data to match expected structure
        const formattedUser = {
          id: currentUser.id,
          name: `${currentUser.first_name || ''} ${currentUser.last_name || ''}`.trim() || currentUser.username || currentUser.email,
          email: currentUser.email,
          username: currentUser.username,
          primary_role: currentUser.primary_role,
          secondary_roles: currentUser.secondary_roles || [],
          all_roles: currentUser.all_roles || [currentUser.primary_role],
          permissions: currentUser.permissions || []
        };

        setUser(formattedUser);
        setIsAuthenticated(true);
        console.log('✅ Loaded real user data:', formattedUser);
      } else {
        console.warn('⚠️ No authenticated user found');
        setIsAuthenticated(false);
      }
    } catch (error) {
      console.error('❌ Error loading user data:', error);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // Load dashboard data when role changes
    if (currentRole) {
      loadDashboardData(currentRole);
    }
  }, [currentRole]);

  const loadDashboardData = async (role) => {
    try {
      console.log(`📊 Loading dashboard data for role: ${role}`);

      // Llamar al servicio de dashboard para obtener estadísticas dinámicas
      const stats = await dashboardService.getDashboardStats(role);

      console.log(`✅ Dashboard stats loaded:`, stats);

      // Si es nutricionista, también cargar citas y alertas
      if (role === 'nutritionist') {
        const [appointments, alerts] = await Promise.all([
          dashboardService.getUpcomingAppointments(),
          dashboardService.getPatientAlerts()
        ]);

        setDashboardData({
          ...stats,
          appointments: appointments,
          alerts: alerts
        });
      } else {
        setDashboardData(stats);
      }

      // Mostrar mensaje si se están usando datos por defecto
      if (stats._isDefault) {
        console.warn(`⚠️ Using default data for ${role} - API endpoints not implemented yet`);
      }

    } catch (error) {
      console.error(`❌ Error loading dashboard data for ${role}:`, error);

      // En caso de error, usar datos por defecto
      const defaultData = dashboardService.getDefaultStats(role);
      setDashboardData(defaultData);
    }
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
        {console.log('🎯 Rendering dashboard for role:', currentRole, {
          isAdmin: currentRole === 'admin',
          isNutritionist: currentRole === 'nutritionist',
          isPatient: currentRole === 'patient'
        })}
        {currentRole === 'admin' && <AdminDashboard data={dashboardData} onNavigate={onNavigate} />}
        {currentRole === 'nutritionist' && <NutritionistDashboard data={dashboardData} user={user} onNavigate={onNavigate} />}
        {currentRole === 'patient' && <PatientDashboard data={dashboardData} user={user} onNavigate={onNavigate} />}
      </div>
    </div>
  );
};

// Componente Dashboard para Administrador
const AdminDashboard = ({ data, onNavigate }) => (
  <div style={styles.adminDashboard}>
    <h2>⚙️ Panel de Administración del Sistema</h2>

    {/* Métricas del sistema */}
    <div style={styles.systemMetrics}>
      <h3>📊 Estado del Sistema</h3>
      <div style={styles.metricsGrid}>
        <MetricCard
          title="Total Usuarios"
          value={data.totalUsers ?? 0}
          icon="👥"
          color="#3498db"
        />
        <MetricCard
          title="Nutricionistas Activos"
          value={data.activeNutritionists ?? 0}
          icon="🥗"
          color="#27ae60"
        />
        <MetricCard
          title="Pacientes Registrados"
          value={data.totalPatients ?? 0}
          icon="👤"
          color="#e74c3c"
        />
        <MetricCard
          title="Salud del Sistema"
          value={data.systemHealth || "Verificando..."}
          icon="⚡"
          color="#f39c12"
        />
      </div>
    </div>

    {/* Acciones Rápidas de Administración */}
    <div style={styles.quickActions}>
      <h3>⚡ Herramientas de Administración</h3>
      <div style={styles.actionGrid}>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('admin-users')}
        >
          <span style={styles.actionIcon}>👥</span>
          Gestionar Usuarios
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('admin-roles')}
        >
          <span style={styles.actionIcon}>🔐</span>
          Roles y Permisos
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('admin-views')}
        >
          <span style={styles.actionIcon}>📱</span>
          Vistas por Rol
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('admin-reports')}
        >
          <span style={styles.actionIcon}>📊</span>
          Reportes del Sistema
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('admin-logs')}
        >
          <span style={styles.actionIcon}>📋</span>
          Logs del Sistema
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('admin-database')}
        >
          <span style={styles.actionIcon}>💾</span>
          Base de Datos
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('admin-settings')}
        >
          <span style={styles.actionIcon}>⚙️</span>
          Configuración
        </button>
      </div>
    </div>

    {/* Estadísticas de uso del sistema */}
    <div style={styles.usageStats}>
      <h3>📈 Estadísticas de Uso del Sistema</h3>
      <div style={styles.metricsGrid}>
        <MetricCard
          title="Cálculos Este Mes"
          value={data.monthlyCalculations ?? 0}
          icon="🧮"
          color="#9b59b6"
        />
        <MetricCard
          title="Planes Generados"
          value={data.monthlyPlans ?? 0}
          icon="📋"
          color="#1abc9c"
        />
        <MetricCard
          title="Consultas IA"
          value={data.aiQueries ?? 0}
          icon="🤖"
          color="#f39c12"
        />
        <MetricCard
          title="Logins Hoy"
          value={data.dailyLogins ?? 0}
          icon="🚪"
          color="#3498db"
        />
      </div>
    </div>

    {/* Nota informativa */}
    <div style={{...styles.infoBox, marginTop: '20px'}}>
      <p style={{margin: 0, color: '#7f8c8d', fontSize: '14px'}}>
        💡 <strong>Panel Administrativo:</strong> Utiliza el menú lateral para acceder a las diferentes herramientas de administración del sistema.
      </p>
    </div>
  </div>
);

// Componente Dashboard para Nutricionista
const NutritionistDashboard = ({ data, user, onNavigate }) => (
  <div style={styles.nutritionistDashboard}>
    <h2>🥗 Panel Profesional - Nutricionista</h2>

    {/* Resumen del día */}
    <div style={styles.todaySummary}>
      <h3>📅 Agenda de Hoy</h3>
      <div style={styles.metricsRow}>
        <MetricCard
          title="Citas Hoy"
          value={data.todayAppointments ?? 0}
          icon="👥"
          color="#3498db"
        />
        <MetricCard
          title="Recordatorios 24h Pendientes"
          value={data.pending24hRecalls ?? 0}
          icon="📝"
          color="#e74c3c"
        />
        <MetricCard
          title="Fotos por Analizar"
          value={data.pendingPhotoAnalysis ?? 0}
          icon="📸"
          color="#f39c12"
        />
        <MetricCard
          title="Mensajes de Pacientes"
          value={data.unreadMessages ?? 0}
          icon="💬"
          color="#9b59b6"
        />
      </div>
    </div>

    {/* Próximas citas */}
    <div style={styles.appointmentsSection}>
      <h3>🗓️ Próximas Citas</h3>
      <div style={styles.appointmentsList}>
        {data.appointments && data.appointments.length > 0 ? (
          data.appointments.slice(0, 3).map((apt, index) => (
            <AppointmentItem
              key={apt.id || index}
              time={apt.time || apt.scheduled_time || '--:--'}
              patient={apt.patient_name || apt.patient || 'Sin nombre'}
              type={apt.type || apt.appointment_type || 'Consulta'}
              status={apt.status || 'pending'}
            />
          ))
        ) : (
          <div style={styles.emptyState}>
            <p style={{color: '#7f8c8d', textAlign: 'center', padding: '20px'}}>
              📅 No hay citas programadas
            </p>
          </div>
        )}
      </div>
      <button
        style={styles.viewAllButton}
        onClick={() => onNavigate && onNavigate('appointments')}
      >
        Ver Agenda Completa
      </button>
    </div>

    {/* Pacientes que requieren atención */}
    <div style={styles.alertsSection}>
      <h3>⚠️ Requieren Atención</h3>
      <div style={styles.alertsList}>
        {data.alerts && data.alerts.length > 0 ? (
          data.alerts.slice(0, 3).map((alert, index) => (
            <AlertItem
              key={alert.id || index}
              patient={alert.patient_name || alert.patient || 'Paciente'}
              alert={alert.message || alert.alert || alert.description || 'Alerta'}
              priority={alert.priority || 'medium'}
              patientId={alert.patient_id || alert.patientId}
              onNavigate={onNavigate}
            />
          ))
        ) : (
          <div style={styles.emptyState}>
            <p style={{color: '#27ae60', textAlign: 'center', padding: '20px'}}>
              ✅ No hay alertas pendientes
            </p>
          </div>
        )}
      </div>
    </div>

    {/* Herramientas profesionales */}
    <div style={styles.quickActions}>
      <h3>🛠️ Herramientas Clínicas</h3>
      <div style={styles.actionGrid}>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('expediente')}
        >
          <span style={styles.actionIcon}>📋</span>
          Nuevo Expediente
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('calculator')}
        >
          <span style={styles.actionIcon}>📊</span>
          Calcular Requerimientos
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('dietas')}
        >
          <span style={styles.actionIcon}>🍽️</span>
          Generar Dieta
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('equivalences')}
        >
          <span style={styles.actionIcon}>🥗</span>
          Sistema de Equivalentes
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('analisis-fotos')}
        >
          <span style={styles.actionIcon}>📸</span>
          Análisis de Fotos
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('chat-ia')}
        >
          <span style={styles.actionIcon}>💬</span>
          Chat IA Nutricional
        </button>
      </div>
    </div>

    {/* Estadísticas del mes */}
    <div style={styles.monthlyStats}>
      <h3>📈 Estadísticas del Mes</h3>
      <div style={styles.metricsGrid}>
        <MetricCard
          title="Pacientes Activos"
          value={data.activePatients ?? 0}
          icon="👥"
          color="#3498db"
        />
        <MetricCard
          title="Consultas Realizadas"
          value={data.monthlyConsultations ?? 0}
          icon="🗓️"
          color="#27ae60"
        />
        <MetricCard
          title="Planes Nutricionales"
          value={data.monthlyPlans ?? 0}
          icon="📋"
          color="#e74c3c"
        />
        <MetricCard
          title="Satisfacción Promedio"
          value={data.avgPatientSatisfaction ? `${data.avgPatientSatisfaction}/5` : 'N/A'}
          icon="⭐"
          color="#f39c12"
        />
      </div>
    </div>

    {/* Si también es paciente, mostrar acceso rápido */}
    {user.all_roles.includes('patient') && (
      <div style={styles.hybridSection}>
        <h3>🔄 Vista Personal</h3>
        <p>Tienes acceso a tu propia vista como paciente.</p>
        <button
          style={styles.hybridButton}
          onClick={() => onNavigate && onNavigate('switch-role/patient')}
        >
          Ver Mi Plan Personal
        </button>
      </div>
    )}
  </div>
);

// Componente Dashboard para Paciente
const PatientDashboard = ({ data, user, onNavigate }) => (
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
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('recordatorio')}
        >
          <span style={styles.actionIcon}>✅</span>
          Registrar Comida
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('recipes')}
        >
          <span style={styles.actionIcon}>⭐</span>
          Calificar Receta
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('gamificacion')}
        >
          <span style={styles.actionIcon}>📊</span>
          Ver Progreso
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('analisis-fotos')}
        >
          <span style={styles.actionIcon}>📸</span>
          Analizar Comida
        </button>
      </div>
    </div>

    {/* Herramientas disponibles para pacientes */}
    <div style={styles.patientTools}>
      <h3>🛠️ Mis Herramientas</h3>
      <div style={styles.actionGrid}>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('analisis-fotos')}
        >
          <span style={styles.actionIcon}>📸</span>
          Análisis de Fotos IA
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('chat-ia')}
        >
          <span style={styles.actionIcon}>💬</span>
          Chat Nutriólogo IA
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('scanner')}
        >
          <span style={styles.actionIcon}>📱</span>
          Escáner NOM-051
        </button>
        <button
          style={styles.quickActionButton}
          onClick={() => onNavigate && onNavigate('gamificacion')}
        >
          <span style={styles.actionIcon}>🏆</span>
          Gamificación
        </button>
      </div>
    </div>

    {/* Si también es nutricionista, mostrar acceso profesional */}
    {user.all_roles.includes('nutritionist') && (
      <div style={styles.hybridSection}>
        <h3>👨‍⚕️ Acceso Profesional</h3>
        <p>Como nutricionista, puedes acceder a las herramientas profesionales para gestionar otros pacientes.</p>
        <button
          style={styles.hybridButton}
          onClick={() => onNavigate && onNavigate('switch-role/nutritionist')}
        >
          Ir a Vista Profesional
        </button>
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

// Componente para mostrar citas
const AppointmentItem = ({ time, patient, type, status }) => {
  const statusColors = {
    confirmed: '#27ae60',
    pending: '#f39c12',
    cancelled: '#e74c3c'
  };

  const statusLabels = {
    confirmed: 'Confirmada',
    pending: 'Pendiente',
    cancelled: 'Cancelada'
  };

  return (
    <div style={styles.appointmentItem}>
      <div style={styles.appointmentTime}>{time}</div>
      <div style={styles.appointmentDetails}>
        <div style={styles.appointmentPatient}>{patient}</div>
        <div style={styles.appointmentType}>{type}</div>
      </div>
      <div
        style={{
          ...styles.appointmentStatus,
          backgroundColor: statusColors[status],
        }}
      >
        {statusLabels[status]}
      </div>
    </div>
  );
};

// Componente para alertas de pacientes
const AlertItem = ({ patient, alert, priority, patientId, onNavigate }) => {
  const priorityColors = {
    high: '#e74c3c',
    medium: '#f39c12',
    low: '#3498db'
  };

  const handleViewPatient = () => {
    if (onNavigate && patientId) {
      onNavigate(`patient-detail/${patientId}`);
    } else if (onNavigate) {
      onNavigate('patients');
    }
  };

  return (
    <div style={{
      ...styles.alertItem,
      borderLeft: `4px solid ${priorityColors[priority]}`
    }}>
      <div style={styles.alertPatient}>
        <span style={styles.alertIcon}>👤</span>
        {patient}
      </div>
      <div style={styles.alertText}>{alert}</div>
      <button
        style={styles.alertButton}
        onClick={handleViewPatient}
      >
        Ver Expediente
      </button>
    </div>
  );
};

// Componente para tarjetas de roles
const RoleCard = ({ role, name, users, permissions, color }) => {
  return (
    <div style={{...styles.roleCard, borderTop: `4px solid ${color}`}}>
      <div style={styles.roleHeader}>
        <h4 style={{...styles.roleName, color}}>{name}</h4>
        <span style={styles.roleUsers}>{users} usuarios</span>
      </div>
      <div style={styles.permissionsList}>
        <p style={styles.permissionsLabel}>Permisos:</p>
        {permissions.map((permission, index) => (
          <div key={index} style={styles.permissionItem}>
            <span style={styles.permissionIcon}>✓</span>
            {permission}
          </div>
        ))}
      </div>
      <button style={{...styles.editRoleButton, backgroundColor: color}}>
        Editar Rol
      </button>
    </div>
  );
};

// Componente tabla de vistas por rol
const ViewsByRoleTable = () => {
  const views = [
    { name: 'Dashboard', nutritionist: true, patient: true, admin: true },
    { name: 'Expediente Clínico', nutritionist: true, patient: false, admin: true },
    { name: 'Dietas Dinámicas', nutritionist: true, patient: false, admin: true },
    { name: 'Gestión de Pacientes', nutritionist: true, patient: false, admin: true },
    { name: 'Alimentos', nutritionist: true, patient: false, admin: true },
    { name: 'Recetas', nutritionist: true, patient: false, admin: true },
    { name: 'Equivalencias', nutritionist: true, patient: false, admin: true },
    { name: 'Análisis de Fotos', nutritionist: true, patient: true, admin: true },
    { name: 'Chat IA', nutritionist: true, patient: true, admin: true },
    { name: 'Escáner NOM-051', nutritionist: true, patient: true, admin: true },
    { name: 'Gamificación', nutritionist: true, patient: true, admin: true },
    { name: 'Calculadora', nutritionist: true, patient: false, admin: true },
    { name: 'Panel Administrativo', nutritionist: false, patient: false, admin: true },
    { name: 'Gestión de Usuarios', nutritionist: false, patient: false, admin: true },
    { name: 'Roles y Permisos', nutritionist: false, patient: false, admin: true },
    { name: 'Configurar Vistas', nutritionist: false, patient: false, admin: true },
    { name: 'Reportes del Sistema', nutritionist: false, patient: false, admin: true },
    { name: 'Logs del Sistema', nutritionist: false, patient: false, admin: true },
  ];

  return (
    <div style={styles.viewsTable}>
      <div style={styles.tableHeader}>
        <div style={styles.tableCell}>Vista / Sección</div>
        <div style={styles.tableCell}>Nutricionista</div>
        <div style={styles.tableCell}>Paciente</div>
        <div style={styles.tableCell}>Admin</div>
      </div>
      {views.map((view, index) => (
        <div key={index} style={styles.tableRow}>
          <div style={styles.tableCell}>{view.name}</div>
          <div style={styles.tableCell}>
            <span style={{...styles.accessBadge, backgroundColor: view.nutritionist ? '#27ae60' : '#e74c3c'}}>
              {view.nutritionist ? '✓' : '✗'}
            </span>
          </div>
          <div style={styles.tableCell}>
            <span style={{...styles.accessBadge, backgroundColor: view.patient ? '#27ae60' : '#e74c3c'}}>
              {view.patient ? '✓' : '✗'}
            </span>
          </div>
          <div style={styles.tableCell}>
            <span style={{...styles.accessBadge, backgroundColor: view.admin ? '#27ae60' : '#e74c3c'}}>
              {view.admin ? '✓' : '✗'}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};

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
  todaySummary: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '25px',
  },
  metricsRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '15px',
    marginTop: '15px',
  },
  appointmentsSection: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '25px',
  },
  appointmentsList: {
    marginTop: '15px',
    marginBottom: '15px',
  },
  appointmentItem: {
    display: 'flex',
    alignItems: 'center',
    padding: '15px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    marginBottom: '10px',
    gap: '15px',
  },
  appointmentTime: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#2c3e50',
    minWidth: '80px',
  },
  appointmentDetails: {
    flex: 1,
  },
  appointmentPatient: {
    fontSize: '15px',
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: '4px',
  },
  appointmentType: {
    fontSize: '13px',
    color: '#7f8c8d',
  },
  appointmentStatus: {
    padding: '6px 12px',
    borderRadius: '20px',
    fontSize: '12px',
    fontWeight: '500',
    color: 'white',
  },
  viewAllButton: {
    width: '100%',
    padding: '12px',
    backgroundColor: '#f8f9fa',
    border: '2px solid #e9ecef',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
    color: '#2c3e50',
    transition: 'all 0.3s ease',
  },
  alertsSection: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '25px',
  },
  alertsList: {
    marginTop: '15px',
  },
  alertItem: {
    padding: '15px',
    backgroundColor: '#fff5f5',
    borderRadius: '8px',
    marginBottom: '12px',
    borderLeft: '4px solid #e74c3c',
  },
  alertPatient: {
    fontSize: '15px',
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: '8px',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  alertIcon: {
    fontSize: '16px',
  },
  alertText: {
    fontSize: '14px',
    color: '#7f8c8d',
    marginBottom: '10px',
  },
  alertButton: {
    padding: '8px 16px',
    backgroundColor: '#3498db',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '13px',
    fontWeight: '500',
    transition: 'background-color 0.3s ease',
  },
  monthlyStats: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '25px',
  },
  systemMetrics: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '25px',
  },
  rolesSection: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '25px',
  },
  rolesGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px',
    marginTop: '20px',
  },
  roleCard: {
    backgroundColor: '#f8f9fa',
    padding: '20px',
    borderRadius: '10px',
    borderTop: '4px solid #3498db',
  },
  roleHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '15px',
  },
  roleName: {
    fontSize: '18px',
    fontWeight: '600',
    margin: 0,
  },
  roleUsers: {
    fontSize: '13px',
    color: '#7f8c8d',
    backgroundColor: 'white',
    padding: '4px 10px',
    borderRadius: '12px',
  },
  permissionsList: {
    marginBottom: '15px',
  },
  permissionsLabel: {
    fontSize: '13px',
    fontWeight: '600',
    color: '#7f8c8d',
    marginBottom: '8px',
  },
  permissionItem: {
    fontSize: '13px',
    color: '#2c3e50',
    padding: '6px 0',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  permissionIcon: {
    color: '#27ae60',
    fontWeight: 'bold',
  },
  editRoleButton: {
    width: '100%',
    padding: '10px',
    backgroundColor: '#3498db',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
    transition: 'opacity 0.3s ease',
  },
  viewsSection: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '25px',
  },
  viewsTable: {
    marginTop: '20px',
    overflow: 'auto',
  },
  tableHeader: {
    display: 'grid',
    gridTemplateColumns: '2fr 1fr 1fr 1fr',
    backgroundColor: '#2c3e50',
    color: 'white',
    padding: '12px',
    borderRadius: '8px 8px 0 0',
    fontWeight: '600',
    fontSize: '14px',
  },
  tableRow: {
    display: 'grid',
    gridTemplateColumns: '2fr 1fr 1fr 1fr',
    padding: '12px',
    borderBottom: '1px solid #e9ecef',
    alignItems: 'center',
  },
  tableCell: {
    padding: '8px',
    textAlign: 'center',
  },
  accessBadge: {
    width: '30px',
    height: '30px',
    borderRadius: '50%',
    backgroundColor: '#27ae60',
    color: 'white',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 'bold',
    fontSize: '14px',
  },
  usageStats: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '25px',
  },
  patientTools: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginTop: '25px',
  },
  infoBox: {
    backgroundColor: '#e3f2fd',
    padding: '15px 20px',
    borderRadius: '8px',
    border: '1px solid #90caf9',
    marginTop: '20px',
  },
};

export default RoleBasedDashboard;