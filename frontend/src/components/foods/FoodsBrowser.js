import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_ENDPOINTS } from '../../config/api';

const FoodsBrowser = () => {
  const [foods, setFoods] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [selectedFood, setSelectedFood] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [showEditForm, setShowEditForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    category: 'FRUITS',
    calories_per_100g: '',
    protein_per_100g: '',
    carbs_per_100g: '',
    fat_per_100g: '',
  });

  const categories = [
    { value: 'ALL', label: 'Todas las Categorías' },
    { value: 'FRUITS', label: 'Frutas' },
    { value: 'VEGETABLES', label: 'Vegetales' },
    { value: 'PROTEINS', label: 'Proteínas' },
    { value: 'GRAINS', label: 'Granos' },
    { value: 'DAIRY', label: 'Lácteos' },
    { value: 'LEGUMES', label: 'Legumbres' },
    { value: 'NUTS_SEEDS', label: 'Nueces y Semillas' },
  ];

  useEffect(() => {
    fetchFoods();
  }, []);

  const fetchFoods = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(API_ENDPOINTS.FOODS);
      setFoods(response.data);
    } catch (err) {
      setError('Error al cargar alimentos: ' + err.message);
      console.error('Error fetching foods:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredFoods = foods.filter(food => {
    const matchesSearch = food.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'ALL' || food.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleFoodClick = (food) => {
    setSelectedFood(food);
    setShowAddForm(false);
    setShowEditForm(false);
  };

  const handleAddNew = () => {
    setSelectedFood(null);
    setShowAddForm(true);
    setShowEditForm(false);
    setFormData({
      name: '',
      category: 'FRUITS',
      calories_per_100g: '',
      protein_per_100g: '',
      carbs_per_100g: '',
      fat_per_100g: '',
    });
  };

  const handleEdit = () => {
    if (selectedFood) {
      setShowEditForm(true);
      setShowAddForm(false);
      setFormData({
        name: selectedFood.name,
        category: selectedFood.category,
        calories_per_100g: selectedFood.calories_per_100g,
        protein_per_100g: selectedFood.protein_per_100g,
        carbs_per_100g: selectedFood.carbs_per_100g,
        fat_per_100g: selectedFood.fat_per_100g,
      });
    }
  };

  const handleCloseDetails = () => {
    setSelectedFood(null);
    setShowAddForm(false);
    setShowEditForm(false);
  };

  const handleFormChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSaveNew = async () => {
    try {
      // En un entorno real, esto haría un POST al backend
      const newFood = {
        id: foods.length + 1,
        ...formData,
        status: 'APPROVED',
        calories_per_100g: parseFloat(formData.calories_per_100g) || 0,
        protein_per_100g: parseFloat(formData.protein_per_100g) || 0,
        carbs_per_100g: parseFloat(formData.carbs_per_100g) || 0,
        fat_per_100g: parseFloat(formData.fat_per_100g) || 0,
      };

      // Agregar al estado local
      setFoods([...foods, newFood]);

      // Mostrar el nuevo alimento
      setSelectedFood(newFood);
      setShowAddForm(false);

      alert('✅ Alimento agregado exitosamente!');
    } catch (err) {
      alert('❌ Error al guardar: ' + err.message);
    }
  };

  const handleSaveEdit = async () => {
    try {
      // En un entorno real, esto haría un PUT al backend
      const updatedFood = {
        ...selectedFood,
        ...formData,
        calories_per_100g: parseFloat(formData.calories_per_100g) || 0,
        protein_per_100g: parseFloat(formData.protein_per_100g) || 0,
        carbs_per_100g: parseFloat(formData.carbs_per_100g) || 0,
        fat_per_100g: parseFloat(formData.fat_per_100g) || 0,
      };

      // Actualizar en el estado local
      setFoods(foods.map(f => f.id === selectedFood.id ? updatedFood : f));

      // Actualizar el alimento seleccionado
      setSelectedFood(updatedFood);
      setShowEditForm(false);

      alert('✅ Alimento actualizado exitosamente!');
    } catch (err) {
      alert('❌ Error al actualizar: ' + err.message);
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`¿Estás seguro de eliminar "${selectedFood.name}"?`)) {
      try {
        // En un entorno real, esto haría un DELETE al backend
        setFoods(foods.filter(f => f.id !== selectedFood.id));
        setSelectedFood(null);
        alert('✅ Alimento eliminado exitosamente!');
      } catch (err) {
        alert('❌ Error al eliminar: ' + err.message);
      }
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>🥗 Gestión de Alimentos</h1>
        <p style={styles.subtitle}>Base de datos de alimentos con información nutricional completa</p>
      </div>

      {/* Search and Filter Section */}
      <div style={styles.searchSection}>
        <div style={styles.searchBar}>
          <input
            type="text"
            placeholder="🔍 Buscar alimentos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={styles.searchInput}
          />
        </div>

        <div style={styles.filterSection}>
          <label style={styles.filterLabel}>Categoría:</label>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            style={styles.select}
          >
            {categories.map(cat => (
              <option key={cat.value} value={cat.value}>
                {cat.label}
              </option>
            ))}
          </select>
        </div>

        <button onClick={handleAddNew} style={styles.addButton}>
          ➕ Agregar Nuevo Alimento
        </button>
      </div>

      {/* Main Content */}
      <div style={styles.mainContent}>
        {/* Foods List */}
        <div style={styles.foodsList}>
          <div style={styles.listHeader}>
            <h3>Alimentos ({filteredFoods.length})</h3>
            <button onClick={fetchFoods} style={styles.refreshButton}>
              🔄 Actualizar
            </button>
          </div>

          {loading && (
            <div style={styles.loadingMessage}>
              Cargando alimentos...
            </div>
          )}

          {error && (
            <div style={styles.errorMessage}>
              {error}
            </div>
          )}

          {!loading && !error && filteredFoods.length === 0 && (
            <div style={styles.emptyMessage}>
              No se encontraron alimentos
            </div>
          )}

          {!loading && !error && filteredFoods.map(food => (
            <div
              key={food.id}
              style={{
                ...styles.foodCard,
                ...(selectedFood?.id === food.id ? styles.selectedFoodCard : {})
              }}
              onClick={() => handleFoodClick(food)}
            >
              <div style={styles.foodCardHeader}>
                <h4 style={styles.foodName}>{food.name}</h4>
                <span style={styles.foodCategory}>
                  {categories.find(c => c.value === food.category)?.label || food.category}
                </span>
              </div>
              <div style={styles.foodCardStats}>
                <span>🔥 {food.calories_per_100g} kcal</span>
                <span>🥩 {food.protein_per_100g}g proteína</span>
                <span>🍞 {food.carbs_per_100g}g carbos</span>
                <span>🥑 {food.fat_per_100g}g grasa</span>
              </div>
            </div>
          ))}
        </div>

        {/* Details Panel */}
        <div style={styles.detailsPanel}>
          {!selectedFood && !showAddForm && (
            <div style={styles.emptyDetails}>
              <h3>Selecciona un alimento</h3>
              <p>Haz clic en un alimento de la lista para ver sus detalles completos</p>
            </div>
          )}

          {selectedFood && !showAddForm && !showEditForm && (
            <div style={styles.foodDetails}>
              <div style={styles.detailsHeader}>
                <h2>{selectedFood.name}</h2>
                <button onClick={handleCloseDetails} style={styles.closeButton}>
                  ✕
                </button>
              </div>

              <div style={styles.detailsContent}>
                <div style={styles.detailsSection}>
                  <h3>Información General</h3>
                  <div style={styles.detailsGrid}>
                    <div style={styles.detailItem}>
                      <span style={styles.detailLabel}>Categoría:</span>
                      <span style={styles.detailValue}>
                        {categories.find(c => c.value === selectedFood.category)?.label}
                      </span>
                    </div>
                    <div style={styles.detailItem}>
                      <span style={styles.detailLabel}>Estado:</span>
                      <span style={{
                        ...styles.detailValue,
                        ...styles.statusBadge,
                        backgroundColor: selectedFood.status === 'APPROVED' ? '#27ae60' : '#f39c12'
                      }}>
                        {selectedFood.status}
                      </span>
                    </div>
                  </div>
                </div>

                <div style={styles.detailsSection}>
                  <h3>Información Nutricional (por 100g)</h3>
                  <div style={styles.nutritionGrid}>
                    <div style={styles.nutritionCard}>
                      <div style={styles.nutritionIcon}>🔥</div>
                      <div style={styles.nutritionValue}>{selectedFood.calories_per_100g}</div>
                      <div style={styles.nutritionLabel}>Calorías</div>
                    </div>
                    <div style={styles.nutritionCard}>
                      <div style={styles.nutritionIcon}>🥩</div>
                      <div style={styles.nutritionValue}>{selectedFood.protein_per_100g}g</div>
                      <div style={styles.nutritionLabel}>Proteínas</div>
                    </div>
                    <div style={styles.nutritionCard}>
                      <div style={styles.nutritionIcon}>🍞</div>
                      <div style={styles.nutritionValue}>{selectedFood.carbs_per_100g}g</div>
                      <div style={styles.nutritionLabel}>Carbohidratos</div>
                    </div>
                    <div style={styles.nutritionCard}>
                      <div style={styles.nutritionIcon}>🥑</div>
                      <div style={styles.nutritionValue}>{selectedFood.fat_per_100g}g</div>
                      <div style={styles.nutritionLabel}>Grasas</div>
                    </div>
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
            </div>
          )}

          {showAddForm && (
            <div style={styles.addForm}>
              <div style={styles.detailsHeader}>
                <h2>➕ Agregar Nuevo Alimento</h2>
                <button onClick={handleCloseDetails} style={styles.closeButton}>
                  ✕
                </button>
              </div>

              <div style={styles.formContent}>
                <div style={styles.formGroup}>
                  <label style={styles.formLabel}>Nombre del Alimento</label>
                  <input
                    type="text"
                    style={styles.formInput}
                    placeholder="Ej: Manzana"
                    value={formData.name}
                    onChange={(e) => handleFormChange('name', e.target.value)}
                  />
                </div>

                <div style={styles.formGroup}>
                  <label style={styles.formLabel}>Categoría</label>
                  <select
                    style={styles.formInput}
                    value={formData.category}
                    onChange={(e) => handleFormChange('category', e.target.value)}
                  >
                    {categories.filter(c => c.value !== 'ALL').map(cat => (
                      <option key={cat.value} value={cat.value}>
                        {cat.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div style={styles.formRow}>
                  <div style={styles.formGroup}>
                    <label style={styles.formLabel}>Calorías (kcal/100g)</label>
                    <input
                      type="number"
                      style={styles.formInput}
                      placeholder="52"
                      value={formData.calories_per_100g}
                      onChange={(e) => handleFormChange('calories_per_100g', e.target.value)}
                    />
                  </div>
                  <div style={styles.formGroup}>
                    <label style={styles.formLabel}>Proteínas (g/100g)</label>
                    <input
                      type="number"
                      style={styles.formInput}
                      placeholder="0.3"
                      step="0.1"
                      value={formData.protein_per_100g}
                      onChange={(e) => handleFormChange('protein_per_100g', e.target.value)}
                    />
                  </div>
                </div>

                <div style={styles.formRow}>
                  <div style={styles.formGroup}>
                    <label style={styles.formLabel}>Carbohidratos (g/100g)</label>
                    <input
                      type="number"
                      style={styles.formInput}
                      placeholder="14.0"
                      step="0.1"
                      value={formData.carbs_per_100g}
                      onChange={(e) => handleFormChange('carbs_per_100g', e.target.value)}
                    />
                  </div>
                  <div style={styles.formGroup}>
                    <label style={styles.formLabel}>Grasas (g/100g)</label>
                    <input
                      type="number"
                      style={styles.formInput}
                      placeholder="0.2"
                      step="0.1"
                      value={formData.fat_per_100g}
                      onChange={(e) => handleFormChange('fat_per_100g', e.target.value)}
                    />
                  </div>
                </div>

                <div style={styles.formActions}>
                  <button style={styles.saveButton} onClick={handleSaveNew}>
                    💾 Guardar Alimento
                  </button>
                  <button style={styles.cancelButton} onClick={handleCloseDetails}>
                    ❌ Cancelar
                  </button>
                </div>
              </div>
            </div>
          )}

          {showEditForm && (
            <div style={styles.addForm}>
              <div style={styles.detailsHeader}>
                <h2>✏️ Editar Alimento</h2>
                <button onClick={handleCloseDetails} style={styles.closeButton}>
                  ✕
                </button>
              </div>

              <div style={styles.formContent}>
                <div style={styles.formGroup}>
                  <label style={styles.formLabel}>Nombre del Alimento</label>
                  <input
                    type="text"
                    style={styles.formInput}
                    placeholder="Ej: Manzana"
                    value={formData.name}
                    onChange={(e) => handleFormChange('name', e.target.value)}
                  />
                </div>

                <div style={styles.formGroup}>
                  <label style={styles.formLabel}>Categoría</label>
                  <select
                    style={styles.formInput}
                    value={formData.category}
                    onChange={(e) => handleFormChange('category', e.target.value)}
                  >
                    {categories.filter(c => c.value !== 'ALL').map(cat => (
                      <option key={cat.value} value={cat.value}>
                        {cat.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div style={styles.formRow}>
                  <div style={styles.formGroup}>
                    <label style={styles.formLabel}>Calorías (kcal/100g)</label>
                    <input
                      type="number"
                      style={styles.formInput}
                      placeholder="52"
                      value={formData.calories_per_100g}
                      onChange={(e) => handleFormChange('calories_per_100g', e.target.value)}
                    />
                  </div>
                  <div style={styles.formGroup}>
                    <label style={styles.formLabel}>Proteínas (g/100g)</label>
                    <input
                      type="number"
                      style={styles.formInput}
                      placeholder="0.3"
                      step="0.1"
                      value={formData.protein_per_100g}
                      onChange={(e) => handleFormChange('protein_per_100g', e.target.value)}
                    />
                  </div>
                </div>

                <div style={styles.formRow}>
                  <div style={styles.formGroup}>
                    <label style={styles.formLabel}>Carbohidratos (g/100g)</label>
                    <input
                      type="number"
                      style={styles.formInput}
                      placeholder="14.0"
                      step="0.1"
                      value={formData.carbs_per_100g}
                      onChange={(e) => handleFormChange('carbs_per_100g', e.target.value)}
                    />
                  </div>
                  <div style={styles.formGroup}>
                    <label style={styles.formLabel}>Grasas (g/100g)</label>
                    <input
                      type="number"
                      style={styles.formInput}
                      placeholder="0.2"
                      step="0.1"
                      value={formData.fat_per_100g}
                      onChange={(e) => handleFormChange('fat_per_100g', e.target.value)}
                    />
                  </div>
                </div>

                <div style={styles.formActions}>
                  <button style={styles.saveButton} onClick={handleSaveEdit}>
                    💾 Actualizar Alimento
                  </button>
                  <button style={styles.cancelButton} onClick={handleCloseDetails}>
                    ❌ Cancelar
                  </button>
                </div>
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
  foodsList: {
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
  foodCard: {
    padding: '15px',
    marginBottom: '10px',
    border: '2px solid #f0f0f0',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'all 0.2s',
  },
  selectedFoodCard: {
    borderColor: '#3498db',
    backgroundColor: '#f0f8ff',
  },
  foodCardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '10px',
  },
  foodName: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#2c3e50',
    margin: 0,
  },
  foodCategory: {
    fontSize: '12px',
    padding: '4px 8px',
    backgroundColor: '#e9ecef',
    borderRadius: '4px',
    color: '#495057',
  },
  foodCardStats: {
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
  foodDetails: {},
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
  detailsContent: {},
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
  statusBadge: {
    display: 'inline-block',
    padding: '4px 12px',
    borderRadius: '4px',
    color: 'white',
    fontSize: '12px',
    fontWeight: '600',
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
    gridTemplateColumns: 'repeat(2, 1fr)',
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

export default FoodsBrowser;