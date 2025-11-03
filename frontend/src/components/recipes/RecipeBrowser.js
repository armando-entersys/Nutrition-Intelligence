import React, { useState, useEffect } from 'react';
import axios from 'axios';
import RecipeRating from './RecipeRating';
import { API_BASE_URL } from '../../config/api';

const RecipeBrowser = ({ currentUser }) => {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [showRatingModal, setShowRatingModal] = useState(false);
  
  // Filters
  const [filters, setFilters] = useState({
    meal_type: '',
    difficulty: '',
    min_rating: '',
    cuisine_type: '',
    sort_by: 'created_at',
    sort_order: 'desc'
  });

  const mealTypes = [
    { value: 'breakfast', label: 'Desayuno' },
    { value: 'morning_snack', label: 'Colación Matutina' },
    { value: 'lunch', label: 'Almuerzo' },
    { value: 'afternoon_snack', label: 'Colación Vespertina' },
    { value: 'dinner', label: 'Cena' },
    { value: 'evening_snack', label: 'Colación Nocturna' }
  ];

  const difficulties = [
    { value: 'very_easy', label: 'Muy Fácil' },
    { value: 'easy', label: 'Fácil' },
    { value: 'medium', label: 'Intermedio' },
    { value: 'hard', label: 'Difícil' },
    { value: 'very_hard', label: 'Muy Difícil' }
  ];

  const sortOptions = [
    { value: 'created_at', label: 'Fecha de Creación' },
    { value: 'rating_average', label: 'Calificación' },
    { value: 'view_count', label: 'Popularidad' },
    { value: 'title', label: 'Nombre' }
  ];

  useEffect(() => {
    fetchRecipes();
  }, [filters]);

  const fetchRecipes = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      
      // Only add non-empty filters
      Object.entries(filters).forEach(([key, value]) => {
        if (value) {
          params.append(key, value);
        }
      });

      const response = await axios.get(`${API_BASE_URL}/api/v1/recipes?${params}`);
      setRecipes(response.data);
    } catch (error) {
      console.error('Error fetching recipes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const getDifficultyLabel = (difficulty) => {
    const diff = difficulties.find(d => d.value === difficulty);
    return diff ? diff.label : difficulty;
  };

  const getMealTypeLabels = (mealTypes) => {
    if (!mealTypes) return '';
    return mealTypes.map(mt => {
      const type = mealTypes.find(t => t.value === mt);
      return type ? type.label : mt;
    }).join(', ');
  };

  const renderStars = (rating, count) => {
    if (!rating) return <span style={styles.noRating}>Sin calificar</span>;
    
    return (
      <div style={styles.starsContainer}>
        {[1, 2, 3, 4, 5].map(star => (
          <span
            key={star}
            style={{
              ...styles.star,
              color: star <= rating ? '#ffc107' : '#e4e5e9'
            }}
          >
            ★
          </span>
        ))}
        <span style={styles.ratingInfo}>
          {rating.toFixed(1)} ({count} calificaciones)
        </span>
      </div>
    );
  };

  const openRatingModal = (recipe) => {
    setSelectedRecipe(recipe);
    setShowRatingModal(true);
  };

  const closeRatingModal = () => {
    setSelectedRecipe(null);
    setShowRatingModal(false);
    // Refresh recipes to get updated ratings
    fetchRecipes();
  };

  if (loading) {
    return <div style={styles.loading}>Cargando recetas...</div>;
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1>🍽️ Explorar Recetas</h1>
        <p>Descubre y califica recetas de nuestra comunidad nutricional</p>
      </div>

      {/* Filters */}
      <div style={styles.filtersSection}>
        <h3>Filtros</h3>
        <div style={styles.filtersGrid}>
          <div style={styles.filterGroup}>
            <label>Tipo de Comida:</label>
            <select
              value={filters.meal_type}
              onChange={(e) => handleFilterChange('meal_type', e.target.value)}
              style={styles.select}
            >
              <option value="">Todos</option>
              {mealTypes.map(type => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </select>
          </div>

          <div style={styles.filterGroup}>
            <label>Dificultad:</label>
            <select
              value={filters.difficulty}
              onChange={(e) => handleFilterChange('difficulty', e.target.value)}
              style={styles.select}
            >
              <option value="">Todas</option>
              {difficulties.map(diff => (
                <option key={diff.value} value={diff.value}>
                  {diff.label}
                </option>
              ))}
            </select>
          </div>

          <div style={styles.filterGroup}>
            <label>Calificación Mínima:</label>
            <select
              value={filters.min_rating}
              onChange={(e) => handleFilterChange('min_rating', e.target.value)}
              style={styles.select}
            >
              <option value="">Cualquiera</option>
              <option value="4.5">4.5+ estrellas</option>
              <option value="4.0">4.0+ estrellas</option>
              <option value="3.5">3.5+ estrellas</option>
              <option value="3.0">3.0+ estrellas</option>
            </select>
          </div>

          <div style={styles.filterGroup}>
            <label>Ordenar por:</label>
            <select
              value={filters.sort_by}
              onChange={(e) => handleFilterChange('sort_by', e.target.value)}
              style={styles.select}
            >
              {sortOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div style={styles.filterGroup}>
            <label>Orden:</label>
            <select
              value={filters.sort_order}
              onChange={(e) => handleFilterChange('sort_order', e.target.value)}
              style={styles.select}
            >
              <option value="desc">Descendente</option>
              <option value="asc">Ascendente</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results */}
      <div style={styles.resultsSection}>
        <div style={styles.resultsHeader}>
          <h3>Resultados ({recipes.length} recetas)</h3>
        </div>

        {recipes.length === 0 ? (
          <div style={styles.noResults}>
            <p>No se encontraron recetas con los filtros seleccionados.</p>
          </div>
        ) : (
          <div style={styles.recipesGrid}>
            {recipes.map(recipe => (
              <div key={recipe.id} style={styles.recipeCard}>
                {recipe.image_url && (
                  <img 
                    src={recipe.image_url} 
                    alt={recipe.title}
                    style={styles.recipeImage}
                  />
                )}
                
                <div style={styles.recipeContent}>
                  <h4 style={styles.recipeTitle}>{recipe.title}</h4>
                  
                  <p style={styles.recipeDescription}>
                    {recipe.description || 'Sin descripción disponible'}
                  </p>

                  <div style={styles.recipeMetrics}>
                    <div style={styles.metric}>
                      <span style={styles.metricLabel}>👨‍🍳 Autor:</span>
                      <span>{recipe.author_type}</span>
                    </div>
                    
                    <div style={styles.metric}>
                      <span style={styles.metricLabel}>🍽️ Porciones:</span>
                      <span>{recipe.servings}</span>
                    </div>

                    {recipe.total_calories && (
                      <div style={styles.metric}>
                        <span style={styles.metricLabel}>🔥 Calorías:</span>
                        <span>{Math.round(recipe.calories_per_serving || recipe.total_calories)} por porción</span>
                      </div>
                    )}

                    <div style={styles.metric}>
                      <span style={styles.metricLabel}>⏱️ Dificultad:</span>
                      <span>{getDifficultyLabel(recipe.difficulty)}</span>
                    </div>

                    {recipe.prep_time_minutes && (
                      <div style={styles.metric}>
                        <span style={styles.metricLabel}>⏰ Prep:</span>
                        <span>{recipe.prep_time_minutes} min</span>
                      </div>
                    )}

                    <div style={styles.metric}>
                      <span style={styles.metricLabel}>👁️ Vistas:</span>
                      <span>{recipe.view_count}</span>
                    </div>
                  </div>

                  {recipe.dietary_tags && recipe.dietary_tags.length > 0 && (
                    <div style={styles.tags}>
                      {recipe.dietary_tags.map(tag => (
                        <span key={tag} style={styles.tag}>{tag}</span>
                      ))}
                    </div>
                  )}

                  <div style={styles.recipeRating}>
                    {renderStars(recipe.rating_average, recipe.rating_count)}
                  </div>

                  <div style={styles.recipeActions}>
                    <button 
                      style={styles.viewButton}
                      onClick={() => openRatingModal(recipe)}
                    >
                      Ver Detalle
                    </button>
                    
                    {currentUser && (
                      <button
                        style={styles.rateButton}
                        onClick={() => openRatingModal(recipe)}
                      >
                        ⭐ Calificar
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Rating Modal */}
      {showRatingModal && selectedRecipe && (
        <div style={styles.modalOverlay}>
          <div style={styles.modal}>
            <div style={styles.modalHeader}>
              <h2>{selectedRecipe.title}</h2>
              <button
                style={styles.closeButton}
                onClick={closeRatingModal}
              >
                ✕
              </button>
            </div>
            
            <div style={styles.modalBody}>
              <div style={styles.recipeDetailHeader}>
                {selectedRecipe.image_url && (
                  <img 
                    src={selectedRecipe.image_url} 
                    alt={selectedRecipe.title}
                    style={styles.modalRecipeImage}
                  />
                )}
                
                <div style={styles.recipeDetailInfo}>
                  <p style={styles.modalDescription}>
                    {selectedRecipe.description}
                  </p>
                  
                  <div style={styles.modalMetrics}>
                    <div>🍽️ {selectedRecipe.servings} porciones</div>
                    {selectedRecipe.total_calories && (
                      <div>🔥 {Math.round(selectedRecipe.calories_per_serving || selectedRecipe.total_calories)} cal/porción</div>
                    )}
                    <div>⏱️ {getDifficultyLabel(selectedRecipe.difficulty)}</div>
                    <div>👁️ {selectedRecipe.view_count} vistas</div>
                  </div>
                </div>
              </div>

              <RecipeRating
                recipeId={selectedRecipe.id}
                currentUser={currentUser}
                onRatingUpdate={() => {
                  // Refresh the recipe in the list
                  fetchRecipes();
                }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif',
  },
  loading: {
    textAlign: 'center',
    padding: '40px',
    color: '#666',
  },
  header: {
    textAlign: 'center',
    marginBottom: '30px',
  },
  filtersSection: {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '30px',
  },
  filtersGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '15px',
    marginTop: '15px',
  },
  filterGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '5px',
  },
  select: {
    padding: '8px',
    borderRadius: '4px',
    border: '1px solid #ddd',
    fontSize: '14px',
  },
  resultsSection: {
    marginBottom: '30px',
  },
  resultsHeader: {
    marginBottom: '20px',
  },
  noResults: {
    textAlign: 'center',
    padding: '40px',
    color: '#666',
    backgroundColor: 'white',
    borderRadius: '12px',
  },
  recipesGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
    gap: '20px',
  },
  recipeCard: {
    backgroundColor: 'white',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    overflow: 'hidden',
    transition: 'transform 0.2s, box-shadow 0.2s',
    ':hover': {
      transform: 'translateY(-2px)',
      boxShadow: '0 4px 20px rgba(0, 0, 0, 0.15)',
    },
  },
  recipeImage: {
    width: '100%',
    height: '200px',
    objectFit: 'cover',
  },
  recipeContent: {
    padding: '20px',
  },
  recipeTitle: {
    margin: '0 0 10px 0',
    color: '#2c3e50',
    fontSize: '18px',
  },
  recipeDescription: {
    color: '#666',
    fontSize: '14px',
    marginBottom: '15px',
    display: '-webkit-box',
    WebkitLineClamp: 2,
    WebkitBoxOrient: 'vertical',
    overflow: 'hidden',
  },
  recipeMetrics: {
    marginBottom: '15px',
  },
  metric: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '5px',
    fontSize: '14px',
  },
  metricLabel: {
    fontWeight: '500',
  },
  tags: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '5px',
    marginBottom: '15px',
  },
  tag: {
    padding: '2px 8px',
    backgroundColor: '#e9ecef',
    borderRadius: '12px',
    fontSize: '12px',
    color: '#495057',
  },
  recipeRating: {
    marginBottom: '15px',
  },
  starsContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: '2px',
  },
  star: {
    fontSize: '16px',
  },
  ratingInfo: {
    marginLeft: '8px',
    color: '#666',
    fontSize: '12px',
  },
  noRating: {
    color: '#999',
    fontSize: '14px',
  },
  recipeActions: {
    display: 'flex',
    gap: '10px',
  },
  viewButton: {
    flex: 1,
    padding: '8px 16px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  rateButton: {
    padding: '8px 16px',
    backgroundColor: '#ffc107',
    color: '#212529',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  modalOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
    padding: '20px',
  },
  modal: {
    backgroundColor: 'white',
    borderRadius: '12px',
    maxWidth: '900px',
    width: '100%',
    maxHeight: '90vh',
    overflow: 'auto',
  },
  modalHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '20px 30px',
    borderBottom: '1px solid #eee',
    position: 'sticky',
    top: 0,
    backgroundColor: 'white',
    zIndex: 1,
  },
  closeButton: {
    background: 'none',
    border: 'none',
    fontSize: '24px',
    cursor: 'pointer',
    color: '#666',
  },
  modalBody: {
    padding: '0',
  },
  recipeDetailHeader: {
    display: 'flex',
    padding: '20px 30px',
    gap: '20px',
    borderBottom: '1px solid #eee',
  },
  modalRecipeImage: {
    width: '200px',
    height: '150px',
    objectFit: 'cover',
    borderRadius: '8px',
  },
  recipeDetailInfo: {
    flex: 1,
  },
  modalDescription: {
    color: '#555',
    marginBottom: '15px',
  },
  modalMetrics: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '15px',
    fontSize: '14px',
    color: '#666',
  },
};

export default RecipeBrowser;