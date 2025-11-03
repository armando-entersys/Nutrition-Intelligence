/**
 * Analizador de Fotos Mejorado con IA Vision
 * Integración preparada para Claude Vision o GPT-4 Vision
 */
import React, { useState, useRef, useCallback } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  LinearProgress,
  Alert,
  Stack,
  Divider,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Tabs,
  Tab,
} from '@mui/material';
import {
  CameraAlt as CameraIcon,
  Upload as UploadIcon,
  Psychology as PsychologyIcon,
  Restaurant as RestaurantIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  Close as CloseIcon,
  Save as SaveIcon,
  History as HistoryIcon,
  TrendingUp,
  TrendingDown,
  TrendingFlat,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';

const AnalizadorFotosMejorado = () => {
  // Estados
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [analysisHistory, setAnalysisHistory] = useState([]);
  const [currentTab, setCurrentTab] = useState(0);
  const [showCameraDialog, setShowCameraDialog] = useState(false);

  // Refs
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  // ============================================================================
  // CAPTURA Y CARGA DE IMÁGENES
  // ============================================================================

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);

      // Crear preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCameraCapture = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' }
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }

      setShowCameraDialog(true);
    } catch (error) {
      console.error('Error accessing camera:', error);
      alert('No se pudo acceder a la cámara. Por favor, verifica los permisos.');
    }
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const video = videoRef.current;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      canvas.toBlob((blob) => {
        const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
        setSelectedImage(file);
        setImagePreview(canvas.toDataURL('image/jpeg'));

        // Detener stream
        const stream = video.srcObject;
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());

        setShowCameraDialog(false);
      }, 'image/jpeg', 0.8);
    }
  };

  const handleCloseCameraDialog = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach(track => track.stop());
    }
    setShowCameraDialog(false);
  };

  // ============================================================================
  // ANÁLISIS CON IA
  // ============================================================================

  const analyzeImageWithAI = async (imageFile) => {
    setAnalyzing(true);

    try {
      // Crear FormData para enviar la imagen al backend
      const formData = new FormData();
      formData.append('file', imageFile);

      // Llamar al backend con Gemini Vision
      console.log('Enviando imagen al backend para análisis con Gemini Vision...');
      const response = await axios.post(
        `${API_BASE_URL}/api/v1/vision/analyze-food`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          timeout: 60000, // 60 segundos timeout
        }
      );

      const result = response.data;

      console.log('Análisis recibido del backend:', result);

      // Agregar campos adicionales para UI
      const analysis = {
        ...result,
        timestamp: new Date().toISOString(),
        image_url: imagePreview,
        // Agregar iconos a las recomendaciones
        recomendaciones: (result.recomendaciones || []).map(rec => ({
          ...rec,
          icon: rec.tipo === 'reduccion' || rec.tipo === 'porcion' ? <TrendingDown /> :
                rec.tipo === 'adicion' || rec.tipo === 'mejora' ? <TrendingUp /> :
                <TrendingFlat />
        }))
      };

      setAnalysisResult(analysis);

      // Agregar al historial
      setAnalysisHistory(prev => [analysis, ...prev].slice(0, 10));

      setAnalyzing(false);
    } catch (error) {
      console.error('Error analyzing image:', error);
      setAnalyzing(false);

      let errorMessage = 'Error al analizar la imagen. Por favor intenta de nuevo.';

      if (error.response) {
        // Error del backend
        errorMessage = `Error del servidor: ${error.response.data.detail || error.response.statusText}`;
      } else if (error.request) {
        // No hay respuesta del backend
        errorMessage = 'No se pudo conectar con el servidor. Verifica que el backend esté ejecutándose.';
      } else if (error.code === 'ECONNABORTED') {
        // Timeout
        errorMessage = 'El análisis tomó demasiado tiempo. Por favor intenta con una imagen más pequeña.';
      }

      alert(errorMessage);
    }
  };

  const handleAnalyze = () => {
    if (selectedImage) {
      analyzeImageWithAI(selectedImage);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setImagePreview(null);
    setAnalysisResult(null);
  };

  const handleSaveAnalysis = () => {
    // En producción, aquí se guardaría en el backend
    alert('Análisis guardado en tu historial');
  };

  // ============================================================================
  // RENDER
  // ============================================================================

  const getScoreColor = (score) => {
    if (score >= 80) return '#4CAF50';
    if (score >= 60) return '#FF9800';
    return '#F44336';
  };

  return (
    <Box sx={{ maxWidth: 1400, mx: 'auto', p: 3 }}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Paper sx={{ p: 3, mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <PsychologyIcon sx={{ fontSize: 48, color: 'white' }} />
            <Box>
              <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
                📸 Análisis de Fotos con IA
              </Typography>
              <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.9)' }}>
                Identifica platillos mexicanos, calcula nutrientes y recibe recomendaciones personalizadas
              </Typography>
            </Box>
          </Box>
        </Paper>
      </motion.div>

      {/* Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={currentTab} onChange={(e, v) => setCurrentTab(v)}>
          <Tab icon={<RestaurantIcon />} label="Análisis" iconPosition="start" />
          <Tab icon={<HistoryIcon />} label={`Historial (${analysisHistory.length})`} iconPosition="start" />
        </Tabs>
      </Paper>

      {/* TAB 1: Análisis */}
      {currentTab === 0 && (
        <Grid container spacing={3}>
          {/* Columna izquierda - Captura/Preview */}
          <Grid item xs={12} md={5}>
            <Paper sx={{ p: 3 }}>
              {!imagePreview ? (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <RestaurantIcon sx={{ fontSize: 80, color: '#667eea', mb: 2 }} />
                  <Typography variant="h6" sx={{ mb: 1, fontWeight: 'bold' }}>
                    Captura o sube una foto
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
                    La IA identificará los alimentos y calculará los nutrientes
                  </Typography>

                  <Stack spacing={2}>
                    <Button
                      variant="contained"
                      size="large"
                      fullWidth
                      startIcon={<CameraIcon />}
                      onClick={handleCameraCapture}
                      sx={{ py: 1.5 }}
                    >
                      Tomar Foto
                    </Button>

                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/*"
                      style={{ display: 'none' }}
                      onChange={handleFileSelect}
                    />

                    <Button
                      variant="outlined"
                      size="large"
                      fullWidth
                      startIcon={<UploadIcon />}
                      onClick={() => fileInputRef.current?.click()}
                      sx={{ py: 1.5 }}
                    >
                      Subir Imagen
                    </Button>
                  </Stack>

                  <Alert severity="info" sx={{ mt: 3, textAlign: 'left' }}>
                    <Typography variant="caption">
                      <strong>Consejos para mejores resultados:</strong><br />
                      • Iluminación adecuada<br />
                      • Vista cenital o frontal<br />
                      • Todos los elementos visibles<br />
                      • Incluir referencia de tamaño si es posible
                    </Typography>
                  </Alert>
                </Box>
              ) : (
                <Box>
                  <Box sx={{ position: 'relative' }}>
                    <img
                      src={imagePreview}
                      alt="Preview"
                      style={{
                        width: '100%',
                        borderRadius: 8,
                        maxHeight: 400,
                        objectFit: 'cover'
                      }}
                    />
                    <IconButton
                      onClick={handleReset}
                      sx={{
                        position: 'absolute',
                        top: 8,
                        right: 8,
                        backgroundColor: 'rgba(0,0,0,0.6)',
                        color: 'white',
                        '&:hover': { backgroundColor: 'rgba(0,0,0,0.8)' }
                      }}
                    >
                      <CloseIcon />
                    </IconButton>
                  </Box>

                  {!analyzing && !analysisResult && (
                    <Button
                      variant="contained"
                      size="large"
                      fullWidth
                      startIcon={<PsychologyIcon />}
                      onClick={handleAnalyze}
                      sx={{ mt: 2 }}
                    >
                      Analizar con IA
                    </Button>
                  )}

                  {analysisResult && (
                    <Stack direction="row" spacing={1} sx={{ mt: 2 }}>
                      <Button
                        variant="outlined"
                        fullWidth
                        startIcon={<SaveIcon />}
                        onClick={handleSaveAnalysis}
                      >
                        Guardar
                      </Button>
                      <Button
                        variant="outlined"
                        fullWidth
                        onClick={handleReset}
                      >
                        Nuevo Análisis
                      </Button>
                    </Stack>
                  )}
                </Box>
              )}
            </Paper>
          </Grid>

          {/* Columna derecha - Resultados */}
          <Grid item xs={12} md={7}>
            {analyzing && (
              <Paper sx={{ p: 6, textAlign: 'center' }}>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                >
                  <PsychologyIcon sx={{ fontSize: 80, color: '#667eea', mb: 2 }} />
                </motion.div>
                <Typography variant="h5" sx={{ fontWeight: 'bold', mb: 2 }}>
                  Analizando con IA...
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  Identificando alimentos, estimando porciones y calculando nutrientes
                </Typography>
                <LinearProgress sx={{ height: 8, borderRadius: 4 }} />
              </Paper>
            )}

            {analysisResult && !analyzing && (
              <Stack spacing={2}>
                {/* Platillo identificado */}
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  <Alert
                    severity="success"
                    icon={<CheckCircleIcon />}
                    sx={{ borderRadius: 2 }}
                  >
                    <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                      {analysisResult.platillo.nombre}
                    </Typography>
                    <Typography variant="body2">
                      {analysisResult.platillo.descripcion} • {analysisResult.platillo.confianza}% confianza
                    </Typography>
                  </Alert>
                </motion.div>

                {/* Score de evaluación */}
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: 0.1 }}
                >
                  <Card sx={{ borderLeft: `4px solid ${analysisResult.evaluacion.color}` }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                        <Box>
                          <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                            Evaluación de Salubridad
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Análisis basado en NOM-051
                          </Typography>
                        </Box>
                        <Box sx={{ textAlign: 'center' }}>
                          <Typography variant="h2" sx={{ fontWeight: 'bold', color: analysisResult.evaluacion.color }}>
                            {analysisResult.evaluacion.score}
                          </Typography>
                          <Typography variant="caption">{analysisResult.evaluacion.nivel}</Typography>
                        </Box>
                      </Box>

                      {/* Sellos NOM-051 */}
                      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                        {analysisResult.sellos_nom051.exceso_grasas_saturadas && (
                          <Chip label="⚠️ Exceso grasas saturadas" size="small" color="warning" />
                        )}
                        {analysisResult.sellos_nom051.exceso_sodio && (
                          <Chip label="⚠️ Exceso sodio" size="small" color="warning" />
                        )}
                        {!analysisResult.sellos_nom051.exceso_azucares && (
                          <Chip label="✓ Sin exceso azúcares" size="small" color="success" />
                        )}
                      </Box>

                      <Divider sx={{ my: 2 }} />

                      {/* Contexto diario */}
                      <Alert severity="info" sx={{ fontSize: '0.875rem' }}>
                        {analysisResult.contexto_diario.mensaje}
                      </Alert>
                    </CardContent>
                  </Card>
                </motion.div>

                {/* Totales nutricionales */}
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                >
                  <Card>
                    <CardContent>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
                        Información Nutricional Total
                      </Typography>

                      <Grid container spacing={2}>
                        <Grid item xs={6} sm={3}>
                          <Box sx={{ textAlign: 'center', p: 2, backgroundColor: '#f5f5f5', borderRadius: 2 }}>
                            <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#667eea' }}>
                              {analysisResult.totales.calorias}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">kcal</Typography>
                          </Box>
                        </Grid>
                        <Grid item xs={6} sm={3}>
                          <Box sx={{ textAlign: 'center', p: 2, backgroundColor: '#f5f5f5', borderRadius: 2 }}>
                            <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#E91E63' }}>
                              {analysisResult.totales.proteina}g
                            </Typography>
                            <Typography variant="caption" color="text.secondary">Proteína</Typography>
                          </Box>
                        </Grid>
                        <Grid item xs={6} sm={3}>
                          <Box sx={{ textAlign: 'center', p: 2, backgroundColor: '#f5f5f5', borderRadius: 2 }}>
                            <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#FF9800' }}>
                              {analysisResult.totales.carbohidratos}g
                            </Typography>
                            <Typography variant="caption" color="text.secondary">Carbohidratos</Typography>
                          </Box>
                        </Grid>
                        <Grid item xs={6} sm={3}>
                          <Box sx={{ textAlign: 'center', p: 2, backgroundColor: '#f5f5f5', borderRadius: 2 }}>
                            <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#2196F3' }}>
                              {analysisResult.totales.grasas}g
                            </Typography>
                            <Typography variant="caption" color="text.secondary">Grasas</Typography>
                          </Box>
                        </Grid>
                      </Grid>

                      <Alert severity="warning" sx={{ mt: 2, fontSize: '0.875rem' }}>
                        Margen de error estimado: ±{analysisResult.totales.margen_error}%
                      </Alert>
                    </CardContent>
                  </Card>
                </motion.div>

                {/* Recomendaciones */}
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: 0.3 }}
                >
                  <Card>
                    <CardContent>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
                        💡 Recomendaciones Personalizadas
                      </Typography>

                      <Stack spacing={2}>
                        {analysisResult.recomendaciones.map((rec, idx) => (
                          <Box
                            key={idx}
                            sx={{
                              p: 2,
                              borderRadius: 2,
                              backgroundColor: '#f5f5f5',
                              borderLeft: '4px solid #667eea'
                            }}
                          >
                            <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                              <Box sx={{ color: '#667eea', mt: 0.5 }}>
                                {rec.icon}
                              </Box>
                              <Box sx={{ flex: 1 }}>
                                <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
                                  {rec.titulo}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  {rec.descripcion}
                                </Typography>
                                <Chip
                                  label={rec.impacto}
                                  size="small"
                                  sx={{ mt: 1, backgroundColor: 'white' }}
                                />
                              </Box>
                            </Box>
                          </Box>
                        ))}
                      </Stack>
                    </CardContent>
                  </Card>
                </motion.div>

                {/* Ingredientes detectados */}
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: 0.4 }}
                >
                  <Card>
                    <CardContent>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
                        Ingredientes Detectados
                      </Typography>

                      <List>
                        {analysisResult.ingredientes.map((ing, idx) => (
                          <ListItem
                            key={idx}
                            sx={{
                              borderRadius: 1,
                              mb: 1,
                              backgroundColor: '#f5f5f5'
                            }}
                          >
                            <ListItemText
                              primary={
                                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                  <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                                    {ing.nombre}
                                  </Typography>
                                  <Chip
                                    label={`${ing.confianza}%`}
                                    size="small"
                                    color="primary"
                                    variant="outlined"
                                  />
                                </Box>
                              }
                              secondary={
                                <Box sx={{ mt: 1 }}>
                                  <Typography variant="body2" color="text.secondary">
                                    {ing.cantidad_estimada} • {ing.calorias} kcal
                                  </Typography>
                                  <Typography variant="caption" color="text.secondary">
                                    P: {ing.proteina}g • C: {ing.carbohidratos}g • G: {ing.grasas}g
                                  </Typography>
                                </Box>
                              }
                            />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                  </Card>
                </motion.div>
              </Stack>
            )}

            {!imagePreview && !analyzing && (
              <Paper sx={{ p: 6, textAlign: 'center', backgroundColor: '#f5f5f5' }}>
                <InfoIcon sx={{ fontSize: 80, color: '#bdbdbd', mb: 2 }} />
                <Typography variant="h6" color="text.secondary">
                  Los resultados del análisis aparecerán aquí
                </Typography>
              </Paper>
            )}
          </Grid>
        </Grid>
      )}

      {/* TAB 2: Historial */}
      {currentTab === 1 && (
        <Paper sx={{ p: 3 }}>
          {analysisHistory.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 6 }}>
              <HistoryIcon sx={{ fontSize: 80, color: '#bdbdbd', mb: 2 }} />
              <Typography variant="h6" color="text.secondary">
                No hay análisis previos
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Los análisis que realices aparecerán aquí
              </Typography>
            </Box>
          ) : (
            <Grid container spacing={2}>
              {analysisHistory.map((analysis, idx) => (
                <Grid item xs={12} sm={6} md={4} key={idx}>
                  <Card sx={{ cursor: 'pointer', '&:hover': { boxShadow: 6 } }}>
                    <img
                      src={analysis.image_url}
                      alt={analysis.platillo.nombre}
                      style={{
                        width: '100%',
                        height: 200,
                        objectFit: 'cover'
                      }}
                    />
                    <CardContent>
                      <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
                        {analysis.platillo.nombre}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                        {new Date(analysis.timestamp).toLocaleString('es-MX')}
                      </Typography>
                      <Chip
                        label={`${analysis.totales.calorias} kcal`}
                        size="small"
                        color="primary"
                      />
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}
        </Paper>
      )}

      {/* Dialog de cámara */}
      <Dialog
        open={showCameraDialog}
        onClose={handleCloseCameraDialog}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Capturar Foto
          <IconButton
            onClick={handleCloseCameraDialog}
            sx={{ position: 'absolute', right: 8, top: 8 }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          <Box sx={{ textAlign: 'center' }}>
            <video
              ref={videoRef}
              style={{
                width: '100%',
                borderRadius: 8,
                backgroundColor: '#000'
              }}
            />
            <canvas ref={canvasRef} style={{ display: 'none' }} />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseCameraDialog}>
            Cancelar
          </Button>
          <Button
            variant="contained"
            startIcon={<CameraIcon />}
            onClick={capturePhoto}
          >
            Capturar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AnalizadorFotosMejorado;
