import React, { useState } from 'react';
import api from '../services/api';

const UpdateCSV = () => {
  const [file, setFile] = useState(null);
  const [uploadType, setUploadType] = useState('empresas');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setMessage('Por favor, selecione um arquivo CSV');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      let endpoint = '';
      switch (uploadType) {
        case 'empresas':
          endpoint = '/empresas/upload-csv/';
          break;
        case 'incentivos':
          endpoint = '/incentivos/upload-csv/';
          break;
        case 'iss':
          endpoint = '/arrecadacao-iss/upload-csv/';
          break;
        case 'iptu':
          endpoint = '/arrecadacao-iptu/upload-csv/';
          break;
        default:
          endpoint = '/empresas/upload-csv/';
      }

      const response = await api.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setMessage(`✅ Sucesso: ${response.data.message}`);
      setFile(null);
      // Reset file input
      e.target.reset();
      
    } catch (error) {
      console.error('Erro no upload:', error);
      const errorMsg = error.response?.data?.error || 'Erro ao fazer upload do arquivo';
      setMessage(`❌ Erro: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-md-8 mx-auto">
          <div className="card">
            <div className="card-header">
              <h3>📁 Upload de Arquivos CSV</h3>
            </div>
            <div className="card-body">
              <form onSubmit={handleUpload}>
                <div className="mb-3">
                  <label className="form-label">Tipo de Arquivo:</label>
                  <select
                    className="form-select"
                    value={uploadType}
                    onChange={(e) => setUploadType(e.target.value)}
                  >
                    <option value="empresas">Empresas</option>
                    <option value="incentivos">Incentivos</option>
                    <option value="iss">Arrecadação ISS</option>
                    <option value="iptu">Arrecadação IPTU</option>
                  </select>
                </div>
                
                <div className="mb-3">
                  <label className="form-label">Arquivo CSV:</label>
                  <input
                    type="file"
                    className="form-control"
                    accept=".csv"
                    onChange={handleFileChange}
                    disabled={loading}
                  />
                  <small className="form-text text-muted">
                    Apenas arquivos .csv são aceitos
                  </small>
                </div>

                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={loading || !file}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2"></span>
                      Enviando...
                    </>
                  ) : (
                    '📤 Fazer Upload'
                  )}
                </button>
              </form>

              {message && (
                <div className={`alert mt-3 ${message.includes('✅') ? 'alert-success' : 'alert-danger'}`}>
                  {message}
                </div>
              )}
            </div>
          </div>

          {/* Guia de formatos */}
          <div className="card mt-4">
            <div className="card-header">
              <h5>📋 Formato dos Arquivos CSV</h5>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col-md-6">
                  <h6>Empresas:</h6>
                  <code>cnpj,razao_social,bairro</code>
                </div>
                <div className="col-md-6">
                  <h6>Incentivos:</h6>
                  <code>cnpj,instrumento_legal,tipo_incentivo,percentual_desconto,data_inicio</code>
                </div>
              </div>
              <div className="row mt-3">
                <div className="col-md-6">
                  <h6>Arrecadação ISS:</h6>
                  <code>cnpj,mes_ref,valor_iss</code>
                </div>
                <div className="col-md-6">
                  <h6>Arrecadação IPTU:</h6>
                  <code>cnpj,ano_ref,valor_iptu,valor_taxas</code>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UpdateCSV;
