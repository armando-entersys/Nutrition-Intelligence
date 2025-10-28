import React, { useState } from 'react';

const FormField = ({
  label,
  type = 'text',
  value,
  onChange,
  error,
  required = false,
  placeholder = '',
  validate,
  helpText,
  min,
  max,
  step,
  options = [], // Para select
  rows = 3, // Para textarea
}) => {
  const [touched, setTouched] = useState(false);
  const [localError, setLocalError] = useState('');

  const handleBlur = () => {
    setTouched(true);
    if (validate && value) {
      const validationError = validate(value);
      setLocalError(validationError || '');
    }
  };

  const handleChange = (e) => {
    const newValue = e.target.value;
    onChange(newValue);

    // Validación en tiempo real mientras escribe
    if (touched && validate) {
      const validationError = validate(newValue);
      setLocalError(validationError || '');
    }
  };

  const displayError = error || (touched && localError);
  const isValid = touched && !displayError && value;

  const renderInput = () => {
    const baseStyle = {
      ...styles.input,
      ...(displayError ? styles.inputError : {}),
      ...(isValid ? styles.inputValid : {}),
    };

    switch (type) {
      case 'textarea':
        return (
          <textarea
            value={value}
            onChange={handleChange}
            onBlur={handleBlur}
            placeholder={placeholder}
            required={required}
            style={{ ...baseStyle, ...styles.textarea }}
            rows={rows}
          />
        );

      case 'select':
        return (
          <select
            value={value}
            onChange={handleChange}
            onBlur={handleBlur}
            required={required}
            style={baseStyle}
          >
            <option value="">Seleccionar...</option>
            {options.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        );

      default:
        return (
          <input
            type={type}
            value={value}
            onChange={handleChange}
            onBlur={handleBlur}
            placeholder={placeholder}
            required={required}
            min={min}
            max={max}
            step={step}
            style={baseStyle}
          />
        );
    }
  };

  return (
    <div style={styles.fieldContainer}>
      <label style={styles.label}>
        {label}
        {required && <span style={styles.required}>*</span>}
      </label>

      <div style={styles.inputContainer}>
        {renderInput()}

        {isValid && (
          <span style={styles.validIcon}>✓</span>
        )}
      </div>

      {displayError && (
        <div style={styles.errorMessage}>
          <span style={styles.errorIcon}>⚠️</span>
          {displayError}
        </div>
      )}

      {helpText && !displayError && (
        <div style={styles.helpText}>{helpText}</div>
      )}
    </div>
  );
};

const styles = {
  fieldContainer: {
    marginBottom: '20px',
  },
  label: {
    display: 'block',
    fontSize: '14px',
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: '8px',
  },
  required: {
    color: '#e74c3c',
    marginLeft: '4px',
  },
  inputContainer: {
    position: 'relative',
  },
  input: {
    width: '100%',
    padding: '12px 40px 12px 12px',
    border: '2px solid #e9ecef',
    borderRadius: '6px',
    fontSize: '14px',
    color: '#2c3e50',
    transition: 'all 0.2s',
    outline: 'none',
    boxSizing: 'border-box',
  },
  textarea: {
    resize: 'vertical',
    fontFamily: 'inherit',
  },
  inputError: {
    borderColor: '#e74c3c',
    backgroundColor: '#fff5f5',
  },
  inputValid: {
    borderColor: '#27ae60',
    backgroundColor: '#f0fff4',
  },
  validIcon: {
    position: 'absolute',
    right: '12px',
    top: '50%',
    transform: 'translateY(-50%)',
    color: '#27ae60',
    fontWeight: 'bold',
    fontSize: '18px',
  },
  errorMessage: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    marginTop: '6px',
    fontSize: '13px',
    color: '#e74c3c',
  },
  errorIcon: {
    fontSize: '14px',
  },
  helpText: {
    marginTop: '6px',
    fontSize: '12px',
    color: '#95a5a6',
    lineHeight: '1.4',
  },
};

export default FormField;
