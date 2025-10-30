import React from 'react';
import { Box, Typography, Grid, Card, CardContent, Chip, LinearProgress, List, ListItem, ListItemText } from '@mui/material';
import { DirectionsRun, FitnessCenter, DirectionsWalk, Psychology, Warning, CheckCircle } from '@mui/icons-material';
import { motion } from 'framer-motion';

const ActividadFisicaView = ({ paciente }) => {
  const { actividad_fisica } = paciente;

  const InfoCard = ({ icon, title, children, color = '#006847' }) => (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
      <Card sx={{ height: '100%', borderRadius: 3, boxShadow: 2 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Box sx={{ bgcolor: color, color: 'white', p: 1, borderRadius: 2, display: 'flex', mr: 1.5 }}>{icon}</Box>
            <Typography variant="h6" fontWeight="700">{title}</Typography>
          </Box>
          {children}
        </CardContent>
      </Card>
    </motion.div>
  );

  const getNivelActividadColor = (nivel) => {
    const colores = { sedentario: '#E63946', ligero: '#FF9800', moderado: '#FFD93D', vigoroso: '#2ecc71' };
    return colores[nivel] || '#757575';
  };

  return (
    <Box>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <InfoCard icon={<DirectionsRun />} title="Nivel de Actividad">
            <Box sx={{ mb: 2 }}>
              <Chip
                label={actividad_fisica.nivel_actividad.toUpperCase()}
                sx={{ bgcolor: getNivelActividadColor(actividad_fisica.nivel_actividad), color: 'white', fontWeight: 600 }}
              />
            </Box>
            <Typography variant="body2"><strong>Tipo de trabajo:</strong> {actividad_fisica.trabajo_tipo}</Typography>
            <Typography variant="body2"><strong>Horas sentado/día:</strong> {actividad_fisica.horas_sentado_dia}</Typography>
            <Typography variant="body2"><strong>Camina diario:</strong> {actividad_fisica.camina_diario_min} min</Typography>
            {actividad_fisica.pasos_promedio_dia && (
              <Typography variant="body2"><strong>Pasos promedio:</strong> {actividad_fisica.pasos_promedio_dia.toLocaleString()} pasos/día</Typography>
            )}
          </InfoCard>
        </Grid>

        <Grid item xs={12} md={6}>
          <InfoCard icon={<FitnessCenter />} title="Ejercicio Estructurado" color="#E91E63">
            <Typography variant="body2"><strong>Realiza ejercicio:</strong> {actividad_fisica.realiza_ejercicio ? 'Sí' : 'No'}</Typography>
            {actividad_fisica.realiza_ejercicio && (
              <>
                <Typography variant="body2"><strong>Frecuencia:</strong> {actividad_fisica.frecuencia_semanal} veces/semana</Typography>
                <Typography variant="body2"><strong>Duración:</strong> {actividad_fisica.duracion_promedio_min} min</Typography>
                <Box sx={{ mt: 2 }}>
                  {actividad_fisica.tipo_ejercicio.map((tipo, i) => (
                    <Chip key={i} label={tipo} size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                  ))}
                </Box>
              </>
            )}
            {actividad_fisica.practica_deporte && (
              <Box sx={{ mt: 2 }}>
                <Chip label={actividad_fisica.deporte_nombre} color="primary" />
                <Chip label={actividad_fisica.nivel} size="small" sx={{ ml: 0.5 }} />
              </Box>
            )}
          </InfoCard>
        </Grid>

        <Grid item xs={12} md={6}>
          <InfoCard icon={<DirectionsWalk />} title="Metas de Actividad" color="#2196F3">
            <Box sx={{ mb: 2 }}>
              <Typography variant="caption" color="text.secondary">Meta de Pasos Diarios</Typography>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                <Typography variant="body2">{actividad_fisica.pasos_promedio_dia || 0} / {actividad_fisica.meta_pasos_dia}</Typography>
                <Typography variant="body2">{Math.round(((actividad_fisica.pasos_promedio_dia || 0) / actividad_fisica.meta_pasos_dia) * 100)}%</Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={Math.min(((actividad_fisica.pasos_promedio_dia || 0) / actividad_fisica.meta_pasos_dia) * 100, 100)}
                sx={{ height: 8, borderRadius: 2, bgcolor: '#E0E0E0', '& .MuiLinearProgress-bar': { bgcolor: '#2196F3', borderRadius: 2 } }}
              />
            </Box>
            <Typography variant="body2"><strong>Meta ejercicio/semana:</strong> {actividad_fisica.meta_ejercicio_semanal_min} min</Typography>
            {actividad_fisica.dispositivo_conectado && (
              <Chip label={actividad_fisica.dispositivo_conectado} icon={<CheckCircle />} size="small" color="success" sx={{ mt: 1 }} />
            )}
          </InfoCard>
        </Grid>

        <Grid item xs={12} md={6}>
          <InfoCard icon={<Warning />} title="Limitaciones" color="#FF9800">
            {actividad_fisica.lesiones_actuales.length > 0 ? (
              <Box sx={{ mb: 2 }}>
                <Typography variant="caption" color="text.secondary">Lesiones Actuales:</Typography>
                {actividad_fisica.lesiones_actuales.map((lesion, i) => (
                  <Chip key={i} label={lesion} size="small" color="error" sx={{ mr: 0.5, mt: 0.5 }} />
                ))}
              </Box>
            ) : (
              <Typography variant="body2" color="text.secondary">Sin lesiones actuales</Typography>
            )}
            {actividad_fisica.limitaciones_medicas.length > 0 && (
              <Box>
                <Typography variant="caption" color="text.secondary">Limitaciones Médicas:</Typography>
                {actividad_fisica.limitaciones_medicas.map((lim, i) => (
                  <Chip key={i} label={lim} size="small" color="warning" sx={{ mr: 0.5, mt: 0.5 }} />
                ))}
              </Box>
            )}
            {actividad_fisica.dolor_ejercicio && (
              <Chip label="Presenta dolor al ejercitarse" color="error" sx={{ mt: 1 }} />
            )}
          </InfoCard>
        </Grid>

        {actividad_fisica.plan_ejercicio_ia && (
          <Grid item xs={12}>
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
              <Card sx={{ borderRadius: 3, boxShadow: 2, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                    <Psychology sx={{ fontSize: 32, mr: 1.5 }} />
                    <Typography variant="h6" fontWeight="700">Plan de Ejercicio Personalizado (IA)</Typography>
                  </Box>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Typography variant="subtitle2" fontWeight="700" gutterBottom>Tipos Recomendados</Typography>
                        <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                          {actividad_fisica.plan_ejercicio_ia.tipo_recomendado.map((tipo, i) => (
                            <Chip key={i} label={tipo} size="small" sx={{ bgcolor: 'rgba(255,255,255,0.3)', color: 'white' }} />
                          ))}
                        </Box>
                        <Typography variant="body2" sx={{ mt: 2 }}>
                          <strong>Intensidad:</strong> {actividad_fisica.plan_ejercicio_ia.intensidad}
                        </Typography>
                        <Typography variant="body2">
                          <strong>Frecuencia:</strong> {actividad_fisica.plan_ejercicio_ia.frecuencia_sugerida} veces/semana
                        </Typography>
                        <Typography variant="body2">
                          <strong>Duración:</strong> {actividad_fisica.plan_ejercicio_ia.duracion_sugerida_min} min
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Typography variant="subtitle2" fontWeight="700" gutterBottom>Consideraciones de Salud</Typography>
                        <List dense>
                          {actividad_fisica.plan_ejercicio_ia.consideraciones_salud.map((cons, i) => (
                            <ListItem key={i} sx={{ py: 0 }}>
                              <ListItemText primary={cons} primaryTypographyProps={{ sx: { color: 'white', fontSize: '0.85rem' } }} />
                            </ListItem>
                          ))}
                        </List>
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

export default ActividadFisicaView;
