import React from 'react';
import { Box, Card, CardContent, Typography, Button, Grid, Chip } from '@mui/material';
import {
  Construction as ConstructionIcon,
  ArrowBack as ArrowBackIcon
} from '@mui/icons-material';

const AdminPlaceholder = ({
  title,
  description,
  icon: Icon,
  features = [],
  onBack
}) => {
  return (
    <Box sx={{ p: 3 }}>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={onBack}
        sx={{ mb: 3 }}
        variant="outlined"
      >
        Volver al Dashboard
      </Button>

      <Card sx={{ maxWidth: 800, mx: 'auto', mt: 4 }}>
        <CardContent sx={{ p: 4, textAlign: 'center' }}>
          <Box
            sx={{
              width: 100,
              height: 100,
              borderRadius: '50%',
              bgcolor: 'primary.light',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mx: 'auto',
              mb: 3,
            }}
          >
            {Icon && <Icon sx={{ fontSize: 48, color: 'primary.dark' }} />}
          </Box>

          <Typography variant="h4" gutterBottom fontWeight={700}>
            {title}
          </Typography>

          <Typography variant="body1" color="text.secondary" paragraph>
            {description}
          </Typography>

          <Chip
            icon={<ConstructionIcon />}
            label="En Desarrollo"
            color="warning"
            sx={{ mb: 3, fontWeight: 600 }}
          />

          {features.length > 0 && (
            <Box sx={{ mt: 4, textAlign: 'left' }}>
              <Typography variant="h6" gutterBottom fontWeight={600}>
                Funcionalidades Planificadas:
              </Typography>
              <Grid container spacing={2} sx={{ mt: 1 }}>
                {features.map((feature, index) => (
                  <Grid item xs={12} sm={6} key={index}>
                    <Box
                      sx={{
                        p: 2,
                        borderRadius: 2,
                        bgcolor: 'grey.50',
                        border: '1px solid',
                        borderColor: 'grey.200',
                      }}
                    >
                      <Typography variant="body2" fontWeight={500}>
                        ✓ {feature}
                      </Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </Box>
          )}

          <Box sx={{ mt: 4, p: 3, bgcolor: 'info.light', borderRadius: 2 }}>
            <Typography variant="body2" color="info.dark">
              Esta sección está actualmente en desarrollo. Las funcionalidades estarán
              disponibles próximamente.
            </Typography>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default AdminPlaceholder;
