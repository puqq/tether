// src/App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import NavBar from './NavBar';
import PrivateRoute from './PrivateRoute';
import Register from './Register';
import Login from './login';
import RelationshipsPage from './RelationshipsPage';

function App() {
  return (
    <div style={{ padding: 20 }}>
      <h1>Welcome to Tether</h1>
      <NavBar />
      <hr />
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<div>Home Page</div>} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />

        {/* Protected routes */}
        <Route element={<PrivateRoute />}>
          <Route path="/relationships" element={<RelationshipsPage />} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;
