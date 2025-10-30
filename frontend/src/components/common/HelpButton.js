import React, { useState } from 'react';
import { IconButton, Tooltip, Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography, List, ListItem, ListItemIcon, ListItemText, Box } from '@mui/material';
import { Help, Keyboard, Search, Dashboard, Restaurant } from '@mui/icons-material';
import { motion } from 'framer-motion';

const HelpButton = () => {
  const [open, setOpen] = useState(false);

  const shortcuts = [
    { key: 'Ctrl + K', description: 'Búsqueda global', icon: <Search /> },
    { key: 'Alt + 1', description: 'Ir al Dashboard', icon: <Dashboard /> },
    { key: 'Alt + 2', description: 'Ir a Alimentos', icon: <Restaurant /> },
    { key: 'Tab', description: 'Navegar entre elementos', icon: <Keyboard /> },
  ];

  const tips = [
    '💡 Usa el sidebar para navegar rápidamente entre secciones',
    '🔍 Presiona Ctrl+K para buscar cualquier cosa',
    '📊 Los gráficos son interactivos - haz click para más detalles',
    '🌮 El Chat IA conoce todos los platillos mexicanos tradicionales',
    '🏆 Completa tareas diarias para ganar XP y badges',
  ];

  return (
    <>
      <Tooltip title="Ayuda y atajos de teclado" arrow>
        <IconButton
          onClick={() => setOpen(true)}
          sx={{
            bgcolor: 'primary.main',
            color: 'white',
            minWidth: 48,
            minHeight: 48,
            '&:hover': {
              bgcolor: 'primary.dark',
              transform: 'scale(1.05)',
            },
            transition: 'all 0.3s',
            boxShadow: 2,
          }}
          aria-label="Abrir ayuda y atajos de teclado"
        >
          <Help />
        </IconButton>
      </Tooltip>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Help />
            <Typography variant="h6" fontWeight="700">Ayuda y Atajos</Typography>
          </Box>
        </DialogTitle>

        <DialogContent sx={{ mt: 2 }}>
          {/* Atajos de teclado */}
          <Typography variant="h6" fontWeight="700" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Keyboard /> Atajos de Teclado
          </Typography>
          <List dense>
            {shortcuts.map((shortcut, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
              >
                <ListItem sx={{ bgcolor: 'grey.50', borderRadius: 2, mb: 1 }}>
                  <ListItemIcon>{shortcut.icon}</ListItemIcon>
                  <ListItemText
                    primary={shortcut.description}
                    secondary={
                      <Box component="kbd" sx={{ bgcolor: 'grey.800', color: 'white', px: 1, py: 0.5, borderRadius: 1, fontSize: '0.8rem', fontFamily: 'monospace' }}>
                        {shortcut.key}
                      </Box>
                    }
                  />
                </ListItem>
              </motion.div>
            ))}
          </List>

          {/* Tips de uso */}
          <Typography variant="h6" fontWeight="700" gutterBottom sx={{ mt: 3 }}>
            💡 Tips de Uso
          </Typography>
          <List dense>
            {tips.map((tip, idx) => (
              <ListItem key={idx} sx={{ bgcolor: 'success.50', borderRadius: 2, mb: 1 }}>
                <ListItemText primary={tip} />
              </ListItem>
            ))}
          </List>
        </DialogContent>

        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setOpen(false)} variant="contained" fullWidth>
            Entendido
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default HelpButton;
