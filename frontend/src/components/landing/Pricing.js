/**
 * Pricing Component - Landing Page
 * Displays separate pricing for Patients (free social network) and Nutritionists (professional)
 */
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const Pricing = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('patients');

  const handlePatientSignup = () => {
    navigate('/auth/register');
  };

  const handleNutritionistDemo = () => {
    window.location.href = 'mailto:contacto@nutrition-intelligence.com?subject=Demo Profesional para Nutriólogos';
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
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Planes Diseñados para Ti
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Para pacientes que buscan salud, o para nutriólogos que transforman vidas
          </p>

          {/* Tab Selector */}
          <div className="inline-flex bg-white rounded-lg shadow-md p-1">
            <button
              onClick={() => setActiveTab('patients')}
              className={`px-8 py-3 rounded-lg font-semibold transition ${
                activeTab === 'patients'
                  ? 'bg-green-600 text-white'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Para Pacientes
            </button>
            <button
              onClick={() => setActiveTab('nutritionists')}
              className={`px-8 py-3 rounded-lg font-semibold transition ${
                activeTab === 'nutritionists'
                  ? 'bg-purple-600 text-white'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Para Nutriólogos
            </button>
          </div>
        </motion.div>

        {/* Patients Plan - FREE SOCIAL NETWORK */}
        {activeTab === 'patients' && (
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.4 }}
            className="max-w-4xl mx-auto"
          >
            <div className="bg-gradient-to-br from-green-50 to-white rounded-3xl shadow-2xl border-4 border-green-500 p-10 relative overflow-hidden">
              {/* Background decoration */}
              <div className="absolute top-0 right-0 w-64 h-64 bg-green-100 rounded-full -mr-32 -mt-32 opacity-50" />
              <div className="absolute bottom-0 left-0 w-48 h-48 bg-green-200 rounded-full -ml-24 -mb-24 opacity-50" />

              <div className="relative">
                {/* Free Badge */}
                <div className="inline-flex items-center gap-2 bg-green-600 text-white px-6 py-3 rounded-full mb-6 shadow-lg">
                  <span className="text-2xl">🎉</span>
                  <span className="font-bold text-lg">100% GRATIS PARA SIEMPRE</span>
                </div>

                <h3 className="text-4xl font-bold text-gray-900 mb-2">
                  Calpulli de Nutrición
                </h3>
                <p className="text-xl text-gray-600 mb-8">
                  Todo lo que necesitas para cuidar tu salud, conectar con tu comunidad y transformar tu alimentación
                </p>

                {/* Feature Grid */}
                <div className="grid md:grid-cols-2 gap-6 mb-8">
                  {/* Column 1 */}
                  <div className="space-y-4">
                    <h4 className="font-bold text-lg text-green-700 mb-3 flex items-center gap-2">
                      <span className="text-2xl">🔥</span>
                      Herramientas Inteligentes
                    </h4>
                    <FeatureItem text="Escaneo ilimitado de productos NOM-051" />
                    <FeatureItem text="Consultas IA ilimitadas con nutricionista virtual" />
                    <FeatureItem text="Planes de alimentación personalizados ilimitados" />
                    <FeatureItem text="Calculadora nutricional completa" />
                    <FeatureItem text="Base de datos SMAE completa (56+ alimentos)" />
                    <FeatureItem text="Análisis de fotos de comidas con IA" />
                    <FeatureItem text="Exportar reportes en PDF" />
                  </div>

                  {/* Column 2 */}
                  <div className="space-y-4">
                    <h4 className="font-bold text-lg text-green-700 mb-3 flex items-center gap-2">
                      <span className="text-2xl">🌟</span>
                      Red Social & Comunidad
                    </h4>
                    <FeatureItem text="Comparte tu progreso con la comunidad" />
                    <FeatureItem text="Sigue a nutriólogos profesionales" />
                    <FeatureItem text="Descubre recetas de otros usuarios" />
                    <FeatureItem text="Sistema de gamificación y logros" />
                    <FeatureItem text="Grupos de apoyo por objetivos" />
                    <FeatureItem text="Recordatorio de comidas y agua" />
                    <FeatureItem text="Seguimiento completo de progreso" />
                  </div>
                </div>

                {/* Why Free Section */}
                <div className="bg-white bg-opacity-80 rounded-xl p-6 mb-8 border-2 border-green-200">
                  <h4 className="font-bold text-lg text-gray-900 mb-3">
                    ¿Por qué es gratis para pacientes?
                  </h4>
                  <p className="text-gray-700">
                    Creemos que <strong>la salud es un derecho</strong>, no un privilegio. Nuestra misión es
                    empoderar a cada mexicano con las herramientas para tomar decisiones alimentarias
                    informadas, apoyar productos locales y construir una comunidad saludable.
                  </p>
                </div>

                {/* CTA Button */}
                <button
                  onClick={handlePatientSignup}
                  className="w-full bg-green-600 hover:bg-green-700 text-white py-5 rounded-xl
                           font-bold text-xl transition shadow-xl hover:shadow-2xl transform hover:-translate-y-1
                           flex items-center justify-center gap-3"
                >
                  <span>Únete Gratis Ahora</span>
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </button>

                <p className="text-center text-gray-500 mt-4 text-sm">
                  Sin tarjeta de crédito • Sin límites • Sin trucos
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Nutritionists Plans - 3 TIERS */}
        {activeTab === 'nutritionists' && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.4 }}
            className="max-w-7xl mx-auto"
          >
            <div className="grid md:grid-cols-3 gap-6">
              {/* PLAN STARTER - GRATIS */}
              <div className="bg-gradient-to-br from-green-50 to-white rounded-2xl shadow-lg border-4 border-green-400 p-8 hover:shadow-2xl transition relative">
                <div className="mb-6">
                  <div className="inline-flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-full mb-4">
                    <span className="text-xl">🎉</span>
                    <span className="font-bold text-sm">100% GRATIS</span>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">
                    Plan Starter
                  </h3>
                  <div className="flex items-baseline gap-2 mb-3">
                    <span className="text-5xl font-bold text-green-600">$0</span>
                    <span className="text-lg text-gray-600">MXN/mes</span>
                  </div>
                  <p className="text-sm text-gray-600">
                    Para nutriólogos iniciando su práctica
                  </p>
                </div>

                <div className="space-y-3 mb-8">
                  <h4 className="font-semibold text-gray-900 text-sm mb-3">Funcionalidades incluidas:</h4>
                  <FeatureItem text="Hasta 30 pacientes activos" compact />
                  <FeatureItem text="Expediente clínico digital" compact />
                  <FeatureItem text="Planes de alimentación personalizados" compact />
                  <FeatureItem text="Recordatorio 24 horas" compact />
                  <FeatureItem text="Análisis antropométrico básico" compact />
                  <FeatureItem text="Gráficas de progreso" compact />
                  <FeatureItem text="Sistema de citas (calendario básico)" compact />
                  <FeatureItem text="Portal completo del paciente" compact />
                  <FeatureItem text="Biblioteca de recetas mexicanas" compact />
                  <FeatureItem text="Mensajería con pacientes" compact />
                  <FeatureItem text="Plantillas de planes" compact />
                  <FeatureItem text="Reportes en PDF" compact />
                  <FeatureItem text="Soporte por email" compact />
                </div>

                <button
                  onClick={handleNutritionistDemo}
                  className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg
                           font-semibold transition shadow-md hover:shadow-lg"
                >
                  Comenzar Gratis Ahora
                </button>
                <p className="text-center text-gray-500 mt-3 text-xs">
                  Gratis para siempre • Sin tarjeta de crédito
                </p>
              </div>

              {/* PLAN PROFESIONAL - HIGHLIGHTED */}
              <div className="bg-gradient-to-br from-purple-50 to-white rounded-2xl shadow-2xl border-4 border-purple-500 p-8 relative transform md:scale-105">
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <div className="bg-purple-600 text-white px-6 py-2 rounded-full text-sm font-bold shadow-lg">
                    ⭐ MÁS POPULAR
                  </div>
                </div>

                <div className="mb-6 mt-4">
                  <div className="inline-flex items-center gap-2 bg-purple-600 text-white px-4 py-2 rounded-full mb-4">
                    <span className="text-xl">👨‍⚕️</span>
                    <span className="font-bold text-sm">PROFESIONAL</span>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">
                    Práctica Completa
                  </h3>
                  <div className="flex items-baseline gap-2 mb-3">
                    <span className="text-4xl font-bold text-gray-900">$543</span>
                    <span className="text-lg text-gray-600">MXN/mes</span>
                  </div>
                  <p className="text-sm text-gray-600">
                    Para nutriólogos establecidos
                  </p>
                </div>

                <div className="space-y-3 mb-8">
                  <h4 className="font-semibold text-purple-900 text-sm mb-3">Todo de Starter, más:</h4>
                  <FeatureItem text="Hasta 150 pacientes activos" purple compact />
                  <FeatureItem text="Videoconsultas integradas" purple compact />
                  <FeatureItem text="Sistema de cobro y facturación CFDI 4.0" purple compact />
                  <FeatureItem text="Análisis avanzados e IA predictiva" purple compact />
                  <FeatureItem text="Dashboard con KPIs profesionales" purple compact />
                  <FeatureItem text="Calendario avanzado + recordatorios automáticos" purple compact />
                  <FeatureItem text="Marca blanca personalizable" purple compact />
                  <FeatureItem text="Integración con wearables" purple compact />
                  <FeatureItem text="WhatsApp Business integration" purple compact />
                  <FeatureItem text="Soporte prioritario 24/7" purple compact />
                </div>

                <button
                  onClick={handleNutritionistDemo}
                  className="w-full bg-purple-600 hover:bg-purple-700 text-white py-3 rounded-lg
                           font-semibold transition shadow-lg hover:shadow-xl"
                >
                  Solicitar Demo
                </button>
                <p className="text-center text-gray-500 mt-3 text-xs">
                  14 días gratis • Cancela cuando quieras
                </p>
              </div>

              {/* PLAN CLÍNICA */}
              <div className="bg-white rounded-2xl shadow-lg border-2 border-gray-200 p-8 hover:shadow-2xl transition relative">
                <div className="mb-6">
                  <div className="inline-flex items-center gap-2 bg-amber-100 text-amber-800 px-4 py-2 rounded-full mb-4">
                    <span className="text-xl">🏢</span>
                    <span className="font-bold text-sm">CLÍNICA</span>
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">
                    Equipos & Enterprise
                  </h3>
                  <div className="flex items-baseline gap-2 mb-3">
                    <span className="text-4xl font-bold text-gray-900">$1,499</span>
                    <span className="text-lg text-gray-600">MXN/mes</span>
                  </div>
                  <p className="text-sm text-gray-600">
                    Para clínicas y equipos profesionales
                  </p>
                </div>

                <div className="space-y-3 mb-8">
                  <h4 className="font-semibold text-gray-900 text-sm mb-3">Todo de Profesional, más:</h4>
                  <FeatureItem text="Pacientes ilimitados" compact amber />
                  <FeatureItem text="Múltiples nutriólogos (hasta 10)" compact amber />
                  <FeatureItem text="Sistema de equipos completo" compact amber />
                  <FeatureItem text="Roles y permisos avanzados" compact amber />
                  <FeatureItem text="Calendario compartido del equipo" compact amber />
                  <FeatureItem text="Notas clínicas con IA" compact amber />
                  <FeatureItem text="Transcripción automática de consultas" compact amber />
                  <FeatureItem text="Generación de contenido con IA" compact amber />
                  <FeatureItem text="Landing page personalizada" compact amber />
                  <FeatureItem text="Marketing automation" compact amber />
                  <FeatureItem text="API completa para integraciones" compact amber />
                  <FeatureItem text="Gerente de cuenta dedicado" compact amber />
                </div>

                <button
                  onClick={handleNutritionistDemo}
                  className="w-full bg-amber-600 hover:bg-amber-700 text-white py-3 rounded-lg
                           font-semibold transition shadow-md hover:shadow-lg"
                >
                  Contactar Ventas
                </button>
                <p className="text-center text-gray-500 mt-3 text-xs">
                  Demo personalizada • Onboarding incluido
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Comparison Note */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mt-16 max-w-4xl mx-auto bg-white rounded-xl shadow-lg p-8"
        >
          <div className="text-center">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              ¿No estás seguro cuál plan elegir?
            </h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 text-left">
              <div className="bg-green-50 rounded-lg p-6 border-2 border-green-200">
                <h4 className="font-bold text-green-800 mb-2 flex items-center gap-2">
                  <span className="text-2xl">👤</span>
                  Elige el plan de Pacientes si:
                </h4>
                <ul className="space-y-2 text-gray-700 text-sm">
                  <li>• Buscas mejorar tu alimentación personal</li>
                  <li>• Quieres conectar con una comunidad saludable</li>
                  <li>• Deseas seguir el consejo de nutriólogos</li>
                  <li>• Te interesa compartir tu progreso</li>
                </ul>
              </div>

              <div className="bg-blue-50 rounded-lg p-6 border-2 border-blue-200">
                <h4 className="font-bold text-blue-800 mb-2 flex items-center gap-2">
                  <span className="text-2xl">🌱</span>
                  Plan Starter si:
                </h4>
                <ul className="space-y-2 text-gray-700 text-sm">
                  <li>• Estás iniciando tu práctica como nutriólogo</li>
                  <li>• Tienes hasta 30 pacientes</li>
                  <li>• Necesitas herramientas básicas profesionales</li>
                  <li>• Buscas una solución económica para comenzar</li>
                </ul>
              </div>

              <div className="bg-purple-50 rounded-lg p-6 border-2 border-purple-200">
                <h4 className="font-bold text-purple-800 mb-2 flex items-center gap-2">
                  <span className="text-2xl">👨‍⚕️</span>
                  Plan Profesional si:
                </h4>
                <ul className="space-y-2 text-gray-700 text-sm">
                  <li>• Tienes una práctica establecida</li>
                  <li>• Gestionas más de 30 pacientes</li>
                  <li>• Necesitas videoconsultas y facturación</li>
                  <li>• Quieres análisis avanzados e IA</li>
                </ul>
              </div>

              <div className="bg-amber-50 rounded-lg p-6 border-2 border-amber-200">
                <h4 className="font-bold text-amber-800 mb-2 flex items-center gap-2">
                  <span className="text-2xl">🏢</span>
                  Plan Clínica si:
                </h4>
                <ul className="space-y-2 text-gray-700 text-sm">
                  <li>• Diriges una clínica o equipo de nutriólogos</li>
                  <li>• Necesitas gestión multi-usuario</li>
                  <li>• Requieres herramientas de IA avanzadas</li>
                  <li>• Quieres marketing automation y API</li>
                </ul>
              </div>
            </div>
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
            <span className="text-sm">Datos Seguros y Encriptados</span>
          </div>
          <div className="flex items-center gap-2">
            <svg className="w-6 h-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span className="text-sm">🇲🇽 Hecho en México</span>
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

// Helper Component for Feature Items
const FeatureItem = ({ text, purple = false, amber = false, compact = false }) => {
  const iconColor = amber ? 'text-amber-600' : purple ? 'text-purple-600' : 'text-green-600';
  const iconSize = compact ? 'w-5 h-5' : 'w-6 h-6';
  const fontSize = compact ? 'text-sm' : 'font-medium';

  return (
    <div className="flex items-start gap-2">
      <svg
        className={`${iconSize} flex-shrink-0 mt-0.5 ${iconColor}`}
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path
          fillRule="evenodd"
          d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
          clipRule="evenodd"
        />
      </svg>
      <span className={`text-gray-700 ${fontSize}`}>{text}</span>
    </div>
  );
};

export default Pricing;
