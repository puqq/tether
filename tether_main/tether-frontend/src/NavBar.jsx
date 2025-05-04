import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

export default function NavBar() {
  const { user, logout } = useAuth();
  const nav = useNavigate();

  const handleLogout = () =>
    logout().then(() => nav('/login'));

  return (
    <nav style={{ marginBottom: 20 }}>
      <Link to="/">Home</Link>
      {user === undefined
        ? null
        : user
          ? (
            <>
              {' | '}
              <Link to="/relationships">Manage Relationships</Link>
              {' | '}
              <button onClick={handleLogout}>Logout</button>
            </>
          )
          : (
            <>
              {' | '}
              <Link to="/login">Login</Link>
              {' | '}
              <Link to="/register">Register</Link>
            </>
          )
      }
    </nav>
  );
}
