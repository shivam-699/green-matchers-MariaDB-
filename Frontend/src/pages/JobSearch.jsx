import { useState, useEffect } from 'react';
import { matchJobs, saveJob, generateResume } from '../utils/api';
import JobCard from '../components/JobCard';
import { saveAs } from 'file-saver';

function JobSearch() {
  const [skills, setSkills] = useState(['Python']);
  const [location, setLocation] = useState('Bengaluru');
  const [jobs, setJobs] = useState([]);
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [error, setError] = useState('');

  useEffect(() => {
    if (token) handleSearch();
  }, [token]);

  const handleSearch = async () => {
    if (!token) {
      setError('Please login first');
      return;
    }
    try {
      const data = await matchJobs(token, skills, location);
      setJobs(data.matches);
    } catch (err) {
      setError('Error fetching jobs');
    }
  };

  const handleSaveJob = async (jobId) => {
    try {
      const data = await saveJob(token, jobId);
      alert(data.message);
    } catch (err) {
      setError('Error saving job');
    }
  };

  const handleGenerateResume = async () => {
    try {
      const blob = await generateResume(token, skills, location);
      saveAs(blob, 'resume.pdf');
    } catch (err) {
      setError('Error generating resume');
    }
  };

  return (
    <div className="py-8">
      <h2 className="text-2xl font-bold mb-4">Job Search</h2>
      {error && <p className="text-red-500">{error}</p>}
      <div className="mb-4">
        <input
          type="text"
          value={skills.join(',')}
          onChange={(e) => setSkills(e.target.value.split(','))}
          placeholder="Skills (e.g., Python, Data)"
          className="p-2 border rounded mr-2"
        />
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Location (e.g., Bengaluru)"
          className="p-2 border rounded mr-2"
        />
        <button onClick={handleSearch} className="bg-green-600 text-white p-2 rounded">
          Search
        </button>
        <button onClick={handleGenerateResume} className="bg-blue-600 text-white p-2 rounded ml-2">
          Generate Resume
        </button>
      </div>
      <div>
        {jobs.map((job) => (
          <JobCard key={job.id} job={job} onSave={handleSaveJob} />
        ))}
      </div>
    </div>
  );
}

export default JobSearch;