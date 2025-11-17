import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import "./App.css";
import Login from "./components/Login";
import RegisteringAsComponent from "./components/RegisteringAsComponent";
import SignUp from "./components/SignUp";
import VerificationComponent from "./components/VerificationComponent";
import CausesComponent from "./components/CausesComponent";
import SizeOptionSelection from "./components/SizeOptionSelection";
import RegistrationForm from "./components/CombinedForm";
import HomePage from "./components/HomePage"; // ✅ CHANGED: Import HomePage instead of WelcomeScreen
import AnalyticsPage from "./components/AnalyticsPage";

const App = () => {
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

        {/* ✅ CHANGED: /home route instead of /register/welcome */}
        <Route path="/home" element={<HomePage />} />
        <Route path="/analytics" element={<AnalyticsPage />}/>

        {/* Catch-all redirect to login */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
};

export default App;