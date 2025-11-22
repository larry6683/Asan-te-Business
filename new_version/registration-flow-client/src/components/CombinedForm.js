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
} from "@mui/material";
import styles from "./CombinedForm.module.css";
import logo from "../assets/TE-Logo.svg";
import { ReactComponent as ArrowBackIcon } from "../assets/ionic-ios-arrow-back.svg";
import CloseIcon from "@mui/icons-material/Close";
import { Stepper, Step, StepLabel } from "@mui/material";
import { US_STATE } from "../types/UsState";
import { useDispatch } from "react-redux";
import { setProfileForm } from "../redux/profileFormSlice";
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
  return user;
};

const RegistrationForm = () => {
  const [activeStep, setActiveStep] = useState(2);
  const [alreadyRegistered, setAlreadyRegistered] = useState(false);
  
  // Backend Error States
  const [nameNotUnique, setNameNotUnique] = useState(false);
  const [emailNotUnique, setEmailNotUnique] = useState(false);
  const [unhandledError, setUnhandledError] = useState(false);
  const [errorMessage, setErrorMessage] = useState(""); 

  const [entityType, setEntityType] = useState("Business");

  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
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
  
  // Client-side validity
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
      registerAndNavigate();
    }
  };

  const registerAndNavigate = () => {
    const userFromStorage = getUserFromStorage();
    const size = sessionStorage.getItem("asante:selectedSize", "");
    const causesString = sessionStorage.getItem("asante:selectedCauses") || "[]";
    const causes = JSON.parse(causesString);

    const registrationDto = EntityRegistrationDtoFactory.createOrganizationRegistrationDto(
        entityType,
        userFromStorage,
        size,
        causes,
        formData,
    );

    console.log('Sending registration data:', registrationDto);
    
    const registrationApiService = new RegistrationApiService();
    
    // Reset error states before request
    setNameNotUnique(false);
    setEmailNotUnique(false);
    setAlreadyRegistered(false);
    setUnhandledError(false);
    setErrorMessage("");

    if (entityType === "Business" || entityType === "business") {
      registrationApiService.registerBusiness(registrationDto, handleSuccess, handleError);
    } else if (entityType === "Non-Profit" || entityType === "nonprofit") {
      registrationApiService.registerBeneficiary(registrationDto, handleSuccess, handleError);
    }
  };

  const handleSuccess = (jsonResponse) => {
    console.log('🎉 Registration successful:', jsonResponse);
    const entityKey = entityType === "Business" ? "business" : "beneficiary";
    const entityId = jsonResponse.data.id;
    
    sessionStorage.setItem(`asante:${entityKey}Id`, entityId);
    
    const user = getUserFromStorage();
    CookieFactory.createAppCookieFromDataOrStorage(
      user,
      { entityType: entityKey, entityId: entityId }
    );
    
    console.log('✅ Registration complete - navigating to /home');
    navigate('/home');
  };

  // ✅ FIXED: Improved Error Parsing logic to use 'detail'
  const handleError = (error) => {
    console.error("Registration Error Raw:", error);
    try {
      let errorData = error;
      
      // Handle case where error is a stringified JSON (common in some gRPC-web setups)
      if (typeof error.message === 'string' && error.message.startsWith('{')) {
          try {
            errorData = JSON.parse(error.message);
          } catch (e) {
            console.warn("Could not parse error message JSON");
          }
      }

      // Extract the specific error object
      // The backend sends `errors` list in the response
      const errorsList = errorData.errors || [];
      const mainError = errorsList.length > 0 ? errorsList[0] : errorData;
      
      // Code 3 = ERROR_ALREADY_EXISTS (from error.proto)
      if (mainError.code === 3) {
         // The 'detail' field usually contains "Business with email 'x' already exists"
         // The 'message' field usually contains just "Business already exists"
         const detailText = mainError.detail || "";
         const messageText = mainError.message || "";
         
         const combinedText = (detailText + " " + messageText).toLowerCase();
         
         // Set specific flags based on content
         if (combinedText.includes("email")) {
             setEmailNotUnique(true);
             setErrorMessage(detailText || "This email is already associated with an account.");
         } else if (combinedText.includes("name")) {
             setNameNotUnique(true);
             setErrorMessage(detailText || "This name is already registered.");
         } else {
             setAlreadyRegistered(true);
             setErrorMessage(detailText || "This entity is already registered.");
         }
      } else {
        // Handle other errors
        setUnhandledError(true);
        setErrorMessage(mainError.detail || mainError.message || "An unexpected error occurred.");
      }
    } catch (parseError) {
      console.error("Error parsing failure:", parseError);
      setUnhandledError(true);
      setErrorMessage("Registration failed due to a network or server error.");
    }
  };

  const formIsValid = () => {
    const email = formData["email"];
    let emailValid = email.length > 7 && email.includes("@") && email.includes(".");

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

    for (const key in newValidationState) {
      if (!newValidationState[key]) {
        return false;
      }
    }
    return true;
  };

  const handleChange = (prop) => (event) => {
    setFormData({ ...formData, [prop]: event.target.value });
    
    // Reset client-side validation error
    if (prop === "locationCity" || prop === "locationState") {
      if (!formValidity["locationCity"] || !formValidity["locationState"]) {
        setFormValidity({ ...formValidity, ["locationCity"]: true, ["locationState"]: true });
      }
    } else if (!formValidity[prop]) {
      setFormValidity({ ...formValidity, [prop]: true });
    }

    // Reset backend error flags immediately when user starts typing to fix it
    if (prop === "name") setNameNotUnique(false);
    if (prop === "email") setEmailNotUnique(false);
    setAlreadyRegistered(false);
    setUnhandledError(false);
  };

  const handleBackClick = () => {
    dispatch(setProfileForm({ selected: formData }));
    navigate(`/register/sizeoptionselection`);
  };

  const handleClose = () => {
    const navigateToLogin = () => setTimeout(() => { navigate(`/`); }, 300);
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
      {/* Header Section */}
      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "16px", transform: "translateY(-40px)" }}>
        <Box onClick={handleBackClick} className={styles.backContainer} sx={{ transform: "translateY(-25px) translateX(-25px)" }}>
          <ArrowBackIcon />
          <BackButton>Back</BackButton>
        </Box>
        <Box sx={{ display: "flex", alignItems: "center" }}>
          <Avatar alt="Company Logo" src={logo} sx={{ width: 88, height: 88 }} />
          <Typography variant="body1" sx={{ color: "#000", fontFamily: "Helvetica Neue", fontSize: "30px", fontWeight: 400 }}>
            You are registering as a <span className={highlightClass}>{entityType === "Business" ? "Business" : "Non-Profit"}</span>
          </Typography>
        </Box>
        <IconButton sx={{ color: "#000", transform: "translateY(-30px) translateX(35px)" }} onClick={handleClose}>
          <CloseIcon />
        </IconButton>
      </Box>

      <Box sx={{ width: "100%", maxWidth: 400, margin: "0 auto", mb: 2, mt: -5 }}>
        <Stepper activeStep={activeStep} alternativeLabel>
          {steps.map((label, index) => (
            <Step key={label} active={index === 2}>
              <StepLabel>
                <Typography variant="body1" sx={{ fontSize: index === 2 ? "16px" : "14px", fontWeight: index === 2 ? 700 : 400, color: index === 2 ? "#000" : "#A0A0A0" }}>
                  {label}
                </Typography>
              </StepLabel>
            </Step>
          ))}
        </Stepper>
      </Box>

      <Box sx={{ display: "flex", alignItems: "center", justifyContent: "center" }} mb={4} mt={4}>
        <Typography variant="body1" sx={{ color: "#4E4E4E", fontFamily: "Helvetica Neue", fontSize: "22px", fontWeight: 400, opacity: 0.57 }}>
          You can edit this information in your PROFILE
        </Typography>
      </Box>

      {/* Global Error Message Display (for unhandled errors) */}
      {unhandledError && (
        <Box sx={{ textAlign: "center", mb: 2 }}>
            <Typography sx={{ color: "#FF5151", fontSize: "18px", fontWeight: 500 }}>
                {errorMessage}
            </Typography>
        </Box>
      )}
      {alreadyRegistered && (
        <Box sx={{ textAlign: "center", mb: 2 }}>
            <Typography sx={{ color: "#FF5151", fontSize: "18px", fontWeight: 500 }}>
                {errorMessage || "This entity is already registered."}
            </Typography>
        </Box>
      )}

      <Grid container spacing={2}>
        <Grid item xs={12} md={6} sx={{ transform: "translateX(175px)" }}>
          
          {/* NAME FIELD */}
          <Box width="70%" mb={2}>
            <Typography variant="body1" sx={{ color: "#000", fontFamily: "Helvetica Neue", fontSize: "23px", fontWeight: 400 }}>
              <span>{entityType === "Business" ? "Business Name *" : "Non-Profit Name *"}</span>
              
              {!formValidity.name && (
                  <span style={{ color: "#FF5151", display: "block", fontSize: "16px", marginTop: "5px" }}>
                      Name is required (min 3 chars).
                  </span>
              )}
              {/* ✅ SPECIFIC DB ERROR FOR NAME */}
              {nameNotUnique && (
                  <span style={{ color: "#FF5151", display: "block", fontSize: "16px", marginTop: "5px" }}>
                      {errorMessage || "This name is already registered."}
                  </span>
              )}
            </Typography>
            <TextField
              variant="outlined"
              required
              fullWidth
              id="name"
              placeholder={`Enter ${entityType} name`}
              name="name"
              value={formData.name}
              onChange={handleChange("name")}
              error={!formValidity.name || nameNotUnique}
              sx={{ width: "100%", height: "49px", borderRadius: "9px", marginTop: "10px", marginBottom: "20px" }}
              InputProps={{ style: { borderRadius: "9px" }, classes: { input: styles.customPlaceholder } }}
            />
          </Box>

          {/* EMAIL FIELD */}
          <Box width="70%" mb={2}>
            <Typography variant="body1" sx={{ color: "#000", fontFamily: "Helvetica Neue", fontSize: "23px", fontWeight: 400 }}>
              <span>{entityType === "Business" ? "Business Email *" : "Non-Profit Email *"}</span>
              
              {!formValidity.email && (
                  <span style={{ color: "#FF5151", display: "block", fontSize: "16px", marginTop: "5px" }}>
                      Valid email is required.
                  </span>
              )}
              {/* ✅ SPECIFIC DB ERROR FOR EMAIL */}
              {emailNotUnique && (
                  <span style={{ color: "#FF5151", display: "block", fontSize: "16px", marginTop: "5px" }}>
                      {errorMessage || "This email is already in use."}
                  </span>
              )}
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="email"
              placeholder={`Enter ${entityType} email`}
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange("email")}
              error={!formValidity.email || emailNotUnique}
              sx={{ width: "100%", height: "49px", borderRadius: "9px", marginTop: "10px", marginBottom: "20px" }}
              InputProps={{ style: { borderRadius: "9px" }, classes: { input: styles.customPlaceholder } }}
            />
          </Box>

          {/* Website (Optional) */}
          <Box width="70%" mb={2}>
            <Typography variant="body1" sx={{ color: "#000", fontFamily: "Helvetica Neue", fontSize: "23px", fontWeight: 400 }}>
              <span>{entityType === "Business" ? "Business Website " : "Non-Profit Website "}</span>
              <span style={{ fontSize: "21px", fontWeight: 380, color: "#000", opacity: 0.59 }}>(optional for now)</span>
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              fullWidth
              id="website"
              placeholder="Enter website link"
              name="website"
              value={formData.website}
              onChange={handleChange("website")}
              sx={{ width: "100%", height: "49px", borderRadius: "9px", marginTop: "10px", marginBottom: "20px" }}
              InputProps={{ style: { borderRadius: "9px" }, classes: { input: styles.customPlaceholder } }}
            />
          </Box>

          {/* Phone (Optional) */}
          <Box width="70%" mb={2}>
            <Typography variant="body1" sx={{ color: "#000", fontFamily: "Helvetica Neue", fontSize: "23px", fontWeight: 400 }}>
              Phone number <span style={{ fontSize: "21px", color: "#000", fontWeight: 380, opacity: 0.59 }}>(optional for now)</span>
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              fullWidth
              type="number"
              id="phoneNumber"
              placeholder="Enter phone number"
              name="phoneNumber"
              value={formData.phoneNumber}
              onChange={handleChange("phoneNumber")}
              sx={{ height: "49px", borderRadius: "9px", marginTop: "10px" }}
              InputProps={{ style: { borderRadius: "9px" }, classes: { input: styles.customPlaceholder } }}
            />
          </Box>
        </Grid>

        <Grid item xs={12} md={6}>
          {/* Location */}
          <Box width="93%" mb={2}>
            <Typography variant="body1" sx={{ color: "#000", fontFamily: "Helvetica Neue", fontSize: "23px", fontWeight: 400 }}>
              <span>{entityType === "Business" ? "Business Location *" : "Non-Profit Location *"}</span>
              {!(formValidity.locationCity && formValidity.locationState) && (
                  <span style={{ color: "#FF5151", display: "block", fontSize: "16px", marginTop: "5px" }}>
                      City and State are required.
                  </span>
              )}
            </Typography>
            <Box width="75%" sx={{ display: "flex", gap: 2.2, marginTop: "5px" }}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="city-location"
                placeholder="Enter city"
                name="location-city"
                value={formData.locationCity}
                onChange={handleChange("locationCity")}
                error={!formValidity.locationCity}
                sx={{ color: "#D6D6D6", fontFamily: "Helvetica Neue", fontSize: "22px", fontWeight: 400 }}
                InputProps={{ style: { borderRadius: "9px" }, classes: { input: styles.customPlaceholder } }}
              />
              <Box width="40%" mb={2}>
                <FormControl fullWidth variant="outlined" error={!formValidity.locationState}>
                  <InputLabel id="city-select-label" sx={{ color: "#303030", fontSize: "22px" }}>State</InputLabel>
                  <Select
                    value={formData.locationState}
                    onChange={handleChange("locationState")}
                    label="State"
                    sx={{ height: "55px", borderRadius: "9px", backgroundColor: "#fff" }}
                    MenuProps={{ PaperProps: { sx: { borderRadius: "9px", maxHeight: "330px" } } }}
                  >
                    {Object.entries(US_STATE).map(([key, value]) => (
                      <MenuItem key={key} value={value}>{value}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Box>
            </Box>
          </Box>

          {/* Social Media */}
          <Box width="70%" mb={2}>
            <Typography variant="body1" sx={{ color: "#000", fontFamily: "Helvetica Neue", fontSize: "23px", fontWeight: 400 }}>
              Add Social Media <span style={{ fontSize: "21px", fontWeight: 380, color: "#000", opacity: 0.59 }}>(optional for now)</span>
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              fullWidth
              placeholder="Enter Linkedln/Instagram link"
              value={formData.socialMedia}
              onChange={handleChange("socialMedia")}
              sx={{ height: "49px", borderRadius: "9px", marginTop: "10px", marginBottom: "20px" }}
              InputProps={{ style: { borderRadius: "9px" }, classes: { input: styles.customPlaceholder } }}
            />
          </Box>

          {/* Shop URL */}
          <Box width="70%" mb={2}>
            <Typography variant="body1" sx={{ color: "#000", fontFamily: "Helvetica Neue", fontSize: "23px", fontWeight: 400 }}>
              Shop URL <span style={{ fontSize: "21px", fontWeight: 380, color: "#000", opacity: 0.59 }}>(optional for now)</span>
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              fullWidth
              id="shopUrl"
              placeholder="Enter link to your store"
              name="shopUrl"
              value={formData.shopUrl}
              onChange={handleChange("shopUrl")}
              sx={{ width: "100%", height: "49px", borderRadius: "9px", marginTop: "10px", marginBottom: "20px" }}
              InputProps={{ style: { borderRadius: "9px" }, classes: { input: styles.customPlaceholder } }}
            />
          </Box>

          {/* Team Member Invite */}
          <Box width="70%" mb={2}>
            <Typography variant="body1" sx={{ color: "#000", fontFamily: "Helvetica Neue", fontSize: "23px", fontWeight: 400 }}>
              Invite Team Member? Email:
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              fullWidth
              placeholder="Enter team member email"
              value={formData.teamMemberEmail}
              onChange={handleChange("teamMemberEmail")}
              sx={{ height: "49px", borderRadius: "9px", marginTop: "10px", marginBottom: "20px" }}
              InputProps={{ style: { borderRadius: "9px" }, classes: { input: styles.customPlaceholder } }}
            />
          </Box>
        </Grid>
      </Grid>

      <Box sx={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
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