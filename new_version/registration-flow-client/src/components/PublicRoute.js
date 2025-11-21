import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const PublicRoute = () => {
  // 1. Check for Authentication Token
  const accessToken = sessionStorage.getItem("asante:accessJwt");
  
  // 2. Check for Entity IDs (Business or Beneficiary)
  const businessId = sessionStorage.getItem("asante:businessId");
  const beneficiaryId = sessionStorage.getItem("asante:beneficiaryId");
  
  const isAuthenticated = !!accessToken;
  const hasEntity = !!(businessId || beneficiaryId);

  // 3. Redirect Logic
  if (isAuthenticated) {
    if (hasEntity) {
      // User is fully registered and logged in -> Go Home
      console.log("🔄 User already logged in with Entity. Redirecting to Home.");
      return <Navigate to="/home" replace />;
    } else {
      // User is logged in but hasn't finished registration -> Resume Flow
      console.log("🔄 User logged in but incomplete. Redirecting to Causes.");
      return <Navigate to="/register/causes" replace />;
    }
  }

  // 4. Not logged in? Allow access to public pages (Login, Signup)
  return <Outlet />;
};

export default PublicRoute;