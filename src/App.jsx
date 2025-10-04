import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import Empresas from './components/Empresas'
import UpdateCSV from './components/UpdateCSV'
import Login from './pages/Login'
import 'bootstrap/dist/css/bootstrap.min.css'

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navbar */}
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
          <div className="container">
            <a className="navbar-brand" href="/">
              🏛️ SEMDEC - Incentivos Fiscais
            </a>
            <div className="navbar-nav ms-auto">
              <a className="nav-link" href="/">Dashboard</a>
              <a className="nav-link" href="/empresas">Empresas</a>
              <a className="nav-link" href="/upload">Upload</a>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <div className="container-fluid mt-4">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/empresas" element={<Empresas />} />
            <Route path="/upload" element={<UpdateCSV />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App
