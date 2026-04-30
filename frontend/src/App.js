import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Signup from './pages/Signup';
import LogForm from './pages/Logs/LogForm';
import ProtectedRoute from './components/ProtectedRoute';
import AssignPlacement from './pages/pages/AssignPlacement';
import CreateLog from './pages/Logs/CreateLog';
import MyLogs from './pages/Logs/MyLogs';
import WorkplaceLogs from './pages/Logs/WorkplaceLogs';
import AcademicLogs from './pages/Logs/cademicLogs';
import CreateEvaluation from './pages/Evaluations/Evaluation';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />}/>
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="/assign-placement" element={<AssignPlacement/>}/>
          <Route path="/create-log" element={<CreateLog/>}/>
          <Route path="/my-logs" element={<MyLogs/>} />
          <Route path="/workplace/logs" element={<WorkplaceLogs />} />
          <Route path="/academic/logs" element={<AcademicLogs />} />
          <Route path="/evaluate/:placementId" element={<CreateEvaluation />} />
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