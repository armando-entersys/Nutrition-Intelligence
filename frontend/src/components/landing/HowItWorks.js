/**
 * HowItWorks Component - Landing Page
 * Displays the 3-step process
 */
import React from 'react';
import { motion } from 'framer-motion';

const steps = [
  {
    number: '1',
    icon: '📱',
    title: 'Descarga y Regístrate',
    description: 'Crea tu cuenta gratis en 2 minutos',
    details: 'Elige tu objetivo: bajar peso, ganar músculo, o salud general',
    color: 'bg-blue-500',
  },
  {
    number: '2',
    icon: '🎯',
    title: 'Usa las Herramientas',
    description: 'Accede a todas las funciones',
    details: 'Escanea productos, pregunta al nutricionista IA, crea tu plan de comidas',
    color: 'bg-purple-500',
  },
  {
    number: '3',
    icon: '📈',
    title: 'Ve tus Resultados',
    description: 'Monitorea tu progreso',
    details: 'Ajusta según necesites y alcanza tus metas de salud',
    color: 'bg-green-500',
  },
];

const HowItWorks = () => {
  return (
    <section className="py-20 bg-white">
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
            Tan fácil como 1, 2, 3
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Comienza tu viaje hacia una mejor nutrición en minutos
          </p>
        </motion.div>

        {/* Steps */}
        <div className="grid md:grid-cols-3 gap-8 relative">
          {/* Connection Lines (Desktop) */}
          <div className="hidden md:block absolute top-20 left-0 right-0 h-0.5 bg-gray-200" style={{ width: '66%', left: '17%' }} />

          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.2, duration: 0.6 }}
              className="relative"
            >
              {/* Step Card */}
              <div className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition relative z-10">
                {/* Number Badge */}
                <div className={`${step.color} text-white w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4 shadow-lg`}>
                  {step.number}
                </div>

                {/* Icon */}
                <div className="text-5xl text-center mb-4">
                  {step.icon}
                </div>

                {/* Title */}
                <h3 className="text-xl font-bold text-gray-900 text-center mb-2">
                  {step.title}
                </h3>

                {/* Description */}
                <p className="text-gray-600 text-center mb-3">
                  {step.description}
                </p>

                {/* Details */}
                <p className="text-sm text-gray-500 text-center">
                  {step.details}
                </p>
              </div>

              {/* Arrow (Desktop) */}
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-20 -right-4 transform translate-x-1/2 z-20">
                  <svg
                    className="w-8 h-8 text-gray-400"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                  </svg>
                </div>
              )}

              {/* Arrow (Mobile) */}
              {index < steps.length - 1 && (
                <div className="md:hidden flex justify-center my-4">
                  <svg
                    className="w-8 h-8 text-gray-400"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
                  </svg>
                </div>
              )}
            </motion.div>
          ))}
        </div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mt-16 text-center"
        >
          <a
            href="/auth/register"
            className="inline-block px-8 py-4 bg-green-600 text-white rounded-lg
                     hover:bg-green-700 transition font-semibold text-lg
                     shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
          >
            Empezar Ahora - Es Gratis
          </a>
          <p className="mt-4 text-sm text-gray-500">
            No se requiere tarjeta de crédito
          </p>
        </motion.div>

        {/* Stats Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mt-20 grid grid-cols-2 md:grid-cols-5 gap-6"
        >
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600 mb-1">56+</div>
            <div className="text-sm text-gray-600">Alimentos SMAE</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600 mb-1">28+</div>
            <div className="text-sm text-gray-600">Productos NOM-051</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600 mb-1">1,000+</div>
            <div className="text-sm text-gray-600">Consultas IA</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600 mb-1">95%</div>
            <div className="text-sm text-gray-600">Satisfacción</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600 mb-1">&lt;2s</div>
            <div className="text-sm text-gray-600">Tiempo respuesta</div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default HowItWorks;
