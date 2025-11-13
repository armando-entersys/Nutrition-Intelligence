/**
 * App Component - Main Router
 * Handles authentication and routing
 */
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import MainApp from './MainApp';
import PrivateRoute from './components/auth/PrivateRoute';
import { Login, Register, ForgotPassword, ResetPassword } from './screens/auth';
import { LandingPage } from './screens/landing';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Landing Page - Public */}
        <Route path="/" element={<LandingPage />} />

        {/* Authentication Routes - Public */}
        <Route path="/auth/login" element={<Login />} />
        <Route path="/auth/register" element={<Register />} />
        <Route path="/auth/forgot-password" element={<ForgotPassword />} />
        <Route path="/auth/reset-password" element={<ResetPassword />} />

        {/* Main Application Routes - Protected */}
        <Route
          path="/dashboard/*"
          element={
            <PrivateRoute>
              <MainApp />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;