import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import Login from './Login/Login';
import Dashboard from './Dashboard/Dashboard';
import Empresas from './Pages/Empresas';
import Upload from './Pages/Upload'; 
import Alertas from './Pages/Alertas';

const AppContent = () => {
  const { user, logout, loading } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');

  // Loading do AuthContext
  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Verificando autenticação...</p>
      </div>
    );
  }

  // Se não há usuário logado, mostrar tela de login
  if (!user) {
    return <Login />;
  }

  // Função para mudar de aba
  const handleChangeTab = (tab) => {
    console.log(`🔄 Mudando para aba: ${tab}`);
    setActiveTab(tab);
  };

  // Componentes das páginas
  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard onChangeTab={handleChangeTab} />;
      case 'empresas':
        return <Empresas onChangeTab={handleChangeTab} />;
      case 'upload':
        return <Upload onChangeTab={handleChangeTab} />;
      case 'alertas':
        return <Alertas onChangeTab={handleChangeTab} />;
      default:
        return <Dashboard onChangeTab={handleChangeTab} />;
    }
  };

  const navigationItems = [
    {
      id: 'dashboard',
      title: "Dashboard",
      icon: "📊",
      description: "Visão geral"
    },
    {
      id: 'empresas',
      title: "Empresas", 
      icon: "🏢",
      description: "Gestão de empresas"
    },
    {
      id: 'upload',
      title: "Upload",
      icon: "📁", 
      description: "Importar dados"
    },
    {
      id: 'alertas',
      title: "Alertas",
      icon: "🚨",
      description: "Monitoramento"
    }
  ];

  return (
    <div className="app-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        {/* Logo */}
        <div className="sidebar-header">
          <div className="logo">
            <div className="logo-icon">📈</div>
            <div className="logo-text">
              <div className="logo-title">FiscalTracker</div>
              <div className="logo-subtitle">Gestão de Incentivos</div>
            </div>
          </div>
        </div>

        {/* User Info */}
        <div className="user-info">
          <div className="user-avatar">
            {user.nome_completo.charAt(0).toUpperCase()}
          </div>
          <div className="user-details">
            <div className="user-name">{user.nome_completo}</div>
            <div className="user-role">{user.cargo}</div>
            <div className="user-department">{user.departamento}</div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="sidebar-nav">
          <div className="nav-section">
            <h4 className="nav-section-title">NAVEGAÇÃO</h4>
            {navigationItems.map(item => (
              <button
                key={item.id}
                className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                onClick={() => handleChangeTab(item.id)}
              >
                <span className="nav-icon">{item.icon}</span>
                <div className="nav-content">
                  <span className="nav-title">{item.title}</span>
                  <span className="nav-description">{item.description}</span>
                </div>
              </button>
            ))}
          </div>
        </nav>

        {/* Status e Logout */}
        <div className="sidebar-footer">
          <div className="sidebar-status">
            <div className="status-header">
              <span className="status-icon">📈</span>
              <span className="status-label">Status do Sistema</span>
            </div>
            <div className="status-metrics">
              <div className="status-value">100%</div>
              <div className="status-text">Operacional</div>
            </div>
          </div>
          
          <button className="logout-button" onClick={logout}>
            🚪 Sair ({user.username})
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <div className="page-indicator">
          <span className="current-page">
            {navigationItems.find(item => item.id === activeTab)?.icon} {" "}
            {navigationItems.find(item => item.id === activeTab)?.title}
          </span>
          <span className="user-welcome">
            Bem-vindo, <strong>{user.nome_completo}</strong>
          </span>
        </div>
        {renderContent()}
      </main>
    </div>
  );
};

export default AppContent;
