/**
 * Forgot Password Screen
 */
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Container, Paper, TextField, Button, Typography, Box, Alert, InputAdornment, CircularProgress
} from '@mui/material';
import { LockReset, Email, ArrowBack } from '@mui/icons-material';
import authService from '../../services/authService';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [resetData, setResetData] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!email) {
      setError('Email is required');
      return;
    }
    if (!authService.validateEmail(email)) {
      setError('Invalid email format');
      return;
    }

    setLoading(true);
    try {
      const response = await authService.forgotPassword(email);
      setSuccess(true);
      setResetData(response);
    } catch (err) {
      setError(err.message || 'Failed to send reset email');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <Container maxWidth="xs" sx={{ mt: 8 }}>
        <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
          <LockReset sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
          <Typography variant="h5" gutterBottom>Check Your Email</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            We've sent password reset instructions to your email. Please check your inbox and follow the link to reset your password.
          </Typography>
          <Alert severity="success" sx={{ mb: 2, textAlign: 'left' }}>
            <Typography variant="body2">
              <strong>📧 Email sent successfully!</strong>
            </Typography>
            <Typography variant="caption" component="div" sx={{ mt: 1 }}>
              The reset link will expire in 1 hour for security reasons.
            </Typography>
          </Alert>
          <Button component={Link} to="/auth/login" variant="contained" fullWidth>
            Back to Login
          </Button>
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
          <Typography variant="h5" gutterBottom>Forgot Password?</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3, textAlign: 'center' }}>
            Enter your email and we'll send you instructions to reset your password
          </Typography>

          {error && <Alert severity="error" sx={{ width: '100%', mb: 2 }}>{error}</Alert>}

          <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
            <TextField
              margin="normal" required fullWidth label="Email Address" type="email"
              value={email} onChange={(e) => setEmail(e.target.value)}
              autoFocus disabled={loading}
              InputProps={{
                startAdornment: <InputAdornment position="start"><Email /></InputAdornment>
              }}
            />
            <Button type="submit" fullWidth variant="contained" disabled={loading}
              sx={{ mt: 3, mb: 2, py: 1.5 }}>
              {loading ? <CircularProgress size={24} /> : 'Send Reset Link'}
            </Button>
            <Button component={Link} to="/auth/login" startIcon={<ArrowBack />}
              fullWidth variant="text" disabled={loading}>
              Back to Login
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default ForgotPassword;
