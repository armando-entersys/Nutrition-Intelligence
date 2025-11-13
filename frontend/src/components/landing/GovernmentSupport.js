/**
 * Government Support Component - Landing Page
 * Shows government initiatives we support
 */
import React from 'react';
import { motion } from 'framer-motion';

const initiatives = [
  {
    icon: '🏪',
    title: 'Alimentación para el Bienestar',
    description: '25,600 Tiendas Bienestar',
    details: [
      'Catálogo de productos marca Bienestar',
      'Mapa de tiendas cercanas',
      'Productos nacionales a precios justos',
      'Maíz, frijol, arroz, cacao, café, miel'
    ],
    color: 'from-green-500 to-green-600'
  },
  {
    icon: '🇲🇽',
    title: 'Soberanía Alimentaria',
    description: 'Apoyo a productores nacionales',
    details: [
      'Productos 100% mexicanos identificados',
      'Información de origen por estado',
      'Sin intermediarios',
      'Apoyo a pequeños productores'
    ],
    color: 'from-red-500 to-red-600'
  },
  {
    icon: '🏷️',
    title: 'NOM-051 Fase 3',
    description: 'Etiquetado más estricto',
    details: [
      'Criterios actualizados octubre 2025',
      'Educación sobre sellos de advertencia',
      'Comparación transparente de productos',
      'Decisiones informadas'
    ],
    color: 'from-orange-500 to-orange-600'
  },
  {
    icon: '🏫',
    title: 'Lineamientos Escolares',
    description: 'Cafeterías saludables',
    details: [
      'Sistema para escuelas (vigente marzo 2025)',
      'Menús certificados saludables',
      'Productos regionales en escuelas',
      'Educación nutricional para niños'
    ],
    color: 'from-blue-500 to-blue-600'
  }
];

const GovernmentSupport = () => {
  return (
    <section className="py-20 bg-gradient-to-br from-green-50 via-white to-green-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center gap-3 bg-white rounded-full px-6 py-3 shadow-md mb-6">
            <span className="text-3xl">🇲🇽</span>
            <span className="font-bold text-gray-900">Gobierno de México</span>
          </div>

          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Apoyando Iniciativas Presidenciales
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Alineados con las políticas de nutrición y alimentación de la
            <span className="font-semibold text-green-600"> Presidenta Claudia Sheinbaum</span>
          </p>
        </motion.div>

        {/* Initiatives Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {initiatives.map((initiative, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.6 }}
              className="bg-white rounded-xl shadow-lg hover:shadow-xl transition overflow-hidden"
            >
              {/* Header with gradient */}
              <div className={`bg-gradient-to-r ${initiative.color} p-6 text-white`}>
                <div className="text-5xl mb-3">{initiative.icon}</div>
                <h3 className="text-xl font-bold mb-1">{initiative.title}</h3>
                <p className="text-sm opacity-90">{initiative.description}</p>
              </div>

              {/* Content */}
              <div className="p-6">
                <ul className="space-y-2">
                  {initiative.details.map((detail, i) => (
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
                      <span>{detail}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Impact Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mt-16 bg-white rounded-2xl shadow-lg p-8"
        >
          <h3 className="text-2xl font-bold text-center mb-8 text-gray-900">
            Impacto en México
          </h3>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">25,600</div>
              <div className="text-sm text-gray-600">Tiendas Bienestar<br/>a nivel nacional</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">56+</div>
              <div className="text-sm text-gray-600">Alimentos SMAE<br/>catalogados</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">100%</div>
              <div className="text-sm text-gray-600">NOM-051 Fase 3<br/>compliant</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">1M+</div>
              <div className="text-sm text-gray-600">Meta usuarios<br/>impactados</div>
            </div>
          </div>
        </motion.div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mt-12 text-center"
        >
          <p className="text-gray-600 mb-4">
            Juntos por un México más saludable y soberano
          </p>
          <a
            href="/auth/register"
            className="inline-block px-8 py-4 bg-green-600 text-white rounded-lg
                     hover:bg-green-700 transition font-semibold text-lg
                     shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
          >
            Únete al Movimiento
          </a>
        </motion.div>
      </div>
    </section>
  );
};

export default GovernmentSupport;
