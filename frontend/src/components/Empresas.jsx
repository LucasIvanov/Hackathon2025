import { useEffect, useState } from "react";
import api from '../services/api';

export default function Empresas() {
  const [empresas, setEmpresas] = useState([]);

  useEffect(() => {
    api.get("/empresas/").then(res => setEmpresas(res.data.results));
  }, []);

  return (
    <div style={{ margin: 40 }}>
      <h2>Empresas</h2>
      <table border={1} cellPadding={5}>
        <thead>
          <tr>
            <th>CNPJ</th>
            <th>Razão Social</th>
            <th>Bairro</th>
            <th>Porte</th>
          </tr>
        </thead>
        <tbody>
          {empresas.map(emp => (
            <tr key={emp.cnpj}>
              <td>{emp.cnpj}</td>
              <td>{emp.razao_social}</td>
              <td>{emp.bairro}</td>
              <td>{emp.porte}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
