import React, { useState, useEffect } from 'react';
import axios from 'axios';

const RecipeRating = ({ recipeId, currentUser, onRatingUpdate }) => {
  const [ratings, setRatings] = useState([]);
  const [stats, setStats] = useState(null);
  const [userRating, setUserRating] = useState(null);
  const [newRating, setNewRating] = useState(5);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [showRatingForm, setShowRatingForm] = useState(false);

  useEffect(() => {
    if (recipeId) {
      fetchRatings();
      fetchStats();
    }
  }, [recipeId]);

  const fetchRatings = async () => {
    try {
      const response = await axios.get(`http://localhost:8001/api/v1/recipes/${recipeId}/ratings`);
      setRatings(response.data);
      
      // Find user's existing rating
      if (currentUser) {
        const existingRating = response.data.find(r => r.user_id === currentUser.id);
        if (existingRating) {
          setUserRating(existingRating);
          setNewRating(existingRating.rating);
          setNewComment(existingRating.comment || '');
        }
      }
    } catch (error) {
      console.error('Error fetching ratings:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`http://localhost:8001/api/v1/recipes/${recipeId}/rating-stats`);
      setStats(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching rating stats:', error);
      setLoading(false);
    }
  };

  const submitRating = async () => {
    if (!currentUser) {
      alert('Debes iniciar sesión para calificar recetas');
      return;
    }

    setSubmitting(true);
    try {
      const response = await axios.post(
        `http://localhost:8001/api/v1/recipes/${recipeId}/ratings`,
        {
          rating: newRating,
          comment: newComment.trim() || null
        },
        {
          headers: {
            Authorization: `Bearer ${currentUser.token}` // Assuming token is stored
          }
        }
      );

      setUserRating(response.data);
      setShowRatingForm(false);
      
      // Refresh data
      await fetchRatings();
      await fetchStats();
      
      if (onRatingUpdate) {
        onRatingUpdate(response.data);
      }

      alert(userRating ? 'Rating actualizado exitosamente' : 'Rating enviado exitosamente');
    } catch (error) {
      console.error('Error submitting rating:', error);
      alert('Error al enviar calificación. Intenta de nuevo.');
    } finally {
      setSubmitting(false);
    }
  };

  const markHelpful = async (ratingId) => {
    if (!currentUser) return;

    try {
      await axios.post(
        `http://localhost:8001/api/v1/recipes/ratings/${ratingId}/helpful`,
        {},
        {
          headers: {
            Authorization: `Bearer ${currentUser.token}`
          }
        }
      );
      
      // Refresh ratings
      await fetchRatings();
    } catch (error) {
      console.error('Error marking rating as helpful:', error);
    }
  };

  const deleteRating = async (ratingId) => {
    if (!confirm('¿Estás seguro de que quieres eliminar tu calificación?')) {
      return;
    }

    try {
      await axios.delete(
        `http://localhost:8001/api/v1/recipes/ratings/${ratingId}`,
        {
          headers: {
            Authorization: `Bearer ${currentUser.token}`
          }
        }
      );

      setUserRating(null);
      setNewRating(5);
      setNewComment('');
      
      // Refresh data
      await fetchRatings();
      await fetchStats();
      
      alert('Calificación eliminada exitosamente');
    } catch (error) {
      console.error('Error deleting rating:', error);
      alert('Error al eliminar calificación');
    }
  };

  const renderStars = (rating, interactive = false, onStarClick = null) => {
    return (
      <div style={styles.starsContainer}>
        {[1, 2, 3, 4, 5].map(star => (
          <span
            key={star}
            style={{
              ...styles.star,
              color: star <= rating ? '#ffc107' : '#e4e5e9',
              cursor: interactive ? 'pointer' : 'default'
            }}
            onClick={interactive ? () => onStarClick(star) : undefined}
          >
            ★
          </span>
        ))}
        {!interactive && (
          <span style={styles.ratingNumber}>({rating.toFixed(1)})</span>
        )}
      </div>
    );
  };

  const renderRatingDistribution = () => {
    if (!stats) return null;

    const maxCount = Math.max(...Object.values(stats.rating_distribution));

    return (
      <div style={styles.distributionContainer}>
        <h4>Distribución de Calificaciones</h4>
        {[5, 4, 3, 2, 1].map(star => (
          <div key={star} style={styles.distributionRow}>
            <span style={styles.distributionLabel}>{star} ★</span>
            <div style={styles.distributionBarContainer}>
              <div
                style={{
                  ...styles.distributionBar,
                  width: maxCount > 0 ? `${(stats.rating_distribution[star] / maxCount) * 100}%` : '0%'
                }}
              />
            </div>
            <span style={styles.distributionCount}>{stats.rating_distribution[star]}</span>
          </div>
        ))}
      </div>
    );
  };

  if (loading) {
    return <div style={styles.loading}>Cargando calificaciones...</div>;
  }

  return (
    <div style={styles.container}>
      {/* Rating Summary */}
      <div style={styles.summarySection}>
        <div style={styles.summaryHeader}>
          <h3>Calificaciones y Comentarios</h3>
          {stats && (
            <div style={styles.averageRating}>
              {renderStars(stats.average_rating)}
              <span style={styles.totalRatings}>
                {stats.total_ratings} calificaciones
              </span>
            </div>
          )}
        </div>
        
        {stats && renderRatingDistribution()}
      </div>

      {/* User's Rating Section */}
      {currentUser && (
        <div style={styles.userRatingSection}>
          {userRating ? (
            <div style={styles.existingRating}>
              <h4>Tu Calificación</h4>
              <div style={styles.userRatingDisplay}>
                {renderStars(userRating.rating)}
                <span style={styles.userRatingDate}>
                  {new Date(userRating.created_at).toLocaleDateString()}
                </span>
              </div>
              {userRating.comment && (
                <p style={styles.userComment}>"{userRating.comment}"</p>
              )}
              <div style={styles.userRatingActions}>
                <button
                  style={styles.editButton}
                  onClick={() => setShowRatingForm(true)}
                >
                  Editar
                </button>
                <button
                  style={styles.deleteButton}
                  onClick={() => deleteRating(userRating.id)}
                >
                  Eliminar
                </button>
              </div>
            </div>
          ) : (
            <div style={styles.noRating}>
              <p>¿Qué te pareció esta receta?</p>
              <button
                style={styles.rateButton}
                onClick={() => setShowRatingForm(true)}
              >
                Calificar Receta
              </button>
            </div>
          )}

          {/* Rating Form Modal */}
          {showRatingForm && (
            <div style={styles.modalOverlay}>
              <div style={styles.modal}>
                <div style={styles.modalHeader}>
                  <h3>{userRating ? 'Editar Calificación' : 'Calificar Receta'}</h3>
                  <button
                    style={styles.closeButton}
                    onClick={() => setShowRatingForm(false)}
                  >
                    ✕
                  </button>
                </div>
                
                <div style={styles.modalBody}>
                  <div style={styles.ratingInput}>
                    <label>Tu calificación:</label>
                    {renderStars(newRating, true, setNewRating)}
                  </div>
                  
                  <div style={styles.commentInput}>
                    <label>Comentario (opcional):</label>
                    <textarea
                      style={styles.textarea}
                      value={newComment}
                      onChange={(e) => setNewComment(e.target.value)}
                      placeholder="Comparte tu experiencia con esta receta..."
                      rows={4}
                      maxLength={1000}
                    />
                    <div style={styles.charCount}>
                      {newComment.length}/1000 caracteres
                    </div>
                  </div>
                  
                  <div style={styles.modalActions}>
                    <button
                      style={styles.cancelButton}
                      onClick={() => setShowRatingForm(false)}
                      disabled={submitting}
                    >
                      Cancelar
                    </button>
                    <button
                      style={styles.submitButton}
                      onClick={submitRating}
                      disabled={submitting}
                    >
                      {submitting ? 'Enviando...' : (userRating ? 'Actualizar' : 'Enviar')}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* All Ratings List */}
      <div style={styles.ratingsSection}>
        <h4>Todas las Calificaciones ({ratings.length})</h4>
        
        {ratings.length === 0 ? (
          <div style={styles.noRatings}>
            <p>Sé el primero en calificar esta receta!</p>
          </div>
        ) : (
          <div style={styles.ratingsList}>
            {ratings.map(rating => (
              <div key={rating.id} style={styles.ratingItem}>
                <div style={styles.ratingHeader}>
                  <div style={styles.ratingUser}>
                    <strong>{rating.user_name}</strong>
                    <span style={styles.userRole}>({rating.user_role})</span>
                  </div>
                  <div style={styles.ratingDate}>
                    {new Date(rating.created_at).toLocaleDateString()}
                  </div>
                </div>
                
                <div style={styles.ratingContent}>
                  {renderStars(rating.rating)}
                  {rating.comment && (
                    <p style={styles.ratingComment}>"{rating.comment}"</p>
                  )}
                </div>
                
                <div style={styles.ratingActions}>
                  <button
                    style={styles.helpfulButton}
                    onClick={() => markHelpful(rating.id)}
                    disabled={!currentUser}
                  >
                    👍 Útil ({rating.helpful_votes})
                  </button>
                  {rating.updated_at && rating.updated_at !== rating.created_at && (
                    <span style={styles.editedIndicator}>
                      (Editado el {new Date(rating.updated_at).toLocaleDateString()})
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Most Helpful Comments */}
      {stats && stats.most_helpful_comments.length > 0 && (
        <div style={styles.helpfulSection}>
          <h4>Comentarios Más Útiles</h4>
          <div style={styles.helpfulComments}>
            {stats.most_helpful_comments.map(rating => (
              <div key={rating.id} style={styles.helpfulComment}>
                <div style={styles.helpfulHeader}>
                  {renderStars(rating.rating)}
                  <span style={styles.helpfulVotes}>
                    👍 {rating.helpful_votes} personas encontraron esto útil
                  </span>
                </div>
                <p style={styles.helpfulText}>"{rating.comment}"</p>
                <div style={styles.helpfulAuthor}>
                  - {rating.user_name} ({rating.user_role})
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif',
  },
  loading: {
    textAlign: 'center',
    padding: '40px',
    color: '#666',
  },
  summarySection: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '20px',
  },
  summaryHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
    flexWrap: 'wrap',
    gap: '15px',
  },
  averageRating: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  totalRatings: {
    color: '#666',
    fontSize: '14px',
  },
  starsContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: '2px',
  },
  star: {
    fontSize: '20px',
    transition: 'color 0.2s',
  },
  ratingNumber: {
    marginLeft: '8px',
    color: '#666',
    fontSize: '14px',
  },
  distributionContainer: {
    marginTop: '20px',
  },
  distributionRow: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '8px',
    gap: '10px',
  },
  distributionLabel: {
    width: '30px',
    fontSize: '14px',
  },
  distributionBarContainer: {
    flex: 1,
    height: '6px',
    backgroundColor: '#f0f0f0',
    borderRadius: '3px',
    overflow: 'hidden',
  },
  distributionBar: {
    height: '100%',
    backgroundColor: '#ffc107',
    transition: 'width 0.3s ease',
  },
  distributionCount: {
    width: '30px',
    textAlign: 'right',
    fontSize: '14px',
    color: '#666',
  },
  userRatingSection: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '20px',
  },
  existingRating: {
    borderLeft: '4px solid #28a745',
    paddingLeft: '15px',
  },
  userRatingDisplay: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
    marginBottom: '10px',
  },
  userRatingDate: {
    color: '#666',
    fontSize: '14px',
  },
  userComment: {
    fontStyle: 'italic',
    color: '#555',
    marginBottom: '15px',
  },
  userRatingActions: {
    display: 'flex',
    gap: '10px',
  },
  editButton: {
    padding: '6px 12px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  deleteButton: {
    padding: '6px 12px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  noRating: {
    textAlign: 'center',
    padding: '20px',
  },
  rateButton: {
    padding: '10px 20px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: '500',
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
  },
  modal: {
    backgroundColor: 'white',
    borderRadius: '12px',
    maxWidth: '500px',
    width: '90%',
    maxHeight: '80vh',
    overflow: 'auto',
  },
  modalHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '20px 30px',
    borderBottom: '1px solid #eee',
  },
  closeButton: {
    background: 'none',
    border: 'none',
    fontSize: '24px',
    cursor: 'pointer',
    color: '#666',
  },
  modalBody: {
    padding: '30px',
  },
  ratingInput: {
    marginBottom: '20px',
  },
  commentInput: {
    marginBottom: '20px',
  },
  textarea: {
    width: '100%',
    padding: '10px',
    borderRadius: '4px',
    border: '1px solid #ddd',
    fontSize: '14px',
    fontFamily: 'inherit',
    resize: 'vertical',
  },
  charCount: {
    textAlign: 'right',
    fontSize: '12px',
    color: '#666',
    marginTop: '5px',
  },
  modalActions: {
    display: 'flex',
    justifyContent: 'flex-end',
    gap: '10px',
  },
  cancelButton: {
    padding: '10px 20px',
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  submitButton: {
    padding: '10px 20px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  ratingsSection: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    marginBottom: '20px',
  },
  noRatings: {
    textAlign: 'center',
    padding: '40px',
    color: '#666',
  },
  ratingsList: {
    marginTop: '20px',
  },
  ratingItem: {
    borderBottom: '1px solid #eee',
    paddingBottom: '20px',
    marginBottom: '20px',
  },
  ratingHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '10px',
  },
  ratingUser: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  userRole: {
    color: '#666',
    fontSize: '14px',
  },
  ratingDate: {
    color: '#666',
    fontSize: '14px',
  },
  ratingContent: {
    marginBottom: '10px',
  },
  ratingComment: {
    marginTop: '10px',
    color: '#555',
    fontStyle: 'italic',
  },
  ratingActions: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
  },
  helpfulButton: {
    padding: '4px 8px',
    backgroundColor: '#f8f9fa',
    border: '1px solid #dee2e6',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '12px',
    color: '#495057',
    transition: 'background-color 0.2s',
  },
  editedIndicator: {
    fontSize: '12px',
    color: '#666',
    fontStyle: 'italic',
  },
  helpfulSection: {
    backgroundColor: '#f8f9fa',
    padding: '30px',
    borderRadius: '12px',
    border: '1px solid #e9ecef',
  },
  helpfulComments: {
    marginTop: '20px',
  },
  helpfulComment: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    marginBottom: '15px',
    border: '1px solid #dee2e6',
  },
  helpfulHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '10px',
  },
  helpfulVotes: {
    color: '#28a745',
    fontSize: '14px',
    fontWeight: '500',
  },
  helpfulText: {
    color: '#555',
    fontStyle: 'italic',
    marginBottom: '10px',
  },
  helpfulAuthor: {
    textAlign: 'right',
    color: '#666',
    fontSize: '14px',
  },
};

export default RecipeRating;