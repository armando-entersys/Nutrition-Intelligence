/**
 * Landing Page - Public Marketing Page
 * Main landing page for Nutrition Intelligence
 */
import React, { useEffect } from 'react';
import Hero from '../../components/landing/Hero';
import Features from '../../components/landing/Features';
import HowItWorks from '../../components/landing/HowItWorks';
import Pricing from '../../components/landing/Pricing';
import Footer from '../../components/landing/Footer';
import { initGA } from '../../utils/analytics';

const LandingPage = () => {
  useEffect(() => {
    // Initialize Google Analytics
    initGA();

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
  }, []);

  return (
    <div className="landing-page">
      {/* Navigation Bar */}
      <nav className="fixed top-0 left-0 right-0 bg-white shadow-sm z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center">
              <a href="/" className="text-2xl font-bold text-green-600">
                Nutrition Intelligence
              </a>
            </div>

            {/* Navigation Links */}
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-700 hover:text-green-600 transition">
                Características
              </a>
              <a href="#how-it-works" className="text-gray-700 hover:text-green-600 transition">
                Cómo Funciona
              </a>
              <a href="#pricing" className="text-gray-700 hover:text-green-600 transition">
                Precios
              </a>
              <a href="/auth/login" className="text-gray-700 hover:text-green-600 transition">
                Iniciar Sesión
              </a>
              <a
                href="/auth/register"
                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-semibold"
              >
                Empezar Gratis
              </a>
            </div>

            {/* Mobile Menu Button */}
            <div className="md:hidden">
              <button
                className="text-gray-700 hover:text-green-600"
                onClick={() => {
                  const mobileMenu = document.getElementById('mobile-menu');
                  mobileMenu.classList.toggle('hidden');
                }}
              >
                <svg className="w-6 h-6" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                  <path d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
              </button>
            </div>
          </div>

          {/* Mobile Menu */}
          <div id="mobile-menu" className="hidden md:hidden pb-4">
            <div className="flex flex-col space-y-3">
              <a href="#features" className="text-gray-700 hover:text-green-600 transition">
                Características
              </a>
              <a href="#how-it-works" className="text-gray-700 hover:text-green-600 transition">
                Cómo Funciona
              </a>
              <a href="#pricing" className="text-gray-700 hover:text-green-600 transition">
                Precios
              </a>
              <a href="/auth/login" className="text-gray-700 hover:text-green-600 transition">
                Iniciar Sesión
              </a>
              <a
                href="/auth/register"
                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-semibold text-center"
              >
                Empezar Gratis
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content - Add padding-top to account for fixed navbar */}
      <div className="pt-16">
        {/* Hero Section */}
        <Hero />

        {/* Features Section */}
        <div id="features">
          <Features />
        </div>

        {/* How It Works Section */}
        <div id="how-it-works">
          <HowItWorks />
        </div>

        {/* Pricing Section */}
        <div id="pricing">
          <Pricing />
        </div>

        {/* Footer */}
        <Footer />
      </div>
    </div>
  );
};

export default LandingPage;
