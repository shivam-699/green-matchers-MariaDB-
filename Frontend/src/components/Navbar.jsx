import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { useState } from 'react';
import LanguageSelector from './LanguageSelector';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { t } = useLanguage();
  const location = useLocation();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsMenuOpen(false);
  };

  const navItems = [
    { path: '/', label: t('nav.home'), icon: '🏠' },
    { path: '/job-search', label: t('nav.jobs'), icon: '🔍' },
    { path: '/dashboard', label: t('nav.dashboard'), icon: '📊' },
    { path: '/trends', label: t('nav.trends'), icon: '📈' },
    { path: '/career-path', label: t('nav.careerPath'), icon: '🚀' },
  ];

  return (
    <>
      <style>{`
        @keyframes slide-down {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .animate-slide-down {
          animation: slide-down 0.3s ease-out;
        }
      `}</style>

      <nav className="sticky top-0 z-50 backdrop-blur-xl bg-slate-900/80 border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            
            {/* Logo */}
            <Link 
              to="/" 
              className="flex items-center gap-3 group"
              onClick={() => setIsMenuOpen(false)}
            >
              <div className="w-11 h-11 bg-gradient-to-br from-emerald-400 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-emerald-500/30 group-hover:shadow-emerald-500/50 transition-all group-hover:scale-105 text-2xl">
                ✨
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-bold text-white leading-tight">Green Matchers</span>
                <span className="text-xs text-emerald-400 font-semibold leading-tight">AI-Powered Platform</span>
              </div>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center gap-2">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-2 px-5 py-2.5 rounded-xl transition-all duration-300 font-medium ${
                    location.pathname === item.path
                      ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg shadow-blue-500/30'
                      : 'text-slate-300 hover:bg-white/5 hover:text-white'
                  }`}
                >
                  <span className="text-lg">{item.icon}</span>
                  <span>{item.label}</span>
                </Link>
              ))}
            </div>

            {/* User Section */}
            <div className="flex items-center gap-4">
              {/* LANGUAGE SELECTOR */}
              <LanguageSelector />
              
              {user ? (
                <div className="flex items-center gap-3">
                  {/* User Info - Desktop */}
                  <div className="hidden sm:flex items-center gap-3">
                    <div className="text-right">
                      <p className="text-white font-semibold text-sm leading-tight">{user.username}</p>
                      <p className="text-emerald-400 text-xs leading-tight font-medium">{t('nav.premiumMember')}</p>
                    </div>
                    <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center text-white font-bold shadow-lg">
                      {user.username.charAt(0).toUpperCase()}
                    </div>
                  </div>

                  {/* Logout Button - Desktop */}
                  <button
                    onClick={handleLogout}
                    className="hidden sm:flex items-center gap-2 px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl transition-all font-medium border border-slate-700 hover:border-slate-600"
                  >
                    <span>🚪</span>
                    <span>{t('nav.logout')}</span>
                  </button>
                </div>
              ) : (
                <Link
                  to="/login"
                  className="hidden sm:flex items-center gap-2 px-7 py-2.5 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white rounded-xl transition-all font-semibold shadow-lg shadow-blue-500/30 hover:shadow-xl hover:scale-105"
                >
                  <span>👤</span>
                  <span>{t('nav.signIn')}</span>
                </Link>
              )}

              {/* Mobile Menu Button */}
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="md:hidden p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 transition-colors border border-slate-700"
                aria-label="Toggle menu"
              >
                <span className="text-white text-xl">{isMenuOpen ? '✕' : '☰'}</span>
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <div className="md:hidden py-4 border-t border-white/5 animate-slide-down">
              <div className="space-y-2">
                {/* LANGUAGE SELECTOR IN MOBILE MENU */}
                <div className="px-4 py-2">
                  <LanguageSelector />
                </div>
                
                {navItems.map((item) => (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setIsMenuOpen(false)}
                    className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-medium ${
                      location.pathname === item.path
                        ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg'
                        : 'text-slate-300 hover:bg-white/5 hover:text-white'
                    }`}
                  >
                    <span className="text-xl">{item.icon}</span>
                    <span>{item.label}</span>
                  </Link>
                ))}

                {/* Mobile User Section */}
                {user ? (
                  <>
                    <div className="flex items-center gap-3 px-4 py-3 bg-slate-800/50 rounded-xl mt-4">
                      <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center text-white font-bold">
                        {user.username.charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <p className="text-white font-semibold text-sm">{user.username}</p>
                        <p className="text-emerald-400 text-xs font-medium">{t('nav.premiumMember')}</p>
                      </div>
                    </div>
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-red-500 hover:bg-red-600 text-white rounded-xl transition-all font-medium"
                    >
                      <span>🚪</span>
                      <span>{t('nav.logout')}</span>
                    </button>
                  </>
                ) : (
                  <Link
                    to="/login"
                    onClick={() => setIsMenuOpen(false)}
                    className="flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold mt-4"
                  >
                    <span>👤</span>
                    <span>{t('nav.signIn')}</span>
                  </Link>
                )}
              </div>
            </div>
          )}
        </div>
      </nav>
    </>
  );
};

export default Navbar;