import React from 'react';

/**
 * PlantCard Component
 * Displays a single medicinal plant card in the explorer grid
 */
const PlantCard = ({ plant, onClick }) => {
  // Get category label in Spanish
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

  // Get evidence level badge color and label
  const getEvidenceBadge = (level) => {
    const badges = {
      'STRONG_EVIDENCE': { color: '#28a745', label: 'Evidencia Fuerte' },
      'MODERATE_EVIDENCE': { color: '#ffc107', label: 'Evidencia Moderada' },
      'TRADITIONAL_ONLY': { color: '#6c757d', label: 'Tradicional' }
    };
    return badges[level] || { color: '#6c757d', label: level };
  };

  // Get safety level badge
  const getSafetyBadge = (level) => {
    const badges = {
      'VERY_SAFE': { color: '#28a745', label: 'Muy Segura', icon: '✓✓' },
      'SAFE': { color: '#17a2b8', label: 'Segura', icon: '✓' },
      'MODERATE': { color: '#ffc107', label: 'Precaución', icon: '⚠' }
    };
    return badges[level] || { color: '#6c757d', label: level, icon: '?' };
  };

  const evidenceBadge = getEvidenceBadge(plant.evidence_level);
  const safetyBadge = getSafetyBadge(plant.safety_level);

  return (
    <div style={styles.card} onClick={() => onClick(plant)}>
      {/* Plant Image */}
      <div style={styles.imageContainer}>
        {plant.main_image_url ? (
          <img
            src={plant.main_image_url}
            alt={plant.scientific_name}
            style={styles.image}
          />
        ) : (
          <div style={styles.placeholderImage}>
            <span style={styles.placeholderIcon}>🌿</span>
          </div>
        )}
      </div>

      {/* Plant Content */}
      <div style={styles.content}>
        {/* Scientific Name */}
        <h3 style={styles.scientificName}>{plant.scientific_name}</h3>

        {/* Popular Names */}
        <p style={styles.popularNames}>
          {plant.popular_names && plant.popular_names.length > 0
            ? plant.popular_names.slice(0, 2).join(', ')
            : 'Sin nombres comunes'
          }
        </p>

        {/* Category Badge */}
        <div style={styles.categoryBadge}>
          <span style={styles.categoryIcon}>🌱</span>
          {getCategoryLabel(plant.primary_category)}
        </div>

        {/* Evidence and Safety Badges */}
        <div style={styles.badges}>
          <span
            style={{
              ...styles.badge,
              backgroundColor: evidenceBadge.color + '20',
              color: evidenceBadge.color,
              border: `1px solid ${evidenceBadge.color}`
            }}
          >
            {evidenceBadge.label}
          </span>

          <span
            style={{
              ...styles.badge,
              backgroundColor: safetyBadge.color + '20',
              color: safetyBadge.color,
              border: `1px solid ${safetyBadge.color}`
            }}
          >
            {safetyBadge.icon} {safetyBadge.label}
          </span>
        </div>

        {/* Traditional Uses (preview) */}
        {plant.traditional_uses && plant.traditional_uses.length > 0 && (
          <div style={styles.uses}>
            <p style={styles.usesLabel}>Usos tradicionales:</p>
            <ul style={styles.usesList}>
              {plant.traditional_uses.slice(0, 2).map((use, index) => (
                <li key={index} style={styles.useItem}>{use}</li>
              ))}
              {plant.traditional_uses.length > 2 && (
                <li style={styles.moreUses}>
                  +{plant.traditional_uses.length - 2} más...
                </li>
              )}
            </ul>
          </div>
        )}

        {/* View Count */}
        <div style={styles.footer}>
          <span style={styles.viewCount}>
            👁 {plant.view_count || 0} vistas
          </span>
          <span style={styles.viewButton}>Ver más →</span>
        </div>
      </div>
    </div>
  );
};

const styles = {
  card: {
    backgroundColor: 'white',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    overflow: 'hidden',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
    ':hover': {
      transform: 'translateY(-4px)',
      boxShadow: '0 4px 20px rgba(0, 0, 0, 0.15)',
    },
  },
  imageContainer: {
    width: '100%',
    height: '200px',
    overflow: 'hidden',
    backgroundColor: '#f8f9fa',
  },
  image: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  },
  placeholderImage: {
    width: '100%',
    height: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#e9ecef',
  },
  placeholderIcon: {
    fontSize: '64px',
    opacity: 0.3,
  },
  content: {
    padding: '20px',
  },
  scientificName: {
    margin: '0 0 8px 0',
    fontSize: '18px',
    fontWeight: '600',
    color: '#2c3e50',
    fontStyle: 'italic',
  },
  popularNames: {
    margin: '0 0 12px 0',
    fontSize: '14px',
    color: '#666',
    minHeight: '20px',
  },
  categoryBadge: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '5px',
    padding: '4px 12px',
    backgroundColor: '#e7f5ff',
    color: '#1971c2',
    borderRadius: '16px',
    fontSize: '12px',
    fontWeight: '500',
    marginBottom: '12px',
  },
  categoryIcon: {
    fontSize: '14px',
  },
  badges: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '8px',
    marginBottom: '15px',
  },
  badge: {
    padding: '4px 10px',
    borderRadius: '12px',
    fontSize: '11px',
    fontWeight: '500',
    display: 'inline-block',
  },
  uses: {
    marginBottom: '15px',
  },
  usesLabel: {
    margin: '0 0 6px 0',
    fontSize: '12px',
    fontWeight: '600',
    color: '#495057',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  usesList: {
    margin: 0,
    paddingLeft: '20px',
    fontSize: '13px',
    color: '#666',
  },
  useItem: {
    marginBottom: '3px',
  },
  moreUses: {
    color: '#007bff',
    fontWeight: '500',
    marginTop: '4px',
  },
  footer: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: '12px',
    borderTop: '1px solid #eee',
  },
  viewCount: {
    fontSize: '12px',
    color: '#868e96',
  },
  viewButton: {
    fontSize: '13px',
    color: '#007bff',
    fontWeight: '500',
  },
};

export default PlantCard;
