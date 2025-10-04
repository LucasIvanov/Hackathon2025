import React, { useState, useEffect } from 'react';
import MetricCard from './MetricCard';
import ImpactChart from './ImpactChart';
import RankingTable from './RankingTable';

const Dashboard = ({ onChangeTab }) => {
  const [metricas, setMetricas] = useState({
    custoTotal: 0,
    retornoTotal: 0,
    impactoLiquido: 0,
    bcMedio: 0,
    totalEmpresas: 0,
    totalIncentivos: 0
  });

  const [chartData, setChartData] = useState(null);
  const [rankingData, setRankingData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = async () => {
    try {
      setLoading(true);
      
      // Simular dados da API
      setTimeout(() => {
        setMetricas({
          custoTotal: 2850000,
          retornoTotal: 4120000,
          impactoLiquido: 1270000,
          bcMedio: 1.45,
          totalEmpresas: 158,
          totalIncentivos: 87
        });

        // Dados do gráfico
        setChartData({
          labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
          custos: [230000, 250000, 280000, 260000, 290000, 310000, 295000, 320000, 285000, 300000, 315000, 285000],
          retornos: [350000, 380000, 420000, 390000, 450000, 480000, 465000, 510000, 445000, 475000, 495000, 445000]
        });

        // Dados de ranking - EXPANDIDOS
        setRankingData([
          { id: 1, nome: 'Empresa Alpha Ltda', cnpj: '12345678000123', setor: 'Tecnologia', ratio: 2.5, impacto_liquido: 450000, crescimento: 15.2 },
          { id: 2, nome: 'Beta Comércio SA', cnpj: '98765432000156', setor: 'Comércio', ratio: 2.1, impacto_liquido: 320000, crescimento: 8.7 },
          { id: 3, nome: 'Gamma Indústria ME', cnpj: '11122233000144', setor: 'Indústria', ratio: 1.9, impacto_liquido: 280000, crescimento: 12.3 },
          { id: 4, nome: 'Delta Serviços Ltda', cnpj: '44455566000177', setor: 'Serviços', ratio: 1.8, impacto_liquido: 250000, crescimento: 6.9 },
          { id: 5, nome: 'Epsilon Tech SA', cnpj: '77788899000166', setor: 'Tecnologia', ratio: 1.7, impacto_liquido: 220000, crescimento: 9.4 },
          { id: 6, nome: 'Zeta Construção ME', cnpj: '33344455000188', setor: 'Construção', ratio: 1.6, impacto_liquido: 200000, crescimento: -2.1 },
          { id: 7, nome: 'Eta Alimentação Ltda', cnpj: '66677788000155', setor: 'Alimentação', ratio: 1.5, impacto_liquido: 180000, crescimento: 4.7 },
          { id: 8, nome: 'Theta Logística SA', cnpj: '99988877000144', setor: 'Logística', ratio: 1.4, impacto_liquido: 160000, crescimento: 7.2 },
          { id: 9, nome: 'Iota Consultoria ME', cnpj: '55566677000133', setor: 'Consultoria', ratio: 1.3, impacto_liquido: 140000, crescimento: 11.8 },
          { id: 10, nome: 'Kappa Varejo Ltda', cnpj: '22233344000122', setor: 'Varejo', ratio: 1.2, impacto_liquido: 120000, crescimento: 3.5 }
        ]);

        setLoading(false);
      }, 1500);
      
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      setLoading(false);
    }
  };

  const handleVerTodasEmpresas = () => {
    console.log('🏢 Navegando para página de empresas...');
    if (onChangeTab) {
      onChangeTab('empresas');
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Carregando dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <h1 className="dashboard-title">Dashboard</h1>
        <p className="dashboard-subtitle">
          Visão geral dos incentivos fiscais e desempenho
        </p>
      </div>

      {/* Metrics */}
      <div className="metrics-grid">
        <MetricCard
          title="Custo Fiscal Total"
          value={`${(metricas.custoTotal / 1000000).toFixed(2)}M`}
          icon="💰"
          color="blue"
          trend="down"
          trendValue="-5.2%"
        />
        
        <MetricCard
          title="Retorno Fiscal Total"
          value={`${(metricas.retornoTotal / 1000000).toFixed(2)}M`}
          icon="📈"
          color="green"
          trend="up"
          trendValue="+12.8%"
        />
        
        <MetricCard
          title="Impacto Líquido"
          value={`${(metricas.impactoLiquido / 1000000).toFixed(2)}M`}
          icon="⚖️"
          color="purple"
          trend="up"
          trendValue="+8.5%"
        />
        
        <MetricCard
          title="Adicionalidade Média"
          value={`${(metricas.bcMedio * 100).toFixed(1)}%`}
          icon="📊"
          color="orange"
          trend="up"
          trendValue="+3.2%"
          prefix=""
        />
      </div>

      {/* Chart e Ranking */}
      <div className="dashboard-grid">
        <div className="chart-section">
          <ImpactChart data={chartData} />
        </div>
        
        <div className="ranking-section">
          <RankingTable 
            empresas={rankingData} 
            tipo="custo_beneficio"
            onVerTodasEmpresas={handleVerTodasEmpresas}
          />
        </div>
      </div>

      {/* Seção adicional de estatísticas */}
      <div className="stats-section">
        <div className="stats-card">
          <h3>📊 Resumo Executivo</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Empresas Cadastradas</span>
              <span className="stat-value">{metricas.totalEmpresas}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Incentivos Ativos</span>
              <span className="stat-value">{metricas.totalIncentivos}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">B/C Ratio Médio</span>
              <span className="stat-value">{metricas.bcMedio.toFixed(2)}x</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">ROI Médio</span>
              <span className="stat-value">{((metricas.bcMedio - 1) * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
