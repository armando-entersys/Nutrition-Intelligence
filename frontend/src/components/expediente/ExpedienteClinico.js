import React, { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  Tabs,
  Tab,
  Avatar,
  Chip,
  Grid,
  Card,
  CardContent,
  Alert,
  IconButton,
  Button,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  LinearProgress,
} from '@mui/material';
import {
  Person as PersonIcon,
  MonitorWeight as MonitorWeightIcon,
  MedicalServices as MedicalServicesIcon,
  Favorite as FavoriteIcon,
  Science as ScienceIcon,
  DirectionsRun as DirectionsRunIcon,
  Restaurant as RestaurantIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Edit as EditIcon,
  Print as PrintIcon,
  Share as ShareIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  WhatsApp as WhatsAppIcon,
  LocationOn as LocationOnIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { PACIENTES_MOCK } from '../../data/pacientesMock';

// Componentes individuales
import DatosGeneralesView from './DatosGeneralesView';
import MedicionesAntropometricasView from './MedicionesAntropometricasView';
import HistoriaClinicaView from './HistoriaClinicaView';
import SignosVitalesView from './SignosVitalesView';
import HabitosView from './HabitosView';
import ActividadFisicaView from './ActividadFisicaView';
import DatosLaboratorioView from './DatosLaboratorioView';

const ExpedienteClinico = () => {
  const [selectedPatient, setSelectedPatient] = useState(PACIENTES_MOCK[0]);
  const [currentTab, setCurrentTab] = useState(0);

  // Tabs del expediente
  const tabs = [
    { id: 0, label: 'Datos Generales', icon: <PersonIcon />, component: DatosGeneralesView },
    { id: 1, label: 'Antropometría', icon: <MonitorWeightIcon />, component: MedicionesAntropometricasView },
    { id: 2, label: 'Historia Clínica', icon: <MedicalServicesIcon />, component: HistoriaClinicaView },
    { id: 3, label: 'Laboratorios', icon: <ScienceIcon />, component: DatosLaboratorioView },
    { id: 4, label: 'Signos Vitales', icon: <FavoriteIcon />, component: SignosVitalesView },
    { id: 5, label: 'Hábitos', icon: <RestaurantIcon />, component: HabitosView },
    { id: 6, label: 'Actividad Física', icon: <DirectionsRunIcon />, component: ActividadFisicaView },
  ];

  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);
  };

  // Cálculo de score de riesgo general
  const getRiesgoGeneral = () => {
    const riesgos = selectedPatient.historia_clinica.analisis_riesgo_ia;
    if (!riesgos) return { score: 0, nivel: 'bajo', color: 'success' };

    const promedioRiesgo = (
      riesgos.riesgo_cardiovascular +
      riesgos.riesgo_diabetes_tipo2 +
      riesgos.riesgo_sindrome_metabolico
    ) / 3;

    let nivel = 'bajo';
    let color = 'success';

    if (promedioRiesgo > 70) {
      nivel = 'crítico';
      color = 'error';
    } else if (promedioRiesgo > 50) {
      nivel = 'alto';
      color = 'warning';
    } else if (promedioRiesgo > 30) {
      nivel = 'moderado';
      color = 'info';
    }

    return { score: Math.round(promedioRiesgo), nivel, color };
  };

  const riesgoGeneral = getRiesgoGeneral();

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header del Expediente */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Paper
          elevation={0}
          sx={{
            p: 3,
            mb: 3,
            background: 'linear-gradient(135deg, #006847 0%, #00a86b 100%)',
            color: 'white',
            borderRadius: 4,
          }}
        >
          <Grid container spacing={3} alignItems="center">
            <Grid item>
              <Avatar
                sx={{
                  width: 100,
                  height: 100,
                  bgcolor: 'white',
                  color: '#006847',
                  fontSize: '2.5rem',
                  fontWeight: 'bold',
                  border: '4px solid rgba(255,255,255,0.3)',
                }}
              >
                {selectedPatient.datos_generales.nombre_completo.charAt(0)}
              </Avatar>
            </Grid>

            <Grid item xs>
              <Typography variant="h4" fontWeight="700" gutterBottom>
                {selectedPatient.datos_generales.nombre_completo}
              </Typography>

              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 2 }}>
                <Chip
                  label={`${selectedPatient.datos_generales.edad} años`}
                  sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white', fontWeight: 600 }}
                />
                <Chip
                  label={selectedPatient.datos_generales.sexo === 'femenino' ? 'Femenino' : 'Masculino'}
                  sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white', fontWeight: 600 }}
                />
                <Chip
                  label={`IMC: ${selectedPatient.mediciones_antropometricas[0].imc}`}
                  sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white', fontWeight: 600 }}
                />
                <Chip
                  icon={<WarningIcon />}
                  label={`Riesgo: ${riesgoGeneral.nivel.toUpperCase()}`}
                  color={riesgoGeneral.color}
                  sx={{ fontWeight: 600 }}
                />
              </Box>

              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <PhoneIcon fontSize="small" />
                  <Typography variant="body2">{selectedPatient.datos_generales.telefono}</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <EmailIcon fontSize="small" />
                  <Typography variant="body2">{selectedPatient.datos_generales.email}</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <WhatsAppIcon fontSize="small" />
                  <Typography variant="body2">{selectedPatient.datos_generales.whatsapp}</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <LocationOnIcon fontSize="small" />
                  <Typography variant="body2">{selectedPatient.datos_generales.estado}</Typography>
                </Box>
              </Box>
            </Grid>

            <Grid item>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Button
                  variant="contained"
                  startIcon={<EditIcon />}
                  sx={{
                    bgcolor: 'white',
                    color: '#006847',
                    '&:hover': { bgcolor: 'rgba(255,255,255,0.9)' },
                    fontWeight: 600,
                  }}
                >
                  Editar
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<PrintIcon />}
                  sx={{
                    borderColor: 'white',
                    color: 'white',
                    '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' },
                  }}
                >
                  Imprimir
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<ShareIcon />}
                  sx={{
                    borderColor: 'white',
                    color: 'white',
                    '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.1)' },
                  }}
                >
                  Compartir
                </Button>
              </Box>
            </Grid>
          </Grid>

          {/* Alertas IA */}
          {selectedPatient.signos_vitales[0]?.alertas_ia?.recomendacion_urgente && (
            <Alert
              severity="error"
              icon={<WarningIcon />}
              sx={{ mt: 2, bgcolor: 'rgba(255,255,255,0.95)', fontWeight: 600 }}
            >
              <strong>ALERTA MÉDICA:</strong> {selectedPatient.signos_vitales[0].alertas_ia.recomendacion_urgente}
            </Alert>
          )}
        </Paper>

        {/* Resumen Ejecutivo con Indicadores Clave */}
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} md={3}>
            <Card sx={{ height: '100%', borderRadius: 3 }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <MonitorWeightIcon sx={{ color: '#006847', mr: 1 }} />
                  <Typography variant="subtitle2" color="text.secondary">
                    Peso Actual
                  </Typography>
                </Box>
                <Typography variant="h4" fontWeight="700">
                  {selectedPatient.mediciones_antropometricas[0].peso_kg} kg
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {selectedPatient.mediciones_antropometricas[0].interpretacion_imc}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={3}>
            <Card sx={{ height: '100%', borderRadius: 3 }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <TrendingUpIcon sx={{ color: '#FF6B35', mr: 1 }} />
                  <Typography variant="subtitle2" color="text.secondary">
                    Meta de Peso
                  </Typography>
                </Box>
                <Typography variant="h4" fontWeight="700">
                  {(selectedPatient.mediciones_antropometricas[0].peso_kg * 0.9).toFixed(1)} kg
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  -10% recomendado
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={3}>
            <Card sx={{ height: '100%', borderRadius: 3 }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <FavoriteIcon sx={{ color: '#E63946', mr: 1 }} />
                  <Typography variant="subtitle2" color="text.secondary">
                    Presión Arterial
                  </Typography>
                </Box>
                <Typography variant="h4" fontWeight="700">
                  {selectedPatient.signos_vitales[0].presion_sistolica_mmHg}/
                  {selectedPatient.signos_vitales[0].presion_diastolica_mmHg}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {selectedPatient.signos_vitales[0].clasificacion_presion}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={3}>
            <Card sx={{ height: '100%', borderRadius: 3 }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <ScienceIcon sx={{ color: '#457B9D', mr: 1 }} />
                  <Typography variant="subtitle2" color="text.secondary">
                    Glucosa
                  </Typography>
                </Box>
                <Typography variant="h4" fontWeight="700">
                  {selectedPatient.signos_vitales[0].glucosa_capilar_mgdl} mg/dL
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {selectedPatient.signos_vitales[0].momento_medicion}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Tabs de Navegación */}
        <Paper elevation={0} sx={{ borderRadius: 3, mb: 3 }}>
          <Tabs
            value={currentTab}
            onChange={handleTabChange}
            variant="scrollable"
            scrollButtons="auto"
            sx={{
              borderBottom: 1,
              borderColor: 'divider',
              '& .MuiTab-root': {
                minHeight: 72,
                textTransform: 'none',
                fontSize: '1rem',
                fontWeight: 600,
              },
              '& .Mui-selected': {
                color: '#006847',
              },
              '& .MuiTabs-indicator': {
                backgroundColor: '#006847',
                height: 3,
              },
            }}
          >
            {tabs.map((tab) => (
              <Tab
                key={tab.id}
                icon={tab.icon}
                label={tab.label}
                iconPosition="start"
              />
            ))}
          </Tabs>
        </Paper>

        {/* Contenido del Tab Actual */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentTab}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            {tabs[currentTab].component &&
              React.createElement(tabs[currentTab].component, { paciente: selectedPatient })
            }
          </motion.div>
        </AnimatePresence>
      </motion.div>

      {/* Información del Nutriólogo Responsable */}
      <Paper
        elevation={0}
        sx={{
          p: 2,
          mt: 3,
          borderRadius: 3,
          bgcolor: '#F8F9FA',
          borderLeft: '4px solid #006847',
        }}
      >
        <Typography variant="body2" color="text.secondary">
          <strong>Nutriólogo Responsable:</strong> {selectedPatient.nutriologo_responsable}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          Última actualización: {new Date(selectedPatient.fecha_ultima_modificacion).toLocaleDateString('es-MX', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
          })}
        </Typography>
      </Paper>
    </Container>
  );
};

export default ExpedienteClinico;
