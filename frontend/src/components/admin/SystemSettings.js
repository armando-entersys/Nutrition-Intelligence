/**
 * System Settings - Configuración del Sistema
 * Ajustes generales, parámetros del sistema
 */
import React, { useState, useEffect } from 'react';
import {
  Box, Paper, Typography, TextField, Button, Alert,
  Grid, Switch, FormControlLabel, Divider, Card,
  CardContent, CircularProgress
} from '@mui/material';
import {
  Save, Refresh
} from '@mui/icons-material';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';

const SystemSettings = () => {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [settings, setSettings] = useState({
    systemName: 'Nutrition Intelligence',
    systemEmail: 'admin@nutrition-intelligence.com',
    allowRegistrations: true,
    requireEmailVerification: false,
    requireNutritionistApproval: true,
    maxPatientsPerNutritionist: 50,
    sessionTimeout: 30,
    passwordMinLength: 8,
    passwordRequireUppercase: true,
    passwordRequireLowercase: true,
    passwordRequireNumber: true,
    passwordRequireSpecial: false
  });

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('nutrition_access_token');
      const response = await axios.get(
        `${API_BASE_URL}/api/v1/admin/settings`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSettings(response.data);
      setError('');
    } catch (err) {
      console.error('Error fetching settings:', err);
      setError('Error cargando configuración');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSettings = async () => {
    try {
      setSaving(true);
      const token = localStorage.getItem('nutrition_access_token');
      await axios.put(
        `${API_BASE_URL}/api/v1/admin/settings`,
        settings,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSuccess('Configuración guardada exitosamente');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Error saving settings:', err);
      setError('Error guardando configuración');
      setTimeout(() => setError(''), 3000);
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (field, value) => {
    setSettings(prev => ({
      ...prev,
      [field]: value
    }));
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
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
          Configuración del Sistema
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={fetchSettings}
          >
            Recargar
          </Button>
          <Button
            variant="contained"
            startIcon={<Save />}
            onClick={handleSaveSettings}
            disabled={saving}
          >
            {saving ? 'Guardando...' : 'Guardar Cambios'}
          </Button>
        </Box>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

      <Grid container spacing={3}>
        {/* General Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Configuración General
              </Typography>
              <Divider sx={{ mb: 2 }} />

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <TextField
                  label="Nombre del Sistema"
                  value={settings.systemName}
                  onChange={(e) => handleChange('systemName', e.target.value)}
                  fullWidth
                />
                <TextField
                  label="Email del Sistema"
                  type="email"
                  value={settings.systemEmail}
                  onChange={(e) => handleChange('systemEmail', e.target.value)}
                  fullWidth
                />
                <TextField
                  label="Tiempo de Sesión (minutos)"
                  type="number"
                  value={settings.sessionTimeout}
                  onChange={(e) => handleChange('sessionTimeout', parseInt(e.target.value))}
                  fullWidth
                  helperText="Tiempo de inactividad antes de cerrar sesión automáticamente"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* User Registration Settings */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Registro de Usuarios
              </Typography>
              <Divider sx={{ mb: 2 }} />

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.allowRegistrations}
                      onChange={(e) => handleChange('allowRegistrations', e.target.checked)}
                    />
                  }
                  label="Permitir nuevos registros"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.requireEmailVerification}
                      onChange={(e) => handleChange('requireEmailVerification', e.target.checked)}
                    />
                  }
                  label="Requerir verificación de email"
                />
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.requireNutritionistApproval}
                      onChange={(e) => handleChange('requireNutritionistApproval', e.target.checked)}
                    />
                  }
                  label="Requerir aprobación de nutriólogos"
                />
                <TextField
                  label="Máximo de pacientes por nutriólogo"
                  type="number"
                  value={settings.maxPatientsPerNutritionist}
                  onChange={(e) => handleChange('maxPatientsPerNutritionist', parseInt(e.target.value))}
                  fullWidth
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Password Policy */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Política de Contraseñas
              </Typography>
              <Divider sx={{ mb: 2 }} />

              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <TextField
                    label="Longitud Mínima"
                    type="number"
                    value={settings.passwordMinLength}
                    onChange={(e) => handleChange('passwordMinLength', parseInt(e.target.value))}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={settings.passwordRequireUppercase}
                        onChange={(e) => handleChange('passwordRequireUppercase', e.target.checked)}
                      />
                    }
                    label="Requerir mayúsculas"
                  />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={settings.passwordRequireLowercase}
                        onChange={(e) => handleChange('passwordRequireLowercase', e.target.checked)}
                      />
                    }
                    label="Requerir minúsculas"
                  />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={settings.passwordRequireNumber}
                        onChange={(e) => handleChange('passwordRequireNumber', e.target.checked)}
                      />
                    }
                    label="Requerir números"
                  />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={settings.passwordRequireSpecial}
                        onChange={(e) => handleChange('passwordRequireSpecial', e.target.checked)}
                      />
                    }
                    label="Requerir caracteres especiales"
                  />
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* System Information */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Información del Sistema
              </Typography>
              <Divider sx={{ mb: 2 }} />

              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="caption" color="text.secondary">
                    Versión
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    1.0.0
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="caption" color="text.secondary">
                    Entorno
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    Producción
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="caption" color="text.secondary">
                    Última Actualización
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {new Date().toLocaleDateString('es-MX')}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Typography variant="caption" color="text.secondary">
                    Base de Datos
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    PostgreSQL
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SystemSettings;
