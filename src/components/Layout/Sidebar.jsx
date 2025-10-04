import React from 'react';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    {
      id: 'dashboard',
      name: 'Dashboard',
      icon: '📊',
      description: 'Visão geral'
    },
    {
      id: 'empresas',
      name: 'Empresas',
      icon: '🏢',
      description: 'Gestão de empresas'
    },
    {
      id: 'upload',
      name: 'Upload',
      icon: '📁',
      description: 'Importar dados'
    },
    {
      id: 'alertas',
      name: 'Alertas',
      icon: '🚨',
      description: 'Monitoramento'
    }
  ];

  return (
    <div className="sidebar">
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
          <h4 className="nav-title">NAVEGAÇÃO</h4>
          {menuItems.map(item => (
            <button
              key={item.id}
              className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
              onClick={() => setActiveTab(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              <div className="nav-content">
                <span className="nav-name">{item.name}</span>
                <span className="nav-description">{item.description}</span>
              </div>
            </button>
          ))}
        </div>
      </nav>

      {/* Status */}
      <div className="sidebar-status">
        <div className="status-indicator">
          <span className="status-icon">📈</span>
          <span className="status-text">Status do Sistema</span>
        </div>
        <div className="status-value">
          <span className="status-number">100%</span>
          <span className="status-label">Operacional</span>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
