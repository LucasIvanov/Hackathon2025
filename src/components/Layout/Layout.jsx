import React, { useState } from "react";

const Layout = ({ children }) => {
  const [activeTab, setActiveTab] = useState('dashboard');

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

        {/* Navigation */}
        <nav className="sidebar-nav">
          <div className="nav-section">
            <h4 className="nav-section-title">NAVEGAÇÃO</h4>
            {navigationItems.map(item => (
              <button
                key={item.id}
                className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                onClick={() => setActiveTab(item.id)}
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

        {/* Status */}
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
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {React.cloneElement(children, { activeTab, setActiveTab })}
      </main>
    </div>
  );
};


export default Layout;
