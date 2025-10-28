import { useState, useEffect } from 'react';
import { useNavigate, useOutletContext, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const { showToast } = useOutletContext();

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  const validateForm = () => {
    const newErrors = {};
    if (!username.trim()) {
      newErrors.username = 'Username is required';
    }
    if (!password) {
      newErrors.password = 'Password is required';
    } else if (password.length < 4) {
      newErrors.password = 'Password must be at least 4 characters';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setIsLoading(true);
    setErrors({});

    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch('http://127.0.0.1:8000/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        login({ 
          username: data.user, 
          role: data.role || 'user',
          email: data.email || `${data.user}@greenmatchers.com`
        }, data.access_token);
        
        showToast('🎉 Welcome back! Login successful', 'success');
        navigate('/dashboard');
      } else {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Invalid credentials');
      }
    } catch (error) {
      console.error('Login error:', error);
      showToast(error.message || 'Login failed. Please check your credentials.', 'error');
      setErrors({ general: error.message });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = () => {
    setUsername('demo');
    setPassword('demo');
  };

  return (
    <div className="max-w-md mx-auto">
      <div className="glass-effect rounded-2xl p-8 shadow-2xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-teal-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg animate-float">
            <span className="text-3xl">🌱</span>
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
          <p className="text-slate-300">Sign in to your Green Matchers account</p>
        </div>

        {/* General Error */}
        {errors.general && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 rounded-xl text-red-400 text-sm">
            {errors.general}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Username Field */}
          <div>
            <label className="block text-white mb-2 font-medium text-sm">
              Username
            </label>
            <div className="relative">
              <input
                type="text"
                value={username}
                onChange={(e) => {
                  setUsername(e.target.value);
                  if (errors.username) setErrors(prev => ({ ...prev, username: null }));
                }}
                className={`w-full px-4 py-3 bg-slate-700 border ${
                  errors.username ? 'border-red-500' : 'border-slate-600'
                } rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-green-500 transition-all`}
                placeholder="Enter your username"
                disabled={isLoading}
              />
              <span className="absolute right-4 top-3.5 text-slate-400">👤</span>
            </div>
            {errors.username && (
              <p className="text-red-400 text-xs mt-1">{errors.username}</p>
            )}
          </div>

          {/* Password Field */}
          <div>
            <label className="block text-white mb-2 font-medium text-sm">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  if (errors.password) setErrors(prev => ({ ...prev, password: null }));
                }}
                className={`w-full px-4 py-3 bg-slate-700 border ${
                  errors.password ? 'border-red-500' : 'border-slate-600'
                } rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-green-500 transition-all pr-12`}
                placeholder="Enter your password"
                disabled={isLoading}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-3.5 text-slate-400 hover:text-white transition-colors"
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            {errors.password && (
              <p className="text-red-400 text-xs mt-1">{errors.password}</p>
            )}
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 text-white py-3 rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-green-500/25 transform hover:scale-[1.02] active:scale-[0.98]"
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                Signing in...
              </div>
            ) : (
              <span className="flex items-center justify-center gap-2">
                <span>Sign In</span>
                <span>→</span>
              </span>
            )}
          </button>
        </form>

        {/* Demo Credentials */}
        <div className="mt-6">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-600"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-slate-800 text-slate-400">Quick Access</span>
            </div>
          </div>
          
          <button
            type="button"
            onClick={handleDemoLogin}
            className="w-full mt-4 bg-slate-700 hover:bg-slate-600 text-white py-3 rounded-xl font-medium transition-colors border border-slate-600"
          >
            🚀 Try Demo Account
          </button>
          
          <p className="text-slate-400 text-xs text-center mt-3">
            Demo: <span className="text-green-400">username: demo</span> | <span className="text-green-400">password: demo</span>
          </p>
        </div>

        {/* Footer Links */}
        <div className="mt-6 text-center">
          <Link 
            to="/" 
            className="text-slate-400 hover:text-white text-sm transition-colors"
          >
            ← Back to Home
          </Link>
        </div>
      </div>

      {/* Additional Info */}
      <div className="mt-6 text-center">
        <p className="text-slate-400 text-sm">
          New to Green Matchers?{' '}
          <span className="text-green-400">Contact admin for access</span>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;