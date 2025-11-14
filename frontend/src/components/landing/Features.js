/**
 * Features Component - Landing Page
 * Displays main product features in a grid layout
 */
import React from 'react';
import { motion } from 'framer-motion';

const features = [
  {
    icon: '🔍',
    title: 'Escáner Inteligente NOM-051',
    description: 'Fortaleciendo la soberanía alimentaria con cada elección',
    points: [
      'Lee códigos de barras automáticamente',
      'Analiza sellos de advertencia NOM-051',
      'Compara con alternativas mexicanas saludables',
      'Prioriza productos locales y de Tiendas Bienestar',
    ],
    gradient: 'from-blue-500 to-blue-600',
  },
  {
    icon: '🌿',
    title: 'Plantas Medicinales Mexicanas',
    description: 'Descubre la medicina tradicional validada por UNAM',
    points: [
      '20+ plantas con evidencia científica',
      'Métodos de preparación tradicionales',
      'Información de seguridad y precauciones',
      'Basado en el Atlas de UNAM',
    ],
    gradient: 'from-green-500 to-emerald-600',
  },
  {
    icon: '🤖',
    title: 'Nutricionista Virtual 24/7',
    description: 'Consulta con IA entrenada en nutrición',
    points: [
      'Respuestas instantáneas basadas en ciencia',
      'Recomendaciones personalizadas',
      'Conversaciones naturales en español',
      'Acceso ilimitado sin citas',
    ],
    gradient: 'from-purple-500 to-purple-600',
  },
  {
    icon: '🍽️',
    title: 'Planes de Alimentación',
    description: 'Soberanía alimentaria en cada comida',
    points: [
      'Basado en Sistema SMAE',
      '56+ alimentos locales priorizados',
      'Identifica productos de Tiendas Bienestar',
      'Recetas con ingredientes nacionales',
    ],
    gradient: 'from-green-500 to-green-600',
  },
  {
    icon: '📊',
    title: 'Seguimiento de Progreso',
    description: 'Monitorea tu evolución',
    points: [
      'Registro de comidas',
      'Gráficas de nutrientes',
      'Historial completo',
      'Exporta reportes PDF',
    ],
    gradient: 'from-orange-500 to-orange-600',
  },
];

const Features = () => {
  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Todo lo que necesitas para mejorar tu nutrición
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Herramientas profesionales al alcance de tu mano, basadas en
            estándares mexicanos de nutrición
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.6 }}
              className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition group"
            >
              {/* Icon */}
              <div className="text-4xl mb-4 transform group-hover:scale-110 transition">
                {feature.icon}
              </div>

              {/* Title */}
              <h3 className="text-xl font-bold mb-2 text-gray-900">
                {feature.title}
              </h3>

              {/* Description */}
              <p className="text-gray-600 mb-4">{feature.description}</p>

              {/* Points List */}
              <ul className="space-y-2">
                {feature.points.map((point, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                    <svg
                      className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clipRule="evenodd"
                      />
                    </svg>
                    <span>{point}</span>
                  </li>
                ))}
              </ul>

              {/* Optional: Gradient indicator */}
              <div className={`h-1 w-full mt-4 rounded-full bg-gradient-to-r ${feature.gradient}`} />
            </motion.div>
          ))}
        </div>

        {/* Technology Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mt-20 bg-white rounded-2xl shadow-lg p-8"
        >
          <h3 className="text-2xl font-bold text-center mb-8 text-gray-900">
            Tecnología de vanguardia al servicio de tu salud
          </h3>

          <div className="grid md:grid-cols-3 lg:grid-cols-5 gap-6">
            <div className="flex flex-col items-center text-center">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-3">
                <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <p className="font-semibold text-sm">Inteligencia Artificial</p>
              <p className="text-xs text-gray-600">Powered by Gemini 1.5</p>
            </div>

            <div className="flex flex-col items-center text-center">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-3">
                <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <p className="font-semibold text-sm">Estándares Mexicanos</p>
              <p className="text-xs text-gray-600">100% NOM-051 y SMAE</p>
            </div>

            <div className="flex flex-col items-center text-center">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-3">
                <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <p className="font-semibold text-sm">Seguridad</p>
              <p className="text-xs text-gray-600">Datos encriptados</p>
            </div>

            <div className="flex flex-col items-center text-center">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-3">
                <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                </svg>
              </div>
              <p className="font-semibold text-sm">Rápido</p>
              <p className="text-xs text-gray-600">Respuesta &lt;2 seg</p>
            </div>

            <div className="flex flex-col items-center text-center">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-3">
                <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M3 12v3c0 1.657 3.134 3 7 3s7-1.343 7-3v-3c0 1.657-3.134 3-7 3s-7-1.343-7-3z" />
                  <path d="M3 7v3c0 1.657 3.134 3 7 3s7-1.343 7-3V7c0 1.657-3.134 3-7 3S3 8.657 3 7z" />
                  <path d="M17 5c0 1.657-3.134 3-7 3S3 6.657 3 5s3.134-3 7-3 7 1.343 7 3z" />
                </svg>
              </div>
              <p className="font-semibold text-sm">Multiplataforma</p>
              <p className="text-xs text-gray-600">Web, iOS, Android</p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Features;
