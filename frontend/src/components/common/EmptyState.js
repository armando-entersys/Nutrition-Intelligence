import React from 'react';
import { Box, Typography, Button, Card } from '@mui/material';
import { motion } from 'framer-motion';

const EmptyState = ({
  icon: Icon,
  title,
  description,
  actionLabel,
  onAction,
  secondaryActionLabel,
  onSecondaryAction,
  illustration = '🤔'
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card
        sx={{
          minHeight: 400,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          p: 4,
          bgcolor: 'grey.50',
          borderRadius: 4,
          textAlign: 'center',
        }}
      >
        <motion.div
          animate={{
            y: [0, -10, 0],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        >
          {Icon ? (
            <Icon sx={{ fontSize: 120, color: 'primary.light', opacity: 0.6 }} />
          ) : (
            <Typography sx={{ fontSize: 120 }}>{illustration}</Typography>
          )}
        </motion.div>

        <Typography variant="h5" fontWeight="700" sx={{ mt: 3, mb: 1 }}>
          {title}
        </Typography>

        <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 500, mb: 3 }}>
          {description}
        </Typography>

        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', justifyContent: 'center' }}>
          {actionLabel && onAction && (
            <Button
              variant="contained"
              onClick={onAction}
              size="large"
              sx={{
                minWidth: 200,
                minHeight: 48,
                borderRadius: 3,
                boxShadow: 3,
              }}
            >
              {actionLabel}
            </Button>
          )}

          {secondaryActionLabel && onSecondaryAction && (
            <Button
              variant="outlined"
              onClick={onSecondaryAction}
              size="large"
              sx={{
                minWidth: 200,
                minHeight: 48,
                borderRadius: 3,
              }}
            >
              {secondaryActionLabel}
            </Button>
          )}
        </Box>
      </Card>
    </motion.div>
  );
};

export default EmptyState;
