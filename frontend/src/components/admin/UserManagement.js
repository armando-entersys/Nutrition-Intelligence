/**
 * User Management - Gestión completa de usuarios
 * CRUD de usuarios, cambio de estado, asignación de roles
 */
import React, { useState, useEffect } from 'react';
import {
  Box, Paper, Typography, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, IconButton, Chip,
  Button, Dialog, DialogTitle, DialogContent, DialogActions,
  TextField, MenuItem, Alert, CircularProgress, Tooltip,
  TablePagination, InputAdornment
} from '@mui/material';
import {
  Edit, Delete, Block, CheckCircle, Search,
  PersonAdd, Visibility
} from '@mui/icons-material';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  // Dialog states
  const [openDialog, setOpenDialog] = useState(false);
  const [dialogMode, setDialogMode] = useState('create'); // 'create', 'edit', 'view'
  const [selectedUser, setSelectedUser] = useState(null);
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    first_name: '',
    last_name: '',
    phone: '',
    primary_role: 'patient',
    account_status: 'active',
    password: ''
  });

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('nutrition_access_token');
      const response = await axios.get(
        `${API_BASE_URL}/api/v1/admin/users`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setUsers(response.data);
      setError('');
    } catch (err) {
      console.error('Error fetching users:', err);
      setError('Error cargando usuarios');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (mode, user = null) => {
    setDialogMode(mode);
    setSelectedUser(user);

    if (mode === 'edit' && user) {
      setFormData({
        email: user.email,
        username: user.username,
        first_name: user.first_name,
        last_name: user.last_name,
        phone: user.phone || '',
        primary_role: user.primary_role,
        account_status: user.account_status,
        password: ''
      });
    } else if (mode === 'create') {
      setFormData({
        email: '',
        username: '',
        first_name: '',
        last_name: '',
        phone: '',
        primary_role: 'patient',
        account_status: 'active',
        password: ''
      });
    }

    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedUser(null);
    setFormData({
      email: '',
      username: '',
      first_name: '',
      last_name: '',
      phone: '',
      primary_role: 'patient',
      account_status: 'active',
      password: ''
    });
  };

  const handleSaveUser = async () => {
    try {
      const token = localStorage.getItem('nutrition_access_token');

      if (dialogMode === 'create') {
        await axios.post(
          `${API_BASE_URL}/api/v1/admin/users`,
          formData,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setSuccess('Usuario creado exitosamente');
      } else if (dialogMode === 'edit') {
        await axios.put(
          `${API_BASE_URL}/api/v1/admin/users/${selectedUser.id}`,
          formData,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setSuccess('Usuario actualizado exitosamente');
      }

      handleCloseDialog();
      fetchUsers();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Error saving user:', err);
      setError(err.response?.data?.detail || 'Error guardando usuario');
      setTimeout(() => setError(''), 3000);
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm('¿Estás seguro de eliminar este usuario?')) return;

    try {
      const token = localStorage.getItem('nutrition_access_token');
      await axios.delete(
        `${API_BASE_URL}/api/v1/admin/users/${userId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSuccess('Usuario eliminado exitosamente');
      fetchUsers();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Error deleting user:', err);
      setError('Error eliminando usuario');
      setTimeout(() => setError(''), 3000);
    }
  };

  const handleToggleStatus = async (user) => {
    const newStatus = user.account_status === 'active' ? 'suspended' : 'active';

    try {
      const token = localStorage.getItem('nutrition_access_token');
      await axios.patch(
        `${API_BASE_URL}/api/v1/admin/users/${user.id}/status`,
        { account_status: newStatus },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSuccess(`Usuario ${newStatus === 'active' ? 'activado' : 'suspendido'} exitosamente`);
      fetchUsers();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Error toggling status:', err);
      setError('Error cambiando estado del usuario');
      setTimeout(() => setError(''), 3000);
    }
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

  const getRoleChip = (role) => {
    const roleConfig = {
      admin: { label: 'Admin', color: 'error' },
      nutritionist: { label: 'Nutriólogo', color: 'success' },
      patient: { label: 'Paciente', color: 'primary' }
    };
    const config = roleConfig[role] || { label: role, color: 'default' };
    return <Chip label={config.label} color={config.color} size="small" />;
  };

  const filteredUsers = users.filter(user =>
    user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    `${user.first_name} ${user.last_name}`.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
          Gestión de Usuarios
        </Typography>
        <Button
          variant="contained"
          startIcon={<PersonAdd />}
          onClick={() => handleOpenDialog('create')}
        >
          Nuevo Usuario
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

      <Paper sx={{ p: 2, mb: 2 }}>
        <TextField
          fullWidth
          placeholder="Buscar por nombre, email o usuario..."
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
              <TableCell>Usuario</TableCell>
              <TableCell>Rol</TableCell>
              <TableCell>Estado</TableCell>
              <TableCell align="right">Acciones</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredUsers
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((user) => (
                <TableRow key={user.id} hover>
                  <TableCell>{user.id}</TableCell>
                  <TableCell>
                    {user.first_name} {user.last_name}
                  </TableCell>
                  <TableCell>{user.email}</TableCell>
                  <TableCell>{user.username}</TableCell>
                  <TableCell>{getRoleChip(user.primary_role)}</TableCell>
                  <TableCell>{getStatusChip(user.account_status)}</TableCell>
                  <TableCell align="right">
                    <Tooltip title="Ver detalles">
                      <IconButton
                        size="small"
                        onClick={() => handleOpenDialog('view', user)}
                      >
                        <Visibility />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Editar">
                      <IconButton
                        size="small"
                        onClick={() => handleOpenDialog('edit', user)}
                      >
                        <Edit />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title={user.account_status === 'active' ? 'Suspender' : 'Activar'}>
                      <IconButton
                        size="small"
                        onClick={() => handleToggleStatus(user)}
                        color={user.account_status === 'active' ? 'error' : 'success'}
                      >
                        {user.account_status === 'active' ? <Block /> : <CheckCircle />}
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Eliminar">
                      <IconButton
                        size="small"
                        onClick={() => handleDeleteUser(user.id)}
                        color="error"
                      >
                        <Delete />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
        <TablePagination
          component="div"
          count={filteredUsers.length}
          page={page}
          onPageChange={(e, newPage) => setPage(newPage)}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={(e) => {
            setRowsPerPage(parseInt(e.target.value, 10));
            setPage(0);
          }}
          labelRowsPerPage="Filas por página:"
        />
      </TableContainer>

      {/* Create/Edit Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {dialogMode === 'create' && 'Crear Nuevo Usuario'}
          {dialogMode === 'edit' && 'Editar Usuario'}
          {dialogMode === 'view' && 'Detalles del Usuario'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              fullWidth
              disabled={dialogMode === 'view'}
              required
            />
            <TextField
              label="Usuario"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              fullWidth
              disabled={dialogMode === 'view'}
              required
            />
            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField
                label="Nombre"
                value={formData.first_name}
                onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                fullWidth
                disabled={dialogMode === 'view'}
                required
              />
              <TextField
                label="Apellido"
                value={formData.last_name}
                onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                fullWidth
                disabled={dialogMode === 'view'}
                required
              />
            </Box>
            <TextField
              label="Teléfono"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              fullWidth
              disabled={dialogMode === 'view'}
            />
            <TextField
              select
              label="Rol"
              value={formData.primary_role}
              onChange={(e) => setFormData({ ...formData, primary_role: e.target.value })}
              fullWidth
              disabled={dialogMode === 'view'}
            >
              <MenuItem value="patient">Paciente</MenuItem>
              <MenuItem value="nutritionist">Nutriólogo</MenuItem>
              <MenuItem value="admin">Administrador</MenuItem>
            </TextField>
            <TextField
              select
              label="Estado"
              value={formData.account_status}
              onChange={(e) => setFormData({ ...formData, account_status: e.target.value })}
              fullWidth
              disabled={dialogMode === 'view'}
            >
              <MenuItem value="active">Activo</MenuItem>
              <MenuItem value="inactive">Inactivo</MenuItem>
              <MenuItem value="suspended">Suspendido</MenuItem>
              <MenuItem value="pending_verification">Pendiente Verificación</MenuItem>
            </TextField>
            {dialogMode !== 'view' && (
              <TextField
                label={dialogMode === 'create' ? 'Contraseña' : 'Nueva Contraseña (opcional)'}
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                fullWidth
                required={dialogMode === 'create'}
                helperText={dialogMode === 'edit' ? 'Dejar en blanco para no cambiar' : ''}
              />
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>
            {dialogMode === 'view' ? 'Cerrar' : 'Cancelar'}
          </Button>
          {dialogMode !== 'view' && (
            <Button onClick={handleSaveUser} variant="contained">
              {dialogMode === 'create' ? 'Crear' : 'Guardar'}
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default UserManagement;
