import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import {
  Box,
  Button,
  Typography,
  Avatar,
  IconButton,
  Grid,
  Card,
  CardContent,
  CardActions,
  useTheme,
  useMediaQuery,
} from "@mui/material";
import { ReactComponent as ArrowBackIcon } from "../assets/ionic-ios-arrow-back.svg";
import CloseIcon from "@mui/icons-material/Close";
import styles from "./SizeOptionSelection.module.css";
import logo from "../assets/TE-Logo.svg";
import { styled } from "@mui/system";
import small_business from "../assets/Smallbusiness.png";
import medium_business from "../assets/Mediumbusiness.png";
import large_business from "../assets/LargeBusiness.png";
import small_nonprofit from "../assets/SmallNon-Profit.png";
import medium_nonprofit from "../assets/MediumsizedNon-Profit.png";
import large_nonprofit from "../assets/LargeNon-Profit.png";
import { Stepper, Step, StepLabel } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { setSelectedSize } from "../redux/selectedSizeSlice";
import { logoutCurrentUser } from "../user-auth/logoutUser";

const SizeOptionSelection = () => {
  const [activeStep, setActiveStep] = useState(1);
  const selectedOption = useSelector((state) => state.selectedOption);
  const [selectedType, setSelectedType] = useState(
    sessionStorage.getItem("asante:selectedOption") || "Business",
  );
  const [selected, setSelected] = useState("");
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));
  const isMediumScreen = useMediaQuery(theme.breakpoints.down("md"));

  useEffect(() => {
    const selectedOption = sessionStorage.getItem("asante:selectedOption");
    if (selectedOption) {
      setSelectedType(selectedOption);
    } else {
      setSelectedType("Business");
    }
  }, []);

  const handleBackClick = () => {
    navigate(`/register/causes`);
  };

  const handleClose = () => {
    // setIsVisible(false);
    const navigateToLogin = () =>
      setTimeout(() => {
        navigate(`/`);
      }, 300);
    logoutCurrentUser(navigateToLogin, navigateToLogin);
  };

  const handleNext = (size) => {
    setSelected(size);
    dispatch(setSelectedSize({ selected: size }));
    navigate(`/register/registrationform`);
    // if (selectedOption.selected === "Business") {
    //   navigate(`/register/businessregister`);
    // } else if (selectedOption.selected === "Non-Profit") {
    //   navigate(`/register/form`);
    // }
  };

  const BackButton = styled(Typography)({
    color: "#918C8C",
    fontFamily: '"Helvetica Neue", sans-serif',
    fontSize: "25px",
    display: "flex",
    marginLeft: "8px",
    alignItems: "center",
  });

  const highlightClass =
    selectedOption.selected === "Business"
      ? styles["highlight-business"]
      : selectedOption.selected === "Consumer"
        ? styles["highlight-consumer"]
        : selectedOption.selected === "Non-Profit"
          ? styles["highlight-non-profit"]
          : "";

  const businessOptions = [
    {
      title: "Solopreneur and small business",
      description: "Creating $0- $500 loyalty rewards/month",
      image: small_business,
      size: "small",
    },
    {
      title: "Medium sized business",
      description: "Creating $500- $5000 loyalty rewards/month",
      image: medium_business,
      size: "medium",
    },
    {
      title: "Large Business",
      description: "Creating $5000 + loyalty rewards/month",
      image: large_business,
      size: "large",
    },
  ];

  const nonprofitOptions = [
    {
      title: "Small Non-profit",
      description: "Empowered by 0-50 volunteers",
      image: small_nonprofit,
      size: "small",
    },
    {
      title: "Medium sized Non-profit",
      description: "Empowered by 50-100 volunteers",
      image: medium_nonprofit,
      size: "medium",
    },
    {
      title: "Large Non-profit",
      description: "Empowered by 100+ volunteers/Implemeting programs valued >$1mil",
      image: large_nonprofit,
      option: "large",
    },
  ];

  const businessSteps = ["Causes", "Size", "Basics"];

  const nonprofitSteps = ["Mission", "Size", "Basics"];

  return (
    <Box 
      className={styles.container}
    >
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "16px",
          transform: "translateY(-40px)",
        }}
      >
        <Box
          onClick={handleBackClick}
          className={styles.backContainer}
          sx={{ transform: "translateY(-20px) translateX(-290px)" }}
        >
          <ArrowBackIcon />
          <BackButton>Back</BackButton>
        </Box>
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
          }}
        >
          <Avatar
            alt="Company Logo"
            src={logo}
            sx={{
              width: 88,
              height: 88,
            }}
          />
          <Typography
            variant="body1"
            sx={{
              color: "#000",
              fontFamily: "Helvetica Neue",
              fontSize: "30px",
              fontStyle: "normal",
              fontWeight: 400,
              lineHeight: "normal",
            }}
          >
            You are registering as a{" "}
            <span className={highlightClass}>{selectedOption.selected}</span>
          </Typography>
        </Box>
        <IconButton
          sx={{
            color: "#000",
            transform: "translateY(-20px) translateX(290px)",
          }}
          onClick={handleClose}
        >
          <CloseIcon />
        </IconButton>
      </Box>
      <Box
        sx={{ width: "100%", maxWidth: 400, margin: "0 auto", mb: 2, mt: -5 }}
      >
        {selectedType === "Business" && (
          <Stepper activeStep={activeStep} alternativeLabel>
            {businessSteps.map((label, index) => (
              <Step key={label} active={index === 1}>
                <StepLabel>
                  <Typography
                    variant="body1"
                    sx={{
                      fontSize: index === 1 ? "16px" : "14px",
                      fontWeight: index === 1 ? 700 : 400,
                      color: index === 1 ? "#000" : "#A0A0A0",
                    }}
                  >
                    {label}
                  </Typography>
                </StepLabel>
              </Step>
            ))}
          </Stepper>
        )}
        {selectedType === "Non-Profit" && (
          <Stepper activeStep={activeStep} alternativeLabel>
            {nonprofitSteps.map((label, index) => (
              <Step key={label} active={index === 1}>
                <StepLabel>
                  <Typography
                    variant="body1"
                    sx={{
                      fontSize: index === 1 ? "16px" : "14px",
                      fontWeight: index === 1 ? 700 : 400,
                      color: index === 1 ? "#000" : "#A0A0A0",
                    }}
                  >
                    {label}
                  </Typography>
                </StepLabel>
              </Step>
            ))}
          </Stepper>
        )}
      </Box>
      <Box
        sx={{ display: "flex", alignItems: "center", justifyContent: "center" }}
      >
        <Typography
          variant="body1"
          sx={{
            textAlign: "left",
            color: " #A0A0A0",
            fontFamily: "Helvetica Neue",
            fontSize: "22px",
            fontStyle: "normal",
            fontWeight: 400,
            lineHeight: "normal",
            marginBottom: "10px",
            marginLeft: "20px",
          }}
        >
          You can edit your choice in your PROFILE
        </Typography>
      </Box>
      {selectedType === "Business" && (
        <Grid
          container
          spacing={4}
          justifyContent="space-around"
          alignItems="stretch"
        >
          {businessOptions.map((option, index) => (
            <Grid item xs={12} sm={6} md={4} key={index} sx={{ display: "flex" }}>
              <Card 
                className={styles.card}
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  flex: 1,
                  // maxWidth: "550px", //
                  borderRadius: "22px",
                  // border: "1px solid #ccc",
                  border:
                    selected === option.title
                      ? "2px solid #738CF7"
                      : "1px solid #ccc",
                  transition: "border 0.3s",
                  "&:hover": {
                    border: "2px solid #738CF7",
                  },
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography 
                    // className={styles.optionTitle}
                    variant="h2"
                    sx={{
                      color: "#000",
                      fontFamily: "Helvetica Neue",
                      fontSize: "25px",
                      fontStyle: "normal",
                      fontWeight: 500,
                      lineHeight: "normal",
                      marginTop: 2,
                      marginBottom: 3,
                      display: "flex",
                      justifyContent: "center",
                    }}
                  >
                    {option.title}
                  </Typography>
                  <Box
                    component="img"
                    src={option.image}
                    alt={option.title}
                    sx={{
                      width: "90%",
                      height: 270,
                      marginBottom: 2,
                      marginTop: 2,
                    }}
                  />
                  <Typography className={styles.optionDescription}
                    variant="body2"
                    sx={{
                      color: " #A0A0A0",
                      fontFamily: "Helvetica Neue",
                      display: "flex",
                      justifyContent: "center",
                      fontSize: "20px",
                      fontStyle: "normal",
                      fontWeight: 400,
                      lineHeight: "normal",
                      marginBottom: "5px",
                      marginTop: -5,
                    }}
                  >
                    {option.description}
                  </Typography>
                </CardContent>
                <CardActions sx={{ justifyContent: "center" }}>
                  <Button
                    className={styles.nextButton}
                    fullWidth
                    variant="contained"
                    sx={{
                      width: isSmallScreen ? "90%" : "350px",
                      height: isSmallScreen ? "50px" : "60px",
                      fontSize: isSmallScreen ? "18px" : isMediumScreen ? "22px" : "25px",
                      fontWeight: 600,
                      borderRadius: "56px",
                      textTransform: "none",
                      background: "linear-gradient(to right, #6271AE, #9ACDDA)",
                      opacity: 0.4,
                      color: "var(--barcolor, #FFF)",
                      marginBottom: 3,
                      "&:hover": {
                        opacity: 1,
                      },
                    }}
                    onClick={() => handleNext(option.size)}
                  >
                    Next
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
      {selectedType === "Non-Profit" && (
        <Grid
        container
        spacing={4}
        justifyContent="space-around"
        alignItems="stretch"
        >
          {nonprofitOptions.map((option, index) => (
            <Grid item xs={12} sm={6} md={4} key={index} sx={{ display: "flex" }}>
              <Card 
                className={styles.card}
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  flex: 1,
                  // maxWidth: "450px", // 
                  borderRadius: "22px",
                  // border: "1px solid #ccc",
                  border:
                    selected === option.title
                      ? "2px solid #738CF7"
                      : "1px solid #ccc",
                  transition: "border 0.3s",
                  "&:hover": {
                    border: "2px solid #738CF7",
                  },
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography 
                    // className={styles.optionTitle}
                    variant="h2"
                    sx={{
                      color: "#000",
                      fontFamily: "Helvetica Neue",
                      fontSize: "25px",
                      fontStyle: "normal",
                      fontWeight: 500,
                      lineHeight: "normal",
                      marginTop: 2,
                      marginBottom: 2,
                      display: "flex",
                      justifyContent: "center",
                    }}
                  >
                    {option.title}
                  </Typography>
                  <Box
                    component="img"
                    src={option.image}
                    alt={option.title}
                    sx={{
                      width: "80%",
                      height: 250,
                      marginBottom: 2,
                      marginTop: 2,
                    }}
                  />
                  <Typography className={styles.optionDescription}
                    variant="body2"
                    sx={{
                      color: " #A0A0A0",
                      fontFamily: "Helvetica Neue",
                      display: "flex",
                      justifyContent: "center",
                      fontSize: "20px",
                      fontStyle: "normal",
                      fontWeight: 400,
                      lineHeight: "normal",
                      marginBottom: "5px",
                      marginTop: -2,
                    }}
                  >
                    {option.description}
                  </Typography>
                </CardContent>
                <CardActions sx={{ justifyContent: "center" }}>
                  <Button
                    className={styles.nextButton}
                    fullWidth
                    variant="contained"
                    sx={{
                      width: isSmallScreen ? "90%" : "350px",
                      height: isSmallScreen ? "50px" : "60px",
                      fontSize: isSmallScreen ? "18px" : isMediumScreen ? "22px" : "25px",
                      fontWeight: 600,
                      borderRadius: "56px",
                      textTransform: "none",
                      background: "linear-gradient(to right, #6271AE, #9ACDDA)",
                      opacity: 0.4,
                      color: "var(--barcolor, #FFF)",
                      marginBottom: 3,
                      "&:hover": {
                        opacity: 1,
                      },
                    }}
                    onClick={() => handleNext(option.size)}
                  >
                    Next
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default SizeOptionSelection;
