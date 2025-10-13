import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  TextField,
  Button,
  FormControl,
  Select,
  MenuItem,
  InputLabel,
  Grid,
  Box,
  Typography,
  IconButton,
  styled,
  Avatar,
  Tooltip,
} from "@mui/material";
import styles from "./CombinedForm.module.css";
import logo from "../assets/TE-Logo.svg";
import { ReactComponent as ArrowBackIcon } from "../assets/ionic-ios-arrow-back.svg";
import CloseIcon from "@mui/icons-material/Close";
import { Stepper, Step, StepLabel } from "@mui/material";
import { US_STATE } from "../types/UsState";
import { useDispatch, useSelector } from "react-redux";
import { setProfileForm } from "../redux/profileFormSlice";
import { clearStore } from "../redux/store";
import { logoutCurrentUser } from "../user-auth/logoutUser";
import { EntityRegistrationDtoFactory } from "../api/models/EntityRegistrationDtoFactory";
import { RegistrationApiService } from "../api/registrationApiService";
import { CookieFactory } from "../cookies/cookieFactory";

const getFormDataFromStorage = () => {
  let profileForm = JSON.parse(
    sessionStorage.getItem("asante:profileForm"),
  );
  return profileForm;
};

const getUserFromStorage = () => {
  const json = sessionStorage.getItem("asante:user", "");
  const user = json
    ? JSON.parse(json)
    : {
        id: "",
        email: "",
        userType: "",
      };
  // console.log("user from storage: ", user);
  return user;
};

const RegistrationForm = () => {
  const [activeStep, setActiveStep] = useState(2);
  const [alreadyRegistered, setAlreadyRegistered] = useState(false);
  // for apiErrors
  const [nameNotUnique, setNameNotUnique] = useState(false);
  const [emailNotUnique, setEmailNotUnique] = useState(false);
  const [unhandledError, setUnhandledError] = useState(false);
  const [entityType, setEntityType] = useState("Business"); // or "Non-Profit"

  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    // Get entity type from storage
    const storedType = sessionStorage.getItem("asante:selectedOption"); 
    if (storedType) {
      setEntityType(storedType);
    }
  }, []);

  const loadForm = () => {
    let form = getFormDataFromStorage();
    if (!form) {
      form = {
        name: "",
        email: "",
        website: "",
        phoneNumber: "",
        locationCity: "",
        locationState: "",
        socialMedia: "",
        shopUrl: "", 
        teamMemberEmail: "",
      };
    }
    return form;
  };

  const [formData, setFormData] = useState(loadForm());
  const [formValidity, setFormValidity] = useState({
    name: true,
    email: true,
    website: true,
    phoneNumber: true,
    locationCity: true,
    locationState: true,
    socialMedia: true,
    shopUrl: true,
    teamMemberEmail: true,
  });

  const handleNext = () => {
    if (formIsValid()) {
      // clearStore(false);
      registerAndNavigate();
    } // else {
    //   highlight invalid fields
    // }
  };

  const registerAndNavigate = () => {
    // collect registration data from session storage
    // let userId = sessionStorage.get("userId")
    const userFromStorage = getUserFromStorage();
    const size = sessionStorage.getItem("asante:selectedSize", "");
    // entityType = sessionStorage.getItem("asante:selectedOption")
    const causes = sessionStorage
      .getItem("asante:selectedCauses", "")
      .split(",");

    const registrationDto = EntityRegistrationDtoFactory.createOrganizationRegistrationDto(
        entityType,
        userFromStorage.id,
        size,
        causes,
        formData,
    );
    // console.log(businessRegistrationDto);
    const registrationApiClient = new RegistrationApiService();
    const registerPromise = entityType === "business" 
      ? registrationApiClient.registerBusiness(registrationDto, handleSuccess, handleError)
      : registrationApiClient.registerNonProfit(registrationDto, handleSuccess, handleError);
  };

  const handleSuccess = (jsonResponse) => {
    sessionStorage.setItem(`asante:${entityType}Id`, jsonResponse[entityType].id);
    CookieFactory.createAppCookieFromDataOrStorage();
    navigate(`/register/welcome`);
  };

  const handleError = (error) => {
    try {
      const errorJson = JSON.parse(error.message);
      setUnhandledError(false);
      if (errorJson.errors) {
        errorJson.errors.forEach((value) => {
          if (value.errorCode === 102) {
            setAlreadyRegistered(true);
          } else if (value.errorCode === 108) {
            setEmailNotUnique(true);
          } else if (value.errorCode === 105) {
            setNameNotUnique(true);
          } else {
            setUnhandledError(true);
          }
        });
      } else if (errorJson.message === "Unauthorized") {
        navigate(`/`);
      } else {
        setUnhandledError(true);
      }
    } catch (error) {
      setUnhandledError(true);
    }
  };

  const formIsValid = () => {
    // iterate over formValidity values and set validity to false if invalid
    const email = formData["email"];
    let emailValid = email.length > 7 && email.includes("@") && email.includes(".");
    // let emailValid = false;
    // // idk why i have to do this but /shrug
    // // email > 7  && email.includes('@') && email.includes('.') does not work ???
    // if (email.length > 7) {
    //   if (email.includes("@")) {
    //     if (email.includes(".")) {
    //       emailValid = true;
    //     }
    //   }
    // }

    const newValidationState = {
      ["name"]: formData["name"].length > 2,
      ["locationCity"]: formData["locationCity"].length > 2,
      ["locationState"]: formData["locationState"].length === 2,
      ["email"]: emailValid,
    };

    setFormValidity({
      ...formValidity,
      ...newValidationState,
    });

    // return Object.values(newValidationState).every(Boolean);
    for (const key in newValidationState) {
      if (!newValidationState[key]) {
        return false;
      }
    }
    return true;
  };

  const handleChange = (prop) => (event) => {
    setFormData({ ...formData, [prop]: event.target.value });
    if (prop === "locationCity" || prop === "locationState") {
      if (!formValidity["locationCity"] || !formValidity["locationState"]) {
        const newState = {
          ["locationCity"]: true,
          ["locationState"]: true,
        };
        setFormValidity({ ...formValidity, ...newState });
      }
    } else if (!formValidity[prop]) {
      setFormValidity({ ...formValidity, [prop]: true });
    }

    if (prop === "name" && nameNotUnique) {
      setNameNotUnique(false);
    } else if (prop === "email" && emailNotUnique) {
      setEmailNotUnique(false);
    } else if (unhandledError) {
      setUnhandledError(false);
    }
  };

  const handleBackClick = () => {
    dispatch(setProfileForm({ selected: formData }));
    navigate(`/register/sizeoptionselection`);
  };

  const handleClose = () => {
    // setIsVisible(false);
    const navigateToLogin = () =>
      setTimeout(() => {
        navigate(`/`);
      }, 300);
    logoutCurrentUser(navigateToLogin, navigateToLogin);
  };

  const BackButton = styled(Typography)({
    color: "#918C8C",
    fontFamily: '"Helvetica Neue", sans-serif',
    fontSize: "25px",
    display: "flex",
    marginLeft: "8px",
    alignItems: "center",
  });


  const highlightClass = entityType === "Business" ? styles["highlight-business"] : styles["highlight-nonprofit"];
  const steps = entityType === "Business" 
    ? ["Causes", "Size", "Basics"]
    : ["Mission", "Size", "Basics"];

  return (
    <Box className={styles.formContainer}>
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
          sx={{ transform: "translateY(-25px) translateX(-25px)" }}
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
            <span className={highlightClass}>
                {entityType === "Business" ? "Business" : "Non-Profit"}
            </span>
          </Typography>
        </Box>
        <IconButton
          sx={{
            color: "#000",
            transform: "translateY(-30px) translateX(35px)",
          }}
          onClick={handleClose}
        >
          <CloseIcon />
        </IconButton>
      </Box>

      <Box
        sx={{ width: "100%", maxWidth: 400, margin: "0 auto", mb: 2, mt: -5 }}
      >
        <Stepper activeStep={activeStep} alternativeLabel>
          {steps.map((label, index) => (
            <Step key={label} active={index === 2}>
              <StepLabel>
                <Typography
                  variant="body1"
                  sx={{
                    fontSize: index === 2 ? "16px" : "14px",
                    fontWeight: index === 2 ? 700 : 400,
                    color: index === 2 ? "#000" : "#A0A0A0",
                  }}
                >
                  {label}
                </Typography>
              </StepLabel>
            </Step>
          ))}
        </Stepper>
      </Box>
      <Box
        sx={{ display: "flex", alignItems: "center", justifyContent: "center" }}
        mb={4}
        mt={4}
      >
        <Typography
          variant="body1"
          sx={{
            color: "#4E4E4E",
            fontFamily: "Helvetica Neue",
            fontSize: "22px",
            fontStyle: "normal",
            fontWeight: 400,
            lineHeight: "normal",
            opacity: 0.57,
          }}
        >
          You can edit this information in your PROFILE
        </Typography>
      </Box>
      <Grid container spacing={2}>
        <Grid item xs={12} md={6} sx={{ transform: "translateX(175px)" }}>
          <Box width="70%" mb={2}>
            <Typography
              variant="body1"
              sx={{
                color: " #000",
                fontFamily: "Helvetica Neue",
                fontSize: "23px",
                fontStyle: "normal",
                fontWeight: 400,
                lineHeight: "normal",
              }}
            >
              <span>{entityType === "Business" ? "Business Name *" : "Non-Profit Name *"}</span>
              <span
                style={{
                  color: "#FF5151",
                  marginTop: "9px",
                  visibility: `${!formValidity.name}`,
                  fontSize: "20px",
                  fontWeight: 380,
                }}
              >
                {formValidity.name ? "" : " Name is required!"}
              </span>
              <span
                style={{
                  color: "#FF5151",
                  marginTop: "9px",
                  visibility: `${alreadyRegistered}`,
                  fontSize: "20px",
                  fontWeight: 380,
                }}
              >
                {alreadyRegistered ? ' You already belong to a ${entityType === "Business" ? "Business" : "Non-Profit"} !' : ""}
              </span>
              <span
                style={{
                  color: "#FF5151",
                  marginTop: "9px",
                  visibility: `${nameNotUnique}`,
                  fontSize: "20px",
                  fontWeight: 380,
                }}
              >
                {nameNotUnique ? ' ${entityType === "Business" ? "Business" : "Non-Profit"} name already in use!' : ""}
              </span>
              <span
                style={{
                  color: "#FF5151",
                  marginTop: "9px",
                  visibility: `${unhandledError}`,
                  fontSize: "20px",
                  fontWeight: 380,
                }}
              >
                {unhandledError ? " Unknown error. Contact Admin." : ""}
              </span>
            </Typography>
            <TextField
              variant="outlined"
              required
              fullWidth
              id="name"
              placeholder={`Enter the name of your ${entityType === "Business" ? "Business" : "Non-Profit"} here`}
              name="name"
              value={formData.name}
              onChange={handleChange("name")}
              sx={{
                width: "100%", // Use 100% width for responsive design
                height: "49px",
                borderRadius: "9px",
                marginTop: "10px",
                marginBottom: "20px",
              }}
              InputProps={{
                style: {
                  borderRadius: "9px",
                  borderColor: `${formValidity.name ? "#000000" : "red"}`, // Add red border if invalid
                },
                classes: {
                  input: styles.customPlaceholder,
                },
              }}
            />
          </Box>
          <Box width="70%" mb={2}>
            <Typography
              variant="body1"
              sx={{
                color: "#000",
                fontFamily: "Helvetica Neue",
                fontSize: "23px",
                fontStyle: "normal",
                fontWeight: 400,
                lineHeight: "normal",
              }}
            >
              <span>{entityType === "Business" ? "Business Email *" : "Non-Profit Email *"}</span>
              <span
                style={{
                  color: "#FF5151",
                  marginTop: "9px",
                  visibility: `${!formValidity.email}`,
                  fontSize: "20px",
                  fontWeight: 380,
                }}
              >
                {formValidity.email ? "" : " Email is required!"}
              </span>
              <span
                style={{
                  color: "#FF5151",
                  marginTop: "9px",
                  visibility: `${emailNotUnique}`,
                  fontSize: "20px",
                  fontWeight: 380,
                }}
              >
                {emailNotUnique ? " Email already in use!" : ""}
              </span>
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="email"
              placeholder={`Enter your ${entityType === "Business" ? "Business" : "Non-Profit"} email here`}
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange("email")}
              sx={{
                width: "100%",
                height: "49px",
                borderRadius: "9px",
                marginTop: "10px",
                marginBottom: "20px",
              }}
              style={{
                color: `${formValidity.email ? "#000000" : "red"}`,
                marginTop: "9px",
                visibility: `${!formValidity.email}`,
              }}
              InputProps={{
                style: {
                  borderRadius: "9px",
                  borderColor: `${formValidity.email ? "#000000" : "red"}`, // Add red border if invalid
                },
                classes: {
                  input: styles.customPlaceholder,
                },
              }}
            />
          </Box>
          <Box width="70%" mb={2}>
            <Typography
              variant="body1"
              sx={{
                color: "#000",
                fontFamily: "Helvetica Neue",
                fontSize: "23px",
                fontStyle: "normal",
                fontWeight: 400,
                lineHeight: "normal",
              }}
            >
              <span>{entityType === "Business" ? "Business Website " : "Non-Profit Website "}</span>
              <span
                style={{
                  fontSize: "21px",
                  fontWeight: 380,
                  color: "#000",
                  opacity: 0.59,
                }}
              >
                (optional for now)
              </span>
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="website"
              placeholder="Enter website link here "
              name="website"
              value={formData.website}
              onChange={handleChange("website")}
              sx={{
                width: "100%",
                height: "49px",
                borderRadius: "9px",
                marginTop: "10px",
                marginBottom: "20px",
              }}
              InputProps={{
                style: {
                  borderRadius: "9px",
                },
                classes: {
                  input: styles.customPlaceholder,
                },
              }}
            />
          </Box>
          <Box width="70%" mb={2}>
            <Typography
              variant="body1"
              sx={{
                color: "#000",
                fontFamily: "Helvetica Neue",
                fontSize: "23px",
                fontStyle: "normal",
                fontWeight: 400,
                lineHeight: "normal",
              }}
            >
              Phone number{" "}
              <span
                style={{
                  fontSize: "21px",
                  color: "#000",
                  fontWeight: 380,
                  opacity: 0.59,
                }}
              >
                (optional for now)
              </span>
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              fullWidth
              type="number"
              id="phoneNumber"
              placeholder="Enter phone number here"
              name="phoneNumber"
              value={formData.phoneNumber}
              onChange={handleChange("phoneNumber")}
              sx={{
                height: "49px",
                borderRadius: "9px",
                marginTop: "10px",
              }}
              InputProps={{
                style: {
                  borderRadius: "9px",
                },
                classes: {
                  input: styles.customPlaceholder,
                },
              }}
            />
          </Box>
        </Grid>
        <Grid item xs={12} md={6}>
          <Box width="93%" mb={2}>
            <Typography
              variant="body1"
              sx={{
                color: "#000",
                fontFamily: "Helvetica Neue",
                fontSize: "23px",
                fontStyle: "normal",
                fontWeight: 400,
                lineHeight: "normal",
              }}
            >
              <span>{entityType === "Business" ? "Business Location *" : "Non-Profit Location *"}</span>
              <span
                style={{
                  color: "#FF5151",
                  marginTop: "9px",
                  visibility: `${!(formValidity.locationCity || formValidity.locationState)}`,
                  fontSize: "20px",
                  fontWeight: 380,
                }}
              >
                {formValidity.locationCity && formValidity.locationState
                  ? ""
                  : " Location is required!"}
              </span>
            </Typography>
            <Box
              width="75%"
              sx={{ display: "flex", gap: 2.2, marginTop: "5px" }}
            >
              <TextField
                variant="outlined"
                required
                fullWidth
                id="city-location"
                placeholder="Enter city here"
                name="location-city"
                value={formData.locationCity}
                onChange={handleChange("locationCity")}
                sx={{
                  color: "#D6D6D6",
                  fontFamily: "Helvetica Neue",
                  fontSize: "22px",
                  fontStyle: "normal",
                  fontWeight: "400",
                  lineHeight: "normal",
                  opacity: 1,
                }}
                InputProps={{
                  style: {
                    borderRadius: "9px",
                    borderColor: `${formValidity.locationCity ? "#000000" : "red"}`, // Add red border if invalid
                  },
                  classes: {
                    input: styles.customPlaceholder,
                  },
                }}
              />
              <Box width="40%" mb={2}>
                <FormControl fullWidth variant="outlined">
                  <InputLabel
                    id="city-select-label"
                    sx={{
                      color: "#303030",
                      fontFamily: "Helvetica Neue",
                      fontSize: "22px",
                      fontStyle: "normal",
                      fontWeight: "500",
                      lineHeight: "normal",
                      opacity: 1,
                      paddingRight: "10px",
                    }}
                  >
                    State
                  </InputLabel>
                  <Select
                    value={formData.locationState}
                    onChange={handleChange("locationState")}
                    label="State"
                    sx={{
                      height: "55px",
                      borderRadius: "9px",
                      backgroundColor: "#fff",
                    }}
                    MenuProps={{
                      PaperProps: {
                        sx: {
                          borderRadius: "9px",
                          maxHeight: "330px",
                        },
                      },
                    }}
                  >
                    {Object.entries(US_STATE).map(([key, value], index) => (
                      <MenuItem key={key} value={value}>
                        {value}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Box>
            </Box>
          </Box>
          <Box width="70%" mb={2}>
            <Typography
              variant="body1"
              sx={{
                color: "#000",
                fontFamily: "Helvetica Neue",
                fontSize: "23px",
                fontStyle: "normal",
                fontWeight: 400,
                lineHeight: "normal",
              }}
            >
              Add Social Media{" "}
              <span
                style={{
                  fontSize: "21px",
                  fontWeight: 380,
                  color: "#000",
                  opacity: 0.59,
                }}
              >
                (optional for now)
              </span>
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              fullWidth
              placeholder="Enter Linkedln/Instagram or other link here"
              value={formData.socialMedia}
              onChange={handleChange("socialMedia")}
              sx={{
                height: "49px",
                borderRadius: "9px",
                marginTop: "10px",
                marginBottom: "20px",
              }}
              InputProps={{
                style: {
                  borderRadius: "9px",
                },
                classes: {
                  input: styles.customPlaceholder,
                },
              }}
            />
          </Box>
          <Box width="70%" mb={2}>
            <Typography
              variant="body1"
              sx={{
                color: "#000",
                fontFamily: "Helvetica Neue",
                fontSize: "23px",
                fontStyle: "normal",
                fontWeight: 400,
                lineHeight: "normal",
              }}
            >
              Shop URL{" "}
              <span
                style={{
                  fontSize: "21px",
                  fontWeight: 380,
                  color: "#000",
                  opacity: 0.59,
                }}
              >
                (optional for now)
              </span>
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="shopUrl"
              placeholder="Enter link to your Shopify store here"
              name="shopUrl"
              value={formData.shopUrl}
              onChange={handleChange("shopUrl")}
              sx={{
                width: "100%",
                height: "49px",
                borderRadius: "9px",
                marginTop: "10px",
                marginBottom: "20px",
              }}
              InputProps={{
                style: {
                  borderRadius: "9px",
                },
                classes: {
                  input: styles.customPlaceholder,
                },
              }}
            />
          </Box>
          <Box width="70%" mb={2}>
            <Typography
              variant="body1"
              sx={{
                color: "#000",
                fontFamily: "Helvetica Neue",
                fontSize: "23px",
                fontStyle: "normal",
                fontWeight: 400,
                lineHeight: "normal",
              }}
            >
              Invite Team Member? Email:
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              fullWidth
              placeholder="Enter team member email here"
              value={formData.teamMemberEmail}
              onChange={handleChange("teamMemberEmail")}
              sx={{
                height: "49px",
                borderRadius: "9px",
                marginTop: "10px",
                marginBottom: "20px",
              }}
              InputProps={{
                style: {
                  borderRadius: "9px",
                },
                classes: {
                  input: styles.customPlaceholder,
                },
              }}
            />
          </Box>
        </Grid>
      </Grid>
      <Box
        sx={{ display: "flex", alignItems: "center", justifyContent: "center" }}
      >
        <Button
          variant="contained"
          sx={{
            marginTop: 2,
            background: "linear-gradient(to right, #6271AE, #9ACDDA)",
            borderRadius: "56px",
            color: "#FFF",
            fontSize: "20px",
            fontWeight: 600,
            width: "287px",
            height: "56px",
            textTransform: "none",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
          onClick={handleNext}
        >
          Access portal
        </Button>
      </Box>
    </Box>
  );
};

export default RegistrationForm;
