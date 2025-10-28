import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const JobSearch = () => {
  const [skills, setSkills] = useState(['Python']);
  const [location, setLocation] = useState('');
  const [salaryRange, setSalaryRange] = useState('');
  const [sdgGoal, setSdgGoal] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [jobs, setJobs] = useState([]);
  const [searchPerformed, setSearchPerformed] = useState(false);
  const [autoDetecting, setAutoDetecting] = useState(false);
  const { user } = useAuth();

  // Load featured jobs on mount
  useEffect(() => {
    setJobs(getFeaturedJobs());
  }, []);

  const getFeaturedJobs = () => [
    {
      id: 1,
      title: "Senior Solar Energy Engineer",
      company: "Tata Power Renewables",
      location: "Bengaluru, Karnataka",
      salary: "₹12-18 LPA",
      match: "95%",
      type: "Full-time",
      sdg: "SDG 7: Affordable & Clean Energy",
      sdgScore: "9/10",
      skills: ["Solar PV", "Grid Integration", "Python"],
      postedDays: 2
    },
    {
      id: 2,
      title: "Sustainability Data Analyst", 
      company: "Adani Green Energy",
      location: "Mumbai, Maharashtra",
      salary: "₹10-15 LPA",
      match: "88%",
      type: "Full-time",
      sdg: "SDG 13: Climate Action",
      sdgScore: "8/10",
      skills: ["Python", "SQL", "Power BI"],
      postedDays: 5
    },
    {
      id: 3,
      title: "Green Building Architect",
      company: "ReNew Power", 
      location: "Delhi NCR",
      salary: "₹14-20 LPA",
      match: "82%",
      type: "Full-time",
      sdg: "SDG 11: Sustainable Cities",
      sdgScore: "9/10",
      skills: ["LEED", "AutoCAD", "BIM"],
      postedDays: 1
    },
    {
      id: 4,
      title: "ESG Reporting Manager",
      company: "Suzlon Energy",
      location: "Pune, Maharashtra",
      salary: "₹15-22 LPA",
      match: "90%",
      type: "Full-time",
      sdg: "SDG 12: Responsible Consumption",
      sdgScore: "8/10",
      skills: ["ESG", "Sustainability", "Reporting"],
      postedDays: 3
    },
    {
      id: 5,
      title: "Wind Energy Analyst",
      company: "Inox Wind",
      location: "Ahmedabad, Gujarat",
      salary: "₹11-16 LPA",
      match: "85%",
      type: "Full-time",
      sdg: "SDG 7: Affordable & Clean Energy",
      sdgScore: "9/10",
      skills: ["Wind Power", "Data Analysis", "Python"],
      postedDays: 4
    },
    {
      id: 6,
      title: "Carbon Accounting Specialist",
      company: "Mahindra Sustainability",
      location: "Chennai, Tamil Nadu",
      salary: "₹12-17 LPA",
      match: "87%",
      type: "Full-time",
      sdg: "SDG 13: Climate Action",
      sdgScore: "9/10",
      skills: ["Carbon Accounting", "GHG Protocol", "Excel"],
      postedDays: 6
    }
  ];

  const handleSearch = async () => {
    if (!user) return;
    
    setIsLoading(true);
    setSearchPerformed(true);
    
    try {
      // Get token from localStorage (where it's stored after login)
      const token = localStorage.getItem('token');
      
      if (!token) {
        throw new Error('No authentication token found. Please login again.');
      }
  
      console.log('🔑 Using token:', token.substring(0, 20) + '...'); // Debug log
  
      // Call the backend API
      const response = await fetch('http://127.0.0.1:8000/match_jobs', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          skill_text: skills.filter(skill => skill.trim() !== ''),
          lang: 'en',
          location: location || undefined
        })
      });
  
      console.log('📡 API Response status:', response.status); // Debug log
  
      if (response.status === 401) {
        // Token is invalid, clear and redirect to login
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return;
      }
  
      if (!response.ok) {
        throw new Error(`API request failed with status: ${response.status}`);
      }
  
      const data = await response.json();
      
      // Transform backend response to match frontend format
      const transformedJobs = data.matches.map(job => ({
        id: job.id,
        title: job.job_title,
        company: job.company,
        location: job.location,
        salary: job.salary_range, // Use salary_range instead of salary_boost
        match: `${Math.round(job.similarity * 100)}%`,
        type: "Full-time", // Keep as default since backend doesn't provide
        sdg: job.sdg_impact,
        sdgScore: extractSDGScore(job.sdg_impact), // Extract from sdg_impact
        skills: extractSkills(job.description), // Extract from description
        postedDays: 1 // Default since backend doesn't provide
      }));
  
      setJobs(transformedJobs);
    } catch (error) {
      console.error('Search failed:', error);
      // Fallback to mock data with filtering
      const filtered = getFeaturedJobs().filter(job => {
        const matchesLocation = !location || job.location.toLowerCase().includes(location.toLowerCase());
        const matchesSalary = !salaryRange || checkSalaryMatch(job.salary, salaryRange);
        const matchesExperience = !experienceLevel || true;
        return matchesLocation && matchesSalary && matchesExperience;
      });
      setJobs(filtered);
    } finally {
      setIsLoading(false);
    }
  };

  
// Helper function to extract SDG score
const extractSDGScore = (sdgImpact) => {
  const match = sdgImpact.match(/\d+\/\d+/);
  return match ? match[0] : "8/10";
};

// Helper function to extract skills from description
const extractSkills = (description) => {
  const commonSkills = ['Python', 'Power BI', 'Analytics', 'Data', 'ESG', 'Solar', 'Renewable', 'Sustainability'];
  return commonSkills.filter(skill => 
    description.toLowerCase().includes(skill.toLowerCase())
  ).slice(0, 3);
};
  const checkSalaryMatch = (jobSalary, range) => {
    const salary = parseInt(jobSalary.match(/\d+/)[0]);
    if (range === '0-10') return salary <= 10;
    if (range === '10-15') return salary >= 10 && salary <= 15;
    if (range === '15-20') return salary >= 15 && salary <= 20;
    if (range === '20+') return salary >= 20;
    return true;
  };

  const handleAutoDetectLocation = () => {
    setAutoDetecting(true);
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        () => {
          setTimeout(() => {
            setLocation('Bengaluru, Karnataka');
            setAutoDetecting(false);
          }, 1000);
        },
        () => {
          setLocation('Bengaluru, Karnataka');
          setAutoDetecting(false);
        }
      );
    }
  };

  const addSkill = () => {
    setSkills([...skills, '']);
  };

  const updateSkill = (index, value) => {
    const newSkills = [...skills];
    newSkills[index] = value;
    setSkills(newSkills);
  };

  const removeSkill = (index) => {
    if (skills.length > 1) {
      setSkills(skills.filter((_, i) => i !== index));
    }
  };

  const clearFilters = () => {
    setSkills(['Python']);
    setLocation('');
    setSalaryRange('');
    setSdgGoal('');
    setExperienceLevel('');
    setJobs(getFeaturedJobs());
    setSearchPerformed(false);
  };

  if (!user) {
    return (
      <div className="max-w-2xl mx-auto text-center py-12">
        <div className="glass-effect rounded-2xl p-12">
          <div className="text-6xl mb-6 animate-bounce">🔒</div>
          <h2 className="text-3xl font-bold text-white mb-4">Authentication Required</h2>
          <p className="text-slate-300 mb-8 text-lg">Please login to access advanced job search features</p>
          <Link
            to="/login"
            className="bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600 text-white px-8 py-4 rounded-xl transition-all inline-block font-semibold shadow-lg"
          >
            Go to Login →
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto w-full">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-4">Find Green Jobs</h1>
        <p className="text-slate-300 text-lg">Discover opportunities in sustainable technology across India</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Search Filters Sidebar */}
        <div className="lg:col-span-1">
          <div className="glass-effect rounded-2xl p-6 sticky top-4">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
              <span>🎯</span> Search Filters
            </h2>
            
            <div className="space-y-5">
              {/* Skills */}
              <div>
                <label className="block text-white mb-3 text-sm font-semibold">
                  Skills *
                </label>
                <div className="space-y-2">
                  {skills.map((skill, index) => (
                    <div key={index} className="flex gap-2 items-center">
                      <input
                        type="text"
                        value={skill}
                        onChange={(e) => updateSkill(index, e.target.value)}
                        className="flex-1 px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="e.g. Python, Solar"
                      />
                      {skills.length > 1 && (
                        <button
                          onClick={() => removeSkill(index)}
                          className="px-3 py-2 bg-red-500 hover:bg-red-600 rounded-lg transition-colors text-white text-sm"
                        >
                          ✕
                        </button>
                      )}
                    </div>
                  ))}
                </div>
                <button
                  onClick={addSkill}
                  className="text-blue-400 hover:text-blue-300 text-sm mt-2 flex items-center gap-1"
                >
                  + Add skill
                </button>
              </div>

              {/* Location */}
              <div>
                <label className="block text-white mb-3 text-sm font-semibold">
                  Location
                </label>
                <div className="relative">
                  <input
                    type="text"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 pr-10"
                    placeholder="City or state"
                  />
                  <button
                    onClick={handleAutoDetectLocation}
                    disabled={autoDetecting}
                    className="absolute right-2 top-2 text-blue-400 hover:text-blue-300"
                    title="Auto-detect location"
                  >
                    {autoDetecting ? '⌛' : '📍'}
                  </button>
                </div>
              </div>

              {/* Salary Range */}
              <div>
                <label className="block text-white mb-3 text-sm font-semibold">
                  Salary Range (LPA)
                </label>
                <select
                  value={salaryRange}
                  onChange={(e) => setSalaryRange(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Any</option>
                  <option value="0-10">₹0 - 10L</option>
                  <option value="10-15">₹10 - 15L</option>
                  <option value="15-20">₹15 - 20L</option>
                  <option value="20+">₹20L+</option>
                </select>
              </div>

              {/* SDG Goal */}
              <div>
                <label className="block text-white mb-3 text-sm font-semibold">
                  SDG Goal
                </label>
                <select
                  value={sdgGoal}
                  onChange={(e) => setSdgGoal(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Goals</option>
                  <option value="7">SDG 7: Clean Energy</option>
                  <option value="11">SDG 11: Sustainable Cities</option>
                  <option value="12">SDG 12: Responsible Consumption</option>
                  <option value="13">SDG 13: Climate Action</option>
                </select>
              </div>

              {/* Experience Level */}
              <div>
                <label className="block text-white mb-3 text-sm font-semibold">
                  Experience Level
                </label>
                <select
                  value={experienceLevel}
                  onChange={(e) => setExperienceLevel(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Any</option>
                  <option value="entry">Entry Level (0-2 years)</option>
                  <option value="mid">Mid Level (3-5 years)</option>
                  <option value="senior">Senior (5+ years)</option>
                </select>
              </div>

              {/* Action Buttons */}
              <div className="space-y-2 pt-4">
                <button
                  onClick={handleSearch}
                  disabled={isLoading}
                  className="w-full bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600 text-white py-3 rounded-lg font-semibold transition-all disabled:opacity-50 shadow-lg"
                >
                  {isLoading ? (
                    <div className="flex items-center justify-center">
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                      Searching...
                    </div>
                  ) : (
                    '🔍 Search Jobs'
                  )}
                </button>
                
                <button
                  onClick={clearFilters}
                  className="w-full bg-slate-700 hover:bg-slate-600 text-white py-2 rounded-lg font-medium transition-colors text-sm"
                >
                  Clear Filters
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Job Results */}
        <div className="lg:col-span-2">
          <div className="glass-effect rounded-2xl p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                <span>💼</span>
                {searchPerformed ? `Search Results (${jobs.length})` : `Featured Jobs (${jobs.length})`}
              </h2>
              <div className="text-sm text-slate-400">
                Sorted by: <span className="text-blue-400">Best Match</span>
              </div>
            </div>

            {jobs.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🔍</div>
                <h3 className="text-xl font-bold text-white mb-2">No jobs found</h3>
                <p className="text-slate-400">Try adjusting your filters</p>
              </div>
            ) : (
              <div className="space-y-4">
                {jobs.map((job) => (
                  <div key={job.id} className="glass-effect rounded-xl p-6 hover-lift transition-all cursor-pointer group">
                    {/* Header */}
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-white group-hover:text-blue-400 transition-colors mb-2">
                          {job.title}
                        </h3>
                        <div className="flex items-center gap-4 text-sm text-slate-300 flex-wrap">
                          <span className="flex items-center gap-1">
                            🏢 {job.company}
                          </span>
                          <span className="flex items-center gap-1">
                            📍 {job.location}
                          </span>
                          <span className="flex items-center gap-1">
                            ⏰ {job.postedDays}d ago
                          </span>
                        </div>
                      </div>
                      <div className="flex flex-col items-end gap-2">
                        <span className="bg-green-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                          {job.match} Match
                        </span>
                        <span className="bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full text-xs">
                          {job.type}
                        </span>
                      </div>
                    </div>

                    {/* Skills */}
                    <div className="flex flex-wrap gap-2 mb-4">
                      {job.skills.map((skill, idx) => (
                        <span key={idx} className="bg-slate-700 text-slate-300 px-3 py-1 rounded-lg text-xs">
                          {skill}
                        </span>
                      ))}
                    </div>

                    {/* Footer */}
                    <div className="flex justify-between items-center pt-4 border-t border-slate-700">
                      <div className="flex items-center gap-4">
                        <span className="text-blue-400 font-bold text-lg">
                          💰 {job.salary}
                        </span>
                        <span className="bg-purple-500/20 text-purple-400 px-3 py-1 rounded-lg text-xs">
                          {job.sdg} • {job.sdgScore}
                        </span>
                      </div>
                      <div className="flex gap-2">
                        <button className="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded-lg text-sm transition-colors">
                          Save
                        </button>
                        <button className="bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600 text-white px-6 py-2 rounded-lg text-sm transition-all font-semibold">
                          Apply Now →
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobSearch;