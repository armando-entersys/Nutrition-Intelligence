import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  Alert,
  LinearProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  MonitorWeight as MonitorWeightIcon,
  Height as HeightIcon,
  FitnessCenter as FitnessCenterIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Psychology as PsychologyIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const MedicionesAntropometricasView = ({ paciente }) => {
  const medicion = paciente.mediciones_antropometricas[0];

  const getIMCColor = (imc) => {
    if (imc < 18.5) return '#3498db';
    if (imc < 25) return '#2ecc71';
    if (imc < 30) return '#f39c12';
    return '#e74c3c';
  };

  const MetricCard = ({ title, value, unit, subtitle, icon, color }) => (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <Card sx={{ height: '100%', borderRadius: 3, boxShadow: 2 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
            <Box>
              <Typography variant="caption" color="text.secondary" fontWeight="600">
                {title}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'baseline', gap: 0.5 }}>
                <Typography variant="h3" fontWeight="700" color={color || 'text.primary'}>
                  {value}
                </Typography>
                <Typography variant="h6" color="text.secondary">
                  {unit}
                </Typography>
              </Box>
              {subtitle && (
                <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                  {subtitle}
                </Typography>
              )}
            </Box>
            <Box
              sx={{
                bgcolor: color || '#006847',
                color: 'white',
                p: 1,
                borderRadius: 2,
                display: 'flex',
              }}
            >
              {icon}
            </Box>
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );

  return (
    <Box>
      <Grid container spacing={3}>
        {/* Mediciones Principales */}
        <Grid item xs={12} md={3}>
          <MetricCard
            title="Peso Corporal"
            value={medicion.peso_kg}
            unit="kg"
            subtitle={new Date(medicion.fecha_medicion).toLocaleDateString('es-MX')}
            icon={<MonitorWeightIcon />}
            color="#006847"
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <MetricCard
            title="Talla"
            value={medicion.talla_cm}
            unit="cm"
            icon={<HeightIcon />}
            color="#2196F3"
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <MetricCard
            title="IMC"
            value={medicion.imc}
            unit="kg/m²"
            subtitle={medicion.interpretacion_imc}
            icon={<FitnessCenterIcon />}
            color={getIMCColor(medicion.imc)}
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <MetricCard
            title="Grasa Corporal"
            value={medicion.porcentaje_grasa || 'N/A'}
            unit="%"
            subtitle={medicion.masa_grasa_kg ? `${medicion.masa_grasa_kg.toFixed(1)} kg` : ''}
            icon={<FitnessCenterIcon />}
            color="#FF6B35"
          />
        </Grid>

        {/* Circunferencias */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <Card sx={{ borderRadius: 3, boxShadow: 2 }}>
              <CardContent>
                <Typography variant="h6" fontWeight="700" gutterBottom>
                  Circunferencias Corporales
                </Typography>
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell><strong>Medición</strong></TableCell>
                        <TableCell align="right"><strong>Valor (cm)</strong></TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      <TableRow>
                        <TableCell>Cintura</TableCell>
                        <TableCell align="right">{medicion.circunferencia_cintura_cm}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Cadera</TableCell>
                        <TableCell align="right">{medicion.circunferencia_cadera_cm}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Brazo</TableCell>
                        <TableCell align="right">{medicion.circunferencia_brazo_cm}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Pantorrilla</TableCell>
                        <TableCell align="right">{medicion.circunferencia_pantorrilla_cm}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Cuello</TableCell>
                        <TableCell align="right">{medicion.circunferencia_cuello_cm}</TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>

                <Box sx={{ mt: 2, p: 2, bgcolor: '#F8F9FA', borderRadius: 2 }}>
                  <Typography variant="subtitle2" fontWeight="700" gutterBottom>
                    Índices Calculados
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2">Índice Cintura-Cadera:</Typography>
                    <Chip
                      label={medicion.indice_cintura_cadera.toFixed(2)}
                      size="small"
                      color={medicion.indice_cintura_cadera > 0.9 ? 'error' : 'success'}
                    />
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography variant="body2">Índice Cintura-Talla:</Typography>
                    <Chip
                      label={medicion.indice_cintura_talla.toFixed(2)}
                      size="small"
                      color={medicion.indice_cintura_talla > 0.5 ? 'error' : 'success'}
                    />
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Composición Corporal */}
        <Grid item xs={12} md={6}>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <Card sx={{ borderRadius: 3, boxShadow: 2 }}>
              <CardContent>
                <Typography variant="h6" fontWeight="700" gutterBottom>
                  Composición Corporal
                </Typography>

                {medicion.porcentaje_grasa && (
                  <>
                    <Box sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="body2">Grasa Corporal</Typography>
                        <Typography variant="body2" fontWeight="600">{medicion.porcentaje_grasa}%</Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={medicion.porcentaje_grasa}
                        sx={{
                          height: 12,
                          borderRadius: 2,
                          bgcolor: '#E0E0E0',
                          '& .MuiLinearProgress-bar': {
                            bgcolor: '#FF6B35',
                            borderRadius: 2,
                          },
                        }}
                      />
                    </Box>

                    <TableContainer>
                      <Table size="small">
                        <TableBody>
                          <TableRow>
                            <TableCell>Masa Grasa</TableCell>
                            <TableCell align="right">{medicion.masa_grasa_kg?.toFixed(1)} kg</TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>Masa Libre de Grasa</TableCell>
                            <TableCell align="right">{medicion.masa_libre_grasa_kg?.toFixed(1)} kg</TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell>Masa Muscular</TableCell>
                            <TableCell align="right">{medicion.masa_muscular_kg?.toFixed(1)} kg</TableCell>
                          </TableRow>
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </>
                )}

                {medicion.somatotipo && (
                  <Box sx={{ mt: 2, p: 2, bgcolor: '#F8F9FA', borderRadius: 2 }}>
                    <Typography variant="subtitle2" fontWeight="700" gutterBottom>
                      Somatotipo (Heath-Carter)
                    </Typography>
                    <Typography variant="body2">
                      <strong>{medicion.somatotipo}</strong>
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Análisis IA */}
        {medicion.analisis_ia && (
          <Grid item xs={12}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.2 }}
            >
              <Card
                sx={{
                  borderRadius: 3,
                  boxShadow: 2,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                    <PsychologyIcon sx={{ fontSize: 32, mr: 1.5 }} />
                    <Typography variant="h6" fontWeight="700">
                      Análisis Inteligente Antropométrico (IA)
                    </Typography>
                  </Box>

                  <Grid container spacing={3}>
                    <Grid item xs={12} md={4}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Typography variant="caption" sx={{ opacity: 0.9 }}>
                          Tendencia de Peso
                        </Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                          <TrendingUpIcon />
                          <Typography variant="h5" fontWeight="700">
                            {medicion.analisis_ia.tendencia_peso}
                          </Typography>
                        </Box>
                        <Typography variant="caption" sx={{ opacity: 0.9, mt: 1, display: 'block' }}>
                          Predicción 30 días: {medicion.analisis_ia.prediccion_peso_30d} kg
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={4}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Typography variant="caption" sx={{ opacity: 0.9 }}>
                          Riesgo de Obesidad
                        </Typography>
                        <Typography variant="h5" fontWeight="700" sx={{ mt: 0.5 }}>
                          {medicion.analisis_ia.riesgo_obesidad}%
                        </Typography>
                        <Box sx={{ mt: 1, bgcolor: 'rgba(255,255,255,0.2)', borderRadius: 1, overflow: 'hidden' }}>
                          <Box
                            sx={{
                              width: `${medicion.analisis_ia.riesgo_obesidad}%`,
                              height: 8,
                              bgcolor: medicion.analisis_ia.riesgo_obesidad > 70
                                ? '#ff6b6b'
                                : medicion.analisis_ia.riesgo_obesidad > 50
                                ? '#ffd93d'
                                : '#6bcf7f',
                            }}
                          />
                        </Box>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={4}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Typography variant="caption" sx={{ opacity: 0.9 }}>
                          Distribución de Grasa
                        </Typography>
                        <Typography variant="h5" fontWeight="700" sx={{ mt: 0.5 }}>
                          {medicion.analisis_ia.distribucion_grasa}
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={6}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Typography variant="subtitle2" fontWeight="700" gutterBottom>
                          Recomendaciones de Ejercicio
                        </Typography>
                        <Box component="ul" sx={{ m: 0, pl: 2 }}>
                          {medicion.analisis_ia.recomendaciones_ejercicio.map((rec, index) => (
                            <Typography key={index} component="li" variant="body2" sx={{ mb: 0.5 }}>
                              {rec}
                            </Typography>
                          ))}
                        </Box>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={6}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                          <WarningIcon />
                          <Typography variant="subtitle2" fontWeight="700">
                            Alertas
                          </Typography>
                        </Box>
                        <Box component="ul" sx={{ m: 0, pl: 2 }}>
                          {medicion.analisis_ia.alertas.map((alerta, index) => (
                            <Typography key={index} component="li" variant="body2" sx={{ mb: 0.5 }}>
                              {alerta}
                            </Typography>
                          ))}
                        </Box>
                      </Box>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default MedicionesAntropometricasView;
