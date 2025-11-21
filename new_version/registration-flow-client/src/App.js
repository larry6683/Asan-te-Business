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
import AnalyticsDashboard from "./components/AnalyticsDashboard";
import PublicRoute from "./components/PublicRoute";
import UserProfile from "./components/UserProfile"; // ✅ IMPORT THIS
import { analyticsService } from "./api/analyticsService";

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
        <Route element={<PublicRoute />}>
            <Route path="/" element={<Login />} />
            <Route path="/register" element={<RegisteringAsComponent />} />
            <Route path="/register/signup" element={<SignUp />} />
        </Route>
        
        <Route path="/register/verification" element={<VerificationComponent />} />
        <Route path="/register/causes" element={<CausesComponent />} />
        <Route path="/register/sizeoptionselection" element={<SizeOptionSelection />} />
        <Route path="/register/registrationform" element={<RegistrationForm />} />

        <Route path="/home" element={<HomePage />} />
        <Route path="/analytics" element={<AnalyticsDashboard />}/>
        
        {/* ✅ ADDED PROFILE ROUTE */}
        <Route path="/profile" element={<UserProfile />} />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};

export default App;