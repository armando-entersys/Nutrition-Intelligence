/**
 * Admin Dashboard - Vista principal de administración
 * Muestra estadísticas y métricas clave del sistema
 */
import React, { useState, useEffect } from 'react';
import {
  Box, Grid, Paper, Typography, Card, CardContent,
  CircularProgress, Alert, Chip, Table, TableBody,
  TableCell, TableContainer, TableHead, TableRow
} from '@mui/material';
import {
  People, PersonAdd, LocalHospital, TrendingUp,
  CheckCircle, Warning, Block, Schedule
} from '@mui/icons-material';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';

const AdminDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalPatients: 0,
    totalNutritionists: 0,
    activeUsers: 0,
    pendingApprovals: 0,
    todayRegistrations: 0
  });
  const [recentUsers, setRecentUsers] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('nutrition_access_token');

      // Fetch statistics
      const statsResponse = await axios.get(
        `${API_BASE_URL}/api/v1/admin/stats`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setStats(statsResponse.data);

      // Fetch recent users
      const usersResponse = await axios.get(
        `${API_BASE_URL}/api/v1/admin/users/recent`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setRecentUsers(usersResponse.data);
      setError('');
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('Error cargando datos del dashboard');
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, icon: Icon, color, subtitle }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box
            sx={{
              bgcolor: `${color}.100`,
              borderRadius: 2,
              p: 1.5,
              mr: 2,
              display: 'flex'
            }}
          >
            <Icon sx={{ color: `${color}.main`, fontSize: 32 }} />
          </Box>
          <Box sx={{ flex: 1 }}>
            <Typography variant="body2" color="text.secondary">
              {title}
            </Typography>
            <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
              {value}
            </Typography>
            {subtitle && (
              <Typography variant="caption" color="text.secondary">
                {subtitle}
              </Typography>
            )}
          </Box>
        </Box>
      </CardContent>
    </Card>
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
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 400 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 'bold' }}>
        Panel de Administración
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Statistics Grid */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Total Usuarios"
            value={stats.totalUsers}
            icon={People}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Pacientes"
            value={stats.totalPatients}
            icon={PersonAdd}
            color="info"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Nutriólogos"
            value={stats.totalNutritionists}
            icon={LocalHospital}
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Usuarios Activos"
            value={stats.activeUsers}
            icon={CheckCircle}
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Pendientes de Aprobación"
            value={stats.pendingApprovals}
            icon={Schedule}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Registros Hoy"
            value={stats.todayRegistrations}
            icon={TrendingUp}
            color="info"
          />
        </Grid>
      </Grid>

      {/* Recent Users Table */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
          Usuarios Recientes
        </Typography>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Nombre</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Rol</TableCell>
                <TableCell>Estado</TableCell>
                <TableCell>Fecha Registro</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {recentUsers.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} align="center">
                    <Typography color="text.secondary">
                      No hay usuarios recientes
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                recentUsers.map((user) => (
                  <TableRow key={user.id} hover>
                    <TableCell>
                      {user.first_name} {user.last_name}
                    </TableCell>
                    <TableCell>{user.email}</TableCell>
                    <TableCell>
                      <Chip
                        label={user.primary_role}
                        size="small"
                        color={user.primary_role === 'nutritionist' ? 'success' : 'primary'}
                      />
                    </TableCell>
                    <TableCell>{getStatusChip(user.account_status)}</TableCell>
                    <TableCell>
                      {new Date(user.created_at).toLocaleDateString('es-MX')}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
};

export default AdminDashboard;
