/*
  FILENAME: new_version/registration-flow-client/src/components/ProtectedRoute.js
  DESCRIPTION: New component to protect routes from unauthenticated access.
*/
import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ element }) => {
  // Check for the authentication token in session storage
  const token = sessionStorage.getItem("asante:accessJwt");

  if (!token) {
    // If no token, redirect to the login page
    return <Navigate to="/" replace />;
  }

  // If token exists, render the requested component
  return element;
};

export default ProtectedRoute;