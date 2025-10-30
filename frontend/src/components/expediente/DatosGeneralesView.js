import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Alert,
} from '@mui/material';
import {
  Person as PersonIcon,
  Cake as CakeIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  Home as HomeIcon,
  Work as WorkIcon,
  School as SchoolIcon,
  Family as FamilyIcon,
  LocalHospital as LocalHospitalIcon,
  Psychology as PsychologyIcon,
  TrendingDown as TrendingDownIcon,
  Lightbulb as LightbulbIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const DatosGeneralesView = ({ paciente }) => {
  const { datos_generales } = paciente;

  const calcularEdad = (fecha_nacimiento) => {
    const hoy = new Date();
    const nacimiento = new Date(fecha_nacimiento);
    let edad = hoy.getFullYear() - nacimiento.getFullYear();
    const mes = hoy.getMonth() - nacimiento.getMonth();
    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
      edad--;
    }
    return edad;
  };

  const InfoCard = ({ icon, title, children }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <Card sx={{ height: '100%', borderRadius: 3, boxShadow: 2 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Box
              sx={{
                bgcolor: '#006847',
                color: 'white',
                p: 1,
                borderRadius: 2,
                display: 'flex',
                mr: 1.5,
              }}
            >
              {icon}
            </Box>
            <Typography variant="h6" fontWeight="700">
              {title}
            </Typography>
          </Box>
          {children}
        </CardContent>
      </Card>
    </motion.div>
  );

  const DataRow = ({ label, value }) => (
    <Box sx={{ mb: 1.5 }}>
      <Typography variant="caption" color="text.secondary" fontWeight="600">
        {label}
      </Typography>
      <Typography variant="body1" fontWeight="500">
        {value || 'No especificado'}
      </Typography>
    </Box>
  );

  return (
    <Box>
      <Grid container spacing={3}>
        {/* Información Personal */}
        <Grid item xs={12} md={6}>
          <InfoCard icon={<PersonIcon />} title="Información Personal">
            <DataRow label="Nombre Completo" value={datos_generales.nombre_completo} />
            <DataRow
              label="Fecha de Nacimiento"
              value={new Date(datos_generales.fecha_nacimiento).toLocaleDateString('es-MX', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            />
            <DataRow label="Edad" value={`${calcularEdad(datos_generales.fecha_nacimiento)} años`} />
            <DataRow
              label="Sexo"
              value={datos_generales.sexo === 'femenino' ? 'Femenino' : datos_generales.sexo === 'masculino' ? 'Masculino' : 'Otro'}
            />
            <DataRow label="CURP" value={datos_generales.curp} />
          </InfoCard>
        </Grid>

        {/* Contacto */}
        <Grid item xs={12} md={6}>
          <InfoCard icon={<PhoneIcon />} title="Datos de Contacto">
            <DataRow label="Teléfono" value={datos_generales.telefono} />
            <DataRow label="WhatsApp" value={datos_generales.whatsapp} />
            <DataRow label="Email" value={datos_generales.email} />

            <Divider sx={{ my: 2 }} />

            <Typography variant="subtitle2" fontWeight="700" gutterBottom sx={{ mt: 2 }}>
              Contacto de Emergencia
            </Typography>
            <DataRow label="Nombre" value={datos_generales.contacto_emergencia.nombre} />
            <DataRow label="Parentesco" value={datos_generales.contacto_emergencia.parentesco} />
            <DataRow label="Teléfono" value={datos_generales.contacto_emergencia.telefono} />
          </InfoCard>
        </Grid>

        {/* Ubicación */}
        <Grid item xs={12} md={6}>
          <InfoCard icon={<HomeIcon />} title="Ubicación">
            <DataRow label="Estado" value={datos_generales.estado} />
            <DataRow label="Municipio" value={datos_generales.municipio} />
            <DataRow label="Colonia" value={datos_generales.colonia} />
            <DataRow label="Dirección" value={datos_generales.direccion_completa} />
            <DataRow label="Código Postal" value={datos_generales.cp} />
          </InfoCard>
        </Grid>

        {/* Datos Socioeconómicos */}
        <Grid item xs={12} md={6}>
          <InfoCard icon={<WorkIcon />} title="Datos Socioeconómicos">
            <DataRow label="Ocupación" value={datos_generales.ocupacion} />
            <DataRow label="Escolaridad" value={datos_generales.escolaridad} />
            <DataRow label="Estado Civil" value={datos_generales.estado_civil} />
            <DataRow
              label="Integrantes de la Familia"
              value={`${datos_generales.num_integrantes_familia} personas`}
            />
          </InfoCard>
        </Grid>

        {/* Seguro Médico */}
        <Grid item xs={12} md={6}>
          <InfoCard icon={<LocalHospitalIcon />} title="Seguro Médico">
            <DataRow
              label="¿Tiene Seguro?"
              value={datos_generales.tiene_seguro ? 'Sí' : 'No'}
            />
            {datos_generales.tiene_seguro && (
              <>
                <DataRow label="Tipo de Seguro" value={datos_generales.tipo_seguro} />
                <DataRow label="Número de Afiliación" value={datos_generales.numero_afiliacion} />
              </>
            )}
          </InfoCard>
        </Grid>

        {/* Análisis de Contexto con IA */}
        {datos_generales.analisis_ia_contexto && (
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
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <PsychologyIcon sx={{ fontSize: 32, mr: 1.5 }} />
                    <Typography variant="h6" fontWeight="700">
                      Análisis Inteligente de Contexto (IA)
                    </Typography>
                  </Box>

                  <Grid container spacing={3}>
                    <Grid item xs={12} md={4}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Typography variant="caption" sx={{ opacity: 0.9 }}>
                          Nivel Socioeconómico Estimado
                        </Typography>
                        <Typography variant="h5" fontWeight="700">
                          {datos_generales.analisis_ia_contexto.nivel_socioeconomico_estimado}
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={4}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Typography variant="caption" sx={{ opacity: 0.9 }}>
                          Riesgo de Deserción
                        </Typography>
                        <Typography variant="h5" fontWeight="700">
                          {datos_generales.analisis_ia_contexto.riesgo_desercion}%
                        </Typography>
                        <Box sx={{ mt: 1, bgcolor: 'rgba(255,255,255,0.2)', borderRadius: 1, overflow: 'hidden' }}>
                          <Box
                            sx={{
                              width: `${datos_generales.analisis_ia_contexto.riesgo_desercion}%`,
                              height: 8,
                              bgcolor: datos_generales.analisis_ia_contexto.riesgo_desercion > 50
                                ? '#ff6b6b'
                                : datos_generales.analisis_ia_contexto.riesgo_desercion > 30
                                ? '#ffd93d'
                                : '#6bcf7f',
                            }}
                          />
                        </Box>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={12}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1.5 }}>
                          <LightbulbIcon sx={{ mr: 1 }} />
                          <Typography variant="subtitle1" fontWeight="700">
                            Recomendaciones de Adaptación
                          </Typography>
                        </Box>
                        <List dense>
                          {datos_generales.analisis_ia_contexto.recomendaciones_adaptacion.map((rec, index) => (
                            <ListItem key={index} sx={{ px: 0 }}>
                              <ListItemText
                                primary={rec}
                                primaryTypographyProps={{
                                  sx: { color: 'white', fontSize: '0.95rem' }
                                }}
                              />
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

export default DatosGeneralesView;
