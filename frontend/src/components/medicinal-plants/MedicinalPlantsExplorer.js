import React, { useState, useEffect } from 'react';
import PlantCard from './PlantCard';
import medicinalPlantsService from '../../services/medicinalPlantsService';

/**
 * MedicinalPlantsExplorer Component
 * Main explorer page for browsing Mexican medicinal plants
 * Based on UNAM's Atlas de las Plantas de la Medicina Tradicional Mexicana
 */
const MedicinalPlantsExplorer = ({ onPlantClick }) => {
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters state
  const [filters, setFilters] = useState({
    category: '',
    evidenceLevel: '',
    safetyLevel: '',
    search: '',
    page: 1,
    pageSize: 20
  });

  // Fetch plants on mount and when filters change
  useEffect(() => {
    fetchPlants();
  }, [filters]);

  const fetchPlants = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await medicinalPlantsService.getPlants(filters);
      setPlants(data.items || data || []);
    } catch (err) {
      console.error('Error fetching medicinal plants:', err);
      setError('Error al cargar las plantas medicinales. Por favor, intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value, page: 1 }));
  };

  const handleSearchChange = (e) => {
    const value = e.target.value;
    // Debounce search
    clearTimeout(window.searchTimeout);
    window.searchTimeout = setTimeout(() => {
      handleFilterChange('search', value);
    }, 500);
  };

  const clearFilters = () => {
    setFilters({
      category: '',
      evidenceLevel: '',
      safetyLevel: '',
      search: '',
      page: 1,
      pageSize: 20
    });
  };

  // Get filter options from service
  const categories = medicinalPlantsService.getCategories();
  const evidenceLevels = medicinalPlantsService.getEvidenceLevels();
  const safetyLevels = medicinalPlantsService.getSafetyLevels();

  if (loading && plants.length === 0) {
    return (
      <div style={styles.container}>
        <div style={styles.loadingContainer}>
          <div style={styles.spinner}></div>
          <p style={styles.loadingText}>Cargando plantas medicinales...</p>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <div style={styles.headerContent}>
          <h1 style={styles.title}>
            <span style={styles.titleIcon}>🌿</span>
            Plantas Medicinales Mexicanas
          </h1>
          <p style={styles.subtitle}>
            Explora el conocimiento ancestral de la medicina tradicional mexicana
            basado en el Atlas de UNAM
          </p>
        </div>
      </div>

      {/* Search Bar */}
      <div style={styles.searchSection}>
        <div style={styles.searchContainer}>
          <span style={styles.searchIcon}>🔍</span>
          <input
            type="text"
            placeholder="Buscar por nombre científico, popular o uso tradicional..."
            style={styles.searchInput}
            onChange={handleSearchChange}
            defaultValue={filters.search}
          />
        </div>
      </div>

      {/* Filters Section */}
      <div style={styles.filtersSection}>
        <div style={styles.filtersHeader}>
          <h3 style={styles.filtersTitle}>Filtros</h3>
          {(filters.category || filters.evidenceLevel || filters.safetyLevel) && (
            <button style={styles.clearButton} onClick={clearFilters}>
              Limpiar filtros
            </button>
          )}
        </div>

        <div style={styles.filtersGrid}>
          {/* Category Filter */}
          <div style={styles.filterGroup}>
            <label style={styles.filterLabel}>Categoría:</label>
            <select
              value={filters.category}
              onChange={(e) => handleFilterChange('category', e.target.value)}
              style={styles.select}
            >
              <option value="">Todas las categorías</option>
              {categories.map(cat => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>
          </div>

          {/* Evidence Level Filter */}
          <div style={styles.filterGroup}>
            <label style={styles.filterLabel}>Nivel de Evidencia:</label>
            <select
              value={filters.evidenceLevel}
              onChange={(e) => handleFilterChange('evidenceLevel', e.target.value)}
              style={styles.select}
            >
              <option value="">Todos los niveles</option>
              {evidenceLevels.map(level => (
                <option key={level.value} value={level.value}>
                  {level.label}
                </option>
              ))}
            </select>
          </div>

          {/* Safety Level Filter */}
          <div style={styles.filterGroup}>
            <label style={styles.filterLabel}>Nivel de Seguridad:</label>
            <select
              value={filters.safetyLevel}
              onChange={(e) => handleFilterChange('safetyLevel', e.target.value)}
              style={styles.select}
            >
              <option value="">Todos los niveles</option>
              {safetyLevels.map(level => (
                <option key={level.value} value={level.value}>
                  {level.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Results Section */}
      <div style={styles.resultsSection}>
        <div style={styles.resultsHeader}>
          <h3 style={styles.resultsTitle}>
            {plants.length > 0 ? (
              <>Encontradas {plants.length} plantas</>
            ) : (
              <>No se encontraron plantas</>
            )}
          </h3>
        </div>

        {error && (
          <div style={styles.errorMessage}>
            <span style={styles.errorIcon}>⚠️</span>
            {error}
          </div>
        )}

        {plants.length === 0 && !loading && !error && (
          <div style={styles.emptyState}>
            <span style={styles.emptyIcon}>🌿</span>
            <h3 style={styles.emptyTitle}>No se encontraron plantas</h3>
            <p style={styles.emptyText}>
              Intenta ajustar los filtros o realizar una búsqueda diferente
            </p>
          </div>
        )}

        {plants.length > 0 && (
          <div style={styles.plantsGrid}>
            {plants.map(plant => (
              <PlantCard
                key={plant.id}
                plant={plant}
                onClick={onPlantClick}
              />
            ))}
          </div>
        )}

        {loading && plants.length > 0 && (
          <div style={styles.loadingMore}>
            Cargando más plantas...
          </div>
        )}
      </div>

      {/* Info Banner */}
      <div style={styles.infoBanner}>
        <div style={styles.infoBannerContent}>
          <span style={styles.infoBannerIcon}>ℹ️</span>
          <div>
            <strong>Importante:</strong> La información presentada es de carácter
            informativo y educativo. Siempre consulta con un profesional de la salud
            antes de usar cualquier planta medicinal, especialmente si estás embarazada,
            amamantando o tomando medicamentos.
          </div>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '1400px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif',
    backgroundColor: '#f8f9fa',
    minHeight: '100vh',
  },
  loadingContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '400px',
  },
  spinner: {
    width: '50px',
    height: '50px',
    border: '4px solid #f3f3f3',
    borderTop: '4px solid #28a745',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  loadingText: {
    marginTop: '20px',
    color: '#666',
    fontSize: '16px',
  },
  header: {
    textAlign: 'center',
    marginBottom: '30px',
    padding: '40px 20px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    borderRadius: '16px',
    color: 'white',
  },
  headerContent: {
    maxWidth: '800px',
    margin: '0 auto',
  },
  title: {
    margin: '0 0 15px 0',
    fontSize: '36px',
    fontWeight: '700',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '15px',
  },
  titleIcon: {
    fontSize: '42px',
  },
  subtitle: {
    margin: 0,
    fontSize: '18px',
    fontWeight: '400',
    opacity: 0.95,
    lineHeight: '1.6',
  },
  searchSection: {
    marginBottom: '25px',
  },
  searchContainer: {
    position: 'relative',
    maxWidth: '800px',
    margin: '0 auto',
  },
  searchIcon: {
    position: 'absolute',
    left: '20px',
    top: '50%',
    transform: 'translateY(-50%)',
    fontSize: '20px',
  },
  searchInput: {
    width: '100%',
    padding: '15px 20px 15px 55px',
    fontSize: '16px',
    border: '2px solid #dee2e6',
    borderRadius: '12px',
    outline: 'none',
    transition: 'border-color 0.2s',
    backgroundColor: 'white',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
  },
  filtersSection: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.08)',
    marginBottom: '30px',
  },
  filtersHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
  },
  filtersTitle: {
    margin: 0,
    fontSize: '20px',
    fontWeight: '600',
    color: '#2c3e50',
  },
  clearButton: {
    padding: '8px 16px',
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '14px',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  filtersGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
  },
  filterGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  filterLabel: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#495057',
  },
  select: {
    padding: '10px 12px',
    fontSize: '15px',
    border: '1px solid #ced4da',
    borderRadius: '6px',
    backgroundColor: 'white',
    cursor: 'pointer',
    outline: 'none',
    transition: 'border-color 0.2s',
  },
  resultsSection: {
    marginBottom: '30px',
  },
  resultsHeader: {
    marginBottom: '25px',
  },
  resultsTitle: {
    margin: 0,
    fontSize: '22px',
    fontWeight: '600',
    color: '#2c3e50',
  },
  errorMessage: {
    backgroundColor: '#fff3cd',
    border: '1px solid #ffc107',
    borderRadius: '8px',
    padding: '15px 20px',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    color: '#856404',
    marginBottom: '20px',
  },
  errorIcon: {
    fontSize: '24px',
  },
  emptyState: {
    textAlign: 'center',
    padding: '60px 20px',
    backgroundColor: 'white',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.08)',
  },
  emptyIcon: {
    fontSize: '64px',
    opacity: 0.3,
  },
  emptyTitle: {
    margin: '20px 0 10px 0',
    fontSize: '24px',
    color: '#495057',
  },
  emptyText: {
    margin: 0,
    fontSize: '16px',
    color: '#6c757d',
  },
  plantsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
    gap: '25px',
  },
  loadingMore: {
    textAlign: 'center',
    padding: '20px',
    color: '#666',
    fontSize: '14px',
  },
  infoBanner: {
    backgroundColor: '#e7f3ff',
    border: '1px solid #b3d9ff',
    borderRadius: '12px',
    padding: '20px',
    marginTop: '30px',
  },
  infoBannerContent: {
    display: 'flex',
    gap: '15px',
    alignItems: 'flex-start',
    fontSize: '14px',
    color: '#004085',
    lineHeight: '1.6',
  },
  infoBannerIcon: {
    fontSize: '24px',
    flexShrink: 0,
  },
};

export default MedicinalPlantsExplorer;
