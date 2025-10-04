import React, { useState, useEffect, useCallback } from "react";
import { dashboardService, calculosService, alertasService } from '../../services/api';
import MetricCard from './MetricCard';
import ImpactChart from './ImpactChart';
import RankingTable from './RankingTable';

export default function Dashboard() {
  const [metricas, setMetricas] = useState({
    custoTotal: 0,
    retornoTotal: 0, 
    impactoLiquido: 0,
    bcMedio: 0,
    totalEmpresas: 0,
    totalIncentivos: 0
  });

  const [chartData, setChartData] = useState(null);
  const [rankings, setRankings] = useState({
    custoBeneficio: [],
    impactoLiquido: []
  });
  const [alertasAtivos, setAlertasAtivos] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  const loadDashboardData = useCallback(async () => {
    setIsLoading(true);
    try {
      // Carregar dados do dashboard
      const resumo = await dashboardService.getResumo();
      
      setMetricas({
        custoTotal: resumo.custo_fiscal_total || 0,
        retornoTotal: resumo.arrecadacao_incremental_total || 0,
        impactoLiquido: resumo.impacto_liquido_total || 0,
        bcMedio: resumo.bc_medio || 0,
        totalEmpresas: resumo.total_empresas || 0,
        totalIncentivos: resumo.total_incentivos_ativos || 0
      });

      setAlertasAtivos(resumo.total_alertas_ativos || 0);

      // Carregar ranking
      const rankingData = await calculosService.getRanking('melhores', 10);
      
      // Adaptar dados para o formato esperado pelo componente
      const empresasRanking = rankingData.map(calc => ({
        id: calc.empresa?.id || Math.random(),
        nome: calc.empresa?.razao_social || 'Empresa não identificada',
        cnpj: calc.empresa?.cnpj || '00000000000000',
        setor: calc.empresa?.cnae_descricao || 'Não informado',
        ratio: calc.bc_ratio || 0,
        impacto_liquido: calc.impacto_liquido || 0,
        crescimento: Math.random() * 20 + 5 // Simulado por enquanto
      }));

      setRankings({
        custoBeneficio: empresasRanking,
        impactoLiquido: [...empresasRanking].sort((a, b) => b.impacto_liquido - a.impacto_liquido)
      });

      // Simular dados do gráfico (últimos 12 meses)
      const chartLabels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                          'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
      
      setChartData({
        labels: chartLabels,
        custos: chartLabels.map(() => Math.random() * 500000 + 200000),
        retornos: chartLabels.map(() => Math.random() * 800000 + 300000)
      });

    } catch (error) {
      console.error("Erro ao carregar dados:", error);
      // Usar dados simulados em caso de erro
      setMetricas({
        custoTotal: 2850000,
        retornoTotal: 4120000,
        impactoLiquido: 1270000,
        bcMedio: 1.45,
        totalEmpresas: 158,
        totalIncentivos: 87
      });
    }
    setIsLoading(false);
  }, []);

  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Carregando dashboard...</p>
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
            empresas={rankings.custoBeneficio} 
            tipo="custo_beneficio"
          />
        </div>
      </div>

      {/* Alertas */}
      {alertasAtivos > 0 && (
        <div className="alerts-banner">
          <div className="alert-content">
            <span className="alert-icon">🚨</span>
            <div className="alert-text">
              <strong>Atenção!</strong> 
              Existem {alertasAtivos} alertas ativos no sistema.
            </div>
            <button 
              className="alert-button"
              onClick={() => window.location.href = '#alertas'}
            >
              Ver alertas
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
