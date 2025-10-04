import React, { useState, useEffect } from 'react';

const Alertas = () => {
  const [alertas, setAlertas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    carregarAlertas();
  }, []);

  const carregarAlertas = async () => {
    setLoading(true);
    
    // Simular dados de alertas
    setTimeout(() => {
      setAlertas([
        {
          id: 1,
          tipo: 'BC_BAIXO',
          empresa: 'Empresa ABC Ltda',
          cnpj: '12345678000123',
          severidade: 'ALTA',
          descricao: 'Relação B/C abaixo de 1: 0.85',
          data: '2025-10-04'
        },
        {
          id: 2,
          tipo: 'SEM_RECOLHIMENTO',
          empresa: 'Comércio XYZ SA',
          cnpj: '98765432000156',
          severidade: 'MEDIA',
          descricao: 'Sem recolhimento de ISS nos últimos 3 meses',
          data: '2025-10-03'
        },
        {
          id: 3,
          tipo: 'INCENTIVO_VENCENDO',
          empresa: 'Tecnologia DEF ME',
          cnpj: '11122233000144',
          severidade: 'MEDIA',
          descricao: 'Incentivo vence em 15 dias',
          data: '2025-10-02'
        }
      ]);
      setLoading(false);
    }, 1000);
  };

  const gerarAlertas = async () => {
    setLoading(true);
    // Simular geração de alertas
    setTimeout(() => {
      setAlertas(prev => [...prev, {
        id: Date.now(),
        tipo: 'NOVO_ALERTA',
        empresa: 'Nova Empresa Ltda',
        cnpj: '99988877000133',
        severidade: 'BAIXA',
        descricao: 'Novo alerta gerado automaticamente',
        data: new Date().toISOString().split('T')[0]
      }]);
      setLoading(false);
    }, 1500);
  };

  const getSeveridadeColor = (severidade) => {
    switch (severidade) {
      case 'ALTA': return 'red';
      case 'MEDIA': return 'orange';
      case 'BAIXA': return 'yellow';
      default: return 'gray';
    }
  };

  const getTipoIcon = (tipo) => {
    switch (tipo) {
      case 'BC_BAIXO': return '📉';
      case 'SEM_RECOLHIMENTO': return '💸';
      case 'INCENTIVO_VENCENDO': return '⏰';
      default: return '🚨';
    }
  };

  return (
    <div className="page-content">
      <div className="page-header">
        <h1>🚨 Alertas</h1>
        <p>Monitoramento e alertas do sistema</p>
      </div>

      <div className="content-card">
        <div className="card-header">
          <h3>Alertas Ativos ({alertas.length})</h3>
          <div className="header-actions">
            <button 
              onClick={gerarAlertas}
              disabled={loading}
              className="btn-primary"
            >
              {loading ? '⏳ Gerando...' : '🔄 Gerar Alertas'}
            </button>
          </div>
        </div>

        <div className="card-body">
          {loading ? (
            <div className="loading-state">
              <div className="loading-spinner"></div>
              <p>Carregando alertas...</p>
            </div>
          ) : (
            <div className="alerts-container">
              {alertas.map(alerta => (
                <div key={alerta.id} className="alert-item">
                  <div className="alert-icon">
                    {getTipoIcon(alerta.tipo)}
                  </div>
                  
                  <div className="alert-content">
                    <div className="alert-header">
                      <span className="alert-empresa">{alerta.empresa}</span>
                      <span className={`alert-severity severity-${getSeveridadeColor(alerta.severidade)}`}>
                        {alerta.severidade}
                      </span>
                    </div>
                    
                    <div className="alert-description">
                      {alerta.descricao}
                    </div>
                    
                    <div className="alert-meta">
                      <span>CNPJ: {alerta.cnpj}</span>
                      <span>Data: {alerta.data}</span>
                    </div>
                  </div>
                  
                  <div className="alert-actions">
                    <button className="btn-small btn-outline">
                      ✅ Resolver
                    </button>
                  </div>
                </div>
              ))}
              
              {alertas.length === 0 && (
                <div className="empty-state">
                  <p>🎉 Nenhum alerta ativo no momento</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Alertas;
