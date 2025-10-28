import React, { useState } from 'react';

const NutritionCalculator = () => {
  const [activeCalculator, setActiveCalculator] = useState('bmi');

  // BMI Calculator State
  const [bmiData, setBmiData] = useState({
    weight: '',
    height: '',
    result: null
  });

  // Calorie Calculator State
  const [calorieData, setCalorieData] = useState({
    weight: '',
    height: '',
    age: '',
    gender: 'male',
    activityLevel: 'sedentary',
    goal: 'maintain',
    result: null
  });

  // Macro Calculator State
  const [macroData, setMacroData] = useState({
    calories: '',
    goal: 'balanced',
    result: null
  });

  // Portion Calculator State
  const [portionData, setPortionData] = useState({
    foodType: 'protein',
    servings: '',
    result: null
  });

  // BMI Calculator Functions
  const calculateBMI = () => {
    const weight = parseFloat(bmiData.weight);
    const height = parseFloat(bmiData.height) / 100; // Convert cm to m

    if (weight && height) {
      const bmi = (weight / (height * height)).toFixed(1);
      let category = '';
      let color = '';
      let recommendation = '';

      if (bmi < 18.5) {
        category = 'Bajo Peso';
        color = '#3498db';
        recommendation = 'Se recomienda aumentar el consumo calórico y consultar con un nutricionista.';
      } else if (bmi < 25) {
        category = 'Peso Normal';
        color = '#27ae60';
        recommendation = 'Mantén tu peso actual con una dieta balanceada y ejercicio regular.';
      } else if (bmi < 30) {
        category = 'Sobrepeso';
        color = '#f39c12';
        recommendation = 'Se recomienda reducir calorías y aumentar actividad física.';
      } else {
        category = 'Obesidad';
        color = '#e74c3c';
        recommendation = 'Consulta con un profesional de la salud para un plan personalizado.';
      }

      setBmiData({
        ...bmiData,
        result: { bmi, category, color, recommendation }
      });
    }
  };

  // Calorie Calculator Functions (Harris-Benedict Equation)
  const calculateCalories = () => {
    const weight = parseFloat(calorieData.weight);
    const height = parseFloat(calorieData.height);
    const age = parseFloat(calorieData.age);

    if (weight && height && age) {
      let bmr;

      // Calculate BMR using Mifflin-St Jeor Equation
      if (calorieData.gender === 'male') {
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5;
      } else {
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161;
      }

      // Activity multipliers
      const activityMultipliers = {
        sedentary: 1.2,
        light: 1.375,
        moderate: 1.55,
        active: 1.725,
        very_active: 1.9
      };

      const tdee = Math.round(bmr * activityMultipliers[calorieData.activityLevel]);

      // Goal adjustments
      let targetCalories;
      let description;

      if (calorieData.goal === 'lose') {
        targetCalories = Math.round(tdee - 500);
        description = 'Déficit de 500 kcal para pérdida de peso saludable (~0.5 kg/semana)';
      } else if (calorieData.goal === 'gain') {
        targetCalories = Math.round(tdee + 500);
        description = 'Superávit de 500 kcal para ganancia de peso saludable (~0.5 kg/semana)';
      } else {
        targetCalories = tdee;
        description = 'Calorías de mantenimiento para peso actual';
      }

      setCalorieData({
        ...calorieData,
        result: { bmr: Math.round(bmr), tdee, targetCalories, description }
      });
    }
  };

  // Macro Calculator Functions
  const calculateMacros = () => {
    const calories = parseFloat(macroData.calories);

    if (calories) {
      let proteinPercent, carbsPercent, fatPercent;
      let description;

      // Different macro ratios based on goal
      if (macroData.goal === 'balanced') {
        proteinPercent = 30;
        carbsPercent = 40;
        fatPercent = 30;
        description = 'Distribución balanceada para mantenimiento general';
      } else if (macroData.goal === 'low_carb') {
        proteinPercent = 35;
        carbsPercent = 25;
        fatPercent = 40;
        description = 'Baja en carbohidratos, ideal para control de glucosa';
      } else if (macroData.goal === 'high_protein') {
        proteinPercent = 40;
        carbsPercent = 30;
        fatPercent = 30;
        description = 'Alta en proteína, ideal para ganancia muscular';
      } else if (macroData.goal === 'low_fat') {
        proteinPercent = 25;
        carbsPercent = 55;
        fatPercent = 20;
        description = 'Baja en grasa, alta en carbohidratos';
      }

      const proteinCalories = calories * (proteinPercent / 100);
      const carbsCalories = calories * (carbsPercent / 100);
      const fatCalories = calories * (fatPercent / 100);

      const proteinGrams = Math.round(proteinCalories / 4);
      const carbsGrams = Math.round(carbsCalories / 4);
      const fatGrams = Math.round(fatCalories / 9);

      setMacroData({
        ...macroData,
        result: {
          protein: { grams: proteinGrams, percent: proteinPercent },
          carbs: { grams: carbsGrams, percent: carbsPercent },
          fat: { grams: fatGrams, percent: fatPercent },
          description
        }
      });
    }
  };

  // Portion Calculator Functions
  const calculatePortions = () => {
    const servings = parseFloat(portionData.servings);

    if (servings) {
      const portionSizes = {
        protein: {
          name: 'Proteína',
          standard: 100,
          unit: 'gramos',
          examples: ['Pechuga de pollo', 'Pescado', 'Carne magra', 'Tofu']
        },
        vegetables: {
          name: 'Vegetales',
          standard: 150,
          unit: 'gramos',
          examples: ['Brócoli', 'Espinacas', 'Zanahorias', 'Pimientos']
        },
        grains: {
          name: 'Granos/Cereales',
          standard: 60,
          unit: 'gramos (cocidos)',
          examples: ['Arroz', 'Pasta', 'Quinoa', 'Avena']
        },
        fruits: {
          name: 'Frutas',
          standard: 120,
          unit: 'gramos',
          examples: ['Manzana mediana', 'Plátano', 'Naranja', '1 taza de fresas']
        },
        dairy: {
          name: 'Lácteos',
          standard: 250,
          unit: 'ml',
          examples: ['Leche', 'Yogur', 'Kéfir']
        },
        fats: {
          name: 'Grasas Saludables',
          standard: 15,
          unit: 'gramos',
          examples: ['Aceite de oliva (1 cucharada)', 'Aguacate (1/4)', 'Frutos secos (pequeño puñado)']
        }
      };

      const foodInfo = portionSizes[portionData.foodType];
      const totalAmount = Math.round(foodInfo.standard * servings);

      setPortionData({
        ...portionData,
        result: {
          ...foodInfo,
          servings,
          totalAmount
        }
      });
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>🧮 Calculadora Nutricional</h1>
        <p style={styles.subtitle}>Herramientas para cálculos nutricionales y dietéticos</p>
      </div>

      {/* Calculator Selection Tabs */}
      <div style={styles.tabsContainer}>
        <button
          onClick={() => setActiveCalculator('bmi')}
          style={{
            ...styles.tab,
            ...(activeCalculator === 'bmi' ? styles.activeTab : {})
          }}
        >
          📊 IMC
        </button>
        <button
          onClick={() => setActiveCalculator('calories')}
          style={{
            ...styles.tab,
            ...(activeCalculator === 'calories' ? styles.activeTab : {})
          }}
        >
          🔥 Calorías
        </button>
        <button
          onClick={() => setActiveCalculator('macros')}
          style={{
            ...styles.tab,
            ...(activeCalculator === 'macros' ? styles.activeTab : {})
          }}
        >
          🥑 Macronutrientes
        </button>
        <button
          onClick={() => setActiveCalculator('portions')}
          style={{
            ...styles.tab,
            ...(activeCalculator === 'portions' ? styles.activeTab : {})
          }}
        >
          ⚖️ Porciones
        </button>
      </div>

      <div style={styles.calculatorContainer}>
        {/* BMI Calculator */}
        {activeCalculator === 'bmi' && (
          <div style={styles.calculator}>
            <h2 style={styles.calculatorTitle}>Calculadora de Índice de Masa Corporal (IMC)</h2>
            <p style={styles.calculatorDescription}>
              El IMC es una medida que relaciona tu peso y altura para estimar si tienes un peso saludable.
            </p>

            <div style={styles.inputGrid}>
              <div style={styles.inputGroup}>
                <label style={styles.label}>Peso (kg)</label>
                <input
                  type="number"
                  value={bmiData.weight}
                  onChange={(e) => setBmiData({ ...bmiData, weight: e.target.value })}
                  placeholder="70"
                  style={styles.input}
                />
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>Altura (cm)</label>
                <input
                  type="number"
                  value={bmiData.height}
                  onChange={(e) => setBmiData({ ...bmiData, height: e.target.value })}
                  placeholder="170"
                  style={styles.input}
                />
              </div>
            </div>

            <button onClick={calculateBMI} style={styles.calculateButton}>
              Calcular IMC
            </button>

            {bmiData.result && (
              <div style={styles.resultContainer}>
                <div style={{
                  ...styles.bmiResult,
                  backgroundColor: bmiData.result.color
                }}>
                  <div style={styles.bmiValue}>{bmiData.result.bmi}</div>
                  <div style={styles.bmiCategory}>{bmiData.result.category}</div>
                </div>

                <div style={styles.recommendation}>
                  <h3 style={styles.recommendationTitle}>Recomendación:</h3>
                  <p>{bmiData.result.recommendation}</p>
                </div>

                <div style={styles.bmiScale}>
                  <h3 style={styles.scaleTitle}>Escala de IMC:</h3>
                  <div style={styles.scaleBar}>
                    <div style={{...styles.scaleSegment, backgroundColor: '#3498db'}}>
                      <span>&lt; 18.5</span>
                      <span>Bajo Peso</span>
                    </div>
                    <div style={{...styles.scaleSegment, backgroundColor: '#27ae60'}}>
                      <span>18.5 - 24.9</span>
                      <span>Normal</span>
                    </div>
                    <div style={{...styles.scaleSegment, backgroundColor: '#f39c12'}}>
                      <span>25 - 29.9</span>
                      <span>Sobrepeso</span>
                    </div>
                    <div style={{...styles.scaleSegment, backgroundColor: '#e74c3c'}}>
                      <span>≥ 30</span>
                      <span>Obesidad</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Calorie Calculator */}
        {activeCalculator === 'calories' && (
          <div style={styles.calculator}>
            <h2 style={styles.calculatorTitle}>Calculadora de Requerimientos Calóricos</h2>
            <p style={styles.calculatorDescription}>
              Calcula tus necesidades calóricas diarias basadas en tu metabolismo basal y nivel de actividad.
            </p>

            <div style={styles.inputGrid}>
              <div style={styles.inputGroup}>
                <label style={styles.label}>Peso (kg)</label>
                <input
                  type="number"
                  value={calorieData.weight}
                  onChange={(e) => setCalorieData({ ...calorieData, weight: e.target.value })}
                  placeholder="70"
                  style={styles.input}
                />
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>Altura (cm)</label>
                <input
                  type="number"
                  value={calorieData.height}
                  onChange={(e) => setCalorieData({ ...calorieData, height: e.target.value })}
                  placeholder="170"
                  style={styles.input}
                />
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>Edad (años)</label>
                <input
                  type="number"
                  value={calorieData.age}
                  onChange={(e) => setCalorieData({ ...calorieData, age: e.target.value })}
                  placeholder="30"
                  style={styles.input}
                />
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>Género</label>
                <select
                  value={calorieData.gender}
                  onChange={(e) => setCalorieData({ ...calorieData, gender: e.target.value })}
                  style={styles.select}
                >
                  <option value="male">Masculino</option>
                  <option value="female">Femenino</option>
                </select>
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>Nivel de Actividad</label>
                <select
                  value={calorieData.activityLevel}
                  onChange={(e) => setCalorieData({ ...calorieData, activityLevel: e.target.value })}
                  style={styles.select}
                >
                  <option value="sedentary">Sedentario (poco o ningún ejercicio)</option>
                  <option value="light">Ligero (ejercicio 1-3 días/semana)</option>
                  <option value="moderate">Moderado (ejercicio 3-5 días/semana)</option>
                  <option value="active">Activo (ejercicio 6-7 días/semana)</option>
                  <option value="very_active">Muy Activo (ejercicio intenso diario)</option>
                </select>
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>Objetivo</label>
                <select
                  value={calorieData.goal}
                  onChange={(e) => setCalorieData({ ...calorieData, goal: e.target.value })}
                  style={styles.select}
                >
                  <option value="lose">Pérdida de Peso</option>
                  <option value="maintain">Mantenimiento</option>
                  <option value="gain">Aumento de Peso</option>
                </select>
              </div>
            </div>

            <button onClick={calculateCalories} style={styles.calculateButton}>
              Calcular Calorías
            </button>

            {calorieData.result && (
              <div style={styles.resultContainer}>
                <div style={styles.calorieResults}>
                  <div style={styles.calorieCard}>
                    <div style={styles.calorieLabel}>Metabolismo Basal (BMR)</div>
                    <div style={styles.calorieValue}>{calorieData.result.bmr} kcal</div>
                    <div style={styles.calorieDesc}>Calorías que quemas en reposo</div>
                  </div>

                  <div style={styles.calorieCard}>
                    <div style={styles.calorieLabel}>Gasto Energético Total (TDEE)</div>
                    <div style={styles.calorieValue}>{calorieData.result.tdee} kcal</div>
                    <div style={styles.calorieDesc}>Calorías de mantenimiento</div>
                  </div>

                  <div style={{...styles.calorieCard, ...styles.targetCard}}>
                    <div style={styles.calorieLabel}>Objetivo Diario</div>
                    <div style={styles.calorieValue}>{calorieData.result.targetCalories} kcal</div>
                    <div style={styles.calorieDesc}>{calorieData.result.description}</div>
                  </div>
                </div>

                <div style={styles.infoBox}>
                  <h3 style={styles.infoTitle}>💡 Información Importante:</h3>
                  <ul style={styles.infoList}>
                    <li>Estos cálculos son estimaciones basadas en ecuaciones estándar</li>
                    <li>Los resultados pueden variar según metabolismo individual</li>
                    <li>Se recomienda ajustar según resultados y consultar con un profesional</li>
                    <li>Para perder peso de forma saludable: 0.5-1 kg por semana</li>
                  </ul>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Macro Calculator */}
        {activeCalculator === 'macros' && (
          <div style={styles.calculator}>
            <h2 style={styles.calculatorTitle}>Calculadora de Macronutrientes</h2>
            <p style={styles.calculatorDescription}>
              Distribuye tus calorías diarias en proteínas, carbohidratos y grasas según tu objetivo.
            </p>

            <div style={styles.inputGrid}>
              <div style={styles.inputGroup}>
                <label style={styles.label}>Calorías Diarias Objetivo</label>
                <input
                  type="number"
                  value={macroData.calories}
                  onChange={(e) => setMacroData({ ...macroData, calories: e.target.value })}
                  placeholder="2000"
                  style={styles.input}
                />
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>Distribución de Macros</label>
                <select
                  value={macroData.goal}
                  onChange={(e) => setMacroData({ ...macroData, goal: e.target.value })}
                  style={styles.select}
                >
                  <option value="balanced">Balanceada (30/40/30)</option>
                  <option value="high_protein">Alta en Proteína (40/30/30)</option>
                  <option value="low_carb">Baja en Carbohidratos (35/25/40)</option>
                  <option value="low_fat">Baja en Grasa (25/55/20)</option>
                </select>
              </div>
            </div>

            <button onClick={calculateMacros} style={styles.calculateButton}>
              Calcular Macros
            </button>

            {macroData.result && (
              <div style={styles.resultContainer}>
                <div style={styles.macroDescription}>
                  <p>{macroData.result.description}</p>
                </div>

                <div style={styles.macrosGrid}>
                  <div style={{...styles.macroCard, borderColor: '#e74c3c'}}>
                    <div style={{...styles.macroIcon, backgroundColor: '#e74c3c'}}>🥩</div>
                    <div style={styles.macroName}>Proteínas</div>
                    <div style={styles.macroAmount}>{macroData.result.protein.grams}g</div>
                    <div style={styles.macroPercent}>{macroData.result.protein.percent}%</div>
                    <div style={styles.macroCalories}>
                      {macroData.result.protein.grams * 4} kcal
                    </div>
                  </div>

                  <div style={{...styles.macroCard, borderColor: '#f39c12'}}>
                    <div style={{...styles.macroIcon, backgroundColor: '#f39c12'}}>🍞</div>
                    <div style={styles.macroName}>Carbohidratos</div>
                    <div style={styles.macroAmount}>{macroData.result.carbs.grams}g</div>
                    <div style={styles.macroPercent}>{macroData.result.carbs.percent}%</div>
                    <div style={styles.macroCalories}>
                      {macroData.result.carbs.grams * 4} kcal
                    </div>
                  </div>

                  <div style={{...styles.macroCard, borderColor: '#3498db'}}>
                    <div style={{...styles.macroIcon, backgroundColor: '#3498db'}}>🥑</div>
                    <div style={styles.macroName}>Grasas</div>
                    <div style={styles.macroAmount}>{macroData.result.fat.grams}g</div>
                    <div style={styles.macroPercent}>{macroData.result.fat.percent}%</div>
                    <div style={styles.macroCalories}>
                      {macroData.result.fat.grams * 9} kcal
                    </div>
                  </div>
                </div>

                <div style={styles.infoBox}>
                  <h3 style={styles.infoTitle}>📌 Funciones de los Macronutrientes:</h3>
                  <div style={styles.macroInfo}>
                    <div style={styles.macroInfoItem}>
                      <strong>Proteínas (4 kcal/g):</strong>
                      <p>Construcción y reparación de tejidos, síntesis de enzimas y hormonas</p>
                    </div>
                    <div style={styles.macroInfoItem}>
                      <strong>Carbohidratos (4 kcal/g):</strong>
                      <p>Principal fuente de energía, especialmente para cerebro y músculos</p>
                    </div>
                    <div style={styles.macroInfoItem}>
                      <strong>Grasas (9 kcal/g):</strong>
                      <p>Energía de reserva, absorción de vitaminas, función hormonal</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Portion Calculator */}
        {activeCalculator === 'portions' && (
          <div style={styles.calculator}>
            <h2 style={styles.calculatorTitle}>Calculadora de Porciones</h2>
            <p style={styles.calculatorDescription}>
              Calcula el tamaño de las porciones según el número de servicios deseados.
            </p>

            <div style={styles.inputGrid}>
              <div style={styles.inputGroup}>
                <label style={styles.label}>Tipo de Alimento</label>
                <select
                  value={portionData.foodType}
                  onChange={(e) => setPortionData({ ...portionData, foodType: e.target.value })}
                  style={styles.select}
                >
                  <option value="protein">Proteína</option>
                  <option value="vegetables">Vegetales</option>
                  <option value="grains">Granos/Cereales</option>
                  <option value="fruits">Frutas</option>
                  <option value="dairy">Lácteos</option>
                  <option value="fats">Grasas Saludables</option>
                </select>
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>Número de Porciones</label>
                <input
                  type="number"
                  value={portionData.servings}
                  onChange={(e) => setPortionData({ ...portionData, servings: e.target.value })}
                  placeholder="2"
                  step="0.5"
                  style={styles.input}
                />
              </div>
            </div>

            <button onClick={calculatePortions} style={styles.calculateButton}>
              Calcular Porciones
            </button>

            {portionData.result && (
              <div style={styles.resultContainer}>
                <div style={styles.portionResult}>
                  <h3 style={styles.portionTitle}>{portionData.result.name}</h3>

                  <div style={styles.portionAmount}>
                    <div style={styles.portionValue}>
                      {portionData.result.totalAmount} {portionData.result.unit}
                    </div>
                    <div style={styles.portionServings}>
                      {portionData.result.servings} {portionData.result.servings === 1 ? 'porción' : 'porciones'}
                    </div>
                  </div>

                  <div style={styles.portionStandard}>
                    <p><strong>Tamaño estándar por porción:</strong> {portionData.result.standard} {portionData.result.unit}</p>
                  </div>

                  <div style={styles.portionExamples}>
                    <h4 style={styles.examplesTitle}>Ejemplos de alimentos:</h4>
                    <ul style={styles.examplesList}>
                      {portionData.result.examples.map((example, index) => (
                        <li key={index}>{example}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div style={styles.infoBox}>
                  <h3 style={styles.infoTitle}>🍽️ Guía Visual de Porciones:</h3>
                  <div style={styles.visualGuide}>
                    <div style={styles.guideItem}>
                      <strong>✊ Puño cerrado:</strong> ~1 taza de vegetales o frutas
                    </div>
                    <div style={styles.guideItem}>
                      <strong>🤚 Palma de la mano:</strong> ~100g de proteína (carne, pescado)
                    </div>
                    <div style={styles.guideItem}>
                      <strong>👍 Pulgar:</strong> ~15g de grasas (mantequilla, aceite)
                    </div>
                    <div style={styles.guideItem}>
                      <strong>🤏 Puñado:</strong> ~30g de frutos secos o cereales
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
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
    marginBottom: '30px',
    textAlign: 'center'
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
  tabsContainer: {
    display: 'flex',
    gap: '10px',
    marginBottom: '30px',
    justifyContent: 'center',
    flexWrap: 'wrap'
  },
  tab: {
    padding: '12px 24px',
    backgroundColor: 'white',
    border: '2px solid #e9ecef',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: '500',
    transition: 'all 0.3s ease'
  },
  activeTab: {
    backgroundColor: '#3498db',
    color: 'white',
    borderColor: '#3498db'
  },
  calculatorContainer: {
    maxWidth: '900px',
    margin: '0 auto'
  },
  calculator: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '30px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
  },
  calculatorTitle: {
    fontSize: '1.8rem',
    color: '#2c3e50',
    marginBottom: '10px'
  },
  calculatorDescription: {
    color: '#7f8c8d',
    marginBottom: '25px',
    lineHeight: '1.6'
  },
  inputGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
    marginBottom: '25px'
  },
  inputGroup: {
    display: 'flex',
    flexDirection: 'column'
  },
  label: {
    fontSize: '0.9rem',
    color: '#2c3e50',
    marginBottom: '8px',
    fontWeight: '600'
  },
  input: {
    padding: '12px',
    border: '2px solid #e9ecef',
    borderRadius: '8px',
    fontSize: '16px'
  },
  select: {
    padding: '12px',
    border: '2px solid #e9ecef',
    borderRadius: '8px',
    fontSize: '16px',
    backgroundColor: 'white'
  },
  calculateButton: {
    width: '100%',
    padding: '15px',
    backgroundColor: '#27ae60',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '18px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'background-color 0.3s ease'
  },
  resultContainer: {
    marginTop: '30px',
    padding: '20px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px'
  },
  // BMI Styles
  bmiResult: {
    padding: '30px',
    borderRadius: '12px',
    textAlign: 'center',
    color: 'white',
    marginBottom: '20px'
  },
  bmiValue: {
    fontSize: '4rem',
    fontWeight: '700',
    marginBottom: '10px'
  },
  bmiCategory: {
    fontSize: '1.5rem',
    fontWeight: '600'
  },
  recommendation: {
    padding: '20px',
    backgroundColor: 'white',
    borderRadius: '8px',
    marginBottom: '20px'
  },
  recommendationTitle: {
    color: '#2c3e50',
    marginBottom: '10px'
  },
  bmiScale: {
    marginTop: '20px'
  },
  scaleTitle: {
    color: '#2c3e50',
    marginBottom: '15px'
  },
  scaleBar: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '10px'
  },
  scaleSegment: {
    padding: '15px',
    borderRadius: '8px',
    textAlign: 'center',
    color: 'white',
    fontSize: '0.85rem',
    fontWeight: '600',
    display: 'flex',
    flexDirection: 'column',
    gap: '5px'
  },
  // Calorie Styles
  calorieResults: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
    marginBottom: '20px'
  },
  calorieCard: {
    padding: '20px',
    backgroundColor: 'white',
    borderRadius: '8px',
    textAlign: 'center'
  },
  targetCard: {
    border: '3px solid #27ae60',
    backgroundColor: '#e8f8f5'
  },
  calorieLabel: {
    fontSize: '0.9rem',
    color: '#7f8c8d',
    marginBottom: '10px',
    fontWeight: '600'
  },
  calorieValue: {
    fontSize: '2.5rem',
    color: '#2c3e50',
    fontWeight: '700',
    marginBottom: '5px'
  },
  calorieDesc: {
    fontSize: '0.85rem',
    color: '#7f8c8d'
  },
  // Macro Styles
  macroDescription: {
    padding: '15px',
    backgroundColor: '#ebf5fb',
    borderRadius: '8px',
    marginBottom: '20px',
    textAlign: 'center',
    color: '#2c3e50'
  },
  macrosGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '20px',
    marginBottom: '20px'
  },
  macroCard: {
    padding: '25px',
    backgroundColor: 'white',
    borderRadius: '12px',
    textAlign: 'center',
    border: '3px solid',
    transition: 'transform 0.2s ease'
  },
  macroIcon: {
    width: '60px',
    height: '60px',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '30px',
    margin: '0 auto 15px',
    color: 'white'
  },
  macroName: {
    fontSize: '1.1rem',
    color: '#2c3e50',
    fontWeight: '600',
    marginBottom: '10px'
  },
  macroAmount: {
    fontSize: '2.5rem',
    color: '#2c3e50',
    fontWeight: '700',
    marginBottom: '5px'
  },
  macroPercent: {
    fontSize: '1.2rem',
    color: '#7f8c8d',
    marginBottom: '5px'
  },
  macroCalories: {
    fontSize: '0.9rem',
    color: '#95a5a6'
  },
  macroInfo: {
    display: 'grid',
    gap: '15px'
  },
  macroInfoItem: {
    padding: '15px',
    backgroundColor: 'white',
    borderRadius: '8px'
  },
  // Portion Styles
  portionResult: {
    padding: '20px',
    backgroundColor: 'white',
    borderRadius: '8px',
    marginBottom: '20px'
  },
  portionTitle: {
    fontSize: '1.5rem',
    color: '#2c3e50',
    marginBottom: '20px',
    textAlign: 'center'
  },
  portionAmount: {
    textAlign: 'center',
    padding: '30px',
    backgroundColor: '#ebf5fb',
    borderRadius: '8px',
    marginBottom: '20px'
  },
  portionValue: {
    fontSize: '3rem',
    color: '#3498db',
    fontWeight: '700',
    marginBottom: '10px'
  },
  portionServings: {
    fontSize: '1.2rem',
    color: '#7f8c8d'
  },
  portionStandard: {
    padding: '15px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    marginBottom: '15px',
    textAlign: 'center'
  },
  portionExamples: {
    padding: '15px'
  },
  examplesTitle: {
    color: '#2c3e50',
    marginBottom: '10px'
  },
  examplesList: {
    listStylePosition: 'inside',
    color: '#7f8c8d'
  },
  // Info Box Styles
  infoBox: {
    padding: '20px',
    backgroundColor: 'white',
    borderRadius: '8px',
    border: '2px solid #3498db'
  },
  infoTitle: {
    color: '#2c3e50',
    marginBottom: '15px'
  },
  infoList: {
    color: '#7f8c8d',
    lineHeight: '1.8',
    paddingLeft: '20px'
  },
  visualGuide: {
    display: 'grid',
    gap: '10px'
  },
  guideItem: {
    padding: '10px',
    backgroundColor: '#f8f9fa',
    borderRadius: '6px',
    color: '#2c3e50'
  }
};

export default NutritionCalculator;
