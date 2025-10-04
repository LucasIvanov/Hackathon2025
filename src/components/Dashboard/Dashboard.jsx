import React, { useState, useEffect } from 'react';
import MetricCard from './MetricCard';
import ImpactChart from './ImpactChart';
import RankingTable from './RankingTable';
import { dashboardService } from '../../services/api';

const Dashboard = () => {
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
      
      // Simular carregamento (substituir pela API real)
      setTimeout(() => {
        setMetricas({
          custoTotal: 2850000,
          retornoTotal: 4120000,
          impactoLiquido: 1270000,
          bcMedio: 1.45,
          totalEmpresas: 158,
          totalIncentivos: 87
        });

        // Dados do gráfico simulados
        setChartData({
          labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
          custos: [230000, 250000, 280000, 260000, 290000, 310000, 295000, 320000, 285000, 300000, 315000, 285000],
          retornos: [350000, 380000, 420000, 390000, 450000, 480000, 465000, 510000, 445000, 475000, 495000, 445000]
        });

        // Dados de ranking simulados
        setRankingData([
          { id: 1, nome: 'Empresa Alpha Ltda', cnpj: '12345678000123', setor: 'Tecnologia', ratio: 2.5, impacto_liquido: 450000, crescimento: 15.2 },
          { id: 2, nome: 'Beta Comércio SA', cnpj: '98765432000156', setor: 'Comércio', ratio: 2.1, impacto_liquido: 320000, crescimento: 8.7 },
          { id: 3, nome: 'Gamma Indústria ME', cnpj: '11122233000144', setor: 'Indústria', ratio: 1.9, impacto_liquido: 280000, crescimento: 12.3 }
        ]);

        setLoading(false);
      }, 1500);
      
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      setLoading(false);
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
          />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
