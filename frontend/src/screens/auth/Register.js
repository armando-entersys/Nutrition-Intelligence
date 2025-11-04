/**
 * Register Screen - User registration
 */
import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Container, Paper, TextField, Button, Typography, Box, Alert,
  InputAdornment, IconButton, CircularProgress, MenuItem,
  FormControl, InputLabel, Select, LinearProgress, Collapse
} from '@mui/material';
import {
  Visibility, VisibilityOff, PersonAdd, Email, Lock, Person, Phone,
  CheckCircle, Error as ErrorIcon, LocalHospital
} from '@mui/icons-material';
import axios from 'axios';
import authService from '../../services/authService';
import { API_ENDPOINTS } from '../../config/api';

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '', username: '', password: '', confirm_password: '',
    first_name: '', last_name: '', phone: '', role: 'patient',
    nutritionist_email: ''
  });
  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [generalError, setGeneralError] = useState('');
  const [passwordStrength, setPasswordStrength] = useState(null);
  const [nutritionistValidation, setNutritionistValidation] = useState({
    validating: false,
    valid: null,
    message: '',
    nutritionist: null
  });

  // Validate nutritionist email
  const validateNutritionistEmail = useCallback(async (email) => {
    if (!email || !authService.validateEmail(email)) {
      setNutritionistValidation({
        validating: false,
        valid: false,
        message: 'Por favor ingresa un email válido',
        nutritionist: null
      });
      return;
    }

    setNutritionistValidation(prev => ({ ...prev, validating: true }));

    try {
      const response = await axios.get(
        `${API_ENDPOINTS.AUTH}/validate-nutritionist/${encodeURIComponent(email)}`
      );

      setNutritionistValidation({
        validating: false,
        valid: true,
        message: response.data.message,
        nutritionist: response.data.nutritionist
      });
    } catch (error) {
      setNutritionistValidation({
        validating: false,
        valid: false,
        message: error.response?.data?.detail || 'Error al validar el email del nutriólogo',
        nutritionist: null
      });
    }
  }, []);

  // Debounce nutritionist email validation
  useEffect(() => {
    if (formData.role === 'patient' && formData.nutritionist_email) {
      const timer = setTimeout(() => {
        validateNutritionistEmail(formData.nutritionist_email);
      }, 500); // Wait 500ms after user stops typing

      return () => clearTimeout(timer);
    } else {
      setNutritionistValidation({
        validating: false,
        valid: null,
        message: '',
        nutritionist: null
      });
    }
  }, [formData.nutritionist_email, formData.role, validateNutritionistEmail]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors(prev => ({ ...prev, [name]: '' }));
    setGeneralError('');

    if (name === 'password') {
      setPasswordStrength(authService.getPasswordStrength(value));
    }

    // Clear nutritionist email if role changes to non-patient
    if (name === 'role' && value !== 'patient') {
      setFormData(prev => ({ ...prev, nutritionist_email: '' }));
      setNutritionistValidation({
        validating: false,
        valid: null,
        message: '',
        nutritionist: null
      });
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.email) newErrors.email = 'Email is required';
    else if (!authService.validateEmail(formData.email)) newErrors.email = 'Invalid email';
    if (!formData.username || formData.username.length < 3) newErrors.username = 'Username must be at least 3 characters';
    if (!formData.first_name) newErrors.first_name = 'First name is required';
    if (!formData.last_name) newErrors.last_name = 'Last name is required';

    // Validate nutritionist email for patients
    if (formData.role === 'patient') {
      if (!formData.nutritionist_email) {
        newErrors.nutritionist_email = 'Nutritionist email is required for patients';
      } else if (!nutritionistValidation.valid) {
        newErrors.nutritionist_email = 'Please enter a valid nutritionist email';
      }
    }

    const passwordValidation = authService.validatePassword(formData.password);
    if (!passwordValidation.isValid) newErrors.password = passwordValidation.errors.join('. ');

    if (formData.password !== formData.confirm_password) {
      newErrors.confirm_password = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);
    try {
      await authService.register(formData);
      navigate('/auth/login', {
        state: { message: 'Registration successful! Please login.' }
      });
    } catch (error) {
      setGeneralError(error.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Box sx={{ width: 60, height: 60, borderRadius: '50%', bgcolor: 'primary.main',
            display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 2 }}>
            <PersonAdd sx={{ fontSize: 30, color: 'white' }} />
          </Box>
          <Typography variant="h5" gutterBottom>Create Account</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3, textAlign: 'center' }}>
            Join Nutrition Intelligence today
          </Typography>

          {generalError && <Alert severity="error" sx={{ width: '100%', mb: 2 }}>{generalError}</Alert>}

          <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
            <TextField margin="dense" required fullWidth label="Email" name="email" type="email"
              value={formData.email} onChange={handleChange} error={!!errors.email}
              helperText={errors.email} disabled={loading}
              InputProps={{ startAdornment: <InputAdornment position="start"><Email /></InputAdornment> }}
            />
            <TextField margin="dense" required fullWidth label="Username" name="username"
              value={formData.username} onChange={handleChange} error={!!errors.username}
              helperText={errors.username} disabled={loading}
              InputProps={{ startAdornment: <InputAdornment position="start"><Person /></InputAdornment> }}
            />
            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField margin="dense" required fullWidth label="First Name" name="first_name"
                value={formData.first_name} onChange={handleChange} error={!!errors.first_name}
                helperText={errors.first_name} disabled={loading}
              />
              <TextField margin="dense" required fullWidth label="Last Name" name="last_name"
                value={formData.last_name} onChange={handleChange} error={!!errors.last_name}
                helperText={errors.last_name} disabled={loading}
              />
            </Box>
            <TextField margin="dense" fullWidth label="Phone (optional)" name="phone"
              value={formData.phone} onChange={handleChange} disabled={loading}
              InputProps={{ startAdornment: <InputAdornment position="start"><Phone /></InputAdornment> }}
            />
            <FormControl fullWidth margin="dense">
              <InputLabel>I am a</InputLabel>
              <Select name="role" value={formData.role} onChange={handleChange} disabled={loading}>
                <MenuItem value="patient">Patient</MenuItem>
                <MenuItem value="nutritionist">Nutritionist</MenuItem>
              </Select>
            </FormControl>

            {/* Nutritionist Email Field - Only for Patients */}
            <Collapse in={formData.role === 'patient'}>
              <TextField
                margin="dense"
                required={formData.role === 'patient'}
                fullWidth
                label="Nutritionist Email"
                name="nutritionist_email"
                type="email"
                value={formData.nutritionist_email}
                onChange={handleChange}
                error={!!errors.nutritionist_email || (nutritionistValidation.valid === false && formData.nutritionist_email)}
                helperText={
                  errors.nutritionist_email ||
                  (formData.nutritionist_email && nutritionistValidation.message) ||
                  'Enter your nutritionist\'s email address'
                }
                disabled={loading}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <LocalHospital />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      {nutritionistValidation.validating && <CircularProgress size={20} />}
                      {nutritionistValidation.valid === true && (
                        <CheckCircle sx={{ color: 'success.main' }} />
                      )}
                      {nutritionistValidation.valid === false && formData.nutritionist_email && (
                        <ErrorIcon sx={{ color: 'error.main' }} />
                      )}
                    </InputAdornment>
                  ),
                }}
              />
              {nutritionistValidation.valid && nutritionistValidation.nutritionist && (
                <Alert severity="success" sx={{ mt: 1, mb: 1 }}>
                  <Typography variant="body2">
                    <strong>Nutritionist Found:</strong> {nutritionistValidation.nutritionist.name}
                  </Typography>
                </Alert>
              )}
            </Collapse>

            <TextField margin="dense" required fullWidth label="Password" name="password"
              type={showPassword ? 'text' : 'password'} value={formData.password}
              onChange={handleChange} error={!!errors.password} helperText={errors.password}
              disabled={loading}
              InputProps={{
                startAdornment: <InputAdornment position="start"><Lock /></InputAdornment>,
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                )
              }}
            />
            {passwordStrength && formData.password && (
              <Box sx={{ mt: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                  <Typography variant="caption">{passwordStrength.text}</Typography>
                  <Typography variant="caption">{passwordStrength.percent}%</Typography>
                </Box>
                <LinearProgress variant="determinate" value={passwordStrength.percent}
                  sx={{ height: 6, borderRadius: 3, backgroundColor: '#e0e0e0',
                    '& .MuiLinearProgress-bar': { backgroundColor: passwordStrength.color }
                  }}
                />
              </Box>
            )}
            <TextField margin="dense" required fullWidth label="Confirm Password"
              name="confirm_password" type={showPassword ? 'text' : 'password'}
              value={formData.confirm_password} onChange={handleChange}
              error={!!errors.confirm_password} helperText={errors.confirm_password}
              disabled={loading}
            />
            <Button type="submit" fullWidth variant="contained" disabled={loading}
              sx={{ mt: 3, mb: 2, py: 1.5 }}>
              {loading ? <CircularProgress size={24} /> : 'Sign Up'}
            </Button>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">
                Already have an account?{' '}
                <Link to="/auth/login" style={{ textDecoration: 'none', fontWeight: 'bold' }}>
                  <Typography component="span" color="primary">Sign In</Typography>
                </Link>
              </Typography>
            </Box>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default Register;
