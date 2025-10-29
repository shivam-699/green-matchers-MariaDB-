import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import App from './App.jsx'
import Home from './pages/Home.jsx'
import { LanguageProvider } from './context/LanguageContext.jsx'
import { AuthProvider } from './context/AuthContext.jsx'
import LoginPage from './pages/LoginPage.jsx'
import JobSearch from './pages/JobSearch.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Trends from './pages/Trends.jsx'
import CareerPathPage from './pages/CareerPathPage.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <LanguageProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<App />}>
              <Route index element={<Home />} />
              <Route path="login" element={<LoginPage />} />
              <Route path="job-search" element={<JobSearch />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="trends" element={<Trends />} />
              <Route path="career-path" element={<CareerPathPage />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </LanguageProvider>
  </React.StrictMode>
)