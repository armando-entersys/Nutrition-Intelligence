import React, { useState, useMemo } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Grid,
  Chip,
  InputAdornment,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Avatar,
  Divider,
  Stack,
  Paper,
  IconButton,
  Collapse,
  Alert,
  AlertTitle,
} from '@mui/material';
import {
  Search as SearchIcon,
  Restaurant as RestaurantIcon,
  FilterList as FilterListIcon,
  LocalDining as LocalDiningIcon,
  EmojiNature as EmojiNatureIcon,
  WbSunny as WbSunnyIcon,
  AttachMoney as AttachMoneyIcon,
  Favorite as FavoriteIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import ALIMENTOS_MEXICANOS, {
  CATEGORIAS_EQUIVALENTES,
  getAlimentosPorCategoria,
  buscarAlimentos,
  getEstadisticasAlimentos,
} from '../../data/alimentosMexicanos';

const MotionCard = motion(Card);
const MotionBox = motion(Box);

// Mapeo de categorías a labels en español
const CATEGORIA_LABELS = {
  [CATEGORIAS_EQUIVALENTES.CEREALES_SIN_GRASA]: 'Cereales sin grasa',
  [CATEGORIAS_EQUIVALENTES.CEREALES_CON_GRASA]: 'Cereales con grasa',
  [CATEGORIAS_EQUIVALENTES.LEGUMINOSAS]: 'Leguminosas',
  [CATEGORIAS_EQUIVALENTES.VERDURAS]: 'Verduras',
  [CATEGORIAS_EQUIVALENTES.FRUTAS]: 'Frutas',
  [CATEGORIAS_EQUIVALENTES.LECHE_DESCREMADA]: 'Leche descremada',
  [CATEGORIAS_EQUIVALENTES.LECHE_SEMIDESCREMADA]: 'Leche semidescremada',
  [CATEGORIAS_EQUIVALENTES.LECHE_ENTERA]: 'Leche entera',
  [CATEGORIAS_EQUIVALENTES.CARNES_MUY_BAJO]: 'Carnes (muy bajo aporte)',
  [CATEGORIAS_EQUIVALENTES.CARNES_BAJO]: 'Carnes (bajo aporte)',
  [CATEGORIAS_EQUIVALENTES.CARNES_MODERADO]: 'Carnes (moderado aporte)',
  [CATEGORIAS_EQUIVALENTES.CARNES_ALTO]: 'Carnes (alto aporte)',
  [CATEGORIAS_EQUIVALENTES.GRASAS_SIN_PROTEINA]: 'Grasas sin proteína',
  [CATEGORIAS_EQUIVALENTES.GRASAS_CON_PROTEINA]: 'Grasas con proteína',
  [CATEGORIAS_EQUIVALENTES.AZUCARES_SIN_GRASA]: 'Azúcares sin grasa',
  [CATEGORIAS_EQUIVALENTES.AZUCARES_CON_GRASA]: 'Azúcares con grasa',
  [CATEGORIAS_EQUIVALENTES.BEBIDA_LIBRE]: 'Bebidas libres',
};

// Colores por categoría
const CATEGORIA_COLORS = {
  [CATEGORIAS_EQUIVALENTES.CEREALES_SIN_GRASA]: '#FFB84D',
  [CATEGORIAS_EQUIVALENTES.LEGUMINOSAS]: '#8D6E63',
  [CATEGORIAS_EQUIVALENTES.VERDURAS]: '#66BB6A',
  [CATEGORIAS_EQUIVALENTES.FRUTAS]: '#FF6F00',
  [CATEGORIAS_EQUIVALENTES.GRASAS_CON_PROTEINA]: '#4CAF50',
  [CATEGORIAS_EQUIVALENTES.BEBIDA_LIBRE]: '#0288D1',
};

const EquivalentesMexicanos = () => {
  const [busqueda, setBusqueda] = useState('');
  const [categoriaFiltro, setCategoriaFiltro] = useState('todas');
  const [soloTradicionales, setSoloTradicionales] = useState(false);
  const [alimentoExpandido, setAlimentoExpandido] = useState(null);
  const estadisticas = getEstadisticasAlimentos();

  // Filtrar alimentos
  const alimentosFiltrados = useMemo(() => {
    let resultado = ALIMENTOS_MEXICANOS;

    // Filtro por búsqueda
    if (busqueda) {
      resultado = buscarAlimentos(busqueda);
    }

    // Filtro por categoría
    if (categoriaFiltro !== 'todas') {
      resultado = resultado.filter(
        (a) => a.categoria_equivalente === categoriaFiltro
      );
    }

    // Filtro solo tradicionales
    if (soloTradicionales) {
      resultado = resultado.filter((a) => a.es_tradicional_mexicano);
    }

    return resultado;
  }, [busqueda, categoriaFiltro, soloTradicionales]);

  const handleExpandir = (id) => {
    setAlimentoExpandido(alimentoExpandido === id ? null : id);
  };

  return (
    <Box sx={{ py: 4 }}>
      {/* Header con estadísticas */}
      <MotionBox
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Paper
          elevation={0}
          sx={{
            p: 4,
            mb: 4,
            background: 'linear-gradient(135deg, #4CAF50 0%, #81C784 100%)',
            color: 'white',
            borderRadius: 4,
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
            <Avatar sx={{ width: 64, height: 64, bgcolor: 'rgba(255,255,255,0.2)' }}>
              <RestaurantIcon sx={{ fontSize: 36 }} />
            </Avatar>
            <Box>
              <Typography variant="h3" fontWeight={700} gutterBottom>
                Alimentos Mexicanos
              </Typography>
              <Typography variant="body1" sx={{ opacity: 0.9 }}>
                Sistema de Equivalentes Mexicano - Basado en NOM
              </Typography>
            </Box>
          </Box>

          <Grid container spacing={2} sx={{ mt: 2 }}>
            <Grid item xs={12} sm={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" fontWeight={700}>
                  {estadisticas.totalAlimentos}
                </Typography>
                <Typography variant="body2">Total de alimentos</Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" fontWeight={700}>
                  {estadisticas.alimentosTradicionales}
                </Typography>
                <Typography variant="body2">Tradicionales</Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" fontWeight={700}>
                  {estadisticas.categorias}
                </Typography>
                <Typography variant="body2">Categorías</Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h4" fontWeight={700}>
                  {estadisticas.porcentajeTradicional}%
                </Typography>
                <Typography variant="body2">México ancestral</Typography>
              </Box>
            </Grid>
          </Grid>
        </Paper>
      </MotionBox>

      {/* Filtros */}
      <MotionBox
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card elevation={2} sx={{ p: 3, mb: 4, borderRadius: 3 }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={5}>
              <TextField
                fullWidth
                placeholder="Buscar alimentos mexicanos..."
                value={busqueda}
                onChange={(e) => setBusqueda(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon color="primary" />
                    </InputAdornment>
                  ),
                }}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: 2,
                  },
                }}
              />
            </Grid>

            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Categoría</InputLabel>
                <Select
                  value={categoriaFiltro}
                  label="Categoría"
                  onChange={(e) => setCategoriaFiltro(e.target.value)}
                  startAdornment={
                    <InputAdornment position="start">
                      <FilterListIcon />
                    </InputAdornment>
                  }
                  sx={{ borderRadius: 2 }}
                >
                  <MenuItem value="todas">Todas las categorías</MenuItem>
                  <Divider />
                  {Object.entries(CATEGORIA_LABELS).map(([value, label]) => (
                    <MenuItem key={value} value={value}>
                      {label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} md={3}>
              <Chip
                icon={<EmojiNatureIcon />}
                label="Solo Tradicionales"
                onClick={() => setSoloTradicionales(!soloTradicionales)}
                color={soloTradicionales ? 'success' : 'default'}
                variant={soloTradicionales ? 'filled' : 'outlined'}
                sx={{
                  width: '100%',
                  height: 56,
                  fontSize: '0.95rem',
                  transition: 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
                  '&:hover': {
                    transform: 'translateY(-2px)',
                  },
                }}
              />
            </Grid>
          </Grid>

          {/* Contador de resultados */}
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Mostrando <strong>{alimentosFiltrados.length}</strong> alimento(s)
            </Typography>
          </Box>
        </Card>
      </MotionBox>

      {/* Grid de alimentos */}
      <Grid container spacing={3}>
        <AnimatePresence>
          {alimentosFiltrados.map((alimento, index) => (
            <Grid item xs={12} sm={6} md={4} key={alimento.id}>
              <MotionCard
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{
                  duration: 0.3,
                  delay: index * 0.05,
                  type: 'spring',
                  stiffness: 100,
                }}
                elevation={2}
                sx={{
                  height: '100%',
                  borderRadius: 3,
                  overflow: 'visible',
                  transition: 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: 6,
                  },
                }}
              >
                <CardContent>
                  {/* Header del alimento */}
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2, mb: 2 }}>
                    <Avatar
                      sx={{
                        width: 56,
                        height: 56,
                        bgcolor:
                          CATEGORIA_COLORS[alimento.categoria_equivalente] || 'primary.main',
                      }}
                    >
                      <LocalDiningIcon sx={{ fontSize: 32 }} />
                    </Avatar>
                    <Box sx={{ flex: 1 }}>
                      <Typography variant="h6" fontWeight={600} gutterBottom>
                        {alimento.nombre}
                      </Typography>
                      <Stack direction="row" spacing={0.5} sx={{ flexWrap: 'wrap', gap: 0.5 }}>
                        {alimento.es_tradicional_mexicano && (
                          <Chip
                            label="🇲🇽 Tradicional"
                            size="small"
                            color="success"
                            sx={{ height: 20, fontSize: '0.7rem' }}
                          />
                        )}
                        <Chip
                          label={CATEGORIA_LABELS[alimento.categoria_equivalente]}
                          size="small"
                          variant="outlined"
                          sx={{ height: 20, fontSize: '0.7rem' }}
                        />
                      </Stack>
                    </Box>
                  </Box>

                  {/* Información básica */}
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {alimento.descripcion}
                    </Typography>

                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                      <Typography variant="body2" fontWeight={600} color="primary">
                        Porción:
                      </Typography>
                      <Typography variant="body2">{alimento.cantidad_porcion}</Typography>
                    </Box>

                    <Grid container spacing={1}>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          Calorías: <strong>{alimento.calorias} kcal</strong>
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          Proteína: <strong>{alimento.proteina_g}g</strong>
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          Carbos: <strong>{alimento.carbohidratos_g}g</strong>
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          Grasas: <strong>{alimento.grasa_g}g</strong>
                        </Typography>
                      </Grid>
                    </Grid>
                  </Box>

                  {/* Información detallada colapsable */}
                  <Box>
                    <IconButton
                      onClick={() => handleExpandir(alimento.id)}
                      sx={{
                        width: '100%',
                        borderRadius: 2,
                        bgcolor: 'action.hover',
                        '&:hover': { bgcolor: 'action.selected' },
                      }}
                    >
                      <Typography variant="body2" fontWeight={500} sx={{ mr: 1 }}>
                        {alimentoExpandido === alimento.id ? 'Ocultar' : 'Ver'} detalles
                      </Typography>
                      {alimentoExpandido === alimento.id ? (
                        <ExpandLessIcon />
                      ) : (
                        <ExpandMoreIcon />
                      )}
                    </IconButton>

                    <Collapse in={alimentoExpandido === alimento.id}>
                      <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.50', borderRadius: 2 }}>
                        <Typography variant="subtitle2" gutterBottom fontWeight={600}>
                          Información nutricional completa:
                        </Typography>
                        <Grid container spacing={1}>
                          <Grid item xs={6}>
                            <Typography variant="caption">Fibra: {alimento.fibra_g}g</Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="caption">
                              Calcio: {alimento.calcio_mg}mg
                            </Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="caption">
                              Hierro: {alimento.hierro_mg}mg
                            </Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="caption">
                              Vit C: {alimento.vitamina_c_mg}mg
                            </Typography>
                          </Grid>
                        </Grid>

                        <Divider sx={{ my: 1.5 }} />

                        <Typography variant="subtitle2" gutterBottom fontWeight={600}>
                          Contexto mexicano:
                        </Typography>
                        <Stack spacing={0.5}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <WbSunnyIcon fontSize="small" color="warning" />
                            <Typography variant="caption">
                              Temporada: {alimento.temporada.join(', ')}
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <EmojiNatureIcon fontSize="small" color="success" />
                            <Typography variant="caption">
                              Región: {alimento.region_origen.join(', ')}
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <AttachMoneyIcon fontSize="small" color="info" />
                            <Typography variant="caption">
                              Costo: {alimento.costo_relativo}
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <FavoriteIcon fontSize="small" color="error" />
                            <Typography variant="caption">
                              IG: {alimento.indice_glucemico} | CG: {alimento.carga_glucemica}
                            </Typography>
                          </Box>
                        </Stack>
                      </Box>
                    </Collapse>
                  </Box>
                </CardContent>
              </MotionCard>
            </Grid>
          ))}
        </AnimatePresence>
      </Grid>

      {/* Mensaje si no hay resultados */}
      {alimentosFiltrados.length === 0 && (
        <MotionBox
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <Alert
            severity="info"
            sx={{
              mt: 4,
              borderRadius: 3,
            }}
          >
            <AlertTitle>No se encontraron alimentos</AlertTitle>
            Intenta cambiar los filtros o la búsqueda para encontrar más alimentos mexicanos.
          </Alert>
        </MotionBox>
      )}
    </Box>
  );
};

export default EquivalentesMexicanos;
