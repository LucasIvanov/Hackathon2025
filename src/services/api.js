import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Serviços específicos para seu backend Django
export const dashboardService = {
  async getResumo() {
    const response = await api.get('/dashboard/resumo/');
    return response.data;
  }
};

export const empresasService = {
  async list(params = {}) {
    const response = await api.get('/empresas/', { params });
    return response.data;
  },
  
  async getDetalhes(cnpj) {
    const response = await api.get(`/empresas/${cnpj}/detalhe-completo/`);
    return response.data;
  }
};

export const calculosService = {
  async getRanking(tipo = 'melhores', limite = 10) {
    const response = await api.get('/calculos/ranking/', {
      params: { tipo, limite }
    });
    return response.data;
  },
  
  async list() {
    const response = await api.get('/calculos/');
    return response.data;
  }
};

export const alertasService = {
  async list() {
    const response = await api.get('/alertas/');
    return response.data;
  },
  
  async gerarAlertas() {
    const response = await api.post('/alertas/gerar-alertas/');
    return response.data;
  }
};

export default api;
