import React, { useState } from 'react';
import Sidebar from './components/Layout/Sidebar';
import Dashboard from './pages/Dashboard';
import './styles/dashboard.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'empresas':
        return (
          <div className="page-content">
            <h1>🏢 Empresas</h1>
            <p>Gestão de empresas cadastradas no sistema</p>
            <div className="coming-soon">Em desenvolvimento...</div>
          </div>
        );
      case 'upload':
        return (
          <div className="page-content">
            <h1>📁 Upload de Dados</h1>
            <p>Importar arquivos CSV para o sistema</p>
            <div className="coming-soon">Em desenvolvimento...</div>
          </div>
        );
      case 'alertas':
        return (
          <div className="page-content">
            <h1>🚨 Alertas</h1>
            <p>Monitoramento e alertas do sistema</p>
            <div className="coming-soon">Em desenvolvimento...</div>
          </div>
        );
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="app">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="main-content">
        {renderContent()}
      </main>
    </div>
  );
}

export default App;
