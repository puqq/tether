import React, { useState } from 'react';
import axios from 'axios';

function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [message, setMessage] = useState('');

  const handleRegister = (e) => {
    e.preventDefault();
    axios.post('http://127.0.0.1:8000/api/register/', {
      username,
      email,
      password1,
      password2
    }, {
      withCredentials: true
    })
    .then(response => {
        setMessage('User registered successfully!');
        // Mark user as "auth" in localStorage, if you want to skip a separate login step
        localStorage.setItem('isAuth', 'true');
        
        // Redirect straight to /relationships
        window.location.href = '/relationships';
      })
    .catch(error => {
      setMessage('Error registering user.');
      console.error('Registration error:', error);
      // Optional: show the server’s error details
      if (error.response) {
        console.log('Response data:', error.response.data);
      }
    });
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
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
          <label>Email: </label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password: </label>
          <input
            type="password"
            value={password1}
            onChange={e => setPassword1(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Confirm Password: </label>
          <input
            type="password"
            value={password2}
            onChange={e => setPassword2(e.target.value)}
            required
          />
        </div>
        <button type="submit">Register</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default Register;
