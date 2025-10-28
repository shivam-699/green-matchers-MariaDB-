import { Link } from 'react-router-dom';
import { useOutletContext } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useState, useEffect } from 'react';

const Home = () => {
  const { user } = useAuth();
  const { showToast } = useOutletContext();
  const [stats, setStats] = useState({ jobs: 0, companies: 0, users: 0 });

  // Animated counter effect
  useEffect(() => {
    const targets = { jobs: 547, companies: 52, users: 1284 };
    const duration = 2000;
    const steps = 60;
    const interval = duration / steps;
    
    let current = { jobs: 0, companies: 0, users: 0 };
    const increment = {
      jobs: targets.jobs / steps,
      companies: targets.companies / steps,
      users: targets.users / steps
    };

    const timer = setInterval(() => {
      current.jobs = Math.min(current.jobs + increment.jobs, targets.jobs);
      current.companies = Math.min(current.companies + increment.companies, targets.companies);
      current.users = Math.min(current.users + increment.users, targets.users);
      
      setStats({
        jobs: Math.floor(current.jobs),
        companies: Math.floor(current.companies),
        users: Math.floor(current.users)
      });

      if (current.jobs >= targets.jobs) clearInterval(timer);
    }, interval);

    return () => clearInterval(timer);
  }, []);

  const features = [
    {
      icon: '🤖',
      title: 'AI Job Matching',
      description: 'Advanced algorithms match your skills with perfect green companies using machine learning',
      color: 'from-blue-500 to-cyan-500',
      gradient: 'bg-gradient-to-br from-blue-500/10 to-cyan-500/10'
    },
    {
      icon: '🌍',
      title: 'SDG Alignment',
      description: 'Find jobs aligned with UN Sustainable Development Goals for maximum impact',
      color: 'from-emerald-500 to-green-600',
      gradient: 'bg-gradient-to-br from-emerald-500/10 to-green-600/10'
    },
    {
      icon: '💰',
      title: 'Salary Insights',
      description: 'Real-time salary data and growth projections powered by market analytics',
      color: 'from-purple-500 to-pink-500',
      gradient: 'bg-gradient-to-br from-purple-500/10 to-pink-500/10'
    },
    {
      icon: '📊',
      title: 'Market Trends',
      description: 'Live tracking of green job market trends and demand patterns across India',
      color: 'from-orange-500 to-red-500',
      gradient: 'bg-gradient-to-br from-orange-500/10 to-red-500/10'
    }
  ];

  const testimonials = [
    {
      name: 'Priya Sharma',
      role: 'Solar Engineer',
      company: 'Tata Power',
      text: 'Found my dream job in renewable energy within 2 weeks!',
      avatar: '👩‍💼',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      name: 'Rahul Kumar',
      role: 'ESG Analyst',
      company: 'Adani Green',
      text: 'The AI matching is incredibly accurate. Highly recommend!',
      avatar: '👨‍💼',
      color: 'from-purple-500 to-pink-500'
    },
    {
      name: 'Anjali Patel',
      role: 'Sustainability Manager',
      company: 'ReNew Power',
      text: 'Best platform for green careers. Changed my professional life!',
      avatar: '👩‍🔬',
      color: 'from-emerald-500 to-teal-500'
    }
  ];

  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
      <div className="space-y-32 md:space-y-40">
        {/* Hero Section */}
        {user ? (
          <section className="text-center py-12 md:py-20">
            <div className="flex justify-center mb-10">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-3xl blur-xl opacity-50 animate-pulse"></div>
                <div className="relative w-28 h-28 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-3xl flex items-center justify-center text-5xl shadow-2xl animate-float">
                  👋
                </div>
              </div>
            </div>
            
            <h2 className="text-5xl md:text-6xl font-extrabold text-white mb-8 leading-tight">
              Welcome back, <br />
              <span className="bg-gradient-to-r from-blue-400 via-cyan-400 to-teal-400 bg-clip-text text-transparent">
                {user.username}
              </span>!
            </h2>
            <p className="text-slate-300 text-xl md:text-2xl max-w-3xl mx-auto leading-relaxed mb-12">
              Ready to continue your journey in sustainable technology?
            </p>
            <div className="flex flex-wrap gap-6 justify-center">
              <Link
                to="/dashboard"
                className="group relative px-10 py-5 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white rounded-2xl font-bold transition-all shadow-xl hover:shadow-2xl transform hover:scale-105 overflow-hidden"
              >
                <span className="relative z-10 flex items-center gap-2">
                  Go to Dashboard
                  <span className="group-hover:translate-x-1 transition-transform">→</span>
                </span>
                <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
              </Link>
              <Link
                to="/job-search"
                className="group px-10 py-5 border-2 border-blue-500 text-blue-400 hover:bg-blue-500 hover:text-white rounded-2xl font-bold transition-all hover:shadow-xl hover:shadow-blue-500/50 transform hover:scale-105"
              >
                <span className="flex items-center gap-2">
                  🔍 Search Jobs
                </span>
              </Link>
            </div>
          </section>
        ) : (
          <section className="text-center py-12 md:py-20">
            <div className="flex justify-center mb-12">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-green-500 via-teal-500 to-blue-500 rounded-3xl blur-2xl opacity-60 animate-pulse"></div>
                <div className="relative w-32 h-32 bg-gradient-to-br from-green-500 via-teal-500 to-blue-500 rounded-3xl flex items-center justify-center text-6xl shadow-2xl animate-float">
                  🌱
                </div>
              </div>
            </div>
            
            <h1 className="text-6xl md:text-7xl font-extrabold text-white mb-10 leading-tight">
              Your Green Career
              <br />
              <span className="bg-gradient-to-r from-green-400 via-teal-400 to-blue-400 bg-clip-text text-transparent animate-pulse">
                Starts Here
              </span>
            </h1>
            <p className="text-slate-300 text-xl md:text-2xl mb-16 max-w-4xl mx-auto leading-relaxed">
              Connect with India's leading sustainable companies and build your career in 
              <span className="text-emerald-400 font-semibold"> renewable energy </span>
              with AI-powered job matching
            </p>

            {/* Stats Bar */}
            <div className="glass-effect rounded-3xl p-10 md:p-12 mb-8 max-w-5xl mx-auto border border-white/20 shadow-2xl">
              <div className="grid grid-cols-3 gap-10 md:gap-16">
                <div className="text-center group cursor-pointer">
                  <div className="text-5xl md:text-6xl font-black bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent mb-4 group-hover:scale-110 transition-transform">
                    {stats.jobs}+
                  </div>
                  <div className="text-slate-300 font-semibold text-sm md:text-base">Green Jobs</div>
                </div>
                <div className="text-center border-x border-slate-600/50 group cursor-pointer">
                  <div className="text-5xl md:text-6xl font-black bg-gradient-to-r from-teal-400 to-teal-600 bg-clip-text text-transparent mb-4 group-hover:scale-110 transition-transform">
                    {stats.companies}+
                  </div>
                  <div className="text-slate-300 font-semibold text-sm md:text-base">Companies</div>
                </div>
                <div className="text-center group cursor-pointer">
                  <div className="text-5xl md:text-6xl font-black bg-gradient-to-r from-purple-400 to-purple-600 bg-clip-text text-transparent mb-4 group-hover:scale-110 transition-transform">
                    {stats.users}+
                  </div>
                  <div className="text-slate-300 font-semibold text-sm md:text-base">Active Users</div>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Features Grid */}
        <section className="py-8">
          <div className="text-center mb-20">
            <div className="inline-block mb-6">
              <span className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-3 rounded-full text-sm font-bold uppercase tracking-wider shadow-lg">
                How It Works
              </span>
            </div>
            <h3 className="text-4xl md:text-5xl font-extrabold text-white mb-8">
              Powered by AI & Innovation
            </h3>
            <p className="text-slate-300 text-lg md:text-xl max-w-3xl mx-auto leading-relaxed">
              Advanced MariaDB analytics combined with cutting-edge AI technology
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group relative glass-effect rounded-3xl p-10 text-center transition-all duration-500 hover:-translate-y-3 hover:shadow-2xl cursor-pointer border border-white/10 overflow-hidden"
              >
                <div className={`absolute inset-0 ${feature.gradient} opacity-0 group-hover:opacity-100 transition-opacity duration-500`}></div>
                
                <div className="relative z-10">
                  <div className={`w-20 h-20 mx-auto mb-8 bg-gradient-to-br ${feature.color} rounded-2xl flex items-center justify-center text-4xl shadow-xl group-hover:scale-110 group-hover:rotate-6 transition-all duration-500`}>
                    {feature.icon}
                  </div>
                  <h4 className="text-2xl font-bold text-white mb-5 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-blue-200 group-hover:bg-clip-text transition-all">
                    {feature.title}
                  </h4>
                  <p className="text-slate-300 text-sm leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Testimonials */}
        <section className="relative py-8">
          <div className="text-center mb-20">
            <div className="inline-block mb-6">
              <span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-3 rounded-full text-sm font-bold uppercase tracking-wider shadow-lg">
                Success Stories
              </span>
            </div>
            <h3 className="text-4xl md:text-5xl font-extrabold text-white mb-8">
              Real Results, Real People
            </h3>
            <p className="text-slate-300 text-lg md:text-xl leading-relaxed">
              Join thousands building sustainable careers
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-10">
            {testimonials.map((testimonial, index) => (
              <div
                key={index}
                className="group relative glass-effect rounded-3xl p-10 hover:shadow-2xl transition-all duration-500 hover:-translate-y-2 cursor-pointer border border-white/10 overflow-hidden"
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${testimonial.color} opacity-0 group-hover:opacity-10 transition-opacity duration-500`}></div>
                
                <div className="relative z-10">
                  <div className="flex items-center gap-5 mb-8">
                    <div className={`w-16 h-16 bg-gradient-to-br ${testimonial.color} rounded-2xl flex items-center justify-center text-3xl shadow-lg group-hover:scale-110 transition-transform`}>
                      {testimonial.avatar}
                    </div>
                    <div className="text-left">
                      <h4 className="text-white font-bold text-lg mb-1">{testimonial.name}</h4>
                      <p className="text-slate-400 text-sm">{testimonial.role}</p>
                    </div>
                  </div>
                  <p className="text-slate-300 italic mb-8 text-base leading-relaxed">
                    "{testimonial.text}"
                  </p>
                  <div className={`inline-block bg-gradient-to-r ${testimonial.color} text-white px-5 py-2 rounded-full text-sm font-semibold shadow-lg`}>
                    @ {testimonial.company}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* CTA Section */}
        {!user && (
          <section className="relative glass-effect rounded-3xl p-16 md:p-20 bg-gradient-to-br from-blue-500/20 via-purple-500/10 to-teal-500/20 border-2 border-blue-500/30 overflow-hidden my-8">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-teal-500/10 animate-pulse"></div>
            
            <div className="relative z-10 text-center">
              <h3 className="text-4xl md:text-5xl font-extrabold text-white mb-8">
                Ready to Make an Impact?
              </h3>
              <p className="text-slate-300 mb-14 text-lg md:text-xl leading-relaxed max-w-3xl mx-auto">
                Join thousands of professionals building sustainable careers and contributing to 
                <span className="text-green-400 font-bold"> UN SDG Goals</span>
              </p>
              <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-14">
                <Link
                  to="/login"
                  className="group relative px-12 py-5 bg-gradient-to-r from-blue-600 to-teal-600 hover:from-blue-500 hover:to-teal-500 text-white rounded-2xl font-bold transition-all text-center shadow-2xl hover:shadow-blue-500/50 transform hover:scale-105 overflow-hidden"
                >
                  <span className="relative z-10 flex items-center gap-2">
                    Get Started Free
                    <span className="group-hover:translate-x-1 transition-transform">→</span>
                  </span>
                  <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                </Link>
                <Link
                  to="/job-search"
                  className="px-12 py-5 border-2 border-blue-500 text-blue-400 hover:bg-blue-500 hover:text-white rounded-2xl font-bold transition-all text-center hover:shadow-xl transform hover:scale-105"
                >
                  Browse Jobs
                </Link>
              </div>
              
              <div className="flex flex-wrap items-center justify-center gap-6 text-sm text-slate-300">
                <div className="flex items-center gap-3 bg-white/5 px-8 py-4 rounded-full">
                  <span className="text-green-400 text-xl">✓</span> 
                  <span className="font-semibold">Free to join</span>
                </div>
                <div className="flex items-center gap-3 bg-white/5 px-8 py-4 rounded-full">
                  <span className="text-green-400 text-xl">✓</span> 
                  <span className="font-semibold">AI-powered matching</span>
                </div>
                <div className="flex items-center gap-3 bg-white/5 px-8 py-4 rounded-full">
                  <span className="text-green-400 text-xl">✓</span> 
                  <span className="font-semibold">SDG aligned</span>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Tech Stack Badge */}
        <section className="text-center pb-12 pt-8">
          <div className="inline-flex items-center gap-5 glass-effect rounded-full px-10 py-5 border border-white/20 shadow-xl">
            <span className="text-slate-400 text-sm font-semibold">Powered by</span>
            <div className="flex items-center gap-4">
              <span className="font-bold text-lg bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">MariaDB</span>
              <span className="text-slate-600">•</span>
              <span className="font-bold text-lg bg-gradient-to-r from-teal-400 to-teal-600 bg-clip-text text-transparent">React</span>
              <span className="text-slate-600">•</span>
              <span className="font-bold text-lg bg-gradient-to-r from-purple-400 to-purple-600 bg-clip-text text-transparent">AI/ML</span>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Home;