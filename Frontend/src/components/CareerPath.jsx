import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

const CareerPath = () => {
  const [currentSkill, setCurrentSkill] = useState('python');
  const [yearsExperience, setYearsExperience] = useState(3);
  const [careerData, setCareerData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const { user } = useAuth();

  const skills = [
    { value: 'python', label: 'Python Development', icon: '🐍' },
    { value: 'design', label: 'Green Design', icon: '🎨' },
    { value: 'data', label: 'Data Analytics', icon: '📊' },
    { value: 'sustainable', label: 'Sustainability', icon: '🌱' }
  ];

  const fetchCareerPath = async () => {
    if (!user) return;
    
    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://127.0.0.1:8000/career_path', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          current_skill: currentSkill,
          years_experience: yearsExperience
        })
      });

      if (response.ok) {
        const data = await response.json();
        setCareerData(data);
      }
    } catch (error) {
      console.error('Career path fetch failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCareerPath();
  }, [currentSkill, yearsExperience]);

  if (!user) {
    return (
      <div className="glass-premium rounded-2xl p-8 text-center">
        <div className="text-6xl mb-4">🔒</div>
        <h3 className="text-xl font-bold text-white mb-2">Authentication Required</h3>
        <p className="text-slate-300">Please login to view your career path</p>
      </div>
    );
  }

  return (
    <div className="glass-premium rounded-2xl p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="text-3xl">🚀</div>
        <h2 className="text-2xl font-bold text-white">Your Career Path</h2>
      </div>

      {/* Skill Selection */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        {skills.map((skill) => (
          <button
            key={skill.value}
            onClick={() => setCurrentSkill(skill.value)}
            className={`p-4 rounded-xl transition-all ${
              currentSkill === skill.value
                ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
                : 'glass-effect text-slate-300 hover:bg-slate-700/50'
            }`}
          >
            <div className="text-2xl mb-2">{skill.icon}</div>
            <div className="text-sm font-medium">{skill.label}</div>
          </button>
        ))}
      </div>

      {/* Experience Slider */}
      <div className="mb-8">
        <label className="block text-white font-semibold mb-4">
          Years of Experience: <span className="text-blue-400">{yearsExperience} years</span>
        </label>
        <input
          type="range"
          min="0"
          max="10"
          value={yearsExperience}
          onChange={(e) => setYearsExperience(parseInt(e.target.value))}
          className="w-full h-3 bg-slate-700 rounded-lg appearance-none cursor-pointer slider"
        />
        <div className="flex justify-between text-sm text-slate-400 mt-2">
          <span>0</span>
          <span>5</span>
          <span>10+</span>
        </div>
      </div>

      {/* Career Path Visualization */}
      {isLoading ? (
        <div className="flex justify-center items-center py-12">
          <div className="flex gap-2">
            <div className="loading-pulse"></div>
            <div className="loading-pulse"></div>
            <div className="loading-pulse"></div>
          </div>
        </div>
      ) : careerData ? (
        <div className="space-y-6">
          {/* Career Progression */}
          <div className="career-path">
            {careerData.career_path.map((role, index) => (
              <div key={index} className="flex flex-col items-center text-center">
                <div className="career-step">
                  {index + 1}
                </div>
                <div className="mt-3">
                  <div className="text-white font-bold text-sm">{role}</div>
                  <div className="text-slate-400 text-xs mt-1">
                    Year {index * 2 + 1}-{index * 2 + 3}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Salary Projection */}
          <div className="glass-effect rounded-xl p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-slate-300 text-sm">Salary Projection</div>
                <div className="text-2xl font-bold text-green-400">
                  {careerData.salary_projection}
                </div>
              </div>
              <div className="text-4xl">💰</div>
            </div>
          </div>

          {/* SDG Impact */}
          <div className="glass-effect rounded-xl p-4">
            <div className="flex items-center gap-3">
              <div className="text-3xl">🌍</div>
              <div>
                <div className="text-slate-300 text-sm">SDG Impact</div>
                <div className="text-white font-semibold">{careerData.sdg_impact}</div>
              </div>
            </div>
          </div>

          {/* Next Steps */}
          <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-4">
            <div className="flex items-center gap-3">
              <div className="text-2xl">🎯</div>
              <div>
                <div className="text-blue-300 font-semibold">Next Step</div>
                <div className="text-white text-sm">
                  Focus on {careerData.career_path[1]} skills at {careerData.company}
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="text-center py-8 text-slate-400">
          Select your skills to see career path
        </div>
      )}
    </div>
  );
};

export default CareerPath;