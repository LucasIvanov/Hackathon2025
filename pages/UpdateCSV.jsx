import api from "../api/axios.jsx";
import { useState } from "react";

export default function UploadCSV() {
  const [msg, setMsg] = useState("");

  const uploadFile = async (endpoint) => {
    setMsg("");
    const file = document.getElementById(endpoint).files[0];
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await api.post(endpoint, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMsg(JSON.stringify(res.data));
    } catch (err) {
      setMsg("Erro no upload: " + (err?.response?.data?.error || err.message));
    }
  };

  return (
    <div style={{ margin: 40 }}>
      <h2>Upload de Base CSV</h2>
      <div>
        <label>Empresas:
          <input type="file" id="empresas" accept=".csv" />
          <button onClick={() => uploadFile("/empresas/upload-csv/")}>Upload Empresas</button>
        </label>
      </div>
      <div>
        <label>Incentivos:
          <input type="file" id="incentivos" accept=".csv" />
          <button onClick={() => uploadFile("/incentivos/upload-csv/")}>Upload Incentivos</button>
        </label>
      </div>
      <div>
        <label>Arrecadação ISS:
          <input type="file" id="arrecadacao-iss" accept=".csv" />
          <button onClick={() => uploadFile("/arrecadacao-iss/upload-csv/")}>Upload ISS</button>
        </label>
      </div>
      <div style={{ marginTop: 10, color: "#660" }}>{msg}</div>
    </div>
  );
}
