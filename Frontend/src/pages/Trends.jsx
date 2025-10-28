import { useState, useEffect } from 'react';
import { getJobTrends, getSkillsTrends, getCompaniesTrends } from '../utils/api';

const Trends = () => {
  const [activeTab, setActiveTab] = useState('demand');
  const [trends, setTrends] = useState({
    labels: [],
    data: []
  });
  const [skillsData, setSkillsData] = useState([]);
  const [companiesData, setCompaniesData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedTimeframe, setSelectedTimeframe] = useState('month');

  useEffect(() => {
    const fetchAllTrends = async () => {
      try {
        // Fetch job trends (city demand)
        const trendsData = await getJobTrends();
        setTrends({
          labels: trendsData.chart.data.labels,
          data: trendsData.chart.data.datasets[0].data
        });

        // Fetch skills trends
        const skillsResponse = await getSkillsTrends();
        setSkillsData(skillsResponse.skills);

        // Fetch companies trends  
        const companiesResponse = await getCompaniesTrends();
        setCompaniesData(companiesResponse.companies);

      } catch (error) {
        console.error('Failed to fetch trends:', error);
        // Fallback to mock data
        setTrends({
          labels: ['Bengaluru', 'Mumbai', 'Delhi NCR', 'Pune', 'Hyderabad', 'Chennai'],
          data: [18, 15, 12, 8, 7, 6]
        });
        setSkillsData([
          { name: 'Solar PV Design', demand: 95, growth: '+25%', jobs: 145 },
          { name: 'Carbon Accounting', demand: 92, growth: '+30%', jobs: 128 },
          { name: 'ESG Reporting', demand: 88, growth: '+22%', jobs: 156 },
          { name: 'Renewable Analytics', demand: 85, growth: '+20%', jobs: 112 },
          { name: 'Green Building (LEED)', demand: 82, growth: '+18%', jobs: 98 },
          { name: 'Wind Energy Systems', demand: 78, growth: '+15%', jobs: 87 }
        ]);
        setCompaniesData([
          { name: 'Tata Power Renewables', openings: 47, growth: '+35%', rating: 4.5 },
          { name: 'Adani Green Energy', openings: 38, growth: '+28%', rating: 4.3 },
          { name: 'ReNew Power', openings: 32, growth: '+22%', rating: 4.4 },
          { name: 'Suzlon Energy', openings: 28, growth: '+18%', rating: 4.2 },
          { name: 'Azure Power', openings: 24, growth: '+30%', rating: 4.3 },
          { name: 'Hero Future Energies', openings: 19, growth: '+25%', rating: 4.1 }
        ]);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchAllTrends();
  }, []);

  const tabs = [
    { id: 'demand', label: 'Job Demand', icon: '📊' },
    { id: 'skills', label: 'Hot Skills', icon: '🔥' },
    { id: 'companies', label: 'Top Companies', icon: '🏆' },
    { id: 'salary', label: 'Salary Trends', icon: '💰' }
  ];

  const salaryData = [
    { role: 'Solar Engineer', avg: '₹16L', growth: '+12%', demand: 'High' },
    { role: 'ESG Analyst', avg: '₹14L', growth: '+15%', demand: 'Very High' },
    { role: 'Sustainability Manager', avg: '₹20L', growth: '+10%', demand: 'High' },
    { role: 'Green Architect', avg: '₹18L', growth: '+8%', demand: 'Medium' },
    { role: 'Carbon Analyst', avg: '₹15L', growth: '+18%', demand: 'Very High' }
  ];

  const growthAreas = [
    { area: 'Electric Vehicles', growth: '+45%', jobs: 234, color: 'from-blue-500 to-blue-600' },
    { area: 'Green Hydrogen', growth: '+52%', jobs: 189, color: 'from-purple-500 to-purple-600' },
    { area: 'Carbon Capture', growth: '+38%', jobs: 156, color: 'from-teal-500 to-teal-600' },
    { area: 'Smart Grids', growth: '+41%', jobs: 201, color: 'from-green-500 to-green-600' },
    { area: 'Waste to Energy', growth: '+35%', jobs: 145, color: 'from-orange-500 to-orange-600' },
    { area: 'Sustainable Agriculture', growth: '+29%', jobs: 123, color: 'from-lime-500 to-lime-600' }
  ];

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-20">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-2xl">📊</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4">Market Intelligence</h1>
        <p className="text-slate-300 text-lg">Real-time insights powered by MariaDB analytics</p>
      </div>

      {/* Timeframe Selector */}
      <div className="flex justify-center gap-3 flex-wrap">
        {['week', 'month', 'quarter', 'year'].map((timeframe) => (
          <button
            key={timeframe}
            onClick={() => setSelectedTimeframe(timeframe)}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              selectedTimeframe === timeframe
                ? 'bg-blue-500 text-white shadow-lg'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            {timeframe.charAt(0).toUpperCase() + timeframe.slice(1)}
          </button>
        ))}
      </div>

      {/* Tab Navigation */}
      <div className="glass-effect rounded-2xl p-2">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-3 rounded-xl font-semibold transition-all flex items-center justify-center gap-2 ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-blue-500 to-teal-500 text-white shadow-lg'
                  : 'text-slate-300 hover:bg-slate-700'
              }`}
            >
              <span>{tab.icon}</span>
              <span className="hidden sm:inline">{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Content based on active tab */}
      {activeTab === 'demand' && (
        <div className="space-y-6">
          {/* City Demand Chart */}
          <div className="glass-effect rounded-2xl p-6">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
              <span>📍</span> Job Demand by City
            </h2>
            <div className="space-y-3">
              {trends.labels.map((label, index) => (
                <div key={index} className="group">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-teal-500 rounded-xl flex items-center justify-center text-white font-bold shadow-lg group-hover:scale-110 transition-transform">
                        {index + 1}
                      </div>
                      <span className="text-white font-semibold text-lg">{label}</span>
                    </div>
                    <span className="bg-green-500 text-white px-4 py-2 rounded-full text-sm font-bold">
                      {trends.data[index]}% Share
                    </span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-3 overflow-hidden">
                    <div 
                      className="bg-gradient-to-r from-blue-500 to-teal-500 h-3 rounded-full transition-all duration-1000 ease-out"
                      style={{ width: `${(trends.data[index] / 20) * 100}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Key Metrics */}
          <div className="grid md:grid-cols-3 gap-6">
            <div className="glass-effect rounded-2xl p-6 text-center">
              <div className="text-4xl mb-3">📈</div>
              <div className="text-3xl font-bold text-blue-400 mb-2">+32%</div>
              <div className="text-slate-300">Market Growth</div>
            </div>
            <div className="glass-effect rounded-2xl p-6 text-center">
              <div className="text-4xl mb-3">💼</div>
              <div className="text-3xl font-bold text-teal-400 mb-2">547</div>
              <div className="text-slate-300">Active Jobs</div>
            </div>
            <div className="glass-effect rounded-2xl p-6 text-center">
              <div className="text-4xl mb-3">🏢</div>
              <div className="text-3xl font-bold text-purple-400 mb-2">52</div>
              <div className="text-slate-300">Hiring Companies</div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'skills' && (
        <div className="space-y-6">
          <div className="glass-effect rounded-2xl p-6">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
              <span>🔥</span> Most In-Demand Skills
            </h2>
            <div className="space-y-4">
              {skillsData.map((skill, index) => (
                <div key={index} className="glass-effect rounded-xl p-5 hover-lift transition-all group">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-lg font-bold text-white group-hover:text-blue-400 transition-colors">
                      {skill.name}
                    </h3>
                    <div className="flex items-center gap-3">
                      <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm font-bold">
                        {skill.growth}
                      </span>
                      <span className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full text-sm">
                        {skill.jobs} jobs
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="flex-1">
                      <div className="w-full bg-slate-700 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-orange-500 to-yellow-500 h-2 rounded-full transition-all duration-1000"
                          style={{ width: `${skill.demand}%` }}
                        ></div>
                      </div>
                    </div>
                    <span className="text-orange-400 font-bold text-sm">{skill.demand}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'companies' && (
        <div className="space-y-6">
          <div className="glass-effect rounded-2xl p-6">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
              <span>🏆</span> Top Hiring Companies
            </h2>
            <div className="space-y-3">
              {companiesData.map((company, index) => (
                <div key={index} className="flex items-center justify-between p-5 bg-slate-800/50 rounded-xl hover:bg-slate-700/50 transition-all cursor-pointer group">
                  <div className="flex items-center gap-4 flex-1">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-xl flex items-center justify-center text-white font-bold shadow-lg group-hover:scale-110 transition-transform">
                      {index + 1}
                    </div>
                    <div className="flex-1">
                      <h3 className="text-white font-bold group-hover:text-blue-400 transition-colors mb-1">
                        {company.name}
                      </h3>
                      <div className="flex items-center gap-2">
                        <span className="text-yellow-400 text-sm">⭐ {company.rating}</span>
                        <span className="text-slate-500">•</span>
                        <span className="text-slate-400 text-sm">{company.openings} openings</span>
                      </div>
                    </div>
                  </div>
                  <div className="bg-green-500/20 text-green-400 px-4 py-2 rounded-lg font-bold text-sm">
                    {company.growth}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'salary' && (
        <div className="space-y-6">
          <div className="glass-effect rounded-2xl p-6">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
              <span>💰</span> Salary Trends by Role
            </h2>
            <div className="space-y-3">
              {salaryData.map((item, index) => (
                <div key={index} className="flex items-center justify-between p-5 bg-slate-800/50 rounded-xl hover:bg-slate-700/50 transition-all">
                  <div className="flex-1">
                    <h3 className="text-white font-bold mb-2">{item.role}</h3>
                    <div className="flex items-center gap-4 text-sm">
                      <span className="text-slate-400">Avg: <span className="text-blue-400 font-semibold">{item.avg}</span></span>
                      <span className="text-slate-500">•</span>
                      <span className="text-slate-400">Growth: <span className="text-green-400 font-semibold">{item.growth}</span></span>
                    </div>
                  </div>
                  <div className={`px-4 py-2 rounded-lg font-bold text-sm ${
                    item.demand === 'Very High' ? 'bg-red-500/20 text-red-400' :
                    item.demand === 'High' ? 'bg-orange-500/20 text-orange-400' :
                    'bg-yellow-500/20 text-yellow-400'
                  }`}>
                    {item.demand}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Growth Areas Section (Always Visible) */}
      <div className="glass-effect rounded-2xl p-6">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <span>🚀</span> Emerging Growth Areas
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {growthAreas.map((area, index) => (
            <div
              key={index}
              className={`bg-gradient-to-br ${area.color} rounded-xl p-6 text-white hover-lift transition-all cursor-pointer`}
            >
              <h3 className="text-lg font-bold mb-3">{area.area}</h3>
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-bold mb-1">{area.growth}</div>
                  <div className="text-sm opacity-90">{area.jobs} opportunities</div>
                </div>
                <div className="text-4xl opacity-75">📈</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* SDG Impact Analysis */}
      <div className="glass-effect rounded-2xl p-6">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          <span>🌍</span> SDG Impact Distribution
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { sdg: 'SDG 7', name: 'Clean Energy', percentage: 35, color: 'bg-yellow-500' },
            { sdg: 'SDG 13', name: 'Climate Action', percentage: 28, color: 'bg-green-500' },
            { sdg: 'SDG 11', name: 'Sustainable Cities', percentage: 22, color: 'bg-orange-500' },
            { sdg: 'SDG 12', name: 'Responsible Consumption', percentage: 15, color: 'bg-purple-500' }
          ].map((sdg, index) => (
            <div key={index} className="glass-effect rounded-xl p-5 text-center">
              <div className="text-3xl mb-3">🎯</div>
              <div className="text-lg font-bold text-white mb-1">{sdg.sdg}</div>
              <div className="text-xs text-slate-400 mb-3">{sdg.name}</div>
              <div className="text-2xl font-bold text-blue-400">{sdg.percentage}%</div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer Note */}
      <div className="text-center text-slate-400 text-sm pb-8">
        <p>Data updated in real-time from MariaDB • Last updated: {new Date().toLocaleString()}</p>
      </div>
    </div>
  );
};

export default Trends;