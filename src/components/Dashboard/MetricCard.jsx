import React from 'react';

const MetricCard = ({ title, value, change, changeType, color, icon }) => {
  return (
    <div className={`metric-card ${color}`}>
      <div className="metric-header">
        <h3 className="metric-title">{title}</h3>
        <div className={`metric-icon ${color}`}>
          {icon}
        </div>
      </div>
      
      <div className="metric-value">
        {value}
      </div>
      
      <div className="metric-change">
        <span className={`change-indicator ${changeType}`}>
          {changeType === 'positive' ? '📈' : '📉'} {change}
        </span>
        <span className="change-label">vs. mês anterior</span>
      </div>
    </div>
  );
};

export default MetricCard;
