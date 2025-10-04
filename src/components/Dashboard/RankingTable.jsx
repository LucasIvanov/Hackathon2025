import React from 'react';
 
export default function RankingTable({ empresas, tipo = "custo_beneficio" }) {
  const getTitleByType = () => {
    switch(tipo) {
      case "custo_beneficio": return "Melhor Custo-Benefício";
      case "impacto_liquido": return "Maior Impacto Líquido";
      case "pior_desempenho": return "Desempenho Abaixo da Média";
      default: return "Ranking";
    }
  };

  const getMedalEmoji = (index) => {
    switch(index) {
      case 0: return "🥇";
      case 1: return "🥈"; 
      case 2: return "🥉";
      default: return `${index + 1}°`;
    }
  };

  const formatValue = (empresa) => {
    if (tipo === "custo_beneficio") {
      return `${empresa.ratio?.toFixed(1)}x`;
    } else {
      return `R$ ${(empresa.impacto_liquido / 1000).toFixed(0)}k`;
    }
  };

  return (
    <div className="ranking-card">
      <div className="ranking-header">
        <div className="ranking-title-section">
          <h3 className="ranking-title">{getTitleByType()}</h3>
          <span className="ranking-subtitle">Top 10</span>
        </div>
        <span className="ranking-icon">🏆</span>
      </div>

      <div className="ranking-list">
        {empresas?.slice(0, 10).map((empresa, index) => (
          <div key={empresa.id || index} className="ranking-item">
            <div className="ranking-position">
              <span className="position-number">{getMedalEmoji(index)}</span>
            </div>
            
            <div className="empresa-info">
              <div className="empresa-name">{empresa.nome}</div>
              <div className="empresa-details">
                <span className="empresa-cnpj">{empresa.cnpj}</span>
                <span className="empresa-setor">{empresa.setor}</span>
              </div>
            </div>
            
            <div className="ranking-metrics">
              <div className="metric-primary">
                {formatValue(empresa)}
              </div>
              <div className={`metric-trend ${empresa.crescimento >= 0 ? 'positive' : 'negative'}`}>
                <span className="trend-icon">
                  {empresa.crescimento >= 0 ? '📈' : '📉'}
                </span>
                <span>{Math.abs(empresa.crescimento).toFixed(1)}%</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="ranking-footer">
        <button className="ranking-see-all"
        onClick={()=>window.dispatchEvent(new CustomEvent('navigateTo',{detail: {tab:'empresas'}}))}
        aria-label = "Ver todas as empresas"
        >
        <span>Ver todas as empresas</span>
        <span className="arrow-icon">→</span>
        </button>
      </div>
    </div>
  );
}
