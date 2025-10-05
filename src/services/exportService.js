export const exportarRelatorioCSV = async (filtros = {}) => {
  try {
    const params = new URLSearchParams();
    
    if (filtros.setor && filtros.setor !== 'todos') {
      params.append('setor', filtros.setor);
    }
    if (filtros.porte && filtros.porte !== 'todos') {
      params.append('porte', filtros.porte);
    }
    if (filtros.busca) {
      params.append('busca', filtros.busca);
    }
    
    const url = `http://localhost:8000/api/empresas/exportar/?${params.toString()}`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'text/csv',
      },
    });
    
    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`);
    }
    
    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    
    const dataHora = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    link.download = `relatorio_empresas_${dataHora}.csv`;
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(downloadUrl);
    
    return { success: true, message: 'Relatório exportado com sucesso!' };
    
  } catch (error) {
    return { 
      success: false, 
      message: `Erro ao exportar relatório: ${error.message}` 
    };
  }
};
