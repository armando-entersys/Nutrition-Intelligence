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
    <Box sx={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      py: 6,
      px: 2
    }}>
      <Container maxWidth="md">
        <Paper
          elevation={24}
          sx={{
            p: { xs: 4, md: 6 },
            borderRadius: 4,
            background: 'linear-gradient(to bottom, #ffffff 0%, #f8f9ff 100%)',
            position: 'relative',
            overflow: 'hidden',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              height: '6px',
              background: 'linear-gradient(90deg, #667eea 0%, #764ba2 50%, #F093FB 100%)',
            }
          }}
        >
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Box sx={{
              width: 90,
              height: 90,
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mb: 3,
              boxShadow: '0 8px 32px rgba(102, 126, 234, 0.4)',
              border: '4px solid white'
            }}>
              <PersonAdd sx={{ fontSize: 48, color: 'white' }} />
            </Box>
            <Typography
              variant="h3"
              gutterBottom
              fontWeight="800"
              sx={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                mb: 1
              }}
            >
              Create Account
            </Typography>
            <Typography
              variant="h6"
              color="text.secondary"
              sx={{
                mb: 5,
                textAlign: 'center',
                fontWeight: 400,
                maxWidth: '500px'
              }}
            >
              Join Nutrition Intelligence and start your health journey today ✨
            </Typography>

            {generalError && <Alert severity="error" sx={{ width: '100%', mb: 3 }}>{generalError}</Alert>}

            <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
              {/* Account Information Section */}
              <Box sx={{ mb: 4 }}>
                <Typography variant="h6" gutterBottom sx={{
                  mb: 2,
                  fontWeight: '700',
                  color: '#667eea',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1
                }}>
                  📧 Account Information
                </Typography>
                <Paper
                  variant="outlined"
                  sx={{
                    p: 3,
                    background: 'linear-gradient(135deg, #f5f7ff 0%, #ffffff 100%)',
                    border: '2px solid #e6eaf7',
                    borderRadius: 3,
                    boxShadow: '0 4px 20px rgba(102, 126, 234, 0.08)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      boxShadow: '0 6px 30px rgba(102, 126, 234, 0.15)',
                      transform: 'translateY(-2px)'
                    }
                  }}>
                  <TextField
                    margin="normal"
                    required
                    fullWidth
                    label="Email Address"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    error={!!errors.email}
                    helperText={errors.email || 'We\'ll never share your email'}
                    disabled={loading}
                    size="medium"
                    InputProps={{ startAdornment: <InputAdornment position="start"><Email /></InputAdornment> }}
                  />
                  <TextField
                    margin="normal"
                    required
                    fullWidth
                    label="Username"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    error={!!errors.username}
                    helperText={errors.username || 'Choose a unique username'}
                    disabled={loading}
                    size="medium"
                    InputProps={{ startAdornment: <InputAdornment position="start"><Person /></InputAdornment> }}
                  />
                </Paper>
              </Box>

              {/* Personal Information Section */}
              <Box sx={{ mb: 4 }}>
                <Typography variant="h6" gutterBottom sx={{
                  mb: 2,
                  fontWeight: '700',
                  color: '#764ba2',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1
                }}>
                  👤 Personal Information
                </Typography>
                <Paper
                  variant="outlined"
                  sx={{
                    p: 3,
                    background: 'linear-gradient(135deg, #fff5fb 0%, #ffffff 100%)',
                    border: '2px solid #f3e6f0',
                    borderRadius: 3,
                    boxShadow: '0 4px 20px rgba(118, 75, 162, 0.08)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      boxShadow: '0 6px 30px rgba(118, 75, 162, 0.15)',
                      transform: 'translateY(-2px)'
                    }
                  }}>
                  <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
                    <TextField
                      margin="normal"
                      required
                      fullWidth
                      label="First Name"
                      name="first_name"
                      value={formData.first_name}
                      onChange={handleChange}
                      error={!!errors.first_name}
                      helperText={errors.first_name}
                      disabled={loading}
                      size="medium"
                    />
                    <TextField
                      margin="normal"
                      required
                      fullWidth
                      label="Last Name"
                      name="last_name"
                      value={formData.last_name}
                      onChange={handleChange}
                      error={!!errors.last_name}
                      helperText={errors.last_name}
                      disabled={loading}
                      size="medium"
                    />
                  </Box>
                  <TextField
                    margin="normal"
                    fullWidth
                    label="Phone Number"
                    name="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    disabled={loading}
                    size="medium"
                    helperText="Optional - for notifications"
                    InputProps={{ startAdornment: <InputAdornment position="start"><Phone /></InputAdornment> }}
                  />
                </Paper>
              </Box>

              {/* Role Selection Section */}
              <Box sx={{ mb: 4 }}>
                <Typography variant="h6" gutterBottom sx={{
                  mb: 2,
                  fontWeight: '700',
                  color: '#F093FB',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1
                }}>
                  🎯 Account Type
                </Typography>
                <Paper
                  variant="outlined"
                  sx={{
                    p: 3,
                    background: 'linear-gradient(135deg, #fff7fd 0%, #ffffff 100%)',
                    border: '2px solid #fee6f9',
                    borderRadius: 3,
                    boxShadow: '0 4px 20px rgba(240, 147, 251, 0.08)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      boxShadow: '0 6px 30px rgba(240, 147, 251, 0.15)',
                      transform: 'translateY(-2px)'
                    }
                  }}>
                  <FormControl fullWidth margin="normal" size="medium">
                    <InputLabel id="role-label">Me registro como</InputLabel>
                    <Select
                      labelId="role-label"
                      name="role"
                      value={formData.role}
                      onChange={handleChange}
                      disabled={loading}
                      label="Me registro como"
                    >
                      <MenuItem value="patient">
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Person sx={{ color: '#667eea' }} />
                          <Box>
                            <Typography variant="body1" fontWeight="600">Paciente</Typography>
                            <Typography variant="caption" color="text.secondary">Busco guía nutricional</Typography>
                          </Box>
                        </Box>
                      </MenuItem>
                      <MenuItem value="nutritionist">
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <LocalHospital sx={{ color: '#4caf50' }} />
                          <Box>
                            <Typography variant="body1" fontWeight="600">Nutriólogo</Typography>
                            <Typography variant="caption" color="text.secondary">Cuenta profesional</Typography>
                          </Box>
                        </Box>
                      </MenuItem>
                    </Select>
                  </FormControl>

                  {/* Nutritionist Email Field - Only for Patients */}
                  <Collapse in={formData.role === 'patient'}>
                    <Box sx={{
                      mt: 2,
                      p: 3,
                      background: 'linear-gradient(135deg, #e3f2fd 0%, #f5f9ff 100%)',
                      borderRadius: 2,
                      border: '2px solid #bbdefb',
                      boxShadow: '0 2px 10px rgba(25, 118, 210, 0.1)'
                    }}>
                      <Typography variant="body2" sx={{ mb: 2, color: '#1976d2', fontWeight: 600 }}>
                        💡 As a patient, you need to be assigned to a nutritionist
                      </Typography>
                      <TextField
                        margin="normal"
                        required={formData.role === 'patient'}
                        fullWidth
                        label="Your Nutritionist's Email"
                        name="nutritionist_email"
                        type="email"
                        value={formData.nutritionist_email}
                        onChange={handleChange}
                        error={!!errors.nutritionist_email || (nutritionistValidation.valid === false && formData.nutritionist_email)}
                        helperText={
                          errors.nutritionist_email ||
                          (formData.nutritionist_email && nutritionistValidation.message) ||
                          'Enter the email address of your assigned nutritionist'
                        }
                        disabled={loading}
                        size="medium"
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
                        <Alert severity="success" sx={{ mt: 2 }}>
                          <Typography variant="body2">
                            <strong>Nutritionist Found:</strong> {nutritionistValidation.nutritionist.name}
                          </Typography>
                        </Alert>
                      )}
                    </Box>
                  </Collapse>
                </Paper>
              </Box>

              {/* Security Section */}
              <Box sx={{ mb: 4 }}>
                <Typography variant="h6" gutterBottom sx={{
                  mb: 2,
                  fontWeight: '700',
                  color: '#4caf50',
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1
                }}>
                  🔒 Security
                </Typography>
                <Paper
                  variant="outlined"
                  sx={{
                    p: 3,
                    background: 'linear-gradient(135deg, #f0fff4 0%, #ffffff 100%)',
                    border: '2px solid #e6f7e9',
                    borderRadius: 3,
                    boxShadow: '0 4px 20px rgba(76, 175, 80, 0.08)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      boxShadow: '0 6px 30px rgba(76, 175, 80, 0.15)',
                      transform: 'translateY(-2px)'
                    }
                  }}>
                  <TextField
                    margin="normal"
                    required
                    fullWidth
                    label="Password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    value={formData.password}
                    onChange={handleChange}
                    error={!!errors.password}
                    helperText={errors.password || 'At least 8 characters, including uppercase, lowercase, and number'}
                    disabled={loading}
                    size="medium"
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
                    <Box sx={{ mt: 2, mb: 1 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body2" fontWeight="medium">{passwordStrength.text}</Typography>
                        <Typography variant="body2" fontWeight="medium">{passwordStrength.percent}%</Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={passwordStrength.percent}
                        sx={{
                          height: 8,
                          borderRadius: 4,
                          backgroundColor: '#e0e0e0',
                          '& .MuiLinearProgress-bar': {
                            backgroundColor: passwordStrength.color,
                            borderRadius: 4
                          }
                        }}
                      />
                    </Box>
                  )}
                  <TextField
                    margin="normal"
                    required
                    fullWidth
                    label="Confirm Password"
                    name="confirm_password"
                    type={showPassword ? 'text' : 'password'}
                    value={formData.confirm_password}
                    onChange={handleChange}
                    error={!!errors.confirm_password}
                    helperText={errors.confirm_password || 'Re-enter your password'}
                    disabled={loading}
                    size="medium"
                  />
                </Paper>
              </Box>

              <Button
                type="submit"
                fullWidth
                variant="contained"
                disabled={loading}
                size="large"
                sx={{
                  mt: 4,
                  mb: 3,
                  py: 2,
                  fontSize: '1.2rem',
                  fontWeight: '700',
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  boxShadow: '0 8px 32px rgba(102, 126, 234, 0.35)',
                  borderRadius: 3,
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #5568d3 0%, #653a8a 100%)',
                    boxShadow: '0 12px 40px rgba(102, 126, 234, 0.45)',
                    transform: 'translateY(-2px)'
                  },
                  '&:disabled': {
                    background: 'linear-gradient(135deg, #ccc 0%, #999 100%)'
                  }
                }}
              >
                {loading ? <CircularProgress size={28} sx={{ color: 'white' }} /> : '✅ Create My Account'}
              </Button>

              <Box sx={{ textAlign: 'center', mt: 2 }}>
                <Typography variant="body1" sx={{ color: '#666' }}>
                  Already have an account?{' '}
                  <Link
                    to="/auth/login"
                    style={{
                      textDecoration: 'none',
                      fontWeight: '700',
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      WebkitBackgroundClip: 'text',
                      WebkitTextFillColor: 'transparent',
                      transition: 'all 0.3s ease'
                    }}
                  >
                    Sign In
                  </Link>
                </Typography>
              </Box>
            </Box>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default Register;
