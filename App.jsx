import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Empresas from "./pages/Empresas";
import UploadCSV from "./pages/UploadCSV";
import Login from "./pages/Login";
import { setAuthToken } from "./api/axios";

export default function App() {
  const [isAuth, setIsAuth] = useState(!!localStorage.getItem("token"));

  useEffect(() => {
    if (isAuth) setAuthToken(localStorage.getItem("token"));
  }, [isAuth]);

  if (!isAuth) return <Login onLogin={setIsAuth} />;

  return (
    <Router>
      <nav style={{ margin: 20 }}>
        <Link to="/">Dashboard</Link> | <Link to="/empresas">Empresas</Link> | <Link to="/upload">Upload CSV</Link>
        <button style={{ float: "right" }} onClick={() => {localStorage.clear(); setIsAuth(false)}}>Sair</button>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/empresas" element={<Empresas />} />
        <Route path="/upload" element={<UploadCSV />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}
