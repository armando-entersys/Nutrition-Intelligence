import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';

const RecipesBrowser = () => {
  const [recipes, setRecipes] = useState([]);
  const [foods, setFoods] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedMealType, setSelectedMealType] = useState('ALL');
  const [selectedDifficulty, setSelectedDifficulty] = useState('ALL');
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    meal_type: 'BREAKFAST',
    difficulty: 'EASY',
    preparation_time_minutes: '',
    cooking_time_minutes: '',
    servings: '',
    instructions: '',
    ingredients: []
  });
  const [newIngredient, setNewIngredient] = useState({
    food_id: '',
    quantity_grams: ''
  });

  const mealTypes = [
    { value: 'ALL', label: 'Todos los Tipos' },
    { value: 'BREAKFAST', label: '🌅 Desayuno' },
    { value: 'LUNCH', label: '🌞 Almuerzo' },
    { value: 'DINNER', label: '🌙 Cena' },
    { value: 'SNACK', label: '🍪 Merienda' },
  ];

  const difficulties = [
    { value: 'ALL', label: 'Todas las Dificultades' },
    { value: 'EASY', label: '😊 Fácil' },
    { value: 'MEDIUM', label: '🤔 Media' },
    { value: 'HARD', label: '😰 Difícil' },
  ];

  useEffect(() => {
    fetchRecipes();
    fetchFoods();
  }, []);

  const fetchRecipes = async () => {
    setLoading(true);
    setError(null);
    try {
      // Mock recipes data
      const mockRecipes = [
        {
          id: 1,
          name: 'Ensalada César con Pollo',
          description: 'Clásica ensalada césar con pechuga de pollo a la plancha',
          meal_type: 'LUNCH',
          difficulty: 'EASY',
          preparation_time_minutes: 15,
          cooking_time_minutes: 10,
          servings: 2,
          instructions: '1. Lavar la lechuga\n2. Cocinar el pollo\n3. Preparar el aderezo\n4. Mezclar todos los ingredientes',
          ingredients: [
            { food_name: 'Pechuga de Pollo', quantity_grams: 200 },
            { food_name: 'Lechuga', quantity_grams: 150 },
          ],
          calories: 350,
          protein: 35,
          carbs: 15,
          fat: 18
        },
        {
          id: 2,
          name: 'Avena con Frutas',
          description: 'Desayuno nutritivo con avena, plátano y fresas',
          meal_type: 'BREAKFAST',
          difficulty: 'EASY',
          preparation_time_minutes: 5,
          cooking_time_minutes: 5,
          servings: 1,
          instructions: '1. Cocinar la avena\n2. Cortar las frutas\n3. Mezclar y servir',
          ingredients: [
            { food_name: 'Avena', quantity_grams: 50 },
            { food_name: 'Plátano', quantity_grams: 100 },
            { food_name: 'Fresas', quantity_grams: 80 },
          ],
          calories: 320,
          protein: 12,
          carbs: 55,
          fat: 6
        },
        {
          id: 3,
          name: 'Salmón al Horno con Vegetales',
          description: 'Salmón perfectamente horneado con vegetales asados',
          meal_type: 'DINNER',
          difficulty: 'MEDIUM',
          preparation_time_minutes: 20,
          cooking_time_minutes: 25,
          servings: 2,
          instructions: '1. Precalentar horno\n2. Preparar vegetales\n3. Sazonar salmón\n4. Hornear todo junto',
          ingredients: [
            { food_name: 'Salmón', quantity_grams: 300 },
            { food_name: 'Brócoli', quantity_grams: 200 },
            { food_name: 'Zanahoria', quantity_grams: 150 },
          ],
          calories: 450,
          protein: 42,
          carbs: 20,
          fat: 22
        }
      ];
      setRecipes(mockRecipes);
    } catch (err) {
      setError('Error al cargar recetas: ' + err.message);
      console.error('Error fetching recipes:', err);
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

  const filteredRecipes = recipes.filter(recipe => {
    const matchesSearch = recipe.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         recipe.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesMealType = selectedMealType === 'ALL' || recipe.meal_type === selectedMealType;
    const matchesDifficulty = selectedDifficulty === 'ALL' || recipe.difficulty === selectedDifficulty;
    return matchesSearch && matchesMealType && matchesDifficulty;
  });

  const handleRecipeClick = (recipe) => {
    setSelectedRecipe(recipe);
    setShowAddForm(false);
    setShowEditForm(false);
  };

  const handleAddNew = () => {
    setSelectedRecipe(null);
    setShowAddForm(true);
    setShowEditForm(false);
    setFormData({
      name: '',
      description: '',
      meal_type: 'BREAKFAST',
      difficulty: 'EASY',
      preparation_time_minutes: '',
      cooking_time_minutes: '',
      servings: '',
      instructions: '',
      ingredients: []
    });
  };

  const handleEdit = () => {
    if (selectedRecipe) {
      setShowEditForm(true);
      setShowAddForm(false);
      setFormData({
        name: selectedRecipe.name,
        description: selectedRecipe.description,
        meal_type: selectedRecipe.meal_type,
        difficulty: selectedRecipe.difficulty,
        preparation_time_minutes: selectedRecipe.preparation_time_minutes,
        cooking_time_minutes: selectedRecipe.cooking_time_minutes,
        servings: selectedRecipe.servings,
        instructions: selectedRecipe.instructions,
        ingredients: selectedRecipe.ingredients || []
      });
    }
  };

  const handleCloseDetails = () => {
    setSelectedRecipe(null);
    setShowAddForm(false);
    setShowEditForm(false);
  };

  const handleFormChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleAddIngredient = () => {
    if (newIngredient.food_id && newIngredient.quantity_grams) {
      const food = foods.find(f => f.id === parseInt(newIngredient.food_id));
      if (food) {
        setFormData(prev => ({
          ...prev,
          ingredients: [...prev.ingredients, {
            food_id: food.id,
            food_name: food.name,
            quantity_grams: parseFloat(newIngredient.quantity_grams)
          }]
        }));
        setNewIngredient({ food_id: '', quantity_grams: '' });
      }
    }
  };

  const handleRemoveIngredient = (index) => {
    setFormData(prev => ({
      ...prev,
      ingredients: prev.ingredients.filter((_, i) => i !== index)
    }));
  };

  const calculateNutrition = (ingredients) => {
    let totalCalories = 0, totalProtein = 0, totalCarbs = 0, totalFat = 0;

    ingredients.forEach(ing => {
      const food = foods.find(f => f.id === ing.food_id || f.name === ing.food_name);
      if (food) {
        const factor = ing.quantity_grams / 100;
        totalCalories += (food.calories_per_100g || 0) * factor;
        totalProtein += (food.protein_per_100g || 0) * factor;
        totalCarbs += (food.carbs_per_100g || 0) * factor;
        totalFat += (food.fat_per_100g || 0) * factor;
      }
    });

    return {
      calories: Math.round(totalCalories),
      protein: Math.round(totalProtein),
      carbs: Math.round(totalCarbs),
      fat: Math.round(totalFat)
    };
  };

  const handleSaveNew = async () => {
    try {
      const nutrition = calculateNutrition(formData.ingredients);
      const newRecipe = {
        id: recipes.length + 1,
        ...formData,
        preparation_time_minutes: parseInt(formData.preparation_time_minutes) || 0,
        cooking_time_minutes: parseInt(formData.cooking_time_minutes) || 0,
        servings: parseInt(formData.servings) || 1,
        ...nutrition
      };

      setRecipes([...recipes, newRecipe]);
      setSelectedRecipe(newRecipe);
      setShowAddForm(false);

      alert('✅ Receta agregada exitosamente!');
    } catch (err) {
      alert('❌ Error al guardar: ' + err.message);
    }
  };

  const handleSaveEdit = async () => {
    try {
      const nutrition = calculateNutrition(formData.ingredients);
      const updatedRecipe = {
        ...selectedRecipe,
        ...formData,
        preparation_time_minutes: parseInt(formData.preparation_time_minutes) || 0,
        cooking_time_minutes: parseInt(formData.cooking_time_minutes) || 0,
        servings: parseInt(formData.servings) || 1,
        ...nutrition
      };

      setRecipes(recipes.map(r => r.id === selectedRecipe.id ? updatedRecipe : r));
      setSelectedRecipe(updatedRecipe);
      setShowEditForm(false);

      alert('✅ Receta actualizada exitosamente!');
    } catch (err) {
      alert('❌ Error al actualizar: ' + err.message);
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`¿Estás seguro de eliminar "${selectedRecipe.name}"?`)) {
      try {
        setRecipes(recipes.filter(r => r.id !== selectedRecipe.id));
        setSelectedRecipe(null);
        alert('✅ Receta eliminada exitosamente!');
      } catch (err) {
        alert('❌ Error al eliminar: ' + err.message);
      }
    }
  };

  const getTotalTime = (recipe) => {
    return (recipe.preparation_time_minutes || 0) + (recipe.cooking_time_minutes || 0);
  };

  const renderRecipeForm = (isEdit = false) => (
    <div style={styles.formContent}>
      <div style={styles.formGroup}>
        <label style={styles.formLabel}>Nombre de la Receta</label>
        <input
          type="text"
          style={styles.formInput}
          placeholder="Ej: Ensalada César"
          value={formData.name}
          onChange={(e) => handleFormChange('name', e.target.value)}
        />
      </div>

      <div style={styles.formGroup}>
        <label style={styles.formLabel}>Descripción</label>
        <textarea
          style={{...styles.formInput, minHeight: '60px'}}
          placeholder="Describe brevemente la receta"
          value={formData.description}
          onChange={(e) => handleFormChange('description', e.target.value)}
        />
      </div>

      <div style={styles.formRow}>
        <div style={styles.formGroup}>
          <label style={styles.formLabel}>Tipo de Comida</label>
          <select
            style={styles.formInput}
            value={formData.meal_type}
            onChange={(e) => handleFormChange('meal_type', e.target.value)}
          >
            {mealTypes.filter(m => m.value !== 'ALL').map(type => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
        </div>
        <div style={styles.formGroup}>
          <label style={styles.formLabel}>Dificultad</label>
          <select
            style={styles.formInput}
            value={formData.difficulty}
            onChange={(e) => handleFormChange('difficulty', e.target.value)}
          >
            {difficulties.filter(d => d.value !== 'ALL').map(diff => (
              <option key={diff.value} value={diff.value}>
                {diff.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div style={styles.formRow}>
        <div style={styles.formGroup}>
          <label style={styles.formLabel}>Tiempo de Prep. (min)</label>
          <input
            type="number"
            style={styles.formInput}
            placeholder="15"
            value={formData.preparation_time_minutes}
            onChange={(e) => handleFormChange('preparation_time_minutes', e.target.value)}
          />
        </div>
        <div style={styles.formGroup}>
          <label style={styles.formLabel}>Tiempo de Cocción (min)</label>
          <input
            type="number"
            style={styles.formInput}
            placeholder="20"
            value={formData.cooking_time_minutes}
            onChange={(e) => handleFormChange('cooking_time_minutes', e.target.value)}
          />
        </div>
        <div style={styles.formGroup}>
          <label style={styles.formLabel}>Porciones</label>
          <input
            type="number"
            style={styles.formInput}
            placeholder="2"
            value={formData.servings}
            onChange={(e) => handleFormChange('servings', e.target.value)}
          />
        </div>
      </div>

      <div style={styles.formGroup}>
        <label style={styles.formLabel}>Instrucciones</label>
        <textarea
          style={{...styles.formInput, minHeight: '120px'}}
          placeholder="1. Paso uno&#10;2. Paso dos&#10;3. Paso tres"
          value={formData.instructions}
          onChange={(e) => handleFormChange('instructions', e.target.value)}
        />
      </div>

      <div style={styles.ingredientsSection}>
        <h4 style={styles.sectionTitle}>Ingredientes</h4>

        <div style={styles.addIngredientRow}>
          <select
            style={{...styles.formInput, flex: 2}}
            value={newIngredient.food_id}
            onChange={(e) => setNewIngredient(prev => ({...prev, food_id: e.target.value}))}
          >
            <option value="">Seleccionar alimento...</option>
            {foods.map(food => (
              <option key={food.id} value={food.id}>
                {food.name}
              </option>
            ))}
          </select>
          <input
            type="number"
            style={{...styles.formInput, flex: 1}}
            placeholder="Cantidad (g)"
            value={newIngredient.quantity_grams}
            onChange={(e) => setNewIngredient(prev => ({...prev, quantity_grams: e.target.value}))}
          />
          <button style={styles.addIngredientButton} onClick={handleAddIngredient}>
            ➕ Agregar
          </button>
        </div>

        <div style={styles.ingredientsList}>
          {formData.ingredients.map((ing, index) => (
            <div key={index} style={styles.ingredientItem}>
              <span>{ing.food_name || 'Alimento'}</span>
              <span>{ing.quantity_grams}g</span>
              <button
                style={styles.removeIngredientButton}
                onClick={() => handleRemoveIngredient(index)}
              >
                ✕
              </button>
            </div>
          ))}
          {formData.ingredients.length === 0 && (
            <p style={styles.emptyIngredients}>No hay ingredientes agregados</p>
          )}
        </div>
      </div>

      <div style={styles.formActions}>
        <button
          style={styles.saveButton}
          onClick={isEdit ? handleSaveEdit : handleSaveNew}
        >
          💾 {isEdit ? 'Actualizar' : 'Guardar'} Receta
        </button>
        <button style={styles.cancelButton} onClick={handleCloseDetails}>
          ❌ Cancelar
        </button>
      </div>
    </div>
  );

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>🍽️ Gestión de Recetas</h1>
        <p style={styles.subtitle}>Crea y administra recetas saludables y nutritivas</p>
      </div>

      {/* Search and Filter Section */}
      <div style={styles.searchSection}>
        <div style={styles.searchBar}>
          <input
            type="text"
            placeholder="🔍 Buscar recetas..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={styles.searchInput}
          />
        </div>

        <div style={styles.filterSection}>
          <label style={styles.filterLabel}>Tipo:</label>
          <select
            value={selectedMealType}
            onChange={(e) => setSelectedMealType(e.target.value)}
            style={styles.select}
          >
            {mealTypes.map(type => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
        </div>

        <div style={styles.filterSection}>
          <label style={styles.filterLabel}>Dificultad:</label>
          <select
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
            style={styles.select}
          >
            {difficulties.map(diff => (
              <option key={diff.value} value={diff.value}>
                {diff.label}
              </option>
            ))}
          </select>
        </div>

        <button onClick={handleAddNew} style={styles.addButton}>
          ➕ Crear Nueva Receta
        </button>
      </div>

      {/* Main Content */}
      <div style={styles.mainContent}>
        {/* Recipes List */}
        <div style={styles.recipesList}>
          <div style={styles.listHeader}>
            <h3>Recetas ({filteredRecipes.length})</h3>
            <button onClick={fetchRecipes} style={styles.refreshButton}>
              🔄 Actualizar
            </button>
          </div>

          {loading && (
            <div style={styles.loadingMessage}>
              Cargando recetas...
            </div>
          )}

          {error && (
            <div style={styles.errorMessage}>
              {error}
            </div>
          )}

          {!loading && !error && filteredRecipes.length === 0 && (
            <div style={styles.emptyMessage}>
              No se encontraron recetas
            </div>
          )}

          {!loading && !error && filteredRecipes.map(recipe => (
            <div
              key={recipe.id}
              style={{
                ...styles.recipeCard,
                ...(selectedRecipe?.id === recipe.id ? styles.selectedRecipeCard : {})
              }}
              onClick={() => handleRecipeClick(recipe)}
            >
              <div style={styles.recipeCardHeader}>
                <h4 style={styles.recipeName}>{recipe.name}</h4>
                <div style={styles.recipeMeta}>
                  <span style={styles.metaBadge}>
                    {mealTypes.find(m => m.value === recipe.meal_type)?.label.split(' ')[0]}
                  </span>
                  <span style={styles.metaBadge}>
                    {difficulties.find(d => d.value === recipe.difficulty)?.label.split(' ')[0]}
                  </span>
                </div>
              </div>
              <p style={styles.recipeDescription}>{recipe.description}</p>
              <div style={styles.recipeCardStats}>
                <span>⏱️ {getTotalTime(recipe)} min</span>
                <span>👥 {recipe.servings} porción(es)</span>
                <span>🔥 {recipe.calories} kcal</span>
              </div>
            </div>
          ))}
        </div>

        {/* Details Panel */}
        <div style={styles.detailsPanel}>
          {!selectedRecipe && !showAddForm && !showEditForm && (
            <div style={styles.emptyDetails}>
              <h3>Selecciona una receta</h3>
              <p>Haz clic en una receta de la lista para ver sus detalles completos</p>
            </div>
          )}

          {selectedRecipe && !showAddForm && !showEditForm && (
            <div style={styles.recipeDetails}>
              <div style={styles.detailsHeader}>
                <h2>{selectedRecipe.name}</h2>
                <button onClick={handleCloseDetails} style={styles.closeButton}>
                  ✕
                </button>
              </div>

              <p style={styles.detailsDescription}>{selectedRecipe.description}</p>

              <div style={styles.detailsSection}>
                <h3>Información</h3>
                <div style={styles.detailsGrid}>
                  <div style={styles.detailItem}>
                    <span style={styles.detailLabel}>Tipo:</span>
                    <span style={styles.detailValue}>
                      {mealTypes.find(m => m.value === selectedRecipe.meal_type)?.label}
                    </span>
                  </div>
                  <div style={styles.detailItem}>
                    <span style={styles.detailLabel}>Dificultad:</span>
                    <span style={styles.detailValue}>
                      {difficulties.find(d => d.value === selectedRecipe.difficulty)?.label}
                    </span>
                  </div>
                  <div style={styles.detailItem}>
                    <span style={styles.detailLabel}>Tiempo Total:</span>
                    <span style={styles.detailValue}>
                      {getTotalTime(selectedRecipe)} minutos
                    </span>
                  </div>
                  <div style={styles.detailItem}>
                    <span style={styles.detailLabel}>Porciones:</span>
                    <span style={styles.detailValue}>
                      {selectedRecipe.servings}
                    </span>
                  </div>
                </div>
              </div>

              <div style={styles.detailsSection}>
                <h3>Información Nutricional (por porción)</h3>
                <div style={styles.nutritionGrid}>
                  <div style={styles.nutritionCard}>
                    <div style={styles.nutritionIcon}>🔥</div>
                    <div style={styles.nutritionValue}>
                      {Math.round(selectedRecipe.calories / selectedRecipe.servings)}
                    </div>
                    <div style={styles.nutritionLabel}>Calorías</div>
                  </div>
                  <div style={styles.nutritionCard}>
                    <div style={styles.nutritionIcon}>🥩</div>
                    <div style={styles.nutritionValue}>
                      {Math.round(selectedRecipe.protein / selectedRecipe.servings)}g
                    </div>
                    <div style={styles.nutritionLabel}>Proteínas</div>
                  </div>
                  <div style={styles.nutritionCard}>
                    <div style={styles.nutritionIcon}>🍞</div>
                    <div style={styles.nutritionValue}>
                      {Math.round(selectedRecipe.carbs / selectedRecipe.servings)}g
                    </div>
                    <div style={styles.nutritionLabel}>Carbohidratos</div>
                  </div>
                  <div style={styles.nutritionCard}>
                    <div style={styles.nutritionIcon}>🥑</div>
                    <div style={styles.nutritionValue}>
                      {Math.round(selectedRecipe.fat / selectedRecipe.servings)}g
                    </div>
                    <div style={styles.nutritionLabel}>Grasas</div>
                  </div>
                </div>
              </div>

              <div style={styles.detailsSection}>
                <h3>Ingredientes</h3>
                <ul style={styles.ingredientsList}>
                  {selectedRecipe.ingredients?.map((ing, idx) => (
                    <li key={idx} style={styles.ingredientListItem}>
                      {ing.food_name} - {ing.quantity_grams}g
                    </li>
                  ))}
                </ul>
              </div>

              <div style={styles.detailsSection}>
                <h3>Instrucciones</h3>
                <div style={styles.instructions}>
                  {selectedRecipe.instructions.split('\n').map((step, idx) => (
                    <p key={idx} style={styles.instructionStep}>
                      {step}
                    </p>
                  ))}
                </div>
              </div>

              <div style={styles.actionsSection}>
                <button style={styles.editButton} onClick={handleEdit}>
                  ✏️ Editar
                </button>
                <button style={styles.deleteButton} onClick={handleDelete}>
                  🗑️ Eliminar
                </button>
              </div>
            </div>
          )}

          {showAddForm && (
            <div style={styles.addForm}>
              <div style={styles.detailsHeader}>
                <h2>➕ Crear Nueva Receta</h2>
                <button onClick={handleCloseDetails} style={styles.closeButton}>
                  ✕
                </button>
              </div>
              {renderRecipeForm(false)}
            </div>
          )}

          {showEditForm && (
            <div style={styles.addForm}>
              <div style={styles.detailsHeader}>
                <h2>✏️ Editar Receta</h2>
                <button onClick={handleCloseDetails} style={styles.closeButton}>
                  ✕
                </button>
              </div>
              {renderRecipeForm(true)}
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
  searchSection: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '12px',
    marginBottom: '20px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    display: 'flex',
    gap: '15px',
    alignItems: 'center',
    flexWrap: 'wrap',
  },
  searchBar: {
    flex: '1 1 300px',
  },
  searchInput: {
    width: '100%',
    padding: '12px',
    fontSize: '16px',
    border: '2px solid #e9ecef',
    borderRadius: '8px',
    outline: 'none',
  },
  filterSection: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  filterLabel: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#2c3e50',
  },
  select: {
    padding: '10px',
    fontSize: '14px',
    border: '2px solid #e9ecef',
    borderRadius: '8px',
    outline: 'none',
    cursor: 'pointer',
  },
  addButton: {
    padding: '12px 24px',
    backgroundColor: '#27ae60',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  mainContent: {
    display: 'grid',
    gridTemplateColumns: '400px 1fr',
    gap: '20px',
  },
  recipesList: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '20px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    height: 'calc(100vh - 350px)',
    overflowY: 'auto',
  },
  listHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '15px',
    paddingBottom: '15px',
    borderBottom: '2px solid #f0f0f0',
  },
  refreshButton: {
    padding: '8px 16px',
    backgroundColor: '#3498db',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '12px',
    cursor: 'pointer',
  },
  loadingMessage: {
    textAlign: 'center',
    padding: '40px',
    color: '#7f8c8d',
  },
  errorMessage: {
    textAlign: 'center',
    padding: '20px',
    color: '#e74c3c',
    backgroundColor: '#ffe5e5',
    borderRadius: '8px',
  },
  emptyMessage: {
    textAlign: 'center',
    padding: '40px',
    color: '#95a5a6',
  },
  recipeCard: {
    padding: '15px',
    marginBottom: '10px',
    border: '2px solid #f0f0f0',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  selectedRecipeCard: {
    borderColor: '#3498db',
    backgroundColor: '#f0f8ff',
  },
  recipeCardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '8px',
  },
  recipeName: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#2c3e50',
    margin: 0,
    flex: 1,
  },
  recipeMeta: {
    display: 'flex',
    gap: '5px',
  },
  metaBadge: {
    fontSize: '11px',
    padding: '3px 8px',
    backgroundColor: '#e9ecef',
    borderRadius: '4px',
    color: '#495057',
  },
  recipeDescription: {
    fontSize: '13px',
    color: '#7f8c8d',
    marginBottom: '10px',
  },
  recipeCardStats: {
    display: 'flex',
    gap: '10px',
    fontSize: '12px',
    color: '#7f8c8d',
    flexWrap: 'wrap',
  },
  detailsPanel: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '20px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    height: 'calc(100vh - 350px)',
    overflowY: 'auto',
  },
  emptyDetails: {
    textAlign: 'center',
    padding: '60px 20px',
    color: '#95a5a6',
  },
  recipeDetails: {},
  detailsHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
    paddingBottom: '15px',
    borderBottom: '2px solid #f0f0f0',
  },
  closeButton: {
    background: 'none',
    border: 'none',
    fontSize: '24px',
    color: '#95a5a6',
    cursor: 'pointer',
  },
  detailsDescription: {
    fontSize: '15px',
    color: '#7f8c8d',
    marginBottom: '20px',
  },
  detailsSection: {
    marginBottom: '25px',
  },
  detailsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)',
    gap: '15px',
  },
  detailItem: {
    display: 'flex',
    flexDirection: 'column',
    gap: '5px',
  },
  detailLabel: {
    fontSize: '12px',
    color: '#7f8c8d',
    fontWeight: '500',
  },
  detailValue: {
    fontSize: '16px',
    color: '#2c3e50',
  },
  nutritionGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '15px',
  },
  nutritionCard: {
    textAlign: 'center',
    padding: '15px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
  },
  nutritionIcon: {
    fontSize: '32px',
    marginBottom: '8px',
  },
  nutritionValue: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: '4px',
  },
  nutritionLabel: {
    fontSize: '12px',
    color: '#7f8c8d',
  },
  ingredientsList: {
    listStyle: 'none',
    padding: 0,
    margin: 0,
  },
  ingredientListItem: {
    padding: '8px 0',
    borderBottom: '1px solid #f0f0f0',
  },
  instructions: {
    lineHeight: '1.8',
  },
  instructionStep: {
    marginBottom: '10px',
    paddingLeft: '10px',
    borderLeft: '3px solid #3498db',
  },
  actionsSection: {
    display: 'flex',
    gap: '10px',
    marginTop: '20px',
  },
  editButton: {
    flex: 1,
    padding: '12px',
    backgroundColor: '#3498db',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '500',
    cursor: 'pointer',
  },
  deleteButton: {
    flex: 1,
    padding: '12px',
    backgroundColor: '#e74c3c',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '500',
    cursor: 'pointer',
  },
  addForm: {},
  formContent: {
    padding: '10px 0',
  },
  formGroup: {
    marginBottom: '20px',
  },
  formRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '15px',
  },
  formLabel: {
    display: 'block',
    fontSize: '14px',
    fontWeight: '500',
    color: '#2c3e50',
    marginBottom: '8px',
  },
  formInput: {
    width: '100%',
    padding: '10px',
    fontSize: '14px',
    border: '2px solid #e9ecef',
    borderRadius: '6px',
    outline: 'none',
  },
  ingredientsSection: {
    marginBottom: '20px',
    padding: '15px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
  },
  sectionTitle: {
    marginTop: 0,
    marginBottom: '15px',
    fontSize: '16px',
    color: '#2c3e50',
  },
  addIngredientRow: {
    display: 'flex',
    gap: '10px',
    marginBottom: '15px',
  },
  addIngredientButton: {
    padding: '10px 20px',
    backgroundColor: '#27ae60',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '14px',
    cursor: 'pointer',
    whiteSpace: 'nowrap',
  },
  ingredientItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '10px',
    backgroundColor: 'white',
    borderRadius: '6px',
    marginBottom: '8px',
  },
  removeIngredientButton: {
    background: 'none',
    border: 'none',
    color: '#e74c3c',
    fontSize: '18px',
    cursor: 'pointer',
  },
  emptyIngredients: {
    textAlign: 'center',
    padding: '20px',
    color: '#95a5a6',
    fontSize: '14px',
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
};

export default RecipesBrowser;