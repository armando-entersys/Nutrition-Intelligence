import React, { useState } from 'react';
import { Container, Box, Typography, Button, Card, CardContent, Grid, Chip, LinearProgress, Alert, List, ListItem, ListItemText } from '@mui/material';
import { CameraAlt, Upload, Psychology, Restaurant, TrendingUp, CheckCircle, Warning } from '@mui/icons-material';
import { motion } from 'framer-motion';

const AnalizadorFotos = () => {
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);

  // Mock de análisis IA
  const mockAnalysis = {
    platillo_identificado: { nombre: 'Tacos al Pastor', confianza: 92, region: 'Centro de México', ingredientes_tipicos: ['Carne de cerdo marinada', 'Piña', 'Cebolla', 'Cilantro', 'Tortilla de maíz'] },
    alimentos_detectados: [
      { nombre: 'Tortilla de maíz', confianza: 95, cantidad_estimada: '6 piezas', calorias_estimadas: 384, categoria: 'Cereales sin grasa' },
      { nombre: 'Carne de cerdo', confianza: 90, cantidad_estimada: '180g', calorias_estimadas: 270, categoria: 'Origen animal moderado aporte' },
      { nombre: 'Piña', confianza: 85, cantidad_estimada: '50g', calorias_estimadas: 25, categoria: 'Frutas' },
      { nombre: 'Cebolla y cilantro', confianza: 88, cantidad_estimada: '30g', calorias_estimadas: 10, categoria: 'Verduras' },
    ],
    estimacion_nutricional: { calorias_total: 689, proteina_g: 35, carbohidratos_g: 75, grasas_g: 22, rango_error: 20 },
    evaluacion_salubridad: { score: 65, alto_en_grasa: true, alto_en_azucar: false, alto_en_sodio: true, ultra_procesado: false, contiene_verduras: true, porcion_adecuada: false },
    sugerencias: ['Reduce la porción de carne a 120g (-50 kcal)', 'Agrega más verduras (pico de gallo, nopales)', 'Usa tortillas integrales (+5g fibra)', 'Limita a 3 tacos en lugar de 6 (-192 kcal)'],
    tags: ['mexicano', 'tradicional', 'alto_proteina', 'moderado_grasa'],
  };

  const handleAnalyze = () => {
    setAnalyzing(true);
    setTimeout(() => {
      setResult(mockAnalysis);
      setAnalyzing(false);
    }, 2000);
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#4CAF50';
    if (score >= 60) return '#FF9800';
    return '#E63946';
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', borderRadius: 4, mb: 3 }}>
          <CardContent sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <Psychology sx={{ fontSize: 48 }} />
              <Box>
                <Typography variant="h4" fontWeight="700">Análisis de Fotos con IA</Typography>
                <Typography variant="body1">Identifica platillos mexicanos, calcula calorías y evalúa salubridad automáticamente</Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>

        {!result && !analyzing && (
          <Card sx={{ borderRadius: 4, textAlign: 'center', p: 6 }}>
            <Restaurant sx={{ fontSize: 80, color: '#667eea', mb: 2 }} />
            <Typography variant="h5" fontWeight="700" gutterBottom>Toma o sube una foto de tu comida</Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>La IA identificará los alimentos, calculará calorías y te dará recomendaciones</Typography>
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
              <Button variant="contained" size="large" startIcon={<CameraAlt />} onClick={handleAnalyze} sx={{ px: 4, py: 1.5 }}>Tomar Foto</Button>
              <Button variant="outlined" size="large" startIcon={<Upload />} onClick={handleAnalyze} sx={{ px: 4, py: 1.5 }}>Subir Imagen</Button>
            </Box>
          </Card>
        )}

        {analyzing && (
          <Card sx={{ borderRadius: 4, p: 6, textAlign: 'center' }}>
            <Psychology sx={{ fontSize: 80, color: '#667eea', mb: 2, animation: 'pulse 1.5s infinite' }} />
            <Typography variant="h5" fontWeight="700" gutterBottom>Analizando imagen con IA...</Typography>
            <LinearProgress sx={{ mt: 3, height: 8, borderRadius: 2 }} />
            <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>Identificando alimentos y calculando valores nutricionales</Typography>
          </Card>
        )}

        {result && (
          <Box>
            {/* Platillo Identificado */}
            <Alert severity="success" icon={<CheckCircle />} sx={{ mb: 3, borderRadius: 3 }}>
              <strong>Platillo identificado:</strong> {result.platillo_identificado.nombre} ({result.platillo_identificado.confianza}% confianza) - {result.platillo_identificado.region}
            </Alert>

            {/* Score de Salubridad */}
            <Card sx={{ borderRadius: 3, mb: 3, border: `3px solid ${getScoreColor(result.evaluacion_salubridad.score)}` }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography variant="h6" fontWeight="700">Evaluación de Salubridad</Typography>
                    <Typography variant="body2" color="text.secondary">Análisis basado en NOM-051 y guías nutricionales</Typography>
                  </Box>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h2" fontWeight="700" sx={{ color: getScoreColor(result.evaluacion_salubridad.score) }}>{result.evaluacion_salubridad.score}</Typography>
                    <Typography variant="caption">de 100</Typography>
                  </Box>
                </Box>
                <Box sx={{ display: 'flex', gap: 1, mt: 2, flexWrap: 'wrap' }}>
                  {result.evaluacion_salubridad.alto_en_grasa && <Chip label="Alto en grasa" color="warning" size="small" />}
                  {result.evaluacion_salubridad.alto_en_sodio && <Chip label="Alto en sodio" color="warning" size="small" />}
                  {result.evaluacion_salubridad.contiene_verduras && <Chip label="Contiene verduras" color="success" size="small" />}
                  {!result.evaluacion_salubridad.ultra_procesado && <Chip label="No ultra procesado" color="success" size="small" />}
                </Box>
              </CardContent>
            </Card>

            {/* Alimentos Detectados y Nutrición */}
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card sx={{ borderRadius: 3 }}>
                  <CardContent>
                    <Typography variant="h6" fontWeight="700" gutterBottom>Alimentos Detectados</Typography>
                    <List>
                      {result.alimentos_detectados.map((alimento, idx) => (
                        <ListItem key={idx}>
                          <ListItemText primary={`${alimento.nombre} (${alimento.confianza}%)`} secondary={`${alimento.cantidad_estimada} - ${alimento.calorias_estimadas} kcal`} />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={6}>
                <Card sx={{ borderRadius: 3 }}>
                  <CardContent>
                    <Typography variant="h6" fontWeight="700" gutterBottom>Estimación Nutricional</Typography>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="h3" fontWeight="700">{result.estimacion_nutricional.calorias_total} kcal</Typography>
                      <Typography variant="caption" color="text.secondary">±{result.estimacion_nutricional.rango_error}% de error estimado</Typography>
                    </Box>
                    <Grid container spacing={2}>
                      <Grid item xs={4}><Typography variant="caption">Proteínas</Typography><Typography variant="h6" fontWeight="700">{result.estimacion_nutricional.proteina_g}g</Typography></Grid>
                      <Grid item xs={4}><Typography variant="caption">Carbohidratos</Typography><Typography variant="h6" fontWeight="700">{result.estimacion_nutricional.carbohidratos_g}g</Typography></Grid>
                      <Grid item xs={4}><Typography variant="caption">Grasas</Typography><Typography variant="h6" fontWeight="700">{result.estimacion_nutricional.grasas_g}g</Typography></Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12}>
                <Card sx={{ borderRadius: 3 }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                      <TrendingUp sx={{ color: '#4CAF50' }} />
                      <Typography variant="h6" fontWeight="700">Sugerencias de Mejora (IA)</Typography>
                    </Box>
                    <List>
                      {result.sugerencias.map((sug, idx) => (
                        <ListItem key={idx}><CheckCircle sx={{ color: '#4CAF50', mr: 1 }} /><ListItemText primary={sug} /></ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
              <Button variant="contained" fullWidth onClick={() => setResult(null)}>Analizar Otra Imagen</Button>
              <Button variant="outlined" fullWidth>Agregar al Recordatorio 24h</Button>
            </Box>
          </Box>
        )}
      </motion.div>
    </Container>
  );
};

export default AnalizadorFotos;
