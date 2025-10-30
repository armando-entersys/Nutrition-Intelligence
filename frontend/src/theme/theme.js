import { createTheme } from '@mui/material/styles';

/**
 * Material 3 Expressive Theme for Nutrition Intelligence
 *
 * Utiliza el sistema HCT (Hue-Chroma-Tone) de Material 3
 * Colores optimizados para aplicaciones de salud y nutrición
 *
 * Paleta Verde Saludable (Hue: 130-150) - Representa nutrición, salud, naturaleza
 * Con acentos cálidos para energía y vitalidad
 */

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#4CAF50',      // Verde saludable - H:122 C:80 T:60
      light: '#81C784',      // Verde claro - H:122 C:60 T:75
      dark: '#388E3C',       // Verde oscuro - H:122 C:90 T:45
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: '#FF6F00',       // Naranja energía - H:30 C:100 T:50
      light: '#FF9E40',      // Naranja claro - H:30 C:80 T:70
      dark: '#C43E00',       // Naranja oscuro - H:30 C:100 T:35
      contrastText: '#FFFFFF',
    },
    tertiary: {
      main: '#0288D1',       // Azul confianza - H:200 C:85 T:50
      light: '#4FC3F7',      // Azul claro - H:200 C:70 T:75
      dark: '#01579B',       // Azul oscuro - H:200 C:95 T:35
      contrastText: '#FFFFFF',
    },
    error: {
      main: '#D32F2F',
      light: '#EF5350',
      dark: '#C62828',
    },
    warning: {
      main: '#F57C00',
      light: '#FF9800',
      dark: '#E65100',
    },
    info: {
      main: '#0288D1',
      light: '#03A9F4',
      dark: '#01579B',
    },
    success: {
      main: '#388E3C',
      light: '#4CAF50',
      dark: '#1B5E20',
    },
    background: {
      default: '#F5F5F5',    // Gris muy claro
      paper: '#FFFFFF',       // Blanco puro
      elevated: '#FAFAFA',    // Blanco cálido
    },
    text: {
      primary: '#212121',     // Negro suave
      secondary: '#757575',   // Gris medio
      disabled: '#BDBDBD',    // Gris claro
    },
    divider: '#E0E0E0',
  },

  // Typography - Sistema de tipos Material 3
  typography: {
    fontFamily: [
      'Roboto',
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),

    // Display - Textos grandes y expresivos
    h1: {
      fontSize: '3.5rem',
      fontWeight: 400,
      lineHeight: 1.2,
      letterSpacing: '-0.02em',
    },
    h2: {
      fontSize: '2.75rem',
      fontWeight: 400,
      lineHeight: 1.3,
      letterSpacing: '-0.01em',
    },
    h3: {
      fontSize: '2.25rem',
      fontWeight: 400,
      lineHeight: 1.4,
    },
    h4: {
      fontSize: '1.75rem',
      fontWeight: 500,
      lineHeight: 1.4,
    },
    h5: {
      fontSize: '1.5rem',
      fontWeight: 500,
      lineHeight: 1.5,
    },
    h6: {
      fontSize: '1.25rem',
      fontWeight: 500,
      lineHeight: 1.5,
    },

    // Body - Texto de contenido
    body1: {
      fontSize: '1rem',
      fontWeight: 400,
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem',
      fontWeight: 400,
      lineHeight: 1.5,
    },

    // Labels - Etiquetas y botones
    button: {
      fontSize: '0.875rem',
      fontWeight: 500,
      lineHeight: 1.75,
      letterSpacing: '0.02em',
      textTransform: 'none', // Sin mayúsculas automáticas
    },
    caption: {
      fontSize: '0.75rem',
      fontWeight: 400,
      lineHeight: 1.66,
    },
    overline: {
      fontSize: '0.75rem',
      fontWeight: 500,
      lineHeight: 2.5,
      letterSpacing: '0.08em',
      textTransform: 'uppercase',
    },
  },

  // Shape - Bordes redondeados Material 3
  shape: {
    borderRadius: 16, // Material 3 usa bordes más redondeados
  },

  // Shadows - Elevaciones Material 3
  shadows: [
    'none',
    '0px 1px 2px rgba(0, 0, 0, 0.05)',
    '0px 2px 4px rgba(0, 0, 0, 0.06)',
    '0px 4px 8px rgba(0, 0, 0, 0.08)',
    '0px 6px 12px rgba(0, 0, 0, 0.10)',
    '0px 8px 16px rgba(0, 0, 0, 0.12)',
    '0px 12px 24px rgba(0, 0, 0, 0.14)',
    '0px 16px 32px rgba(0, 0, 0, 0.16)',
    '0px 24px 48px rgba(0, 0, 0, 0.18)',
    '0px 32px 64px rgba(0, 0, 0, 0.20)',
    '0px 40px 80px rgba(0, 0, 0, 0.22)',
    '0px 48px 96px rgba(0, 0, 0, 0.24)',
    '0px 56px 112px rgba(0, 0, 0, 0.26)',
    '0px 64px 128px rgba(0, 0, 0, 0.28)',
    '0px 72px 144px rgba(0, 0, 0, 0.30)',
    '0px 80px 160px rgba(0, 0, 0, 0.32)',
    '0px 88px 176px rgba(0, 0, 0, 0.34)',
    '0px 96px 192px rgba(0, 0, 0, 0.36)',
    '0px 104px 208px rgba(0, 0, 0, 0.38)',
    '0px 112px 224px rgba(0, 0, 0, 0.40)',
    '0px 120px 240px rgba(0, 0, 0, 0.42)',
    '0px 128px 256px rgba(0, 0, 0, 0.44)',
    '0px 136px 272px rgba(0, 0, 0, 0.46)',
    '0px 144px 288px rgba(0, 0, 0, 0.48)',
    '0px 152px 304px rgba(0, 0, 0, 0.50)',
  ],

  // Transitions - Animaciones con spring physics
  transitions: {
    duration: {
      shortest: 150,
      shorter: 200,
      short: 250,
      standard: 300,
      complex: 375,
      enteringScreen: 225,
      leavingScreen: 195,
    },
    easing: {
      // Material 3 Expressive usa curvas de animación basadas en física
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)', // Standard
      easeOut: 'cubic-bezier(0.0, 0, 0.2, 1)',    // Decelerate
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',       // Accelerate
      sharp: 'cubic-bezier(0.4, 0, 0.6, 1)',      // Sharp
      spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)', // Spring physics
    },
  },

  // Components - Estilos personalizados de componentes
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 20,
          padding: '10px 24px',
          fontSize: '0.9375rem',
          fontWeight: 500,
          textTransform: 'none',
          boxShadow: 'none',
          transition: 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)', // Spring animation
          '&:hover': {
            boxShadow: '0px 4px 12px rgba(76, 175, 80, 0.3)',
            transform: 'translateY(-2px)',
          },
          '&:active': {
            transform: 'translateY(0px)',
          },
        },
        contained: {
          '&:hover': {
            boxShadow: '0px 6px 16px rgba(76, 175, 80, 0.4)',
          },
        },
        outlined: {
          borderWidth: 2,
          '&:hover': {
            borderWidth: 2,
          },
        },
      },
      defaultProps: {
        disableElevation: false,
      },
    },

    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 20,
          boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.08)',
          transition: 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
          '&:hover': {
            boxShadow: '0px 8px 24px rgba(0, 0, 0, 0.12)',
            transform: 'translateY(-4px)',
          },
        },
      },
    },

    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
        },
        elevation1: {
          boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.06)',
        },
        elevation2: {
          boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.08)',
        },
        elevation3: {
          boxShadow: '0px 6px 12px rgba(0, 0, 0, 0.10)',
        },
      },
    },

    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          fontWeight: 500,
        },
      },
    },

    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: '0px 2px 8px rgba(0, 0, 0, 0.08)',
        },
      },
    },

    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 12,
          },
        },
      },
    },

    MuiSelect: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },

    MuiDialog: {
      styleOverrides: {
        paper: {
          borderRadius: 24,
        },
      },
    },

    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRadius: '0px 24px 24px 0px',
        },
      },
    },
  },

  // Breakpoints - Responsive design
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 960,
      lg: 1280,
      xl: 1920,
    },
  },

  // Spacing - Sistema de espaciado 8px
  spacing: 8,

  // Z-Index layers
  zIndex: {
    mobileStepper: 1000,
    speedDial: 1050,
    appBar: 1100,
    drawer: 1200,
    modal: 1300,
    snackbar: 1400,
    tooltip: 1500,
  },
});

export default theme;
