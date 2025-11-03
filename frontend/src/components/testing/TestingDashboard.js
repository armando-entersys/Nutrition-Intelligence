/**
 * ============================================================================
 * Testing Dashboard - Sistema de Pruebas Colaborativo
 * ============================================================================
 * Dashboard profesional para gestión de casos de prueba
 * Permite comentarios de: Técnicos, Funcionales, Pacientes, Nutriólogos
 * ============================================================================
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Card,
  CardContent,
  Grid,
  Tabs,
  Tab,
  IconButton,
  Tooltip,
  Alert,
  LinearProgress,
  Badge,
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Schedule as ScheduleIcon,
  PlayArrow as PlayArrowIcon,
  Comment as CommentIcon,
  Assignment as AssignmentIcon,
  BugReport as BugReportIcon,
  People as PeopleIcon,
  Science as ScienceIcon,
  Download as DownloadIcon,
  Visibility as VisibilityIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const TestingDashboard = () => {
  const [currentTab, setCurrentTab] = useState(0);
  const [testCases, setTestCases] = useState([]);
  const [selectedTest, setSelectedTest] = useState(null);
  const [openCommentDialog, setOpenCommentDialog] = useState(false);
  const [commentForm, setCommentForm] = useState({
    role: 'tecnico',
    comment: '',
    status: '',
  });

  // Matriz de 15 casos de prueba E2E
  const initialTestCases = [
    // Expediente Clínico (5 casos)
    {
      id: 'E2E-001',
      category: 'Expediente Clínico',
      title: 'Carga de aplicación con Web Vitals',
      description: 'Validar que la app carga en <5s con FCP <2.5s',
      priority: 'Alta',
      type: 'Automatizada',
      status: 'Pending',
      assignedTo: '',
      comments: [],
      automated: true,
    },
    {
      id: 'E2E-002',
      category: 'Expediente Clínico',
      title: 'Navegación a Expediente Clínico',
      description: 'Validar navegación y carga de tabs del expediente',
      priority: 'Alta',
      type: 'Automatizada',
      status: 'Pending',
      assignedTo: '',
      comments: [],
      automated: true,
    },
    {
      id: 'E2E-003',
      category: 'Expediente Clínico',
      title: 'Acceso a Historia Clínica',
      description: 'Validar visualización y edición de historia clínica',
      priority: 'Media',
      type: 'Manual',
      status: 'Pending',
      assignedTo: 'Nutriólogo',
      comments: [],
      automated: false,
    },
    {
      id: 'E2E-004',
      category: 'Expediente Clínico',
      title: 'Datos de Laboratorio',
      description: 'Validar carga y visualización de datos de laboratorio',
      priority: 'Alta',
      type: 'Manual',
      status: 'Pending',
      assignedTo: 'Técnico + Nutriólogo',
      comments: [],
      automated: false,
    },
    {
      id: 'E2E-005',
      category: 'Expediente Clínico',
      title: 'Responsive Design (Mobile)',
      description: 'Validar funcionamiento en dispositivos móviles',
      priority: 'Media',
      type: 'Manual',
      status: 'Pending',
      assignedTo: 'Paciente',
      comments: [],
      automated: false,
    },

    // WhatsApp Integration (5 casos)
    {
      id: 'E2E-WA-001',
      category: 'WhatsApp',
      title: 'Navegación WhatsApp Manager',
      description: 'Validar acceso a sección de mensajería',
      priority: 'Media',
      type: 'Manual',
      status: 'Pending',
      assignedTo: 'Nutriólogo',
      comments: [],
      automated: false,
    },
    {
      id: 'E2E-WA-002',
      category: 'WhatsApp',
      title: 'Mensajes Rápidos',
      description: 'Validar interfaz de mensajes predefinidos',
      priority: 'Media',
      type: 'Manual',
      status: 'Pending',
      assignedTo: 'Funcional',
      comments: [],
      automated: false,
    },
    {
      id: 'E2E-WA-003',
      category: 'WhatsApp',
      title: 'Envío de Recordatorio',
      description: 'Validar envío de recordatorios de cita',
      priority: 'Alta',
      type: 'Manual',
      status: 'Pending',
      assignedTo: 'Nutriólogo + Paciente',
      comments: [],
      automated: false,
    },
    {
      id: 'E2E-WA-004',
      category: 'WhatsApp',
      title: 'Historial de Mensajes',
      description: 'Validar visualización de historial',
      priority: 'Media',
      type: 'Manual',
      status: 'Pending',
      assignedTo: 'Técnico',
      comments: [],
      automated: false,
    },
    {
      id: 'E2E-WA-005',
      category: 'WhatsApp',
      title: 'Configuración Twilio',
      description: 'Validar configuración y alertas de Twilio',
      priority: 'Baja',
      type: 'Manual',
      status: 'Pending',
      assignedTo: 'Técnico',
      comments: [],
      automated: false,
    },

    // AI Vision (5 casos)
    {
      id: 'E2E-AI-001',
      category: 'AI Vision',
      title: 'Navegación Análisis de Fotos',
      description: 'Validar acceso a módulo de análisis con IA',
      priority: 'Media',
      type: 'Manual',
      status: 'Pending',
      assignedTo: 'Funcional',
      comments: [],
      automated: false,
    },
    {
      id: 'E2E-AI-002',
      category: 'AI Vision',
      title: 'Interfaz de Carga',
      description: 'Validar UI de carga de fotos',
      priority: 'Media',
      type: 'Manual',
      status: 'Pending',
      assignedTo: 'Nutriólogo + Paciente',
      comments: [],
      automated: false,
    },
    {
      id: 'E2E-AI-003',
      category: 'AI Vision',
      title: 'Configuración IA (Gemini/Claude)',
      description: 'Validar selección de modelo de IA',
      priority: 'Alta',
      type: 'Manual',
      status: 'Pending',
      assignedTo: 'Técnico',
      comments: [],
      automated: false,
    },
    {
      id: 'E2E-AI-004',
      category: 'AI Vision',
      title: 'Análisis de Foto Real',
      description: 'Validar análisis completo de alimento con IA',
      priority: 'Alta',
      type: 'Manual',
      status: 'Pending',
      assignedTo: 'Paciente + Nutriólogo',
      comments: [],
      automated: false,
    },
    {
      id: 'E2E-AI-005',
      category: 'AI Vision',
      title: 'Accesibilidad',
      description: 'Validar estándares de accesibilidad WCAG AA',
      priority: 'Media',
      type: 'Manual',
      status: 'Pending',
      assignedTo: 'Funcional',
      comments: [],
      automated: false,
    },
  ];

  useEffect(() => {
    // Cargar test cases desde localStorage o usar iniciales
    const saved = localStorage.getItem('nutrition_test_cases');
    if (saved) {
      setTestCases(JSON.parse(saved));
    } else {
      setTestCases(initialTestCases);
    }
  }, []);

  const saveTestCases = (cases) => {
    setTestCases(cases);
    localStorage.setItem('nutrition_test_cases', JSON.stringify(cases));
  };

  const handleOpenCommentDialog = (testCase) => {
    setSelectedTest(testCase);
    setOpenCommentDialog(true);
  };

  const handleAddComment = () => {
    if (!commentForm.comment.trim()) return;

    const updated = testCases.map(tc => {
      if (tc.id === selectedTest.id) {
        const newComment = {
          id: Date.now(),
          role: commentForm.role,
          comment: commentForm.comment,
          timestamp: new Date().toISOString(),
          author: getRoleLabel(commentForm.role),
        };

        return {
          ...tc,
          comments: [...tc.comments, newComment],
          status: commentForm.status || tc.status,
        };
      }
      return tc;
    });

    saveTestCases(updated);
    setOpenCommentDialog(false);
    setCommentForm({ role: 'tecnico', comment: '', status: '' });
  };

  const handleUpdateStatus = (testId, newStatus) => {
    const updated = testCases.map(tc =>
      tc.id === testId ? { ...tc, status: newStatus } : tc
    );
    saveTestCases(updated);
  };

  const getRoleLabel = (role) => {
    const roles = {
      tecnico: '👨‍💻 Técnico',
      funcional: '📋 Funcional',
      nutriologo: '🥗 Nutriólogo',
      paciente: '😊 Paciente',
    };
    return roles[role] || role;
  };

  const getStatusColor = (status) => {
    const colors = {
      Pending: 'default',
      'In Progress': 'info',
      Passed: 'success',
      Failed: 'error',
      Blocked: 'warning',
    };
    return colors[status] || 'default';
  };

  const getStatusIcon = (status) => {
    const icons = {
      Pending: <ScheduleIcon />,
      'In Progress': <PlayArrowIcon />,
      Passed: <CheckCircleIcon />,
      Failed: <ErrorIcon />,
      Blocked: <BugReportIcon />,
    };
    return icons[status] || <ScheduleIcon />;
  };

  const getPriorityColor = (priority) => {
    return priority === 'Alta' ? 'error' : priority === 'Media' ? 'warning' : 'info';
  };

  const calculateStats = () => {
    const total = testCases.length;
    const passed = testCases.filter(tc => tc.status === 'Passed').length;
    const failed = testCases.filter(tc => tc.status === 'Failed').length;
    const inProgress = testCases.filter(tc => tc.status === 'In Progress').length;
    const pending = testCases.filter(tc => tc.status === 'Pending').length;
    const automated = testCases.filter(tc => tc.automated).length;
    const manual = testCases.filter(tc => !tc.automated).length;

    return { total, passed, failed, inProgress, pending, automated, manual };
  };

  const exportResults = () => {
    const dataStr = JSON.stringify(testCases, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
    const exportFileDefaultName = `test-results-${new Date().toISOString().split('T')[0]}.json`;

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const stats = calculateStats();
  const progressPercent = stats.total > 0 ? ((stats.passed + stats.failed) / stats.total) * 100 : 0;

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <AssignmentIcon sx={{ fontSize: 40, color: 'primary.main' }} />
            <Typography variant="h4" fontWeight="700">
              Dashboard de Pruebas
            </Typography>
          </Box>
          <Button
            variant="outlined"
            startIcon={<DownloadIcon />}
            onClick={exportResults}
          >
            Exportar Resultados
          </Button>
        </Box>
        <Typography variant="body1" color="text.secondary">
          Sistema colaborativo de pruebas E2E - Nutrition Intelligence Platform
        </Typography>
      </Box>

      {/* Statistics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={3}>
          <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
            <CardContent>
              <Typography variant="h3" fontWeight="700">{stats.total}</Typography>
              <Typography variant="body2">Total de Casos</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card sx={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', color: 'white' }}>
            <CardContent>
              <Typography variant="h3" fontWeight="700">{stats.passed}</Typography>
              <Typography variant="body2">✅ Pasaron</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card sx={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white' }}>
            <CardContent>
              <Typography variant="h3" fontWeight="700">{stats.automated}</Typography>
              <Typography variant="body2">🤖 Automatizadas</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card sx={{ background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', color: 'white' }}>
            <CardContent>
              <Typography variant="h3" fontWeight="700">{stats.manual}</Typography>
              <Typography variant="body2">👥 Manuales</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Progress */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" fontWeight="700" gutterBottom>
          Progreso General
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Box sx={{ flex: 1 }}>
            <LinearProgress
              variant="determinate"
              value={progressPercent}
              sx={{ height: 10, borderRadius: 5 }}
            />
          </Box>
          <Typography variant="h6" fontWeight="700">
            {progressPercent.toFixed(1)}%
          </Typography>
        </Box>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          {stats.passed + stats.failed} de {stats.total} casos completados
        </Typography>
      </Paper>

      {/* Test Cases Table */}
      <Paper sx={{ borderRadius: 3 }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow sx={{ bgcolor: 'grey.100' }}>
                <TableCell><strong>ID</strong></TableCell>
                <TableCell><strong>Categoría</strong></TableCell>
                <TableCell><strong>Título</strong></TableCell>
                <TableCell><strong>Tipo</strong></TableCell>
                <TableCell><strong>Asignado a</strong></TableCell>
                <TableCell><strong>Prioridad</strong></TableCell>
                <TableCell><strong>Estado</strong></TableCell>
                <TableCell><strong>Comentarios</strong></TableCell>
                <TableCell><strong>Acciones</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {testCases.map((testCase, index) => (
                <TableRow key={testCase.id} hover>
                  <TableCell>
                    <Chip
                      label={testCase.id}
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                  </TableCell>
                  <TableCell>{testCase.category}</TableCell>
                  <TableCell>
                    <Typography variant="body2" fontWeight="600">
                      {testCase.title}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {testCase.description}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={testCase.type}
                      size="small"
                      color={testCase.automated ? 'info' : 'default'}
                      icon={testCase.automated ? <ScienceIcon /> : <PeopleIcon />}
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="caption">{testCase.assignedTo}</Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={testCase.priority}
                      size="small"
                      color={getPriorityColor(testCase.priority)}
                    />
                  </TableCell>
                  <TableCell>
                    <FormControl size="small" sx={{ minWidth: 130 }}>
                      <Select
                        value={testCase.status}
                        onChange={(e) => handleUpdateStatus(testCase.id, e.target.value)}
                        displayEmpty
                      >
                        <MenuItem value="Pending">⏳ Pending</MenuItem>
                        <MenuItem value="In Progress">▶️ In Progress</MenuItem>
                        <MenuItem value="Passed">✅ Passed</MenuItem>
                        <MenuItem value="Failed">❌ Failed</MenuItem>
                        <MenuItem value="Blocked">🚫 Blocked</MenuItem>
                      </Select>
                    </FormControl>
                  </TableCell>
                  <TableCell>
                    <Badge badgeContent={testCase.comments.length} color="primary">
                      <IconButton
                        size="small"
                        onClick={() => handleOpenCommentDialog(testCase)}
                      >
                        <CommentIcon />
                      </IconButton>
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Tooltip title="Ver detalles">
                      <IconButton size="small">
                        <VisibilityIcon />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Comment Dialog */}
      <Dialog
        open={openCommentDialog}
        onClose={() => setOpenCommentDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {selectedTest?.id} - {selectedTest?.title}
        </DialogTitle>
        <DialogContent>
          {/* Existing Comments */}
          {selectedTest?.comments.length > 0 && (
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle2" fontWeight="700" gutterBottom>
                Comentarios Anteriores
              </Typography>
              {selectedTest.comments.map(comment => (
                <Paper key={comment.id} sx={{ p: 2, mb: 2, bgcolor: 'grey.50' }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="subtitle2" fontWeight="600">
                      {comment.author}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {new Date(comment.timestamp).toLocaleString('es-MX')}
                    </Typography>
                  </Box>
                  <Typography variant="body2">{comment.comment}</Typography>
                </Paper>
              ))}
            </Box>
          )}

          {/* New Comment Form */}
          <Typography variant="subtitle2" fontWeight="700" gutterBottom>
            Agregar Nuevo Comentario
          </Typography>

          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Rol</InputLabel>
            <Select
              value={commentForm.role}
              label="Rol"
              onChange={(e) => setCommentForm({ ...commentForm, role: e.target.value })}
            >
              <MenuItem value="tecnico">👨‍💻 Técnico QA</MenuItem>
              <MenuItem value="funcional">📋 Analista Funcional</MenuItem>
              <MenuItem value="nutriologo">🥗 Nutriólogo</MenuItem>
              <MenuItem value="paciente">😊 Paciente</MenuItem>
            </Select>
          </FormControl>

          <TextField
            fullWidth
            multiline
            rows={4}
            label="Comentario"
            placeholder="Describe tu observación, resultado de la prueba, o feedback..."
            value={commentForm.comment}
            onChange={(e) => setCommentForm({ ...commentForm, comment: e.target.value })}
            sx={{ mb: 2 }}
          />

          <FormControl fullWidth>
            <InputLabel>Cambiar Estado (Opcional)</InputLabel>
            <Select
              value={commentForm.status}
              label="Cambiar Estado (Opcional)"
              onChange={(e) => setCommentForm({ ...commentForm, status: e.target.value })}
            >
              <MenuItem value="">-- No cambiar --</MenuItem>
              <MenuItem value="In Progress">▶️ In Progress</MenuItem>
              <MenuItem value="Passed">✅ Passed</MenuItem>
              <MenuItem value="Failed">❌ Failed</MenuItem>
              <MenuItem value="Blocked">🚫 Blocked</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenCommentDialog(false)}>Cancelar</Button>
          <Button variant="contained" onClick={handleAddComment}>
            Agregar Comentario
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default TestingDashboard;
