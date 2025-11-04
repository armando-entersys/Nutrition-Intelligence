/**
 * Reset Password Screen
 */
import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import {
  Container, Paper, TextField, Button, Typography, Box, Alert,
  InputAdornment, IconButton, CircularProgress, LinearProgress
} from '@mui/material';
import { LockReset, Lock, Visibility, VisibilityOff, CheckCircle } from '@mui/icons-material';
import authService from '../../services/authService';

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');

  const [formData, setFormData] = useState({ new_password: '', confirm_password: '' });
  const [errors, setErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [generalError, setGeneralError] = useState('');
  const [success, setSuccess] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState(null);

  useEffect(() => {
    if (!token) {
      setGeneralError('Invalid or missing reset token');
    }
  }, [token]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors(prev => ({ ...prev, [name]: '' }));
    setGeneralError('');
    if (name === 'new_password') {
      setPasswordStrength(authService.getPasswordStrength(value));
    }
  };

  const validate = () => {
    const newErrors = {};
    const passwordValidation = authService.validatePassword(formData.new_password);
    if (!passwordValidation.isValid) {
      newErrors.new_password = passwordValidation.errors.join('. ');
    }
    if (formData.new_password !== formData.confirm_password) {
      newErrors.confirm_password = 'Passwords do not match';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate() || !token) return;
    setLoading(true);
    try {
      await authService.resetPassword(token, formData.new_password, formData.confirm_password);
      setSuccess(true);
      setTimeout(() => navigate('/auth/login', {
        state: { message: 'Password reset successful! Please login with your new password.' }
      }), 2000);
    } catch (error) {
      setGeneralError(error.message || 'Failed to reset password');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <Container maxWidth="xs" sx={{ mt: 8 }}>
        <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
          <CheckCircle sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
          <Typography variant="h5" gutterBottom>Password Reset Successful!</Typography>
          <Typography variant="body2" color="text.secondary">
            Redirecting to login...
          </Typography>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="xs" sx={{ mt: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Box sx={{ width: 60, height: 60, borderRadius: '50%', bgcolor: 'primary.main',
            display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 2 }}>
            <LockReset sx={{ fontSize: 30, color: 'white' }} />
          </Box>
          <Typography variant="h5" gutterBottom>Reset Password</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3, textAlign: 'center' }}>
            Enter your new password below
          </Typography>

          {generalError && <Alert severity="error" sx={{ width: '100%', mb: 2 }}>{generalError}</Alert>}

          <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
            <TextField
              margin="normal" required fullWidth label="New Password" name="new_password"
              type={showPassword ? 'text' : 'password'} value={formData.new_password}
              onChange={handleChange} error={!!errors.new_password}
              helperText={errors.new_password} disabled={loading}
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
            {passwordStrength && formData.new_password && (
              <Box sx={{ mt: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                  <Typography variant="caption">{passwordStrength.text}</Typography>
                  <Typography variant="caption">{passwordStrength.percent}%</Typography>
                </Box>
                <LinearProgress variant="determinate" value={passwordStrength.percent}
                  sx={{ height: 6, borderRadius: 3,
                    '& .MuiLinearProgress-bar': { backgroundColor: passwordStrength.color }
                  }}
                />
              </Box>
            )}
            <TextField
              margin="normal" required fullWidth label="Confirm Password"
              name="confirm_password" type={showPassword ? 'text' : 'password'}
              value={formData.confirm_password} onChange={handleChange}
              error={!!errors.confirm_password} helperText={errors.confirm_password}
              disabled={loading}
            />
            <Button type="submit" fullWidth variant="contained" disabled={loading || !token}
              sx={{ mt: 3, mb: 2, py: 1.5 }}>
              {loading ? <CircularProgress size={24} /> : 'Reset Password'}
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default ResetPassword;
