import React from 'react'
import { useAuth } from './AuthContext'
import { Navigate, Outlet } from 'react-router-dom'

export default function PrivateRoute() {
  const { user } = useAuth()
  if (user === undefined) {
    // still loading auth state
    return <div>Loading…</div>
  }
  return user ? <Outlet /> : <Navigate to="/login" replace />
}
