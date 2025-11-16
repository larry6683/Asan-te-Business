import React, { useEffect, useState } from "react";
import styles from "./HomePage.module.css";
import { styled } from "@mui/material/styles";
import { Box, Typography, Button, Paper, useTheme, Link } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import businessWelcome from "../assets/HomeScreen-Confetti.svg";
import welcomePortal from "../assets/WelcomePortal.svg";
import { AppCookieService } from "../cookies/appCookieService";
import { redirectUrls } from "../web-data/redirectUrls";

const HomePage = () => {
  const selectedOption = useSelector((state) => state.selectedOption);
  const [selectedType, setSelectedType] = useState(
    sessionStorage.getItem("asante:selectedOption") || "Business",
  );
  const [userData, setUserData] = useState(null);
  const [entityData, setEntityData] = useState(null);

  useEffect(() => {
    const selectedOption = sessionStorage.getItem("asante:selectedOption");
    if (selectedOption) {
      setSelectedType(selectedOption);
    }

    // Load user data
    try {
      const userStr = sessionStorage.getItem("asante:user");
      if (userStr) {
        const user = JSON.parse(userStr);
        setUserData(user);
      }

      // Load entity data
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

    // Log cookie for debugging
    const appCookie = AppCookieService.getAppCookie();
    console.log('HomePage loaded - Cookie:', appCookie);
  }, []);

  const backgroundImageUrl = businessWelcome;
  const portalImageUrl = welcomePortal;

  const navigate = useNavigate();
  
  const handleNext = () => {
    console.log("Navigating to portal...");
    setTimeout(() => {
      window.location.href = `${redirectUrls.portal}`;
    }, 500);
  };

  return (
    <React.Fragment>
      <Box>
        <Box
          sx={{
            display: "flex",
            flexDirection: "row",
            justifyContent: "center",
            alignItems: "center",
            height: "100vh",
            width: "100vw",
            backgroundImage: `url(${backgroundImageUrl})`,
            backgroundSize: "cover",
            backgroundPosition: "center center",
            backgroundRepeat: "no-repeat",
            overflow: "hidden",
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
              minHeight: 650
            }}
          >
            {userData && (
              <Typography
                sx={{
                  color: "#6d7cb0",
                  fontFamily: "Helvetica Neue",
                  fontSize: "18px",
                  fontWeight: 500,
                  marginTop: "20px",
                }}
              >
                {userData.email}
              </Typography>
            )}

            <Typography 
              height="15%"
              variant="body1"
              gutterBottom
              marginTop={userData ? "5%" : "15%"}
              sx={{
                marginBottom: 0,
                color: "#000",
                fontFamily: "Helvetica Neue",
                fontSize: "30px",
                fontStyle: "normal",
                fontWeight: 400,
                lineHeight: "normal",
              }}
            >
              Welcome to your portal on {' '}
              <span className={styles.highlight}>
                AsanTe
              </span>
            </Typography>

            {entityData && (
              <Typography
                sx={{
                  color: "#999",
                  fontFamily: "Helvetica Neue",
                  fontSize: "14px",
                  marginTop: "10px",
                }}
              >
                {entityData.type === 'business' ? '🏢 Business' : '💚 Non-Profit'} Account
              </Typography>
            )}

            <Box
              width="85%"
              height="85%"
              sx={{
                background: `url(${portalImageUrl})`,
                backgroundSize: "contain",
                backgroundRepeat: "no-repeat",
                flexGrow: "1",
                marginTop: "4vh"
              }}
            />

            <Button
              fullWidth
              variant="contained"
              sx={{
                width: "13vw",
                height: "56px",
                fontSize: "24px",
                fontWeight: 500,
                borderRadius: "28px",
                textTransform: "none",
                background: "linear-gradient(to right, #6271AE, #9ACDDA)",
                opacity: 1,
                color: "var(--barcolor, #FFF)",
                "&:hover": {
                  opacity: 1,
                  background: "linear-gradient(to right, #5B6BB0, #8ACDDB)",
                },
                marginBottom: "8vh",
                minWidth: 200
              }}
              onClick={handleNext}
            >
              Next
            </Button>
          </Box>
        </Box>
      </Box>
    </React.Fragment>
  );
};

export default HomePage;