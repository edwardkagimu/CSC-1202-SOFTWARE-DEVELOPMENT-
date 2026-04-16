import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Login from './pages/Auth/Login';
import Dashboard from './pages/Dashboard/Dashboard';
import LogForm from './pages/Logs/LogForm';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      
      <AuthProvider>
        <Routes>
          
          <Route path="/login" element={<Login />} />

          {/* Protected Routes (Only logged-in users can enter) */}
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/submit-log" 
            element={
              <ProtectedRoute>
                <LogForm />
              </ProtectedRoute>
            } 
          />

          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;