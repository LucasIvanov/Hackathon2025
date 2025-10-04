import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function ImpactChart({ data }) {
  if (!data || !data.labels) {
    return (
      <div className="chart-card">
        <div className="chart-header">
          <h3 className="chart-title">Tendência de Impacto Fiscal (12 meses)</h3>
        </div>
        <div className="chart-loading">
          <div className="loading-spinner"></div>
          <p>Carregando dados do gráfico...</p>
        </div>
      </div>
    );
  }

  // Transformar dados para o formato do Recharts
  const chartData = data.labels.map((label, index) => ({
    mes: label,
    custos: data.custos[index] || 0,
    retornos: data.retornos[index] || 0,
    liquido: (data.retornos[index] || 0) - (data.custos[index] || 0)
  }));

  const formatCurrency = (value) => {
    return `R$ ${(value / 1000).toFixed(0)}k`;
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="chart-tooltip">
          <p className="tooltip-label">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} className="tooltip-item" style={{ color: entry.color }}>
              {entry.name}: {formatCurrency(entry.value)}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="chart-card">
      <div className="chart-header">
        <h3 className="chart-title">Tendência de Impacto Fiscal (12 meses)</h3>
      </div>
      
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e8eaed" />
            <XAxis 
              dataKey="mes" 
              stroke="#5f6368"
              fontSize={12}
            />
            <YAxis 
              stroke="#5f6368"
              fontSize={12}
              tickFormatter={formatCurrency}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="retornos" 
              stroke="#34a853" 
              strokeWidth={3}
              name="Retorno Fiscal"
              dot={{ fill: '#34a853', r: 4 }}
            />
            <Line 
              type="monotone" 
              dataKey="custos" 
              stroke="#4285f4" 
              strokeWidth={3}
              name="Custo Fiscal"
              dot={{ fill: '#4285f4', r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
