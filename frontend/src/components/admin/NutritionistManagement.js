/**
 * Nutritionist Management - Gestión de Nutriólogos
 * Aprobación de cuentas, gestión de pacientes asignados
 */
import React, { useState, useEffect } from 'react';
import {
  Box, Paper, Typography, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, IconButton, Chip,
  Button, Dialog, DialogTitle, DialogContent, DialogActions,
  TextField, Alert, CircularProgress, Tabs, Tab, Badge,
  List, ListItem, ListItemText, ListItemAvatar, Avatar,
  Divider
} from '@mui/material';
import {
  CheckCircle, Cancel, Visibility, People, LocalHospital,
  Email, Phone, CalendarToday
} from '@mui/icons-material';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';

const NutritionistManagement = () => {
  const [nutritionists, setNutritionists] = useState([]);
  const [pendingNutritionists, setPendingNutritionists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [currentTab, setCurrentTab] = useState(0);
  const [selectedNutritionist, setSelectedNutritionist] = useState(null);
  const [openDetailsDialog, setOpenDetailsDialog] = useState(false);
  const [nutritionistPatients, setNutritionistPatients] = useState([]);

  useEffect(() => {
    fetchNutritionists();
    fetchPendingNutritionists();
  }, []);

  const fetchNutritionists = async () => {
    try {
      const token = localStorage.getItem('nutrition_access_token');
      const response = await axios.get(
        `${API_BASE_URL}/api/v1/admin/nutritionists`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setNutritionists(response.data);
      setError('');
    } catch (err) {
      console.error('Error fetching nutritionists:', err);
      setError('Error cargando nutriólogos');
    } finally {
      setLoading(false);
    }
  };

  const fetchPendingNutritionists = async () => {
    try {
      const token = localStorage.getItem('nutrition_access_token');
      const response = await axios.get(
        `${API_BASE_URL}/api/v1/admin/nutritionists/pending`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setPendingNutritionists(response.data);
    } catch (err) {
      console.error('Error fetching pending nutritionists:', err);
    }
  };

  const fetchNutritionistPatients = async (nutritionistId) => {
    try {
      const token = localStorage.getItem('nutrition_access_token');
      const response = await axios.get(
        `${API_BASE_URL}/api/v1/admin/nutritionists/${nutritionistId}/patients`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setNutritionistPatients(response.data);
    } catch (err) {
      console.error('Error fetching nutritionist patients:', err);
      setNutritionistPatients([]);
    }
  };

  const handleApproveNutritionist = async (nutritionistId) => {
    try {
      const token = localStorage.getItem('nutrition_access_token');
      await axios.post(
        `${API_BASE_URL}/api/v1/admin/nutritionists/${nutritionistId}/approve`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSuccess('Nutriólogo aprobado exitosamente');
      fetchNutritionists();
      fetchPendingNutritionists();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Error approving nutritionist:', err);
      setError('Error aprobando nutriólogo');
      setTimeout(() => setError(''), 3000);
    }
  };

  const handleRejectNutritionist = async (nutritionistId) => {
    if (!window.confirm('¿Estás seguro de rechazar este nutriólogo?')) return;

    try {
      const token = localStorage.getItem('nutrition_access_token');
      await axios.post(
        `${API_BASE_URL}/api/v1/admin/nutritionists/${nutritionistId}/reject`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSuccess('Nutriólogo rechazado');
      fetchPendingNutritionists();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Error rejecting nutritionist:', err);
      setError('Error rechazando nutriólogo');
      setTimeout(() => setError(''), 3000);
    }
  };

  const handleViewDetails = async (nutritionist) => {
    setSelectedNutritionist(nutritionist);
    await fetchNutritionistPatients(nutritionist.id);
    setOpenDetailsDialog(true);
  };

  const handleCloseDetails = () => {
    setOpenDetailsDialog(false);
    setSelectedNutritionist(null);
    setNutritionistPatients([]);
  };

  const getStatusChip = (status) => {
    const statusConfig = {
      active: { label: 'Activo', color: 'success' },
      inactive: { label: 'Inactivo', color: 'default' },
      suspended: { label: 'Suspendido', color: 'error' },
      pending_verification: { label: 'Pendiente', color: 'warning' }
    };
    const config = statusConfig[status] || { label: status, color: 'default' };
    return <Chip label={config.label} color={config.color} size="small" />;
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" sx={{ fontWeight: 'bold', mb: 3 }}>
        Gestión de Nutriólogos
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={currentTab}
          onChange={(e, newValue) => setCurrentTab(newValue)}
          indicatorColor="primary"
          textColor="primary"
        >
          <Tab
            label={
              <Badge badgeContent={pendingNutritionists.length} color="warning">
                Pendientes de Aprobación
              </Badge>
            }
          />
          <Tab label="Nutriólogos Activos" />
        </Tabs>
      </Paper>

      {/* Pending Nutritionists */}
      {currentTab === 0 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Nombre</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Teléfono</TableCell>
                <TableCell>Fecha Registro</TableCell>
                <TableCell align="right">Acciones</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {pendingNutritionists.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} align="center">
                    <Typography color="text.secondary" sx={{ py: 4 }}>
                      No hay nutriólogos pendientes de aprobación
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                pendingNutritionists.map((nutritionist) => (
                  <TableRow key={nutritionist.id} hover>
                    <TableCell>
                      {nutritionist.first_name} {nutritionist.last_name}
                    </TableCell>
                    <TableCell>{nutritionist.email}</TableCell>
                    <TableCell>{nutritionist.phone || 'N/A'}</TableCell>
                    <TableCell>
                      {new Date(nutritionist.created_at).toLocaleDateString('es-MX')}
                    </TableCell>
                    <TableCell align="right">
                      <IconButton
                        size="small"
                        onClick={() => handleViewDetails(nutritionist)}
                        color="primary"
                      >
                        <Visibility />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => handleApproveNutritionist(nutritionist.id)}
                        color="success"
                      >
                        <CheckCircle />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => handleRejectNutritionist(nutritionist.id)}
                        color="error"
                      >
                        <Cancel />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Active Nutritionists */}
      {currentTab === 1 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Nombre</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Pacientes Asignados</TableCell>
                <TableCell>Estado</TableCell>
                <TableCell align="right">Acciones</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {nutritionists.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center">
                    <Typography color="text.secondary" sx={{ py: 4 }}>
                      No hay nutriólogos registrados
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                nutritionists.map((nutritionist) => (
                  <TableRow key={nutritionist.id} hover>
                    <TableCell>{nutritionist.id}</TableCell>
                    <TableCell>
                      {nutritionist.first_name} {nutritionist.last_name}
                    </TableCell>
                    <TableCell>{nutritionist.email}</TableCell>
                    <TableCell>
                      <Chip
                        icon={<People />}
                        label={nutritionist.patient_count || 0}
                        size="small"
                        color="primary"
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>{getStatusChip(nutritionist.account_status)}</TableCell>
                    <TableCell align="right">
                      <Button
                        size="small"
                        startIcon={<Visibility />}
                        onClick={() => handleViewDetails(nutritionist)}
                      >
                        Ver Detalles
                      </Button>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Details Dialog */}
      <Dialog
        open={openDetailsDialog}
        onClose={handleCloseDetails}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <LocalHospital color="primary" />
            <Typography variant="h6">
              Detalles del Nutriólogo
            </Typography>
          </Box>
        </DialogTitle>
        <DialogContent>
          {selectedNutritionist && (
            <Box>
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Información Personal
                </Typography>
                <Divider sx={{ my: 1 }} />
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="body2" fontWeight="bold">
                      Nombre Completo:
                    </Typography>
                    <Typography variant="body2">
                      {selectedNutritionist.first_name} {selectedNutritionist.last_name}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Email fontSize="small" color="action" />
                    <Typography variant="body2">
                      {selectedNutritionist.email}
                    </Typography>
                  </Box>
                  {selectedNutritionist.phone && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Phone fontSize="small" color="action" />
                      <Typography variant="body2">
                        {selectedNutritionist.phone}
                      </Typography>
                    </Box>
                  )}
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <CalendarToday fontSize="small" color="action" />
                    <Typography variant="body2">
                      Registrado: {new Date(selectedNutritionist.created_at).toLocaleDateString('es-MX')}
                    </Typography>
                  </Box>
                </Box>
              </Box>

              <Box>
                <Typography variant="subtitle2" color="text.secondary">
                  Pacientes Asignados ({nutritionistPatients.length})
                </Typography>
                <Divider sx={{ my: 1 }} />
                {nutritionistPatients.length === 0 ? (
                  <Typography variant="body2" color="text.secondary" sx={{ py: 2, textAlign: 'center' }}>
                    No tiene pacientes asignados
                  </Typography>
                ) : (
                  <List dense>
                    {nutritionistPatients.map((patient) => (
                      <ListItem key={patient.id}>
                        <ListItemAvatar>
                          <Avatar>{patient.first_name[0]}{patient.last_name[0]}</Avatar>
                        </ListItemAvatar>
                        <ListItemText
                          primary={`${patient.first_name} ${patient.last_name}`}
                          secondary={patient.email}
                        />
                      </ListItem>
                    ))}
                  </List>
                )}
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDetails}>Cerrar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default NutritionistManagement;
