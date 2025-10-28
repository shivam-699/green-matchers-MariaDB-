import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp } from 'lucide-react';

function JobTrendsChart({ data }) {
  // Transform data for recharts
  const chartData = data.chart.data.labels.map((label, index) => ({
    name: label,
    value: data.chart.data.datasets[0].data[index],
  }));

  // Custom Tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-800/95 backdrop-blur-xl border border-slate-700 rounded-xl p-4 shadow-2xl">
          <p className="text-white font-semibold mb-1">{payload[0].payload.name}</p>
          <p className="text-blue-400 font-bold text-lg">
            {payload[0].value.toLocaleString()} jobs
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-slate-800/40 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 hover:border-slate-600 transition-all">
      
      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-blue-500/10 border border-blue-500/30 rounded-xl flex items-center justify-center">
          <TrendingUp className="w-5 h-5 text-blue-400" />
        </div>
        <div>
          <h3 className="text-xl font-bold text-white">Job Market Trends</h3>
          <p className="text-slate-400 text-sm">Current opportunities by category</p>
        </div>
      </div>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={400}>
        <BarChart 
          data={chartData} 
          margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
        >
          <defs>
            <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3B82F6" stopOpacity={0.8} />
              <stop offset="100%" stopColor="#8B5CF6" stopOpacity={0.8} />
            </linearGradient>
          </defs>
          
          <CartesianGrid 
            strokeDasharray="3 3" 
            stroke="#334155" 
            opacity={0.3}
          />
          
          <XAxis 
            dataKey="name" 
            stroke="#94A3B8"
            tick={{ fill: '#94A3B8', fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={100}
          />
          
          <YAxis 
            stroke="#94A3B8"
            tick={{ fill: '#94A3B8', fontSize: 12 }}
            label={{ 
              value: 'Number of Jobs', 
              angle: -90, 
              position: 'insideLeft',
              fill: '#94A3B8',
              fontSize: 12
            }}
          />
          
          <Tooltip 
            content={<CustomTooltip />}
            cursor={{ fill: 'rgba(59, 130, 246, 0.1)' }}
          />
          
          <Legend 
            wrapperStyle={{
              paddingTop: '20px',
              fontSize: '14px',
              color: '#94A3B8'
            }}
          />
          
          <Bar 
            dataKey="value" 
            fill="url(#barGradient)"
            radius={[8, 8, 0, 0]}
            name="Available Jobs"
          />
        </BarChart>
      </ResponsiveContainer>

      {/* Stats Summary */}
      <div className="grid grid-cols-3 gap-4 mt-6 pt-6 border-t border-slate-700/50">
        <div className="text-center">
          <p className="text-2xl font-bold text-white">
            {chartData.reduce((sum, item) => sum + item.value, 0).toLocaleString()}
          </p>
          <p className="text-slate-400 text-sm">Total Jobs</p>
        </div>
        <div className="text-center">
          <p className="text-2xl font-bold text-emerald-400">
            {Math.max(...chartData.map(item => item.value)).toLocaleString()}
          </p>
          <p className="text-slate-400 text-sm">Highest Category</p>
        </div>
        <div className="text-center">
          <p className="text-2xl font-bold text-blue-400">
            {chartData.length}
          </p>
          <p className="text-slate-400 text-sm">Categories</p>
        </div>
      </div>
    </div>
  );
}

export default JobTrendsChart;