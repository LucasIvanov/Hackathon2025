import React, { useState, useEffect } from 'react';
import { empresasService } from '../../services/api';

const Empresas = () => {
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filtro, setFiltro] = useState('');

  useEffect(() => {
    carregarEmpresas();
  }, []);

  const carregarEmpresas = async () => {
    try {
      setLoading(true);
      const data = await empresasService.list();
      setEmpresas(Array.isArray(data) ? data : data.results || []);
    } catch (error) {
      console.error('Erro ao carregar empresas:', error);
      // Dados simulados em caso de erro
      setEmpresas([
        {
          id: 1,
          cnpj: '12345678000123',
          razao_social: 'Empresa Exemplo Ltda',
          cnae_descricao: 'Comércio Varejista',
          bairro: 'Centro',
          porte: 'ME'
        },
        {
          id: 2, 
          cnpj: '98765432000156',
          razao_social: 'Tecnologia Cascavel SA',
          cnae_descricao: 'Desenvolvimento de Software',
          bairro: 'Jardim Universitário',
          porte: 'GRANDE'
        }
      ]);
    }
    setLoading(false);
  };

  const empresasFiltradas = empresas.filter(empresa =>
    empresa.razao_social?.toLowerCase().includes(filtro.toLowerCase()) ||
    empresa.cnpj?.includes(filtro)
  );

  return (
    <div className="page-content">
      <div className="page-header">
        <h1>🏢 Empresas</h1>
        <p>Gestão de empresas cadastradas no sistema</p>
      </div>

      <div className="content-card">
        <div className="card-header">
          <h3>Lista de Empresas</h3>
          <div className="header-actions">
            <input
              type="text"
              placeholder="Filtrar por nome ou CNPJ..."
              value={filtro}
              onChange={(e) => setFiltro(e.target.value)}
              className="search-input"
            />
            <button className="btn-primary">
              📁 Upload CSV
            </button>
          </div>
        </div>

        <div className="card-body">
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
                    <th>CNPJ</th>
                    <th>Razão Social</th>
                    <th>Setor</th>
                    <th>Bairro</th>
                    <th>Porte</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {empresasFiltradas.map(empresa => (
                    <tr key={empresa.id}>
                      <td className="cnpj-cell">{empresa.cnpj}</td>
                      <td className="name-cell">{empresa.razao_social}</td>
                      <td>{empresa.cnae_descricao}</td>
                      <td>{empresa.bairro}</td>
                      <td>
                        <span className={`badge badge-${empresa.porte?.toLowerCase()}`}>
                          {empresa.porte}
                        </span>
                      </td>
                      <td>
                        <button className="btn-small btn-outline">
                          👁️ Ver
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              
              {empresasFiltradas.length === 0 && (
                <div className="empty-state">
                  <p>Nenhuma empresa encontrada</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Empresas;
