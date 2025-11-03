/**
 * Calculadora de Requerimientos Nutricionales
 * Calcula TMB, GET y distribución de macronutrientes
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormLabel,
  Divider,
  Chip,
  Alert,
  Stack,
  Slider,
  Tooltip,
  IconButton,
} from '@mui/material';
import {
  Calculate as CalculateIcon,
  FitnessCenter as FitnessCenterIcon,
  Restaurant as RestaurantIcon,
  Info as InfoIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  TrendingFlat as TrendingFlatIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const CalculadoraRequerimientos = ({ onResultsCalculated }) => {
  // Estados del formulario
  const [formData, setFormData] = useState({
    peso: '',
    talla: '',
    edad: '',
    sexo: 'masculino',
    nivelActividad: 'sedentario',
    objetivo: 'mantenimiento',
    formula: 'mifflin',
  });

  // Estados de resultados
  const [results, setResults] = useState(null);
  const [distribucionMacros, setDistribucionMacros] = useState({
    proteina: 25,
    carbohidratos: 50,
    grasas: 25,
  });

  // Niveles de actividad física
  const nivelesActividad = {
    sedentario: { label: 'Sedentario (poco o ningún ejercicio)', factor: 1.2 },
    ligero: { label: 'Ligero (ejercicio 1-3 días/semana)', factor: 1.375 },
    moderado: { label: 'Moderado (ejercicio 3-5 días/semana)', factor: 1.55 },
    activo: { label: 'Activo (ejercicio 6-7 días/semana)', factor: 1.725 },
    muyActivo: { label: 'Muy Activo (ejercicio intenso diario)', factor: 1.9 },
  };

  // Objetivos y sus ajustes calóricos
  const objetivos = {
    reduccion: { label: 'Reducción de peso', ajuste: -500, icon: <TrendingDownIcon />, color: '#F44336' },
    mantenimiento: { label: 'Mantenimiento', ajuste: 0, icon: <TrendingFlatIcon />, color: '#2196F3' },
    aumento: { label: 'Aumento de peso/masa muscular', ajuste: +500, icon: <TrendingUpIcon />, color: '#4CAF50' },
  };

  // ============================================================================
  // CÁLCULOS
  // ============================================================================

  const calcularTMB = () => {
    const { peso, talla, edad, sexo, formula } = formData;

    if (!peso || !talla || !edad) return null;

    let tmb = 0;

    if (formula === 'mifflin') {
      // Fórmula Mifflin-St Jeor (más precisa)
      if (sexo === 'masculino') {
        tmb = (10 * parseFloat(peso)) + (6.25 * parseFloat(talla)) - (5 * parseFloat(edad)) + 5;
      } else {
        tmb = (10 * parseFloat(peso)) + (6.25 * parseFloat(talla)) - (5 * parseFloat(edad)) - 161;
      }
    } else if (formula === 'harris') {
      // Fórmula Harris-Benedict (clásica)
      if (sexo === 'masculino') {
        tmb = 66.5 + (13.75 * parseFloat(peso)) + (5.003 * parseFloat(talla)) - (6.75 * parseFloat(edad));
      } else {
        tmb = 655.1 + (9.563 * parseFloat(peso)) + (1.850 * parseFloat(talla)) - (4.676 * parseFloat(edad));
      }
    }

    return Math.round(tmb);
  };

  const calcularGET = (tmb) => {
    if (!tmb) return null;

    const factorActividad = nivelesActividad[formData.nivelActividad].factor;
    const get = tmb * factorActividad;

    return Math.round(get);
  };

  const calcularCaloriasObjetivo = (get) => {
    if (!get) return null;

    const ajuste = objetivos[formData.objetivo].ajuste;
    return Math.round(get + ajuste);
  };

  const calcularMacronutrientes = (calorias) => {
    if (!calorias) return null;

    const { proteina, carbohidratos, grasas } = distribucionMacros;

    const proteinaKcal = (calorias * proteina) / 100;
    const carbohidratosKcal = (calorias * carbohidratos) / 100;
    const grasasKcal = (calorias * grasas) / 100;

    return {
      proteina: {
        gramos: Math.round(proteinaKcal / 4),
        kcal: Math.round(proteinaKcal),
        porcentaje: proteina,
        gramosPorKg: Math.round((proteinaKcal / 4) / parseFloat(formData.peso) * 10) / 10,
      },
      carbohidratos: {
        gramos: Math.round(carbohidratosKcal / 4),
        kcal: Math.round(carbohidratosKcal),
        porcentaje: carbohidratos,
      },
      grasas: {
        gramos: Math.round(grasasKcal / 9),
        kcal: Math.round(grasasKcal),
        porcentaje: grasas,
      },
    };
  };

  const calcularIMC = () => {
    const { peso, talla } = formData;
    if (!peso || !talla) return null;

    const tallaMetros = parseFloat(talla) / 100;
    const imc = parseFloat(peso) / (tallaMetros * tallaMetros);

    return Math.round(imc * 10) / 10;
  };

  const getIMCCategoria = (imc) => {
    if (!imc) return null;

    if (imc < 18.5) return { label: 'Bajo peso', color: '#FF9800' };
    if (imc < 25) return { label: 'Peso normal', color: '#4CAF50' };
    if (imc < 30) return { label: 'Sobrepeso', color: '#FF9800' };
    return { label: 'Obesidad', color: '#F44336' };
  };

  // ============================================================================
  // HANDLERS
  // ============================================================================

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleCalcular = () => {
    const tmb = calcularTMB();
    if (!tmb) {
      alert('Por favor complete todos los campos');
      return;
    }

    const get = calcularGET(tmb);
    const caloriasObjetivo = calcularCaloriasObjetivo(get);
    const macros = calcularMacronutrientes(caloriasObjetivo);
    const imc = calcularIMC();
    const imcCategoria = getIMCCategoria(imc);

    const resultados = {
      tmb,
      get,
      caloriasObjetivo,
      macros,
      imc,
      imcCategoria,
      formData: { ...formData },
      distribucionMacros: { ...distribucionMacros },
    };

    setResults(resultados);

    // Callback para pasar resultados al componente padre
    if (onResultsCalculated) {
      onResultsCalculated(resultados);
    }
  };

  const handleMacroChange = (macro, value) => {
    setDistribucionMacros(prev => {
      const newValues = { ...prev, [macro]: value };

      // Ajustar otros macros para que sumen 100%
      const total = Object.values(newValues).reduce((sum, val) => sum + val, 0);

      if (total !== 100) {
        const diff = 100 - total;
        const otherMacros = Object.keys(newValues).filter(m => m !== macro);
        const adjustment = diff / otherMacros.length;

        otherMacros.forEach(m => {
          newValues[m] = Math.max(5, Math.min(70, newValues[m] + adjustment));
        });
      }

      return newValues;
    });
  };

  // ============================================================================
  // RENDER
  // ============================================================================

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Paper sx={{ p: 3, mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
          <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold', mb: 1 }}>
            🧮 Calculadora de Requerimientos Nutricionales
          </Typography>
          <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.9)' }}>
            Calcula TMB, GET y distribución de macronutrientes personalizada
          </Typography>
        </Paper>
      </motion.div>

      <Grid container spacing={3}>
        {/* Formulario */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 'bold' }}>
              Datos del Paciente
            </Typography>

            <Stack spacing={3}>
              {/* Datos antropométricos */}
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Peso (kg)"
                    type="number"
                    value={formData.peso}
                    onChange={(e) => handleInputChange('peso', e.target.value)}
                    inputProps={{ min: 20, max: 300, step: 0.1 }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Talla (cm)"
                    type="number"
                    value={formData.talla}
                    onChange={(e) => handleInputChange('talla', e.target.value)}
                    inputProps={{ min: 100, max: 250 }}
                  />
                </Grid>
              </Grid>

              <TextField
                fullWidth
                label="Edad (años)"
                type="number"
                value={formData.edad}
                onChange={(e) => handleInputChange('edad', e.target.value)}
                inputProps={{ min: 1, max: 120 }}
              />

              {/* Sexo */}
              <FormControl>
                <FormLabel>Sexo</FormLabel>
                <RadioGroup
                  row
                  value={formData.sexo}
                  onChange={(e) => handleInputChange('sexo', e.target.value)}
                >
                  <FormControlLabel value="masculino" control={<Radio />} label="Masculino" />
                  <FormControlLabel value="femenino" control={<Radio />} label="Femenino" />
                </RadioGroup>
              </FormControl>

              {/* Nivel de actividad */}
              <FormControl fullWidth>
                <InputLabel>Nivel de Actividad Física</InputLabel>
                <Select
                  value={formData.nivelActividad}
                  onChange={(e) => handleInputChange('nivelActividad', e.target.value)}
                  label="Nivel de Actividad Física"
                >
                  {Object.entries(nivelesActividad).map(([key, { label }]) => (
                    <MenuItem key={key} value={key}>{label}</MenuItem>
                  ))}
                </Select>
              </FormControl>

              {/* Objetivo */}
              <FormControl fullWidth>
                <InputLabel>Objetivo</InputLabel>
                <Select
                  value={formData.objetivo}
                  onChange={(e) => handleInputChange('objetivo', e.target.value)}
                  label="Objetivo"
                >
                  {Object.entries(objetivos).map(([key, { label, icon }]) => (
                    <MenuItem key={key} value={key}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        {icon}
                        {label}
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              {/* Fórmula */}
              <FormControl fullWidth>
                <InputLabel>Fórmula de Cálculo</InputLabel>
                <Select
                  value={formData.formula}
                  onChange={(e) => handleInputChange('formula', e.target.value)}
                  label="Fórmula de Cálculo"
                >
                  <MenuItem value="mifflin">Mifflin-St Jeor (Recomendada)</MenuItem>
                  <MenuItem value="harris">Harris-Benedict (Clásica)</MenuItem>
                </Select>
              </FormControl>

              <Divider />

              {/* Distribución de macronutrientes */}
              <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mt: 2 }}>
                Distribución de Macronutrientes
              </Typography>

              {[
                { key: 'proteina', label: 'Proteína', color: '#E91E63' },
                { key: 'carbohidratos', label: 'Carbohidratos', color: '#FF9800' },
                { key: 'grasas', label: 'Grasas', color: '#2196F3' },
              ].map(({ key, label, color }) => (
                <Box key={key}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2">{label}</Typography>
                    <Typography variant="body2" sx={{ fontWeight: 'bold', color }}>
                      {Math.round(distribucionMacros[key])}%
                    </Typography>
                  </Box>
                  <Slider
                    value={distribucionMacros[key]}
                    onChange={(e, value) => handleMacroChange(key, value)}
                    min={5}
                    max={70}
                    step={5}
                    sx={{
                      color: color,
                      '& .MuiSlider-thumb': { bgcolor: color },
                      '& .MuiSlider-track': { bgcolor: color },
                    }}
                  />
                </Box>
              ))}

              <Alert severity="info" sx={{ mt: 1 }}>
                Los porcentajes se ajustan automáticamente para sumar 100%
              </Alert>

              <Button
                variant="contained"
                size="large"
                fullWidth
                startIcon={<CalculateIcon />}
                onClick={handleCalcular}
                sx={{ mt: 2 }}
              >
                Calcular Requerimientos
              </Button>
            </Stack>
          </Paper>
        </Grid>

        {/* Resultados */}
        <Grid item xs={12} md={6}>
          {results ? (
            <Stack spacing={2}>
              {/* IMC */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5 }}
              >
                <Card sx={{ borderLeft: `4px solid ${results.imcCategoria.color}` }}>
                  <CardContent>
                    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                      Índice de Masa Corporal (IMC)
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                        {results.imc}
                      </Typography>
                      <Chip
                        label={results.imcCategoria.label}
                        sx={{ backgroundColor: results.imcCategoria.color, color: 'white', fontWeight: 'bold' }}
                      />
                    </Box>
                  </CardContent>
                </Card>
              </motion.div>

              {/* TMB y GET */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.1 }}
              >
                <Card>
                  <CardContent>
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          TMB (Tasa Metabólica Basal)
                          <Tooltip title="Calorías que quemas en reposo total">
                            <IconButton size="small" sx={{ ml: 0.5 }}>
                              <InfoIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </Typography>
                        <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#9C27B0' }}>
                          {results.tmb} kcal
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          GET (Gasto Energético Total)
                          <Tooltip title="Calorías totales considerando actividad física">
                            <IconButton size="small" sx={{ ml: 0.5 }}>
                              <InfoIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </Typography>
                        <Typography variant="h5" sx={{ fontWeight: 'bold', color: '#3F51B5' }}>
                          {results.get} kcal
                        </Typography>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </motion.div>

              {/* Calorías objetivo */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
              >
                <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                      {objetivos[results.formData.objetivo].icon}
                      <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                        Calorías Objetivo
                      </Typography>
                    </Box>
                    <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                      {results.caloriasObjetivo} kcal/día
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1, opacity: 0.9 }}>
                      {objetivos[results.formData.objetivo].label}
                      {objetivos[results.formData.objetivo].ajuste !== 0 &&
                        ` (${objetivos[results.formData.objetivo].ajuste > 0 ? '+' : ''}${objetivos[results.formData.objetivo].ajuste} kcal/día)`
                      }
                    </Typography>
                  </CardContent>
                </Card>
              </motion.div>

              {/* Macronutrientes */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.3 }}
              >
                <Card>
                  <CardContent>
                    <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>
                      Distribución de Macronutrientes
                    </Typography>

                    <Stack spacing={2}>
                      {/* Proteína */}
                      <Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                            Proteína
                          </Typography>
                          <Typography variant="body2" sx={{ color: '#E91E63', fontWeight: 'bold' }}>
                            {results.macros.proteina.gramos}g ({results.macros.proteina.porcentaje}%)
                          </Typography>
                        </Box>
                        <Typography variant="caption" color="text.secondary">
                          {results.macros.proteina.kcal} kcal • {results.macros.proteina.gramosPorKg}g/kg peso
                        </Typography>
                      </Box>

                      <Divider />

                      {/* Carbohidratos */}
                      <Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                            Carbohidratos
                          </Typography>
                          <Typography variant="body2" sx={{ color: '#FF9800', fontWeight: 'bold' }}>
                            {results.macros.carbohidratos.gramos}g ({results.macros.carbohidratos.porcentaje}%)
                          </Typography>
                        </Box>
                        <Typography variant="caption" color="text.secondary">
                          {results.macros.carbohidratos.kcal} kcal
                        </Typography>
                      </Box>

                      <Divider />

                      {/* Grasas */}
                      <Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                            Grasas
                          </Typography>
                          <Typography variant="body2" sx={{ color: '#2196F3', fontWeight: 'bold' }}>
                            {results.macros.grasas.gramos}g ({results.macros.grasas.porcentaje}%)
                          </Typography>
                        </Box>
                        <Typography variant="caption" color="text.secondary">
                          {results.macros.grasas.kcal} kcal
                        </Typography>
                      </Box>
                    </Stack>
                  </CardContent>
                </Card>
              </motion.div>

              {/* Recomendaciones */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.4 }}
              >
                <Alert severity="success" sx={{ mt: 2 }}>
                  <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 1 }}>
                    Recomendaciones
                  </Typography>
                  <Typography variant="body2">
                    • Estos valores son estimaciones basadas en fórmulas estándar<br />
                    • Ajusta según la respuesta individual y monitorea semanalmente<br />
                    • Considera factores como estrés, sueño y composición corporal<br />
                    • Usa estos datos para generar un plan alimenticio personalizado
                  </Typography>
                </Alert>
              </motion.div>
            </Stack>
          ) : (
            <Paper sx={{ p: 4, textAlign: 'center', backgroundColor: '#f5f5f5' }}>
              <FitnessCenterIcon sx={{ fontSize: 64, color: '#bdbdbd', mb: 2 }} />
              <Typography variant="h6" color="text.secondary">
                Completa el formulario para calcular los requerimientos nutricionales
              </Typography>
            </Paper>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default CalculadoraRequerimientos;
