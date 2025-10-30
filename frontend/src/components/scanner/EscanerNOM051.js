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
  ListItemIcon,
  Collapse,
} from '@mui/material';
import {
  CameraAlt as CameraIcon,
  QrCodeScanner as QrIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Close as CloseIcon,
  CompareArrows as CompareIcon,
  TipsAndUpdates as TipsIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';

const MotionPaper = motion(Paper);
const MotionCard = motion(Card);
const MotionBox = motion(Box);

/**
 * EscanerNOM051 - Escáner de Etiquetas según NOM-051
 *
 * Sistema para escanear productos y evaluar su cumplimiento con la NOM-051
 * Detecta los 5 sellos de advertencia y sugiere alternativas más saludables
 */
const EscanerNOM051 = () => {
  const [scanning, setScanning] = useState(false);
  const [scannedProduct, setScannedProduct] = useState(null);
  const [currentTab, setCurrentTab] = useState(0);
  const [showAlternatives, setShowAlternatives] = useState(false);
  const videoRef = useRef(null);

  // Simulación de productos para demostración
  const productosDemo = [
    {
      id: 'prod_001',
      nombre: 'Refresco de Cola Regular 600ml',
      marca: 'Marca Demo',
      codigo_barras: '7501234567890',
      informacion_nutricional: {
        porcion: '100ml',
        calorias: 42,
        azucares_g: 10.6,
        grasas_saturadas_g: 0,
        grasas_trans_g: 0,
        sodio_mg: 10,
      },
      sellos_advertencia: [
        { tipo: 'exceso_azucares', activo: true },
        { tipo: 'exceso_calorias', activo: false },
        { tipo: 'exceso_grasas_saturadas', activo: false },
        { tipo: 'exceso_grasas_trans', activo: false },
        { tipo: 'exceso_sodio', activo: false },
      ],
      tiene_edulcorantes: false,
      tiene_cafeina: true,
      alternativas_saludables: ['prod_alt_001', 'prod_alt_002'],
      imagen_url: '/images/productos/refresco-cola.jpg',
    },
    {
      id: 'prod_002',
      nombre: 'Galletas con Chispas de Chocolate',
      marca: 'Marca Demo',
      codigo_barras: '7501234567891',
      informacion_nutricional: {
        porcion: '30g (3 galletas)',
        calorias: 145,
        azucares_g: 8.5,
        grasas_saturadas_g: 3.2,
        grasas_trans_g: 0.1,
        sodio_mg: 95,
      },
      sellos_advertencia: [
        { tipo: 'exceso_azucares', activo: true },
        { tipo: 'exceso_calorias', activo: true },
        { tipo: 'exceso_grasas_saturadas', activo: true },
        { tipo: 'exceso_grasas_trans', activo: false },
        { tipo: 'exceso_sodio', activo: false },
      ],
      tiene_edulcorantes: false,
      tiene_cafeina: false,
      alternativas_saludables: ['prod_alt_003', 'prod_alt_004'],
      imagen_url: '/images/productos/galletas-chocolate.jpg',
    },
  ];

  const alternativasDemo = {
    prod_alt_001: {
      nombre: 'Agua Simple Natural',
      sellos: 0,
      beneficio: 'Sin calorías, sin azúcares, hidratación pura',
    },
    prod_alt_002: {
      nombre: 'Agua de Jamaica sin Azúcar',
      sellos: 0,
      beneficio: 'Antioxidantes naturales, sin calorías añadidas',
    },
    prod_alt_003: {
      nombre: 'Galletas de Avena Integral',
      sellos: 0,
      beneficio: 'Alto contenido de fibra, endulzadas con miel',
    },
    prod_alt_004: {
      nombre: 'Amaranto con Miel',
      sellos: 1,
      beneficio: 'Proteína de alta calidad, superalimento mexicano',
    },
  };

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

  const handleScanDemo = () => {
    setScanning(true);
    // Simular escaneo con un pequeño delay
    setTimeout(() => {
      const productoAleatorio = productosDemo[Math.floor(Math.random() * productosDemo.length)];
      setScannedProduct(productoAleatorio);
      setScanning(false);
      setCurrentTab(0);
    }, 2000);
  };

  const handleCloseScan = () => {
    setScannedProduct(null);
    setShowAlternatives(false);
  };

  const renderSello = (sello) => {
    const info = sellosInfo[sello.tipo];
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
                5
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
                100%
              </Typography>
              <Typography variant="body2">Cumplimiento Legal</Typography>
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
          <Box sx={{ textAlign: 'center' }}>
            <Box
              sx={{
                width: '100%',
                maxWidth: 400,
                height: 300,
                mx: 'auto',
                mb: 3,
                background: 'linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%)',
                borderRadius: 3,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                position: 'relative',
                overflow: 'hidden',
                border: '3px dashed #ccc',
              }}
            >
              {scanning ? (
                <Box sx={{ textAlign: 'center' }}>
                  <CameraIcon sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
                  <Typography variant="h6" color="text.secondary">
                    Escaneando producto...
                  </Typography>
                  <LinearProgress sx={{ mt: 2, width: 200 }} />
                </Box>
              ) : (
                <Box sx={{ textAlign: 'center' }}>
                  <QrIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h6" color="text.secondary">
                    Coloca el código de barras aquí
                  </Typography>
                </Box>
              )}
            </Box>

            <Button
              variant="contained"
              size="large"
              startIcon={<CameraIcon />}
              onClick={handleScanDemo}
              disabled={scanning}
              sx={{
                py: 1.5,
                px: 4,
                fontSize: '1.1rem',
                borderRadius: 2,
                background: 'linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%)',
                },
              }}
            >
              {scanning ? 'Escaneando...' : 'Escanear Producto (Demo)'}
            </Button>

            <Alert severity="info" sx={{ mt: 3 }}>
              <Typography variant="body2">
                <strong>Modo demostración:</strong> Esta funcionalidad muestra productos de ejemplo.
                La versión completa integrará OCR real y base de datos de productos.
              </Typography>
            </Alert>
          </Box>
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
                background: 'linear-gradient(135deg, #1976D2 0%, #0D47A1 100%)',
                color: 'white',
                p: 3,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'flex-start',
              }}
            >
              <Box>
                <Typography variant="h5" fontWeight={700}>
                  {scannedProduct.nombre}
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.9, mt: 0.5 }}>
                  {scannedProduct.marca} • Código: {scannedProduct.codigo_barras}
                </Typography>
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
              <Tab label="Alternativas Saludables" />
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

                  {/* Resumen de riesgo */}
                  {scannedProduct.sellos_advertencia.filter((s) => s.activo).length > 0 && (
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
                  )}
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
                        primary="Sodio"
                        secondary={`${scannedProduct.informacion_nutricional.sodio_mg}mg`}
                      />
                      {scannedProduct.sellos_advertencia.find(
                        (s) => s.tipo === 'exceso_sodio' && s.activo
                      ) && <WarningIcon color="error" />}
                    </ListItem>
                  </List>
                </Box>
              )}

              {/* Tab 2: Alternativas Saludables */}
              {currentTab === 2 && (
                <Box>
                  <Typography variant="h6" gutterBottom fontWeight={700}>
                    Alternativas Más Saludables
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Productos similares con menos sellos de advertencia
                  </Typography>

                  <Grid container spacing={2} sx={{ mt: 2 }}>
                    {scannedProduct.alternativas_saludables.map((altId) => {
                      const alt = alternativasDemo[altId];
                      return (
                        <Grid item xs={12} sm={6} key={altId}>
                          <MotionCard
                            whileHover={{ scale: 1.02 }}
                            sx={{
                              p: 2,
                              border: '2px solid',
                              borderColor: alt.sellos === 0 ? 'success.main' : 'warning.main',
                              borderRadius: 2,
                              cursor: 'pointer',
                            }}
                          >
                            <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                              <CheckCircleIcon
                                sx={{
                                  fontSize: 40,
                                  color: alt.sellos === 0 ? 'success.main' : 'warning.main',
                                }}
                              />
                              <Box sx={{ flex: 1 }}>
                                <Typography variant="subtitle1" fontWeight={700}>
                                  {alt.nombre}
                                </Typography>
                                <Chip
                                  size="small"
                                  label={`${alt.sellos} sellos`}
                                  color={alt.sellos === 0 ? 'success' : 'warning'}
                                  sx={{ mt: 1 }}
                                />
                                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                                  {alt.beneficio}
                                </Typography>
                              </Box>
                            </Box>
                          </MotionCard>
                        </Grid>
                      );
                    })}
                  </Grid>

                  <Alert severity="success" icon={<TipsIcon />} sx={{ mt: 3 }}>
                    <Typography variant="body2" fontWeight={700}>
                      Consejo Nutricional
                    </Typography>
                    <Typography variant="body2">
                      Prioriza alimentos con menos sellos de advertencia. Los productos sin sellos
                      son más saludables para ti y tu familia.
                    </Typography>
                  </Alert>
                </Box>
              )}
            </CardContent>

            {/* Footer con acciones */}
            <Box sx={{ p: 2, bgcolor: 'background.default', borderTop: '1px solid #e0e0e0' }}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<CompareIcon />}
                    onClick={() => setCurrentTab(2)}
                  >
                    Ver Alternativas
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<CameraIcon />}
                    onClick={handleScanDemo}
                  >
                    Escanear Otro Producto
                  </Button>
                </Grid>
              </Grid>
            </Box>
          </MotionCard>
        )}
      </AnimatePresence>

      {/* Información sobre NOM-051 */}
      {!scannedProduct && (
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
            productos procesados. Los 5 sellos de advertencia alertan sobre el exceso de:
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
          </Grid>
        </MotionPaper>
      )}
    </Container>
  );
};

export default EscanerNOM051;
