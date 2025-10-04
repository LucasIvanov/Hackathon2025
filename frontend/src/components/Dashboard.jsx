import { useEffect, useState } from "react";
import api from '../services/api';

export default function Dashboard() {
  const [kpi, setKPI] = useState(null);

  useEffect(() => {
    api.get("/dashboard/resumo/").then(res => setKPI(res.data));
  }, []);

  if (!kpi) return <div>Carregando...</div>;

  return (
    <div style={{ margin: 40 }}>
      <h2>Dashboard SEMDEC</h2>
      <div style={{ display: "flex", gap: 40 }}>
        <div><b>Empresas Ativas:</b> {kpi.total_empresas}</div>
        <div><b>Incentivos Ativos:</b> {kpi.total_incentivos_ativos}</div>
        <div><b>Custo Fiscal Total:</b> R$ {kpi.custo_fiscal_total.toLocaleString("pt-br")}</div>
        <div><b>B/C Médio:</b> {Number(kpi.bc_medio).toFixed(2)}</div>
        <div><b>Alertas Ativos:</b> {kpi.total_alertas_ativos}</div>
      </div>
    </div>
  );
}
