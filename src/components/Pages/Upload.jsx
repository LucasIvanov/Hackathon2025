import React, { useState } from 'react';

const Upload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadType, setUploadType] = useState('empresas');
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setMessage('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage('❌ Por favor, selecione um arquivo');
      return;
    }

    setUploading(true);
    setMessage('⏳ Fazendo upload...');

    // Simular upload
    setTimeout(() => {
      setUploading(false);
      setMessage(`✅ Upload realizado com sucesso! Arquivo: ${selectedFile.name}`);
      setSelectedFile(null);
    }, 2000);
  };

  const uploadTypes = [
    { value: 'empresas', label: '🏢 Empresas', format: 'cnpj,razao_social,bairro' },
    { value: 'incentivos', label: '💰 Incentivos', format: 'cnpj,tipo_incentivo,percentual' },
    { value: 'iss', label: '📊 Arrecadação ISS', format: 'cnpj,mes_ref,valor_iss' },
    { value: 'iptu', label: '🏠 Arrecadação IPTU', format: 'cnpj,ano_ref,valor_iptu' }
  ];

  return (
    <div className="page-content">
      <div className="page-header">
        <h1>📁 Upload de Dados</h1>
        <p>Importar arquivos CSV para o sistema</p>
      </div>

      <div className="upload-container">
        <div className="upload-card">
          <div className="upload-header">
            <h3>Selecionar Tipo de Arquivo</h3>
          </div>
          
          <div className="upload-body">
            <div className="form-group">
              <label>Tipo de dados:</label>
              <select 
                value={uploadType} 
                onChange={(e) => setUploadType(e.target.value)}
                className="form-select"
              >
                {uploadTypes.map(type => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Arquivo CSV:</label>
              <div className="file-input-container">
                <input
                  type="file"
                  id="file-input"
                  accept=".csv"
                  onChange={handleFileSelect}
                  className="file-input"
                />
                <label htmlFor="file-input" className="file-input-label">
                  {selectedFile ? selectedFile.name : 'Escolher arquivo...'}
                </label>
              </div>
            </div>

            <button
              onClick={handleUpload}
              disabled={!selectedFile || uploading}
              className={`upload-button ${uploading ? 'uploading' : ''}`}
            >
              {uploading ? '⏳ Enviando...' : '📤 Fazer Upload'}
            </button>

            {message && (
              <div className={`message ${message.includes('❌') ? 'error' : 'success'}`}>
                {message}
              </div>
            )}
          </div>
        </div>

        {/* Formato do arquivo */}
        <div className="format-card">
          <h4>📋 Formato Esperado</h4>
          <div className="format-info">
            <p><strong>Tipo selecionado:</strong> {uploadTypes.find(t => t.value === uploadType)?.label}</p>
            <p><strong>Formato CSV:</strong></p>
            <code>{uploadTypes.find(t => t.value === uploadType)?.format}</code>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Upload;
