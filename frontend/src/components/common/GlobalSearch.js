import React, { useState, useEffect, useRef } from 'react';

const GlobalSearch = ({ isOpen, onClose, onNavigate }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef(null);
  const resultsRef = useRef(null);

  // Mock data - En producción vendría del backend
  const mockData = {
    patients: [
      { id: 1, name: 'María González', type: 'patient', section: 'Pacientes', meta: 'IMC: 25.0' },
      { id: 2, name: 'Carlos Rodríguez', type: 'patient', section: 'Pacientes', meta: 'IMC: 26.8' },
      { id: 3, name: 'Ana Martínez', type: 'patient', section: 'Pacientes', meta: 'IMC: 24.2' },
    ],
    foods: [
      { id: 1, name: 'Manzana', type: 'food', section: 'Alimentos', meta: '52 kcal/100g' },
      { id: 2, name: 'Plátano', type: 'food', section: 'Alimentos', meta: '89 kcal/100g' },
      { id: 3, name: 'Aguacate', type: 'food', section: 'Alimentos', meta: '160 kcal/100g' },
    ],
    recipes: [
      { id: 1, name: 'Ensalada César', type: 'recipe', section: 'Recetas', meta: '350 kcal/porción' },
      { id: 2, name: 'Bowl Mediterráneo', type: 'recipe', section: 'Recetas', meta: '420 kcal/porción' },
      { id: 3, name: 'Smoothie Verde', type: 'recipe', section: 'Recetas', meta: '180 kcal/vaso' },
    ],
    sections: [
      { id: 'dashboard', name: 'Dashboard', type: 'section', section: 'Navegación', meta: 'Panel principal' },
      { id: 'foods', name: 'Alimentos', type: 'section', section: 'Navegación', meta: 'Base de datos de alimentos' },
      { id: 'recipes', name: 'Recetas', type: 'section', section: 'Navegación', meta: 'Recetas y menús' },
      { id: 'equivalences', name: 'Equivalencias', type: 'section', section: 'Navegación', meta: 'Sistema de equivalencias' },
      { id: 'patients', name: 'Pacientes', type: 'section', section: 'Navegación', meta: 'Gestión de pacientes' },
      { id: 'calculator', name: 'Calculadora', type: 'section', section: 'Navegación', meta: 'Herramientas de cálculo' },
    ]
  };

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      setSelectedIndex(0);
      return;
    }

    const searchQuery = query.toLowerCase();
    const allResults = [];

    // Buscar en todas las categorías
    Object.values(mockData).forEach(category => {
      const filtered = category.filter(item =>
        item.name.toLowerCase().includes(searchQuery)
      );
      allResults.push(...filtered);
    });

    setResults(allResults);
    setSelectedIndex(0);
  }, [query]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isOpen) return;

      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          setSelectedIndex(prev => Math.min(prev + 1, results.length - 1));
          break;
        case 'ArrowUp':
          e.preventDefault();
          setSelectedIndex(prev => Math.max(prev - 1, 0));
          break;
        case 'Enter':
          e.preventDefault();
          if (results[selectedIndex]) {
            handleSelect(results[selectedIndex]);
          }
          break;
        case 'Escape':
          e.preventDefault();
          onClose();
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, results, selectedIndex]);

  // Scroll al elemento seleccionado
  useEffect(() => {
    if (resultsRef.current && results.length > 0) {
      const selectedElement = resultsRef.current.children[selectedIndex];
      if (selectedElement) {
        selectedElement.scrollIntoView({ block: 'nearest' });
      }
    }
  }, [selectedIndex]);

  const handleSelect = (item) => {
    onNavigate(item);
    onClose();
    setQuery('');
  };

  const getIcon = (type) => {
    const icons = {
      patient: '👤',
      food: '🥗',
      recipe: '🍽️',
      section: '📁'
    };
    return icons[type] || '📄';
  };

  if (!isOpen) return null;

  return (
    <>
      <div style={styles.overlay} onClick={onClose} />
      <div style={styles.modal}>
        <div style={styles.searchBar}>
          <span style={styles.searchIcon}>🔍</span>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar pacientes, alimentos, recetas..."
            style={styles.input}
          />
          <kbd style={styles.kbd}>ESC</kbd>
        </div>

        {results.length > 0 && (
          <div ref={resultsRef} style={styles.results}>
            {results.map((result, index) => (
              <div
                key={`${result.type}-${result.id}`}
                onClick={() => handleSelect(result)}
                style={{
                  ...styles.resultItem,
                  ...(index === selectedIndex ? styles.selectedItem : {})
                }}
              >
                <div style={styles.resultIcon}>{getIcon(result.type)}</div>
                <div style={styles.resultContent}>
                  <div style={styles.resultName}>{result.name}</div>
                  <div style={styles.resultMeta}>
                    <span style={styles.resultSection}>{result.section}</span>
                    {result.meta && (
                      <>
                        <span style={styles.separator}>•</span>
                        <span style={styles.resultDetails}>{result.meta}</span>
                      </>
                    )}
                  </div>
                </div>
                {index === selectedIndex && (
                  <kbd style={styles.enterKbd}>↵</kbd>
                )}
              </div>
            ))}
          </div>
        )}

        {query && results.length === 0 && (
          <div style={styles.emptyState}>
            <span style={styles.emptyIcon}>🔍</span>
            <p style={styles.emptyText}>No se encontraron resultados</p>
            <p style={styles.emptyHint}>Intenta con otro término de búsqueda</p>
          </div>
        )}

        {!query && (
          <div style={styles.hints}>
            <div style={styles.hintSection}>
              <h4 style={styles.hintTitle}>Búsqueda rápida</h4>
              <div style={styles.hintList}>
                <div style={styles.hintItem}>
                  <span>👤 Pacientes</span>
                  <span style={styles.hintExample}>María, Carlos...</span>
                </div>
                <div style={styles.hintItem}>
                  <span>🥗 Alimentos</span>
                  <span style={styles.hintExample}>Manzana, Aguacate...</span>
                </div>
                <div style={styles.hintItem}>
                  <span>🍽️ Recetas</span>
                  <span style={styles.hintExample}>Ensalada, Bowl...</span>
                </div>
              </div>
            </div>

            <div style={styles.shortcuts}>
              <h4 style={styles.hintTitle}>Atajos de teclado</h4>
              <div style={styles.shortcutList}>
                <div style={styles.shortcutItem}>
                  <kbd style={styles.shortcutKbd}>↑ ↓</kbd>
                  <span>Navegar</span>
                </div>
                <div style={styles.shortcutItem}>
                  <kbd style={styles.shortcutKbd}>↵</kbd>
                  <span>Seleccionar</span>
                </div>
                <div style={styles.shortcutItem}>
                  <kbd style={styles.shortcutKbd}>ESC</kbd>
                  <span>Cerrar</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

const styles = {
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    zIndex: 9998,
    animation: 'fadeIn 0.2s ease-out',
  },
  modal: {
    position: 'fixed',
    top: '20%',
    left: '50%',
    transform: 'translateX(-50%)',
    width: '90%',
    maxWidth: '600px',
    backgroundColor: 'white',
    borderRadius: '12px',
    boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
    zIndex: 9999,
    overflow: 'hidden',
    animation: 'slideDown 0.2s ease-out',
  },
  searchBar: {
    display: 'flex',
    alignItems: 'center',
    padding: '16px 20px',
    borderBottom: '1px solid #e9ecef',
    gap: '12px',
  },
  searchIcon: {
    fontSize: '20px',
  },
  input: {
    flex: 1,
    border: 'none',
    outline: 'none',
    fontSize: '16px',
    color: '#2c3e50',
  },
  kbd: {
    padding: '4px 8px',
    backgroundColor: '#f8f9fa',
    border: '1px solid #e9ecef',
    borderRadius: '4px',
    fontSize: '12px',
    color: '#7f8c8d',
    fontWeight: '600',
    fontFamily: 'monospace',
  },
  results: {
    maxHeight: '400px',
    overflowY: 'auto',
  },
  resultItem: {
    display: 'flex',
    alignItems: 'center',
    padding: '12px 20px',
    gap: '12px',
    cursor: 'pointer',
    transition: 'background-color 0.15s',
    borderBottom: '1px solid #f8f9fa',
  },
  selectedItem: {
    backgroundColor: '#ebf5fb',
  },
  resultIcon: {
    fontSize: '24px',
    flexShrink: 0,
  },
  resultContent: {
    flex: 1,
    minWidth: 0,
  },
  resultName: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: '4px',
  },
  resultMeta: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    fontSize: '12px',
    color: '#7f8c8d',
  },
  resultSection: {
    color: '#3498db',
    fontWeight: '500',
  },
  separator: {
    color: '#bdc3c7',
  },
  resultDetails: {
    color: '#95a5a6',
  },
  enterKbd: {
    padding: '4px 8px',
    backgroundColor: '#3498db',
    color: 'white',
    borderRadius: '4px',
    fontSize: '12px',
    fontWeight: '600',
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
    fontSize: '16px',
    color: '#2c3e50',
    marginBottom: '8px',
  },
  emptyHint: {
    fontSize: '14px',
    color: '#95a5a6',
  },
  hints: {
    padding: '20px',
  },
  hintSection: {
    marginBottom: '20px',
  },
  hintTitle: {
    fontSize: '12px',
    fontWeight: '600',
    color: '#7f8c8d',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
    marginBottom: '12px',
  },
  hintList: {
    display: 'grid',
    gap: '8px',
  },
  hintItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '8px 12px',
    backgroundColor: '#f8f9fa',
    borderRadius: '6px',
    fontSize: '14px',
  },
  hintExample: {
    color: '#95a5a6',
    fontSize: '13px',
  },
  shortcuts: {
    borderTop: '1px solid #e9ecef',
    paddingTop: '20px',
  },
  shortcutList: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '12px',
  },
  shortcutItem: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '6px',
    fontSize: '13px',
    color: '#7f8c8d',
  },
  shortcutKbd: {
    padding: '6px 12px',
    backgroundColor: '#f8f9fa',
    border: '1px solid #e9ecef',
    borderRadius: '4px',
    fontSize: '14px',
    fontWeight: '600',
    fontFamily: 'monospace',
  },
};

// Agregar animaciones
if (typeof document !== 'undefined') {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = `
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }

    @keyframes slideDown {
      from {
        opacity: 0;
        transform: translateX(-50%) translateY(-20px);
      }
      to {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
      }
    }
  `;
  if (!document.getElementById('global-search-animations')) {
    styleSheet.id = 'global-search-animations';
    document.head.appendChild(styleSheet);
  }
}

export default GlobalSearch;
