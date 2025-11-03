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

  // Base de conocimiento
  const generateAIResponse = (userMessage) => {
    const lowerMessage = userMessage.toLowerCase();

    if (lowerMessage.includes('tacos') || lowerMessage.includes('taco')) {
      return {
        text: '🌮 **Análisis de Tacos al Pastor**\n\n**Información Nutricional (3 tacos):**\n\n• Calorías: ~680 kcal\n• Proteína: 35g\n• Carbohidratos: 75g\n• Grasas: 22g\n\n**Tips para hacerlos más saludables:**\n\n✓ Usa tortilla de maíz (más fibra)\n✓ Reduce la porción de carne a 120g\n✓ Agrega piña natural, cebolla y cilantro\n✓ Limita a 2-3 tacos por comida\n✓ Acompaña con frijoles de la olla\n\n**Equivalencias SMAE:** 3 cereales + 3 carnes moderada grasa',
        tags: ['alto_proteína', 'tradicional_mexicano'],
      };
    }

    if (lowerMessage.includes('frijol') || lowerMessage.includes('frijoles')) {
      return {
        text: '🫘 **Los Frijoles - Superalimento Mexicano**\n\n**Beneficios Nutricionales:**\n\n• 15g proteína vegetal por taza\n• 15g fibra soluble\n• Rico en hierro y magnesio\n• Bajo índice glucémico\n• Excelente para control de peso\n\n**Recetas Saludables:**\n\n1. Frijoles de la olla con epazote\n2. Sopa de frijol negro con chile\n3. Enfrijoladas con queso panela\n4. Tostadas con nopales\n\n**Equivalencia:** 1 taza = 2 leguminosas SMAE',
        tags: ['alto_fibra', 'proteína_vegetal'],
      };
    }

    if (lowerMessage.includes('tortilla')) {
      return {
        text: '🌽 **Tortillas - Comparativa Nutricional**\n\n**Tortilla de Maíz (30g):**\n• 64 kcal | 13g carbs | 1.5g fibra\n• Índice glucémico: Medio (52)\n• ✓ Más calcio y fibra\n\n**Tortilla de Harina (40g):**\n• 104 kcal | 18g carbs | 1g fibra\n• Índice glucémico: Alto (70)\n• ✗ Más calorías y menor fibra\n\n**Recomendación:** Prefiere maíz nixtamalizado\n\n**Alternativas:**\n• Maíz azul (más antioxidantes)\n• Integral\n• Con nopal (menos calorías)',
        tags: ['cereal', 'índice_glucémico'],
      };
    }

    if (lowerMessage.includes('crema') || lowerMessage.includes('sustituto')) {
      return {
        text: '💡 **Sustitutos Saludables para Crema**\n\n1. **Yogurt Griego Natural** (0% grasa)\n   → 90% menos grasa\n   → Alto en proteína\n   → Textura cremosa\n\n2. **Jocoque**\n   → Tradicional mexicano\n   → Probióticos naturales\n\n3. **Aguacate Machacado**\n   → Grasas saludables\n   → Alto en fibra\n\n4. **Queso Cottage** licuado + limón\n   → Textura cremosa\n   → Bajo en grasa\n\n**Equivalencias:** 2 cdas crema = 1 grasa | 2 cdas yogurt = ½ leche',
        tags: ['sustitución', 'bajo_grasa'],
      };
    }

    if (lowerMessage.includes('receta') || lowerMessage.includes('chilaquiles')) {
      return {
        text: '👨‍🍳 **Chilaquiles Verdes Saludables**\n\n**Ingredientes (4 porciones):**\n• 8 tortillas (horneadas)\n• 2 tazas salsa verde casera\n• 1 pechuga deshebrada\n• ½ taza cebolla morada\n• ¼ taza queso panela\n• Cilantro fresco\n\n**Preparación:**\n1. Hornea las tortillas a 180°C x 15 min\n2. Licúa tomates, chile, cebolla, cilantro\n3. Calienta salsa y agrega tortillas\n4. Sirve con pollo y guarniciones\n\n**Por porción:** 320 kcal | 25g proteína\n**Equivalencias:** 2 cereales + 1 verdura + 2 carnes',
        tags: ['receta', 'alto_proteína'],
      };
    }

    if (lowerMessage.includes('cena') || lowerMessage.includes('ligera') || lowerMessage.includes('1800')) {
      return {
        text: '🌙 **Cenas Ligeras para ${patientData.calories_target} kcal/día**\n\n**Opción 1: Ensalada de Atún** (350 kcal)\n• 120g atún en agua\n• 2 tazas verduras mixtas\n• ½ aguacate\n• Limón y chile piquín\n\n**Opción 2: Tacos de Pescado** (420 kcal)\n• 2 tortillas de maíz\n• 150g pescado a la plancha\n• Pico de gallo\n• Repollo morado\n\n**Opción 3: Sopa de Verduras** (280 kcal)\n• Caldo de pollo\n• Nopales, calabaza, chayote\n• 1 taza frijoles\n\n**Tip:** Cena antes de las 8pm para mejor digestión',
        tags: ['cena', 'bajo_calorías'],
      };
    }

    if (lowerMessage.includes('pescado')) {
      return {
        text: '🐟 **Tacos Saludables de Pescado**\n\n**Ingredientes (2 tacos):**\n• 150g filete de pescado blanco\n• 2 tortillas de maíz\n• 1 taza repollo morado\n• ½ aguacate\n• Pico de gallo\n• Limón y cilantro\n\n**Preparación:**\n1. Sazona pescado con limón, ajo, comino\n2. Cocina a la plancha 4 min por lado\n3. Calienta tortillas\n4. Sirve con repollo, aguacate y pico de gallo\n\n**Información Nutricional:**\n• 420 kcal | 35g proteína | 12g grasa\n• Omega-3: 850mg\n\n**Equivalencias:** 2 cereales + 2 carnes bajo grasa + 1 grasa',
        tags: ['pescado', 'alto_proteína', 'omega3'],
      };
    }

    if (lowerMessage.includes('ensalada') || lowerMessage.includes('nopales') || lowerMessage.includes('atún')) {
      return {
        text: '🥗 **Ensalada de Nopales y Atún**\n\n**Ingredientes (1 porción):**\n• 1 taza nopales cocidos\n• 120g atún en agua\n• 1 taza jitomate cherry\n• ½ cebolla morada\n• Cilantro fresco\n• Jugo de 1 limón\n• 1 cdta aceite de oliva\n\n**Preparación:**\n1. Corta nopales en cuadritos\n2. Mezcla con atún escurrido\n3. Agrega jitomates, cebolla, cilantro\n4. Aliña con limón y aceite\n\n**Información Nutricional:**\n• 280 kcal | 30g proteína | 6g grasa | 8g fibra\n\n**Beneficios:** Alta fibra, bajo en calorías, perfecto para perder peso',
        tags: ['ensalada', 'alto_fibra', 'bajo_calorías'],
      };
    }

    if (lowerMessage.includes('lactosa') || lowerMessage.includes('alternativa') || lowerMessage.includes('sin lactosa')) {
      return {
        text: '🥛 **Alternativas Sin Lactosa para Crema**\n\n**1. Crema de Anacardo**\n• Remojar 1 taza anacardos 4hrs\n• Licuar con ½ taza agua\n• Agregar limón al gusto\n→ Textura cremosa, 0% lactosa\n\n**2. Yogurt de Coco**\n• Natural y sin azúcar\n• Probióticos incluidos\n→ Sabor suave, muy cremoso\n\n**3. Aguacate Batido**\n• Licuar aguacate maduro\n• Agregar limón y sal\n→ Grasas saludables, rico en fibra\n\n**4. Tofu Sedoso Licuado**\n• Licuar con limón\n• Agregar hierbas frescas\n→ Alto en proteína\n\n**Todas son aptas para tu restricción de lactosa**',
        tags: ['sin_lactosa', 'alternativas'],
      };
    }

    return {
      text: '🤔 Puedo ayudarte con:\n\n• 📊 Análisis nutricional de platillos mexicanos\n• 🍽️ Recetas saludables tradicionales\n• 🔄 Equivalencias SMAE\n• 💡 Sustituciones para reducir calorías\n• 📋 Planificación de menús balanceados\n\n¿Sobre qué te gustaría saber?',
      tags: ['ayuda_general'],
    };
  };

  const handleSendMessage = () => {
    if (inputText.trim() === '') return;

    const userMessage = {
      id: messages.length + 1,
      sender: 'user',
      text: inputText,
      timestamp: new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages([...messages, userMessage]);
    setInputText('');
    setIsTyping(true);

    setTimeout(() => {
      const aiResponse = generateAIResponse(inputText);
      const botMessage = {
        id: messages.length + 2,
        sender: 'bot',
        text: aiResponse.text,
        tags: aiResponse.tags,
        timestamp: new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, botMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const handleQuickSuggestion = (text) => {
    setInputText(text);
    // Enviar automáticamente la sugerencia
    setTimeout(() => {
      const newMessage = {
        id: messages.length + 1,
        sender: 'user',
        text: text,
        timestamp: new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages([...messages, newMessage]);
      setInputText('');
      setIsTyping(true);

      // Simular respuesta de la IA
      setTimeout(() => {
        const aiResponse = generateAIResponse(text);
        const botMessage = {
          id: messages.length + 2,
          sender: 'bot',
          text: aiResponse.text,
          timestamp: new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }),
        };
        setMessages((prev) => [...prev, botMessage]);
        setIsTyping(false);
      }, 1500);
    }, 100);
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
