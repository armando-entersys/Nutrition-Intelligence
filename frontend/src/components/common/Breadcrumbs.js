import React from 'react';

const Breadcrumbs = ({ items }) => {
  return (
    <nav style={styles.container}>
      <ol style={styles.breadcrumbList}>
        {items.map((item, index) => (
          <li key={index} style={styles.breadcrumbItem}>
            {index > 0 && <span style={styles.separator}>›</span>}
            {item.onClick ? (
              <button onClick={item.onClick} style={styles.link}>
                {item.label}
              </button>
            ) : (
              <span style={index === items.length - 1 ? styles.current : styles.label}>
                {item.label}
              </span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
};

const styles = {
  container: {
    padding: '12px 20px',
    backgroundColor: '#f8f9fa',
    borderBottom: '1px solid #e9ecef',
  },
  breadcrumbList: {
    display: 'flex',
    alignItems: 'center',
    listStyle: 'none',
    margin: 0,
    padding: 0,
    gap: '8px',
  },
  breadcrumbItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  separator: {
    color: '#95a5a6',
    fontSize: '16px',
    userSelect: 'none',
  },
  link: {
    background: 'none',
    border: 'none',
    color: '#3498db',
    cursor: 'pointer',
    fontSize: '14px',
    padding: '4px 8px',
    borderRadius: '4px',
    transition: 'background-color 0.2s',
    fontWeight: '500',
  },
  label: {
    color: '#7f8c8d',
    fontSize: '14px',
    fontWeight: '500',
  },
  current: {
    color: '#2c3e50',
    fontSize: '14px',
    fontWeight: '600',
  },
};

export default Breadcrumbs;
