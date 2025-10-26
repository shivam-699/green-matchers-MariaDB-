import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="py-8 text-center">
      <h2 className="text-3xl font-bold mb-4">Welcome to Green Matchers</h2>
      <p className="text-gray-600 mb-6">Find sustainable jobs that match your skills and make a positive impact.</p>
      <Link to="/login" className="bg-green-600 text-white p-2 rounded">
        Get Started
      </Link>
    </div>
  );
}

export default Home;