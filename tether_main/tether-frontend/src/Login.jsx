// src/Login.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError]       = useState('');
  const { setUser }             = useAuth();
  const navigate                = useNavigate();

  const handleLogin = async e => {
    e.preventDefault();
    setError('');
    try {
      // 1) send credentials
      await axios.post('/api/login/', 
        { username, password }, 
        { withCredentials: true }
      );

      // 2) fetch the current user
      const res = await axios.get('/api/users/me/', { withCredentials: true });
      setUser(res.data);           // ← update AuthContext

      // 3) navigate to the protected page
      navigate('/relationships');
    } catch (err) {
      console.error('Login error:', err);
      setError('Invalid username or password');
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleLogin}>
        <div>
          <label>Username:&nbsp;</label>
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
          />
        </div>
        <div style={{ marginTop: 8 }}>
          <label>Password:&nbsp;</label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </div>
        <button style={{ marginTop: 12 }} type="submit">
          Login
        </button>
      </form>
      <p style={{ marginTop: 12 }}>
        Don't have an account? <Link to="/register">Register here</Link>
      </p>
    </div>
  );
}
