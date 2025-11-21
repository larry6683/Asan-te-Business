/*
  FILENAME: new_version/registration-flow-client/src/components/HomePage.js
  DESCRIPTION: 
    - Implements a "Dashboard" background view.
    - "Welcome" screen is now an overlay (Modal style) that can be dismissed.
    - Added "Profile" button navigating to /profile.
*/
import React, { useEffect, useState } from "react";
import styles from "./HomePage.module.css";
import { Box, Typography, Button, IconButton, AppBar, Toolbar } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import MenuIcon from "@mui/icons-material/Menu";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import businessWelcome from "../assets/HomeScreen-Confetti.svg";
import welcomePortal from "../assets/WelcomePortal.svg";
import { AppCookieService } from "../cookies/appCookieService";
import { analyticsService } from "../api/analyticsService";
import { logoutUser } from "../authentication/logoutUser";
import { AsanteUsersUserPool } from "../user-auth/asanteUsersUserPool"; 

const HomePage = () => {
  const [userData, setUserData] = useState(null);
  const [entityData, setEntityData] = useState(null);
  const [showWelcome, setShowWelcome] = useState(true); // ✅ Controls the popup visibility

  const navigate = useNavigate();

  useEffect(() => {
    analyticsService.trackStep(6, 0, 0);

    try {
      const userStr = sessionStorage.getItem("asante:user");
      if (userStr) {
        const user = JSON.parse(userStr);
        setUserData(user);
      }

      const businessId = sessionStorage.getItem("asante:businessId");
      const beneficiaryId = sessionStorage.getItem("asante:beneficiaryId");

      if (businessId) {
        setEntityData({ type: 'business', id: businessId });
      } else if (beneficiaryId) {
        setEntityData({ type: 'beneficiary', id: beneficiaryId });
      }
    } catch (error) {
      console.error('Error loading user data:', error);
    }

    const appCookie = AppCookieService.getAppCookie();
    console.log('HomePage loaded - Cookie:', appCookie);
  }, []);

  const handleDismiss = () => {
    console.log("Dismissing welcome screen -> Showing Dashboard");
    setShowWelcome(false); // ✅ Just hide the popup, don't redirect
  };

  const handleProfile = () => {
    console.log("Navigating to Profile...");
    navigate('/profile');
  };

  const handleLogout = () => {
    console.log("Logging out...");
    const email = userData?.email || JSON.parse(sessionStorage.getItem("asante:user") || '{}').email;
    
    const performLocalLogout = () => {
      sessionStorage.clear();
      navigate("/");
    };

    if (email) {
      logoutUser(
        AsanteUsersUserPool, 
        email, 
        (msg) => {
          console.log("Cognito Logout Success:", msg);
          performLocalLogout();
        },
        (err) => {
          console.error("Cognito Logout Error:", err);
          performLocalLogout();
        }
      );
    } else {
      performLocalLogout();
    }
  };

  // --- RENDER ---

  return (
    <Box sx={{ height: "100vh", width: "100vw", overflow: "hidden", position: "relative", backgroundColor: "#F4F6F8" }}>
      
      {/* ✅ BACKGROUND DASHBOARD CONTENT (Visible when popup is closed) */}
      <Box sx={{ height: "100%", display: "flex", flexDirection: "column" }}>
        {/* Simple Header */}
        <AppBar position="static" sx={{ backgroundColor: "white", color: "black", boxShadow: 1 }}>
          <Toolbar>
            <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" sx={{ flexGrow: 1, color: "#6271AE", fontWeight: "bold" }}>
              AsanTe Dashboard
            </Typography>
            {userData && <Typography variant="body2" sx={{ mr: 2 }}>{userData.email}</Typography>}
            <Button color="inherit" onClick={handleLogout}>Logout</Button>
          </Toolbar>
        </AppBar>

        {/* Main Content Area */}
        <Box sx={{ p: 4, flexGrow: 1, display: "flex", justifyContent: "center", alignItems: "center" }}>
          <Typography variant="h4" color="textSecondary">
            Dashboard Content Goes Here
          </Typography>
        </Box>
      </Box>

      {/* ✅ WELCOME POPUP OVERLAY */}
      {showWelcome && (
        <Box
          sx={{
            position: "absolute",
            top: 0,
            left: 0,
            height: "100%",
            width: "100%",
            zIndex: 1200, // High z-index to sit on top
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            backgroundImage: `url(${businessWelcome})`,
            backgroundSize: "cover",
            backgroundPosition: "center center",
            backgroundRepeat: "no-repeat",
            backdropFilter: "blur(5px)" // Optional: blur the background slightly
          }}
        >
          <Box
            className={styles.box}
            sx={{
              display: "flex",
              flexDirection: "column",
              flexWrap: "nowrap",
              alignItems: "center",
              alignContent: "flex-end",
              minWidth: 500,
              minHeight: 650,
              position: "relative",
              backgroundColor: "white",
              borderRadius: "25px",
              boxShadow: "0px 10px 30px rgba(0,0,0,0.1)"
            }}
          >
            {/* Dismiss Button */}
            <Box sx={{ position: 'absolute', top: 15, right: 15, zIndex: 10 }}>
              <IconButton onClick={handleDismiss} aria-label="dismiss">
                <CloseIcon sx={{ color: "#999", fontSize: "1.5rem" }} />
              </IconButton>
            </Box>

            {userData && (
              <Typography
                sx={{
                  color: "#6d7cb0",
                  fontFamily: "Helvetica Neue",
                  fontSize: "18px",
                  fontWeight: 500,
                  marginTop: "30px",
                }}
              >
                {userData.email}
              </Typography>
            )}

            <Typography 
              height="15%"
              variant="body1"
              gutterBottom
              marginTop={userData ? "2%" : "10%"}
              sx={{
                marginBottom: 0,
                color: "#000",
                fontFamily: "Helvetica Neue",
                fontSize: "30px",
                fontWeight: 400,
              }}
            >
              Welcome to your portal on {' '}
              <span className={styles.highlight}>AsanTe</span>
            </Typography>

            {entityData && (
              <Typography
                sx={{
                  color: "#999",
                  fontFamily: "Helvetica Neue",
                  fontSize: "14px",
                  marginTop: "5px",
                }}
              >
                {entityData.type === 'business' ? '🏢 Business' : '💚 Non-Profit'} Account
              </Typography>
            )}

            <Box
              width="85%"
              height="85%"
              sx={{
                background: `url(${welcomePortal})`,
                backgroundSize: "contain",
                backgroundRepeat: "no-repeat",
                backgroundPosition: "center",
                flexGrow: "1",
                marginTop: "2vh",
                marginBottom: "2vh"
              }}
            />

            {/* ✅ ADDED: Profile Button */}
            <Button
              fullWidth
              variant="contained"
              sx={{
                width: "13vw",
                height: "50px",
                fontSize: "18px",
                fontWeight: 500,
                borderRadius: "28px",
                textTransform: "none",
                background: "linear-gradient(to right, #6271AE, #9ACDDA)",
                color: "#FFF",
                marginBottom: "2vh", // Spacing between buttons
                minWidth: 200,
                "&:hover": {
                  background: "linear-gradient(to right, #5B6BB0, #8ACDDB)",
                },
              }}
              onClick={handleProfile}
            >
              Profile
            </Button>

            {/* Logout Button */}
            <Button
              fullWidth
              variant="outlined"
              sx={{
                width: "13vw",
                height: "50px",
                fontSize: "18px",
                fontWeight: 500,
                borderRadius: "28px",
                textTransform: "none",
                borderColor: "#6271AE",
                color: "#6271AE",
                marginBottom: "5vh",
                minWidth: 200,
                "&:hover": {
                  backgroundColor: "#F5F5F5",
                  borderColor: "#5B6BB0",
                },
              }}
              onClick={handleLogout}
            >
              Logout
            </Button>
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default HomePage;