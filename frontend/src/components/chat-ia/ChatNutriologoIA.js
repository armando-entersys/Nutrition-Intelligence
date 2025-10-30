import React, { useState, useRef, useEffect } from 'react';
import { Container, Box, Typography, Card, CardContent, TextField, Button, Avatar, Chip, IconButton, List, ListItem, ListItemAvatar, ListItemText, Paper, Grid, Divider } from '@mui/material';
import { Send, SmartToy, Person, Restaurant, Psychology, LocalFireDepartment, Fastfood, LightbulbOutlined, TipsAndUpdates } from '@mui/icons-material';
import { motion } from 'framer-motion';

const ChatNutriologoIA = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: '¡Hola! Soy tu Nutriólogo Virtual con IA. 🇲🇽 Estoy especializado en nutrición mexicana y puedo ayudarte con:',
      timestamp: new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }),
    },
    {
      id: 2,
      sender: 'bot',
      text: '• Responder preguntas sobre alimentos mexicanos\n• Sugerir recetas saludables\n• Calcular calorías y macros\n• Recomendar sustituciones de alimentos\n• Explicar el Sistema Mexicano de Alimentos Equivalentes',
      timestamp: new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Sugerencias rápidas
  const quickSuggestions = [
    { icon: <Restaurant />, text: '¿Cuántas calorías tienen 3 tacos al pastor?', color: '#FF6B35' },
    { icon: <Fastfood />, text: 'Recetas mexicanas saludables con frijol', color: '#4CAF50' },
    { icon: <LocalFireDepartment />, text: '¿Cómo hacer tortillas más saludables?', color: '#FF9800' },
    { icon: <TipsAndUpdates />, text: 'Sustitutos saludables para la crema', color: '#2196F3' },
  ];

  // Respuestas mock de la IA
  const generateAIResponse = (userMessage) => {
    const lowerMessage = userMessage.toLowerCase();

    // Base de conocimiento mexicana
    if (lowerMessage.includes('tacos') || lowerMessage.includes('taco')) {
      return {
        text: 'Los tacos son parte fundamental de la dieta mexicana. 🌮\n\n**Análisis Nutricional (3 tacos al pastor):**\n\n• Calorías: ~680 kcal\n• Proteína: 35g\n• Carbohidratos: 75g\n• Grasas: 22g\n\n**Recomendaciones para hacerlos más saludables:**\n\n1. Usa tortilla de maíz (no harina) - más fibra y menor índice glucémico\n2. Reduce la carne a 120g en lugar de 180g (-50 kcal)\n3. Agrega más verduras: cebolla, cilantro, nopales, pico de gallo\n4. Limita el consumo a 2-3 tacos por comida\n5. Acompaña con frijoles de la olla (sin manteca)\n\n¿Te gustaría una receta específica de tacos saludables?',
        tags: ['alto_proteina', 'tradicional_mexicano', 'mejorable'],
      };
    }

    if (lowerMessage.includes('frijol') || lowerMessage.includes('frijoles')) {
      return {
        text: 'Los frijoles son una **leguminosa estrella** de la cocina mexicana. 🫘\n\n**Beneficios nutricionales:**\n\n• Alto en proteína vegetal (15g/taza)\n• Rico en fibra soluble (15g/taza)\n• Fuente de hierro, magnesio y potasio\n• Bajo índice glucémico\n• Excelente para control de peso\n\n**Recetas saludables con frijol:**\n\n1. **Frijoles de la olla** - Sin manteca, solo con epazote\n2. **Sopa de frijol negro** - Con chile guajillo y aguacate\n3. **Enfrijoladas** - Con tortilla de maíz y queso panela\n4. **Tostadas de frijol con nopales** - Alta fibra\n\n**Equivalencia SMAE:** 1 taza de frijoles = 2 equivalentes de leguminosas',
        tags: ['alto_fibra', 'proteina_vegetal', 'tradicional'],
      };
    }

    if (lowerMessage.includes('tortilla')) {
      return {
        text: 'La tortilla es la base de la alimentación mexicana. 🌽\n\n**Comparación Nutricional:**\n\n**Tortilla de Maíz (1 pieza, 30g):**\n• Calorías: 64 kcal\n• Carbohidratos: 13g\n• Proteína: 1.5g\n• Fibra: 1.5g\n• Índice glucémico: Medio (52)\n\n**Tortilla de Harina (1 pieza, 40g):**\n• Calorías: 104 kcal\n• Carbohidratos: 18g\n• Proteína: 3g\n• Fibra: 1g\n• Índice glucémico: Alto (70)\n\n**Recomendación:** Prefiere tortilla de maíz nixtamalizado. Es más nutritiva, tiene más calcio biodisponible y fibra.\n\n**Alternativas más saludables:**\n• Tortilla de maíz azul (más antioxidantes)\n• Tortilla integral\n• Tortilla de nopal (baja en calorías)\n\n¿Te gustaría saber cómo hacer tortillas caseras?',
        tags: ['cereal', 'tradicional', 'indice_glucemico'],
      };
    }

    if (lowerMessage.includes('crema') || lowerMessage.includes('sustituto')) {
      return {
        text: '¡Excelente pregunta sobre sustituciones! 💡\n\n**Sustitutos saludables para la crema:**\n\n1. **Yogurt griego natural** (0% grasa)\n   - 90% menos grasa\n   - Alto en proteína\n   - Textura similar\n\n2. **Jocoque**\n   - Tradicional mexicano\n   - Bajo en grasa\n   - Probióticos naturales\n\n3. **Aguacate machacado**\n   - Grasas saludables (omega-3)\n   - Cremoso\n   - Alto en fibra\n\n4. **Queso cottage licuado** con limón\n   - Alto en proteína\n   - Bajo en grasa\n   - Textura cremosa\n\n**Equivalencias SMAE:**\n• 2 cdas de crema = 1 grasa con proteína\n• 2 cdas yogurt griego = 1/2 leche descremada\n• 1/4 aguacate = 1 grasa\n\n¿Necesitas más sustituciones para otros ingredientes?',
        tags: ['sustitucion', 'bajo_grasa', 'saludable'],
      };
    }

    if (lowerMessage.includes('receta')) {
      return {
        text: 'Te comparto una receta tradicional mexicana saludable: 👨‍🍳\n\n**CHILAQUILES VERDES SALUDABLES**\n\n**Ingredientes (4 porciones):**\n• 8 tortillas de maíz (horneadas, no fritas)\n• 2 tazas de salsa verde casera\n• 1 pechuga de pollo deshebrada\n• 1/2 taza de cebolla morada\n• 1/4 taza de queso panela\n• 2 cdas de crema light\n• Cilantro fresco\n\n**Preparación:**\n1. Corta las tortillas en triángulos y hornéalas a 180°C por 15 min hasta que estén crujientes\n2. Prepara salsa verde licuando tomates verdes, chile serrano, cebolla y cilantro\n3. Calienta la salsa y agrega las tortillas horneadas\n4. Sirve con pollo deshebrado, cebolla, queso y crema\n\n**Info Nutricional (por porción):**\n• Calorías: 320 kcal\n• Proteína: 25g\n• Carbohidratos: 38g\n• Grasas: 8g\n\n**Equivalencias:** 2 cereales + 1 verdura + 2 carnes bajo aporte\n\n¿Te gustaría más recetas mexicanas saludables?',
        tags: ['receta', 'tradicional', 'alto_proteina'],
      };
    }

    // Respuesta por defecto
    return {
      text: 'Entiendo tu pregunta. 🤔 Como Nutriólogo Virtual especializado en comida mexicana, puedo ayudarte con:\n\n• **Análisis nutricional** de platillos mexicanos\n• **Recetas saludables** con ingredientes tradicionales\n• **Equivalencias de alimentos** según SMAE\n• **Sustituciones saludables** para reducir calorías\n• **Planificación de menús** mexicanos balanceados\n\n¿Sobre qué te gustaría saber más? Puedes preguntarme sobre tacos, tamales, moles, frijoles, tortillas, o cualquier platillo mexicano.',
      tags: ['ayuda_general'],
    };
  };

  const handleSendMessage = () => {
    if (inputText.trim() === '') return;

    // Agregar mensaje del usuario
    const userMessage = {
      id: messages.length + 1,
      sender: 'user',
      text: inputText,
      timestamp: new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages([...messages, userMessage]);
    setInputText('');
    setIsTyping(true);

    // Simular respuesta de la IA con delay
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
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4, height: 'calc(100vh - 120px)' }}>
      <Grid container spacing={3} sx={{ height: '100%' }}>
        {/* Panel principal del chat */}
        <Grid item xs={12} md={8} sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
          {/* Header */}
          <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
            <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', borderRadius: 4, mb: 2 }}>
              <CardContent sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Avatar sx={{ width: 56, height: 56, bgcolor: 'rgba(255,255,255,0.2)' }}>
                    <Psychology sx={{ fontSize: 32 }} />
                  </Avatar>
                  <Box>
                    <Typography variant="h5" fontWeight="700">Chat con Nutriólogo Virtual IA</Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 0.5 }}>
                      <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: '#4CAF50' }} />
                      <Typography variant="body2">En línea • Disponible 24/7</Typography>
                    </Box>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </motion.div>

          {/* Área de mensajes */}
          <Card sx={{ flex: 1, display: 'flex', flexDirection: 'column', borderRadius: 4, overflow: 'hidden' }}>
            <Box sx={{ flex: 1, overflowY: 'auto', p: 3, bgcolor: '#F5F5F5' }}>
              <List>
                {messages.map((message, index) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, x: message.sender === 'user' ? 20 : -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.05 }}
                  >
                    <ListItem
                      sx={{
                        display: 'flex',
                        justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                        mb: 2,
                        p: 0,
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1, maxWidth: '80%', flexDirection: message.sender === 'user' ? 'row-reverse' : 'row' }}>
                        <Avatar sx={{ bgcolor: message.sender === 'user' ? '#2196F3' : '#667eea', width: 36, height: 36 }}>
                          {message.sender === 'user' ? <Person /> : <SmartToy />}
                        </Avatar>
                        <Paper
                          sx={{
                            p: 2,
                            bgcolor: message.sender === 'user' ? '#2196F3' : 'white',
                            color: message.sender === 'user' ? 'white' : 'text.primary',
                            borderRadius: 3,
                            boxShadow: 2,
                          }}
                        >
                          <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', mb: 1 }}>{message.text}</Typography>
                          {message.tags && (
                            <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap', mt: 1 }}>
                              {message.tags.map((tag, idx) => (
                                <Chip key={idx} label={tag} size="small" sx={{ bgcolor: 'rgba(102, 126, 234, 0.1)', color: '#667eea', height: 20, fontSize: '0.7rem' }} />
                              ))}
                            </Box>
                          )}
                          <Typography variant="caption" sx={{ display: 'block', mt: 0.5, opacity: 0.7, textAlign: message.sender === 'user' ? 'right' : 'left' }}>
                            {message.timestamp}
                          </Typography>
                        </Paper>
                      </Box>
                    </ListItem>
                  </motion.div>
                ))}

                {isTyping && (
                  <ListItem sx={{ justifyContent: 'flex-start', p: 0 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Avatar sx={{ bgcolor: '#667eea', width: 36, height: 36 }}>
                        <SmartToy />
                      </Avatar>
                      <Paper sx={{ p: 2, bgcolor: 'white', borderRadius: 3, boxShadow: 2 }}>
                        <Box sx={{ display: 'flex', gap: 0.5 }}>
                          <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: '#667eea', animation: 'pulse 1.4s infinite', animationDelay: '0s' }} />
                          <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: '#667eea', animation: 'pulse 1.4s infinite', animationDelay: '0.2s' }} />
                          <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: '#667eea', animation: 'pulse 1.4s infinite', animationDelay: '0.4s' }} />
                        </Box>
                      </Paper>
                    </Box>
                  </ListItem>
                )}
                <div ref={messagesEndRef} />
              </List>
            </Box>

            {/* Input de mensaje */}
            <Divider />
            <Box sx={{ p: 2, bgcolor: 'white' }}>
              <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-end' }}>
                <TextField
                  fullWidth
                  multiline
                  maxRows={3}
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Escribe tu pregunta sobre nutrición mexicana..."
                  variant="outlined"
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      borderRadius: 3,
                    },
                  }}
                />
                <Button
                  variant="contained"
                  onClick={handleSendMessage}
                  disabled={inputText.trim() === ''}
                  sx={{
                    minWidth: 56,
                    height: 56,
                    borderRadius: 3,
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  }}
                >
                  <Send />
                </Button>
              </Box>
            </Box>
          </Card>
        </Grid>

        {/* Panel lateral con sugerencias y tips */}
        <Grid item xs={12} md={4} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {/* Sugerencias rápidas */}
          <Card sx={{ borderRadius: 4 }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <LightbulbOutlined sx={{ color: '#FF9800' }} />
                <Typography variant="h6" fontWeight="700">Sugerencias Rápidas</Typography>
              </Box>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                {quickSuggestions.map((suggestion, idx) => (
                  <Button
                    key={idx}
                    variant="outlined"
                    onClick={() => handleQuickSuggestion(suggestion.text)}
                    sx={{
                      justifyContent: 'flex-start',
                      textAlign: 'left',
                      borderRadius: 2,
                      p: 1.5,
                      borderColor: suggestion.color,
                      color: suggestion.color,
                      textTransform: 'none',
                      '&:hover': {
                        borderColor: suggestion.color,
                        bgcolor: `${suggestion.color}15`,
                      },
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {suggestion.icon}
                      <Typography variant="body2" fontWeight="500">{suggestion.text}</Typography>
                    </Box>
                  </Button>
                ))}
              </Box>
            </CardContent>
          </Card>

          {/* Capacidades del bot */}
          <Card sx={{ borderRadius: 4 }}>
            <CardContent>
              <Typography variant="h6" fontWeight="700" gutterBottom>Capacidades del Asistente</Typography>
              <List dense>
                <ListItem>
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: '#4CAF50', width: 32, height: 32 }}>
                      <Restaurant sx={{ fontSize: 18 }} />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText primary="Análisis Nutricional" secondary="Calcula macros y calorías de platillos mexicanos" />
                </ListItem>
                <ListItem>
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: '#FF6B35', width: 32, height: 32 }}>
                      <Fastfood sx={{ fontSize: 18 }} />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText primary="Recetas Saludables" secondary="Versiones nutritivas de platillos tradicionales" />
                </ListItem>
                <ListItem>
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: '#2196F3', width: 32, height: 32 }}>
                      <TipsAndUpdates sx={{ fontSize: 18 }} />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText primary="Sustituciones" secondary="Alternativas saludables para ingredientes" />
                </ListItem>
                <ListItem>
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: '#9C27B0', width: 32, height: 32 }}>
                      <Psychology sx={{ fontSize: 18 }} />
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText primary="Equivalencias SMAE" secondary="Sistema Mexicano de Alimentos Equivalentes" />
                </ListItem>
              </List>
            </CardContent>
          </Card>

          {/* Tips nutricionales */}
          <Card sx={{ borderRadius: 4, background: 'linear-gradient(135deg, #FF6B35 0%, #FF9800 100%)', color: 'white' }}>
            <CardContent>
              <Typography variant="h6" fontWeight="700" gutterBottom>💡 Tip del Día</Typography>
              <Typography variant="body2">
                Los frijoles negros son ricos en antioxidantes llamados antocianinas. Consúmelos de la olla sin manteca para aprovechar todos sus beneficios. 1 taza = 15g de proteína vegetal + 15g de fibra.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 0.3; transform: scale(0.8); }
          50% { opacity: 1; transform: scale(1.2); }
        }
      `}</style>
    </Container>
  );
};

export default ChatNutriologoIA;
