import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import "./App.css";
import Login from "./components/Login";
import RegisteringAsComponent from "./components/RegisteringAsComponent";
import SignUp from "./components/SignUp";
import VerificationComponent from "./components/VerificationComponent";
import CausesComponent from "./components/CausesComponent";
import SizeOptionSelection from "./components/SizeOptionSelection";
import BusinessRegistrationForm from "./components/BusinessRegistrationForm";
import NonprofitRegistrationForm from "./components/NonprofitRegistrationForm";
import RegistrationForm from "./components/CombinedForm";
import WelcomeScreen from "./components/WelcomeScreen";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register">
          <Route index element={<RegisteringAsComponent />} />
          <Route path="signup" element={<SignUp />} />
          <Route path="verification" element={<VerificationComponent />} />
          <Route path="causes" element={<CausesComponent />} />
          <Route path="sizeoptionselection" element={<SizeOptionSelection />} />
          <Route path="businessregister" element={<BusinessRegistrationForm />} />
          <Route path="nonprofitregister" element={<NonprofitRegistrationForm />} />
          <Route path="registrationform" element={<RegistrationForm />} />
          <Route path="welcome" element={<WelcomeScreen />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
