import React from 'react';
import { Box, Typography, CircularProgress, LinearProgress } from '@mui/material';
import { motion } from 'framer-motion';

const LoadingState = ({
  message = 'Cargando...',
  submessage,
  progress,
  type = 'circular', // 'circular', 'linear', 'skeleton'
}) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: 300,
        p: 4,
      }}
    >
      {type === 'circular' && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 200 }}
        >
          <CircularProgress
            size={80}
            thickness={4}
            sx={{
              color: 'primary.main',
              mb: 3,
            }}
            aria-label="Cargando contenido"
          />
        </motion.div>
      )}

      {type === 'linear' && progress !== undefined && (
        <Box sx={{ width: '100%', maxWidth: 400, mb: 3 }}>
          <LinearProgress
            variant="determinate"
            value={progress}
            sx={{
              height: 8,
              borderRadius: 4,
              bgcolor: 'grey.200',
              '& .MuiLinearProgress-bar': {
                borderRadius: 4,
                background: 'linear-gradient(90deg, #4CAF50 0%, #81C784 100%)',
              },
            }}
          />
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block', textAlign: 'center' }}>
            {Math.round(progress)}%
          </Typography>
        </Box>
      )}

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <Typography
          variant="h6"
          fontWeight="600"
          color="primary.main"
          sx={{ textAlign: 'center', mb: 1 }}
        >
          {message}
        </Typography>

        {submessage && (
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ textAlign: 'center', maxWidth: 400 }}
          >
            {submessage}
          </Typography>
        )}
      </motion.div>

      {/* Animated dots */}
      <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
        {[0, 1, 2].map((i) => (
          <motion.div
            key={i}
            animate={{
              scale: [1, 1.3, 1],
              opacity: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 1,
              repeat: Infinity,
              delay: i * 0.2,
            }}
          >
            <Box
              sx={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                bgcolor: 'primary.main',
              }}
            />
          </motion.div>
        ))}
      </Box>
    </Box>
  );
};

export default LoadingState;
