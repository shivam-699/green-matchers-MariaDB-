import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: { 'Content-Type': 'application/json' },
});

export const login = async (username, password) => {
  const response = await api.post('/token', new URLSearchParams({
    grant_type: 'password',
    username,
    password,
    scope: '',
    client_id: 'string',
    client_secret: '',
  }), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return response.data;
};

export const getJobTrends = async () => {
  const response = await api.get('/job_trends');
  return response.data;
};

export const matchJobs = async (token, skills, location) => {
  const response = await api.post('/match_jobs', {
    skill_text: skills,
    lang: 'en',
    location,
  }, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const saveJob = async (token, jobId) => {
  const response = await api.post(`/save_job?job_id=${jobId}`, {}, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const generateResume = async (token, skills, location) => {
  const response = await api.post('/generate_resume', {
    skill_text: skills,
    lang: 'en',
    location,
  }, {
    headers: { Authorization: `Bearer ${token}` },
    responseType: 'blob',
  });
  return response.data;
};