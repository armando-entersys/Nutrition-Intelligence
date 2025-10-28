import React from 'react';

// Skeleton genérico
export const Skeleton = ({ width = '100%', height = '20px', borderRadius = '4px', style = {} }) => {
  return (
    <div
      style={{
        ...styles.skeleton,
        width,
        height,
        borderRadius,
        ...style,
      }}
    />
  );
};

// Skeleton para cards (como pacientes, alimentos, etc.)
export const SkeletonCard = ({ count = 1 }) => {
  return (
    <>
      {Array.from({ length: count }).map((_, index) => (
        <div key={index} style={styles.card}>
          <div style={styles.cardHeader}>
            <Skeleton width="60%" height="24px" />
            <Skeleton width="60px" height="24px" borderRadius="12px" />
          </div>
          <Skeleton width="80%" height="16px" style={{ marginTop: '12px' }} />
          <Skeleton width="70%" height="16px" style={{ marginTop: '8px' }} />
          <Skeleton width="90%" height="16px" style={{ marginTop: '8px' }} />
        </div>
      ))}
    </>
  );
};

// Skeleton para tabla
export const SkeletonTable = ({ rows = 5, columns = 4 }) => {
  return (
    <div style={styles.table}>
      {/* Header */}
      <div style={styles.tableRow}>
        {Array.from({ length: columns }).map((_, index) => (
          <div key={index} style={styles.tableCell}>
            <Skeleton height="20px" />
          </div>
        ))}
      </div>

      {/* Rows */}
      {Array.from({ length: rows }).map((_, rowIndex) => (
        <div key={rowIndex} style={styles.tableRow}>
          {Array.from({ length: columns }).map((_, colIndex) => (
            <div key={colIndex} style={styles.tableCell}>
              <Skeleton height="16px" />
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

// Skeleton para formulario
export const SkeletonForm = ({ fields = 6 }) => {
  return (
    <div style={styles.form}>
      {Array.from({ length: fields }).map((_, index) => (
        <div key={index} style={styles.formField}>
          <Skeleton width="120px" height="16px" style={{ marginBottom: '8px' }} />
          <Skeleton width="100%" height="40px" />
        </div>
      ))}
    </div>
  );
};

// Skeleton para detalles de paciente
export const SkeletonPatientDetails = () => {
  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: '25px' }}>
        <Skeleton width="250px" height="32px" style={{ marginBottom: '15px' }} />
        <div style={{ display: 'flex', gap: '10px' }}>
          <Skeleton width="100px" height="36px" borderRadius="6px" />
          <Skeleton width="100px" height="36px" borderRadius="6px" />
        </div>
      </div>

      {/* Info Cards */}
      <div style={styles.cardsGrid}>
        {Array.from({ length: 3 }).map((_, index) => (
          <div key={index} style={styles.infoCard}>
            <Skeleton width="150px" height="20px" style={{ marginBottom: '15px' }} />
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} style={{ marginBottom: '10px' }}>
                <Skeleton width="100%" height="16px" />
              </div>
            ))}
          </div>
        ))}
      </div>

      {/* Plan Section */}
      <div style={{ marginTop: '25px', padding: '20px', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
        <Skeleton width="180px" height="22px" style={{ marginBottom: '20px' }} />
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '15px' }}>
          {Array.from({ length: 4 }).map((_, index) => (
            <div key={index} style={{ textAlign: 'center' }}>
              <Skeleton width="100%" height="60px" style={{ marginBottom: '8px' }} />
              <Skeleton width="80%" height="16px" style={{ margin: '0 auto' }} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const styles = {
  skeleton: {
    backgroundColor: '#e9ecef',
    position: 'relative',
    overflow: 'hidden',
    animation: 'pulse 1.5s ease-in-out infinite',
  },
  card: {
    padding: '15px',
    border: '2px solid #e9ecef',
    borderRadius: '8px',
    marginBottom: '10px',
    backgroundColor: 'white',
  },
  cardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  table: {
    width: '100%',
  },
  tableRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
    gap: '15px',
    padding: '12px',
    borderBottom: '1px solid #e9ecef',
  },
  tableCell: {
    padding: '4px',
  },
  form: {
    display: 'grid',
    gap: '20px',
  },
  formField: {
    display: 'flex',
    flexDirection: 'column',
  },
  cardsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px',
  },
  infoCard: {
    padding: '20px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    border: '1px solid #e9ecef',
  },
};

// Agregar animación de pulso
if (typeof document !== 'undefined') {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = `
    @keyframes pulse {
      0%, 100% {
        opacity: 1;
      }
      50% {
        opacity: 0.5;
      }
    }

    @keyframes shimmer {
      0% {
        transform: translateX(-100%);
      }
      100% {
        transform: translateX(100%);
      }
    }
  `;
  document.head.appendChild(styleSheet);
}

export default Skeleton;
