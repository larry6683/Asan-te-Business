import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const RegistrationRoute = () => {
  const token = sessionStorage.getItem("asante:accessJwt");
  const businessId = sessionStorage.getItem("asante:businessId");
  const beneficiaryId = sessionStorage.getItem("asante:beneficiaryId");
  
  const isAuthenticated = !!token;
  const isRegistrationComplete = !!(businessId || beneficiaryId);

  // 1. Must be logged in to access registration steps
  if (!isAuthenticated) {
    console.log("⛔ RegistrationRoute: Not authenticated. Redirecting to Login.");
    return <Navigate to="/" replace />;
  }

  // 2. If already fully registered, shouldn't be here -> Go Home
  if (isRegistrationComplete) {
    console.log("✅ RegistrationRoute: Registration already complete. Redirecting to Home.");
    return <Navigate to="/home" replace />;
  }

  // 3. Authenticated + Incomplete -> Allow access to forms
  return <Outlet />;
};

export default RegistrationRoute;