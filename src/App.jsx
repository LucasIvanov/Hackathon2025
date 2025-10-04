import React from 'react';
import { AuthProvider } from './context/AuthContext';
import AppContent from './components/AppContent';
import './styles/dashboard.css';

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
