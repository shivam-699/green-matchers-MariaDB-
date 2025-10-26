import { useState, useEffect } from 'react';
import { getJobTrends } from '../utils/api';
import JobTrendsChart from '../components/JobTrendsChart';

function Dashboard() {
  const [trends, setTrends] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        const data = await getJobTrends();
        setTrends(data);
      } catch (err) {
        setError('Error fetching trends');
      }
    };
    fetchTrends();
  }, []);

  return (
    <div className="py-8">
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
      {error && <p className="text-red-500">{error}</p>}
      {trends && <JobTrendsChart data={trends} />}
    </div>
  );
}

export default Dashboard;