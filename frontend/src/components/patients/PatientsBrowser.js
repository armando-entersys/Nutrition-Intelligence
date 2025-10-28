import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';
import MultiStepForm from '../common/MultiStepForm';
import FormField from '../common/FormField';

const PatientsBrowser = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [showPlanForm, setShowPlanForm] = useState(false);

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    birth_date: '',
    gender: 'M',
    height_cm: '',
    weight_kg: '',
    activity_level: 'SEDENTARY',
    medical_conditions: '',
    allergies: '',
    dietary_preferences: '',
    notes: ''
  });

  const [planFormData, setPlanFormData] = useState({
    goal: 'WEIGHT_LOSS',
    target_calories: '',
    target_protein_g: '',
    target_carbs_g: '',
    target_fat_g: '',
    duration_weeks: '',
    notes: ''
  });

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    setLoading(true);
    try {
      // Mock patients data
      const mockPatients = [
        {
          id: 1,
          name: 'María González',
          email: 'maria.gonzalez@example.com',
          phone: '+34 612 345 678',
          birth_date: '1985-03-15',
          gender: 'F',
          height_cm: 165,
          weight_kg: 68,
          activity_level: 'MODERATE',
          medical_conditions: 'Diabetes tipo 2',
          allergies: 'Ninguna',
          dietary_preferences: 'Vegetariana',
          bmi: 25.0,
          created_at: '2024-01-15',
          last_visit: '2024-10-20',
          nutritional_plan: {
            id: 1,
            goal: 'WEIGHT_LOSS',
            target_calories: 1800,
            target_protein_g: 90,
            target_carbs_g: 180,
            target_fat_g: 60,
            duration_weeks: 12,
            progress: 45
          },
          measurements: [
            { date: '2024-10-01', weight_kg: 70, bmi: 25.7 },
            { date: '2024-10-15', weight_kg: 68.5, bmi: 25.2 },
            { date: '2024-10-27', weight_kg: 68, bmi: 25.0 }
          ]
        },
        {
          id: 2,
          name: 'Carlos Rodríguez',
          email: 'carlos.rodriguez@example.com',
          phone: '+34 623 456 789',
          birth_date: '1990-07-22',
          gender: 'M',
          height_cm: 178,
          weight_kg: 85,
          activity_level: 'ACTIVE',
          medical_conditions: 'Ninguna',
          allergies: 'Frutos secos',
          dietary_preferences: 'Sin restricciones',
          bmi: 26.8,
          created_at: '2024-02-10',
          last_visit: '2024-10-25',
          nutritional_plan: {
            id: 2,
            goal: 'MUSCLE_GAIN',
            target_calories: 2800,
            target_protein_g: 170,
            target_carbs_g: 300,
            target_fat_g: 85,
            duration_weeks: 16,
            progress: 60
          },
          measurements: [
            { date: '2024-09-15', weight_kg: 82, bmi: 25.9 },
            { date: '2024-10-01', weight_kg: 84, bmi: 26.5 },
            { date: '2024-10-25', weight_kg: 85, bmi: 26.8 }
          ]
        },
        {
          id: 3,
          name: 'Ana Martínez',
          email: 'ana.martinez@example.com',
          phone: '+34 634 567 890',
          birth_date: '1978-11-08',
          gender: 'F',
          height_cm: 160,
          weight_kg: 62,
          activity_level: 'LIGHT',
          medical_conditions: 'Hipertensión',
          allergies: 'Lactosa',
          dietary_preferences: 'Baja en sodio',
          bmi: 24.2,
          created_at: '2024-03-20',
          last_visit: '2024-10-22',
          nutritional_plan: {
            id: 3,
            goal: 'MAINTENANCE',
            target_calories: 1900,
            target_protein_g: 75,
            target_carbs_g: 200,
            target_fat_g: 65,
            duration_weeks: 8,
            progress: 30
          },
          measurements: [
            { date: '2024-09-20', weight_kg: 63, bmi: 24.6 },
            { date: '2024-10-05', weight_kg: 62.5, bmi: 24.4 },
            { date: '2024-10-22', weight_kg: 62, bmi: 24.2 }
          ]
        }
      ];
      setPatients(mockPatients);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching patients:', error);
      setLoading(false);
    }
  };

  const calculateBMI = (weight, height) => {
    const heightM = height / 100;
    return (weight / (heightM * heightM)).toFixed(1);
  };

  const calculateAge = (birthDate) => {
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age;
  };

  const handleFormChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePlanFormChange = (field, value) => {
    setPlanFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSelectPatient = (patient) => {
    setSelectedPatient(patient);
    setShowAddForm(false);
    setShowEditForm(false);
    setShowPlanForm(false);
  };

  const handleAddNew = () => {
    setFormData({
      name: '',
      email: '',
      phone: '',
      birth_date: '',
      gender: 'M',
      height_cm: '',
      weight_kg: '',
      activity_level: 'SEDENTARY',
      medical_conditions: '',
      allergies: '',
      dietary_preferences: '',
      notes: ''
    });
    setShowAddForm(true);
    setShowEditForm(false);
    setSelectedPatient(null);
    setShowPlanForm(false);
  };

  const handleEdit = () => {
    if (selectedPatient) {
      setFormData({
        name: selectedPatient.name,
        email: selectedPatient.email,
        phone: selectedPatient.phone,
        birth_date: selectedPatient.birth_date,
        gender: selectedPatient.gender,
        height_cm: selectedPatient.height_cm,
        weight_kg: selectedPatient.weight_kg,
        activity_level: selectedPatient.activity_level,
        medical_conditions: selectedPatient.medical_conditions || '',
        allergies: selectedPatient.allergies || '',
        dietary_preferences: selectedPatient.dietary_preferences || '',
        notes: selectedPatient.notes || ''
      });
      setShowEditForm(true);
      setShowAddForm(false);
      setShowPlanForm(false);
    }
  };

  const handleSaveNew = async () => {
    try {
      const bmi = calculateBMI(parseFloat(formData.weight_kg), parseFloat(formData.height_cm));
      const newPatient = {
        id: patients.length + 1,
        ...formData,
        weight_kg: parseFloat(formData.weight_kg),
        height_cm: parseFloat(formData.height_cm),
        bmi: parseFloat(bmi),
        created_at: new Date().toISOString().split('T')[0],
        last_visit: new Date().toISOString().split('T')[0],
        measurements: [{
          date: new Date().toISOString().split('T')[0],
          weight_kg: parseFloat(formData.weight_kg),
          bmi: parseFloat(bmi)
        }]
      };

      setPatients(prev => [...prev, newPatient]);
      setSelectedPatient(newPatient);
      setShowAddForm(false);
      alert('Paciente agregado exitosamente');
    } catch (error) {
      console.error('Error adding patient:', error);
      alert('Error al agregar paciente');
    }
  };

  const handleSaveEdit = async () => {
    try {
      const bmi = calculateBMI(parseFloat(formData.weight_kg), parseFloat(formData.height_cm));
      const updatedPatient = {
        ...selectedPatient,
        ...formData,
        weight_kg: parseFloat(formData.weight_kg),
        height_cm: parseFloat(formData.height_cm),
        bmi: parseFloat(bmi)
      };

      setPatients(prev => prev.map(p => p.id === selectedPatient.id ? updatedPatient : p));
      setSelectedPatient(updatedPatient);
      setShowEditForm(false);
      alert('Paciente actualizado exitosamente');
    } catch (error) {
      console.error('Error updating patient:', error);
      alert('Error al actualizar paciente');
    }
  };

  const handleDelete = async () => {
    if (selectedPatient && window.confirm(`¿Estás seguro de eliminar al paciente ${selectedPatient.name}?`)) {
      try {
        setPatients(prev => prev.filter(p => p.id !== selectedPatient.id));
        setSelectedPatient(null);
        alert('Paciente eliminado exitosamente');
      } catch (error) {
        console.error('Error deleting patient:', error);
        alert('Error al eliminar paciente');
      }
    }
  };

  const handleAssignPlan = () => {
    setPlanFormData({
      goal: 'WEIGHT_LOSS',
      target_calories: '',
      target_protein_g: '',
      target_carbs_g: '',
      target_fat_g: '',
      duration_weeks: '',
      notes: ''
    });
    setShowPlanForm(true);
    setShowAddForm(false);
    setShowEditForm(false);
  };

  const handleSavePlan = () => {
    if (selectedPatient) {
      const newPlan = {
        id: (selectedPatient.nutritional_plan?.id || 0) + 1,
        ...planFormData,
        target_calories: parseFloat(planFormData.target_calories),
        target_protein_g: parseFloat(planFormData.target_protein_g),
        target_carbs_g: parseFloat(planFormData.target_carbs_g),
        target_fat_g: parseFloat(planFormData.target_fat_g),
        duration_weeks: parseInt(planFormData.duration_weeks),
        progress: 0,
        created_at: new Date().toISOString()
      };

      const updatedPatient = {
        ...selectedPatient,
        nutritional_plan: newPlan
      };

      setPatients(prev => prev.map(p => p.id === selectedPatient.id ? updatedPatient : p));
      setSelectedPatient(updatedPatient);
      setShowPlanForm(false);
      alert('Plan nutricional asignado exitosamente');
    }
  };

  const filteredPatients = patients.filter(patient =>
    patient.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    patient.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getActivityLevelLabel = (level) => {
    const labels = {
      'SEDENTARY': 'Sedentario',
      'LIGHT': 'Ligera',
      'MODERATE': 'Moderada',
      'ACTIVE': 'Activa',
      'VERY_ACTIVE': 'Muy Activa'
    };
    return labels[level] || level;
  };

  const getGoalLabel = (goal) => {
    const labels = {
      'WEIGHT_LOSS': 'Pérdida de Peso',
      'WEIGHT_GAIN': 'Aumento de Peso',
      'MUSCLE_GAIN': 'Ganancia Muscular',
      'MAINTENANCE': 'Mantenimiento'
    };
    return labels[goal] || goal;
  };

  const getBMICategory = (bmi) => {
    if (bmi < 18.5) return { text: 'Bajo Peso', color: '#3498db' };
    if (bmi < 25) return { text: 'Normal', color: '#27ae60' };
    if (bmi < 30) return { text: 'Sobrepeso', color: '#f39c12' };
    return { text: 'Obesidad', color: '#e74c3c' };
  };

  // Validators for form fields
  const validators = {
    email: (value) => {
      if (!value) return 'El email es requerido';
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        return 'Email inválido';
      }
      return '';
    },
    phone: (value) => {
      if (value && !/^\+?[\d\s-]{9,}$/.test(value)) {
        return 'Teléfono inválido';
      }
      return '';
    },
    height: (value) => {
      const num = parseFloat(value);
      if (!num || num < 50 || num > 250) {
        return 'Altura debe estar entre 50-250 cm';
      }
      return '';
    },
    weight: (value) => {
      const num = parseFloat(value);
      if (!num || num < 20 || num > 300) {
        return 'Peso debe estar entre 20-300 kg';
      }
      return '';
    }
  };

  // Multi-step form configuration
  const patientFormSteps = [
    {
      title: 'Datos Personales',
      description: 'Información básica del paciente',
      validate: (data) => {
        const errors = {};
        if (!data.name || data.name.trim().length < 3) {
          errors.name = 'El nombre debe tener al menos 3 caracteres';
        }
        const emailError = validators.email(data.email);
        if (emailError) errors.email = emailError;

        const phoneError = validators.phone(data.phone);
        if (phoneError) errors.phone = phoneError;

        if (!data.birth_date) {
          errors.birth_date = 'La fecha de nacimiento es requerida';
        }
        return errors;
      },
      render: ({ formData, updateFormData, errors }) => (
        <div style={{ display: 'grid', gap: '15px' }}>
          <FormField
            label="Nombre Completo"
            value={formData.name || ''}
            onChange={(value) => updateFormData('name', value)}
            error={errors.name}
            required
            placeholder="Ej: María González"
          />
          <FormField
            label="Email"
            type="email"
            value={formData.email || ''}
            onChange={(value) => updateFormData('email', value)}
            error={errors.email}
            required
            validate={validators.email}
            placeholder="correo@ejemplo.com"
          />
          <FormField
            label="Teléfono"
            type="tel"
            value={formData.phone || ''}
            onChange={(value) => updateFormData('phone', value)}
            error={errors.phone}
            validate={validators.phone}
            placeholder="+34 612 345 678"
            helpText="Formato: +34 XXX XXX XXX"
          />
          <FormField
            label="Fecha de Nacimiento"
            type="date"
            value={formData.birth_date || ''}
            onChange={(value) => updateFormData('birth_date', value)}
            error={errors.birth_date}
            required
          />
          <FormField
            label="Género"
            type="select"
            value={formData.gender || 'M'}
            onChange={(value) => updateFormData('gender', value)}
            required
            options={[
              { value: 'M', label: 'Masculino' },
              { value: 'F', label: 'Femenino' },
              { value: 'O', label: 'Otro' }
            ]}
          />
        </div>
      )
    },
    {
      title: 'Mediciones',
      description: 'Datos antropométricos del paciente',
      validate: (data) => {
        const errors = {};
        const heightError = validators.height(data.height_cm);
        if (heightError) errors.height_cm = heightError;

        const weightError = validators.weight(data.weight_kg);
        if (weightError) errors.weight_kg = weightError;

        return errors;
      },
      render: ({ formData, updateFormData, errors }) => {
        const bmi = formData.height_cm && formData.weight_kg
          ? calculateBMI(parseFloat(formData.weight_kg), parseFloat(formData.height_cm))
          : null;
        const bmiCategory = bmi ? getBMICategory(parseFloat(bmi)) : null;

        return (
          <div style={{ display: 'grid', gap: '15px' }}>
            <FormField
              label="Altura (cm)"
              type="number"
              value={formData.height_cm || ''}
              onChange={(value) => updateFormData('height_cm', value)}
              error={errors.height_cm}
              required
              validate={validators.height}
              placeholder="165"
              min="50"
              max="250"
              helpText="Entre 50 y 250 cm"
            />
            <FormField
              label="Peso (kg)"
              type="number"
              value={formData.weight_kg || ''}
              onChange={(value) => updateFormData('weight_kg', value)}
              error={errors.weight_kg}
              required
              validate={validators.weight}
              placeholder="68.5"
              min="20"
              max="300"
              step="0.1"
              helpText="Entre 20 y 300 kg"
            />
            <FormField
              label="Nivel de Actividad"
              type="select"
              value={formData.activity_level || 'SEDENTARY'}
              onChange={(value) => updateFormData('activity_level', value)}
              options={[
                { value: 'SEDENTARY', label: 'Sedentario (poco o ningún ejercicio)' },
                { value: 'LIGHT', label: 'Ligera (1-3 días/semana)' },
                { value: 'MODERATE', label: 'Moderada (3-5 días/semana)' },
                { value: 'ACTIVE', label: 'Activa (6-7 días/semana)' },
                { value: 'VERY_ACTIVE', label: 'Muy Activa (deportista)' }
              ]}
            />
            {bmi && (
              <div style={{
                padding: '15px',
                backgroundColor: '#f8f9fa',
                borderRadius: '8px',
                border: `2px solid ${bmiCategory.color}`
              }}>
                <div style={{ fontSize: '14px', color: '#7f8c8d', marginBottom: '5px' }}>
                  IMC Calculado:
                </div>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: bmiCategory.color }}>
                  {bmi}
                </div>
                <div style={{ fontSize: '13px', color: '#7f8c8d', marginTop: '5px' }}>
                  Categoría: {bmiCategory.text}
                </div>
              </div>
            )}
          </div>
        );
      }
    },
    {
      title: 'Información Médica',
      description: 'Condiciones médicas y preferencias dietéticas',
      render: ({ formData, updateFormData }) => (
        <div style={{ display: 'grid', gap: '15px' }}>
          <FormField
            label="Condiciones Médicas"
            type="textarea"
            value={formData.medical_conditions || ''}
            onChange={(value) => updateFormData('medical_conditions', value)}
            placeholder="Diabetes, hipertensión, etc."
            rows={3}
            helpText="Enumera las condiciones médicas relevantes"
          />
          <FormField
            label="Alergias"
            type="textarea"
            value={formData.allergies || ''}
            onChange={(value) => updateFormData('allergies', value)}
            placeholder="Lactosa, frutos secos, gluten, etc."
            rows={2}
            helpText="Alergias e intolerancias alimentarias"
          />
          <FormField
            label="Preferencias Dietéticas"
            type="textarea"
            value={formData.dietary_preferences || ''}
            onChange={(value) => updateFormData('dietary_preferences', value)}
            placeholder="Vegetariano, vegano, sin gluten, etc."
            rows={2}
            helpText="Dietas especiales o restricciones alimentarias"
          />
          <FormField
            label="Notas Adicionales"
            type="textarea"
            value={formData.notes || ''}
            onChange={(value) => updateFormData('notes', value)}
            placeholder="Información adicional relevante..."
            rows={3}
            helpText="Cualquier otra información importante"
          />
        </div>
      )
    }
  ];

  const handleMultiStepComplete = async (data) => {
    if (showEditForm) {
      // Modo edición
      try {
        const bmi = calculateBMI(parseFloat(data.weight_kg), parseFloat(data.height_cm));
        const updatedPatient = {
          ...selectedPatient,
          ...data,
          weight_kg: parseFloat(data.weight_kg),
          height_cm: parseFloat(data.height_cm),
          bmi: parseFloat(bmi),
          measurements: [
            ...(selectedPatient.measurements || []),
            {
              date: new Date().toISOString().split('T')[0],
              weight_kg: parseFloat(data.weight_kg),
              bmi: parseFloat(bmi)
            }
          ]
        };
        setPatients(prev => prev.map(p => p.id === selectedPatient.id ? updatedPatient : p));
        setSelectedPatient(updatedPatient);
        setShowEditForm(false);
        alert('Paciente actualizado exitosamente');
      } catch (error) {
        console.error('Error updating patient:', error);
        alert('Error al actualizar paciente');
      }
    } else {
      // Modo agregar nuevo
      await handleSaveNew();
    }
  };

  const handleMultiStepCancel = () => {
    setShowAddForm(false);
    setShowEditForm(false);
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>👥 Gestión de Pacientes</h1>
        <p style={styles.subtitle}>Administra perfiles de pacientes y sus planes nutricionales</p>
      </div>

      <div style={styles.mainContent}>
        {/* Left Panel - Patients List */}
        <div style={styles.leftPanel}>
          <div style={styles.controlsBar}>
            <input
              type="text"
              placeholder="Buscar paciente..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={styles.searchInput}
            />
            <button onClick={handleAddNew} style={styles.addButton}>
              ➕ Nuevo Paciente
            </button>
          </div>

          <div style={styles.patientsList}>
            <h3 style={styles.listTitle}>Pacientes ({filteredPatients.length})</h3>
            {loading ? (
              <p>Cargando pacientes...</p>
            ) : (
              filteredPatients.map(patient => (
                <div
                  key={patient.id}
                  onClick={() => handleSelectPatient(patient)}
                  style={{
                    ...styles.patientCard,
                    ...(selectedPatient?.id === patient.id ? styles.selectedCard : {})
                  }}
                >
                  <div style={styles.patientCardHeader}>
                    <h4 style={styles.patientName}>{patient.name}</h4>
                    <span style={{
                      ...styles.badge,
                      backgroundColor: getBMICategory(patient.bmi).color
                    }}>
                      IMC: {patient.bmi}
                    </span>
                  </div>
                  <p style={styles.patientInfo}>📧 {patient.email}</p>
                  <p style={styles.patientInfo}>📞 {patient.phone}</p>
                  <p style={styles.patientInfo}>
                    🎂 {calculateAge(patient.birth_date)} años | {patient.gender === 'M' ? '♂️' : '♀️'}
                  </p>
                  <p style={styles.patientInfo}>
                    📊 {patient.weight_kg} kg | {patient.height_cm} cm
                  </p>
                  {patient.nutritional_plan && (
                    <div style={styles.planPreview}>
                      <span style={styles.planBadge}>
                        🎯 {getGoalLabel(patient.nutritional_plan.goal)}
                      </span>
                      <div style={styles.progressBar}>
                        <div style={{
                          ...styles.progressFill,
                          width: `${patient.nutritional_plan.progress}%`
                        }} />
                      </div>
                      <span style={styles.progressText}>
                        {patient.nutritional_plan.progress}% completado
                      </span>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right Panel - Patient Details / Forms */}
        <div style={styles.rightPanel}>
          {showAddForm || showEditForm ? (
            <div>
              <h2>{showEditForm ? '✏️ Editar Paciente' : '➕ Agregar Nuevo Paciente'}</h2>
              <MultiStepForm
                steps={patientFormSteps}
                onComplete={handleMultiStepComplete}
                onCancel={handleMultiStepCancel}
                initialData={showEditForm ? formData : {
                  name: '',
                  email: '',
                  phone: '',
                  birth_date: '',
                  gender: 'M',
                  height_cm: '',
                  weight_kg: '',
                  activity_level: 'SEDENTARY',
                  medical_conditions: '',
                  allergies: '',
                  dietary_preferences: '',
                  notes: ''
                }}
              />
            </div>
          ) : showPlanForm ? (
            <div style={styles.formContainer}>
              <h2>🎯 Asignar Plan Nutricional</h2>
              <p style={styles.formSubtitle}>Paciente: {selectedPatient?.name}</p>

              <div style={styles.formSection}>
                <div style={styles.formGroup}>
                  <label style={styles.label}>Objetivo del Plan *</label>
                  <select
                    value={planFormData.goal}
                    onChange={(e) => handlePlanFormChange('goal', e.target.value)}
                    style={styles.select}
                  >
                    <option value="WEIGHT_LOSS">Pérdida de Peso</option>
                    <option value="WEIGHT_GAIN">Aumento de Peso</option>
                    <option value="MUSCLE_GAIN">Ganancia Muscular</option>
                    <option value="MAINTENANCE">Mantenimiento</option>
                  </select>
                </div>

                <div style={styles.formGrid}>
                  <div style={styles.formGroup}>
                    <label style={styles.label}>Calorías Objetivo (kcal) *</label>
                    <input
                      type="number"
                      value={planFormData.target_calories}
                      onChange={(e) => handlePlanFormChange('target_calories', e.target.value)}
                      placeholder="1800"
                      style={styles.input}
                    />
                  </div>

                  <div style={styles.formGroup}>
                    <label style={styles.label}>Proteínas (g) *</label>
                    <input
                      type="number"
                      value={planFormData.target_protein_g}
                      onChange={(e) => handlePlanFormChange('target_protein_g', e.target.value)}
                      placeholder="90"
                      style={styles.input}
                    />
                  </div>

                  <div style={styles.formGroup}>
                    <label style={styles.label}>Carbohidratos (g) *</label>
                    <input
                      type="number"
                      value={planFormData.target_carbs_g}
                      onChange={(e) => handlePlanFormChange('target_carbs_g', e.target.value)}
                      placeholder="180"
                      style={styles.input}
                    />
                  </div>

                  <div style={styles.formGroup}>
                    <label style={styles.label}>Grasas (g) *</label>
                    <input
                      type="number"
                      value={planFormData.target_fat_g}
                      onChange={(e) => handlePlanFormChange('target_fat_g', e.target.value)}
                      placeholder="60"
                      style={styles.input}
                    />
                  </div>

                  <div style={styles.formGroup}>
                    <label style={styles.label}>Duración (semanas) *</label>
                    <input
                      type="number"
                      value={planFormData.duration_weeks}
                      onChange={(e) => handlePlanFormChange('duration_weeks', e.target.value)}
                      placeholder="12"
                      style={styles.input}
                    />
                  </div>
                </div>

                <div style={styles.formGroup}>
                  <label style={styles.label}>Notas del Plan</label>
                  <textarea
                    value={planFormData.notes}
                    onChange={(e) => handlePlanFormChange('notes', e.target.value)}
                    placeholder="Instrucciones especiales, recordatorios, etc."
                    style={{...styles.input, minHeight: '80px'}}
                  />
                </div>
              </div>

              <div style={styles.buttonGroup}>
                <button onClick={handleSavePlan} style={styles.saveButton}>
                  💾 Asignar Plan
                </button>
                <button onClick={() => setShowPlanForm(false)} style={styles.cancelButton}>
                  ❌ Cancelar
                </button>
              </div>
            </div>
          ) : selectedPatient ? (
            <div style={styles.detailsContainer}>
              <div style={styles.detailsHeader}>
                <h2>{selectedPatient.name}</h2>
                <div style={styles.detailsActions}>
                  <button onClick={handleEdit} style={styles.editButton}>
                    ✏️ Editar
                  </button>
                  <button onClick={handleDelete} style={styles.deleteButton}>
                    🗑️ Eliminar
                  </button>
                </div>
              </div>

              {/* Patient Info Cards */}
              <div style={styles.cardsGrid}>
                <div style={styles.infoCard}>
                  <h3 style={styles.cardTitle}>📋 Información Personal</h3>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Email:</span>
                    <span>{selectedPatient.email}</span>
                  </div>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Teléfono:</span>
                    <span>{selectedPatient.phone}</span>
                  </div>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Edad:</span>
                    <span>{calculateAge(selectedPatient.birth_date)} años</span>
                  </div>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Género:</span>
                    <span>{selectedPatient.gender === 'M' ? 'Masculino' : selectedPatient.gender === 'F' ? 'Femenino' : 'Otro'}</span>
                  </div>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Registrado:</span>
                    <span>{selectedPatient.created_at}</span>
                  </div>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Última Visita:</span>
                    <span>{selectedPatient.last_visit}</span>
                  </div>
                </div>

                <div style={styles.infoCard}>
                  <h3 style={styles.cardTitle}>📊 Datos Antropométricos</h3>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Altura:</span>
                    <span>{selectedPatient.height_cm} cm</span>
                  </div>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Peso:</span>
                    <span>{selectedPatient.weight_kg} kg</span>
                  </div>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>IMC:</span>
                    <span style={{
                      fontWeight: 'bold',
                      color: getBMICategory(selectedPatient.bmi).color
                    }}>
                      {selectedPatient.bmi} ({getBMICategory(selectedPatient.bmi).text})
                    </span>
                  </div>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Actividad:</span>
                    <span>{getActivityLevelLabel(selectedPatient.activity_level)}</span>
                  </div>
                </div>

                <div style={styles.infoCard}>
                  <h3 style={styles.cardTitle}>🏥 Información Médica</h3>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Condiciones:</span>
                    <span>{selectedPatient.medical_conditions || 'Ninguna'}</span>
                  </div>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Alergias:</span>
                    <span>{selectedPatient.allergies || 'Ninguna'}</span>
                  </div>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Preferencias:</span>
                    <span>{selectedPatient.dietary_preferences || 'Sin restricciones'}</span>
                  </div>
                </div>
              </div>

              {/* Nutritional Plan Section */}
              <div style={styles.planSection}>
                <div style={styles.planHeader}>
                  <h3 style={styles.cardTitle}>🎯 Plan Nutricional</h3>
                  <button onClick={handleAssignPlan} style={styles.assignButton}>
                    ➕ {selectedPatient.nutritional_plan ? 'Actualizar Plan' : 'Asignar Plan'}
                  </button>
                </div>

                {selectedPatient.nutritional_plan ? (
                  <div style={styles.planDetails}>
                    <div style={styles.planGoal}>
                      <span style={styles.planLabel}>Objetivo:</span>
                      <span style={styles.goalBadge}>
                        {getGoalLabel(selectedPatient.nutritional_plan.goal)}
                      </span>
                    </div>

                    <div style={styles.macrosGrid}>
                      <div style={styles.macroCard}>
                        <div style={styles.macroValue}>{selectedPatient.nutritional_plan.target_calories}</div>
                        <div style={styles.macroLabel}>Calorías</div>
                      </div>
                      <div style={styles.macroCard}>
                        <div style={styles.macroValue}>{selectedPatient.nutritional_plan.target_protein_g}g</div>
                        <div style={styles.macroLabel}>Proteínas</div>
                      </div>
                      <div style={styles.macroCard}>
                        <div style={styles.macroValue}>{selectedPatient.nutritional_plan.target_carbs_g}g</div>
                        <div style={styles.macroLabel}>Carbohidratos</div>
                      </div>
                      <div style={styles.macroCard}>
                        <div style={styles.macroValue}>{selectedPatient.nutritional_plan.target_fat_g}g</div>
                        <div style={styles.macroLabel}>Grasas</div>
                      </div>
                    </div>

                    <div style={styles.planProgress}>
                      <div style={styles.progressHeader}>
                        <span>Progreso del Plan</span>
                        <span style={styles.progressPercent}>{selectedPatient.nutritional_plan.progress}%</span>
                      </div>
                      <div style={styles.progressBar}>
                        <div style={{
                          ...styles.progressFill,
                          width: `${selectedPatient.nutritional_plan.progress}%`
                        }} />
                      </div>
                      <div style={styles.planInfo}>
                        <span>Duración: {selectedPatient.nutritional_plan.duration_weeks} semanas</span>
                      </div>
                    </div>
                  </div>
                ) : (
                  <p style={styles.noPlan}>No hay plan nutricional asignado</p>
                )}
              </div>

              {/* Measurements History */}
              {selectedPatient.measurements && selectedPatient.measurements.length > 0 && (
                <div style={styles.measurementsSection}>
                  <h3 style={styles.cardTitle}>📈 Historial de Mediciones</h3>
                  <table style={styles.table}>
                    <thead>
                      <tr style={styles.tableHeader}>
                        <th style={styles.th}>Fecha</th>
                        <th style={styles.th}>Peso (kg)</th>
                        <th style={styles.th}>IMC</th>
                        <th style={styles.th}>Categoría</th>
                      </tr>
                    </thead>
                    <tbody>
                      {selectedPatient.measurements.map((measurement, index) => (
                        <tr key={index} style={styles.tableRow}>
                          <td style={styles.td}>{measurement.date}</td>
                          <td style={styles.td}>{measurement.weight_kg}</td>
                          <td style={styles.td}>{measurement.bmi}</td>
                          <td style={styles.td}>
                            <span style={{
                              ...styles.categoryBadge,
                              backgroundColor: getBMICategory(measurement.bmi).color
                            }}>
                              {getBMICategory(measurement.bmi).text}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          ) : (
            <div style={styles.emptyState}>
              <h2>Selecciona un paciente</h2>
              <p>Haz clic en un paciente de la lista o agrega uno nuevo</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '20px',
    backgroundColor: '#f8f9fa',
    minHeight: '100vh'
  },
  header: {
    marginBottom: '30px'
  },
  title: {
    fontSize: '2.5rem',
    color: '#2c3e50',
    marginBottom: '10px'
  },
  subtitle: {
    fontSize: '1.1rem',
    color: '#7f8c8d'
  },
  mainContent: {
    display: 'grid',
    gridTemplateColumns: '400px 1fr',
    gap: '20px',
    height: 'calc(100vh - 200px)'
  },
  leftPanel: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '20px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden'
  },
  rightPanel: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '30px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    overflowY: 'auto'
  },
  controlsBar: {
    marginBottom: '20px'
  },
  searchInput: {
    width: '100%',
    padding: '12px',
    border: '2px solid #e9ecef',
    borderRadius: '8px',
    fontSize: '14px',
    marginBottom: '10px'
  },
  addButton: {
    width: '100%',
    padding: '12px',
    backgroundColor: '#27ae60',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer'
  },
  patientsList: {
    flex: 1,
    overflowY: 'auto'
  },
  listTitle: {
    fontSize: '1.1rem',
    color: '#2c3e50',
    marginBottom: '15px'
  },
  patientCard: {
    padding: '15px',
    border: '2px solid #e9ecef',
    borderRadius: '8px',
    marginBottom: '10px',
    cursor: 'pointer',
    transition: 'all 0.2s ease'
  },
  selectedCard: {
    borderColor: '#3498db',
    backgroundColor: '#ebf5fb'
  },
  patientCardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '8px'
  },
  patientName: {
    fontSize: '1rem',
    color: '#2c3e50',
    margin: 0
  },
  badge: {
    padding: '4px 8px',
    borderRadius: '12px',
    fontSize: '0.75rem',
    color: 'white',
    fontWeight: '600'
  },
  patientInfo: {
    fontSize: '0.85rem',
    color: '#7f8c8d',
    margin: '4px 0'
  },
  planPreview: {
    marginTop: '10px',
    padding: '8px',
    backgroundColor: '#f8f9fa',
    borderRadius: '6px'
  },
  planBadge: {
    fontSize: '0.8rem',
    color: '#3498db',
    fontWeight: '600',
    display: 'block',
    marginBottom: '6px'
  },
  progressBar: {
    width: '100%',
    height: '6px',
    backgroundColor: '#e9ecef',
    borderRadius: '3px',
    overflow: 'hidden',
    marginBottom: '4px'
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#3498db',
    transition: 'width 0.3s ease'
  },
  progressText: {
    fontSize: '0.75rem',
    color: '#7f8c8d'
  },
  formContainer: {
    maxWidth: '900px'
  },
  formSection: {
    marginBottom: '25px',
    padding: '20px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px'
  },
  sectionTitle: {
    fontSize: '1.2rem',
    color: '#2c3e50',
    marginBottom: '15px'
  },
  formGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '15px'
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column'
  },
  label: {
    fontSize: '0.9rem',
    color: '#2c3e50',
    marginBottom: '6px',
    fontWeight: '500'
  },
  input: {
    padding: '10px',
    border: '2px solid #e9ecef',
    borderRadius: '6px',
    fontSize: '14px'
  },
  select: {
    padding: '10px',
    border: '2px solid #e9ecef',
    borderRadius: '6px',
    fontSize: '14px',
    backgroundColor: 'white'
  },
  buttonGroup: {
    display: 'flex',
    gap: '10px',
    marginTop: '20px'
  },
  saveButton: {
    padding: '12px 24px',
    backgroundColor: '#3498db',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer'
  },
  cancelButton: {
    padding: '12px 24px',
    backgroundColor: '#95a5a6',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer'
  },
  detailsContainer: {
    maxWidth: '1000px'
  },
  detailsHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '25px',
    paddingBottom: '15px',
    borderBottom: '2px solid #e9ecef'
  },
  detailsActions: {
    display: 'flex',
    gap: '10px'
  },
  editButton: {
    padding: '10px 20px',
    backgroundColor: '#f39c12',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer'
  },
  deleteButton: {
    padding: '10px 20px',
    backgroundColor: '#e74c3c',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer'
  },
  cardsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '20px',
    marginBottom: '25px'
  },
  infoCard: {
    padding: '20px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    border: '1px solid #e9ecef'
  },
  cardTitle: {
    fontSize: '1.1rem',
    color: '#2c3e50',
    marginBottom: '15px',
    fontWeight: '600'
  },
  infoRow: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '8px 0',
    borderBottom: '1px solid #e9ecef',
    fontSize: '0.9rem'
  },
  infoLabel: {
    color: '#7f8c8d',
    fontWeight: '500'
  },
  planSection: {
    marginBottom: '25px',
    padding: '20px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px'
  },
  planHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px'
  },
  assignButton: {
    padding: '10px 20px',
    backgroundColor: '#27ae60',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer'
  },
  planDetails: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px'
  },
  planGoal: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    marginBottom: '20px'
  },
  planLabel: {
    fontSize: '1rem',
    color: '#7f8c8d',
    fontWeight: '500'
  },
  goalBadge: {
    padding: '6px 12px',
    backgroundColor: '#3498db',
    color: 'white',
    borderRadius: '16px',
    fontSize: '0.9rem',
    fontWeight: '600'
  },
  macrosGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '15px',
    marginBottom: '20px'
  },
  macroCard: {
    textAlign: 'center',
    padding: '15px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px'
  },
  macroValue: {
    fontSize: '1.5rem',
    color: '#2c3e50',
    fontWeight: '700',
    marginBottom: '5px'
  },
  macroLabel: {
    fontSize: '0.85rem',
    color: '#7f8c8d'
  },
  planProgress: {
    marginTop: '20px'
  },
  progressHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '8px'
  },
  progressPercent: {
    fontWeight: '600',
    color: '#3498db'
  },
  planInfo: {
    fontSize: '0.9rem',
    color: '#7f8c8d',
    marginTop: '8px'
  },
  noPlan: {
    textAlign: 'center',
    color: '#7f8c8d',
    padding: '40px',
    fontSize: '1rem'
  },
  measurementsSection: {
    marginTop: '25px',
    padding: '20px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px'
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: '15px'
  },
  tableHeader: {
    backgroundColor: '#2c3e50',
    color: 'white'
  },
  th: {
    padding: '12px',
    textAlign: 'left',
    fontWeight: '600'
  },
  tableRow: {
    borderBottom: '1px solid #e9ecef'
  },
  td: {
    padding: '12px'
  },
  categoryBadge: {
    padding: '4px 12px',
    borderRadius: '12px',
    color: 'white',
    fontSize: '0.85rem',
    fontWeight: '600'
  },
  emptyState: {
    textAlign: 'center',
    padding: '60px 20px',
    color: '#7f8c8d'
  },
  formSubtitle: {
    color: '#7f8c8d',
    marginBottom: '20px'
  }
};

export default PatientsBrowser;
