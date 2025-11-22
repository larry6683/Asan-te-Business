import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const PublicRoute = () => {
  // 1. Check Authentication
  const token = sessionStorage.getItem("asante:accessJwt");
  
  // 2. Check Registration Status
  const businessId = sessionStorage.getItem("asante:businessId");
  const beneficiaryId = sessionStorage.getItem("asante:beneficiaryId");
  
  const isAuthenticated = !!token;
  const isRegistrationComplete = !!(businessId || beneficiaryId);

  // 3. Logic: If Logged In, Redirect based on status
  if (isAuthenticated) {
    if (isRegistrationComplete) {
      // Fully registered -> Go to Dashboard
      console.log("🔄 PublicRoute: User already logged in & complete. Redirecting to Home.");
      return <Navigate to="/home" replace />;
    } else {
      // Logged in but incomplete -> Resume Registration
      console.log("🔄 PublicRoute: User logged in but incomplete. Redirecting to Causes.");
      return <Navigate to="/register/causes" replace />;
    }
  }

  // 4. Not Logged In -> Allow access to Login, Signup, Verification
  return <Outlet />;
};

export default PublicRoute;