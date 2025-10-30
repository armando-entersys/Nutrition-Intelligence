import React from 'react';
import { Box, Typography, Grid, Card, CardContent, Alert, Chip } from '@mui/material';
import {
  Favorite as FavoriteIcon,
  Thermostat as ThermostatIcon,
  Air as AirIcon,
  MonitorHeart as MonitorHeartIcon,
  Bloodtype as BloodtypeIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const SignosVitalesView = ({ paciente }) => {
  const signosVitales = paciente.signos_vitales[0];

  const MetricCard = ({ title, value, unit, subtitle, icon, color, alert }) => (
    <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}>
      <Card sx={{ height: '100%', borderRadius: 3, boxShadow: 2, border: alert ? '2px solid #ff6b6b' : 'none' }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <Box>
              <Typography variant="caption" color="text.secondary" fontWeight="600">{title}</Typography>
              <Box sx={{ display: 'flex', alignItems: 'baseline', gap: 0.5 }}>
                <Typography variant="h3" fontWeight="700" color={color}>{value}</Typography>
                <Typography variant="h6" color="text.secondary">{unit}</Typography>
              </Box>
              {subtitle && <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>{subtitle}</Typography>}
            </Box>
            <Box sx={{ bgcolor: color, color: 'white', p: 1, borderRadius: 2, display: 'flex' }}>
              {icon}
            </Box>
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );

  const getPresionColor = (sistolica, diastolica) => {
    if (sistolica >= 140 || diastolica >= 90) return '#E63946';
    if (sistolica >= 130 || diastolica >= 80) return '#FF6B35';
    return '#2ecc71';
  };

  return (
    <Box>
      {signosVitales.alertas_ia?.recomendacion_urgente && (
        <Alert severity="error" icon={<WarningIcon />} sx={{ mb: 3, fontWeight: 600 }}>
          {signosVitales.alertas_ia.recomendacion_urgente}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <MetricCard
            title="Presión Arterial"
            value={`${signosVitales.presion_sistolica_mmHg}/${signosVitales.presion_diastolica_mmHg}`}
            unit="mmHg"
            subtitle={signosVitales.clasificacion_presion}
            icon={<FavoriteIcon />}
            color={getPresionColor(signosVitales.presion_sistolica_mmHg, signosVitales.presion_diastolica_mmHg)}
            alert={signosVitales.alertas_ia?.presion_anormal}
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <MetricCard
            title="Frecuencia Cardíaca"
            value={signosVitales.frecuencia_cardiaca_lpm}
            unit="lpm"
            subtitle={signosVitales.ritmo_regular ? 'Ritmo regular' : 'Ritmo irregular'}
            icon={<MonitorHeartIcon />}
            color="#E91E63"
            alert={signosVitales.alertas_ia?.taquicardia || signosVitales.alertas_ia?.bradicardia}
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <MetricCard
            title="Glucosa Capilar"
            value={signosVitales.glucosa_capilar_mgdl}
            unit="mg/dL"
            subtitle={signosVitales.momento_medicion}
            icon={<BloodtypeIcon />}
            color="#9C27B0"
            alert={signosVitales.alertas_ia?.hipoglucemia || signosVitales.alertas_ia?.hiperglucemia}
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <MetricCard
            title="Temperatura"
            value={signosVitales.temperatura_celsius}
            unit="°C"
            icon={<ThermostatIcon />}
            color="#FF9800"
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <MetricCard
            title="Frecuencia Respiratoria"
            value={signosVitales.frecuencia_respiratoria_rpm}
            unit="rpm"
            icon={<AirIcon />}
            color="#00BCD4"
          />
        </Grid>

        {signosVitales.saturacion_oxigeno_porcentaje && (
          <Grid item xs={12} md={4}>
            <MetricCard
              title="Saturación de Oxígeno"
              value={signosVitales.saturacion_oxigeno_porcentaje}
              unit="%"
              icon={<AirIcon />}
              color="#4CAF50"
            />
          </Grid>
        )}

        <Grid item xs={12}>
          <Card sx={{ borderRadius: 3, boxShadow: 2 }}>
            <CardContent>
              <Typography variant="subtitle2" color="text.secondary">Información Adicional</Typography>
              <Typography variant="body2" sx={{ mt: 1 }}>
                <strong>Fecha:</strong> {new Date(signosVitales.fecha_hora).toLocaleString('es-MX')}
              </Typography>
              <Typography variant="body2">
                <strong>Lugar:</strong> {signosVitales.lugar_medicion}
              </Typography>
              <Typography variant="body2">
                <strong>Medido por:</strong> {signosVitales.medido_por}
              </Typography>
              {signosVitales.notas && (
                <Typography variant="body2" sx={{ mt: 1 }}>
                  <strong>Notas:</strong> {signosVitales.notas}
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SignosVitalesView;
