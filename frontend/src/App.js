import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import logo from './logo.svg';
import Login from './pages/Auth/Login';
import Dashboard from './pages/Dashboard/Dashboard';
import LogForm from './pages/Logs/LogForm';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>

        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/submit-log" element={<LogForm />} />
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;