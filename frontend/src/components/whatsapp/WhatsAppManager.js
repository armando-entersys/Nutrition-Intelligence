import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Card,
  CardContent,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Chip,
  List,
  ListItem,
  ListItemText,
  Alert,
  Tab,
  Tabs,
  IconButton,
  Divider,
} from '@mui/material';
import {
  WhatsApp as WhatsAppIcon,
  Send as SendIcon,
  Schedule as ScheduleIcon,
  Message as MessageIcon,
  History as HistoryIcon,
  Close as CloseIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';

const WhatsAppManager = () => {
  const [currentTab, setCurrentTab] = useState(0);
  const [openSendDialog, setOpenSendDialog] = useState(false);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedPatient, setSelectedPatient] = useState(null);

  const [messageForm, setMessageForm] = useState({
    message_type: 'appointment_reminder',
    patient_id: '',
    patient_name: '',
    patient_phone: '',
    message_body: '',
  });

  const messageTypes = [
    { value: 'appointment_reminder', label: 'Recordatorio de Cita', icon: '🗓️' },
    { value: 'meal_plan_ready', label: 'Plan de Alimentación Listo', icon: '📋' },
    { value: 'lab_results', label: 'Resultados de Laboratorio', icon: '🔬' },
    { value: 'motivational', label: 'Mensaje Motivacional', icon: '💪' },
    { value: 'follow_up', label: 'Seguimiento', icon: '👋' },
    { value: 'custom', label: 'Mensaje Personalizado', icon: '✉️' },
  ];

  useEffect(() => {
    if (currentTab === 1) {
      loadMessages();
    }
  }, [currentTab]);

  const loadMessages = async () => {
    setLoading(true);
    try {
      // Por ahora usamos un paciente de ejemplo (ID 1)
      const response = await axios.get(`${API_BASE_URL}/api/v1/whatsapp/messages/patient/1`);
      setMessages(response.data.items || []);
    } catch (error) {
      console.error('Error cargando mensajes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendAppointmentReminder = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/api/v1/whatsapp/send/appointment-reminder`, {
        patient_id: 1,
        patient_name: 'María Guadalupe Hernández López',
        patient_phone: '+525512345678',
        appointment_date: 'Viernes 10 de Enero, 2025',
        appointment_time: '10:00 AM',
        nutritionist_name: 'Dra. Ana Pérez Lizaur',
        nutritionist_id: 1,
      });

      if (response.data.success) {
        alert('✅ Mensaje enviado exitosamente');
        setOpenSendDialog(false);
        loadMessages();
      } else {
        alert('❌ Error al enviar mensaje: ' + (response.data.error || 'Error desconocido'));
      }
    } catch (error) {
      console.error('Error enviando mensaje:', error);
      alert('❌ Error al enviar mensaje: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSendMealPlanNotification = async () => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/api/v1/whatsapp/send/meal-plan-notification`, {
        patient_id: 1,
        patient_name: 'María Guadalupe Hernández López',
        patient_phone: '+525512345678',
        nutritionist_name: 'Dra. Ana Pérez Lizaur',
        nutritionist_id: 1,
      });

      if (response.data.success) {
        alert('✅ Notificación enviada exitosamente');
        setOpenSendDialog(false);
        loadMessages();
      } else {
        alert('❌ Error al enviar notificación: ' + (response.data.error || 'Error desconocido'));
      }
    } catch (error) {
      console.error('Error enviando notificación:', error);
      alert('❌ Error al enviar notificación: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleSendMotivationalMessage = async (messageText) => {
    try {
      setLoading(true);
      const response = await axios.post(`${API_BASE_URL}/api/v1/whatsapp/send/motivational-message`, {
        patient_id: 1,
        patient_name: 'María Guadalupe Hernández López',
        patient_phone: '+525512345678',
        message_text: messageText || '¡Sigue adelante! Cada pequeño paso cuenta en tu camino hacia una mejor salud. Estamos orgullosos de tu dedicación. 💪🥗',
        nutritionist_id: 1,
      });

      if (response.data.success) {
        alert('✅ Mensaje motivacional enviado');
        setOpenSendDialog(false);
        loadMessages();
      } else {
        alert('❌ Error al enviar mensaje: ' + (response.data.error || 'Error desconocido'));
      }
    } catch (error) {
      console.error('Error enviando mensaje:', error);
      alert('❌ Error al enviar mensaje: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      sent: 'success',
      delivered: 'info',
      read: 'primary',
      failed: 'error',
      queued: 'warning',
    };
    return colors[status] || 'default';
  };

  const getStatusIcon = (status) => {
    return status === 'sent' || status === 'delivered' ? <CheckCircleIcon /> : <ErrorIcon />;
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <WhatsAppIcon sx={{ fontSize: 40, color: '#25D366' }} />
          <Typography variant="h4" fontWeight="700">
            Mensajería WhatsApp
          </Typography>
        </Box>
        <Typography variant="body1" color="text.secondary">
          Envía notificaciones y mensajes a tus pacientes vía WhatsApp
        </Typography>
      </Box>

      {/* Tabs */}
      <Paper sx={{ borderRadius: 3, mb: 3 }}>
        <Tabs
          value={currentTab}
          onChange={(e, newValue) => setCurrentTab(newValue)}
          sx={{
            '& .MuiTab-root': {
              minHeight: 64,
              textTransform: 'none',
              fontSize: '1rem',
              fontWeight: 600,
            },
          }}
        >
          <Tab icon={<SendIcon />} label="Enviar Mensajes" iconPosition="start" />
          <Tab icon={<HistoryIcon />} label="Historial" iconPosition="start" />
        </Tabs>
      </Paper>

      {/* TAB 1: Enviar Mensajes */}
      {currentTab === 0 && (
        <Grid container spacing={3}>
          {/* Quick Actions */}
          <Grid item xs={12}>
            <Typography variant="h6" fontWeight="700" gutterBottom>
              Acciones Rápidas
            </Typography>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', cursor: 'pointer', '&:hover': { boxShadow: 4 } }} onClick={handleSendAppointmentReminder}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ fontSize: 48, mr: 2 }}>🗓️</Box>
                  <Box>
                    <Typography variant="h6" fontWeight="700">
                      Recordatorio de Cita
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Enviar recordatorio de próxima cita
                    </Typography>
                  </Box>
                </Box>
                <Button variant="contained" fullWidth disabled={loading}>
                  Enviar Recordatorio
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', cursor: 'pointer', '&:hover': { boxShadow: 4 } }} onClick={handleSendMealPlanNotification}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ fontSize: 48, mr: 2 }}>📋</Box>
                  <Box>
                    <Typography variant="h6" fontWeight="700">
                      Plan Listo
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Notificar plan de alimentación listo
                    </Typography>
                  </Box>
                </Box>
                <Button variant="contained" fullWidth disabled={loading}>
                  Enviar Notificación
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', cursor: 'pointer', '&:hover': { boxShadow: 4 } }} onClick={() => handleSendMotivationalMessage()}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ fontSize: 48, mr: 2 }}>💪</Box>
                  <Box>
                    <Typography variant="h6" fontWeight="700">
                      Mensaje Motivacional
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Enviar mensaje de motivación
                    </Typography>
                  </Box>
                </Box>
                <Button variant="contained" fullWidth disabled={loading}>
                  Enviar Mensaje
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Alert severity="info" icon={<WhatsAppIcon />}>
              <strong>Nota:</strong> Los mensajes se envían usando la cuenta de Twilio configurada.
              {' '}Para modo de prueba, se usarán valores mock. Configura tus credenciales de Twilio en el archivo .env del backend.
            </Alert>
          </Grid>
        </Grid>
      )}

      {/* TAB 2: Historial */}
      {currentTab === 1 && (
        <Box>
          <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h6" fontWeight="700">
              Mensajes Enviados
            </Typography>
            <Button variant="outlined" startIcon={<HistoryIcon />} onClick={loadMessages} disabled={loading}>
              Actualizar
            </Button>
          </Box>

          {messages.length === 0 ? (
            <Paper sx={{ p: 6, textAlign: 'center' }}>
              <MessageIcon sx={{ fontSize: 80, color: '#bdbdbd', mb: 2 }} />
              <Typography variant="h6" color="text.secondary">
                No hay mensajes enviados
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Los mensajes que envíes aparecerán aquí
              </Typography>
            </Paper>
          ) : (
            <List>
              {messages.map((message, index) => (
                <Paper key={message.id} sx={{ mb: 2, p: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Box sx={{ flex: 1 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                        <WhatsAppIcon sx={{ color: '#25D366' }} />
                        <Typography variant="subtitle1" fontWeight="700">
                          {message.recipient_name || message.recipient_phone}
                        </Typography>
                        <Chip
                          label={message.message_type.replace('_', ' ')}
                          size="small"
                          color="primary"
                        />
                        <Chip
                          label={message.status}
                          size="small"
                          color={getStatusColor(message.status)}
                          icon={getStatusIcon(message.status)}
                        />
                      </Box>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                        {message.message_body}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Enviado: {new Date(message.created_at).toLocaleString('es-MX')}
                      </Typography>
                      {message.twilio_sid && (
                        <Typography variant="caption" color="text.secondary" display="block">
                          Twilio SID: {message.twilio_sid}
                        </Typography>
                      )}
                    </Box>
                  </Box>
                </Paper>
              ))}
            </List>
          )}
        </Box>
      )}
    </Box>
  );
};

export default WhatsAppManager;
