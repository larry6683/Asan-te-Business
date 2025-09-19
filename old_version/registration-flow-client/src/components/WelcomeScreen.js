import React, { useEffect, useState } from "react";
import styles from "./WelcomeScreen.module.css";
import { styled } from "@mui/material/styles";
import { Box, Typography, Button, Paper, useTheme, Link } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import businessWelcome from "../assets/HomeScreen-Confetti.svg";
// import nonprofitWelcome from "../assets/welcome_nonprofit.png";
import welcomePortal from "../assets/WelcomePortal.svg";
import { AppCookieService } from "../cookies/appCookieService";
import { redirectUrls } from "../web-data/redirectUrls";

const WelcomeScreen = () => {
  const selectedOption = useSelector((state) => state.selectedOption);
  const [selectedType, setSelectedType] = useState(
    sessionStorage.getItem("asante:selectedOption") || "Business",
  );

  useEffect(() => {
    const selectedOption = sessionStorage.getItem("asante:selectedOption");
    if (selectedOption) {
      setSelectedType(selectedOption);
    }
    // this can be commented out while testing
    const appCookie = AppCookieService.getAppCookie();
    console.log(appCookie);
  }, []);

  const backgroundImageUrl = businessWelcome;
  const portalImageUrl = welcomePortal;
  // selectedType === "Non-Profit" ? nonprofitWelcome : businessWelcome;

  const navigate = useNavigate();
  const handleNext = () => {
    // console.log("Next button clicked");
    setTimeout(() => {
      window.location.href = `${redirectUrls.portal}`;
    }, 500);
  };

  const handleSkipClick = () => {
    // console.log("Skip button clicked");
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
            // margin: "0",
            // position: "relative",
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
            <Typography 
              height="15%"
              variant="body1"
              gutterBottom
              marginTop="15%"
              sx={{
                marginBottom: 0,
                color: "#000",
                fontFamily: "Helvetica Neue",
                fontSize: "30px",
                fontStyle: "normal",
                fontWeight: 400,
                lineHeight: "normal",
              }}>
                Welcome to your portal on {' '}
                <span className={styles.highlight} sx={{
                  marginLeft: "10px"
                }}>
                AsanTe
                </span>
            </Typography>
            <Box
              width="85%"
              height="85%"
              sx={{
                background: `url(${portalImageUrl})`,
                backgroundSize: "contain",
                backgroundRepeat: "no-repeat",
                flexGrow: "1",
                marginTop: "4vh"
              }}>
            </Box>
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

export default WelcomeScreen;
