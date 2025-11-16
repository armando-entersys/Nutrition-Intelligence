/**
 * Hero Component - Landing Page
 * Main hero section with CTA buttons
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { trackSignup } from '../../utils/analytics';

const Hero = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    trackSignup('landing_hero');
    navigate('/auth/register');
  };

  const handleWatchDemo = () => {
    // Scroll to demo video section or open modal
    const demoSection = document.getElementById('demo-video');
    if (demoSection) {
      demoSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="relative min-h-screen flex items-center bg-gradient-to-br from-green-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Column - Content */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              Tu Nutricionista
              <span className="text-green-600"> Inteligente</span>
              <br />
              en México
            </h1>

            <p className="text-xl text-gray-600 mb-6">
              Escanea productos, crea planes personalizados, explora plantas medicinales
              y consulta con IA. Todo basado en estándares mexicanos y sabiduría ancestral.
            </p>

            {/* Mexican Food Sovereignty Badge */}
            <div className="mb-6 inline-flex items-center gap-2 bg-green-50 border-2 border-green-600 rounded-full px-4 py-2">
              <span className="text-2xl">🇲🇽</span>
              <span className="text-sm font-semibold text-green-800">
                Promoviendo la soberanía alimentaria mexicana
              </span>
            </div>

            {/* Mexican Wisdom Badge */}
            <div className="mb-8 bg-gradient-to-r from-purple-50 to-indigo-50 border-2 border-purple-300 rounded-xl px-5 py-3">
              <p className="text-xs text-purple-700 leading-relaxed">
                🌟 Una plataforma que honra la sabiduría mexicana: comunicación clara,
                respeto mutuo, transparencia y excelencia en cada interacción.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 mt-8">
              <button
                onClick={handleGetStarted}
                className="px-8 py-4 bg-green-600 text-white rounded-lg
                         hover:bg-green-700 transition font-semibold text-lg
                         shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                Empezar Gratis
              </button>

              <button
                onClick={handleWatchDemo}
                className="px-8 py-4 border-2 border-green-600 text-green-600
                         rounded-lg hover:bg-green-50 transition font-semibold text-lg"
              >
                Ver Demo
              </button>
            </div>

            {/* Trust Indicators */}
            <div className="mt-8 flex flex-col sm:flex-row gap-6 text-sm text-gray-500">
              <div className="flex items-center gap-2">
                <svg
                  className="w-5 h-5 text-green-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                <span>Gratis para siempre</span>
              </div>
              <div className="flex items-center gap-2">
                <svg
                  className="w-5 h-5 text-green-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                <span>Sin tarjeta de crédito</span>
              </div>
              <div className="flex items-center gap-2">
                <svg
                  className="w-5 h-5 text-green-600"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                <span>Datos seguros</span>
              </div>
            </div>
          </motion.div>

          {/* Right Column - Hero Image/Animation */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="relative">
              {/* Placeholder for app mockup - can be replaced with actual image */}
              <div className="bg-gradient-to-br from-green-100 to-green-200 rounded-3xl shadow-2xl p-8 h-[500px] flex items-center justify-center">
                <div className="text-center">
                  <div className="text-6xl mb-4">📱</div>
                  <p className="text-gray-700 font-semibold">
                    App Screenshot
                  </p>
                  <p className="text-sm text-gray-600 mt-2">
                    Escaneo de productos con NOM-051
                  </p>
                </div>
              </div>

              {/* Floating animated elements */}
              <motion.div
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute top-10 -right-10 hidden lg:block"
              >
                <div className="bg-white rounded-lg shadow-xl p-4 max-w-[200px]">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center text-white font-bold">
                      !
                    </div>
                    <span className="font-semibold text-sm">Exceso Azúcares</span>
                  </div>
                </div>
              </motion.div>

              <motion.div
                animate={{ y: [0, 10, 0] }}
                transition={{ duration: 2.5, repeat: Infinity, delay: 0.5 }}
                className="absolute bottom-10 -left-10 hidden lg:block"
              >
                <div className="bg-white rounded-lg shadow-xl p-4 max-w-[200px]">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white">
                      ✓
                    </div>
                    <span className="font-semibold text-sm">Plan Creado</span>
                  </div>
                </div>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        animate={{ y: [0, 10, 0] }}
        transition={{ duration: 1.5, repeat: Infinity }}
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
      >
        <svg
          className="w-6 h-6 text-gray-400"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
        </svg>
      </motion.div>
    </section>
  );
};

export default Hero;
