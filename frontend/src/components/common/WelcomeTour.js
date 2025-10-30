import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography, Box, Stepper, Step, StepLabel, Card, CardContent, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import { Restaurant, Psychology, EmojiEvents, MenuBook, TrendingUp, CheckCircle } from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';

const WelcomeTour = () => {
  const [open, setOpen] = useState(false);
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    // Verificar si es la primera vez que el usuario visita
    const hasSeenTour = localStorage.getItem('hasSeenWelcomeTour');
    if (!hasSeenTour) {
      setTimeout(() => setOpen(true), 1000);
    }
  }, []);

  const steps = [
    {
      title: '¡Bienvenido a Nutrition Intelligence! 🇲🇽',
      icon: <Restaurant sx={{ fontSize: 60, color: '#4CAF50' }} />,
      description: 'La plataforma líder en nutrición mexicana con inteligencia artificial',
      features: [
        { icon: <Restaurant />, text: 'Base de datos con +500 alimentos mexicanos' },
        { icon: <Psychology />, text: 'Análisis nutricional con IA avanzada' },
        { icon: <MenuBook />, text: 'Recetas tradicionales saludables' },
      ]
    },
    {
      title: 'Navegación Intuitiva',
      icon: <TrendingUp sx={{ fontSize: 60, color: '#2196F3' }} />,
      description: 'Explora todas las funcionalidades desde el menú lateral',
      features: [
        { icon: <CheckCircle />, text: 'Dashboard: Vista general de tu actividad' },
        { icon: <CheckCircle />, text: 'Expediente Clínico: Historial completo del paciente' },
        { icon: <CheckCircle />, text: 'Dietas Dinámicas: Planes personalizados con IA' },
        { icon: <CheckCircle />, text: 'Chat Nutriólogo: Asistente virtual 24/7' },
      ]
    },
    {
      title: 'Gamificación Mexicana 🏆',
      icon: <EmojiEvents sx={{ fontSize: 60, color: '#FFD700' }} />,
      description: 'Gana XP, desbloquea badges y compite en el ranking nacional',
      features: [
        { icon: <CheckCircle />, text: 'Sistema de niveles: De Novato a Patrimonio UNESCO' },
        { icon: <CheckCircle />, text: 'Badges culturales: Taquero de Corazón, Guardián del Maíz' },
        { icon: <CheckCircle />, text: 'Racha de días: Mantén tu consistencia' },
      ]
    },
    {
      title: '¿Listo para empezar?',
      icon: <Psychology sx={{ fontSize: 60, color: '#9C27B0' }} />,
      description: 'Algunos tips rápidos para comenzar',
      features: [
        { icon: <CheckCircle />, text: 'Presiona Ctrl+K para búsqueda global' },
        { icon: <CheckCircle />, text: 'Click en el botón de ayuda (?) para ver atajos' },
        { icon: <CheckCircle />, text: 'Usa el Chat IA para resolver dudas al instante' },
        { icon: <CheckCircle />, text: 'Explora el Dashboard para conocer todas las funciones' },
      ]
    },
  ];

  const handleNext = () => {
    if (activeStep === steps.length - 1) {
      localStorage.setItem('hasSeenWelcomeTour', 'true');
      setOpen(false);
    } else {
      setActiveStep(activeStep + 1);
    }
  };

  const handleBack = () => {
    setActiveStep(activeStep - 1);
  };

  const handleSkip = () => {
    localStorage.setItem('hasSeenWelcomeTour', 'true');
    setOpen(false);
  };

  return (
    <Dialog open={open} onClose={handleSkip} maxWidth="md" fullWidth>
      <DialogTitle sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', pb: 2 }}>
        <Stepper activeStep={activeStep} alternativeLabel sx={{ mt: 2 }}>
          {steps.map((step, index) => (
            <Step key={index}>
              <StepLabel
                StepIconProps={{
                  sx: {
                    color: 'rgba(255,255,255,0.5)',
                    '&.Mui-active': { color: 'white' },
                    '&.Mui-completed': { color: '#4CAF50' },
                  }
                }}
              />
            </Step>
          ))}
        </Stepper>
      </DialogTitle>

      <DialogContent sx={{ mt: 3, minHeight: 400 }}>
        <AnimatePresence mode="wait">
          <motion.div
            key={activeStep}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.3 }}
          >
            <Card elevation={0} sx={{ bgcolor: 'transparent' }}>
              <CardContent>
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
                  {steps[activeStep].icon}
                  <Typography variant="h4" fontWeight="700" sx={{ mt: 2, textAlign: 'center' }}>
                    {steps[activeStep].title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary" sx={{ mt: 1, textAlign: 'center' }}>
                    {steps[activeStep].description}
                  </Typography>
                </Box>

                <List>
                  {steps[activeStep].features.map((feature, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.1 }}
                    >
                      <ListItem sx={{ bgcolor: 'grey.50', borderRadius: 2, mb: 1 }}>
                        <ListItemIcon>{feature.icon}</ListItemIcon>
                        <ListItemText primary={feature.text} primaryTypographyProps={{ fontWeight: 500 }} />
                      </ListItem>
                    </motion.div>
                  ))}
                </List>
              </CardContent>
            </Card>
          </motion.div>
        </AnimatePresence>
      </DialogContent>

      <DialogActions sx={{ p: 2, justifyContent: 'space-between' }}>
        <Button onClick={handleSkip} color="inherit">
          Saltar tour
        </Button>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button onClick={handleBack} disabled={activeStep === 0}>
            Anterior
          </Button>
          <Button variant="contained" onClick={handleNext}>
            {activeStep === steps.length - 1 ? '¡Comenzar!' : 'Siguiente'}
          </Button>
        </Box>
      </DialogActions>
    </Dialog>
  );
};

export default WelcomeTour;
