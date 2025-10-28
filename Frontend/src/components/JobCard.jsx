import { MapPin, Building2, DollarSign, ExternalLink, Bookmark, Target, Calendar } from 'lucide-react';
import { useState } from 'react';

function JobCard({ job, onSave }) {
  const [isSaved, setIsSaved] = useState(false);

  const handleSave = () => {
    setIsSaved(!isSaved);
    onSave?.(job.id);
  };

  return (
    <div className="group relative bg-slate-800/40 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 hover:border-slate-600 hover:bg-slate-800/60 transition-all duration-300 hover:-translate-y-1">
      
      {/* Gradient Overlay on Hover */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>

      {/* Content */}
      <div className="relative z-10">
        
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-xl font-bold text-white mb-2 group-hover:text-blue-400 transition-colors">
              {job.job_title}
            </h3>
            <div className="flex items-center gap-4 text-slate-400 text-sm">
              <div className="flex items-center gap-1.5">
                <Building2 className="w-4 h-4" />
                <span>{job.company}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <MapPin className="w-4 h-4" />
                <span>{job.location}</span>
              </div>
            </div>
          </div>

          {/* Save Button */}
          <button
            onClick={handleSave}
            className={`p-2.5 rounded-xl transition-all ${
              isSaved 
                ? 'bg-blue-500 text-white' 
                : 'bg-slate-700/50 text-slate-400 hover:bg-slate-700 hover:text-white'
            }`}
            aria-label={isSaved ? 'Unsave job' : 'Save job'}
          >
            <Bookmark className={`w-5 h-5 ${isSaved ? 'fill-current' : ''}`} />
          </button>
        </div>

        {/* Description */}
        <p className="text-slate-300 text-sm leading-relaxed mb-4 line-clamp-2">
          {job.description}
        </p>

        {/* Details Grid */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          {/* Salary */}
          <div className="flex items-center gap-2 px-3 py-2 bg-slate-700/30 rounded-lg">
            <DollarSign className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span className="text-emerald-400 font-semibold text-sm">{job.salary_range}</span>
          </div>

          {/* SDG Impact */}
          <div className="flex items-center gap-2 px-3 py-2 bg-slate-700/30 rounded-lg">
            <Target className="w-4 h-4 text-purple-400 flex-shrink-0" />
            <span className="text-purple-400 font-semibold text-sm truncate">
              SDG {job.sdg_impact}
            </span>
          </div>
        </div>

        {/* Tags */}
        {job.tags && (
          <div className="flex flex-wrap gap-2 mb-4">
            {job.tags.slice(0, 3).map((tag, index) => (
              <span 
                key={index}
                className="px-3 py-1 bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs font-medium rounded-full"
              >
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* Footer Actions */}
        <div className="flex items-center gap-3 pt-4 border-t border-slate-700/50">
          {/* Posted Date */}
          {job.posted_date && (
            <div className="flex items-center gap-1.5 text-slate-400 text-xs">
              <Calendar className="w-3.5 h-3.5" />
              <span>{job.posted_date}</span>
            </div>
          )}

          <div className="flex-1"></div>

          {/* Apply Button */}
          <a
            href={job.website}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white rounded-xl transition-all font-semibold text-sm shadow-lg hover:shadow-xl hover:scale-105"
          >
            <span>Apply Now</span>
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
      </div>
    </div>
  );
}

export default JobCard;