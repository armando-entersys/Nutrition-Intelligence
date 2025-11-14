import React, { useState, useEffect } from 'react';
import medicinalPlantsService from '../../services/medicinalPlantsService';

/**
 * PlantDetail Component
 * Displays detailed information about a single medicinal plant
 */
const PlantDetail = ({ plantId, onClose }) => {
  const [plant, setPlant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('general');

  useEffect(() => {
    if (plantId) {
      fetchPlantDetail();
    }
  }, [plantId]);

  const fetchPlantDetail = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await medicinalPlantsService.getPlantById(plantId);
      setPlant(data);
    } catch (err) {
      console.error('Error fetching plant detail:', err);
      setError('Error al cargar los detalles de la planta.');
    } finally {
      setLoading(false);
    }
  };

  const getCategoryLabel = (category) => {
    const categoryLabels = {
      'DIGESTIVE': 'Digestiva',
      'RESPIRATORY': 'Respiratoria',
      'CALMING': 'Calmante',
      'METABOLIC': 'Metabólica',
      'ANTI_INFLAMMATORY': 'Antiinflamatoria',
      'SKIN_HAIR': 'Piel y Cabello',
      'PAIN_RELIEF': 'Alivio del Dolor',
      'IMMUNE_SUPPORT': 'Apoyo Inmune',
      'FEMALE_HEALTH': 'Salud Femenina',
      'MEMORY_COGNITION': 'Memoria y Cognición',
      'URINARY': 'Urinaria',
      'OTHER': 'Otra'
    };
    return categoryLabels[category] || category;
  };

  const getEvidenceLabel = (level) => {
    const labels = {
      'STRONG_EVIDENCE': 'Evidencia Científica Fuerte',
      'MODERATE_EVIDENCE': 'Evidencia Científica Moderada',
      'TRADITIONAL_ONLY': 'Solo Uso Tradicional Documentado'
    };
    return labels[level] || level;
  };

  const getSafetyLabel = (level) => {
    const labels = {
      'VERY_SAFE': 'Muy Segura',
      'SAFE': 'Segura con dosis adecuadas',
      'MODERATE': 'Seguridad moderada - Precauciones necesarias'
    };
    return labels[level] || level;
  };

  const getPreparationTypeLabel = (type) => {
    const labels = {
      'TEA': 'Té/Infusión',
      'DECOCTION': 'Cocimiento/Decocción',
      'TINCTURE': 'Tintura',
      'POULTICE': 'Cataplasma',
      'SYRUP': 'Jarabe',
      'EXTRACT': 'Extracto',
      'FRESH': 'Fresco/Directo',
      'POWDER': 'Polvo',
      'BATH': 'Baño',
      'INHALATION': 'Inhalación/Vapor',
      'TOPICAL': 'Uso Tópico/Externo',
      'JUICE': 'Jugo',
      'CAPSULE': 'Cápsulas',
      'COMPRESS': 'Compresas'
    };
    return labels[type] || type;
  };

  if (loading) {
    return (
      <div style={styles.modalOverlay}>
        <div style={styles.modal}>
          <div style={styles.loadingContainer}>
            <div style={styles.spinner}></div>
            <p>Cargando información...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !plant) {
    return (
      <div style={styles.modalOverlay}>
        <div style={styles.modal}>
          <div style={styles.errorContainer}>
            <p style={styles.errorText}>{error || 'Planta no encontrada'}</p>
            <button style={styles.closeBtn} onClick={onClose}>
              Cerrar
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.modalOverlay} onClick={onClose}>
      <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div style={styles.header}>
          <div style={styles.headerContent}>
            <h2 style={styles.scientificName}>{plant.scientific_name}</h2>
            {plant.botanical_family && (
              <p style={styles.botanicalFamily}>
                Familia: {plant.botanical_family}
              </p>
            )}
          </div>
          <button style={styles.closeButton} onClick={onClose}>
            ✕
          </button>
        </div>

        {/* Main Image */}
        {plant.main_image_url && (
          <div style={styles.imageContainer}>
            <img
              src={plant.main_image_url}
              alt={plant.scientific_name}
              style={styles.mainImage}
            />
          </div>
        )}

        {/* Tabs */}
        <div style={styles.tabs}>
          <button
            style={{
              ...styles.tab,
              ...(activeTab === 'general' ? styles.activeTab : {}),
            }}
            onClick={() => setActiveTab('general')}
          >
            Información General
          </button>
          <button
            style={{
              ...styles.tab,
              ...(activeTab === 'uses' ? styles.activeTab : {}),
            }}
            onClick={() => setActiveTab('uses')}
          >
            Usos y Preparación
          </button>
          <button
            style={{
              ...styles.tab,
              ...(activeTab === 'safety' ? styles.activeTab : {}),
            }}
            onClick={() => setActiveTab('safety')}
          >
            Seguridad
          </button>
        </div>

        {/* Content */}
        <div style={styles.content}>
          {/* General Tab */}
          {activeTab === 'general' && (
            <div style={styles.tabContent}>
              {/* Popular Names */}
              {plant.popular_names && plant.popular_names.length > 0 && (
                <div style={styles.section}>
                  <h3 style={styles.sectionTitle}>Nombres Comunes</h3>
                  <div style={styles.namesList}>
                    {plant.popular_names.map((name, idx) => (
                      <span key={idx} style={styles.nameTag}>{name}</span>
                    ))}
                  </div>
                </div>
              )}

              {/* Indigenous Names */}
              {plant.indigenous_names && Object.keys(plant.indigenous_names).length > 0 && (
                <div style={styles.section}>
                  <h3 style={styles.sectionTitle}>Nombres Indígenas</h3>
                  <ul style={styles.list}>
                    {Object.entries(plant.indigenous_names).map(([lang, name]) => (
                      <li key={lang}>
                        <strong>{lang}:</strong> {name}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Category */}
              <div style={styles.section}>
                <h3 style={styles.sectionTitle}>Categoría</h3>
                <div style={styles.categoryBadge}>
                  🌱 {getCategoryLabel(plant.primary_category)}
                </div>
              </div>

              {/* Description */}
              {plant.plant_description && (
                <div style={styles.section}>
                  <h3 style={styles.sectionTitle}>Descripción Botánica</h3>
                  <p style={styles.text}>{plant.plant_description}</p>
                </div>
              )}

              {/* Where Found */}
              {plant.states_found && plant.states_found.length > 0 && (
                <div style={styles.section}>
                  <h3 style={styles.sectionTitle}>Distribución en México</h3>
                  <p style={styles.text}>
                    {plant.states_found.join(', ')}
                  </p>
                </div>
              )}

              {/* Evidence Level */}
              <div style={styles.section}>
                <h3 style={styles.sectionTitle}>Nivel de Evidencia Científica</h3>
                <div style={styles.evidenceBadge}>
                  📊 {getEvidenceLabel(plant.evidence_level)}
                </div>
                {plant.clinical_studies_count > 0 && (
                  <p style={styles.studiesCount}>
                    {plant.clinical_studies_count} estudios clínicos
                  </p>
                )}
              </div>

              {/* Active Compounds */}
              {plant.active_compounds && plant.active_compounds.length > 0 && (
                <div style={styles.section}>
                  <h3 style={styles.sectionTitle}>Compuestos Activos</h3>
                  <ul style={styles.list}>
                    {plant.active_compounds.map((compound, idx) => (
                      <li key={idx}>{compound}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Historical Notes */}
              {plant.historical_notes && (
                <div style={styles.section}>
                  <h3 style={styles.sectionTitle}>Notas Históricas</h3>
                  <p style={styles.text}>{plant.historical_notes}</p>
                </div>
              )}
            </div>
          )}

          {/* Uses Tab */}
          {activeTab === 'uses' && (
            <div style={styles.tabContent}>
              {/* Traditional Uses */}
              {plant.traditional_uses && plant.traditional_uses.length > 0 && (
                <div style={styles.section}>
                  <h3 style={styles.sectionTitle}>Usos Tradicionales</h3>
                  <ul style={styles.list}>
                    {plant.traditional_uses.map((use, idx) => (
                      <li key={idx}>{use}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Preparation Methods */}
              {plant.preparation_methods && plant.preparation_methods.length > 0 && (
                <div style={styles.section}>
                  <h3 style={styles.sectionTitle}>Métodos de Preparación</h3>
                  {plant.preparation_methods.map((method, idx) => (
                    <div key={idx} style={styles.preparationCard}>
                      <h4 style={styles.preparationTitle}>
                        {getPreparationTypeLabel(method.type)}
                      </h4>
                      {method.dosage && (
                        <p style={styles.preparationDetail}>
                          <strong>Dosificación:</strong> {method.dosage}
                        </p>
                      )}
                      {method.preparation && (
                        <p style={styles.preparationDetail}>
                          <strong>Preparación:</strong> {method.preparation}
                        </p>
                      )}
                      {method.frequency && (
                        <p style={styles.preparationDetail}>
                          <strong>Frecuencia:</strong> {method.frequency}
                        </p>
                      )}
                      {method.duration && (
                        <p style={styles.preparationDetail}>
                          <strong>Duración:</strong> {method.duration}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {/* Where to Find */}
              {plant.where_to_find && plant.where_to_find.length > 0 && (
                <div style={styles.section}>
                  <h3 style={styles.sectionTitle}>Dónde Conseguirla</h3>
                  <ul style={styles.list}>
                    {plant.where_to_find.map((place, idx) => (
                      <li key={idx}>{place}</li>
                    ))}
                  </ul>
                  {plant.approximate_price_range && (
                    <p style={styles.priceRange}>
                      <strong>Precio aproximado:</strong> {plant.approximate_price_range}
                    </p>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Safety Tab */}
          {activeTab === 'safety' && (
            <div style={styles.tabContent}>
              {/* Safety Level */}
              <div style={styles.section}>
                <h3 style={styles.sectionTitle}>Nivel de Seguridad</h3>
                <div style={styles.safetyBadge}>
                  {getSafetyLabel(plant.safety_level)}
                </div>
              </div>

              {/* Precautions */}
              {plant.precautions && plant.precautions.length > 0 && (
                <div style={styles.section}>
                  <h3 style={styles.sectionTitle}>⚠️ Precauciones</h3>
                  <ul style={styles.warningList}>
                    {plant.precautions.map((precaution, idx) => (
                      <li key={idx}>{precaution}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Contraindications */}
              {plant.contraindications && plant.contraindications.length > 0 && (
                <div style={styles.section}>
                  <h3 style={styles.sectionTitle}>🚫 Contraindicaciones</h3>
                  <ul style={styles.warningList}>
                    {plant.contraindications.map((contra, idx) => (
                      <li key={idx}>{contra}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Adverse Effects */}
              {plant.adverse_effects && plant.adverse_effects.length > 0 && (
                <div style={styles.section}>
                  <h3 style={styles.sectionTitle}>Efectos Adversos Posibles</h3>
                  <ul style={styles.list}>
                    {plant.adverse_effects.map((effect, idx) => (
                      <li key={idx}>{effect}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Drug Interactions */}
              {plant.drug_interactions && plant.drug_interactions.length > 0 && (
                <div style={styles.section}>
                  <h3 style={styles.sectionTitle}>Interacciones Medicamentosas</h3>
                  <ul style={styles.warningList}>
                    {plant.drug_interactions.map((interaction, idx) => (
                      <li key={idx}>{interaction}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Special Populations */}
              <div style={styles.section}>
                <h3 style={styles.sectionTitle}>Poblaciones Especiales</h3>
                <div style={styles.specialPopulations}>
                  <div style={styles.populationItem}>
                    <span style={styles.populationIcon}>
                      {plant.safe_in_pregnancy ? '✅' : '❌'}
                    </span>
                    <span>Embarazo: {plant.safe_in_pregnancy ? 'Segura' : 'No recomendada'}</span>
                  </div>
                  <div style={styles.populationItem}>
                    <span style={styles.populationIcon}>
                      {plant.safe_in_lactation ? '✅' : '❌'}
                    </span>
                    <span>Lactancia: {plant.safe_in_lactation ? 'Segura' : 'No recomendada'}</span>
                  </div>
                  <div style={styles.populationItem}>
                    <span style={styles.populationIcon}>
                      {plant.safe_for_children ? '✅' : '❌'}
                    </span>
                    <span>
                      Niños: {plant.safe_for_children ? 'Segura' : 'No recomendada'}
                      {plant.minimum_age_years && ` (desde ${plant.minimum_age_years} años)`}
                    </span>
                  </div>
                </div>
              </div>

              {/* Disclaimer */}
              <div style={styles.disclaimer}>
                <strong>IMPORTANTE:</strong> Esta información es de carácter educativo e
                informativo. Siempre consulte con un profesional de la salud antes de usar
                cualquier planta medicinal, especialmente si está embarazada, amamantando,
                tiene condiciones médicas preexistentes o toma medicamentos.
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={styles.footer}>
          <div style={styles.footerInfo}>
            <span>Fuente: {plant.source || 'UNAM'}</span>
            {plant.view_count > 0 && (
              <span>👁 {plant.view_count} vistas</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const styles = {
  modalOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
    padding: '20px',
    overflowY: 'auto',
  },
  modal: {
    backgroundColor: 'white',
    borderRadius: '16px',
    maxWidth: '900px',
    width: '100%',
    maxHeight: '90vh',
    overflow: 'hidden',
    display: 'flex',
    flexDirection: 'column',
    boxShadow: '0 10px 40px rgba(0, 0, 0, 0.3)',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    padding: '25px 30px',
    borderBottom: '1px solid #eee',
    backgroundColor: '#f8f9fa',
  },
  headerContent: {
    flex: 1,
  },
  scientificName: {
    margin: '0 0 8px 0',
    fontSize: '28px',
    fontWeight: '700',
    color: '#2c3e50',
    fontStyle: 'italic',
  },
  botanicalFamily: {
    margin: 0,
    fontSize: '14px',
    color: '#666',
  },
  closeButton: {
    background: 'none',
    border: 'none',
    fontSize: '28px',
    cursor: 'pointer',
    color: '#666',
    padding: '0 0 0 20px',
    lineHeight: 1,
  },
  imageContainer: {
    width: '100%',
    maxHeight: '300px',
    overflow: 'hidden',
    backgroundColor: '#f8f9fa',
  },
  mainImage: {
    width: '100%',
    height: 'auto',
    objectFit: 'cover',
  },
  tabs: {
    display: 'flex',
    borderBottom: '2px solid #eee',
    backgroundColor: '#f8f9fa',
    padding: '0 30px',
  },
  tab: {
    padding: '15px 25px',
    fontSize: '15px',
    fontWeight: '500',
    color: '#666',
    backgroundColor: 'transparent',
    border: 'none',
    cursor: 'pointer',
    borderBottom: '3px solid transparent',
    transition: 'all 0.2s',
  },
  activeTab: {
    color: '#667eea',
    borderBottomColor: '#667eea',
  },
  content: {
    flex: 1,
    overflowY: 'auto',
    padding: '30px',
  },
  tabContent: {
    animation: 'fadeIn 0.3s',
  },
  section: {
    marginBottom: '30px',
  },
  sectionTitle: {
    margin: '0 0 15px 0',
    fontSize: '20px',
    fontWeight: '600',
    color: '#2c3e50',
  },
  text: {
    margin: 0,
    fontSize: '15px',
    lineHeight: '1.7',
    color: '#495057',
  },
  namesList: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '10px',
  },
  nameTag: {
    padding: '6px 14px',
    backgroundColor: '#e7f5ff',
    color: '#1971c2',
    borderRadius: '20px',
    fontSize: '14px',
    fontWeight: '500',
  },
  categoryBadge: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    padding: '10px 20px',
    backgroundColor: '#e7f5ff',
    color: '#1971c2',
    borderRadius: '20px',
    fontSize: '16px',
    fontWeight: '500',
  },
  evidenceBadge: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    padding: '10px 20px',
    backgroundColor: '#d3f9d8',
    color: '#2f9e44',
    borderRadius: '20px',
    fontSize: '15px',
    fontWeight: '500',
  },
  safetyBadge: {
    display: 'inline-block',
    padding: '10px 20px',
    backgroundColor: '#fff3bf',
    color: '#f08c00',
    borderRadius: '20px',
    fontSize: '15px',
    fontWeight: '500',
  },
  studiesCount: {
    marginTop: '10px',
    fontSize: '14px',
    color: '#666',
  },
  list: {
    margin: 0,
    paddingLeft: '25px',
    fontSize: '15px',
    lineHeight: '1.8',
    color: '#495057',
  },
  warningList: {
    margin: 0,
    paddingLeft: '25px',
    fontSize: '15px',
    lineHeight: '1.8',
    color: '#856404',
  },
  preparationCard: {
    padding: '20px',
    backgroundColor: '#f8f9fa',
    borderRadius: '12px',
    marginBottom: '15px',
    border: '1px solid #dee2e6',
  },
  preparationTitle: {
    margin: '0 0 12px 0',
    fontSize: '18px',
    fontWeight: '600',
    color: '#495057',
  },
  preparationDetail: {
    margin: '8px 0',
    fontSize: '14px',
    lineHeight: '1.6',
    color: '#495057',
  },
  priceRange: {
    marginTop: '15px',
    fontSize: '14px',
    color: '#495057',
    padding: '10px',
    backgroundColor: '#e7f5ff',
    borderRadius: '8px',
  },
  specialPopulations: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  populationItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    fontSize: '15px',
    color: '#495057',
  },
  populationIcon: {
    fontSize: '20px',
  },
  disclaimer: {
    padding: '20px',
    backgroundColor: '#fff3cd',
    border: '1px solid #ffc107',
    borderRadius: '12px',
    fontSize: '14px',
    lineHeight: '1.6',
    color: '#856404',
  },
  footer: {
    padding: '20px 30px',
    borderTop: '1px solid #eee',
    backgroundColor: '#f8f9fa',
  },
  footerInfo: {
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '13px',
    color: '#666',
  },
  loadingContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '60px 20px',
  },
  spinner: {
    width: '40px',
    height: '40px',
    border: '4px solid #f3f3f3',
    borderTop: '4px solid #667eea',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  errorContainer: {
    padding: '40px',
    textAlign: 'center',
  },
  errorText: {
    marginBottom: '20px',
    color: '#dc3545',
    fontSize: '16px',
  },
  closeBtn: {
    padding: '10px 24px',
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '14px',
    cursor: 'pointer',
  },
};

export default PlantDetail;
