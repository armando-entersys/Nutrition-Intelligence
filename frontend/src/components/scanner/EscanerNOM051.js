import React, { useState, useRef } from 'react';
import {
  Box,
  Container,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  Alert,
  Divider,
  LinearProgress,
  IconButton,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  TextField,
  ToggleButtonGroup,
  ToggleButton,
  CircularProgress,
} from '@mui/material';
import {
  CameraAlt as CameraIcon,
  QrCodeScanner as QrIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Close as CloseIcon,
  CompareArrows as CompareIcon,
  TipsAndUpdates as TipsIcon,
  PhotoCamera as PhotoCameraIcon,
  Image as ImageIcon,
  Verified as VerifiedIcon,
  People as PeopleIcon,
  AutoAwesome as AutoAwesomeIcon,
  Public as PublicIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { scanBarcode, scanLabel, formatProductData } from '../../services/scannerService';

const MotionPaper = motion(Paper);
const MotionCard = motion(Card);
const MotionBox = motion(Box);

/**
 * EscanerNOM051 - Escáner de Etiquetas según NOM-051
 *
 * Sistema para escanear productos y evaluar su cumplimiento con la NOM-051
 * Detecta los 7 sellos de advertencia y sugiere alternativas más saludables
 *
 * Soporta dos modos de escaneo:
 * 1. Código de barras: Busca en Open Food Facts
 * 2. Etiqueta: Usa Vision AI para leer la tabla nutricional
 */
const EscanerNOM051 = () => {
  const [scanMode, setScanMode] = useState('barcode'); // 'barcode' o 'label'
  const [scanning, setScanning] = useState(false);
  const [scannedProduct, setScannedProduct] = useState(null);
  const [currentTab, setCurrentTab] = useState(0);
  const [error, setError] = useState(null);
  const [barcode, setBarcode] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);

  const sellosInfo = {
    exceso_azucares: {
      nombre: 'EXCESO AZÚCARES',
      color: '#000000',
      icon: '⚠',
      descripcion: 'Contiene más del 10% de azúcares añadidos',
      limite_nom: '10% del contenido energético total',
    },
    exceso_calorias: {
      nombre: 'EXCESO CALORÍAS',
      color: '#000000',
      icon: '⚠',
      descripcion: 'Alto contenido calórico',
      limite_nom: '275 kcal por 100g (sólidos) o 70 kcal por 100ml (líquidos)',
    },
    exceso_grasas_saturadas: {
      nombre: 'EXCESO GRASAS SATURADAS',
      color: '#000000',
      icon: '⚠',
      descripcion: 'Contiene más del 10% de grasas saturadas',
      limite_nom: '10% del contenido energético total',
    },
    exceso_grasas_trans: {
      nombre: 'EXCESO GRASAS TRANS',
      color: '#000000',
      icon: '⚠',
      descripcion: 'Contiene grasas trans industriales',
      limite_nom: '1% del contenido energético total',
    },
    exceso_sodio: {
      nombre: 'EXCESO SODIO',
      color: '#000000',
      icon: '⚠',
      descripcion: 'Alto contenido de sodio',
      limite_nom: '1mg por 1 kcal',
    },
  };

  // Get auth token from localStorage
  const getAuthToken = () => {
    const authData = localStorage.getItem('auth');
    if (authData) {
      try {
        const parsed = JSON.parse(authData);
        return parsed.access_token || parsed.token;
      } catch (e) {
        console.error('Error parsing auth data:', e);
      }
    }
    return null;
  };

  const handleScanModeChange = (event, newMode) => {
    if (newMode !== null) {
      setScanMode(newMode);
      setError(null);
      setBarcode('');
      setSelectedFile(null);
    }
  };

  const handleScanBarcode = async () => {
    if (!barcode.trim()) {
      setError('Por favor ingresa un código de barras válido');
      return;
    }

    setScanning(true);
    setError(null);

    try {
      const token = getAuthToken();
      if (!token) {
        throw new Error('No se encontró token de autenticación. Por favor inicia sesión.');
      }

      const data = await scanBarcode(barcode, token);
      const formattedData = formatProductData(data);
      setScannedProduct(formattedData);
      setCurrentTab(0);
    } catch (err) {
      console.error('Error scanning barcode:', err);
      setError(err.message || 'Error al escanear código de barras. Intenta de nuevo.');
    } finally {
      setScanning(false);
    }
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Validate file type
      const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
      if (!validTypes.includes(file.type)) {
        setError('Formato de archivo inválido. Por favor usa JPG, PNG o WEBP.');
        return;
      }

      // Validate file size (10MB max)
      const maxSize = 10 * 1024 * 1024;
      if (file.size > maxSize) {
        setError('El archivo es demasiado grande. Tamaño máximo: 10MB.');
        return;
      }

      setSelectedFile(file);
      setError(null);
    }
  };

  const handleScanLabel = async () => {
    if (!selectedFile) {
      setError('Por favor selecciona una imagen de la etiqueta del producto');
      return;
    }

    setScanning(true);
    setError(null);

    try {
      const token = getAuthToken();
      if (!token) {
        throw new Error('No se encontró token de autenticación. Por favor inicia sesión.');
      }

      const data = await scanLabel(selectedFile, token);
      const formattedData = formatProductData(data);
      setScannedProduct(formattedData);
      setCurrentTab(0);
    } catch (err) {
      console.error('Error scanning label:', err);
      setError(err.message || 'Error al escanear etiqueta. Asegúrate de que la foto muestre claramente la tabla nutricional.');
    } finally {
      setScanning(false);
    }
  };

  const handleCloseScan = () => {
    setScannedProduct(null);
    setBarcode('');
    setSelectedFile(null);
    setError(null);
  };

  const renderSello = (sello) => {
    const info = sellosInfo[sello.tipo];
    if (!info) return null;

    return (
      <MotionBox
        key={sello.tipo}
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: 'spring', stiffness: 200 }}
        sx={{ position: 'relative' }}
      >
        <Paper
          elevation={sello.activo ? 6 : 1}
          sx={{
            p: 2,
            background: sello.activo
              ? 'linear-gradient(135deg, #000000 0%, #2c2c2c 100%)'
              : 'linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 100%)',
            color: sello.activo ? 'white' : 'text.disabled',
            borderRadius: 2,
            textAlign: 'center',
            border: sello.activo ? '3px solid #000' : '2px solid #ccc',
            opacity: sello.activo ? 1 : 0.4,
            transition: 'all 0.3s ease',
            position: 'relative',
            overflow: 'hidden',
            '&::before': sello.activo ? {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              height: '6px',
              background: 'linear-gradient(90deg, #ff0000 0%, #ff6b00 100%)',
            } : {},
          }}
        >
          <Typography
            variant="caption"
            sx={{
              fontWeight: 900,
              fontSize: '0.65rem',
              letterSpacing: '0.5px',
              display: 'block',
              lineHeight: 1.2,
            }}
          >
            {info.nombre}
          </Typography>
          {sello.activo && (
            <Box sx={{ mt: 1 }}>
              <WarningIcon sx={{ fontSize: 24, color: '#ffd700' }} />
            </Box>
          )}
        </Paper>
      </MotionBox>
    );
  };

  const getHealthScoreColor = (score) => {
    if (score >= 80) return '#4CAF50';
    if (score >= 60) return '#FFC107';
    return '#F44336';
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <MotionPaper
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        elevation={0}
        sx={{
          p: 4,
          mb: 4,
          background: 'linear-gradient(135deg, #2196F3 0%, #1976D2 100%)',
          color: 'white',
          borderRadius: 3,
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <QrIcon sx={{ fontSize: 48 }} />
          <Box>
            <Typography variant="h3" fontWeight={700}>
              Escáner NOM-051
            </Typography>
            <Typography variant="h6" sx={{ opacity: 0.9 }}>
              Detecta sellos de advertencia en productos procesados
            </Typography>
          </Box>
        </Box>

        <Divider sx={{ my: 2, borderColor: 'rgba(255,255,255,0.2)' }} />

        <Grid container spacing={2}>
          <Grid item xs={12} sm={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" fontWeight={700}>
                7
              </Typography>
              <Typography variant="body2">Sellos de Advertencia</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" fontWeight={700}>
                NOM-051
              </Typography>
              <Typography variant="body2">Norma Oficial Mexicana</Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" fontWeight={700}>
                AI
              </Typography>
              <Typography variant="body2">Vision AI + OCR</Typography>
            </Box>
          </Grid>
        </Grid>
      </MotionPaper>

      {/* Scanner Interface */}
      {!scannedProduct && (
        <MotionPaper
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4 }}
          elevation={3}
          sx={{ p: 4, borderRadius: 3 }}
        >
          {/* Mode Selector */}
          <Box sx={{ mb: 4, textAlign: 'center' }}>
            <Typography variant="h6" gutterBottom fontWeight={700}>
              Selecciona el Modo de Escaneo
            </Typography>
            <ToggleButtonGroup
              value={scanMode}
              exclusive
              onChange={handleScanModeChange}
              sx={{ mt: 2 }}
            >
              <ToggleButton value="barcode" sx={{ px: 4, py: 1.5 }}>
                <QrIcon sx={{ mr: 1 }} />
                Código de Barras
              </ToggleButton>
              <ToggleButton value="label" sx={{ px: 4, py: 1.5 }}>
                <PhotoCameraIcon sx={{ mr: 1 }} />
                Etiqueta (Foto)
              </ToggleButton>
            </ToggleButtonGroup>
          </Box>

          <Divider sx={{ my: 3 }} />

          {/* Barcode Scanner */}
          {scanMode === 'barcode' && (
            <Box>
              <Typography variant="h6" gutterBottom fontWeight={700}>
                Escanear Código de Barras
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
                Ingresa el código de barras del producto (13 dígitos)
              </Typography>

              <Box
                sx={{
                  width: '100%',
                  maxWidth: 400,
                  mx: 'auto',
                  mb: 3,
                }}
              >
                <TextField
                  fullWidth
                  label="Código de Barras"
                  placeholder="7501234567890"
                  value={barcode}
                  onChange={(e) => setBarcode(e.target.value)}
                  disabled={scanning}
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      handleScanBarcode();
                    }
                  }}
                  sx={{ mb: 2 }}
                />
                <Button
                  fullWidth
                  variant="contained"
                  size="large"
                  startIcon={scanning ? <CircularProgress size={20} color="inherit" /> : <QrIcon />}
                  onClick={handleScanBarcode}
                  disabled={scanning || !barcode.trim()}
                  sx={{
                    py: 1.5,
                    fontSize: '1.1rem',
                    borderRadius: 2,
                    background: 'linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%)',
                    '&:hover': {
                      background: 'linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%)',
                    },
                  }}
                >
                  {scanning ? 'Buscando producto...' : 'Buscar Producto'}
                </Button>
              </Box>

              <Alert severity="info" sx={{ mt: 3 }}>
                <Typography variant="body2">
                  <strong>Base de datos:</strong> Busca en Open Food Facts (12,000+ productos mexicanos).
                  Si no encuentra el producto, prueba el modo de escaneo por foto.
                </Typography>
              </Alert>
            </Box>
          )}

          {/* Label Scanner */}
          {scanMode === 'label' && (
            <Box>
              <Typography variant="h6" gutterBottom fontWeight={700}>
                Escanear Etiqueta Nutricional
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom sx={{ mb: 3 }}>
                Toma una foto de la tabla nutricional del producto
              </Typography>

              <Box
                sx={{
                  width: '100%',
                  maxWidth: 400,
                  mx: 'auto',
                  mb: 3,
                }}
              >
                <Box
                  sx={{
                    width: '100%',
                    height: 250,
                    background: selectedFile
                      ? `url(${URL.createObjectURL(selectedFile)}) center/cover`
                      : 'linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%)',
                    borderRadius: 3,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    border: '3px dashed #ccc',
                    mb: 2,
                    position: 'relative',
                    overflow: 'hidden',
                  }}
                >
                  {!selectedFile && (
                    <Box sx={{ textAlign: 'center' }}>
                      <ImageIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 1 }} />
                      <Typography variant="body2" color="text.secondary">
                        Selecciona una imagen
                      </Typography>
                    </Box>
                  )}
                </Box>

                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/jpeg,image/jpg,image/png,image/webp"
                  onChange={handleFileSelect}
                  style={{ display: 'none' }}
                />

                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<PhotoCameraIcon />}
                  onClick={() => fileInputRef.current?.click()}
                  disabled={scanning}
                  sx={{ mb: 2 }}
                >
                  Seleccionar Imagen
                </Button>

                <Button
                  fullWidth
                  variant="contained"
                  size="large"
                  startIcon={scanning ? <CircularProgress size={20} color="inherit" /> : <CameraIcon />}
                  onClick={handleScanLabel}
                  disabled={scanning || !selectedFile}
                  sx={{
                    py: 1.5,
                    fontSize: '1.1rem',
                    borderRadius: 2,
                    background: 'linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%)',
                    '&:hover': {
                      background: 'linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%)',
                    },
                  }}
                >
                  {scanning ? 'Analizando imagen...' : 'Analizar Etiqueta'}
                </Button>
              </Box>

              <Alert severity="info" sx={{ mt: 3 }}>
                <Typography variant="body2">
                  <strong>Vision AI:</strong> Usa inteligencia artificial para leer la tabla nutricional.
                  Asegúrate de que la foto sea clara y muestre toda la información nutricional.
                </Typography>
              </Alert>
            </Box>
          )}

          {/* Error Display */}
          {error && (
            <Alert severity="error" sx={{ mt: 3 }} onClose={() => setError(null)}>
              {error}
            </Alert>
          )}

          {/* Loading State */}
          {scanning && (
            <Box sx={{ mt: 3, textAlign: 'center' }}>
              <LinearProgress sx={{ mb: 2 }} />
              <Typography variant="body2" color="text.secondary">
                {scanMode === 'barcode'
                  ? 'Buscando producto en la base de datos...'
                  : 'Extrayendo información nutricional con Vision AI...'}
              </Typography>
            </Box>
          )}
        </MotionPaper>
      )}

      {/* Results */}
      <AnimatePresence>
        {scannedProduct && (
          <MotionCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
            sx={{ borderRadius: 3, overflow: 'hidden' }}
          >
            {/* Header con producto */}
            <Box
              sx={{
                background: `linear-gradient(135deg, ${getHealthScoreColor(scannedProduct.health_score)} 0%, ${getHealthScoreColor(scannedProduct.health_score)}dd 100%)`,
                color: 'white',
                p: 3,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'flex-start',
              }}
            >
              <Box sx={{ flex: 1 }}>
                <Typography variant="h5" fontWeight={700}>
                  {scannedProduct.nombre}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.9, mt: 0.5 }}>
                  {scannedProduct.marca} • Código: {scannedProduct.codigo_barras}
                </Typography>
                <Box sx={{ mt: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Box>
                    <Typography variant="h3" fontWeight={700}>
                      {scannedProduct.health_score}
                    </Typography>
                    <Typography variant="caption">Puntuación</Typography>
                  </Box>
                  <Box>
                    <Chip
                      label={scannedProduct.health_level}
                      sx={{
                        bgcolor: 'rgba(255,255,255,0.3)',
                        color: 'white',
                        fontWeight: 700,
                      }}
                    />
                  </Box>
                </Box>

                {/* Estadísticas Globales del Producto */}
                <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {/* Badge: Producto Duplicado */}
                  {scannedProduct.is_duplicate && (
                    <Chip
                      icon={<AutoAwesomeIcon />}
                      label="Producto ya registrado"
                      size="small"
                      sx={{
                        bgcolor: 'rgba(255,255,255,0.25)',
                        color: 'white',
                        fontWeight: 600,
                        border: '1px solid rgba(255,255,255,0.4)',
                      }}
                    />
                  )}

                  {/* Chip: Número de escaneos */}
                  {scannedProduct.scan_count > 1 && (
                    <Chip
                      icon={<PeopleIcon />}
                      label={`Escaneado ${scannedProduct.scan_count} veces`}
                      size="small"
                      sx={{
                        bgcolor: 'rgba(255,255,255,0.25)',
                        color: 'white',
                        fontWeight: 600,
                        border: '1px solid rgba(255,255,255,0.4)',
                      }}
                    />
                  )}

                  {/* Badge: Verificado por nutriólogo */}
                  {scannedProduct.verified && (
                    <Chip
                      icon={<VerifiedIcon />}
                      label="Verificado por Nutriólogo"
                      size="small"
                      sx={{
                        bgcolor: 'rgba(33, 150, 243, 0.9)',
                        color: 'white',
                        fontWeight: 700,
                        border: '2px solid rgba(255,255,255,0.8)',
                      }}
                    />
                  )}

                  {/* Chip: Producto Global */}
                  {scannedProduct.is_global && (
                    <Chip
                      icon={<PublicIcon />}
                      label="Global"
                      size="small"
                      sx={{
                        bgcolor: 'rgba(255,255,255,0.25)',
                        color: 'white',
                        fontWeight: 600,
                        border: '1px solid rgba(255,255,255,0.4)',
                      }}
                    />
                  )}

                  {/* Chip: Confianza de IA (solo para escaneos con Vision AI) */}
                  {scannedProduct.confidence_score && scannedProduct.fuente === 'ai_vision' && (
                    <Chip
                      icon={<AutoAwesomeIcon />}
                      label={`IA: ${Math.round(scannedProduct.confidence_score)}% confianza`}
                      size="small"
                      sx={{
                        bgcolor: 'rgba(156, 39, 176, 0.9)',
                        color: 'white',
                        fontWeight: 600,
                        border: '1px solid rgba(255,255,255,0.4)',
                      }}
                    />
                  )}
                </Box>
              </Box>
              <IconButton onClick={handleCloseScan} sx={{ color: 'white' }}>
                <CloseIcon />
              </IconButton>
            </Box>

            {/* Tabs */}
            <Tabs
              value={currentTab}
              onChange={(e, newValue) => setCurrentTab(newValue)}
              sx={{ borderBottom: 1, borderColor: 'divider', px: 2 }}
            >
              <Tab label="Sellos de Advertencia" />
              <Tab label="Información Nutricional" />
            </Tabs>

            <CardContent sx={{ p: 3 }}>
              {/* Tab 0: Sellos de Advertencia */}
              {currentTab === 0 && (
                <Box>
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom fontWeight={700}>
                      Sellos de Advertencia Detectados
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Este producto presenta los siguientes sellos según la NOM-051
                    </Typography>
                  </Box>

                  <Grid container spacing={2} sx={{ mb: 4 }}>
                    {scannedProduct.sellos_advertencia.map((sello) => (
                      <Grid item xs={6} md={4} key={sello.tipo}>
                        {renderSello(sello)}
                      </Grid>
                    ))}
                  </Grid>

                  {/* Advertencias adicionales */}
                  {(scannedProduct.tiene_edulcorantes || scannedProduct.tiene_cafeina) && (
                    <Box sx={{ mb: 3 }}>
                      <Typography variant="subtitle1" fontWeight={700} gutterBottom>
                        Leyendas Precautorias
                      </Typography>
                      <Grid container spacing={1}>
                        {scannedProduct.tiene_edulcorantes && (
                          <Grid item xs={12} sm={6}>
                            <Chip
                              icon={<WarningIcon />}
                              label="Contiene Edulcorantes - No Recomendable en Niños"
                              color="warning"
                              sx={{ width: '100%' }}
                            />
                          </Grid>
                        )}
                        {scannedProduct.tiene_cafeina && (
                          <Grid item xs={12} sm={6}>
                            <Chip
                              icon={<WarningIcon />}
                              label="Contiene Cafeína - Evitar en Niños"
                              color="warning"
                              sx={{ width: '100%' }}
                            />
                          </Grid>
                        )}
                      </Grid>
                    </Box>
                  )}

                  {/* Resumen de riesgo */}
                  {scannedProduct.sellos_advertencia.filter((s) => s.activo).length > 0 ? (
                    <Alert severity="error" sx={{ mt: 3 }}>
                      <Typography variant="body2" fontWeight={700}>
                        Producto NO RECOMENDADO
                      </Typography>
                      <Typography variant="body2">
                        Este producto contiene{' '}
                        {scannedProduct.sellos_advertencia.filter((s) => s.activo).length} sello(s)
                        de advertencia. Se recomienda limitar su consumo y considerar alternativas
                        más saludables.
                      </Typography>
                    </Alert>
                  ) : (
                    <Alert severity="success" icon={<CheckCircleIcon />} sx={{ mt: 3 }}>
                      <Typography variant="body2" fontWeight={700}>
                        Producto SALUDABLE
                      </Typography>
                      <Typography variant="body2">
                        Este producto no presenta sellos de advertencia NOM-051.
                      </Typography>
                    </Alert>
                  )}

                  {/* Fuente de datos y estadísticas globales */}
                  <Box sx={{ mt: 3, pt: 2, borderTop: '1px solid #e0e0e0' }}>
                    <Typography variant="caption" color="text.secondary" display="block" gutterBottom>
                      <strong>Fuente:</strong>{' '}
                      {scannedProduct.fuente === 'open_food_facts' && 'Open Food Facts'}
                      {scannedProduct.fuente === 'ai_vision' && 'Vision AI (OCR)'}
                      {scannedProduct.fuente === 'local' && 'Base de datos local'}
                    </Typography>
                    {scannedProduct.is_duplicate && (
                      <Typography variant="caption" color="text.secondary" display="block">
                        Este producto ya existía en nuestra base de datos global. Tu escaneo se ha registrado
                        en tu historial personal.
                      </Typography>
                    )}
                    {!scannedProduct.is_duplicate && scannedProduct.fuente === 'ai_vision' && (
                      <Typography variant="caption" color="success.main" display="block">
                        ¡Gracias! Has agregado este producto a la base de datos global.
                        Ahora otros usuarios podrán beneficiarse de esta información.
                      </Typography>
                    )}
                  </Box>
                </Box>
              )}

              {/* Tab 1: Información Nutricional */}
              {currentTab === 1 && (
                <Box>
                  <Typography variant="h6" gutterBottom fontWeight={700}>
                    Información Nutricional
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Por porción de {scannedProduct.informacion_nutricional.porcion}
                  </Typography>

                  <List>
                    <ListItem>
                      <ListItemText
                        primary="Calorías"
                        secondary={`${scannedProduct.informacion_nutricional.calorias} kcal`}
                      />
                      {scannedProduct.sellos_advertencia.find(
                        (s) => s.tipo === 'exceso_calorias' && s.activo
                      ) && <WarningIcon color="error" />}
                    </ListItem>
                    <Divider />
                    <ListItem>
                      <ListItemText
                        primary="Proteínas"
                        secondary={`${scannedProduct.informacion_nutricional.proteinas_g}g`}
                      />
                    </ListItem>
                    <Divider />
                    <ListItem>
                      <ListItemText
                        primary="Carbohidratos"
                        secondary={`${scannedProduct.informacion_nutricional.carbohidratos_g}g`}
                      />
                    </ListItem>
                    <Divider />
                    <ListItem>
                      <ListItemText
                        primary="Azúcares"
                        secondary={`${scannedProduct.informacion_nutricional.azucares_g}g`}
                      />
                      {scannedProduct.sellos_advertencia.find(
                        (s) => s.tipo === 'exceso_azucares' && s.activo
                      ) && <WarningIcon color="error" />}
                    </ListItem>
                    <Divider />
                    <ListItem>
                      <ListItemText
                        primary="Grasas Saturadas"
                        secondary={`${scannedProduct.informacion_nutricional.grasas_saturadas_g}g`}
                      />
                      {scannedProduct.sellos_advertencia.find(
                        (s) => s.tipo === 'exceso_grasas_saturadas' && s.activo
                      ) && <WarningIcon color="error" />}
                    </ListItem>
                    <Divider />
                    <ListItem>
                      <ListItemText
                        primary="Grasas Trans"
                        secondary={`${scannedProduct.informacion_nutricional.grasas_trans_g}g`}
                      />
                      {scannedProduct.sellos_advertencia.find(
                        (s) => s.tipo === 'exceso_grasas_trans' && s.activo
                      ) && <WarningIcon color="error" />}
                    </ListItem>
                    <Divider />
                    <ListItem>
                      <ListItemText
                        primary="Fibra"
                        secondary={`${scannedProduct.informacion_nutricional.fibra_g}g`}
                      />
                    </ListItem>
                    <Divider />
                    <ListItem>
                      <ListItemText
                        primary="Sodio"
                        secondary={`${scannedProduct.informacion_nutricional.sodio_mg}mg`}
                      />
                      {scannedProduct.sellos_advertencia.find(
                        (s) => s.tipo === 'exceso_sodio' && s.activo
                      ) && <WarningIcon color="error" />}
                    </ListItem>
                  </List>

                  {/* Ingredientes si están disponibles */}
                  {scannedProduct.ingredientes && (
                    <Box sx={{ mt: 3, p: 2, bgcolor: 'background.default', borderRadius: 2 }}>
                      <Typography variant="subtitle2" fontWeight={700} gutterBottom>
                        Ingredientes
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {scannedProduct.ingredientes}
                      </Typography>
                    </Box>
                  )}
                </Box>
              )}
            </CardContent>

            {/* Footer con acciones */}
            <Box sx={{ p: 2, bgcolor: 'background.default', borderTop: '1px solid #e0e0e0' }}>
              <Button
                fullWidth
                variant="contained"
                startIcon={<CameraIcon />}
                onClick={handleCloseScan}
              >
                Escanear Otro Producto
              </Button>
            </Box>
          </MotionCard>
        )}
      </AnimatePresence>

      {/* Información sobre NOM-051 */}
      {!scannedProduct && !scanning && (
        <MotionPaper
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          sx={{ p: 3, mt: 3, borderRadius: 3 }}
        >
          <Typography variant="h6" gutterBottom fontWeight={700}>
            ¿Qué es la NOM-051?
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            La Norma Oficial Mexicana NOM-051 establece el etiquetado frontal de advertencia para
            productos procesados. Los 7 sellos de advertencia alertan sobre el exceso de:
          </Typography>
          <Grid container spacing={2}>
            {Object.entries(sellosInfo).map(([key, info]) => (
              <Grid item xs={12} sm={6} md={4} key={key}>
                <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-start' }}>
                  <WarningIcon color="warning" />
                  <Box>
                    <Typography variant="body2" fontWeight={700}>
                      {info.nombre}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {info.descripcion}
                    </Typography>
                  </Box>
                </Box>
              </Grid>
            ))}
            <Grid item xs={12} sm={6} md={4}>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-start' }}>
                <WarningIcon color="warning" />
                <Box>
                  <Typography variant="body2" fontWeight={700}>
                    CONTIENE EDULCORANTES
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    No recomendable para niños
                  </Typography>
                </Box>
              </Box>
            </Grid>
            <Grid item xs={12} sm={6} md={4}>
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-start' }}>
                <WarningIcon color="warning" />
                <Box>
                  <Typography variant="body2" fontWeight={700}>
                    CONTIENE CAFEÍNA
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Evitar en niños
                  </Typography>
                </Box>
              </Box>
            </Grid>
          </Grid>
        </MotionPaper>
      )}
    </Container>
  );
};

export default EscanerNOM051;
