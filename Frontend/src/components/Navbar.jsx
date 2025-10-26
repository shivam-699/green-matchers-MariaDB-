import { NavLink } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-green-600 p-4">
      <div className="container mx-auto flex justify-between">
        <h1 className="text-white text-2xl font-bold">Green Matchers</h1>
        <div className="space-x-4">
          <NavLink to="/" className="text-white hover:text-gray-200">Home</NavLink>
          <NavLink to="/dashboard" className="text-white hover:text-gray-200">Dashboard</NavLink>
          <NavLink to="/login" className="text-white hover:text-gray-200">Login</NavLink>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;