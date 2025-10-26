function JobCard({ job, onSave }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow-md mb-4">
      <h3 className="text-xl font-bold">{job.job_title}</h3>
      <p className="text-gray-700">{job.company} - {job.location}</p>
      <p className="text-gray-600">{job.description}</p>
      <p className="text-green-600 font-semibold">{job.salary_range}</p>
      <p className="text-gray-500">SDG Impact: {job.sdg_impact}</p>
      <a href={job.website} target="_blank" className="text-blue-500">Apply</a>
      <button
        onClick={() => onSave(job.id)}
        className="ml-4 bg-green-600 text-white p-2 rounded"
      >
        Save Job
      </button>
    </div>
  );
}

export default JobCard;