import React from 'react';
import { Container, Box, Typography, Grid, Card, CardContent, Chip, LinearProgress, Avatar, List, ListItem, ListItemText, ListItemAvatar } from '@mui/material';
import { EmojiEvents, LocalFireDepartment, Star, TrendingUp } from '@mui/icons-material';
import { motion } from 'framer-motion';

const GamificacionMexicana = () => {
  const userData = {
    nivel: 3,
    nombre_nivel: 'Águila Mexicana',
    xp_actual: 450,
    xp_siguiente_nivel: 600,
    xp_total: 450,
    racha_actual: 12,
    racha_maxima: 18,
    badges_obtenidos: [
      { id: 1, nombre: 'Taquero de Corazón', icono: '🌮', descripcion: '30 días comiendo tacos saludables', fecha_obtenido: '2024-10-15' },
      { id: 2, nombre: 'Guardián del Maíz', icono: '🌽', descripcion: 'Tortilla de maíz 90% del tiempo', fecha_obtenido: '2024-10-20' },
      { id: 3, nombre: 'Maestro del Frijol', icono: '🫘', descripcion: '50 días consumiendo frijoles', fecha_obtenido: '2024-10-25' },
    ],
    badges_disponibles: [
      { id: 4, nombre: 'Amante del Chile', icono: '🌶️', descripcion: 'Incorporar chile en 30 comidas', progreso: 22, total: 30 },
      { id: 5, nombre: 'Rey del Aguacate', icono: '🥑', descripcion: 'Usar aguacate como grasa saludable 20 veces', progreso: 15, total: 20 },
    ],
  };

  const niveles = [
    { nivel: 1, nombre: 'Novato', icono: '🌱', xp_min: 0, xp_max: 100, color: '#9E9E9E' },
    { nivel: 2, nombre: 'Guerrero Azteca', icono: '🗿', xp_min: 101, xp_max: 300, color: '#8D6E63' },
    { nivel: 3, nombre: 'Águila Mexicana', icono: '🦅', xp_min: 301, xp_max: 600, color: '#FF9800' },
    { nivel: 4, nombre: 'Luchador', icono: '🤼', xp_min: 601, xp_max: 1000, color: '#E91E63' },
    { nivel: 5, nombre: 'Leyenda Nacional', icono: '🇲🇽', xp_min: 1001, xp_max: 2000, color: '#9C27B0' },
    { nivel: 6, nombre: 'Patrimonio UNESCO', icono: '🏆', xp_min: 2001, xp_max: 99999, color: '#FFD700' },
  ];

  const leaderboard = [
    { posicion: 1, nombre: 'María Hernández', estado: 'CDMX', xp: 1850, avatar_color: '#FFD700' },
    { posicion: 2, nombre: 'Carlos Ramírez', estado: 'Edo. México', xp: 1720, avatar_color: '#C0C0C0' },
    { posicion: 3, nombre: 'Ana López', estado: 'Jalisco', xp: 1650, avatar_color: '#CD7F32' },
    { posicion: 12, nombre: 'Tú', estado: 'Ciudad de México', xp: 450, avatar_color: '#2196F3', es_usuario: true },
  ];

  const nivelActual = niveles[userData.nivel - 1];
  const progresoNivel = ((userData.xp_actual - nivelActual.xp_min) / (nivelActual.xp_max - nivelActual.xp_min)) * 100;

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', borderRadius: 4, mb: 3 }}>
          <CardContent sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Box>
                <Typography variant="h4" fontWeight="700" gutterBottom>🎮 Gamificación Mexicana</Typography>
                <Typography variant="body1">Gana XP, desbloquea badges culturales y compite en el ranking nacional</Typography>
              </Box>
              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="h1" sx={{ fontSize: '4rem' }}>{nivelActual.icono}</Typography>
                <Typography variant="h6" fontWeight="700">{nivelActual.nombre}</Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </motion.div>

      {/* Nivel y XP */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6" fontWeight="700">Tu Nivel</Typography>
                <Chip label={`Nivel ${userData.nivel}`} sx={{ bgcolor: nivelActual.color, color: 'white', fontWeight: 700 }} />
              </Box>
              <Typography variant="h5" fontWeight="700" gutterBottom>{nivelActual.nombre}</Typography>
              <Box sx={{ mb: 1 }}>
                <Typography variant="body2" color="text.secondary">{userData.xp_actual} / {nivelActual.xp_max} XP</Typography>
                <LinearProgress variant="determinate" value={progresoNivel} sx={{ mt: 1, height: 12, borderRadius: 2, bgcolor: '#E0E0E0', '& .MuiLinearProgress-bar': { bgcolor: nivelActual.color } }} />
              </Box>
              <Typography variant="caption" color="text.secondary">{nivelActual.xp_max - userData.xp_actual} XP para siguiente nivel</Typography>

              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle2" fontWeight="700" gutterBottom>Niveles Disponibles:</Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  {niveles.map((niv) => (
                    <Box key={niv.nivel} sx={{ display: 'flex', alignItems: 'center', gap: 1, opacity: niv.nivel > userData.nivel ? 0.4 : 1 }}>
                      <Typography sx={{ fontSize: '1.5rem' }}>{niv.icono}</Typography>
                      <Typography variant="body2" fontWeight={niv.nivel === userData.nivel ? 700 : 400}>
                        {niv.nivel}. {niv.nombre}
                      </Typography>
                      {niv.nivel === userData.nivel && <Chip label="Actual" size="small" color="primary" />}
                      {niv.nivel < userData.nivel && <Chip label="✓" size="small" color="success" />}
                    </Box>
                  ))}
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Racha */}
        <Grid item xs={12} md={6}>
          <Card sx={{ borderRadius: 3, mb: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <LocalFireDepartment sx={{ fontSize: 48, color: '#FF6B35' }} />
                <Box>
                  <Typography variant="h6" fontWeight="700">Racha Actual</Typography>
                  <Typography variant="h3" fontWeight="700" sx={{ color: '#FF6B35' }}>{userData.racha_actual} días</Typography>
                </Box>
              </Box>
              <Typography variant="body2" color="text.secondary">Racha máxima: {userData.racha_maxima} días</Typography>
              <LinearProgress variant="determinate" value={(userData.racha_actual / userData.racha_maxima) * 100} sx={{ mt: 2, height: 8, borderRadius: 2, bgcolor: '#FFE0DB', '& .MuiLinearProgress-bar': { bgcolor: '#FF6B35' } }} />
            </CardContent>
          </Card>

          {/* Badges Obtenidos */}
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <EmojiEvents sx={{ color: '#FFD700' }} />
                <Typography variant="h6" fontWeight="700">Badges Mexicanos</Typography>
              </Box>
              <List>
                {userData.badges_obtenidos.map((badge) => (
                  <ListItem key={badge.id} sx={{ bgcolor: '#F5F5F5', borderRadius: 2, mb: 1 }}>
                    <ListItemAvatar><Avatar sx={{ bgcolor: '#FFD700' }}>{badge.icono}</Avatar></ListItemAvatar>
                    <ListItemText primary={badge.nombre} secondary={badge.descripcion} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Badges en Progreso */}
        <Grid item xs={12}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Typography variant="h6" fontWeight="700" gutterBottom>Badges en Progreso</Typography>
              <Grid container spacing={2}>
                {userData.badges_disponibles.map((badge) => (
                  <Grid item xs={12} md={6} key={badge.id}>
                    <Card variant="outlined" sx={{ borderRadius: 2 }}>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                          <Typography sx={{ fontSize: '2rem' }}>{badge.icono}</Typography>
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="subtitle1" fontWeight="700">{badge.nombre}</Typography>
                            <Typography variant="caption" color="text.secondary">{badge.descripcion}</Typography>
                          </Box>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <LinearProgress variant="determinate" value={(badge.progreso / badge.total) * 100} sx={{ flex: 1, height: 8, borderRadius: 2 }} />
                          <Typography variant="caption" fontWeight="600">{badge.progreso}/{badge.total}</Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Leaderboard */}
        <Grid item xs={12}>
          <Card sx={{ borderRadius: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <TrendingUp sx={{ color: '#2196F3' }} />
                <Typography variant="h6" fontWeight="700">Ranking Nacional</Typography>
              </Box>
              <List>
                {leaderboard.map((usuario) => (
                  <ListItem key={usuario.posicion} sx={{ bgcolor: usuario.es_usuario ? '#E3F2FD' : 'transparent', borderRadius: 2, mb: 0.5 }}>
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: usuario.avatar_color, fontWeight: 700 }}>
                        {usuario.posicion <= 3 ? ['🥇', '🥈', '🥉'][usuario.posicion - 1] : usuario.posicion}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText primary={<Typography fontWeight={usuario.es_usuario ? 700 : 400}>{usuario.nombre}</Typography>} secondary={usuario.estado} />
                    <Chip label={`${usuario.xp} XP`} sx={{ fontWeight: 700 }} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default GamificacionMexicana;
