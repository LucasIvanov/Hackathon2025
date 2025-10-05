import React, { useState, useEffect } from 'react';

const Empresas = ({ onChangeTab }) => {
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filtro, setFiltro] = useState('');
  const [filtroSetor, setFiltroSetor] = useState('');
  const [filtroPorte, setFiltroPorte] = useState('');

  useEffect(() => {
    carregarEmpresas();
  }, []);

  const carregarEmpresas = async () => {
    try {
      setLoading(true);
      
      // Simular dados completos (integrar com API depois)
      setTimeout(() => {
        setEmpresas([
          { id: 1, cnpj: '12345678000123', razao_social: 'Empresa Alpha Ltda', cnae_descricao: 'Tecnologia', bairro: 'Centro', porte: 'ME', bc_ratio: 2.5, impacto_liquido: 450000 },
          { id: 2, cnpj: '98765432000156', razao_social: 'Beta Comércio SA', cnae_descricao: 'Comércio', bairro: 'Jardim Universitário', porte: 'GRANDE', bc_ratio: 2.1, impacto_liquido: 320000 },
          { id: 3, cnpj: '11122233000144', razao_social: 'Gamma Indústria ME', cnae_descricao: 'Indústria', bairro: 'Distrito Industrial', porte: 'EPP', bc_ratio: 1.9, impacto_liquido: 280000 },
          { id: 4, cnpj: '44455566000177', razao_social: 'Delta Serviços Ltda', cnae_descricao: 'Serviços', bairro: 'Centro', porte: 'ME', bc_ratio: 1.8, impacto_liquido: 250000 },
          { id: 5, cnpj: '77788899000166', razao_social: 'Epsilon Tech SA', cnae_descricao: 'Tecnologia', bairro: 'Jardim Universitário', porte: 'GRANDE', bc_ratio: 1.7, impacto_liquido: 220000 },
          { id: 6, cnpj: '33344455000188', razao_social: 'Zeta Construção ME', cnae_descricao: 'Construção', bairro: 'Centro', porte: 'ME', bc_ratio: 1.6, impacto_liquido: 200000 },
          { id: 7, cnpj: '66677788000155', razao_social: 'Eta Alimentação Ltda', cnae_descricao: 'Alimentação', bairro: 'Cascavel Velho', porte: 'EPP', bc_ratio: 1.5, impacto_liquido: 180000 },
          { id: 8, cnpj: '99988877000144', razao_social: 'Theta Logística SA', cnae_descricao: 'Logística', bairro: 'Distrito Industrial', porte: 'GRANDE', bc_ratio: 1.4, impacto_liquido: 160000 },
          { id: 9, cnpj: '55566677000133', razao_social: 'Iota Consultoria ME', cnae_descricao: 'Consultoria', bairro: 'Centro', porte: 'ME', bc_ratio: 1.3, impacto_liquido: 140000 },
          { id: 10, cnpj: '22233344000122', razao_social: 'Kappa Varejo Ltda', cnae_descricao: 'Varejo', bairro: 'Jardim Universitário', porte: 'EPP', bc_ratio: 1.2, impacto_liquido: 120000 }
        ]);
        setLoading(false);
      }, 1000);
      
    } catch (error) {
      console.error('Erro ao carregar empresas:', error);
      setLoading(false);
    }
  };

  // Exportar as empresas filtradas para CSV
  const exportReport = () => {
    const rows = empresasFiltradas;
    if (!rows || rows.length === 0) {
      alert('Nenhuma empresa para exportar');
      return;
    }

    const headers = ['ID','CNPJ','Razão Social','Setor','Bairro','Porte','B/C Ratio','Impacto Líquido'];

    const escapeCsv = (value) => {
      if (value === null || value === undefined) return '';
      const s = String(value);
      // Escapa aspas duplas conforme RFC4180
      if (s.includes(',') || s.includes('"') || s.includes('\n')) {
        return '"' + s.replace(/"/g, '""') + '"';
      }
      return s;
    };

    const lines = rows.map(r => [
      r.id,
      // forçar CNPJ como string para preservar zeros à esquerda
      `"${String(r.cnpj)}"`,
      escapeCsv(r.razao_social),
      escapeCsv(r.cnae_descricao),
      escapeCsv(r.bairro),
      escapeCsv(r.porte),
      r.bc_ratio,
      // exportar impacto em reais
      Number(r.impacto_liquido)
    ].join(','));

    const csvContent = '\uFEFF' + [headers.join(','), ...lines].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const filename = `empresas-report-${new Date().toISOString().slice(0,10)}.csv`;

    if (navigator.msSaveBlob) { // IE10+
      navigator.msSaveBlob(blob, filename);
    } else {
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', filename);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }
  };

  // Função única para ver detalhes da empresa
  const handleVerDetalhes = (empresa) => {
    const detalhes = `📋 DETALHES DA EMPRESA

🏢 Informações Básicas:
• Razão Social: ${empresa.razao_social}
• CNPJ: ${empresa.cnpj}
• Setor: ${empresa.cnae_descricao}
• Localização: ${empresa.bairro}
• Porte: ${empresa.porte}

📊 Indicadores de Performance:
• B/C Ratio: ${empresa.bc_ratio}x
• Impacto Líquido: R$ ${(empresa.impacto_liquido / 1000).toFixed(0)}k
• Ranking: ${empresasFiltradas.findIndex(e => e.id === empresa.id) + 1}° posição

💡 Em uma versão completa:
• Gráfico de evolução mensal
• Detalhes dos incentivos ativos
• Histórico de recolhimentos
• Alertas específicos da empresa`;
    
    alert(detalhes);
  };

  // Aplicar filtros
  const empresasFiltradas = empresas.filter(empresa => {
    const matchNome = empresa.razao_social?.toLowerCase().includes(filtro.toLowerCase());
    const matchCnpj = empresa.cnpj?.includes(filtro);
    const matchSetor = filtroSetor === '' || empresa.cnae_descricao === filtroSetor;
    const matchPorte = filtroPorte === '' || empresa.porte === filtroPorte;
    
    return (matchNome || matchCnpj) && matchSetor && matchPorte;
  });

  // Obter setores únicos para filtro
  const setoresUnicos = [...new Set(empresas.map(e => e.cnae_descricao))];
  const portesUnicos = [...new Set(empresas.map(e => e.porte))];

  return (
    <div className="page-content">
      <div className="page-header">
        <div className="header-content">
          <h1>🏢 Empresas</h1>
          <p>Gestão de empresas com incentivos fiscais ativos</p>
        </div>
        <div className="header-actions">
          <button 
            className="btn-outline"
            onClick={() => onChangeTab && onChangeTab('dashboard')}
          >
            ← Voltar ao Dashboard
          </button>
          <button 
            className="btn-primary"
            onClick={exportReport}
            aria-label="Exportar relatório de empresas"
          >
            📊 Exportar Relatório
          </button>
        </div>
      </div>

      <div className="content-card">
        {/* Filtros */}
        <div className="filters-section">
          <div className="filters-row">
            <input
              type="text"
              placeholder="🔍 Buscar por nome ou CNPJ..."
              value={filtro}
              onChange={(e) => setFiltro(e.target.value)}
              className="search-input"
            />
            
            <select 
              value={filtroSetor} 
              onChange={(e) => setFiltroSetor(e.target.value)}
              className="form-select"
            >
              <option value="">Todos os setores</option>
              {setoresUnicos.map(setor => (
                <option key={setor} value={setor}>{setor}</option>
              ))}
            </select>
            
            <select 
              value={filtroPorte} 
              onChange={(e) => setFiltroPorte(e.target.value)}
              className="form-select"
            >
              <option value="">Todos os portes</option>
              {portesUnicos.map(porte => (
                <option key={porte} value={porte}>{porte}</option>
              ))}
            </select>
            
            <button 
              className="btn-primary"
              onClick={() => onChangeTab && onChangeTab('upload')}
            >
              📁 Upload CSV
            </button>
          </div>
        </div>

        <div className="card-body">
          <div className="results-info">
            <p>Mostrando <strong>{empresasFiltradas.length}</strong> de <strong>{empresas.length}</strong> empresas</p>
          </div>

          {loading ? (
            <div className="loading-state">
              <div className="loading-spinner"></div>
              <p>Carregando empresas...</p>
            </div>
          ) : (
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Pos.</th>
                    <th>CNPJ</th>
                    <th>Razão Social</th>
                    <th>Setor</th>
                    <th>Bairro</th>
                    <th>Porte</th>
                    <th>B/C Ratio</th>
                    <th>Impacto Líquido</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {empresasFiltradas.map((empresa, index) => (
                    <tr key={empresa.id}>
                      <td className="position-cell">
                        {index < 3 ? ['🥇', '🥈', '🥉'][index] : `${index + 1}°`}
                      </td>
                      <td className="cnpj-cell">
                        <code>{empresa.cnpj}</code>
                      </td>
                      <td className="name-cell">
                        <strong>{empresa.razao_social}</strong>
                      </td>
                      <td>{empresa.cnae_descricao}</td>
                      <td>{empresa.bairro}</td>
                      <td>
                        <span className={`badge badge-${empresa.porte?.toLowerCase()}`}>
                          {empresa.porte}
                        </span>
                      </td>
                      <td className="ratio-cell">
                        <span className={`ratio-value ${empresa.bc_ratio >= 1.5 ? 'good' : empresa.bc_ratio >= 1.0 ? 'ok' : 'bad'}`}>
                          {empresa.bc_ratio}x
                        </span>
                      </td>
                      <td className="impact-cell">
                        <strong>R$ {(empresa.impacto_liquido / 1000).toFixed(0)}k</strong>
                      </td>
                      <td className="actions-cell">
                        <button 
                          className="btn-small btn-outline"
                          onClick={() => handleVerDetalhes(empresa)}
                        >
                          👁️ Ver
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              
              {empresasFiltradas.length === 0 && (
                <div className="empty-state">
                  <p>🔍 Nenhuma empresa encontrada com os filtros aplicados</p>
                  <button 
                    className="btn-outline"
                    onClick={() => {
                      setFiltro('');
                      setFiltroSetor('');
                      setFiltroPorte('');
                    }}
                  >
                    Limpar Filtros
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Estatísticas adicionais */}
      <div className="stats-section">
        <div className="stats-card">
          <h3>📊 Estatísticas Gerais</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Total de Empresas</span>
              <span className="stat-value">{empresas.length}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">B/C Ratio Médio</span>
              <span className="stat-value">
                {empresas.length > 0 ? 
                  (empresas.reduce((acc, emp) => acc + emp.bc_ratio, 0) / empresas.length).toFixed(1) + 'x' : 
                  '0x'
                }
              </span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Impacto Total</span>
              <span className="stat-value">
                R$ {(empresas.reduce((acc, emp) => acc + emp.impacto_liquido, 0) / 1000000).toFixed(1)}M
              </span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Empresas com B/C {'>'} 1.5</span>
              <span className="stat-value">
                {empresas.filter(emp => emp.bc_ratio > 1.5).length}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Empresas;
