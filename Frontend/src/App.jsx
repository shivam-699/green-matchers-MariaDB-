import { useState, useEffect } from 'react';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import LoadingSpinner from './components/LoadingSpinner';
import Toast from './components/Toast';
import ParticleBackground from './components/ParticleBackground';

function AppContent() {
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(null);
  const { user, login } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  // Initialize user from localStorage
  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      try {
        login(JSON.parse(userData));
      } catch (error) {
        console.error('Error parsing user data:', error);
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      }
    }
    
    const timer = setTimeout(() => setLoading(false), 800);
    return () => clearTimeout(timer);
  }, [login]);

  // Scroll reveal observer
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
          }
        });
      },
      { 
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      }
    );
    
    const elements = document.querySelectorAll('.scroll-reveal, .reveal');
    elements.forEach((el) => observer.observe(el));
    
    return () => observer.disconnect();
  }, [location.pathname]);

  // Toast notification function
  const showToast = (message, type = 'info') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  // Loading screen
  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%)' }}>
      {/* Background Animation - ALWAYS BEHIND EVERYTHING */}
      {location.pathname === '/' && <ParticleBackground />}
      
      {/* Navigation - Fixed at top */}
      <div style={{ position: 'relative', zIndex: 50 }}>
        <Navbar />
      </div>

      {/* Main Content Wrapper - Centered with padding */}
      <main style={{ position: 'relative', zIndex: 10, width: '100%', maxWidth: '1200px', margin: '0 auto', padding: '2rem 2rem' }}>
        <Outlet context={{ showToast, user }} />
      </main>

      {/* Toast Notifications */}
      {toast && (
        <Toast 
          message={toast.message} 
          type={toast.type} 
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;