import React, { useState, useEffect, createContext, useContext } from 'react';

// Context para compartir el sistema de toast en toda la app
const ToastContext = createContext();

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast debe usarse dentro de ToastProvider');
  }
  return context;
};

export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);

  const showToast = ({ type = 'info', message, duration = 3000, action }) => {
    const id = Date.now();
    const toast = { id, type, message, action };

    setToasts(prev => [...prev, toast]);

    if (duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, duration);
    }

    return id;
  };

  const removeToast = (id) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  };

  return (
    <ToastContext.Provider value={{ showToast, removeToast }}>
      {children}
      <ToastContainer toasts={toasts} removeToast={removeToast} />
    </ToastContext.Provider>
  );
};

const ToastContainer = ({ toasts, removeToast }) => {
  return (
    <div style={styles.container}>
      {toasts.map(toast => (
        <Toast key={toast.id} toast={toast} onClose={() => removeToast(toast.id)} />
      ))}
    </div>
  );
};

const Toast = ({ toast, onClose }) => {
  const [isExiting, setIsExiting] = useState(false);

  const handleClose = () => {
    setIsExiting(true);
    setTimeout(onClose, 300);
  };

  const getIcon = () => {
    switch (toast.type) {
      case 'success': return '✅';
      case 'error': return '❌';
      case 'warning': return '⚠️';
      case 'info': return 'ℹ️';
      default: return '📢';
    }
  };

  const getColor = () => {
    switch (toast.type) {
      case 'success': return '#27ae60';
      case 'error': return '#e74c3c';
      case 'warning': return '#f39c12';
      case 'info': return '#3498db';
      default: return '#95a5a6';
    }
  };

  return (
    <div
      style={{
        ...styles.toast,
        backgroundColor: getColor(),
        animation: isExiting ? 'slideOut 0.3s ease-out forwards' : 'slideIn 0.3s ease-out',
      }}
    >
      <div style={styles.content}>
        <span style={styles.icon}>{getIcon()}</span>
        <span style={styles.message}>{toast.message}</span>
      </div>

      <div style={styles.actions}>
        {toast.action && (
          <button
            onClick={() => {
              toast.action.onClick();
              handleClose();
            }}
            style={styles.actionButton}
          >
            {toast.action.label}
          </button>
        )}
        <button onClick={handleClose} style={styles.closeButton}>
          ✕
        </button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    position: 'fixed',
    top: '20px',
    right: '20px',
    zIndex: 9999,
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
    pointerEvents: 'none',
  },
  toast: {
    minWidth: '300px',
    maxWidth: '500px',
    padding: '16px',
    borderRadius: '8px',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    color: 'white',
    pointerEvents: 'all',
  },
  content: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    flex: 1,
  },
  icon: {
    fontSize: '20px',
  },
  message: {
    fontSize: '14px',
    fontWeight: '500',
    lineHeight: '1.4',
  },
  actions: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    marginLeft: '12px',
  },
  actionButton: {
    padding: '6px 12px',
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    border: '1px solid rgba(255, 255, 255, 0.3)',
    borderRadius: '4px',
    color: 'white',
    fontSize: '13px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  closeButton: {
    padding: '4px 8px',
    backgroundColor: 'transparent',
    border: 'none',
    color: 'white',
    fontSize: '16px',
    cursor: 'pointer',
    opacity: 0.8,
    transition: 'opacity 0.2s',
  },
};

// Agregar animaciones al head del documento
if (typeof document !== 'undefined') {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = `
    @keyframes slideIn {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }

    @keyframes slideOut {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(400px);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(styleSheet);
}

export default Toast;
