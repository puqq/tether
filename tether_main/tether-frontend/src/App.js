// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Register from './Register';
import RelationshipsPage from './RelationshipsPage';
import Login from './login';

function App() {
  return (
    <Router>
      <div style={{ padding: '20px' }}>
        <h1>Welcome to Tether</h1>
        <nav>
          <Link to="/">Home</Link> |{' '}
          <Link to="/login">Login</Link> |{' '}
          <Link to="/relationships">Manage Relationships</Link>
        </nav>
        <hr />

        <Routes>
          <Route path="/" element={<div>Home Page</div>} />
          {/* No link in nav, but we still have a /register route */}
          <Route path="/register" element={<Register />} /> 
          <Route path="/login" element={<Login />} />
          <Route path="/relationships" element={<RelationshipsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
