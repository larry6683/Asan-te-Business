import React, { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import "./App.css";
import Login from "./components/Login";
import RegisteringAsComponent from "./components/RegisteringAsComponent";
import SignUp from "./components/SignUp";
import VerificationComponent from "./components/VerificationComponent";
import CausesComponent from "./components/CausesComponent";
import SizeOptionSelection from "./components/SizeOptionSelection";
import RegistrationForm from "./components/CombinedForm";
import HomePage from "./components/HomePage";
import AnalyticsPage from "./components/AnalyticsPage";
import { analyticsService } from "./api/analyticsService"; // ✅ Import Analytics Service

const App = () => {
  
  // ✅ ADDED: Track initial session on app load
  useEffect(() => {
    const initSession = async () => {
      try {
        // Track Step 1 (Welcome/Signup) immediately as Anonymous
        // This creates the session in the database with "In Progress" status
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
        {/* Login route */}
        <Route path="/" element={<Login />} />
        
        {/* Registration flow routes */}
        <Route path="/register">
          <Route index element={<RegisteringAsComponent />} />
          <Route path="signup" element={<SignUp />} />
          <Route path="verification" element={<VerificationComponent />} />
          <Route path="causes" element={<CausesComponent />} />
          <Route path="sizeoptionselection" element={<SizeOptionSelection />} />
          <Route path="registrationform" element={<RegistrationForm />} />
        </Route>

        {/* /home route */}
        <Route path="/home" element={<HomePage />} />
        <Route path="/analytics" element={<AnalyticsPage />}/>

        {/* Catch-all redirect to login */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};

export default App;