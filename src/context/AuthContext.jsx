import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    // Recuperar usuário do localStorage ao inicializar
    const savedUser = localStorage.getItem('user');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const login = async (username, senha) => {
    try {
      console.log('🔐 Fazendo login:', username);
      
      const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, senha }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        console.log('✅ Login realizado:', data.usuario.nome_completo);
        
        setUser(data.usuario);
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.usuario));
        
        return { success: true, user: data.usuario };
      } else {
        console.log('❌ Erro no login:', data.error);
        return { success: false, error: data.error || 'Erro no login' };
      }
    } catch (error) {
      console.error('❌ Erro de conexão:', error);
      return { success: false, error: 'Erro de conexão com o servidor' };
    }
  };

  const logout = () => {
    console.log('🚪 Logout realizado');
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const value = {
    user,
    login,
    logout,
    loading: false, // Simplificado para protótipo
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
