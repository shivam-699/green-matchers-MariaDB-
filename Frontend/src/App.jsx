import { Outlet } from 'react-router-dom';
import Navbar from './components/Navbar.jsx';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <div className="container mx-auto p-4">
        <Outlet />
      </div>
    </div>
  );
}

export default App;