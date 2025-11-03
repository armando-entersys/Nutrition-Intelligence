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
  List,
  ListItem,
  ListItemText,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  MedicalServices as MedicalServicesIcon,
  FamilyRestroom as FamilyRestroomIcon,
  LocalHospital as LocalHospitalIcon,
  Medication as MedicationIcon,
  Psychology as PsychologyIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
  Business as BusinessIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const HistoriaClinicaView = ({ paciente }) => {
  const { historia_clinica } = paciente;

  const InfoCard = ({ icon, title, children, color = '#006847' }) => (
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
                bgcolor: color,
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

  const AntecedenteFamiliarItem = ({ titulo, presente, quien, tipo }) => (
    <Box sx={{ mb: 2 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
        {presente ? (
          <WarningIcon sx={{ color: '#ff6b6b', fontSize: 20 }} />
        ) : (
          <CheckCircleIcon sx={{ color: '#51cf66', fontSize: 20 }} />
        )}
        <Typography variant="body1" fontWeight="600">
          {titulo}
        </Typography>
        <Chip
          label={presente ? 'Presente' : 'No presente'}
          size="small"
          color={presente ? 'error' : 'success'}
        />
      </Box>
      {presente && quien && quien.length > 0 && (
        <Typography variant="body2" color="text.secondary" sx={{ ml: 3.5 }}>
          {quien.join(', ')}
        </Typography>
      )}
      {tipo && (
        <Typography variant="body2" color="text.secondary" sx={{ ml: 3.5 }}>
          Tipo: {tipo}
        </Typography>
      )}
    </Box>
  );

  return (
    <Box>
      <Grid container spacing={3}>
        {/* Antecedentes Heredofamiliares */}
        <Grid item xs={12} md={6}>
          <InfoCard icon={<FamilyRestroomIcon />} title="Antecedentes Heredofamiliares" color="#006847">
            <AntecedenteFamiliarItem
              titulo="Diabetes"
              presente={historia_clinica.antecedentes_familiares.diabetes.presente}
              quien={historia_clinica.antecedentes_familiares.diabetes.quien}
            />
            <AntecedenteFamiliarItem
              titulo="Hipertensión"
              presente={historia_clinica.antecedentes_familiares.hipertension.presente}
              quien={historia_clinica.antecedentes_familiares.hipertension.quien}
            />
            <AntecedenteFamiliarItem
              titulo="Obesidad"
              presente={historia_clinica.antecedentes_familiares.obesidad.presente}
              quien={historia_clinica.antecedentes_familiares.obesidad.quien}
            />
            <AntecedenteFamiliarItem
              titulo="Dislipidemias"
              presente={historia_clinica.antecedentes_familiares.dislipidemias.presente}
              quien={historia_clinica.antecedentes_familiares.dislipidemias.quien}
            />
            <AntecedenteFamiliarItem
              titulo="Cáncer"
              presente={historia_clinica.antecedentes_familiares.cancer.presente}
              quien={historia_clinica.antecedentes_familiares.cancer.quien}
              tipo={historia_clinica.antecedentes_familiares.cancer.tipo}
            />
            <AntecedenteFamiliarItem
              titulo="Enfermedades Cardiacas"
              presente={historia_clinica.antecedentes_familiares.enfermedades_cardiacas.presente}
              quien={historia_clinica.antecedentes_familiares.enfermedades_cardiacas.quien}
              tipo={historia_clinica.antecedentes_familiares.enfermedades_cardiacas.tipo}
            />
          </InfoCard>
        </Grid>

        {/* Antecedentes Personales Patológicos */}
        <Grid item xs={12} md={6}>
          <InfoCard icon={<LocalHospitalIcon />} title="Antecedentes Personales" color="#2196F3">
            <Typography variant="subtitle2" fontWeight="700" gutterBottom>
              Enfermedades Crónicas
            </Typography>
            {historia_clinica.antecedentes_patologicos.enfermedades_cronicas.length > 0 ? (
              <List dense>
                {historia_clinica.antecedentes_patologicos.enfermedades_cronicas.map((enfermedad, index) => (
                  <ListItem key={index} sx={{ px: 0 }}>
                    <ListItemText
                      primary={enfermedad.nombre}
                      secondary={
                        <>
                          Diagnóstico: {new Date(enfermedad.fecha_diagnostico).toLocaleDateString('es-MX')}
                          <br />
                          Tratamiento: {enfermedad.tratamiento_actual}
                          <br />
                          {enfermedad.controlada ? (
                            <Chip label="Controlada" size="small" color="success" sx={{ mt: 0.5 }} />
                          ) : (
                            <Chip label="No controlada" size="small" color="warning" sx={{ mt: 0.5 }} />
                          )}
                        </>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Sin enfermedades crónicas registradas
              </Typography>
            )}

            <Divider sx={{ my: 2 }} />

            <Typography variant="subtitle2" fontWeight="700" gutterBottom>
              Alergias e Intolerancias
            </Typography>
            <Box sx={{ mb: 2 }}>
              <Typography variant="caption" color="text.secondary">Alergias a Medicamentos:</Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                {historia_clinica.antecedentes_patologicos.alergias_medicamentos.length > 0 ? (
                  historia_clinica.antecedentes_patologicos.alergias_medicamentos.map((alergia, index) => (
                    <Chip key={index} label={alergia} size="small" color="error" />
                  ))
                ) : (
                  <Typography variant="body2" color="text.secondary">Ninguna</Typography>
                )}
              </Box>
            </Box>

            <Box sx={{ mb: 2 }}>
              <Typography variant="caption" color="text.secondary">Alergias a Alimentos:</Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                {historia_clinica.antecedentes_patologicos.alergias_alimentos.length > 0 ? (
                  historia_clinica.antecedentes_patologicos.alergias_alimentos.map((alergia, index) => (
                    <Chip key={index} label={alergia} size="small" color="error" />
                  ))
                ) : (
                  <Typography variant="body2" color="text.secondary">Ninguna</Typography>
                )}
              </Box>
            </Box>

            <Box>
              <Typography variant="caption" color="text.secondary">Intolerancias Alimentarias:</Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                {historia_clinica.antecedentes_patologicos.intolerancias_alimentarias.length > 0 ? (
                  historia_clinica.antecedentes_patologicos.intolerancias_alimentarias.map((intolerancia, index) => (
                    <Chip key={index} label={intolerancia} size="small" color="warning" />
                  ))
                ) : (
                  <Typography variant="body2" color="text.secondary">Ninguna</Typography>
                )}
              </Box>
            </Box>
          </InfoCard>
        </Grid>

        {/* Cirugías Previas */}
        <Grid item xs={12} md={6}>
          <InfoCard icon={<BusinessIcon />} title="Cirugías Previas" color="#FF9800">
            {historia_clinica.antecedentes_patologicos.cirugias_previas.length > 0 ? (
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell><strong>Tipo</strong></TableCell>
                      <TableCell><strong>Fecha</strong></TableCell>
                      <TableCell><strong>Hospital</strong></TableCell>
                      <TableCell><strong>Motivo</strong></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {historia_clinica.antecedentes_patologicos.cirugias_previas.map((cirugia, index) => (
                      <TableRow key={index}>
                        <TableCell>{cirugia.tipo}</TableCell>
                        <TableCell>{new Date(cirugia.fecha).toLocaleDateString('es-MX')}</TableCell>
                        <TableCell>{cirugia.hospital}</TableCell>
                        <TableCell>
                          {cirugia.motivo}
                          {cirugia.complicaciones && (
                            <Chip
                              label="Con complicaciones"
                              size="small"
                              color="warning"
                              sx={{ ml: 1 }}
                            />
                          )}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            ) : (
              <Typography variant="body2" color="text.secondary">
                Sin cirugías previas registradas
              </Typography>
            )}
          </InfoCard>
        </Grid>

        {/* Hospitalizaciones */}
        <Grid item xs={12} md={6}>
          <InfoCard icon={<LocalHospitalIcon />} title="Hospitalizaciones" color="#F44336">
            {historia_clinica.antecedentes_patologicos.hospitalizaciones.length > 0 ? (
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell><strong>Razón</strong></TableCell>
                      <TableCell><strong>Fecha</strong></TableCell>
                      <TableCell><strong>Duración</strong></TableCell>
                      <TableCell><strong>Hospital</strong></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {historia_clinica.antecedentes_patologicos.hospitalizaciones.map((hosp, index) => (
                      <TableRow key={index}>
                        <TableCell>{hosp.razon}</TableCell>
                        <TableCell>{new Date(hosp.fecha).toLocaleDateString('es-MX')}</TableCell>
                        <TableCell>
                          {hosp.duracion_dias} {hosp.duracion_dias === 1 ? 'día' : 'días'}
                        </TableCell>
                        <TableCell>{hosp.hospital}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            ) : (
              <Typography variant="body2" color="text.secondary">
                Sin hospitalizaciones previas registradas
              </Typography>
            )}
          </InfoCard>
        </Grid>

        {/* Antecedentes Gineco-obstétricos (si aplica) */}
        {historia_clinica.antecedentes_gineco && (
          <Grid item xs={12} md={6}>
            <InfoCard icon={<MedicalServicesIcon />} title="Antecedentes Gineco-Obstétricos" color="#E91E63">
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="caption" color="text.secondary">Menarca</Typography>
                  <Typography variant="body1" fontWeight="600">{historia_clinica.antecedentes_gineco.menarca_edad} años</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="caption" color="text.secondary">Ciclos</Typography>
                  <Typography variant="body1" fontWeight="600">
                    {historia_clinica.antecedentes_gineco.ciclos_regulares ? 'Regulares' : 'Irregulares'}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="caption" color="text.secondary">Embarazos</Typography>
                  <Typography variant="body1" fontWeight="600">{historia_clinica.antecedentes_gineco.embarazos_previos}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="caption" color="text.secondary">Partos</Typography>
                  <Typography variant="body1" fontWeight="600">{historia_clinica.antecedentes_gineco.partos}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="caption" color="text.secondary">Cesáreas</Typography>
                  <Typography variant="body1" fontWeight="600">{historia_clinica.antecedentes_gineco.cesareas}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="caption" color="text.secondary">Abortos</Typography>
                  <Typography variant="body1" fontWeight="600">{historia_clinica.antecedentes_gineco.abortos}</Typography>
                </Grid>
                <Grid item xs={12}>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    {historia_clinica.antecedentes_gineco.lactancia_actual && (
                      <Chip label="Lactancia actual" size="small" color="info" />
                    )}
                    {historia_clinica.antecedentes_gineco.menopausia && (
                      <Chip label={`Menopausia (${historia_clinica.antecedentes_gineco.edad_menopausia} años)`} size="small" />
                    )}
                    {historia_clinica.antecedentes_gineco.terapia_hormonal && (
                      <Chip label="Terapia hormonal" size="small" color="warning" />
                    )}
                  </Box>
                </Grid>
              </Grid>
            </InfoCard>
          </Grid>
        )}

        {/* Medicamentos y Suplementos */}
        <Grid item xs={12} md={6}>
          <InfoCard icon={<MedicationIcon />} title="Medicamentos y Suplementos" color="#9C27B0">
            <Typography variant="subtitle2" fontWeight="700" gutterBottom>
              Medicamentos Actuales
            </Typography>
            {historia_clinica.medicamentos_actuales.length > 0 ? (
              <TableContainer sx={{ mb: 2 }}>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell><strong>Medicamento</strong></TableCell>
                      <TableCell><strong>Dosis</strong></TableCell>
                      <TableCell><strong>Frecuencia</strong></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {historia_clinica.medicamentos_actuales.map((med, index) => (
                      <TableRow key={index}>
                        <TableCell>{med.nombre}</TableCell>
                        <TableCell>{med.dosis}</TableCell>
                        <TableCell>{med.frecuencia}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            ) : (
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Sin medicamentos actuales
              </Typography>
            )}

            <Divider sx={{ my: 2 }} />

            <Typography variant="subtitle2" fontWeight="700" gutterBottom>
              Suplementos
            </Typography>
            {historia_clinica.suplementos.length > 0 ? (
              <List dense>
                {historia_clinica.suplementos.map((supl, index) => (
                  <ListItem key={index} sx={{ px: 0 }}>
                    <ListItemText
                      primary={supl.nombre}
                      secondary={`${supl.dosis} - ${supl.frecuencia} (${supl.marca})`}
                    />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography variant="body2" color="text.secondary">
                Sin suplementos
              </Typography>
            )}
          </InfoCard>
        </Grid>

        {/* Análisis de Riesgo IA */}
        {historia_clinica.analisis_riesgo_ia && (
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
                      Análisis Inteligente de Riesgo (IA)
                    </Typography>
                  </Box>

                  <Grid container spacing={3}>
                    <Grid item xs={12} md={2.4}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2, textAlign: 'center' }}>
                        <Typography variant="caption" sx={{ opacity: 0.9 }}>
                          Cardiovascular
                        </Typography>
                        <Typography variant="h4" fontWeight="700">
                          {historia_clinica.analisis_riesgo_ia.riesgo_cardiovascular}%
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={2.4}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2, textAlign: 'center' }}>
                        <Typography variant="caption" sx={{ opacity: 0.9 }}>
                          Diabetes T2
                        </Typography>
                        <Typography variant="h4" fontWeight="700">
                          {historia_clinica.analisis_riesgo_ia.riesgo_diabetes_tipo2}%
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={2.4}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2, textAlign: 'center' }}>
                        <Typography variant="caption" sx={{ opacity: 0.9 }}>
                          Síndrome Metabólico
                        </Typography>
                        <Typography variant="h4" fontWeight="700">
                          {historia_clinica.analisis_riesgo_ia.riesgo_sindrome_metabolico}%
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={2.4}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2, textAlign: 'center' }}>
                        <Typography variant="caption" sx={{ opacity: 0.9 }}>
                          Osteoporosis
                        </Typography>
                        <Typography variant="h4" fontWeight="700">
                          {historia_clinica.analisis_riesgo_ia.riesgo_osteoporosis}%
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={2.4}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2, textAlign: 'center' }}>
                        <Typography variant="caption" sx={{ opacity: 0.9 }}>
                          Anemia
                        </Typography>
                        <Typography variant="h4" fontWeight="700">
                          {historia_clinica.analisis_riesgo_ia.riesgo_anemia}%
                        </Typography>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={6}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                          <WarningIcon />
                          <Typography variant="subtitle2" fontWeight="700">
                            Factores de Riesgo Identificados
                          </Typography>
                        </Box>
                        <Box component="ul" sx={{ m: 0, pl: 2 }}>
                          {historia_clinica.analisis_riesgo_ia.factores_riesgo_identificados.map((factor, index) => (
                            <Typography key={index} component="li" variant="body2" sx={{ mb: 0.5 }}>
                              {factor}
                            </Typography>
                          ))}
                        </Box>
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={6}>
                      <Box sx={{ bgcolor: 'rgba(255,255,255,0.1)', p: 2, borderRadius: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                          <CheckCircleIcon />
                          <Typography variant="subtitle2" fontWeight="700">
                            Recomendaciones Preventivas
                          </Typography>
                        </Box>
                        <Box component="ul" sx={{ m: 0, pl: 2 }}>
                          {historia_clinica.analisis_riesgo_ia.recomendaciones_preventivas.map((rec, index) => (
                            <Typography key={index} component="li" variant="body2" sx={{ mb: 0.5 }}>
                              {rec}
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

export default HistoriaClinicaView;
