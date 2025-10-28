import { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_jobs: 0,
    companies: 0,
    sdg_goals: 0,
    favorites: 0,
    applications: 0,
    profile_views: 0
  });
  const [chartData, setChartData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [timeOfDay, setTimeOfDay] = useState('');
  const { user } = useAuth();

  // Determine time-based greeting
  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setTimeOfDay('Morning');
    else if (hour < 17) setTimeOfDay('Afternoon');
    else setTimeOfDay('Evening');
  }, []);

  // ✅ RECOMMENDATION FOR HACKATHON:
  // Use the polling approach - it's more reliable and achieves the same "live updates" effect without WebSocket complexity. The polling version I provided will:
  // ✅ Update stats every 15 seconds
  // ✅ Work reliably without WebSocket issues
  // ✅ Show the same real-time effect to users
  // ✅ Be easier to debug and demo

  // Real-time stats updates using polling (more reliable for demo)
  useEffect(() => {
    if (!user) return;
  
    const pollStats = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:8000/stats', {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });
        
        if (response.ok) {
          const statsData = await response.json();
          setStats(prev => ({
            ...prev,
            total_jobs: statsData.total_jobs,
            companies: statsData.companies
          }));
          console.log('📊 Updated stats via polling');
        }
      } catch (error) {
        console.error('Polling error:', error);
      }
    };
  
    // Poll every 15 seconds for live updates
    const interval = setInterval(pollStats, 15000);
    
    // Initial poll
    pollStats();
  
    return () => clearInterval(interval);
  }, [user]);

  // Fetch dashboard data on initial load
  useEffect(() => {
    if (user) {
      fetchDashboardData();
    }
  }, [user]);

  const fetchDashboardData = async () => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      
      if (!token) {
        throw new Error('No authentication token found');
      }

      // Fetch stats from backend
      const statsResponse = await fetch('http://127.0.0.1:8000/stats', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats({
          total_jobs: statsData.total_jobs || 0,
          companies: statsData.companies || 0,
          sdg_goals: statsData.sdg_goals || 0,
          favorites: statsData.favorites || 0,
          applications: statsData.applications || 0, 
          profile_views: statsData.profile_views || 0 
        });
      }

      // Fetch chart data from backend
      const chartResponse = await fetch('http://127.0.0.1:8000/dashboard', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (chartResponse.ok) {
        const chartData = await chartResponse.json();
        // Transform backend chart data to frontend format if needed
        if (chartData.chart && chartData.chart.data) {
          setChartData(chartData.chart.data.datasets[0].data);
        }
      }

    } catch (error) {
      console.error('Dashboard data fetch failed:', error);
      // Fallback to mock data if API fails
      setStats({
        total_jobs: 547,
        companies: 52,
        sdg_goals: 15,
        favorites: 12,
        applications: 8,
        profile_views: 143
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Calculate completion percentage
  const profileCompletion = useMemo(() => {
    if (!user) return 0;
    const fields = ['username', 'email', 'skills', 'location', 'bio'];
    const completed = fields.filter(field => user[field]).length;
    return Math.round((completed / fields.length) * 100);
  }, [user]);

  if (!user) {
    return (
      <div className="max-w-2xl mx-auto text-center py-12">
        <div className="glass-effect rounded-2xl p-12">
          <div className="text-6xl mb-6 animate-bounce">🔒</div>
          <h2 className="text-3xl font-bold text-white mb-4">Authentication Required</h2>
          <p className="text-slate-300 mb-8 text-lg">Please login to access your personalized dashboard</p>
          <Link
            to="/login"
            className="bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600 text-white px-8 py-4 rounded-xl transition-all inline-block font-semibold shadow-lg transform hover:scale-105"
          >
            Go to Login →
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto w-full space-y-8">
      {/* Welcome Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-3">
          Good {timeOfDay}, {user.username}! 👋
        </h1>
        <p className="text-slate-300 text-lg">
          Your green career dashboard is ready
        </p>
      </div>

      {isLoading ? (
        <div className="flex justify-center items-center py-20">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-2xl">🌱</span>
            </div>
          </div>
        </div>
      ) : (
        <>
          {/* Profile Completion Banner */}
          {profileCompletion < 100 && (
            <div className="glass-effect rounded-2xl p-6 bg-gradient-to-r from-orange-500/10 to-yellow-500/10 border border-orange-500/30">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                  ⚡ Complete Your Profile
                </h3>
                <span className="text-yellow-400 font-bold">{profileCompletion}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-3 mb-3">
                <div 
                  className="bg-gradient-to-r from-orange-500 to-yellow-500 h-3 rounded-full transition-all duration-500"
                  style={{ width: `${profileCompletion}%` }}
                ></div>
              </div>
              <p className="text-slate-300 text-sm">
                Complete your profile to get better job matches and increase visibility to employers
              </p>
            </div>
          )}

          {/* Stats Grid */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {[
              { icon: '💼', value: stats.total_jobs, label: 'Available Jobs', color: 'from-blue-500 to-blue-600', emoji: '📈' },
              { icon: '🏢', value: stats.companies, label: 'Companies', color: 'from-teal-500 to-teal-600', emoji: '🏆' },
              { icon: '🌍', value: stats.sdg_goals, label: 'SDG Goals', color: 'from-purple-500 to-purple-600', emoji: '🎯' },
              { icon: '⭐', value: stats.favorites, label: 'Saved Jobs', color: 'from-yellow-500 to-yellow-600', emoji: '💾' },
              { icon: '📨', value: stats.applications, label: 'Applications', color: 'from-green-500 to-green-600', emoji: '✅' },
              { icon: '👁️', value: stats.profile_views, label: 'Profile Views', color: 'from-pink-500 to-pink-600', emoji: '📊' }
            ].map((stat, index) => (
              <div 
                key={index} 
                className="glass-effect rounded-xl p-5 text-center hover-lift transition-all duration-300 group cursor-pointer"
              >
                <div className="text-3xl mb-2 group-hover:scale-110 transition-transform">{stat.icon}</div>
                <div className={`text-2xl font-bold bg-gradient-to-r ${stat.color} bg-clip-text text-transparent mb-1`}>
                  {stat.value}+
                </div>
                <div className="text-slate-300 text-xs font-medium">{stat.label}</div>
              </div>
            ))}
          </div>

          {/* Quick Actions */}
          <div className="glass-effect rounded-2xl p-6">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
              <span>⚡</span> Quick Actions
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {[
                { icon: '🔍', label: 'Find Jobs', path: '/job-search', color: 'from-blue-500 to-blue-600', desc: 'Search opportunities' },
                { icon: '📈', label: 'View Trends', path: '/trends', color: 'from-teal-500 to-teal-600', desc: 'Market insights' },
                { icon: '📝', label: 'My Resume', path: '#', color: 'from-purple-500 to-purple-600', desc: 'Update profile' },
                { icon: '🎯', label: 'Career Path', path: '#', color: 'from-orange-500 to-orange-600', desc: 'Plan your future' }
              ].map((action, index) => (
                <Link
                  key={index}
                  to={action.path}
                  className={`bg-gradient-to-br ${action.color} text-white p-5 rounded-xl transition-all text-center flex flex-col items-center justify-center min-h-[120px] shadow-lg hover:shadow-2xl transform hover:scale-105 hover:-translate-y-1`}
                >
                  <div className="text-3xl mb-2">{action.icon}</div>
                  <div className="font-bold text-sm mb-1">{action.label}</div>
                  <div className="text-xs opacity-90">{action.desc}</div>
                </Link>
              ))}
            </div>
          </div>

          {/* Two Column Layout */}
          <div className="grid lg:grid-cols-2 gap-6">
            {/* Recent Activity */}
            <div className="glass-effect rounded-2xl p-6">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                <span>📊</span> Recent Activity
              </h2>
              <div className="space-y-3">
                {[
                  { action: 'Applied to', company: 'Tata Power Renewables', time: '2 hours ago', type: 'application', color: 'bg-green-500' },
                  { action: 'Saved job at', company: 'Adani Green Energy', time: '1 day ago', type: 'save', color: 'bg-blue-500' },
                  { action: 'Viewed profile of', company: 'ReNew Power', time: '2 days ago', type: 'view', color: 'bg-purple-500' },
                  { action: 'Updated resume', company: 'Profile', time: '3 days ago', type: 'update', color: 'bg-teal-500' }
                ].map((activity, index) => (
                  <div key={index} className="flex items-center gap-4 p-4 bg-slate-800/50 rounded-xl hover:bg-slate-700/50 transition-all cursor-pointer group">
                    <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${activity.color} shadow-lg group-hover:scale-110 transition-transform`}>
                      {activity.type === 'application' ? '📨' : 
                       activity.type === 'save' ? '💾' : 
                       activity.type === 'update' ? '✏️' : '👀'}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-white font-medium truncate">
                        {activity.action} <span className="text-blue-400">{activity.company}</span>
                      </p>
                      <p className="text-slate-400 text-sm">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recommended Jobs */}
            <div className="glass-effect rounded-2xl p-6">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                <span>✨</span> Recommended For You
              </h2>
              <div className="space-y-3">
                {[
                  { title: 'Solar Engineer', company: 'Tata Power', match: '95%', salary: '₹15-20L' },
                  { title: 'ESG Analyst', company: 'Adani Green', match: '92%', salary: '₹12-18L' },
                  { title: 'Sustainability Manager', company: 'ReNew', match: '88%', salary: '₹18-25L' }
                ].map((job, index) => (
                  <div key={index} className="p-4 bg-slate-800/50 rounded-xl hover:bg-slate-700/50 transition-all cursor-pointer group">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="text-white font-semibold group-hover:text-blue-400 transition-colors">{job.title}</h3>
                      <span className="bg-green-500 text-white px-2 py-1 rounded-lg text-xs font-bold">
                        {job.match}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-300">🏢 {job.company}</span>
                      <span className="text-blue-400 font-semibold">💰 {job.salary}</span>
                    </div>
                    
                  </div>
                ))}
              </div>
              <Link 
                to="/job-search"
                className="w-full mt-4 bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-xl font-semibold transition-colors text-center block"
              >
                View All Jobs →
              </Link>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;