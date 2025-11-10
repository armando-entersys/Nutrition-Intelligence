import React, { useState, useRef, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Card,
  TextField,
  Button,
  Avatar,
  Chip,
  Paper,
  Fade,
  Tooltip,
  IconButton,
  useTheme,
  alpha,
} from '@mui/material';
import {
  Send,
  SmartToy,
  Person,
  Restaurant,
  Fastfood,
  LocalFireDepartment,
  TipsAndUpdates,
  AutoAwesome,
  EmojiEvents,
  FiberManualRecord,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import { API_BASE_URL } from '../../config/api';

const ChatNutriologoIA = () => {
  const theme = useTheme();
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: '¡Hola! 👋 Soy tu Nutriólogo Virtual con IA especializado en nutrición mexicana.',
      timestamp: new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }),
    },
    {
      id: 2,
      sender: 'bot',
      text: 'Puedo ayudarte con análisis nutricional de platillos mexicanos, recetas saludables, equivalencias SMAE y mucho más. ¿En qué te puedo ayudar hoy?',
      timestamp: new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [currentTipIndex, setCurrentTipIndex] = useState(0);
  const messagesEndRef = useRef(null);

  // Datos simulados del paciente (en producción vendrían del backend)
  const patientData = {
    name: 'María',
    age: 32,
    goal: 'perder_peso',
    calories_target: 1800,
    preferences: ['tacos', 'ensaladas', 'pescado'],
    restrictions: ['lactosa'],
    recent_meals: ['chilaquiles', 'tacos al pastor', 'ensalada']
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Tips nutricionales dinámicos (rotan cada 10 segundos)
  const nutritionTips = [
    {
      emoji: '🫘',
      title: 'FRIJOLES NEGROS',
      text: 'Ricos en antocianinas. 1 taza = 15g proteína + 15g fibra. Perfectos para tu meta.'
    },
    {
      emoji: '🥑',
      title: 'AGUACATE',
      text: 'Grasas saludables omega-3. ½ aguacate = 1 equivalente de grasa. Mejora absorción de vitaminas.'
    },
    {
      emoji: '🌮',
      title: 'TACOS SALUDABLES',
      text: 'Usa tortilla de maíz (64 kcal) vs harina (104 kcal). Agrega verduras para más fibra.'
    },
    {
      emoji: '🥗',
      title: 'ENSALADAS MEXICANAS',
      text: 'Nopales: solo 14 kcal/taza + alta fibra. Excelente para control de peso.'
    },
    {
      emoji: '🐟',
      title: 'PESCADO FRESCO',
      text: 'Proteína magra: 25g proteína/100g. Bajo en grasa, alto en omega-3. Ideal para tus metas.'
    },
    {
      emoji: '🌶️',
      title: 'CHILES',
      text: 'Capsaicina acelera metabolismo 8%. Cero calorías, máximo sabor mexicano.'
    }
  ];

  // Rotar tips cada 10 segundos
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTipIndex((prev) => (prev + 1) % nutritionTips.length);
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  // Generar sugerencias personalizadas basadas en datos del paciente
  const generatePersonalizedSuggestions = () => {
    const suggestions = [];

    // Sugerencia basada en objetivo
    if (patientData.goal === 'perder_peso') {
      suggestions.push({
        icon: <LocalFireDepartment fontSize="small" />,
        text: `Cenas ligeras para ${patientData.calories_target} kcal`,
        color: '#FF6B6B',
        priority: 1
      });
    }

    // Sugerencia basada en preferencias
    if (patientData.preferences.includes('tacos')) {
      suggestions.push({
        icon: <Restaurant fontSize="small" />,
        text: 'Tacos saludables de pescado',
        color: '#4ECDC4',
        priority: 2
      });
    }

    if (patientData.preferences.includes('ensaladas')) {
      suggestions.push({
        icon: <Fastfood fontSize="small" />,
        text: 'Ensalada de nopales y atún',
        color: '#4CAF50',
        priority: 3
      });
    }

    // Sugerencia basada en restricciones
    if (patientData.restrictions.includes('lactosa')) {
      suggestions.push({
        icon: <TipsAndUpdates fontSize="small" />,
        text: 'Alternativas sin lactosa para crema',
        color: '#FFB142',
        priority: 4
      });
    }

    // Sugerencia basada en comidas recientes
    if (patientData.recent_meals.includes('chilaquiles')) {
      suggestions.push({
        icon: <Restaurant fontSize="small" />,
        text: 'Chilaquiles verdes más ligeros',
        color: '#95E1D3',
        priority: 5
      });
    }

    // Ordenar por prioridad y tomar las primeras 4
    return suggestions.sort((a, b) => a.priority - b.priority).slice(0, 4);
  };

  const quickSuggestions = generatePersonalizedSuggestions();

  // Función para llamar al API de chat del nutriólogo
  const generateAIResponse = async (userMessage) => {
    try {
      // Construir el historial de conversación en el formato esperado por el API
      const conversationHistory = messages
        .filter(msg => msg.sender === 'user' || msg.sender === 'bot')
        .map(msg => ({
          role: msg.sender === 'user' ? 'user' : 'assistant',
          content: msg.text
        }));

      // Llamar al endpoint del backend
      const response = await axios.post(
        `${API_BASE_URL}/api/v1/nutritionist-chat/chat`,
        {
          message: userMessage,
          conversation_history: conversationHistory
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          timeout: 30000, // 30 segundos de timeout
        }
      );

      // El API devuelve { response: string, tags: string[] }
      return {
        text: response.data.response,
        tags: response.data.tags,
      };
    } catch (error) {
      console.error('Error al comunicarse con el nutriólogo IA:', error);

      // Respuesta de fallback en caso de error
      return {
        text: '🤔 Lo siento, estoy teniendo problemas para conectarme en este momento. Por favor intenta de nuevo en unos segundos.\n\nPuedo ayudarte con:\n\n• 📊 Análisis nutricional de platillos mexicanos\n• 🍽️ Recetas saludables tradicionales\n• 🔄 Equivalencias SMAE\n• 💡 Sustituciones para reducir calorías\n• 📋 Planificación de menús balanceados',
        tags: ['error_conexion'],
      };
    }
  };

  const handleSendMessage = async () => {
    if (inputText.trim() === '') return;

    const userMessage = {
      id: messages.length + 1,
      sender: 'user',
      text: inputText,
      timestamp: new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }),
    };

    const currentInput = inputText;
    setMessages([...messages, userMessage]);
    setInputText('');
    setIsTyping(true);

    // Llamar al API de forma asíncrona
    try {
      const aiResponse = await generateAIResponse(currentInput);
      const botMessage = {
        id: messages.length + 2,
        sender: 'bot',
        text: aiResponse.text,
        tags: aiResponse.tags,
        timestamp: new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error al procesar mensaje:', error);
    } finally {
      setIsTyping(false);
    }
  };

  const handleQuickSuggestion = async (text) => {
    setInputText(text);

    // Pequeño delay para que se vea la sugerencia en el input
    await new Promise(resolve => setTimeout(resolve, 100));

    const newMessage = {
      id: messages.length + 1,
      sender: 'user',
      text: text,
      timestamp: new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages([...messages, newMessage]);
    setInputText('');
    setIsTyping(true);

    // Llamar al API de forma asíncrona
    try {
      const aiResponse = await generateAIResponse(text);
      const botMessage = {
        id: messages.length + 2,
        sender: 'bot',
        text: aiResponse.text,
        tags: aiResponse.tags,
        timestamp: new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error al procesar sugerencia:', error);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Box
      sx={{
        width: '100%',
        height: 'calc(100vh - 120px)',
        display: 'flex',
        bgcolor: alpha(theme.palette.primary.main, 0.02),
        borderRadius: 3,
        overflow: 'hidden',
      }}
    >
      {/* Panel lateral - Sugerencias */}
      <Box
        sx={{
          width: { xs: '100%', md: 320 },
          borderRight: { md: `1px solid ${alpha(theme.palette.divider, 0.1)}` },
          display: { xs: 'none', md: 'flex' },
          flexDirection: 'column',
          bgcolor: 'background.paper',
          p: 2,
          overflowY: 'auto',
          height: '100%',
        }}
      >

        {/* Sugerencias personalizadas */}
        <Box>
          <Typography variant="subtitle2" fontWeight={700} sx={{ mb: 1.5, color: 'text.secondary' }}>
            💡 Sugerencias
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            {quickSuggestions.map((suggestion, idx) => (
              <motion.div key={idx} whileHover={{ x: 4 }} whileTap={{ scale: 0.98 }}>
                <Button
                  onClick={() => handleQuickSuggestion(suggestion.text)}
                  sx={{
                    width: '100%',
                    justifyContent: 'flex-start',
                    textAlign: 'left',
                    borderRadius: 2,
                    p: 1.5,
                    bgcolor: alpha(suggestion.color, 0.08),
                    border: `1px solid ${alpha(suggestion.color, 0.2)}`,
                    textTransform: 'none',
                    '&:hover': {
                      bgcolor: alpha(suggestion.color, 0.15),
                      borderColor: alpha(suggestion.color, 0.4),
                    },
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    {React.cloneElement(suggestion.icon, { sx: { color: suggestion.color } })}
                    <Typography variant="body2" fontWeight={500} color="text.primary">
                      {suggestion.text}
                    </Typography>
                  </Box>
                </Button>
              </motion.div>
            ))}
          </Box>
        </Box>

        {/* Tip nutricional dinámico con animación */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentTipIndex}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
          >
            <Box
              sx={{
                mt: 'auto',
                p: 2,
                borderRadius: 2,
                background: `linear-gradient(135deg, ${theme.palette.success.main} 0%, ${theme.palette.success.dark} 100%)`,
                color: 'white',
              }}
            >
              <Typography variant="caption" fontWeight={700} sx={{ display: 'block', mb: 0.5, opacity: 0.9 }}>
                {nutritionTips[currentTipIndex].emoji} {nutritionTips[currentTipIndex].title}
              </Typography>
              <Typography variant="body2" sx={{ fontSize: '0.85rem', lineHeight: 1.4 }}>
                {nutritionTips[currentTipIndex].text}
              </Typography>
              <Box sx={{ display: 'flex', gap: 0.5, mt: 1, justifyContent: 'center' }}>
                {nutritionTips.map((_, idx) => (
                  <Box
                    key={idx}
                    sx={{
                      width: 6,
                      height: 6,
                      borderRadius: '50%',
                      bgcolor: idx === currentTipIndex ? 'white' : alpha(theme.palette.common.white, 0.3),
                      transition: 'all 0.3s ease',
                    }}
                  />
                ))}
              </Box>
            </Box>
          </motion.div>
        </AnimatePresence>
      </Box>

      {/* Panel principal del chat */}
      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {/* Header compacto */}
        <Box
          sx={{
            p: 2,
            borderBottom: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
            bgcolor: 'background.paper',
            boxShadow: `0 1px 3px ${alpha(theme.palette.common.black, 0.05)}`,
            flexShrink: 0,
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Avatar
              sx={{
                width: 44,
                height: 44,
                bgcolor: theme.palette.primary.main,
                boxShadow: `0 4px 12px ${alpha(theme.palette.primary.main, 0.3)}`,
              }}
            >
              <SmartToy />
            </Avatar>
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" fontWeight={700} sx={{ lineHeight: 1.2 }}>
                Nutriólogo Virtual IA
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mt: 0.5 }}>
                <FiberManualRecord sx={{ fontSize: 10, color: theme.palette.success.main }} />
                <Typography variant="caption" color="text.secondary">
                  Disponible 24/7
                </Typography>
              </Box>
            </Box>
          </Box>
        </Box>

        {/* Área de mensajes */}
        <Box
          sx={{
            flex: 1,
            overflowY: 'auto',
            p: 3,
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
          }}
        >
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.3, ease: 'easeOut' }}
              >
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                    alignItems: 'flex-end',
                    gap: 1,
                  }}
                >
                  {message.sender === 'bot' && (
                    <Avatar
                      sx={{
                        width: 32,
                        height: 32,
                        bgcolor: theme.palette.primary.main,
                        boxShadow: `0 2px 8px ${alpha(theme.palette.primary.main, 0.2)}`,
                      }}
                    >
                      <SmartToy sx={{ fontSize: 18 }} />
                    </Avatar>
                  )}
                  <Box sx={{ maxWidth: '70%' }}>
                    <Paper
                      elevation={0}
                      sx={{
                        p: 2,
                        bgcolor: message.sender === 'user' ? theme.palette.primary.main : 'background.paper',
                        color: message.sender === 'user' ? 'white' : 'text.primary',
                        borderRadius: 3,
                        border: message.sender === 'bot' ? `1px solid ${alpha(theme.palette.divider, 0.1)}` : 'none',
                        boxShadow:
                          message.sender === 'user'
                            ? `0 4px 12px ${alpha(theme.palette.primary.main, 0.3)}`
                            : `0 2px 8px ${alpha(theme.palette.common.black, 0.05)}`,
                      }}
                    >
                      <Typography
                        variant="body1"
                        sx={{
                          whiteSpace: 'pre-wrap',
                          lineHeight: 1.6,
                          fontSize: '0.95rem',
                          '& strong': { fontWeight: 700 },
                        }}
                      >
                        {message.text}
                      </Typography>
                      {message.tags && (
                        <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap', mt: 1.5 }}>
                          {message.tags.map((tag, idx) => (
                            <Chip
                              key={idx}
                              label={tag.replace('_', ' ')}
                              size="small"
                              sx={{
                                height: 22,
                                fontSize: '0.7rem',
                                fontWeight: 600,
                                bgcolor: alpha(theme.palette.primary.main, 0.12),
                                color: theme.palette.primary.dark,
                                borderRadius: 1.5,
                              }}
                            />
                          ))}
                        </Box>
                      )}
                      <Typography
                        variant="caption"
                        sx={{
                          display: 'block',
                          mt: 1,
                          opacity: 0.7,
                          fontSize: '0.7rem',
                          textAlign: message.sender === 'user' ? 'right' : 'left',
                        }}
                      >
                        {message.timestamp}
                      </Typography>
                    </Paper>
                  </Box>
                  {message.sender === 'user' && (
                    <Avatar
                      sx={{
                        width: 32,
                        height: 32,
                        bgcolor: theme.palette.grey[600],
                      }}
                    >
                      <Person sx={{ fontSize: 18 }} />
                    </Avatar>
                  )}
                </Box>
              </motion.div>
            ))}
          </AnimatePresence>

          {isTyping && (
            <Fade in={isTyping}>
              <Box sx={{ display: 'flex', alignItems: 'flex-end', gap: 1 }}>
                <Avatar sx={{ width: 32, height: 32, bgcolor: theme.palette.primary.main }}>
                  <SmartToy sx={{ fontSize: 18 }} />
                </Avatar>
                <Paper
                  elevation={0}
                  sx={{
                    p: 2,
                    bgcolor: 'background.paper',
                    borderRadius: 3,
                    border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
                  }}
                >
                  <Box sx={{ display: 'flex', gap: 0.5 }}>
                    {[0, 1, 2].map((i) => (
                      <Box
                        key={i}
                        sx={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          bgcolor: theme.palette.primary.main,
                          animation: 'pulse 1.4s infinite',
                          animationDelay: `${i * 0.2}s`,
                        }}
                      />
                    ))}
                  </Box>
                </Paper>
              </Box>
            </Fade>
          )}
          <div ref={messagesEndRef} />
        </Box>

        {/* Input de mensaje */}
        <Box
          sx={{
            p: 2,
            borderTop: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
            bgcolor: 'background.paper',
            flexShrink: 0,
          }}
        >
          <Box sx={{ display: 'flex', gap: 1.5, alignItems: 'flex-end' }}>
            <TextField
              fullWidth
              multiline
              maxRows={4}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Pregunta sobre nutrición mexicana..."
              variant="outlined"
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 3,
                  bgcolor: alpha(theme.palette.primary.main, 0.02),
                  '&:hover': {
                    bgcolor: alpha(theme.palette.primary.main, 0.04),
                  },
                  '&.Mui-focused': {
                    bgcolor: 'background.paper',
                  },
                },
              }}
            />
            <Tooltip title="Enviar mensaje" arrow>
              <span>
                <IconButton
                  onClick={handleSendMessage}
                  disabled={inputText.trim() === ''}
                  sx={{
                    width: 48,
                    height: 48,
                    bgcolor: theme.palette.primary.main,
                    color: 'white',
                    boxShadow: `0 4px 12px ${alpha(theme.palette.primary.main, 0.3)}`,
                    '&:hover': {
                      bgcolor: theme.palette.primary.dark,
                      boxShadow: `0 6px 16px ${alpha(theme.palette.primary.main, 0.4)}`,
                    },
                    '&:disabled': {
                      bgcolor: alpha(theme.palette.primary.main, 0.3),
                      color: alpha(theme.palette.common.white, 0.5),
                    },
                  }}
                >
                  <Send />
                </IconButton>
              </span>
            </Tooltip>
          </Box>
        </Box>
      </Box>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 0.3; transform: scale(0.8); }
          50% { opacity: 1; transform: scale(1.2); }
        }
      `}</style>
    </Box>
  );
};

export default ChatNutriologoIA;
