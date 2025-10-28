import React, { useState, useRef, useEffect } from 'react';

const NotificationsPanel = ({ onClose, onNavigate }) => {
  const [notifications, setNotifications] = useState([
    {
      id: 1,
      type: 'info',
      title: 'Nuevo paciente asignado',
      message: 'María González ha sido asignada a tu lista',
      time: 'Hace 5 minutos',
      read: false,
      icon: '👤',
      action: { type: 'navigate', target: 'patients' }
    },
    {
      id: 2,
      type: 'warning',
      title: 'Plan nutricional próximo a vencer',
      message: 'El plan de Carlos Rodríguez vence en 3 días',
      time: 'Hace 1 hora',
      read: false,
      icon: '⏰',
      action: { type: 'navigate', target: 'patients' }
    },
    {
      id: 3,
      type: 'success',
      title: 'Receta guardada',
      message: 'Tu nueva receta "Ensalada César" se guardó correctamente',
      time: 'Hace 2 horas',
      read: true,
      icon: '✅',
      action: { type: 'navigate', target: 'recipes' }
    },
    {
      id: 4,
      type: 'info',
      title: 'Actualización del sistema',
      message: 'Nueva versión disponible con mejoras de rendimiento',
      time: 'Ayer',
      read: true,
      icon: '🔄',
      action: { type: 'navigate', target: 'dashboard' }
    }
  ]);

  const panelRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (panelRef.current && !panelRef.current.contains(event.target)) {
        onClose();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [onClose]);

  const markAsRead = (id) => {
    setNotifications(prev =>
      prev.map(notif =>
        notif.id === id ? { ...notif, read: true } : notif
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev =>
      prev.map(notif => ({ ...notif, read: true }))
    );
  };

  const deleteNotification = (id) => {
    setNotifications(prev => prev.filter(notif => notif.id !== id));
  };

  const handleNotificationClick = (notification) => {
    // Marcar como leída
    if (!notification.read) {
      markAsRead(notification.id);
    }

    // Navegar si tiene acción
    if (notification.action && notification.action.type === 'navigate') {
      onNavigate(notification.action.target);
      onClose();
    }
  };

  const handleViewAll = () => {
    // Por ahora navega a dashboard, en el futuro podría ser una página de notificaciones
    onNavigate('dashboard');
    onClose();
  };

  const unreadCount = notifications.filter(n => !n.read).length;

  const getTypeColor = (type) => {
    const colors = {
      info: '#3498db',
      success: '#27ae60',
      warning: '#f39c12',
      error: '#e74c3c'
    };
    return colors[type] || '#95a5a6';
  };

  return (
    <div ref={panelRef} style={styles.panel}>
      <div style={styles.header}>
        <div>
          <h3 style={styles.title}>Notificaciones</h3>
          {unreadCount > 0 && (
            <span style={styles.unreadBadge}>{unreadCount} sin leer</span>
          )}
        </div>
        <div style={styles.headerActions}>
          {unreadCount > 0 && (
            <button onClick={markAllAsRead} style={styles.markAllButton}>
              Marcar todas como leídas
            </button>
          )}
          <button onClick={onClose} style={styles.closeButton}>
            ✕
          </button>
        </div>
      </div>

      <div style={styles.notificationsList}>
        {notifications.length === 0 ? (
          <div style={styles.emptyState}>
            <span style={styles.emptyIcon}>🔔</span>
            <p style={styles.emptyText}>No hay notificaciones</p>
          </div>
        ) : (
          notifications.map(notification => (
            <div
              key={notification.id}
              style={{
                ...styles.notificationItem,
                backgroundColor: notification.read ? '#f8f9fa' : 'white',
                borderLeft: `4px solid ${getTypeColor(notification.type)}`
              }}
              onClick={() => handleNotificationClick(notification)}
            >
              <div style={styles.notificationIcon}>
                {notification.icon}
              </div>

              <div style={styles.notificationContent}>
                <div style={styles.notificationHeader}>
                  <h4 style={{
                    ...styles.notificationTitle,
                    fontWeight: notification.read ? '500' : '700'
                  }}>
                    {notification.title}
                  </h4>
                  {!notification.read && (
                    <span style={styles.unreadDot} />
                  )}
                </div>
                <p style={styles.notificationMessage}>
                  {notification.message}
                </p>
                <span style={styles.notificationTime}>
                  {notification.time}
                </span>
              </div>

              <button
                onClick={(e) => {
                  e.stopPropagation();
                  deleteNotification(notification.id);
                }}
                style={styles.deleteButton}
                title="Eliminar notificación"
              >
                🗑️
              </button>
            </div>
          ))
        )}
      </div>

      <div style={styles.footer}>
        <button style={styles.viewAllButton} onClick={handleViewAll}>
          Ver todas las notificaciones →
        </button>
      </div>
    </div>
  );
};

const styles = {
  panel: {
    position: 'absolute',
    top: '60px',
    right: '20px',
    width: '420px',
    maxHeight: '600px',
    backgroundColor: 'white',
    borderRadius: '12px',
    boxShadow: '0 8px 24px rgba(0, 0, 0, 0.15)',
    display: 'flex',
    flexDirection: 'column',
    zIndex: 1000,
    animation: 'slideDown 0.2s ease-out',
  },
  header: {
    padding: '20px',
    borderBottom: '1px solid #e9ecef',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  title: {
    margin: 0,
    fontSize: '18px',
    color: '#2c3e50',
    fontWeight: '700',
  },
  unreadBadge: {
    display: 'inline-block',
    marginTop: '5px',
    padding: '2px 8px',
    backgroundColor: '#e74c3c',
    color: 'white',
    borderRadius: '12px',
    fontSize: '12px',
    fontWeight: '600',
  },
  headerActions: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  markAllButton: {
    padding: '6px 12px',
    backgroundColor: '#f8f9fa',
    border: '1px solid #e9ecef',
    borderRadius: '6px',
    fontSize: '13px',
    color: '#3498db',
    cursor: 'pointer',
    fontWeight: '500',
    transition: 'background-color 0.2s',
  },
  closeButton: {
    background: 'none',
    border: 'none',
    fontSize: '20px',
    cursor: 'pointer',
    color: '#95a5a6',
    padding: '4px',
    transition: 'color 0.2s',
  },
  notificationsList: {
    flex: 1,
    overflowY: 'auto',
    maxHeight: '450px',
  },
  notificationItem: {
    padding: '16px',
    borderBottom: '1px solid #e9ecef',
    display: 'flex',
    gap: '12px',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
    position: 'relative',
  },
  notificationIcon: {
    fontSize: '24px',
    flexShrink: 0,
  },
  notificationContent: {
    flex: 1,
    minWidth: 0,
  },
  notificationHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    marginBottom: '4px',
  },
  notificationTitle: {
    margin: 0,
    fontSize: '14px',
    color: '#2c3e50',
  },
  unreadDot: {
    width: '8px',
    height: '8px',
    backgroundColor: '#3498db',
    borderRadius: '50%',
    flexShrink: 0,
  },
  notificationMessage: {
    margin: '4px 0',
    fontSize: '13px',
    color: '#7f8c8d',
    lineHeight: '1.4',
  },
  notificationTime: {
    fontSize: '12px',
    color: '#95a5a6',
  },
  deleteButton: {
    background: 'none',
    border: 'none',
    fontSize: '16px',
    cursor: 'pointer',
    opacity: 0,
    transition: 'opacity 0.2s',
    padding: '4px',
  },
  footer: {
    padding: '12px',
    borderTop: '1px solid #e9ecef',
    textAlign: 'center',
  },
  viewAllButton: {
    width: '100%',
    padding: '10px',
    backgroundColor: '#f8f9fa',
    border: '1px solid #e9ecef',
    borderRadius: '6px',
    fontSize: '14px',
    color: '#3498db',
    cursor: 'pointer',
    fontWeight: '600',
    transition: 'background-color 0.2s',
  },
  emptyState: {
    padding: '60px 20px',
    textAlign: 'center',
  },
  emptyIcon: {
    fontSize: '48px',
    display: 'block',
    marginBottom: '12px',
    opacity: 0.3,
  },
  emptyText: {
    color: '#95a5a6',
    fontSize: '14px',
  },
};

// Agregar animación al head
if (typeof document !== 'undefined') {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = `
    @keyframes slideDown {
      from {
        opacity: 0;
        transform: translateY(-10px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .notification-item:hover .delete-button {
      opacity: 1 !important;
    }
  `;
  if (!document.getElementById('notifications-animations')) {
    styleSheet.id = 'notifications-animations';
    document.head.appendChild(styleSheet);
  }
}

export default NotificationsPanel;
