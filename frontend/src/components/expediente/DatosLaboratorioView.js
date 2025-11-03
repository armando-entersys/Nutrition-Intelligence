import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Tabs,
  Tab,
  IconButton,
  Tooltip,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  Science as ScienceIcon,
  Add as AddIcon,
  Upload as UploadIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  TrendingFlat as TrendingFlatIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  PictureAsPdf as PdfIcon,
  Refresh as RefreshIcon,
  Visibility as VisibilityIcon,
  Delete as DeleteIcon,
  Analytics as AnalyticsIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';

const DatosLaboratorioView = ({ paciente }) => {
  const [labRecords, setLabRecords] = useState([]);
  const [selectedLab, setSelectedLab] = useState(null);
  const [loading, setLoading] = useState(false);
  const [openAddDialog, setOpenAddDialog] = useState(false);
  const [openViewDialog, setOpenViewDialog] = useState(false);
  const [openUploadDialog, setOpenUploadDialog] = useState(false);
  const [currentTab, setCurrentTab] = useState(0);
  const [trends, setTrends] = useState([]);
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [fileToUpload, setFileToUpload] = useState({
    file: null,
    file_type: 'laboratory',
    description: '',
    document_date: new Date().toISOString().split('T')[0],
  });

  // Form state for new lab
  const [newLab, setNewLab] = useState({
    study_date: new Date().toISOString().split('T')[0],
    test_type: 'blood_chemistry',
    laboratory_name: '',
    ordering_physician: '',
    fasting_glucose_mgdl: '',
    hemoglobin_a1c_pct: '',
    total_cholesterol_mgdl: '',
    ldl_cholesterol_mgdl: '',
    hdl_cholesterol_mgdl: '',
    triglycerides_mgdl: '',
    creatinine_mgdl: '',
    alt_tgp_UI_l: '',
  });

  useEffect(() => {
    if (paciente?.id) {
      loadLabRecords();
      loadTrends();
      loadFiles();
    }
  }, [paciente]);

  const loadLabRecords = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/laboratory/patient/${paciente.id}`);
      setLabRecords(response.data.items || []);
    } catch (error) {
      console.error('Error loading lab records:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadTrends = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/laboratory/trends/patient/${paciente.id}`);
      setTrends(response.data || []);
    } catch (error) {
      console.error('Error loading trends:', error);
    }
  };

  const loadFiles = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/laboratory/files/patient/${paciente.id}`);
      setFiles(response.data || []);
    } catch (error) {
      console.error('Error loading files:', error);
    }
  };

  const handleFileUpload = async () => {
    if (!fileToUpload.file) {
      alert('Por favor selecciona un archivo');
      return;
    }

    try {
      setUploadProgress(10);
      const formData = new FormData();
      formData.append('file', fileToUpload.file);

      const queryParams = new URLSearchParams({
        patient_id: paciente.id,
        file_type: fileToUpload.file_type,
        description: fileToUpload.description || '',
        document_date: fileToUpload.document_date,
        uploaded_by: 'nutritionist',
        uploaded_by_id: 1,
      });

      setUploadProgress(30);

      const response = await axios.post(
        `${API_BASE_URL}/api/v1/laboratory/files/upload?${queryParams}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              30 + (progressEvent.loaded * 60) / progressEvent.total
            );
            setUploadProgress(percentCompleted);
          },
        }
      );

      setUploadProgress(100);
      console.log('File uploaded successfully:', response.data);

      // Reset form
      setFileToUpload({
        file: null,
        file_type: 'laboratory',
        description: '',
        document_date: new Date().toISOString().split('T')[0],
      });
      setOpenUploadDialog(false);
      setUploadProgress(0);

      // Reload files
      await loadFiles();
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error al subir el archivo: ' + (error.response?.data?.detail || error.message));
      setUploadProgress(0);
    }
  };

  const handleDeleteFile = async (fileId) => {
    if (!window.confirm('¿Estás seguro de eliminar este archivo?')) {
      return;
    }

    try {
      await axios.delete(`${API_BASE_URL}/api/v1/laboratory/files/${fileId}`);
      await loadFiles();
    } catch (error) {
      console.error('Error deleting file:', error);
      alert('Error al eliminar el archivo');
    }
  };

  const handleAddLab = async () => {
    try {
      // Filter out empty values
      const labData = Object.fromEntries(
        Object.entries(newLab).filter(([_, value]) => value !== '')
      );
      labData.patient_id = paciente.id;

      await axios.post(`${API_BASE_URL}/api/v1/laboratory/`, labData);
      setOpenAddDialog(false);
      loadLabRecords();
      loadTrends();
      // Reset form
      setNewLab({
        study_date: new Date().toISOString().split('T')[0],
        test_type: 'blood_chemistry',
        laboratory_name: '',
        ordering_physician: '',
        fasting_glucose_mgdl: '',
        hemoglobin_a1c_pct: '',
        total_cholesterol_mgdl: '',
        ldl_cholesterol_mgdl: '',
        hdl_cholesterol_mgdl: '',
        triglycerides_mgdl: '',
        creatinine_mgdl: '',
        alt_tgp_UI_l: '',
      });
    } catch (error) {
      console.error('Error adding lab record:', error);
      alert('Error al agregar laboratorio: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleViewLab = (lab) => {
    setSelectedLab(lab);
    setOpenViewDialog(true);
  };

  const handleDeleteLab = async (labId) => {
    if (!window.confirm('¿Estás seguro de eliminar este laboratorio?')) return;

    try {
      await axios.delete(`${API_BASE_URL}/api/v1/laboratory/${labId}`);
      loadLabRecords();
      loadTrends();
    } catch (error) {
      console.error('Error deleting lab record:', error);
      alert('Error al eliminar laboratorio');
    }
  };

  const getSeverityColor = (severity) => {
    const colors = {
      normal: '#51cf66',
      mild: '#ffd43b',
      moderate: '#ff9f43',
      severe: '#f44336',
    };
    return colors[severity] || '#9e9e9e';
  };

  const getTrendIcon = (direction) => {
    if (direction === 'improving') return <TrendingDownIcon sx={{ color: '#51cf66' }} />;
    if (direction === 'worsening') return <TrendingUpIcon sx={{ color: '#f44336' }} />;
    return <TrendingFlatIcon sx={{ color: '#9e9e9e' }} />;
  };

  const prepareChartData = (parameterName) => {
    const trend = trends.find(t => t.parameter_name === parameterName);
    if (!trend || !trend.values) return [];

    return trend.values.map(v => ({
      date: new Date(v.date).toLocaleDateString('es-MX', { month: 'short', day: 'numeric' }),
      value: v.value,
    }));
  };

  return (
    <Box>
      {/* Header with actions */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" fontWeight="700">
          📊 Datos de Laboratorio
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setOpenAddDialog(true)}
            sx={{ bgcolor: '#006847' }}
          >
            Agregar Laboratorio
          </Button>
          <Button
            variant="outlined"
            startIcon={<UploadIcon />}
            onClick={() => alert('Funcionalidad de upload próximamente')}
          >
            Subir PDF
          </Button>
        </Box>
      </Box>

      {/* Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={currentTab} onChange={(e, v) => setCurrentTab(v)}>
          <Tab icon={<ScienceIcon />} label="Laboratorios" iconPosition="start" />
          <Tab icon={<AnalyticsIcon />} label="Tendencias" iconPosition="start" />
          <Tab icon={<PdfIcon />} label={`Archivos (${files.length})`} iconPosition="start" />
        </Tabs>
      </Paper>

      {loading && <LinearProgress sx={{ mb: 2 }} />}

      {/* TAB 1: Laboratorios */}
      {currentTab === 0 && (
        <Grid container spacing={2}>
          {labRecords.length === 0 ? (
            <Grid item xs={12}>
              <Paper sx={{ p: 6, textAlign: 'center' }}>
                <ScienceIcon sx={{ fontSize: 80, color: '#bdbdbd', mb: 2 }} />
                <Typography variant="h6" color="text.secondary">
                  No hay laboratorios registrados
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={() => setOpenAddDialog(true)}
                  sx={{ mt: 2, bgcolor: '#006847' }}
                >
                  Agregar primer laboratorio
                </Button>
              </Paper>
            </Grid>
          ) : (
            labRecords.map((lab, index) => (
              <Grid item xs={12} key={lab.id}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <Card sx={{ borderRadius: 3 }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                        <Box>
                          <Typography variant="h6" fontWeight="700">
                            {lab.laboratory_name}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {new Date(lab.study_date).toLocaleDateString('es-MX', {
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric',
                            })}
                          </Typography>
                          <Chip
                            label={lab.test_type.replace('_', ' ').toUpperCase()}
                            size="small"
                            sx={{ mt: 1 }}
                          />
                        </Box>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          <Tooltip title="Ver detalles">
                            <IconButton onClick={() => handleViewLab(lab)} color="primary">
                              <VisibilityIcon />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Eliminar">
                            <IconButton onClick={() => handleDeleteLab(lab.id)} color="error">
                              <DeleteIcon />
                            </IconButton>
                          </Tooltip>
                        </Box>
                      </Box>

                      {/* Quick summary of key values */}
                      <Grid container spacing={2} sx={{ mb: 2 }}>
                        {lab.fasting_glucose_mgdl && (
                          <Grid item xs={6} md={3}>
                            <Paper sx={{ p: 1.5, bgcolor: '#f5f5f5', textAlign: 'center' }}>
                              <Typography variant="caption" color="text.secondary">
                                Glucosa
                              </Typography>
                              <Typography variant="h6" fontWeight="700">
                                {lab.fasting_glucose_mgdl} mg/dL
                              </Typography>
                            </Paper>
                          </Grid>
                        )}
                        {lab.hemoglobin_a1c_pct && (
                          <Grid item xs={6} md={3}>
                            <Paper sx={{ p: 1.5, bgcolor: '#f5f5f5', textAlign: 'center' }}>
                              <Typography variant="caption" color="text.secondary">
                                HbA1c
                              </Typography>
                              <Typography variant="h6" fontWeight="700">
                                {lab.hemoglobin_a1c_pct}%
                              </Typography>
                            </Paper>
                          </Grid>
                        )}
                        {lab.total_cholesterol_mgdl && (
                          <Grid item xs={6} md={3}>
                            <Paper sx={{ p: 1.5, bgcolor: '#f5f5f5', textAlign: 'center' }}>
                              <Typography variant="caption" color="text.secondary">
                                Colesterol
                              </Typography>
                              <Typography variant="h6" fontWeight="700">
                                {lab.total_cholesterol_mgdl} mg/dL
                              </Typography>
                            </Paper>
                          </Grid>
                        )}
                        {lab.triglycerides_mgdl && (
                          <Grid item xs={6} md={3}>
                            <Paper sx={{ p: 1.5, bgcolor: '#f5f5f5', textAlign: 'center' }}>
                              <Typography variant="caption" color="text.secondary">
                                Triglicéridos
                              </Typography>
                              <Typography variant="h6" fontWeight="700">
                                {lab.triglycerides_mgdl} mg/dL
                              </Typography>
                            </Paper>
                          </Grid>
                        )}
                      </Grid>

                      {/* AI Interpretation Summary */}
                      {lab.ai_interpretation && lab.ai_interpretation.out_of_range_values?.length > 0 && (
                        <Alert
                          severity={lab.ai_interpretation.critical_alerts?.length > 0 ? 'error' : 'warning'}
                          sx={{ mb: 1 }}
                        >
                          <Typography variant="subtitle2" fontWeight="700">
                            ⚠️ {lab.ai_interpretation.out_of_range_values.length} valores fuera de rango
                          </Typography>
                          {lab.ai_interpretation.out_of_range_values.slice(0, 2).map((val, idx) => (
                            <Typography key={idx} variant="caption" display="block">
                              • {val.parameter}: {val.value} ({val.clinical_meaning})
                            </Typography>
                          ))}
                        </Alert>
                      )}

                      {lab.ai_interpretation && lab.ai_interpretation.out_of_range_values?.length === 0 && (
                        <Alert severity="success">
                          ✅ Todos los valores dentro de rangos normales
                        </Alert>
                      )}
                    </CardContent>
                  </Card>
                </motion.div>
              </Grid>
            ))
          )}
        </Grid>
      )}

      {/* TAB 2: Tendencias */}
      {currentTab === 1 && (
        <Grid container spacing={3}>
          {trends.length === 0 ? (
            <Grid item xs={12}>
              <Paper sx={{ p: 6, textAlign: 'center' }}>
                <AnalyticsIcon sx={{ fontSize: 80, color: '#bdbdbd', mb: 2 }} />
                <Typography variant="h6" color="text.secondary">
                  Se requieren al menos 2 laboratorios para ver tendencias
                </Typography>
              </Paper>
            </Grid>
          ) : (
            trends.map((trend, index) => (
              <Grid item xs={12} md={6} key={index}>
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <Card sx={{ borderRadius: 3 }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                        <Typography variant="h6" fontWeight="700">
                          {trend.parameter_name}
                        </Typography>
                        {getTrendIcon(trend.trend)}
                      </Box>

                      <Box sx={{ mb: 2 }}>
                        <Typography variant="caption" color="text.secondary">
                          Rango normal: {trend.normal_range}
                        </Typography>
                      </Box>

                      {/* Chart */}
                      <ResponsiveContainer width="100%" height={200}>
                        <LineChart data={trend.values.map(v => ({
                          date: new Date(v.date).toLocaleDateString('es-MX', { month: 'short', day: 'numeric' }),
                          value: v.value
                        }))}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="date" />
                          <YAxis />
                          <RechartsTooltip />
                          <Line
                            type="monotone"
                            dataKey="value"
                            stroke={trend.trend === 'improving' ? '#51cf66' : trend.trend === 'worsening' ? '#f44336' : '#9e9e9e'}
                            strokeWidth={2}
                            dot={{ fill: '#006847', r: 4 }}
                          />
                        </LineChart>
                      </ResponsiveContainer>

                      <Alert
                        severity={trend.trend === 'improving' ? 'success' : trend.trend === 'worsening' ? 'warning' : 'info'}
                        sx={{ mt: 2 }}
                      >
                        {trend.interpretation}
                      </Alert>
                    </CardContent>
                  </Card>
                </motion.div>
              </Grid>
            ))
          )}
        </Grid>
      )}

      {/* TAB 3: Archivos */}
      {currentTab === 2 && (
        <Box>
          {files.length > 0 && (
            <Box sx={{ mb: 2, display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                startIcon={<UploadIcon />}
                onClick={() => setOpenUploadDialog(true)}
              >
                Subir archivo
              </Button>
            </Box>
          )}

          <Grid container spacing={2}>
            {files.length === 0 ? (
              <Grid item xs={12}>
                <Paper sx={{ p: 6, textAlign: 'center' }}>
                  <PdfIcon sx={{ fontSize: 80, color: '#bdbdbd', mb: 2 }} />
                  <Typography variant="h6" color="text.secondary">
                    No hay archivos cargados
                  </Typography>
                  <Button
                    variant="contained"
                    startIcon={<UploadIcon />}
                    onClick={() => setOpenUploadDialog(true)}
                    sx={{ mt: 2 }}
                  >
                    Subir primer archivo
                  </Button>
                </Paper>
              </Grid>
            ) : (
              files.map((file, index) => (
                <Grid item xs={12} md={6} key={file.id}>
                  <Card>
                    <CardContent>
                      <Box sx={{ display: 'flex', gap: 2 }}>
                        <PdfIcon sx={{ fontSize: 48, color: file.file_format === 'pdf' ? '#f44336' : '#2196F3' }} />
                        <Box sx={{ flex: 1 }}>
                          <Typography variant="subtitle1" fontWeight="700">
                            {file.file_name}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                            {file.description || 'Sin descripción'}
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 1 }}>
                            <Chip label={file.file_type} size="small" color="primary" />
                            <Chip label={`${file.file_size_mb} MB`} size="small" variant="outlined" />
                            {file.ocr_processed && (
                              <Chip label="OCR procesado" size="small" color="success" icon={<CheckCircleIcon />} />
                            )}
                          </Box>
                          <Typography variant="caption" color="text.secondary" display="block">
                            Subido: {new Date(file.uploaded_at).toLocaleDateString('es-MX', {
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric'
                            })}
                          </Typography>
                          {file.document_date && (
                            <Typography variant="caption" color="text.secondary" display="block">
                              Fecha del documento: {new Date(file.document_date).toLocaleDateString('es-MX')}
                            </Typography>
                          )}
                        </Box>
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                          <Tooltip title="Ver detalles">
                            <IconButton
                              size="small"
                              color="primary"
                              onClick={() => setSelectedFile(file)}
                            >
                              <VisibilityIcon />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Eliminar">
                            <IconButton
                              size="small"
                              color="error"
                              onClick={() => handleDeleteFile(file.id)}
                            >
                              <DeleteIcon />
                            </IconButton>
                          </Tooltip>
                        </Box>
                      </Box>

                      {file.ocr_processed && file.extracted_data && (
                        <Box sx={{ mt: 2, p: 2, bgcolor: '#f5f5f5', borderRadius: 2 }}>
                          <Typography variant="caption" fontWeight="700" display="block" gutterBottom>
                            Datos extraídos con OCR:
                          </Typography>
                          {file.extracted_data.analysis && (
                            <>
                              <Typography variant="caption" display="block">
                                <strong>Tipo de documento:</strong> {file.extracted_data.analysis.document_type}
                              </Typography>
                              {file.extracted_data.analysis.detected_values.length > 0 && (
                                <Box sx={{ mt: 1 }}>
                                  <Typography variant="caption" display="block" fontWeight="700">
                                    Valores detectados:
                                  </Typography>
                                  {file.extracted_data.analysis.detected_values.map((val, idx) => (
                                    <Chip
                                      key={idx}
                                      label={`${val.parameter}: ${val.value} ${val.unit}`}
                                      size="small"
                                      sx={{ mr: 0.5, mt: 0.5 }}
                                    />
                                  ))}
                                </Box>
                              )}
                            </>
                          )}
                        </Box>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
              ))
            )}
          </Grid>
        </Box>
      )}

      {/* Dialog: Add Lab */}
      <Dialog open={openAddDialog} onClose={() => setOpenAddDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <AddIcon />
            Agregar Nuevo Laboratorio
          </Box>
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Fecha del estudio"
                type="date"
                value={newLab.study_date}
                onChange={(e) => setNewLab({ ...newLab, study_date: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                select
                label="Tipo de estudio"
                value={newLab.test_type}
                onChange={(e) => setNewLab({ ...newLab, test_type: e.target.value })}
              >
                <MenuItem value="blood_chemistry">Química Sanguínea</MenuItem>
                <MenuItem value="lipid_profile">Perfil Lipídico</MenuItem>
                <MenuItem value="renal_function">Función Renal</MenuItem>
                <MenuItem value="liver_function">Función Hepática</MenuItem>
                <MenuItem value="thyroid_profile">Perfil Tiroideo</MenuItem>
                <MenuItem value="complete_blood_count">Biometría Hemática</MenuItem>
                <MenuItem value="vitamins_minerals">Vitaminas y Minerales</MenuItem>
                <MenuItem value="other">Otro</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Laboratorio"
                value={newLab.laboratory_name}
                onChange={(e) => setNewLab({ ...newLab, laboratory_name: e.target.value })}
                placeholder="Ej: Laboratorio Chopo"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Médico solicitante"
                value={newLab.ordering_physician}
                onChange={(e) => setNewLab({ ...newLab, ordering_physician: e.target.value })}
                placeholder="Opcional"
              />
            </Grid>

            <Grid item xs={12}>
              <Divider sx={{ my: 2 }}>
                <Chip label="Perfil Glucémico" />
              </Divider>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="Glucosa en ayunas (mg/dL)"
                value={newLab.fasting_glucose_mgdl}
                onChange={(e) => setNewLab({ ...newLab, fasting_glucose_mgdl: e.target.value })}
                placeholder="70-99"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="Hemoglobina A1c (%)"
                value={newLab.hemoglobin_a1c_pct}
                onChange={(e) => setNewLab({ ...newLab, hemoglobin_a1c_pct: e.target.value })}
                placeholder="< 5.7"
              />
            </Grid>

            <Grid item xs={12}>
              <Divider sx={{ my: 2 }}>
                <Chip label="Perfil Lipídico" />
              </Divider>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="Colesterol Total (mg/dL)"
                value={newLab.total_cholesterol_mgdl}
                onChange={(e) => setNewLab({ ...newLab, total_cholesterol_mgdl: e.target.value })}
                placeholder="< 200"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="LDL (mg/dL)"
                value={newLab.ldl_cholesterol_mgdl}
                onChange={(e) => setNewLab({ ...newLab, ldl_cholesterol_mgdl: e.target.value })}
                placeholder="< 100"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="HDL (mg/dL)"
                value={newLab.hdl_cholesterol_mgdl}
                onChange={(e) => setNewLab({ ...newLab, hdl_cholesterol_mgdl: e.target.value })}
                placeholder="> 40"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="Triglicéridos (mg/dL)"
                value={newLab.triglycerides_mgdl}
                onChange={(e) => setNewLab({ ...newLab, triglycerides_mgdl: e.target.value })}
                placeholder="< 150"
              />
            </Grid>

            <Grid item xs={12}>
              <Divider sx={{ my: 2 }}>
                <Chip label="Otros" />
              </Divider>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="Creatinina (mg/dL)"
                value={newLab.creatinine_mgdl}
                onChange={(e) => setNewLab({ ...newLab, creatinine_mgdl: e.target.value })}
                placeholder="0.6-1.2"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="number"
                label="ALT/TGP (UI/L)"
                value={newLab.alt_tgp_UI_l}
                onChange={(e) => setNewLab({ ...newLab, alt_tgp_UI_l: e.target.value })}
                placeholder="7-40"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAddDialog(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleAddLab} sx={{ bgcolor: '#006847' }}>
            Guardar Laboratorio
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog: View Lab Details */}
      <Dialog
        open={openViewDialog}
        onClose={() => setOpenViewDialog(false)}
        maxWidth="lg"
        fullWidth
      >
        {selectedLab && (
          <>
            <DialogTitle>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                  <Typography variant="h6" fontWeight="700">
                    {selectedLab.laboratory_name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {new Date(selectedLab.study_date).toLocaleDateString('es-MX', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })}
                  </Typography>
                </Box>
                <Chip label={selectedLab.test_type.replace('_', ' ').toUpperCase()} />
              </Box>
            </DialogTitle>
            <DialogContent>
              {/* AI Interpretation */}
              {selectedLab.ai_interpretation && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="h6" fontWeight="700" sx={{ mb: 2 }}>
                    🤖 Análisis con IA
                  </Typography>

                  {/* Critical Alerts */}
                  {selectedLab.ai_interpretation.critical_alerts?.length > 0 && (
                    <Alert severity="error" sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" fontWeight="700">
                        Alertas Críticas
                      </Typography>
                      {selectedLab.ai_interpretation.critical_alerts.map((alert, idx) => (
                        <Typography key={idx} variant="body2">
                          • {alert}
                        </Typography>
                      ))}
                    </Alert>
                  )}

                  {/* Out of Range Values */}
                  {selectedLab.ai_interpretation.out_of_range_values?.length > 0 && (
                    <TableContainer component={Paper} sx={{ mb: 2 }}>
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            <TableCell><strong>Parámetro</strong></TableCell>
                            <TableCell><strong>Valor</strong></TableCell>
                            <TableCell><strong>Rango Normal</strong></TableCell>
                            <TableCell><strong>Severidad</strong></TableCell>
                            <TableCell><strong>Significado</strong></TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {selectedLab.ai_interpretation.out_of_range_values.map((val, idx) => (
                            <TableRow key={idx}>
                              <TableCell>{val.parameter}</TableCell>
                              <TableCell><strong>{val.value}</strong></TableCell>
                              <TableCell>{val.normal_range}</TableCell>
                              <TableCell>
                                <Chip
                                  label={val.severity}
                                  size="small"
                                  sx={{ bgcolor: getSeverityColor(val.severity), color: 'white' }}
                                />
                              </TableCell>
                              <TableCell>{val.clinical_meaning}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  )}

                  {/* Diet Adjustments */}
                  {selectedLab.ai_interpretation.diet_adjustments?.length > 0 && (
                    <Alert severity="info" sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" fontWeight="700">
                        💡 Ajustes de Dieta Recomendados
                      </Typography>
                      {selectedLab.ai_interpretation.diet_adjustments.map((adj, idx) => (
                        <Typography key={idx} variant="body2">
                          • {adj}
                        </Typography>
                      ))}
                    </Alert>
                  )}

                  {/* Suggested Diagnoses */}
                  {selectedLab.ai_interpretation.suggested_diagnoses?.length > 0 && (
                    <Alert severity="warning" sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" fontWeight="700">
                        🔍 Diagnósticos Sugeridos (Requieren confirmación médica)
                      </Typography>
                      {selectedLab.ai_interpretation.suggested_diagnoses.map((diag, idx) => (
                        <Typography key={idx} variant="body2">
                          • {diag}
                        </Typography>
                      ))}
                    </Alert>
                  )}
                </Box>
              )}

              {/* All Lab Values */}
              <Typography variant="h6" fontWeight="700" sx={{ mb: 2 }}>
                📋 Todos los Valores
              </Typography>
              <TableContainer component={Paper}>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell><strong>Parámetro</strong></TableCell>
                      <TableCell><strong>Valor</strong></TableCell>
                      <TableCell><strong>Unidad</strong></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {selectedLab.fasting_glucose_mgdl && (
                      <TableRow>
                        <TableCell>Glucosa en ayunas</TableCell>
                        <TableCell><strong>{selectedLab.fasting_glucose_mgdl}</strong></TableCell>
                        <TableCell>mg/dL</TableCell>
                      </TableRow>
                    )}
                    {selectedLab.hemoglobin_a1c_pct && (
                      <TableRow>
                        <TableCell>Hemoglobina A1c</TableCell>
                        <TableCell><strong>{selectedLab.hemoglobin_a1c_pct}</strong></TableCell>
                        <TableCell>%</TableCell>
                      </TableRow>
                    )}
                    {selectedLab.total_cholesterol_mgdl && (
                      <TableRow>
                        <TableCell>Colesterol Total</TableCell>
                        <TableCell><strong>{selectedLab.total_cholesterol_mgdl}</strong></TableCell>
                        <TableCell>mg/dL</TableCell>
                      </TableRow>
                    )}
                    {selectedLab.ldl_cholesterol_mgdl && (
                      <TableRow>
                        <TableCell>LDL</TableCell>
                        <TableCell><strong>{selectedLab.ldl_cholesterol_mgdl}</strong></TableCell>
                        <TableCell>mg/dL</TableCell>
                      </TableRow>
                    )}
                    {selectedLab.hdl_cholesterol_mgdl && (
                      <TableRow>
                        <TableCell>HDL</TableCell>
                        <TableCell><strong>{selectedLab.hdl_cholesterol_mgdl}</strong></TableCell>
                        <TableCell>mg/dL</TableCell>
                      </TableRow>
                    )}
                    {selectedLab.triglycerides_mgdl && (
                      <TableRow>
                        <TableCell>Triglicéridos</TableCell>
                        <TableCell><strong>{selectedLab.triglycerides_mgdl}</strong></TableCell>
                        <TableCell>mg/dL</TableCell>
                      </TableRow>
                    )}
                    {selectedLab.creatinine_mgdl && (
                      <TableRow>
                        <TableCell>Creatinina</TableCell>
                        <TableCell><strong>{selectedLab.creatinine_mgdl}</strong></TableCell>
                        <TableCell>mg/dL</TableCell>
                      </TableRow>
                    )}
                    {selectedLab.alt_tgp_UI_l && (
                      <TableRow>
                        <TableCell>ALT/TGP</TableCell>
                        <TableCell><strong>{selectedLab.alt_tgp_UI_l}</strong></TableCell>
                        <TableCell>UI/L</TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setOpenViewDialog(false)}>Cerrar</Button>
            </DialogActions>
          </>
        )}
      </Dialog>

      {/* Dialog: Upload File */}
      <Dialog open={openUploadDialog} onClose={() => setOpenUploadDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <UploadIcon />
            Subir Archivo Clínico
          </Box>
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <input
                accept=".pdf,.jpg,.jpeg,.png"
                style={{ display: 'none' }}
                id="file-upload-input"
                type="file"
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    setFileToUpload({ ...fileToUpload, file: e.target.files[0] });
                  }
                }}
              />
              <label htmlFor="file-upload-input">
                <Button
                  variant="outlined"
                  component="span"
                  fullWidth
                  startIcon={<UploadIcon />}
                  sx={{ py: 2 }}
                >
                  {fileToUpload.file ? fileToUpload.file.name : 'Seleccionar archivo (PDF, JPG, PNG)'}
                </Button>
              </label>
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                select
                label="Tipo de archivo"
                value={fileToUpload.file_type}
                onChange={(e) => setFileToUpload({ ...fileToUpload, file_type: e.target.value })}
              >
                <MenuItem value="laboratory">Resultados de Laboratorio</MenuItem>
                <MenuItem value="radiology">Estudios de Imagen</MenuItem>
                <MenuItem value="ultrasound">Ultrasonido</MenuItem>
                <MenuItem value="prescription">Receta Médica</MenuItem>
                <MenuItem value="consent">Consentimiento</MenuItem>
                <MenuItem value="other">Otro</MenuItem>
              </TextField>
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Descripción (opcional)"
                value={fileToUpload.description}
                onChange={(e) => setFileToUpload({ ...fileToUpload, description: e.target.value })}
                multiline
                rows={2}
                placeholder="Ej: Resultados de química sanguínea completa"
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Fecha del documento"
                type="date"
                value={fileToUpload.document_date}
                onChange={(e) => setFileToUpload({ ...fileToUpload, document_date: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>

            {uploadProgress > 0 && (
              <Grid item xs={12}>
                <LinearProgress variant="determinate" value={uploadProgress} />
                <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
                  Subiendo archivo... {uploadProgress}%
                </Typography>
              </Grid>
            )}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            setOpenUploadDialog(false);
            setFileToUpload({
              file: null,
              file_type: 'laboratory',
              description: '',
              document_date: new Date().toISOString().split('T')[0],
            });
            setUploadProgress(0);
          }}>
            Cancelar
          </Button>
          <Button
            onClick={handleFileUpload}
            variant="contained"
            disabled={!fileToUpload.file || uploadProgress > 0}
          >
            {uploadProgress > 0 ? 'Subiendo...' : 'Subir archivo'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog: View File Details */}
      {selectedFile && (
        <Dialog open={!!selectedFile} onClose={() => setSelectedFile(null)} maxWidth="md" fullWidth>
          <DialogTitle>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <PdfIcon />
              Detalles del Archivo
            </Box>
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>{selectedFile.file_name}</Typography>
                <Divider sx={{ my: 2 }} />
              </Grid>

              <Grid item xs={6}>
                <Typography variant="caption" color="text.secondary">Tipo de archivo</Typography>
                <Typography variant="body1" fontWeight="600">{selectedFile.file_type}</Typography>
              </Grid>

              <Grid item xs={6}>
                <Typography variant="caption" color="text.secondary">Formato</Typography>
                <Typography variant="body1" fontWeight="600">{selectedFile.file_format.toUpperCase()}</Typography>
              </Grid>

              <Grid item xs={6}>
                <Typography variant="caption" color="text.secondary">Tamaño</Typography>
                <Typography variant="body1" fontWeight="600">{selectedFile.file_size_mb} MB</Typography>
              </Grid>

              <Grid item xs={6}>
                <Typography variant="caption" color="text.secondary">Fecha del documento</Typography>
                <Typography variant="body1" fontWeight="600">
                  {selectedFile.document_date
                    ? new Date(selectedFile.document_date).toLocaleDateString('es-MX')
                    : 'No especificada'}
                </Typography>
              </Grid>

              <Grid item xs={12}>
                <Typography variant="caption" color="text.secondary">Descripción</Typography>
                <Typography variant="body1">{selectedFile.description || 'Sin descripción'}</Typography>
              </Grid>

              {selectedFile.ocr_processed && selectedFile.extracted_data && (
                <>
                  <Grid item xs={12}>
                    <Divider sx={{ my: 1 }} />
                    <Typography variant="subtitle1" fontWeight="700" gutterBottom>
                      Datos extraídos con OCR
                    </Typography>
                  </Grid>

                  {selectedFile.extracted_data.analysis && (
                    <>
                      <Grid item xs={12}>
                        <Alert severity="info">
                          <strong>Tipo de documento detectado:</strong> {selectedFile.extracted_data.analysis.document_type}
                        </Alert>
                      </Grid>

                      {selectedFile.extracted_data.analysis.detected_values.length > 0 && (
                        <Grid item xs={12}>
                          <Typography variant="subtitle2" fontWeight="700" gutterBottom>
                            Valores detectados:
                          </Typography>
                          <TableContainer>
                            <Table size="small">
                              <TableHead>
                                <TableRow>
                                  <TableCell><strong>Parámetro</strong></TableCell>
                                  <TableCell><strong>Valor</strong></TableCell>
                                  <TableCell><strong>Unidad</strong></TableCell>
                                </TableRow>
                              </TableHead>
                              <TableBody>
                                {selectedFile.extracted_data.analysis.detected_values.map((val, idx) => (
                                  <TableRow key={idx}>
                                    <TableCell>{val.parameter}</TableCell>
                                    <TableCell><strong>{val.value}</strong></TableCell>
                                    <TableCell>{val.unit}</TableCell>
                                  </TableRow>
                                ))}
                              </TableBody>
                            </Table>
                          </TableContainer>
                        </Grid>
                      )}

                      {selectedFile.extracted_data.raw_text && (
                        <Grid item xs={12}>
                          <Typography variant="subtitle2" fontWeight="700" gutterBottom>
                            Texto extraído (primeros 1000 caracteres):
                          </Typography>
                          <Paper sx={{ p: 2, bgcolor: '#f5f5f5', maxHeight: 200, overflow: 'auto' }}>
                            <Typography variant="caption" style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
                              {selectedFile.extracted_data.raw_text.substring(0, 1000)}
                              {selectedFile.extracted_data.raw_text.length > 1000 && '...'}
                            </Typography>
                          </Paper>
                        </Grid>
                      )}
                    </>
                  )}
                </>
              )}
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setSelectedFile(null)}>Cerrar</Button>
          </DialogActions>
        </Dialog>
      )}
    </Box>
  );
};

export default DatosLaboratorioView;
