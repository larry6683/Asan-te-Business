import React, { useEffect } from "react";
// ✅ FIXED: Added 'Outlet' to the imports
import { BrowserRouter as Router, Route, Routes, Navigate, Outlet } from "react-router-dom";
import "./App.css";
import Login from "./components/Login";
import RegisteringAsComponent from "./components/RegisteringAsComponent";
import SignUp from "./components/SignUp";
import VerificationComponent from "./components/VerificationComponent";
import CausesComponent from "./components/CausesComponent";
import SizeOptionSelection from "./components/SizeOptionSelection";
import RegistrationForm from "./components/CombinedForm";
import NonprofitRegistrationForm from "./components/NonprofitRegistrationForm";
import HomePage from "./components/HomePage";
import AnalyticsDashboard from "./components/AnalyticsDashboard";
import UserProfile from "./components/UserProfile";
import { analyticsService } from "./api/analyticsService";

// Import Route Guards
import PublicRoute from "./components/PublicRoute";
import RegistrationRoute from "./components/RegistrationRoute";
import ProtectedRoute from "./components/ProtectedRoute";

const App = () => {
  
  useEffect(() => {
    const initSession = async () => {
      try {
        console.log("🚀 App loaded - Initializing Analytics Session...");
        await analyticsService.trackStep(1);
      } catch (error) {
        console.error("Failed to track initial session:", error);
      }
    };
    initSession();
  }, []);

  return (
    <Router>
      <Routes>
        {/* ✅ PUBLIC ROUTES: Login, Signup, Verification 
          - If Not Logged In: Accessible
          - If Logged In + Complete: Redirects to /home
          - If Logged In + Incomplete: Redirects to /register/causes
        */}
        <Route element={<PublicRoute />}>
            <Route path="/" element={<Login />} />
            <Route path="/register" element={<RegisteringAsComponent />} />
            <Route path="/register/signup" element={<SignUp />} />
            <Route path="/register/verification" element={<VerificationComponent />} />
            <Route path="/analytics" element={<AnalyticsDashboard />}/>
        </Route>

        {/* ✅ REGISTRATION STEPS: Causes, Size, Forms
          - If Not Logged In: Redirects to Login
          - If Logged In + Complete: Redirects to /home
          - If Logged In + Incomplete: Accessible
        */}
        <Route element={<RegistrationRoute />}>
            <Route path="/register/causes" element={<CausesComponent />} />
            <Route path="/register/sizeoptionselection" element={<SizeOptionSelection />} />
            <Route path="/register/registrationform" element={<RegistrationForm />} />
            <Route path="/register/nonprofit" element={<NonprofitRegistrationForm />} />
        </Route>

        {/* ✅ APP ROUTES: Home, Profile, Analytics
          - ProtectedRoute checks for token. 
          - We pass <Outlet /> as the element so nested routes render.
        */}
        <Route element={<ProtectedRoute element={<Outlet />} />}> 
            <Route path="/home" element={<HomePage />} />
            <Route path="/profile" element={<UserProfile />} />
            
        </Route>

        {/* Catch-all */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};

export default App;