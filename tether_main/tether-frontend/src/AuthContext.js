import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(undefined);
  // undefined = “still loading”, null = “no user”, object = “logged in”

  useEffect(() => {
    // On mount, try to fetch the current user
    axios.get('/api/users/me/')
      .then(res => setUser(res.data))
      .catch(() => setUser(null));
  }, []);

  const logout = () =>
    axios.post('/api/logout/')
         .then(() => setUser(null));

  return (
    <AuthContext.Provider value={{ user, setUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
