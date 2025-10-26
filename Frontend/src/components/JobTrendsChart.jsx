import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function JobTrendsChart({ data }) {
  const chartData = data.chart.data.labels.map((label, index) => ({
    name: label,
    value: data.chart.data.datasets[0].data[index],
  }));

  return (
    <BarChart width={500} height={300} data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar dataKey="value" fill="#36A2EB" />
    </BarChart>
  );
}

export default JobTrendsChart;