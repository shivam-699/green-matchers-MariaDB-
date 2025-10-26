import Login from '../components/Login';
import { useState } from 'react';

function LoginPage() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');

  return (
    <div className="py-8">
      <Login setToken={(token) => {
        localStorage.setItem('token', token);
        setToken(token);
      }} />
    </div>
  );
}

export default LoginPage;