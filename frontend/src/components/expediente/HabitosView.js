import React from 'react';
import { Box, Typography, Grid, Card, CardContent, Chip, List, ListItem, ListItemText, LinearProgress } from '@mui/material';
import { Restaurant, LocalCafe, SmokingRooms, Sports, ShoppingCart, Psychology } from '@mui/icons-material';
import { motion } from 'framer-motion';

const HabitosView = ({ paciente }) => {
  const { habitos } = paciente;

  const InfoCard = ({ icon, title, children, color = '#006847' }) => (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
      <Card sx={{ height: '100%', borderRadius: 3, boxShadow: 2 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Box sx={{ bgcolor: color, color: 'white', p: 1, borderRadius: 2, display: 'flex', mr: 1.5 }}>
              {icon}
            </Box>
            <Typography variant="h6" fontWeight="700">{title}</Typography>
          </Box>
          {children}
        </CardContent>
      </Card>
    </motion.div>
  );

  return (
    <Box>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <InfoCard icon={<Restaurant />} title="Hábitos Alimentarios">
            <Typography variant="body2"><strong>Comidas al día:</strong> {habitos.num_comidas_dia}</Typography>
            <Typography variant="body2"><strong>Desayuna:</strong> {habitos.desayuna_diario ? 'Sí' : 'No'}</Typography>
            <Typography variant="body2"><strong>Primera comida:</strong> {habitos.hora_primera_comida}</Typography>
            <Typography variant="body2"><strong>Última comida:</strong> {habitos.hora_ultima_comida}</Typography>
            <Typography variant="body2"><strong>Ventana alimentación:</strong> {habitos.ventana_alimentacion_horas} horas</Typography>
            <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {habitos.come_viendo_tv && <Chip label="Come viendo TV" size="small" color="warning" />}
              {habitos.come_rapido && <Chip label="Come rápido" size="small" color="warning" />}
              {!habitos.mastica_suficiente && <Chip label="Mastica poco" size="small" color="error" />}
            </Box>
          </InfoCard>
        </Grid>

        <Grid item xs={12} md={6}>
          <InfoCard icon={<LocalCafe />} title="Hidratación y Bebidas" color="#2196F3">
            <Typography variant="body2"><strong>Agua al día:</strong> {habitos.vasos_agua_dia} vasos</Typography>
            <Box sx={{ my: 1, bgcolor: '#E3F2FD', borderRadius: 1, overflow: 'hidden' }}>
              <Box sx={{ width: `${(habitos.vasos_agua_dia / 8) * 100}%`, height: 8, bgcolor: '#2196F3' }} />
            </Box>
            <Typography variant="body2"><strong>Refrescos/semana:</strong> {habitos.refrescos_semana}</Typography>
            {habitos.consume_alcohol && (
              <Typography variant="body2"><strong>Alcohol/semana:</strong> {habitos.bebidas_alcoholicas_semana} bebidas</Typography>
            )}
          </InfoCard>
        </Grid>

        {habitos.fuma && (
          <Grid item xs={12} md={6}>
            <InfoCard icon={<SmokingRooms />} title="Tabaquismo" color="#E63946">
              <Typography variant="body2"><strong>Cigarros al día:</strong> {habitos.cigarros_dia}</Typography>
              <Typography variant="body2"><strong>Años fumando:</strong> {habitos.años_fumando}</Typography>
            </InfoCard>
          </Grid>
        )}

        <Grid item xs={12} md={6}>
          <InfoCard icon={<Restaurant />} title="Hábitos Culturales Mexicanos" color="#006847">
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
              {habitos.consume_tortilla_diario && <Chip label="Tortilla diaria" icon={<span>🌮</span>} />}
              {habitos.consume_frijol_diario && <Chip label="Frijol diario" icon={<span>🫘</span>} />}
              {habitos.consume_chile_diario && <Chip label="Chile diario" icon={<span>🌶️</span>} />}
            </Box>
            <Typography variant="body2"><strong>Tacos/semana:</strong> {habitos.come_tacos_semana}</Typography>
            <Typography variant="body2"><strong>Fondas/semana:</strong> {habitos.asiste_fondas_semana}</Typography>
            <Typography variant="body2"><strong>Desayuno típico:</strong> {habitos.desayuno_tipico}</Typography>
          </InfoCard>
        </Grid>

        <Grid item xs={12} md={6}>
          <InfoCard icon={<ShoppingCart />} title="Compras y Cocina" color="#FF9800">
            <Typography variant="body2"><strong>Cocina:</strong> {habitos.quien_cocina_hogar}</Typography>
            <Typography variant="body2"><strong>Frecuencia compra:</strong> {habitos.frecuencia_compra_alimentos}</Typography>
            {habitos.presupuesto_mensual_alimentos && (
              <Typography variant="body2"><strong>Presupuesto:</strong> ${habitos.presupuesto_mensual_alimentos} MXN/mes</Typography>
            )}
            <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
              {habitos.compra_mercado_local && <Chip label="Mercado local" size="small" color="success" />}
              {habitos.compra_supermercado && <Chip label="Supermercado" size="small" />}
            </Box>
          </InfoCard>
        </Grid>

        {habitos.analisis_habitos_ia && (
          <Grid item xs={12}>
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
              <Card sx={{ borderRadius: 3, boxShadow: 2, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                    <Psychology sx={{ fontSize: 32, mr: 1.5 }} />
                    <Typography variant="h6" fontWeight="700">Análisis Inteligente de Hábitos (IA)</Typography>
                  </Box>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Typography variant="subtitle2" fontWeight="700" gutterBottom>Hábitos Positivos ✅</Typography>
                        <List dense>
                          {habitos.analisis_habitos_ia.habitos_positivos.map((h, i) => (
                            <ListItem key={i} sx={{ py: 0 }}>
                              <ListItemText primary={h} primaryTypographyProps={{ sx: { color: 'white', fontSize: '0.9rem' } }} />
                            </ListItem>
                          ))}
                        </List>
                      </Box>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Typography variant="subtitle2" fontWeight="700" gutterBottom>Hábitos Críticos ⚠️</Typography>
                        <List dense>
                          {habitos.analisis_habitos_ia.habitos_criticos.map((h, i) => (
                            <ListItem key={i} sx={{ py: 0 }}>
                              <ListItemText primary={h} primaryTypographyProps={{ sx: { color: 'white', fontSize: '0.9rem' } }} />
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

export default HabitosView;
