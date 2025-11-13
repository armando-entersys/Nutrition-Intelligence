/**
 * Pricing Component - Landing Page
 * Displays pricing plans
 */
import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const plans = [
  {
    name: 'Gratis',
    price: '$0',
    period: 'para siempre',
    description: 'Perfecto para comenzar tu viaje de nutrición',
    features: [
      { text: 'Escaneo ilimitado de productos', included: true },
      { text: '10 consultas IA por mes', included: true },
      { text: 'Calculadora nutricional', included: true },
      { text: 'Base de datos SMAE completa', included: true },
      { text: 'Planes de alimentación limitados', included: false },
      { text: 'Exportar PDF', included: false },
    ],
    cta: 'Empezar Gratis',
    popular: false,
    color: 'border-gray-300',
    buttonColor: 'bg-gray-600 hover:bg-gray-700',
  },
  {
    name: 'Premium',
    price: '$99',
    period: 'MXN/mes',
    description: 'Para usuarios serios sobre su salud',
    features: [
      { text: 'Todo lo del plan gratuito', included: true },
      { text: 'Consultas IA ilimitadas', included: true },
      { text: 'Planes de alimentación ilimitados', included: true },
      { text: 'Exportar a PDF', included: true },
      { text: 'Seguimiento avanzado', included: true },
      { text: 'Recetas exclusivas', included: true },
      { text: 'Soporte prioritario', included: true },
    ],
    cta: 'Prueba 14 días gratis',
    popular: true,
    color: 'border-green-500 ring-2 ring-green-500',
    buttonColor: 'bg-green-600 hover:bg-green-700',
  },
  {
    name: 'Profesional',
    price: '$499',
    period: 'MXN/mes',
    description: 'Para nutriólogos y profesionales de la salud',
    features: [
      { text: 'Todo lo de Premium', included: true },
      { text: 'Hasta 50 pacientes', included: true },
      { text: 'Dashboard profesional', included: true },
      { text: 'Marca blanca', included: true },
      { text: 'API access', included: true },
      { text: 'Capacitación incluida', included: true },
      { text: 'Soporte dedicado', included: true },
    ],
    cta: 'Solicitar Demo',
    popular: false,
    color: 'border-purple-300',
    buttonColor: 'bg-purple-600 hover:bg-purple-700',
  },
];

const Pricing = () => {
  const navigate = useNavigate();

  const handlePlanClick = (plan) => {
    if (plan.name === 'Profesional') {
      // Open contact form or email
      window.location.href = 'mailto:contacto@nutrition-intelligence.com?subject=Demo Profesional';
    } else {
      navigate('/auth/register');
    }
  };

  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-white">
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
            Planes para todos
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Elige el plan que mejor se adapte a tus necesidades. Todos incluyen garantía de satisfacción.
          </p>
        </motion.div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1, duration: 0.6 }}
              className={`relative bg-white rounded-2xl shadow-lg ${plan.color} border-2 p-8 hover:shadow-xl transition ${
                plan.popular ? 'transform md:-translate-y-2' : ''
              }`}
            >
              {/* Popular Badge */}
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-green-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                    Más Popular
                  </span>
                </div>
              )}

              {/* Plan Name */}
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                {plan.name}
              </h3>

              {/* Price */}
              <div className="mb-4">
                <span className="text-5xl font-bold text-gray-900">{plan.price}</span>
                <span className="text-gray-600 ml-2">{plan.period}</span>
              </div>

              {/* Description */}
              <p className="text-gray-600 mb-6">{plan.description}</p>

              {/* CTA Button */}
              <button
                onClick={() => handlePlanClick(plan)}
                className={`w-full ${plan.buttonColor} text-white py-3 rounded-lg font-semibold mb-6 transition shadow-md hover:shadow-lg`}
              >
                {plan.cta}
              </button>

              {/* Features List */}
              <ul className="space-y-3">
                {plan.features.map((feature, i) => (
                  <li key={i} className="flex items-start gap-2">
                    {feature.included ? (
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
                    ) : (
                      <svg
                        className="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                          clipRule="evenodd"
                        />
                      </svg>
                    )}
                    <span className={feature.included ? 'text-gray-700' : 'text-gray-400'}>
                      {feature.text}
                    </span>
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>

        {/* FAQ Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mt-20 max-w-3xl mx-auto"
        >
          <h3 className="text-2xl font-bold text-center mb-8 text-gray-900">
            Preguntas Frecuentes
          </h3>

          <div className="space-y-4">
            <details className="bg-white rounded-lg p-6 shadow-sm">
              <summary className="font-semibold text-gray-900 cursor-pointer">
                ¿Puedo cambiar de plan después?
              </summary>
              <p className="mt-2 text-gray-600">
                Sí, puedes actualizar o degradar tu plan en cualquier momento desde tu cuenta.
              </p>
            </details>

            <details className="bg-white rounded-lg p-6 shadow-sm">
              <summary className="font-semibold text-gray-900 cursor-pointer">
                ¿Cómo funciona la prueba gratuita de Premium?
              </summary>
              <p className="mt-2 text-gray-600">
                Tienes 14 días para probar Premium sin costo. Puedes cancelar antes de que termine sin cargo alguno.
              </p>
            </details>

            <details className="bg-white rounded-lg p-6 shadow-sm">
              <summary className="font-semibold text-gray-900 cursor-pointer">
                ¿Qué métodos de pago aceptan?
              </summary>
              <p className="mt-2 text-gray-600">
                Aceptamos todas las tarjetas de crédito/débito principales y transferencias bancarias para el plan profesional.
              </p>
            </details>

            <details className="bg-white rounded-lg p-6 shadow-sm">
              <summary className="font-semibold text-gray-900 cursor-pointer">
                ¿Ofrecen descuentos para estudiantes o instituciones?
              </summary>
              <p className="mt-2 text-gray-600">
                Sí, ofrecemos descuentos especiales para estudiantes de nutrición y para instituciones educativas. Contáctanos para más información.
              </p>
            </details>
          </div>
        </motion.div>

        {/* Trust Badges */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mt-16 flex flex-wrap justify-center gap-8 items-center text-gray-500"
        >
          <div className="flex items-center gap-2">
            <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span className="text-sm">Datos Seguros</span>
          </div>
          <div className="flex items-center gap-2">
            <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span className="text-sm">Hecho en México</span>
          </div>
          <div className="flex items-center gap-2">
            <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span className="text-sm">Garantía de Satisfacción</span>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Pricing;
