// src/login.js
import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('login', username);
    formData.append('password', password);

    axios.post('http://127.0.0.1:8000/accounts/login/', formData, {
      withCredentials: true
    })
    .then(response => {
      setMessage('Login successful!');
      localStorage.setItem('isAuth', 'true'); 
      window.location.href = '/relationships'; // redirect to manage relationships
    })
    .catch(error => {
      setMessage('Error logging in. Check username/password.');
      console.error(error);
    });
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Username: </label>
          <input 
            type="text" 
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password: </label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
      
      {message && <p>{message}</p>}

      {/* Link to Register Page */}
      <p>Don't have an account?{' '}
         <Link to="/register">Register here</Link>
      </p>
    </div>
  );
}

export default Login;
