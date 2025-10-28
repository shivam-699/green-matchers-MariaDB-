const LoadingSpinner = ({ message = "Initializing Green Matchers..." }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 relative overflow-hidden">
      
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-30">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="text-center relative z-10">
        
        {/* Animated Spinner */}
        <div className="relative mb-10 inline-block">
          {/* Outer Ring */}
          <div className="w-32 h-32 border-4 border-slate-700/30 rounded-full"></div>
          <div className="w-32 h-32 border-4 border-transparent border-t-blue-500 border-r-blue-500 rounded-full animate-spin absolute top-0 left-0"></div>
          
          {/* Middle Ring */}
          <div className="w-24 h-24 border-4 border-slate-700/30 rounded-full absolute top-4 left-4"></div>
          <div className="w-24 h-24 border-4 border-transparent border-t-emerald-500 border-r-emerald-500 rounded-full animate-spin absolute top-4 left-4" style={{ animationDuration: '1.5s', animationDirection: 'reverse' }}></div>
          
          {/* Inner Ring */}
          <div className="w-16 h-16 border-4 border-slate-700/30 rounded-full absolute top-8 left-8"></div>
          <div className="w-16 h-16 border-4 border-transparent border-t-purple-500 border-r-purple-500 rounded-full animate-spin absolute top-8 left-8" style={{ animationDuration: '2s' }}></div>
          
          {/* Center Icon */}
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-4xl animate-pulse">
            ✨
          </div>
        </div>

        {/* Message */}
        <div className="space-y-3 mb-8">
          <h2 className="text-2xl font-bold text-white">{message}</h2>
          <p className="text-slate-400 text-sm font-medium">
            Powered by AI • Sustainable Careers • Real Impact
          </p>
        </div>

        {/* Animated Dots */}
        <div className="flex justify-center items-center gap-2 mb-6">
          <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce"></div>
          <div className="w-3 h-3 bg-emerald-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-3 h-3 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>

        {/* Features Loading */}
        <div className="flex justify-center items-center gap-8 text-slate-500 text-sm">
          <div className="flex items-center gap-2 animate-pulse">
            <span className="text-emerald-400 text-lg">🌱</span>
            <span>Green Jobs</span>
          </div>
          <div className="flex items-center gap-2 animate-pulse" style={{ animationDelay: '0.3s' }}>
            <span className="text-blue-400 text-lg">⚡</span>
            <span>AI Matching</span>
          </div>
          <div className="flex items-center gap-2 animate-pulse" style={{ animationDelay: '0.6s' }}>
            <span className="text-purple-400 text-lg">✨</span>
            <span>Real-time Data</span>
          </div>
        </div>

      </div>
    </div>
  );
};

export default LoadingSpinner;