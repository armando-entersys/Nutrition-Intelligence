/**
 * App Component - Main Router
 * Handles authentication and routing
 */
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import MainApp from './MainApp';
import PrivateRoute from './components/auth/PrivateRoute';
import { Login, Register, ForgotPassword, ResetPassword } from './screens/auth';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Authentication Routes - Public */}
        <Route path="/auth/login" element={<Login />} />
        <Route path="/auth/register" element={<Register />} />
        <Route path="/auth/forgot-password" element={<ForgotPassword />} />
        <Route path="/auth/reset-password" element={<ResetPassword />} />

        {/* Main Application Routes - Protected */}
        <Route
          path="/*"
          element={
            <PrivateRoute>
              <MainApp />
            </PrivateRoute>
          }
        />

        {/* Redirect root to main app (will be protected) */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;