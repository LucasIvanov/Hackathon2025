import React, { useState, useEffect } from 'react';
import MetricCard from '../components/Dashboard/MetricCard';

const Dashboard = () => {
  const [metrics, setMetrics] = useState({
    custoFiscal: 'R$ 0.00M',
    retornoFiscal: 'R$ 0.00M',
    impactoLiquido: 'R$ 0.00M',
    adicionalidade: '0.0%'
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simular carregamento de dados da API
    setTimeout(() => {
      setMetrics({
        custoFiscal: 'R$ 2.85M',
        retornoFiscal: 'R$ 4.12M',
        impactoLiquido: 'R$ 1.27M',
        adicionalidade: '68.4%'
      });
      setLoading(false);
    }, 1500);
  }, []);

  const chartData = Array.from({ length: 12 }, (_, i) => ({
    month: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'][i],
    value: Math.floor(Math.random() * 1000000) + 500000
  }));

  return (
    <div className="dashboard-content">
      {/* Header */}
      <div className="dashboard-header">
        <h1 className="dashboard-title">Dashboard</h1>
        <p className="dashboard-subtitle">Visão geral dos incentivos fiscais e desempenho</p>
      </div>

      {/* Metrics Grid */}
      <div className="metrics-grid">
        <MetricCard
          title="Custo Fiscal Total"
          value={loading ? 'R$ 0.00M' : metrics.custoFiscal}
          change="-5.2%"
          changeType="negative"
          color="blue"
          icon="💰"
        />
        
        <MetricCard
          title="Retorno Fiscal Total"
          value={loading ? 'R$ 0.00M' : metrics.retornoFiscal}
          change="+12.8%"
          changeType="positive"
          color="green"
          icon="📈"
        />
        
        <MetricCard
          title="Impacto Líquido"
          value={loading ? 'R$ 0.00M' : metrics.impactoLiquido}
          change="+8.5%"
          changeType="positive"
          color="purple"
          icon="⚖️"
        />
        
        <MetricCard
          title="Adicionalidade Média"
          value={loading ? '0.0%' : metrics.adicionalidade}
          change="+3.2%"
          changeType="positive"
          color="orange"
          icon="📊"
        />
      </div>

      {/* Chart Section */}
      <div className="chart-section">
        <div className="chart-header">
          <h2 className="chart-title">Tendência de Impacto Fiscal (12 meses)</h2>
        </div>
        
        <div className="chart-container">
          <div className="chart-placeholder">
            <div className="chart-y-axis">
              <span>R$ 6k</span>
              <span>R$ 4k</span>
              <span>R$ 2k</span>
              <span>R$ 0k</span>
            </div>
            
            <div className="chart-area">
              {loading ? (
                <div className="chart-loading">
                  <div className="loading-spinner"></div>
                  <p>Carregando dados do gráfico...</p>
                </div>
              ) : (
                <svg className="chart-svg" viewBox="0 0 400 200">
                  <defs>
                    <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stopColor="#4285f4" stopOpacity="0.3"/>
                      <stop offset="100%" stopColor="#4285f4" stopOpacity="0.1"/>
                    </linearGradient>
                  </defs>
                  
                  {/* Chart line */}
                  <path
                    d="M 0 150 Q 50 100 100 120 T 200 80 T 300 60 T 400 40"
                    stroke="#4285f4"
                    strokeWidth="3"
                    fill="none"
                  />
                  
                  {/* Chart area */}
                  <path
                    d="M 0 150 Q 50 100 100 120 T 200 80 T 300 60 T 400 40 L 400 200 L 0 200 Z"
                    fill="url(#chartGradient)"
                  />
                  
                  {/* Data points */}
                  {[0, 100, 200, 300, 400].map((x, i) => (
                    <circle
                      key={i}
                      cx={x}
                      cy={[150, 120, 80, 60, 40][i]}
                      r="4"
                      fill="#4285f4"
                    />
                  ))}
                </svg>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
