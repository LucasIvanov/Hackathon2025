import React, { useState, useEffect } from 'react';
import { exportarRelatorioCSV } from '../services/exportService';
import './Empresas.css';

const Empresas = () => {
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [exportando, setExportando] = useState(false);
  const [filtros, setFiltros] = useState({
    setor: 'todos',
    porte: 'todos',
    busca: ''
  });

  const buscarEmpresas = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/empresas/');
      const data = await response.json();
      setEmpresas(data);
    } catch (error) {
      setEmpresas([
        { id: 1, cnpj: '12345678000123', razao_social: 'Empresa Alpha Ltda', setor: 'Tecnologia', bairro: 'Centro', porte: 'ME', bc_ratio: '2.5', impacto_liquido: '450' },
        { id: 2, cnpj: '98765432000156', razao_social: 'Beta Comércio SA', setor: 'Comércio', bairro: 'Jardim Universitário', porte: 'GRANDE', bc_ratio: '2.1', impacto_liquido: '320' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleExportarRelatorio = async () => {
    setExportando(true);
    
    try {
      const resultado = await exportarRelatorioCSV(filtros);
      
      if (resultado.success) {
        alert('✅ ' + resultado.message);
      } else {
        alert('❌ ' + resultado.message);
      }
    } catch (error) {
      alert('❌ Erro ao exportar relatório');
    } finally {
      setExportando(false);
    }
  };

  useEffect(() => {
    buscarEmpresas();
  }, []);

  return (
    <div className="empresas-container">
      <div className="empresas-header">
        <h1>🏢 Empresas</h1>
        <p>Gestão de empresas com incentivos fiscais ativos</p>
      </div>

      <div className="empresas-acoes">
        <button 
          className="btn-voltar"
          onClick={() => window.location.href = '/dashboard'}
        >
          ← Voltar ao Dashboard
        </button>
        
        <button 
          className="btn-exportar"
          onClick={handleExportarRelatorio}
          disabled={exportando}
        >
          {exportando ? '⏳ Exportando...' : '📊 Exportar Relatório'}
        </button>
      </div>

      <div className="empresas-filtros">
        <input
          type="text"
          placeholder="🔍 Buscar por nome ou CNPJ..."
          value={filtros.busca}
          onChange={(e) => setFiltros({ ...filtros, busca: e.target.value })}
        />
        
        <select
          value={filtros.setor}
          onChange={(e) => setFiltros({ ...filtros, setor: e.target.value })}
        >
          <option value="todos">Todos os setores</option>
          <option value="Tecnologia">Tecnologia</option>
          <option value="Comércio">Comércio</option>
          <option value="Indústria">Indústria</option>
          <option value="Serviços">Serviços</option>
          <option value="Alimentação">Alimentação</option>
          <option value="Construção">Construção</option>
        </select>
        
        <select
          value={filtros.porte}
          onChange={(e) => setFiltros({ ...filtros, porte: e.target.value })}
        >
          <option value="todos">Todos os portes</option>
          <option value="ME">ME</option>
          <option value="GRANDE">GRANDE</option>
          <option value="EPP">EPP</option>
        </select>
        
        <button className="btn-upload">📤 Upload CSV</button>
      </div>

      {loading ? (
        <div className="loading">Carregando empresas...</div>
      ) : (
        <div className="empresas-tabela">
          <p>Mostrando {empresas.length} de {empresas.length} empresas</p>
          <table>
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
              {empresas.map((empresa, idx) => (
                <tr key={empresa.id || idx}>
                  <td>{idx + 1}</td>
                  <td>{empresa.cnpj}</td>
                  <td>{empresa.razao_social}</td>
                  <td>{empresa.setor}</td>
                  <td>{empresa.bairro}</td>
                  <td>
                    <span className={`badge-porte ${empresa.porte?.toLowerCase()}`}>
                      {empresa.porte}
                    </span>
                  </td>
                  <td className="bc-ratio">{empresa.bc_ratio}x</td>
                  <td className="impacto">R$ {empresa.impacto_liquido}k</td>
                  <td>
                    <button className="btn-ver">👁️ Ver</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Empresas;
