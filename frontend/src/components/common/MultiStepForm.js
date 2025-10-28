import React, { useState } from 'react';

const MultiStepForm = ({ steps, onComplete, onCancel, initialData = {} }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState(initialData);
  const [errors, setErrors] = useState({});

  const updateFormData = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));

    // Limpiar error del campo cuando el usuario empieza a escribir
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const validateStep = () => {
    const step = steps[currentStep];
    if (!step.validate) return true;

    const stepErrors = step.validate(formData);
    if (Object.keys(stepErrors).length > 0) {
      setErrors(stepErrors);
      return false;
    }
    return true;
  };

  const handleNext = () => {
    if (validateStep()) {
      if (currentStep < steps.length - 1) {
        setCurrentStep(currentStep + 1);
        setErrors({});
      } else {
        // Último paso - enviar formulario
        onComplete(formData);
      }
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
      setErrors({});
    }
  };

  const currentStepData = steps[currentStep];
  const progress = ((currentStep + 1) / steps.length) * 100;

  return (
    <div style={styles.container}>
      {/* Progress Bar */}
      <div style={styles.progressContainer}>
        <div style={styles.progressBar}>
          <div style={{ ...styles.progressFill, width: `${progress}%` }} />
        </div>
        <div style={styles.progressText}>
          Paso {currentStep + 1} de {steps.length}: {currentStepData.title}
        </div>
      </div>

      {/* Step Indicators */}
      <div style={styles.stepIndicators}>
        {steps.map((step, index) => (
          <div key={index} style={styles.stepIndicator}>
            <div
              style={{
                ...styles.stepCircle,
                ...(index === currentStep ? styles.stepCircleActive : {}),
                ...(index < currentStep ? styles.stepCircleCompleted : {})
              }}
            >
              {index < currentStep ? '✓' : index + 1}
            </div>
            <div style={styles.stepLabel}>{step.title}</div>
          </div>
        ))}
      </div>

      {/* Step Content */}
      <div style={styles.stepContent}>
        {currentStepData.description && (
          <p style={styles.stepDescription}>{currentStepData.description}</p>
        )}

        {currentStepData.render({
          formData,
          updateFormData,
          errors
        })}
      </div>

      {/* Action Buttons */}
      <div style={styles.actions}>
        <button
          onClick={onCancel}
          style={styles.cancelButton}
          type="button"
        >
          Cancelar
        </button>

        <div style={styles.navigationButtons}>
          {currentStep > 0 && (
            <button
              onClick={handleBack}
              style={styles.backButton}
              type="button"
            >
              ← Atrás
            </button>
          )}

          <button
            onClick={handleNext}
            style={styles.nextButton}
            type="button"
          >
            {currentStep < steps.length - 1 ? 'Siguiente →' : '✓ Completar'}
          </button>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '30px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  },
  progressContainer: {
    marginBottom: '30px',
  },
  progressBar: {
    width: '100%',
    height: '8px',
    backgroundColor: '#e9ecef',
    borderRadius: '4px',
    overflow: 'hidden',
    marginBottom: '10px',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#3498db',
    transition: 'width 0.3s ease',
  },
  progressText: {
    fontSize: '14px',
    color: '#7f8c8d',
    fontWeight: '600',
  },
  stepIndicators: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '40px',
    position: 'relative',
  },
  stepIndicator: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    position: 'relative',
  },
  stepCircle: {
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    backgroundColor: '#e9ecef',
    color: '#95a5a6',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: '700',
    fontSize: '16px',
    marginBottom: '8px',
    transition: 'all 0.3s ease',
  },
  stepCircleActive: {
    backgroundColor: '#3498db',
    color: 'white',
    transform: 'scale(1.1)',
  },
  stepCircleCompleted: {
    backgroundColor: '#27ae60',
    color: 'white',
  },
  stepLabel: {
    fontSize: '12px',
    color: '#7f8c8d',
    textAlign: 'center',
    fontWeight: '500',
  },
  stepContent: {
    minHeight: '300px',
    marginBottom: '30px',
  },
  stepDescription: {
    fontSize: '14px',
    color: '#7f8c8d',
    marginBottom: '20px',
    lineHeight: '1.6',
  },
  actions: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: '20px',
    borderTop: '1px solid #e9ecef',
  },
  cancelButton: {
    padding: '10px 20px',
    backgroundColor: 'white',
    border: '2px solid #e74c3c',
    color: '#e74c3c',
    borderRadius: '6px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  navigationButtons: {
    display: 'flex',
    gap: '10px',
  },
  backButton: {
    padding: '10px 20px',
    backgroundColor: '#f8f9fa',
    border: '2px solid #e9ecef',
    color: '#2c3e50',
    borderRadius: '6px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  nextButton: {
    padding: '10px 30px',
    backgroundColor: '#3498db',
    border: 'none',
    color: 'white',
    borderRadius: '6px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
};

export default MultiStepForm;
