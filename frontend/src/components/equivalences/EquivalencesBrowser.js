import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';

const EquivalencesBrowser = () => {
  const [groups, setGroups] = useState([]);
  const [foods, setFoods] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [showAddGroupForm, setShowAddGroupForm] = useState(false);
  const [showAddEquivalenceForm, setShowAddEquivalenceForm] = useState(false);
  const [calculator, setCalculator] = useState({
    fromFood: null,
    toFood: null,
    amount: 100,
    result: null
  });

  const [groupFormData, setGroupFormData] = useState({
    name: '',
    description: '',
    equivalences: []
  });

  const [equivalenceFormData, setEquivalenceFormData] = useState({
    food_id: '',
    portion_size_grams: '',
    calories: ''
  });

  useEffect(() => {
    fetchGroups();
    fetchFoods();
  }, []);

  const fetchGroups = async () => {
    setLoading(true);
    try {
      // Mock equivalence groups data
      const mockGroups = [
        {
          id: 1,
          name: 'Frutas Frescas',
          description: 'Equivalencias de frutas comunes basadas en contenido calórico similar',
          equivalences: [
            { id: 1, food_name: 'Manzana', portion_size_grams: 130, calories: 68 },
            { id: 2, food_name: 'Plátano', portion_size_grams: 80, calories: 71 },
            { id: 3, food_name: 'Naranja', portion_size_grams: 150, calories: 71 },
            { id: 4, food_name: 'Uvas', portion_size_grams: 100, calories: 69 },
          ],
          created_at: '2024-01-15'
        },
        {
          id: 2,
          name: 'Vegetales de Hoja Verde',
          description: 'Vegetales bajos en calorías con alto contenido de fibra',
          equivalences: [
            { id: 5, food_name: 'Espinaca', portion_size_grams: 100, calories: 23 },
            { id: 6, food_name: 'Lechuga', portion_size_grams: 100, calories: 15 },
            { id: 7, food_name: 'Brócoli', portion_size_grams: 100, calories: 34 },
          ],
          created_at: '2024-01-16'
        },
        {
          id: 3,
          name: 'Proteínas Magras',
          description: 'Fuentes de proteína baja en grasa',
          equivalences: [
            { id: 8, food_name: 'Pechuga de Pollo', portion_size_grams: 100, calories: 165 },
            { id: 9, food_name: 'Atún enlatado', portion_size_grams: 100, calories: 132 },
            { id: 10, food_name: 'Pescado (Salmón)', portion_size_grams: 80, calories: 166 },
          ],
          created_at: '2024-01-17'
        },
        {
          id: 4,
          name: 'Granos Integrales',
          description: 'Cereales y granos con alto contenido de fibra',
          equivalences: [
            { id: 11, food_name: 'Arroz Integral', portion_size_grams: 150, calories: 167 },
            { id: 12, food_name: 'Pan Integral', portion_size_grams: 60, calories: 148 },
            { id: 13, food_name: 'Avena', portion_size_grams: 40, calories: 156 },
          ],
          created_at: '2024-01-18'
        },
        {
          id: 5,
          name: 'Lácteos',
          description: 'Productos lácteos con contenido calórico similar',
          equivalences: [
            { id: 14, food_name: 'Leche Descremada', portion_size_grams: 240, calories: 82 },
            { id: 15, food_name: 'Yogurt Natural', portion_size_grams: 150, calories: 89 },
            { id: 16, food_name: 'Queso Fresco', portion_size_grams: 80, calories: 78 },
          ],
          created_at: '2024-01-19'
        }
      ];
      setGroups(mockGroups);
    } catch (err) {
      console.error('Error fetching groups:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchFoods = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/foods`);
      setFoods(response.data);
    } catch (err) {
      console.error('Error fetching foods:', err);
    }
  };

  const handleGroupClick = (group) => {
    setSelectedGroup(group);
    setShowAddGroupForm(false);
    setShowAddEquivalenceForm(false);
  };

  const handleAddGroup = () => {
    setSelectedGroup(null);
    setShowAddGroupForm(true);
    setShowAddEquivalenceForm(false);
    setGroupFormData({ name: '', description: '', equivalences: [] });
  };

  const handleAddEquivalence = () => {
    if (selectedGroup) {
      setShowAddEquivalenceForm(true);
      setShowAddGroupForm(false);
    }
  };

  const handleSaveGroup = () => {
    const newGroup = {
      id: groups.length + 1,
      ...groupFormData,
      created_at: new Date().toISOString().split('T')[0]
    };
    setGroups([...groups, newGroup]);
    setSelectedGroup(newGroup);
    setShowAddGroupForm(false);
    alert('✅ Grupo de equivalencias creado exitosamente!');
  };

  const handleSaveEquivalence = () => {
    if (!selectedGroup || !equivalenceFormData.food_id) return;

    const food = foods.find(f => f.id === parseInt(equivalenceFormData.food_id));
    if (!food) return;

    const newEquivalence = {
      id: selectedGroup.equivalences.length + 1,
      food_name: food.name,
      portion_size_grams: parseFloat(equivalenceFormData.portion_size_grams),
      calories: parseFloat(equivalenceFormData.calories)
    };

    const updatedGroup = {
      ...selectedGroup,
      equivalences: [...selectedGroup.equivalences, newEquivalence]
    };

    setGroups(groups.map(g => g.id === selectedGroup.id ? updatedGroup : g));
    setSelectedGroup(updatedGroup);
    setShowAddEquivalenceForm(false);
    setEquivalenceFormData({ food_id: '', portion_size_grams: '', calories: '' });
    alert('✅ Equivalencia agregada exitosamente!');
  };

  const handleDeleteGroup = () => {
    if (window.confirm(`¿Eliminar el grupo "${selectedGroup.name}"?`)) {
      setGroups(groups.filter(g => g.id !== selectedGroup.id));
      setSelectedGroup(null);
      alert('✅ Grupo eliminado exitosamente!');
    }
  };

  const handleDeleteEquivalence = (equivId) => {
    const updatedGroup = {
      ...selectedGroup,
      equivalences: selectedGroup.equivalences.filter(e => e.id !== equivId)
    };
    setGroups(groups.map(g => g.id === selectedGroup.id ? updatedGroup : g));
    setSelectedGroup(updatedGroup);
  };

  const calculateEquivalence = () => {
    if (!calculator.fromFood || !calculator.toFood || !calculator.amount) return;

    const fromEquiv = selectedGroup.equivalences.find(e => e.id === calculator.fromFood);
    const toEquiv = selectedGroup.equivalences.find(e => e.id === calculator.toFood);

    if (fromEquiv && toEquiv) {
      // Calculate based on calories
      const fromCaloriesPerGram = fromEquiv.calories / fromEquiv.portion_size_grams;
      const toCaloriesPerGram = toEquiv.calories / toEquiv.portion_size_grams;
      const equivalentAmount = (calculator.amount * fromCaloriesPerGram) / toCaloriesPerGram;

      setCalculator(prev => ({
        ...prev,
        result: {
          amount: Math.round(equivalentAmount),
          fromFood: fromEquiv.food_name,
          toFood: toEquiv.food_name,
          fromCalories: Math.round(calculator.amount * fromCaloriesPerGram),
          toCalories: Math.round(equivalentAmount * toCaloriesPerGram)
        }
      }));
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>⚖️ Sistema de Equivalencias Nutricionales</h1>
        <p style={styles.subtitle}>
          Gestiona grupos de equivalencias y calcula sustituciones de alimentos
        </p>
      </div>

      <div style={styles.mainLayout}>
        {/* Groups Sidebar */}
        <div style={styles.groupsSidebar}>
          <div style={styles.sidebarHeader}>
            <h3>Grupos de Equivalencias</h3>
            <button onClick={handleAddGroup} style={styles.addButton}>
              ➕ Nuevo Grupo
            </button>
          </div>

          {loading && <div style={styles.loading}>Cargando...</div>}

          {groups.map(group => (
            <div
              key={group.id}
              style={{
                ...styles.groupCard,
                ...(selectedGroup?.id === group.id ? styles.selectedGroupCard : {})
              }}
              onClick={() => handleGroupClick(group)}
            >
              <h4 style={styles.groupCardTitle}>{group.name}</h4>
              <p style={styles.groupCardDescription}>{group.description}</p>
              <div style={styles.groupCardFooter}>
                <span>{group.equivalences.length} equivalencias</span>
              </div>
            </div>
          ))}
        </div>

        {/* Main Content */}
        <div style={styles.mainContent}>
          {!selectedGroup && !showAddGroupForm && (
            <div style={styles.emptyState}>
              <h3>Selecciona un grupo de equivalencias</h3>
              <p>Haz clic en un grupo de la izquierda o crea uno nuevo</p>
            </div>
          )}

          {showAddGroupForm && (
            <div style={styles.formContainer}>
              <h2>➕ Crear Nuevo Grupo de Equivalencias</h2>

              <div style={styles.formGroup}>
                <label style={styles.label}>Nombre del Grupo</label>
                <input
                  type="text"
                  style={styles.input}
                  placeholder="Ej: Frutas Frescas"
                  value={groupFormData.name}
                  onChange={(e) => setGroupFormData({...groupFormData, name: e.target.value})}
                />
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Descripción</label>
                <textarea
                  style={{...styles.input, minHeight: '80px'}}
                  placeholder="Describe el grupo de equivalencias"
                  value={groupFormData.description}
                  onChange={(e) => setGroupFormData({...groupFormData, description: e.target.value})}
                />
              </div>

              <div style={styles.formActions}>
                <button style={styles.saveButton} onClick={handleSaveGroup}>
                  💾 Crear Grupo
                </button>
                <button
                  style={styles.cancelButton}
                  onClick={() => setShowAddGroupForm(false)}
                >
                  ❌ Cancelar
                </button>
              </div>
            </div>
          )}

          {selectedGroup && !showAddEquivalenceForm && (
            <div>
              <div style={styles.groupHeader}>
                <div>
                  <h2>{selectedGroup.name}</h2>
                  <p style={styles.groupDescription}>{selectedGroup.description}</p>
                </div>
                <button style={styles.deleteButton} onClick={handleDeleteGroup}>
                  🗑️ Eliminar Grupo
                </button>
              </div>

              {/* Equivalences Table */}
              <div style={styles.section}>
                <div style={styles.sectionHeader}>
                  <h3>Equivalencias en este Grupo</h3>
                  <button style={styles.addEquivButton} onClick={handleAddEquivalence}>
                    ➕ Agregar Equivalencia
                  </button>
                </div>

                <table style={styles.table}>
                  <thead>
                    <tr>
                      <th style={styles.th}>Alimento</th>
                      <th style={styles.th}>Porción (g)</th>
                      <th style={styles.th}>Calorías</th>
                      <th style={styles.th}>Cal/100g</th>
                      <th style={styles.th}>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedGroup.equivalences.map(equiv => (
                      <tr key={equiv.id} style={styles.tr}>
                        <td style={styles.td}>{equiv.food_name}</td>
                        <td style={styles.td}>{equiv.portion_size_grams}g</td>
                        <td style={styles.td}>{equiv.calories} kcal</td>
                        <td style={styles.td}>
                          {Math.round((equiv.calories / equiv.portion_size_grams) * 100)}
                        </td>
                        <td style={styles.td}>
                          <button
                            style={styles.deleteIconButton}
                            onClick={() => handleDeleteEquivalence(equiv.id)}
                          >
                            ✕
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                {selectedGroup.equivalences.length === 0 && (
                  <div style={styles.emptyTable}>
                    No hay equivalencias en este grupo
                  </div>
                )}
              </div>

              {/* Calculator */}
              {selectedGroup.equivalences.length >= 2 && (
                <div style={styles.section}>
                  <h3>🧮 Calculadora de Equivalencias</h3>
                  <p style={styles.calculatorDescription}>
                    Calcula cuánto de un alimento equivale a otro basado en calorías
                  </p>

                  <div style={styles.calculatorGrid}>
                    <div style={styles.formGroup}>
                      <label style={styles.label}>De:</label>
                      <select
                        style={styles.input}
                        value={calculator.fromFood || ''}
                        onChange={(e) => setCalculator({...calculator, fromFood: parseInt(e.target.value)})}
                      >
                        <option value="">Seleccionar alimento...</option>
                        {selectedGroup.equivalences.map(equiv => (
                          <option key={equiv.id} value={equiv.id}>
                            {equiv.food_name}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div style={styles.formGroup}>
                      <label style={styles.label}>Cantidad (g):</label>
                      <input
                        type="number"
                        style={styles.input}
                        value={calculator.amount}
                        onChange={(e) => setCalculator({...calculator, amount: parseFloat(e.target.value)})}
                      />
                    </div>

                    <div style={styles.formGroup}>
                      <label style={styles.label}>A:</label>
                      <select
                        style={styles.input}
                        value={calculator.toFood || ''}
                        onChange={(e) => setCalculator({...calculator, toFood: parseInt(e.target.value)})}
                      >
                        <option value="">Seleccionar alimento...</option>
                        {selectedGroup.equivalences.map(equiv => (
                          <option key={equiv.id} value={equiv.id}>
                            {equiv.food_name}
                          </option>
                        ))}
                      </select>
                    </div>

                    <button
                      style={styles.calculateButton}
                      onClick={calculateEquivalence}
                    >
                      = Calcular
                    </button>
                  </div>

                  {calculator.result && (
                    <div style={styles.calculatorResult}>
                      <h4>Resultado:</h4>
                      <p style={styles.resultText}>
                        <strong>{calculator.amount}g</strong> de <strong>{calculator.result.fromFood}</strong>
                        {' '}({calculator.result.fromCalories} kcal)
                        {' '}≈{' '}
                        <strong>{calculator.result.amount}g</strong> de <strong>{calculator.result.toFood}</strong>
                        {' '}({calculator.result.toCalories} kcal)
                      </p>
                    </div>
                  )}
                </div>
              )}

              {/* Visual Comparison */}
              {selectedGroup.equivalences.length > 0 && (
                <div style={styles.section}>
                  <h3>📊 Comparación Visual</h3>
                  <div style={styles.comparisonGrid}>
                    {selectedGroup.equivalences.map(equiv => (
                      <div key={equiv.id} style={styles.comparisonCard}>
                        <div style={styles.comparisonHeader}>
                          <h4>{equiv.food_name}</h4>
                        </div>
                        <div style={styles.comparisonBody}>
                          <div style={styles.comparisonValue}>
                            {equiv.portion_size_grams}g
                          </div>
                          <div style={styles.comparisonLabel}>Porción</div>
                          <div style={styles.comparisonCalories}>
                            {equiv.calories} kcal
                          </div>
                          <div
                            style={{
                              ...styles.comparisonBar,
                              width: `${(equiv.calories / 200) * 100}%`
                            }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {showAddEquivalenceForm && (
            <div style={styles.formContainer}>
              <h2>➕ Agregar Equivalencia a "{selectedGroup.name}"</h2>

              <div style={styles.formGroup}>
                <label style={styles.label}>Alimento</label>
                <select
                  style={styles.input}
                  value={equivalenceFormData.food_id}
                  onChange={(e) => setEquivalenceFormData({...equivalenceFormData, food_id: e.target.value})}
                >
                  <option value="">Seleccionar alimento...</option>
                  {foods.map(food => (
                    <option key={food.id} value={food.id}>
                      {food.name}
                    </option>
                  ))}
                </select>
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Tamaño de Porción (gramos)</label>
                <input
                  type="number"
                  style={styles.input}
                  placeholder="100"
                  value={equivalenceFormData.portion_size_grams}
                  onChange={(e) => setEquivalenceFormData({...equivalenceFormData, portion_size_grams: e.target.value})}
                />
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Calorías de la Porción</label>
                <input
                  type="number"
                  style={styles.input}
                  placeholder="70"
                  value={equivalenceFormData.calories}
                  onChange={(e) => setEquivalenceFormData({...equivalenceFormData, calories: e.target.value})}
                />
              </div>

              <div style={styles.formActions}>
                <button style={styles.saveButton} onClick={handleSaveEquivalence}>
                  💾 Agregar Equivalencia
                </button>
                <button
                  style={styles.cancelButton}
                  onClick={() => setShowAddEquivalenceForm(false)}
                >
                  ❌ Cancelar
                </button>
              </div>
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
    maxWidth: '1400px',
    margin: '0 auto',
  },
  header: {
    marginBottom: '30px',
  },
  title: {
    fontSize: '32px',
    color: '#2c3e50',
    marginBottom: '10px',
  },
  subtitle: {
    fontSize: '16px',
    color: '#7f8c8d',
  },
  mainLayout: {
    display: 'grid',
    gridTemplateColumns: '350px 1fr',
    gap: '20px',
  },
  groupsSidebar: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '20px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    height: 'calc(100vh - 250px)',
    overflowY: 'auto',
  },
  sidebarHeader: {
    marginBottom: '20px',
  },
  addButton: {
    width: '100%',
    padding: '12px',
    backgroundColor: '#27ae60',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '500',
    cursor: 'pointer',
    marginTop: '10px',
  },
  groupCard: {
    padding: '15px',
    marginBottom: '10px',
    border: '2px solid #f0f0f0',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  selectedGroupCard: {
    borderColor: '#3498db',
    backgroundColor: '#f0f8ff',
  },
  groupCardTitle: {
    margin: '0 0 8px 0',
    fontSize: '16px',
    color: '#2c3e50',
  },
  groupCardDescription: {
    margin: '0 0 10px 0',
    fontSize: '13px',
    color: '#7f8c8d',
  },
  groupCardFooter: {
    fontSize: '12px',
    color: '#95a5a6',
  },
  mainContent: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '30px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    height: 'calc(100vh - 250px)',
    overflowY: 'auto',
  },
  emptyState: {
    textAlign: 'center',
    padding: '60px 20px',
    color: '#95a5a6',
  },
  groupHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '30px',
    paddingBottom: '20px',
    borderBottom: '2px solid #f0f0f0',
  },
  groupDescription: {
    fontSize: '15px',
    color: '#7f8c8d',
    margin: '8px 0 0 0',
  },
  deleteButton: {
    padding: '10px 20px',
    backgroundColor: '#e74c3c',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    cursor: 'pointer',
  },
  section: {
    marginBottom: '30px',
  },
  sectionHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '15px',
  },
  addEquivButton: {
    padding: '8px 16px',
    backgroundColor: '#3498db',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '13px',
    cursor: 'pointer',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
  },
  th: {
    padding: '12px',
    backgroundColor: '#f8f9fa',
    textAlign: 'left',
    borderBottom: '2px solid #e9ecef',
    fontSize: '14px',
    fontWeight: '600',
    color: '#2c3e50',
  },
  tr: {
    borderBottom: '1px solid #f0f0f0',
  },
  td: {
    padding: '12px',
    fontSize: '14px',
    color: '#2c3e50',
  },
  emptyTable: {
    textAlign: 'center',
    padding: '40px',
    color: '#95a5a6',
    fontSize: '14px',
  },
  deleteIconButton: {
    background: 'none',
    border: 'none',
    color: '#e74c3c',
    fontSize: '18px',
    cursor: 'pointer',
  },
  calculatorDescription: {
    fontSize: '14px',
    color: '#7f8c8d',
    marginBottom: '20px',
  },
  calculatorGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 150px 1fr 120px',
    gap: '15px',
    alignItems: 'end',
  },
  calculateButton: {
    padding: '12px',
    backgroundColor: '#9b59b6',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    height: '44px',
  },
  calculatorResult: {
    marginTop: '20px',
    padding: '20px',
    backgroundColor: '#e8f5e9',
    borderRadius: '8px',
    border: '2px solid #27ae60',
  },
  resultText: {
    fontSize: '16px',
    color: '#2c3e50',
    margin: '10px 0 0 0',
    lineHeight: '1.6',
  },
  comparisonGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
    gap: '15px',
  },
  comparisonCard: {
    border: '2px solid #e9ecef',
    borderRadius: '8px',
    overflow: 'hidden',
  },
  comparisonHeader: {
    padding: '12px',
    backgroundColor: '#f8f9fa',
    borderBottom: '2px solid #e9ecef',
  },
  comparisonBody: {
    padding: '15px',
    textAlign: 'center',
  },
  comparisonValue: {
    fontSize: '24px',
    fontWeight: '600',
    color: '#3498db',
  },
  comparisonLabel: {
    fontSize: '12px',
    color: '#7f8c8d',
    marginBottom: '10px',
  },
  comparisonCalories: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#e74c3c',
    marginBottom: '10px',
  },
  comparisonBar: {
    height: '8px',
    backgroundColor: '#3498db',
    borderRadius: '4px',
    transition: 'width 0.3s ease',
  },
  formContainer: {
    maxWidth: '600px',
  },
  formGroup: {
    marginBottom: '20px',
  },
  label: {
    display: 'block',
    fontSize: '14px',
    fontWeight: '500',
    color: '#2c3e50',
    marginBottom: '8px',
  },
  input: {
    width: '100%',
    padding: '10px',
    fontSize: '14px',
    border: '2px solid #e9ecef',
    borderRadius: '6px',
    outline: 'none',
  },
  formActions: {
    display: 'flex',
    gap: '10px',
    marginTop: '30px',
  },
  saveButton: {
    flex: 1,
    padding: '14px',
    backgroundColor: '#27ae60',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
  },
  cancelButton: {
    flex: 1,
    padding: '14px',
    backgroundColor: '#95a5a6',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
  },
  loading: {
    textAlign: 'center',
    padding: '20px',
    color: '#7f8c8d',
  },
};

export default EquivalencesBrowser;