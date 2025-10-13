import React, { useState, useEffect } from "react";
import {
  Box,
  Card,
  CardContent,
  CardActions,
  Button,
  Typography,
  Grid,
  Avatar,
  IconButton,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import styles from "./RegsiteringAsComponent.module.css";
import logo from "../assets/TE-Logo.svg";
import BusinessImage from "../assets/business.png";
import ConsumerImage from "../assets/consumer.png";
import NonprofitImage from "../assets/nonprofit.png";
import { useNavigate } from "react-router-dom";
import { CSSTransition } from "react-transition-group";
import { useDispatch } from "react-redux";
import { setSelectedOption } from "../redux/selectedOptionSlice";
import { logoutCurrentUser } from "../user-auth/logoutUser";
import { redirectUrls } from "../web-data/redirectUrls";

const options = [
  {
    title: "Business",
    description: "Build customer loyalty with rewards that make a difference.",
    image: BusinessImage,
  },
  {
    title: "Consumer",
    description:
      "Use your rewards to empower your favorite businesses and causes.",
    image: ConsumerImage,
  },
  {
    title: "Non-Profit",
    description: "Show gratitude to your donors.",
    image: NonprofitImage,
  },
];

const RegisteringAsComponent = () => {
  const [selected, setSelected] = useState("");
  const [isVisible, setIsVisible] = useState(true);
  const [navigateFlag, setNavigateFlag] = useState(false);
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));
  const isMediumScreen = useMediaQuery(theme.breakpoints.down("md"));

  const handleSelect = (option) => {
    setSelected(option.title);
    dispatch(
      setSelectedOption({ selected: option.title, image: option.image }),
    );
    setNavigateFlag(true);
  };

  useEffect(() => {
    if (navigateFlag) {
      navigate(`/register/signup`);
    }
  }, [navigateFlag, navigate]);

  const handleClose = () => {
    const navigateToLogin = () =>
      setTimeout(() => {
        navigate(`/`);
      }, 300);
    logoutCurrentUser(navigateToLogin, navigateToLogin);
  };

  return (
    <CSSTransition
      in={isVisible}
      timeout={300}
      classNames={{
        enterActive: styles.enterActive,
        exitActive: styles.exitActive,
      }}
      unmountOnExit
    >
      <Box className={styles.container}>
        <IconButton
          sx={{
            position: "absolute",
            top: 8,
            right: 8,
            color: "#000",
          }}
          onClick={handleClose}
        >
          <CloseIcon />
        </IconButton>
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            mb: 2,
            flexDirection: isSmallScreen ? "column" : "row",
          }}
        >
          <Avatar
            alt="Company Logo"
            src={logo}
            sx={{
              width: isSmallScreen ? 80 : 109,
              height: isSmallScreen ? 80 : 109,
              mb: isSmallScreen ? 2 : 0,
            }}
          />
          <Typography
            variant="body1"
            sx={{
              color: "#000",
              fontFamily: "Helvetica Neue",
              fontSize: isSmallScreen ? "24px" : "30px",
              fontStyle: "normal",
              fontWeight: 700,
              lineHeight: "normal",
              ml: isSmallScreen ? 0 : 2,
            }}
          >
            Registering as
          </Typography>
        </Box>
        <Grid
          container
          spacing={2}
          justifyContent="space-around"
          alignItems="stretch"
        >
          {options.map((option, index) => (
            <Grid item xs={12} sm={6} md={4} key={index} sx={{ display: "flex" }}>
              <Card
                className={styles.card}
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  flex: 1,
                  borderRadius: "22px",
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
                  <Box
                    component="img"
                    src={option.image}
                    alt={option.title}
                    // className={styles.cardImage}
                    sx={{
                      width: "80%",
                      height: 250,
                      marginBottom: 4,
                      marginTop: 6,
                    }}
                  />
                  <Typography
                    variant="h2"
                    gutterBottom
                    sx={{
                      color: "#000",
                      fontFamily: "Helvetica Neue",
                      fontSize: isSmallScreen ? "22px" : isMediumScreen ? "24px" : "28px",
                      fontStyle: "normal",
                      fontWeight: 700,
                      lineHeight: "normal",
                      marginBottom: 3,
                    }}
                  >
                    {option.title}
                  </Typography>
                  <Typography
                    variant="body2"
                    sx={{
                      color: " #A0A0A0",
                      fontFamily: "Helvetica Neue",
                      fontSize: isSmallScreen ? "16px" : isMediumScreen ? "18px" : "20px",
                      fontStyle: "normal",
                      fontWeight: 400,
                      lineHeight: "normal",
                      marginBottom: 2,
                    }}
                  >
                    {option.description}
                  </Typography>
                </CardContent>
                <CardActions sx={{ justifyContent: "center" }}>
                  <Button
                    fullWidth
                    variant="contained"
                    className={styles.selectButton}
                    sx={{
                      width: isSmallScreen ? "90%" : "350px",
                      height: isSmallScreen ? "50px" : "60px",
                      fontSize: isSmallScreen ? "18px" : isMediumScreen ? "22px" : "25px",
                      fontWeight: 600,
                      borderRadius: "56px",
                      textTransform: "none",
                      background: "linear-gradient(to right, #6271AE, #9ACDDA)",
                      opacity: selected === option.title ? 1 : 0.4,
                      color: "var(--barcolor, #FFF)",
                      marginBottom: 3,
                      "&:hover": {
                        opacity: 1,
                      },
                    }}
                    disabled={option.title !== "Business" && option.title !== "Non-Profit"}
                    onClick={() => handleSelect(option)}
                  >
                    Select
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </CSSTransition>
  );
};

export default RegisteringAsComponent;