import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import './Login.css';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    senha: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError(''); // Limpar erro ao digitar
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.username || !formData.senha) {
      setError('Por favor, preencha todos os campos');
      return;
    }

    setLoading(true);
    setError('');

    const result = await login(formData.username, formData.senha);

    if (!result.success) {
      setError(result.error);
    }

    setLoading(false);
  };

  // Usuários de demonstração
  const usuariosDemo = [
    { username: 'admin', senha: 'admin123', nome: 'Administrador', cargo: 'Coordenador' },
    { username: 'analista1', senha: 'senha123', nome: 'Analista Fiscal', cargo: 'Analista' },
    { username: 'gestor', senha: 'gestor123', nome: 'Gerente', cargo: 'Gerente' }
  ];

  const preencherDemo = (usuario) => {
    setFormData({
      username: usuario.username,
      senha: usuario.senha
    });
    setError('');
  };

  return (
    <div className="login-container">
      <div className="login-background">
        <div className="background-pattern"></div>
      </div>
      
      <div className="login-content">
        <div className="login-card">
          <div className="login-header">
            <div className="login-logo">
              <div className="logo-icon">📈</div>
              <div className="logo-text">
                <h1>FiscalTracker</h1>
                <p>Sistema de Incentivos Fiscais</p>
              </div>
            </div>
          </div>

          <div className="login-body">
            <h2>Acesso ao Sistema</h2>
            <p className="login-subtitle">SEMDEC - Secretaria Municipal de Desenvolvimento Econômico</p>

            <form onSubmit={handleSubmit} className="login-form">
              <div className="form-group">
                <label htmlFor="username">Usuário:</label>
                <input
                  type="text"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleInputChange}
                  placeholder="Digite seu usuário"
                  disabled={loading}
                  autoComplete="username"
                />
              </div>

              <div className="form-group">
                <label htmlFor="senha">Senha:</label>
                <input
                  type="password"
                  id="senha"
                  name="senha"
                  value={formData.senha}
                  onChange={handleInputChange}
                  placeholder="Digite sua senha"
                  disabled={loading}
                  autoComplete="current-password"
                />
              </div>

              {error && (
                <div className="error-message">
                  ❌ {error}
                </div>
              )}

              <button
                type="submit"
                className={`login-button ${loading ? 'loading' : ''}`}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Entrando...
                  </>
                ) : (
                  <>
                    🔐 Entrar no Sistema
                  </>
                )}
              </button>
            </form>

            {/* Usuários de demonstração */}
            <div className="demo-users">
              <h4>👤 Usuários de Demonstração:</h4>
              <div className="demo-buttons">
                {usuariosDemo.map((usuario, index) => (
                  <button
                    key={index}
                    type="button"
                    className="demo-button"
                    onClick={() => preencherDemo(usuario)}
                    disabled={loading}
                  >
                    <div className="demo-info">
                      <strong>{usuario.nome}</strong>
                      <small>{usuario.cargo}</small>
                      <code>({usuario.username}/{usuario.senha})</code>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="login-footer">
            <p>© 2025 Prefeitura de Cascavel - SEMDEC</p>
            <p>Hackathon FUNDETEC 2025</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
