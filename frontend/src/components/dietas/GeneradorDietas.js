import React, { useState } from 'react';
import { Container, Box, Typography, Grid, Card, CardContent, Tabs, Tab, Chip, Button, List, ListItem, ListItemText, LinearProgress, Alert, Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import { Restaurant, ShoppingCart, MenuBook, Psychology, TrendingUp, ExpandMore, AutoAwesome, CheckCircle, AttachMoney } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { DIETAS_MOCK } from '../../data/dietasMock';

const GeneradorDietas = () => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [selectedDay, setSelectedDay] = useState(0);
  const dieta = DIETAS_MOCK[0];

  const getObjetivoColor = (obj) => {
    const colores = { reduccion: '#FF6B35', mantenimiento: '#2196F3', aumento: '#4CAF50', deportivo: '#9C27B0', terapeutico: '#FF9800' };
    return colores[obj] || '#757575';
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', borderRadius: 4, mb: 3 }}>
          <CardContent sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Box>
                <Typography variant="h4" fontWeight="700" gutterBottom>{dieta.nombre}</Typography>
                <Typography variant="body1">Del {new Date(dieta.fecha_inicio).toLocaleDateString('es-MX')} al {new Date(dieta.fecha_fin).toLocaleDateString('es-MX')}</Typography>
                <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                  <Chip label={`Objetivo: ${dieta.objetivo}`} sx={{ bgcolor: getObjetivoColor(dieta.objetivo), color: 'white', fontWeight: 600 }} />
                  <Chip icon={<AutoAwesome />} label="Generado por IA" sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }} />
                  <Chip label={`${dieta.calorias_totales} kcal/día`} sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }} />
                </Box>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h2" fontWeight="700">{dieta.adherencia_porcentaje}%</Typography>
                <Typography variant="caption">Adherencia</Typography>
                <Box sx={{ mt: 1, width: 120, bgcolor: 'rgba(255,255,255,0.2)', borderRadius: 1, overflow: 'hidden', height: 8 }}>
                  <Box sx={{ width: `${dieta.adherencia_porcentaje}%`, height: '100%', bgcolor: '#4CAF50' }} />
                </Box>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </motion.div>

      {/* Macros */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Typography variant="caption" color="text.secondary">Proteína</Typography>
              <Typography variant="h5" fontWeight="700">{dieta.distribucion_macros.proteina_g}g ({dieta.distribucion_macros.proteina_porcentaje}%)</Typography>
              <LinearProgress variant="determinate" value={dieta.distribucion_macros.proteina_porcentaje * 2} sx={{ mt: 1, height: 8, borderRadius: 2, bgcolor: '#E0E0E0', '& .MuiLinearProgress-bar': { bgcolor: '#E91E63' } }} />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Typography variant="caption" color="text.secondary">Carbohidratos</Typography>
              <Typography variant="h5" fontWeight="700">{dieta.distribucion_macros.carbohidratos_g}g ({dieta.distribucion_macros.carbohidratos_porcentaje}%)</Typography>
              <LinearProgress variant="determinate" value={dieta.distribucion_macros.carbohidratos_porcentaje * 2} sx={{ mt: 1, height: 8, borderRadius: 2, bgcolor: '#E0E0E0', '& .MuiLinearProgress-bar': { bgcolor: '#FF9800' } }} />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Typography variant="caption" color="text.secondary">Grasas</Typography>
              <Typography variant="h5" fontWeight="700">{dieta.distribucion_macros.grasas_g}g ({dieta.distribucion_macros.grasas_porcentaje}%)</Typography>
              <LinearProgress variant="determinate" value={dieta.distribucion_macros.grasas_porcentaje * 2} sx={{ mt: 1, height: 8, borderRadius: 2, bgcolor: '#E0E0E0', '& .MuiLinearProgress-bar': { bgcolor: '#2196F3' } }} />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Tabs */}
      <Card sx={{ borderRadius: 3 }}>
        <Tabs value={selectedTab} onChange={(e, v) => setSelectedTab(v)} sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tab icon={<Restaurant />} label="Menú Semanal" iconPosition="start" />
          <Tab icon={<MenuBook />} label="Recetas" iconPosition="start" />
          <Tab icon={<ShoppingCart />} label="Lista de Compras" iconPosition="start" />
          <Tab icon={<Psychology />} label="Optimizaciones IA" iconPosition="start" />
        </Tabs>

        <Box sx={{ p: 3 }}>
          {/* TAB 1: Menú Semanal */}
          {selectedTab === 0 && (
            <Box>
              <Box sx={{ display: 'flex', gap: 1, mb: 3, flexWrap: 'wrap' }}>
                {dieta.menu_semanal.map((dia, idx) => (
                  <Chip key={idx} label={dia.nombre_dia} onClick={() => setSelectedDay(idx)} color={selectedDay === idx ? 'primary' : 'default'} clickable />
                ))}
              </Box>

              {dieta.menu_semanal[selectedDay] && (
                <Box>
                  <Typography variant="h6" fontWeight="700" gutterBottom>{dieta.menu_semanal[selectedDay].nombre_dia} - {dieta.menu_semanal[selectedDay].calorias_total} kcal</Typography>

                  {['desayuno', 'colacion_1', 'comida', 'colacion_2', 'cena'].map((tiempo, idx) => (
                    <Accordion key={idx} sx={{ mb: 1 }}>
                      <AccordionSummary expandIcon={<ExpandMore />}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%', pr: 2 }}>
                          <Typography fontWeight="600">{tiempo.replace('_', ' ').toUpperCase()} - {dieta.menu_semanal[selectedDay][tiempo].hora_recomendada}</Typography>
                          <Chip label={`${dieta.menu_semanal[selectedDay][tiempo].calorias} kcal`} size="small" />
                        </Box>
                      </AccordionSummary>
                      <AccordionDetails>
                        <List dense>
                          {dieta.menu_semanal[selectedDay][tiempo].alimentos.map((alimento, i) => (
                            <ListItem key={i}>
                              <ListItemText primary={alimento.nombre} secondary={`${alimento.cantidad} - ${alimento.equivalentes_usados}`} />
                            </ListItem>
                          ))}
                        </List>
                        {dieta.menu_semanal[selectedDay][tiempo].opciones_sustitucion?.length > 0 && (
                          <Alert severity="info" icon={<AutoAwesome />} sx={{ mt: 1 }}>
                            <strong>Sustituciones IA:</strong> {dieta.menu_semanal[selectedDay][tiempo].opciones_sustitucion.join(', ')}
                          </Alert>
                        )}
                      </AccordionDetails>
                    </Accordion>
                  ))}
                </Box>
              )}
            </Box>
          )}

          {/* TAB 2: Recetas */}
          {selectedTab === 1 && (
            <Grid container spacing={3}>
              {dieta.recetas_incluidas.map((receta, idx) => (
                <Grid item xs={12} md={6} key={idx}>
                  <Card variant="outlined" sx={{ borderRadius: 3 }}>
                    <CardContent>
                      <Typography variant="h6" fontWeight="700" gutterBottom>{receta.nombre}</Typography>
                      <Box sx={{ display: 'flex', gap: 0.5, mb: 2 }}>
                        {receta.tags.map((tag, i) => <Chip key={i} label={tag} size="small" />)}
                      </Box>
                      <Typography variant="body2" color="text.secondary" gutterBottom><strong>Región:</strong> {receta.region}</Typography>
                      <Typography variant="body2" color="text.secondary" gutterBottom><strong>Tiempo:</strong> {receta.tiempo_prep_min} min | <strong>Porciones:</strong> {receta.porciones} | <strong>Calorías:</strong> {receta.calorias_porcion} kcal/porción</Typography>
                      <Typography variant="subtitle2" fontWeight="700" sx={{ mt: 2 }}>Ingredientes:</Typography>
                      <List dense>
                        {receta.ingredientes.map((ing, i) => <ListItem key={i}><ListItemText primary={ing} /></ListItem>)}
                      </List>
                      <Typography variant="subtitle2" fontWeight="700" sx={{ mt: 1 }}>Preparación:</Typography>
                      <Typography variant="body2">{receta.preparacion}</Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}

          {/* TAB 3: Lista de Compras */}
          {selectedTab === 2 && (
            <Box>
              <Alert severity="success" icon={<AttachMoney />} sx={{ mb: 3 }}>
                <strong>Presupuesto semanal estimado:</strong> ${dieta.lista_compras.reduce((sum, cat) => sum + cat.items.reduce((s, i) => s + i.costo_estimado_mxn, 0), 0)} MXN
              </Alert>
              <Grid container spacing={3}>
                {dieta.lista_compras.map((categoria, idx) => (
                  <Grid item xs={12} md={6} key={idx}>
                    <Card variant="outlined" sx={{ borderRadius: 3 }}>
                      <CardContent>
                        <Typography variant="h6" fontWeight="700" gutterBottom>{categoria.categoria}</Typography>
                        <List dense>
                          {categoria.items.map((item, i) => (
                            <ListItem key={i}>
                              <CheckCircle sx={{ mr: 1, color: '#4CAF50' }} />
                              <ListItemText primary={item.producto} secondary={`${item.cantidad} - $${item.costo_estimado_mxn} MXN`} />
                            </ListItem>
                          ))}
                        </List>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
              <Button variant="contained" fullWidth sx={{ mt: 3, py: 1.5, borderRadius: 3 }} startIcon={<ShoppingCart />}>Descargar Lista de Compras (PDF)</Button>
            </Box>
          )}

          {/* TAB 4: Optimizaciones IA */}
          {selectedTab === 3 && (
            <Box>
              <Alert severity="info" icon={<Psychology />} sx={{ mb: 3 }}>
                Este plan fue generado automáticamente por IA considerando el perfil completo del paciente y optimizado para máxima adherencia.
              </Alert>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Card variant="outlined" sx={{ borderRadius: 3 }}>
                    <CardContent>
                      <Typography variant="h6" fontWeight="700" gutterBottom>Optimizaciones Aplicadas</Typography>
                      <List>
                        <ListItem><CheckCircle sx={{ color: '#4CAF50', mr: 1 }} /><ListItemText primary="Alimentos culturales mexicanos prioritarios" /></ListItem>
                        <ListItem><CheckCircle sx={{ color: '#4CAF50', mr: 1 }} /><ListItemText primary="Considera presupuesto familiar" /></ListItem>
                        <ListItem><CheckCircle sx={{ color: '#4CAF50', mr: 1 }} /><ListItemText primary="Alimentos de temporada" /></ListItem>
                        <ListItem><CheckCircle sx={{ color: '#4CAF50', mr: 1 }} /><ListItemText primary="Evita alergias: Camarones" /></ListItem>
                      </List>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Card variant="outlined" sx={{ borderRadius: 3 }}>
                    <CardContent>
                      <Typography variant="h6" fontWeight="700" gutterBottom>Ajustes Automáticos</Typography>
                      {dieta.ajustes_automaticos.map((ajuste, idx) => (
                        <Alert key={idx} severity="warning" icon={<TrendingUp />} sx={{ mb: 2 }}>
                          <Typography variant="caption">{new Date(ajuste.fecha).toLocaleDateString('es-MX')}</Typography>
                          <Typography variant="body2" fontWeight="600">{ajuste.razon}</Typography>
                          <List dense>
                            {ajuste.cambios.map((cambio, i) => <ListItem key={i}><ListItemText primary={cambio} /></ListItem>)}
                          </List>
                        </Alert>
                      ))}
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          )}
        </Box>
      </Card>
    </Container>
  );
};

export default GeneradorDietas;
