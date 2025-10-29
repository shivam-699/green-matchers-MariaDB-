// Vector Search API functions
const API_BASE = 'http://localhost:8000';

export const vectorAPI = {
  // Initialize vector data
  initializeVectors: async (token) => {
    const response = await fetch(`${API_BASE}/api/vector/initialize`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return await response.json();
  },

  // Semantic job search
  semanticSearchJobs: async (query, location = null, limit = 10, lang = 'en', token) => {
    const params = new URLSearchParams({
      q: query,
      limit: limit.toString(),
      lang
    });
    if (location) params.append('location', location);

    const response = await fetch(`${API_BASE}/api/jobs/semantic-search?${params}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return await response.json();
  },

  // Semantic career search
  semanticSearchCareers: async (query, limit = 10, lang = 'en', token) => {
    const params = new URLSearchParams({
      q: query,
      limit: limit.toString(),
      lang
    });

    const response = await fetch(`${API_BASE}/api/careers/semantic-search?${params}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return await response.json();
  },

  // Career recommendations by skills
  recommendCareersBySkills: async (skills, limit = 5, lang = 'en', token) => {
    const params = new URLSearchParams({
      skills,
      limit: limit.toString(),
      lang
    });

    const response = await fetch(`${API_BASE}/api/careers/recommend-by-skills?${params}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return await response.json();
  },

  // Skill-based job matching
  skillBasedJobMatching: async (skills, location = null, limit = 10, lang = 'en', token) => {
    const params = new URLSearchParams({
      skills,
      limit: limit.toString(),
      lang
    });
    if (location) params.append('location', location);

    const response = await fetch(`${API_BASE}/api/jobs/skill-match?${params}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return await response.json();
  },

  // Get similar careers
  getSimilarCareers: async (careerId, limit = 5, lang = 'en', token) => {
    const params = new URLSearchParams({
      limit: limit.toString(),
      lang
    });

    const response = await fetch(`${API_BASE}/api/careers/${careerId}/similar?${params}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return await response.json();
  },

  // Get vector system status
  getVectorStatus: async (token) => {
    const response = await fetch(`${API_BASE}/api/vector/status`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return await response.json();
  }
};