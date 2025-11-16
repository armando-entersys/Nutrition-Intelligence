/**
 * Patient Management - Gestión de Pacientes
 * Ver lista de pacientes, reasignar nutriólogos
 */
import React, { useState, useEffect } from 'react';
import {
  Box, Paper, Typography, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Chip, Button,
  Dialog, DialogTitle, DialogContent, DialogActions,
  TextField, MenuItem, Alert, CircularProgress,
  InputAdornment, IconButton, Tooltip
} from '@mui/material';
import {
  Search, Visibility, SwapHoriz, PersonAdd
} from '@mui/icons-material';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';

const PatientManagement = () => {
  const [patients, setPatients] = useState([]);
  const [nutritionists, setNutritionists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [openAssignDialog, setOpenAssignDialog] = useState(false);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [selectedNutritionist, setSelectedNutritionist] = useState('');

  useEffect(() => {
    fetchPatients();
    fetchNutritionists();
  }, []);

  const fetchPatients = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('nutrition_access_token');
      const response = await axios.get(
        `${API_BASE_URL}/api/v1/admin/patients`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setPatients(response.data);
      setError('');
    } catch (err) {
      console.error('Error fetching patients:', err);
      setError('Error cargando pacientes');
    } finally {
      setLoading(false);
    }
  };

  const fetchNutritionists = async () => {
    try {
      const token = localStorage.getItem('nutrition_access_token');
      const response = await axios.get(
        `${API_BASE_URL}/api/v1/admin/nutritionists`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setNutritionists(response.data.filter(n => n.account_status === 'active'));
    } catch (err) {
      console.error('Error fetching nutritionists:', err);
    }
  };

  const handleOpenAssignDialog = (patient) => {
    setSelectedPatient(patient);
    setSelectedNutritionist(patient.nutritionist_id || '');
    setOpenAssignDialog(true);
  };

  const handleCloseAssignDialog = () => {
    setOpenAssignDialog(false);
    setSelectedPatient(null);
    setSelectedNutritionist('');
  };

  const handleAssignNutritionist = async () => {
    if (!selectedNutritionist) {
      setError('Por favor selecciona un nutriólogo');
      return;
    }

    try {
      const token = localStorage.getItem('nutrition_access_token');
      await axios.patch(
        `${API_BASE_URL}/api/v1/admin/patients/${selectedPatient.id}/assign-nutritionist`,
        { nutritionist_id: selectedNutritionist },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSuccess('Nutriólogo asignado exitosamente');
      handleCloseAssignDialog();
      fetchPatients();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Error assigning nutritionist:', err);
      setError('Error asignando nutriólogo');
      setTimeout(() => setError(''), 3000);
    }
  };

  const filteredPatients = patients.filter(patient =>
    patient.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    patient.username?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    `${patient.first_name} ${patient.last_name}`.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
        Gestión de Pacientes
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

      <Paper sx={{ p: 2, mb: 2 }}>
        <TextField
          fullWidth
          placeholder="Buscar paciente por nombre, email o usuario..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          }}
        />
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Nombre</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Nutriólogo Asignado</TableCell>
              <TableCell>Estado</TableCell>
              <TableCell>Fecha Registro</TableCell>
              <TableCell align="right">Acciones</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredPatients.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} align="center">
                  <Typography color="text.secondary" sx={{ py: 4 }}>
                    {searchTerm ? 'No se encontraron pacientes' : 'No hay pacientes registrados'}
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              filteredPatients.map((patient) => (
                <TableRow key={patient.id} hover>
                  <TableCell>{patient.id}</TableCell>
                  <TableCell>
                    {patient.first_name} {patient.last_name}
                  </TableCell>
                  <TableCell>{patient.email}</TableCell>
                  <TableCell>
                    {patient.nutritionist ? (
                      <Tooltip title={patient.nutritionist.email}>
                        <Chip
                          label={`${patient.nutritionist.first_name} ${patient.nutritionist.last_name}`}
                          size="small"
                          color="success"
                          variant="outlined"
                        />
                      </Tooltip>
                    ) : (
                      <Chip
                        label="Sin asignar"
                        size="small"
                        color="warning"
                        variant="outlined"
                      />
                    )}
                  </TableCell>
                  <TableCell>{getStatusChip(patient.account_status)}</TableCell>
                  <TableCell>
                    {new Date(patient.created_at).toLocaleDateString('es-MX')}
                  </TableCell>
                  <TableCell align="right">
                    <Tooltip title="Asignar/Cambiar Nutriólogo">
                      <IconButton
                        size="small"
                        onClick={() => handleOpenAssignDialog(patient)}
                        color="primary"
                      >
                        {patient.nutritionist ? <SwapHoriz /> : <PersonAdd />}
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Assign Nutritionist Dialog */}
      <Dialog open={openAssignDialog} onClose={handleCloseAssignDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {selectedPatient?.nutritionist ? 'Reasignar Nutriólogo' : 'Asignar Nutriólogo'}
        </DialogTitle>
        <DialogContent>
          {selectedPatient && (
            <Box sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Box>
                <Typography variant="subtitle2" color="text.secondary">
                  Paciente
                </Typography>
                <Typography variant="body1" fontWeight="bold">
                  {selectedPatient.first_name} {selectedPatient.last_name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {selectedPatient.email}
                </Typography>
              </Box>

              {selectedPatient.nutritionist && (
                <Box>
                  <Typography variant="subtitle2" color="text.secondary">
                    Nutriólogo Actual
                  </Typography>
                  <Typography variant="body2">
                    {selectedPatient.nutritionist.first_name} {selectedPatient.nutritionist.last_name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {selectedPatient.nutritionist.email}
                  </Typography>
                </Box>
              )}

              <TextField
                select
                label="Nuevo Nutriólogo"
                value={selectedNutritionist}
                onChange={(e) => setSelectedNutritionist(e.target.value)}
                fullWidth
                required
              >
                <MenuItem value="">
                  <em>Selecciona un nutriólogo</em>
                </MenuItem>
                {nutritionists.map((nutritionist) => (
                  <MenuItem key={nutritionist.id} value={nutritionist.id}>
                    {nutritionist.first_name} {nutritionist.last_name} - {nutritionist.email}
                  </MenuItem>
                ))}
              </TextField>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseAssignDialog}>
            Cancelar
          </Button>
          <Button onClick={handleAssignNutritionist} variant="contained">
            Asignar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PatientManagement;
