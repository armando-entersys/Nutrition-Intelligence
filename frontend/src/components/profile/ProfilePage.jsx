import React, { useState } from 'react';
import {
    Box,
    Card,
    CardContent,
    Typography,
    TextField,
    Button,
    Avatar,
    Grid,
    Divider,
    Alert,
    IconButton,
    InputAdornment,
} from '@mui/material';
import {
    Person as PersonIcon,
    Edit as EditIcon,
    Save as SaveIcon,
    Cancel as CancelIcon,
    Visibility,
    VisibilityOff,
    PhotoCamera,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const MotionCard = motion(Card);

const ProfilePage = ({ currentUser }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showNewPassword, setShowNewPassword] = useState(false);
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const [formData, setFormData] = useState({
        first_name: currentUser?.first_name || '',
        last_name: currentUser?.last_name || '',
        username: currentUser?.username || '',
        email: currentUser?.email || '',
        phone: currentUser?.phone || '',
    });

    const [passwordData, setPasswordData] = useState({
        current_password: '',
        new_password: '',
        confirm_password: '',
    });

    const handleInputChange = (field, value) => {
        setFormData(prev => ({
            ...prev,
            [field]: value,
        }));
    };

    const handlePasswordChange = (field, value) => {
        setPasswordData(prev => ({
            ...prev,
            [field]: value,
        }));
    };

    const handleSave = async () => {
        try {
            // TODO: Implement API call to update profile
            console.log('Guardando perfil:', formData);
            setSuccessMessage('✅ Perfil actualizado correctamente');
            setIsEditing(false);
            setTimeout(() => setSuccessMessage(''), 3000);
        } catch (error) {
            setErrorMessage('❌ Error al actualizar perfil');
            setTimeout(() => setErrorMessage(''), 3000);
        }
    };

    const handleChangePassword = async () => {
        if (passwordData.new_password !== passwordData.confirm_password) {
            setErrorMessage('❌ Las contraseñas no coinciden');
            setTimeout(() => setErrorMessage(''), 3000);
            return;
        }

        try {
            // TODO: Implement API call to change password
            console.log('Cambiando contraseña');
            setSuccessMessage('✅ Contraseña actualizada correctamente');
            setPasswordData({
                current_password: '',
                new_password: '',
                confirm_password: '',
            });
            setTimeout(() => setSuccessMessage(''), 3000);
        } catch (error) {
            setErrorMessage('❌ Error al cambiar contraseña');
            setTimeout(() => setErrorMessage(''), 3000);
        }
    };

    const handleCancel = () => {
        setFormData({
            first_name: currentUser?.first_name || '',
            last_name: currentUser?.last_name || '',
            username: currentUser?.username || '',
            email: currentUser?.email || '',
            phone: currentUser?.phone || '',
        });
        setIsEditing(false);
    };

    const getUserInitials = () => {
        const firstName = formData.first_name || '';
        const lastName = formData.last_name || '';
        if (firstName && lastName) {
            return `${firstName[0]}${lastName[0]}`.toUpperCase();
        }
        return formData.username?.substring(0, 2).toUpperCase() || 'U';
    };

    return (
        <Box sx={{ p: 3, maxWidth: 1000, margin: '0 auto' }}>
            <Typography variant="h4" gutterBottom fontWeight={600} sx={{ mb: 3 }}>
                👤 Mi Perfil
            </Typography>

            {successMessage && (
                <Alert severity="success" sx={{ mb: 2 }}>
                    {successMessage}
                </Alert>
            )}

            {errorMessage && (
                <Alert severity="error" sx={{ mb: 2 }}>
                    {errorMessage}
                </Alert>
            )}

            <Grid container spacing={3}>
                {/* Profile Picture Card */}
                <Grid item xs={12} md={4}>
                    <MotionCard
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.5 }}
                    >
                        <CardContent sx={{ textAlign: 'center', py: 4 }}>
                            <Box sx={{ position: 'relative', display: 'inline-block', mb: 2 }}>
                                <Avatar
                                    sx={{
                                        width: 120,
                                        height: 120,
                                        fontSize: '2.5rem',
                                        bgcolor: 'primary.main',
                                        margin: '0 auto',
                                    }}
                                >
                                    {getUserInitials()}
                                </Avatar>
                                <IconButton
                                    sx={{
                                        position: 'absolute',
                                        bottom: 0,
                                        right: 0,
                                        bgcolor: 'background.paper',
                                        boxShadow: 2,
                                        '&:hover': {
                                            bgcolor: 'primary.main',
                                            color: 'white',
                                        },
                                    }}
                                    size="small"
                                >
                                    <PhotoCamera fontSize="small" />
                                </IconButton>
                            </Box>
                            <Typography variant="h6" fontWeight={600}>
                                {formData.first_name} {formData.last_name}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                                @{formData.username}
                            </Typography>
                            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                                {currentUser?.primary_role === 'NUTRITIONIST' ? 'Nutricionista' : 'Usuario'}
                            </Typography>
                        </CardContent>
                    </MotionCard>
                </Grid>

                {/* Personal Information Card */}
                <Grid item xs={12} md={8}>
                    <MotionCard
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.5, delay: 0.1 }}
                    >
                        <CardContent>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                                <Typography variant="h6" fontWeight={600}>
                                    Información Personal
                                </Typography>
                                {!isEditing ? (
                                    <Button
                                        startIcon={<EditIcon />}
                                        onClick={() => setIsEditing(true)}
                                        variant="outlined"
                                    >
                                        Editar
                                    </Button>
                                ) : (
                                    <Box sx={{ display: 'flex', gap: 1 }}>
                                        <Button
                                            startIcon={<SaveIcon />}
                                            onClick={handleSave}
                                            variant="contained"
                                            color="primary"
                                        >
                                            Guardar
                                        </Button>
                                        <Button
                                            startIcon={<CancelIcon />}
                                            onClick={handleCancel}
                                            variant="outlined"
                                            color="error"
                                        >
                                            Cancelar
                                        </Button>
                                    </Box>
                                )}
                            </Box>

                            <Divider sx={{ mb: 3 }} />

                            <Grid container spacing={2}>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        fullWidth
                                        label="Nombre"
                                        value={formData.first_name}
                                        onChange={(e) => handleInputChange('first_name', e.target.value)}
                                        disabled={!isEditing}
                                        variant="outlined"
                                    />
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        fullWidth
                                        label="Apellidos"
                                        value={formData.last_name}
                                        onChange={(e) => handleInputChange('last_name', e.target.value)}
                                        disabled={!isEditing}
                                        variant="outlined"
                                    />
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        fullWidth
                                        label="Usuario"
                                        value={formData.username}
                                        onChange={(e) => handleInputChange('username', e.target.value)}
                                        disabled={!isEditing}
                                        variant="outlined"
                                    />
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <TextField
                                        fullWidth
                                        label="Correo Electrónico"
                                        value={formData.email}
                                        onChange={(e) => handleInputChange('email', e.target.value)}
                                        disabled={!isEditing}
                                        variant="outlined"
                                        type="email"
                                    />
                                </Grid>
                                <Grid item xs={12}>
                                    <TextField
                                        fullWidth
                                        label="Teléfono"
                                        value={formData.phone}
                                        onChange={(e) => handleInputChange('phone', e.target.value)}
                                        disabled={!isEditing}
                                        variant="outlined"
                                    />
                                </Grid>
                            </Grid>
                        </CardContent>
                    </MotionCard>
                </Grid>

                {/* Change Password Card */}
                <Grid item xs={12}>
                    <MotionCard
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                    >
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Cambiar Contraseña
                            </Typography>
                            <Divider sx={{ mb: 3 }} />

                            <Grid container spacing={2}>
                                <Grid item xs={12} md={4}>
                                    <TextField
                                        fullWidth
                                        label="Contraseña Actual"
                                        type={showPassword ? 'text' : 'password'}
                                        value={passwordData.current_password}
                                        onChange={(e) => handlePasswordChange('current_password', e.target.value)}
                                        variant="outlined"
                                        InputProps={{
                                            endAdornment: (
                                                <InputAdornment position="end">
                                                    <IconButton
                                                        onClick={() => setShowPassword(!showPassword)}
                                                        edge="end"
                                                    >
                                                        {showPassword ? <VisibilityOff /> : <Visibility />}
                                                    </IconButton>
                                                </InputAdornment>
                                            ),
                                        }}
                                    />
                                </Grid>
                                <Grid item xs={12} md={4}>
                                    <TextField
                                        fullWidth
                                        label="Nueva Contraseña"
                                        type={showNewPassword ? 'text' : 'password'}
                                        value={passwordData.new_password}
                                        onChange={(e) => handlePasswordChange('new_password', e.target.value)}
                                        variant="outlined"
                                        InputProps={{
                                            endAdornment: (
                                                <InputAdornment position="end">
                                                    <IconButton
                                                        onClick={() => setShowNewPassword(!showNewPassword)}
                                                        edge="end"
                                                    >
                                                        {showNewPassword ? <VisibilityOff /> : <Visibility />}
                                                    </IconButton>
                                                </InputAdornment>
                                            ),
                                        }}
                                    />
                                </Grid>
                                <Grid item xs={12} md={4}>
                                    <TextField
                                        fullWidth
                                        label="Confirmar Contraseña"
                                        type={showNewPassword ? 'text' : 'password'}
                                        value={passwordData.confirm_password}
                                        onChange={(e) => handlePasswordChange('confirm_password', e.target.value)}
                                        variant="outlined"
                                    />
                                </Grid>
                                <Grid item xs={12}>
                                    <Button
                                        variant="contained"
                                        color="secondary"
                                        onClick={handleChangePassword}
                                        disabled={!passwordData.current_password || !passwordData.new_password || !passwordData.confirm_password}
                                    >
                                        Actualizar Contraseña
                                    </Button>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </MotionCard>
                </Grid>

                {/* Account Information Card */}
                <Grid item xs={12}>
                    <MotionCard
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.3 }}
                    >
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} gutterBottom>
                                Información de la Cuenta
                            </Typography>
                            <Divider sx={{ mb: 2 }} />

                            <Grid container spacing={2}>
                                <Grid item xs={12} sm={6}>
                                    <Typography variant="body2" color="text.secondary">
                                        Rol Principal
                                    </Typography>
                                    <Typography variant="body1" fontWeight={500}>
                                        {currentUser?.primary_role === 'NUTRITIONIST' ? 'Nutricionista' : 'Usuario'}
                                    </Typography>
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <Typography variant="body2" color="text.secondary">
                                        Estado de la Cuenta
                                    </Typography>
                                    <Typography variant="body1" fontWeight={500}>
                                        {currentUser?.account_status === 'ACTIVE' ? '✅ Activa' : '❌ Inactiva'}
                                    </Typography>
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <Typography variant="body2" color="text.secondary">
                                        Email Verificado
                                    </Typography>
                                    <Typography variant="body1" fontWeight={500}>
                                        {currentUser?.is_email_verified ? '✅ Sí' : '❌ No'}
                                    </Typography>
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <Typography variant="body2" color="text.secondary">
                                        Miembro desde
                                    </Typography>
                                    <Typography variant="body1" fontWeight={500}>
                                        {currentUser?.created_at ? new Date(currentUser.created_at).toLocaleDateString('es-MX') : 'N/A'}
                                    </Typography>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </MotionCard>
                </Grid>
            </Grid>
        </Box>
    );
};

export default ProfilePage;
