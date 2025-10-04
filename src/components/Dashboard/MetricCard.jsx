import React from 'react';

const MetricCard = ({ 
  title, 
  value, 
  icon, 
  color = "blue", 
  trend, 
  trendValue, 
  prefix = "R$" 
}) => {
  const colorClasses = {
    blue: "from-blue-500 to-blue-600",
    green: "from-green-500 to-green-600", 
    orange: "from-orange-500 to-orange-600",
    purple: "from-purple-500 to-purple-600"
  };

  const iconBgColors = {
    blue: "#4285f4",
    green: "#34a853",
    orange: "#ff9800", 
    purple: "#9c27b0"
  };

  return (
    <div className="metric-card">
      <div className="metric-header">
        <div className="metric-title">{title}</div>
        <div 
          className="metric-icon"
          style={{ backgroundColor: iconBgColors[color] }}
        >
          {icon}
        </div>
      </div>
      
      <div className="metric-value">
        {prefix !== "" && <span className="metric-prefix">{prefix}</span>}
        <span className="metric-number">{value}</span>
      </div>
      
      {trend && trendValue && (
        <div className="metric-trend">
          <div className={`trend-indicator ${trend === 'up' ? 'positive' : 'negative'}`}>
            <span className="trend-icon">
              {trend === 'up' ? '📈' : '📉'}
            </span>
            <span className="trend-value">{trendValue}</span>
          </div>
          <span className="trend-label">vs. mês anterior</span>
        </div>
      )}
    </div>
  );
};

export default MetricCard;
