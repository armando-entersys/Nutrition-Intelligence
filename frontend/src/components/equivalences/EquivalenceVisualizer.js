import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';

const EquivalenceVisualizer = ({ patientId = 1 }) => {
  const [groups, setGroups] = useState([]);
  const [patientGoals, setPatientGoals] = useState([]);
  const [dailyProgress, setDailyProgress] = useState({});
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [alternatives, setAlternatives] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadEquivalenceData();
  }, [patientId]);

  const loadEquivalenceData = async () => {
    try {
      setLoading(true);
      
      // Cargar grupos de equivalencias
      const groupsResponse = await axios.get(`${API_BASE_URL}/api/v1/equivalences/groups`);
      setGroups(groupsResponse.data);

      // Cargar metas del paciente
      const goalsResponse = await axios.get(`${API_BASE_URL}/api/v1/equivalences/patient/${patientId}/goals`);
      setPatientGoals(goalsResponse.data);
      
      // Cargar progreso de hoy (simulado)
      const today = new Date().toISOString().split('T')[0];
      setDailyProgress({
        cereales: 4.5,
        frutas: 2.0,
        verduras: 6.0,
        aoa_bajo_grasa: 2.0,
        leche_descremada: 2.5
      });
      
    } catch (error) {
      console.error('Error cargando datos de equivalencias:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadAlternatives = async (group) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/equivalences/groups/${group}/alternatives`);
      setAlternatives(response.data.alternatives || []);
      setSelectedGroup(response.data);
    } catch (error) {
      console.error('Error cargando alternativas:', error);
    }
  };

  const getProgressPercentage = (groupKey, consumed) => {
    const goal = patientGoals.find(g => g.equivalence_group === groupKey);
    if (!goal) return 0;
    return Math.min((consumed / goal.daily_target) * 100, 100);
  };

  const getProgressColor = (percentage) => {
    if (percentage < 60) return '#ff6b6b';
    if (percentage < 80) return '#ffd93d';
    if (percentage <= 120) return '#6bcf7f';
    return '#ff9500';
  };

  if (loading) {
    return (
      <div style={styles.loading}>
        <div style={styles.spinner}></div>
        <p>Cargando sistema de equivalencias...</p>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2>🔄 Sistema de Equivalencias SMAE</h2>
        <p>Aprende a intercambiar alimentos manteniendo el balance nutricional</p>
      </div>

      {/* Panel de progreso diario */}
      <div style={styles.progressPanel}>
        <h3>📊 Tu Progreso de Hoy</h3>
        <div style={styles.progressGrid}>
          {groups.map(group => {
            const consumed = dailyProgress[group.group] || 0;
            const goal = patientGoals.find(g => g.equivalence_group === group.group);
            const percentage = getProgressPercentage(group.group, consumed);
            
            if (!goal) return null;
            
            return (
              <div 
                key={group.group} 
                style={{
                  ...styles.progressCard,
                  borderColor: group.color,
                  backgroundColor: `${group.color}10`
                }}
                onClick={() => loadAlternatives(group.group)}
              >
                <div style={styles.progressHeader}>
                  <span style={{...styles.groupName, color: group.color}}>
                    {group.name}
                  </span>
                  <span style={styles.progressText}>
                    {consumed.toFixed(1)} / {goal.daily_target} equiv.
                  </span>
                </div>
                
                <div style={styles.progressBar}>
                  <div 
                    style={{
                      ...styles.progressFill,
                      width: `${Math.min(percentage, 100)}%`,
                      backgroundColor: getProgressColor(percentage)
                    }}
                  ></div>
                </div>
                
                <div style={styles.progressInfo}>
                  <small style={styles.calories}>
                    {Math.round(consumed * group.standard_calories)} kcal
                  </small>
                  <small style={styles.percentage}>
                    {Math.round(percentage)}%
                  </small>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Panel de alternativas */}
      {selectedGroup && (
        <div style={styles.alternativesPanel}>
          <div style={styles.alternativesHeader}>
            <h3 style={{ color: selectedGroup.group_info.color }}>
              🔄 Intercambios para {selectedGroup.group_info.name}
            </h3>
            <p>{selectedGroup.group_info.description}</p>
            <div style={styles.groupStandards}>
              <span>1 equivalente = {selectedGroup.group_info.calories} kcal</span>
              <span>Proteína: {selectedGroup.group_info.protein}g</span>
              <span>Carbohidratos: {selectedGroup.group_info.carbs}g</span>
              <span>Grasas: {selectedGroup.group_info.fat}g</span>
            </div>
          </div>
          
          <div style={styles.alternativesGrid}>
            {alternatives.map((alt, index) => (
              <div key={index} style={styles.alternativeCard}>
                <div style={styles.alternativeHeader}>
                  <strong>{alt.food_name}</strong>
                  <span style={styles.portion}>
                    {alt.standard_portion} {alt.standard_unit}
                  </span>
                </div>
                
                <div style={styles.alternativeNutrition}>
                  <div style={styles.nutritionItem}>
                    <span className="icon">🔥</span>
                    <span>{Math.round(alt.calories_per_equivalent)} kcal</span>
                  </div>
                  <div style={styles.nutritionItem}>
                    <span className="icon">🥩</span>
                    <span>{alt.protein_per_equivalent.toFixed(1)}g</span>
                  </div>
                  <div style={styles.nutritionItem}>
                    <span className="icon">🍞</span>
                    <span>{alt.carbs_per_equivalent.toFixed(1)}g</span>
                  </div>
                  <div style={styles.nutritionItem}>
                    <span className="icon">🥑</span>
                    <span>{alt.fat_per_equivalent.toFixed(1)}g</span>
                  </div>
                </div>
                
                {alt.notes && (
                  <div style={styles.alternativeNotes}>
                    <small>💡 {alt.notes}</small>
                  </div>
                )}
                
                <button 
                  style={{
                    ...styles.addButton,
                    backgroundColor: selectedGroup.group_info.color
                  }}
                  onClick={() => addToMeal(alt)}
                >
                  + Agregar a mi comida
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Panel de información educativa */}
      <div style={styles.educationPanel}>
        <h3>📚 ¿Cómo funcionan las equivalencias?</h3>
        <div style={styles.educationGrid}>
          <div style={styles.educationCard}>
            <h4>🎯 Concepto</h4>
            <p>
              Los alimentos del mismo grupo aportan nutrientes similares. 
              Puedes intercambiarlos manteniendo el balance nutricional.
            </p>
          </div>
          
          <div style={styles.educationCard}>
            <h4>⚖️ Porciones</h4>
            <p>
              Cada equivalente aporta la misma cantidad de calorías y nutrientes principales.
              Aprende las porciones estándar.
            </p>
          </div>
          
          <div style={styles.educationCard}>
            <h4>🎨 Variedad</h4>
            <p>
              Usa diferentes alimentos del mismo grupo para obtener diversos 
              micronutrientes y sabores.
            </p>
          </div>
          
          <div style={styles.educationCard}>
            <h4>📈 Flexibilidad</h4>
            <p>
              Puedes distribuir tus equivalentes a lo largo del día según 
              tus preferencias y horarios.
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  function addToMeal(alternative) {
    // Lógica para agregar alimento a la comida actual
    console.log('Agregando a la comida:', alternative);
    alert(`Agregado: ${alternative.food_name} (${alternative.standard_portion} ${alternative.standard_unit})`);
  }
};

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
  },
  loading: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '300px',
    gap: '20px',
  },
  spinner: {
    width: '40px',
    height: '40px',
    border: '4px solid #f3f3f3',
    borderTop: '4px solid #3498db',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  header: {
    textAlign: 'center',
    marginBottom: '30px',
  },
  progressPanel: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '20px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    marginBottom: '20px',
  },
  progressGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '15px',
    marginTop: '15px',
  },
  progressCard: {
    padding: '15px',
    borderRadius: '8px',
    border: '2px solid',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  progressHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '10px',
  },
  groupName: {
    fontWeight: 'bold',
    fontSize: '14px',
  },
  progressText: {
    fontSize: '12px',
    color: '#666',
  },
  progressBar: {
    width: '100%',
    height: '8px',
    backgroundColor: '#e0e0e0',
    borderRadius: '4px',
    overflow: 'hidden',
    marginBottom: '8px',
  },
  progressFill: {
    height: '100%',
    borderRadius: '4px',
    transition: 'width 0.3s ease',
  },
  progressInfo: {
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '12px',
  },
  calories: {
    color: '#666',
  },
  percentage: {
    fontWeight: 'bold',
  },
  alternativesPanel: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '20px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    marginBottom: '20px',
  },
  alternativesHeader: {
    marginBottom: '20px',
  },
  groupStandards: {
    display: 'flex',
    gap: '15px',
    fontSize: '12px',
    color: '#666',
    marginTop: '10px',
  },
  alternativesGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '15px',
  },
  alternativeCard: {
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '15px',
    backgroundColor: '#fafafa',
  },
  alternativeHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '10px',
  },
  portion: {
    backgroundColor: '#e3f2fd',
    padding: '2px 8px',
    borderRadius: '12px',
    fontSize: '12px',
    color: '#1976d2',
  },
  alternativeNutrition: {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)',
    gap: '8px',
    marginBottom: '10px',
  },
  nutritionItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '5px',
    fontSize: '12px',
  },
  alternativeNotes: {
    marginBottom: '10px',
    padding: '8px',
    backgroundColor: '#fff3cd',
    borderRadius: '4px',
  },
  addButton: {
    width: '100%',
    padding: '8px',
    border: 'none',
    borderRadius: '4px',
    color: 'white',
    fontWeight: 'bold',
    cursor: 'pointer',
    fontSize: '14px',
  },
  educationPanel: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '20px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
  },
  educationGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '15px',
    marginTop: '15px',
  },
  educationCard: {
    padding: '15px',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
    backgroundColor: '#f9f9f9',
  }
};

export default EquivalenceVisualizer;