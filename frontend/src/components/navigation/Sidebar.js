import React from 'react';

const Sidebar = ({ currentView, setCurrentView, isCollapsed, toggleSidebar, currentRole, setCurrentRole, userRoles }) => {
  const navigationItems = [
    { id: 'dashboard', icon: '🏠', label: 'Dashboard', description: 'Panel principal' },
    { id: 'foods', icon: '🥗', label: 'Alimentos', description: 'Base de datos de alimentos', roles: ['nutritionist', 'admin'] },
    { id: 'recipes', icon: '🍽️', label: 'Recetas', description: 'Recetas y menús', roles: ['nutritionist', 'admin'] },
    { id: 'equivalences', icon: '⚖️', label: 'Equivalencias', description: 'Sistema de equivalencias', roles: ['nutritionist', 'admin'] },
    { id: 'patients', icon: '👥', label: 'Pacientes', description: 'Gestión de pacientes', roles: ['nutritionist', 'admin'] },
    { id: 'calculator', icon: '🧮', label: 'Calculadora', description: 'Herramientas de cálculo', roles: ['nutritionist', 'admin'] },
  ];

  const roleLabels = {
    nutritionist: '👨‍⚕️ Nutricionista',
    patient: '👤 Paciente',
    admin: '⚙️ Admin'
  };

  const handleRoleChange = (newRole) => {
    setCurrentRole(newRole);
    // Reset to dashboard when changing role
    setCurrentView('dashboard');
  };

  // Filter navigation items based on current role
  const visibleNavigationItems = navigationItems.filter(item =>
    !item.roles || item.roles.includes(currentRole)
  );

  return (
    <div style={{
      ...styles.sidebar,
      width: isCollapsed ? '80px' : '280px',
    }}>
      {/* Header */}
      <div style={styles.sidebarHeader}>
        <button onClick={toggleSidebar} style={styles.toggleButton}>
          {isCollapsed ? '▶️' : '◀️'}
        </button>
        {!isCollapsed && (
          <div style={styles.logo}>
            <h3 style={styles.logoText}>Nutrition Intelligence</h3>
          </div>
        )}
      </div>

      {/* Navigation Items */}
      <nav style={styles.navigation}>
        {visibleNavigationItems.map((item) => {
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              style={{
                ...styles.navItem,
                ...(isActive ? styles.activeNavItem : {}),
                justifyContent: isCollapsed ? 'center' : 'flex-start',
              }}
              onClick={() => setCurrentView(item.id)}
              title={isCollapsed ? item.label : ''}
              onMouseEnter={(e) => {
                if (!isActive) {
                  e.currentTarget.style.backgroundColor = 'rgba(52, 152, 219, 0.1)';
                }
              }}
              onMouseLeave={(e) => {
                if (!isActive) {
                  e.currentTarget.style.backgroundColor = 'transparent';
                }
              }}
            >
              <span style={styles.navIcon}>{item.icon}</span>
              {!isCollapsed && (
                <div style={styles.navContent}>
                  <span style={styles.navLabel}>{item.label}</span>
                  <span style={styles.navDescription}>{item.description}</span>
                </div>
              )}
            </button>
          );
        })}
      </nav>

      {/* Role Selector */}
      {!isCollapsed && userRoles && userRoles.length > 1 && (
        <div style={styles.roleSelectorContainer}>
          <div style={styles.roleSelectorLabel}>Cambiar Vista:</div>
          <select
            value={currentRole}
            onChange={(e) => handleRoleChange(e.target.value)}
            style={styles.roleSelector}
          >
            {userRoles.map(role => (
              <option key={role} value={role}>
                {roleLabels[role]}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Footer */}
      {!isCollapsed && (
        <div style={styles.sidebarFooter}>
          <div style={styles.userInfo}>
            <div style={styles.userAvatar}>👤</div>
            <div style={styles.userDetails}>
              <span style={styles.userName}>Dra. Sara Gallegos</span>
              <span style={styles.userRole}>{roleLabels[currentRole] || 'Nutricionista'}</span>
            </div>
          </div>
          <a
            href="https://saragallegos.com/"
            target="_blank"
            rel="noopener noreferrer"
            style={styles.websiteLink}
          >
            🌐 saragallegos.com
          </a>
        </div>
      )}
    </div>
  );
};

const styles = {
  sidebar: {
    background: 'linear-gradient(180deg, #2c3e50 0%, #34495e 100%)',
    color: 'white',
    height: '100vh',
    position: 'fixed',
    left: 0,
    top: 0,
    display: 'flex',
    flexDirection: 'column',
    transition: 'width 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    zIndex: 1000,
    boxShadow: '4px 0 20px rgba(0, 0, 0, 0.15)',
  },
  sidebarHeader: {
    padding: '20px',
    borderBottom: '1px solid #34495e',
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
  },
  toggleButton: {
    background: 'none',
    border: 'none',
    color: 'white',
    fontSize: '18px',
    cursor: 'pointer',
    padding: '5px',
  },
  logo: {
    flex: 1,
  },
  logoText: {
    margin: 0,
    fontSize: '18px',
    fontWeight: '600',
  },
  navigation: {
    flex: 1,
    padding: '20px 0',
  },
  navItem: {
    width: '100%',
    padding: '15px 20px',
    border: 'none',
    background: 'transparent',
    color: 'rgba(255, 255, 255, 0.9)',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
    transition: 'all 0.2s ease',
    textAlign: 'left',
    position: 'relative',
  },
  activeNavItem: {
    backgroundColor: 'rgba(52, 152, 219, 0.3)',
    borderLeft: '4px solid #3498db',
    color: 'white',
    fontWeight: '600',
  },
  navIcon: {
    fontSize: '20px',
    minWidth: '20px',
  },
  navContent: {
    display: 'flex',
    flexDirection: 'column',
    gap: '2px',
  },
  navLabel: {
    fontSize: '16px',
    fontWeight: '500',
  },
  navDescription: {
    fontSize: '12px',
    opacity: 0.8,
  },
  sidebarFooter: {
    padding: '20px',
    borderTop: '1px solid #34495e',
  },
  userInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },
  userAvatar: {
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    backgroundColor: '#3498db',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '18px',
  },
  userDetails: {
    display: 'flex',
    flexDirection: 'column',
  },
  userName: {
    fontSize: '14px',
    fontWeight: '500',
  },
  userRole: {
    fontSize: '12px',
    opacity: 0.8,
  },
  websiteLink: {
    display: 'block',
    marginTop: '12px',
    padding: '8px 12px',
    backgroundColor: '#34495e',
    color: 'white',
    textDecoration: 'none',
    borderRadius: '6px',
    fontSize: '12px',
    textAlign: 'center',
    transition: 'background-color 0.2s',
    ':hover': {
      backgroundColor: '#3498db',
    }
  },
  roleSelectorContainer: {
    padding: '20px',
    borderTop: '1px solid #34495e',
    borderBottom: '1px solid #34495e',
  },
  roleSelectorLabel: {
    fontSize: '12px',
    opacity: 0.8,
    marginBottom: '8px',
    fontWeight: '500',
  },
  roleSelector: {
    width: '100%',
    padding: '10px 12px',
    backgroundColor: '#34495e',
    color: 'white',
    border: '1px solid #3498db',
    borderRadius: '6px',
    fontSize: '14px',
    cursor: 'pointer',
    transition: 'all 0.2s',
    outline: 'none',
  },
};

export default Sidebar;