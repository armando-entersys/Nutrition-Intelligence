/**
 * Recordatorio 24 Horas - Food Diary Component
 * Permite a los pacientes registrar todo lo que consumen en un día
 */
import React, { useState, useEffect, useMemo } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  IconButton,
  Chip,
  Divider,
  Tabs,
  Tab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  Alert,
  LinearProgress,
  Autocomplete,
  InputAdornment,
  Stack,
  Tooltip,
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Search as SearchIcon,
  Restaurant as RestaurantIcon,
  LocalCafe as CoffeeIcon,
  Fastfood as FastfoodIcon,
  Analytics as AnalyticsIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  CalendarToday as CalendarIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';

// Tiempos de comida
const MEAL_TIMES = {
  desayuno: { label: 'Desayuno', icon: '🌅', color: '#FF9800' },
  colacion_am: { label: 'Colación AM', icon: '☕', color: '#8BC34A' },
  comida: { label: 'Comida', icon: '🍽️', color: '#F44336' },
  colacion_pm: { label: 'Colación PM', icon: '🍎', color: '#8BC34A' },
  cena: { label: 'Cena', icon: '🌙', color: '#3F51B5' },
};

const Recordatorio24Horas = () => {
  // Estados
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [currentMealTime, setCurrentMealTime] = useState('desayuno');
  const [foodEntries, setFoodEntries] = useState({
    desayuno: [],
    colacion_am: [],
    comida: [],
    colacion_pm: [],
    cena: [],
  });

  // Estados del diálogo de búsqueda
  const [searchDialogOpen, setSearchDialogOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedFood, setSelectedFood] = useState(null);
  const [portionSize, setPortionSize] = useState(1);

  // Estados de análisis
  const [dailySummary, setDailySummary] = useState({
    calories: 0,
    protein: 0,
    carbs: 0,
    fat: 0,
    fiber: 0,
  });
  const [adherenceScore, setAdherenceScore] = useState(null);

  // Metas diarias (simuladas - en producción vendrían del plan del paciente)
  const dailyGoals = {
    calories: 2000,
    protein: 150,
    carbs: 250,
    fat: 67,
    fiber: 30,
  };

  // ============================================================================
  // BÚSQUEDA DE ALIMENTOS
  // ============================================================================

  const searchFoods = async (query) => {
    if (query.length < 2) {
      setSearchResults([]);
      return;
    }

    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/foods/search`, {
        params: { q: query, limit: 20 }
      });
      setSearchResults(response.data);
    } catch (error) {
      console.error('Error searching foods:', error);
      // Fallback a datos mock si el backend no está disponible
      setSearchResults(getMockFoods(query));
    }
  };

  // Mock data para desarrollo
  const getMockFoods = (query) => {
    const mockFoods = [
      { id: 1, name: 'Tortilla de maíz', serving_size: 30, calories_per_serving: 64, protein_g: 1.5, carbs_g: 13.8, fat_g: 0.9, fiber_g: 1.5 },
      { id: 2, name: 'Frijoles negros cocidos', serving_size: 90, calories_per_serving: 114, protein_g: 7.6, carbs_g: 20.4, fat_g: 0.5, fiber_g: 7.5 },
      { id: 3, name: 'Aguacate hass', serving_size: 50, calories_per_serving: 80, protein_g: 1.0, carbs_g: 4.3, fat_g: 7.3, fiber_g: 3.4 },
      { id: 4, name: 'Pechuga de pollo sin piel', serving_size: 100, calories_per_serving: 165, protein_g: 31.0, carbs_g: 0, fat_g: 3.6, fiber_g: 0 },
      { id: 5, name: 'Arroz integral cocido', serving_size: 150, calories_per_serving: 165, protein_g: 3.5, carbs_g: 34.2, fat_g: 1.5, fiber_g: 2.8 },
    ];

    return mockFoods.filter(food =>
      food.name.toLowerCase().includes(query.toLowerCase())
    );
  };

  useEffect(() => {
    const debounce = setTimeout(() => {
      if (searchQuery) {
        searchFoods(searchQuery);
      }
    }, 300);

    return () => clearTimeout(debounce);
  }, [searchQuery]);

  // ============================================================================
  // MANEJO DE ALIMENTOS
  // ============================================================================

  const handleOpenSearchDialog = (mealTime) => {
    setCurrentMealTime(mealTime);
    setSearchDialogOpen(true);
    setSearchQuery('');
    setSelectedFood(null);
    setPortionSize(1);
  };

  const handleCloseSearchDialog = () => {
    setSearchDialogOpen(false);
    setSelectedFood(null);
    setPortionSize(1);
  };

  const handleAddFood = () => {
    if (!selectedFood) return;

    const newEntry = {
      id: Date.now(),
      food: selectedFood,
      portions: portionSize,
      totalCalories: selectedFood.calories_per_serving * portionSize,
      totalProtein: selectedFood.protein_g * portionSize,
      totalCarbs: selectedFood.carbs_g * portionSize,
      totalFat: selectedFood.fat_g * portionSize,
      totalFiber: selectedFood.fiber_g * portionSize,
      timestamp: new Date().toISOString(),
    };

    setFoodEntries(prev => ({
      ...prev,
      [currentMealTime]: [...prev[currentMealTime], newEntry]
    }));

    handleCloseSearchDialog();
  };

  const handleDeleteEntry = (mealTime, entryId) => {
    setFoodEntries(prev => ({
      ...prev,
      [mealTime]: prev[mealTime].filter(entry => entry.id !== entryId)
    }));
  };

  // ============================================================================
  // CÁLCULOS Y ANÁLISIS
  // ============================================================================

  useEffect(() => {
    // Calcular resumen diario
    let totals = {
      calories: 0,
      protein: 0,
      carbs: 0,
      fat: 0,
      fiber: 0,
    };

    Object.values(foodEntries).forEach(mealEntries => {
      mealEntries.forEach(entry => {
        totals.calories += entry.totalCalories;
        totals.protein += entry.totalProtein;
        totals.carbs += entry.totalCarbs;
        totals.fat += entry.totalFat;
        totals.fiber += entry.totalFiber;
      });
    });

    setDailySummary(totals);

    // Calcular adherencia
    const calorieAdherence = Math.min((totals.calories / dailyGoals.calories) * 100, 100);
    const proteinAdherence = Math.min((totals.protein / dailyGoals.protein) * 100, 100);
    const carbsAdherence = Math.min((totals.carbs / dailyGoals.carbs) * 100, 100);
    const fatAdherence = Math.min((totals.fat / dailyGoals.fat) * 100, 100);
    const fiberAdherence = Math.min((totals.fiber / dailyGoals.fiber) * 100, 100);

    const avgAdherence = (calorieAdherence + proteinAdherence + carbsAdherence + fatAdherence + fiberAdherence) / 5;

    setAdherenceScore({
      overall: avgAdherence,
      calories: calorieAdherence,
      protein: proteinAdherence,
      carbs: carbsAdherence,
      fat: fatAdherence,
      fiber: fiberAdherence,
    });
  }, [foodEntries]);

  const getAdherenceColor = (score) => {
    if (score >= 90) return '#4CAF50';
    if (score >= 70) return '#FF9800';
    return '#F44336';
  };

  const getAdherenceLevel = (score) => {
    if (score >= 90) return 'Excelente';
    if (score >= 70) return 'Buena';
    if (score >= 50) return 'Regular';
    return 'Baja';
  };

  // ============================================================================
  // RENDER
  // ============================================================================

  return (
    <Box sx={{ p: 3, maxWidth: 1400, mx: 'auto' }}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Paper sx={{ p: 3, mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
          <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold', mb: 1 }}>
            📋 Recordatorio 24 Horas
          </Typography>
          <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.9)' }}>
            Registra todo lo que consumes durante el día para analizar tu adherencia al plan
          </Typography>
        </Paper>
      </motion.div>

      {/* Selector de fecha */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <CalendarIcon sx={{ color: '#667eea', fontSize: 32 }} />
          </Grid>
          <Grid item xs>
            <TextField
              type="date"
              label="Fecha"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
        </Grid>
      </Paper>

      <Grid container spacing={3}>
        {/* Columna izquierda - Registro de alimentos */}
        <Grid item xs={12} md={8}>
          {/* Tiempos de comida */}
          {Object.entries(MEAL_TIMES).map(([mealTimeKey, mealTimeInfo]) => (
            <motion.div
              key={mealTimeKey}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <Paper sx={{ p: 3, mb: 3 }}>
                {/* Header del tiempo de comida */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="h5" sx={{ fontSize: 28 }}>
                      {mealTimeInfo.icon}
                    </Typography>
                    <Typography variant="h6" sx={{ fontWeight: 'bold', color: mealTimeInfo.color }}>
                      {mealTimeInfo.label}
                    </Typography>
                    <Chip
                      label={`${foodEntries[mealTimeKey].length} alimentos`}
                      size="small"
                      sx={{ backgroundColor: `${mealTimeInfo.color}20`, color: mealTimeInfo.color }}
                    />
                  </Box>
                  <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => handleOpenSearchDialog(mealTimeKey)}
                    sx={{
                      backgroundColor: mealTimeInfo.color,
                      '&:hover': { backgroundColor: mealTimeInfo.color, opacity: 0.9 }
                    }}
                  >
                    Agregar
                  </Button>
                </Box>

                {/* Lista de alimentos */}
                {foodEntries[mealTimeKey].length === 0 ? (
                  <Alert severity="info" sx={{ backgroundColor: '#e3f2fd' }}>
                    No hay alimentos registrados para {mealTimeInfo.label.toLowerCase()}
                  </Alert>
                ) : (
                  <Stack spacing={1}>
                    <AnimatePresence>
                      {foodEntries[mealTimeKey].map((entry) => (
                        <motion.div
                          key={entry.id}
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          exit={{ opacity: 0, scale: 0.9 }}
                          transition={{ duration: 0.2 }}
                        >
                          <Card variant="outlined" sx={{ backgroundColor: '#fafafa' }}>
                            <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                <Box sx={{ flex: 1 }}>
                                  <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 0.5 }}>
                                    {entry.food.name}
                                  </Typography>
                                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                                    {entry.portions} porción(es) × {entry.food.serving_size}g
                                  </Typography>
                                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                                    <Chip
                                      label={`${Math.round(entry.totalCalories)} kcal`}
                                      size="small"
                                      color="primary"
                                      variant="outlined"
                                    />
                                    <Chip
                                      label={`P: ${entry.totalProtein.toFixed(1)}g`}
                                      size="small"
                                      sx={{ borderColor: '#2196F3', color: '#2196F3' }}
                                      variant="outlined"
                                    />
                                    <Chip
                                      label={`C: ${entry.totalCarbs.toFixed(1)}g`}
                                      size="small"
                                      sx={{ borderColor: '#FF9800', color: '#FF9800' }}
                                      variant="outlined"
                                    />
                                    <Chip
                                      label={`G: ${entry.totalFat.toFixed(1)}g`}
                                      size="small"
                                      sx={{ borderColor: '#F44336', color: '#F44336' }}
                                      variant="outlined"
                                    />
                                  </Box>
                                </Box>
                                <IconButton
                                  size="small"
                                  color="error"
                                  onClick={() => handleDeleteEntry(mealTimeKey, entry.id)}
                                >
                                  <DeleteIcon />
                                </IconButton>
                              </Box>
                            </CardContent>
                          </Card>
                        </motion.div>
                      ))}
                    </AnimatePresence>
                  </Stack>
                )}
              </Paper>
            </motion.div>
          ))}
        </Grid>

        {/* Columna derecha - Resumen y análisis */}
        <Grid item xs={12} md={4}>
          <Box sx={{ position: 'sticky', top: 20 }}>
            {/* Resumen nutricional */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
            >
              <Paper sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
                  <AnalyticsIcon color="primary" />
                  Resumen del Día
                </Typography>

                <Divider sx={{ mb: 2 }} />

                {/* Calorías totales */}
                <Box sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2" color="text.secondary">
                      Calorías
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                      {Math.round(dailySummary.calories)} / {dailyGoals.calories} kcal
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={Math.min((dailySummary.calories / dailyGoals.calories) * 100, 100)}
                    sx={{
                      height: 8,
                      borderRadius: 4,
                      backgroundColor: '#e0e0e0',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: getAdherenceColor((dailySummary.calories / dailyGoals.calories) * 100)
                      }
                    }}
                  />
                </Box>

                {/* Macronutrientes */}
                {[
                  { label: 'Proteína', value: dailySummary.protein, goal: dailyGoals.protein, unit: 'g', color: '#2196F3' },
                  { label: 'Carbohidratos', value: dailySummary.carbs, goal: dailyGoals.carbs, unit: 'g', color: '#FF9800' },
                  { label: 'Grasas', value: dailySummary.fat, goal: dailyGoals.fat, unit: 'g', color: '#F44336' },
                  { label: 'Fibra', value: dailySummary.fiber, goal: dailyGoals.fiber, unit: 'g', color: '#4CAF50' },
                ].map((macro) => (
                  <Box key={macro.label} sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                      <Typography variant="body2" color="text.secondary">
                        {macro.label}
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                        {macro.value.toFixed(1)} / {macro.goal}{macro.unit}
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={Math.min((macro.value / macro.goal) * 100, 100)}
                      sx={{
                        height: 6,
                        borderRadius: 3,
                        backgroundColor: '#e0e0e0',
                        '& .MuiLinearProgress-bar': {
                          backgroundColor: macro.color
                        }
                      }}
                    />
                  </Box>
                ))}
              </Paper>
            </motion.div>

            {/* Análisis de adherencia */}
            {adherenceScore && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
              >
                <Paper sx={{ p: 3, backgroundColor: getAdherenceColor(adherenceScore.overall) + '10' }}>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
                    {adherenceScore.overall >= 70 ? <CheckCircleIcon sx={{ color: getAdherenceColor(adherenceScore.overall) }} /> : <WarningIcon sx={{ color: getAdherenceColor(adherenceScore.overall) }} />}
                    Adherencia al Plan
                  </Typography>

                  <Box sx={{ textAlign: 'center', mb: 2 }}>
                    <Typography variant="h2" sx={{ fontWeight: 'bold', color: getAdherenceColor(adherenceScore.overall) }}>
                      {Math.round(adherenceScore.overall)}%
                    </Typography>
                    <Typography variant="body1" sx={{ color: 'text.secondary' }}>
                      {getAdherenceLevel(adherenceScore.overall)}
                    </Typography>
                  </Box>

                  <Divider sx={{ my: 2 }} />

                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Desglose por nutriente:
                  </Typography>

                  <Stack spacing={1}>
                    {[
                      { label: 'Calorías', value: adherenceScore.calories },
                      { label: 'Proteína', value: adherenceScore.protein },
                      { label: 'Carbohidratos', value: adherenceScore.carbs },
                      { label: 'Grasas', value: adherenceScore.fat },
                      { label: 'Fibra', value: adherenceScore.fiber },
                    ].map((item) => (
                      <Box key={item.label} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Typography variant="body2">{item.label}</Typography>
                        <Chip
                          label={`${Math.round(item.value)}%`}
                          size="small"
                          sx={{
                            backgroundColor: getAdherenceColor(item.value),
                            color: 'white',
                            fontWeight: 'bold'
                          }}
                        />
                      </Box>
                    ))}
                  </Stack>
                </Paper>
              </motion.div>
            )}
          </Box>
        </Grid>
      </Grid>

      {/* Dialog de búsqueda de alimentos */}
      <Dialog
        open={searchDialogOpen}
        onClose={handleCloseSearchDialog}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Buscar Alimento para {MEAL_TIMES[currentMealTime]?.label}
        </DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            fullWidth
            placeholder="Buscar por nombre..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            sx={{ mb: 2, mt: 1 }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />

          {searchQuery.length < 2 ? (
            <Alert severity="info">Escribe al menos 2 caracteres para buscar</Alert>
          ) : searchResults.length === 0 ? (
            <Alert severity="warning">No se encontraron resultados</Alert>
          ) : (
            <List>
              {searchResults.map((food) => (
                <ListItemButton
                  key={food.id}
                  selected={selectedFood?.id === food.id}
                  onClick={() => setSelectedFood(food)}
                  sx={{
                    borderRadius: 1,
                    mb: 1,
                    border: selectedFood?.id === food.id ? '2px solid #667eea' : '1px solid #e0e0e0'
                  }}
                >
                  <ListItemText
                    primary={food.name}
                    secondary={`${food.serving_size}g • ${food.calories_per_serving} kcal • P: ${food.protein_g}g C: ${food.carbs_g}g G: ${food.fat_g}g`}
                  />
                </ListItemButton>
              ))}
            </List>
          )}

          {selectedFood && (
            <Box sx={{ mt: 3 }}>
              <Divider sx={{ mb: 2 }} />
              <TextField
                label="Número de porciones"
                type="number"
                value={portionSize}
                onChange={(e) => setPortionSize(Math.max(0.1, parseFloat(e.target.value) || 1))}
                inputProps={{ min: 0.1, step: 0.5 }}
                fullWidth
                helperText={`Total: ${Math.round(selectedFood.calories_per_serving * portionSize)} kcal`}
              />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseSearchDialog}>Cancelar</Button>
          <Button
            variant="contained"
            onClick={handleAddFood}
            disabled={!selectedFood}
          >
            Agregar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Recordatorio24Horas;
