import React, { useState } from "react";
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
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import styles from "./NonprofitRegistrationForm.module.css";
import logo from "../assets/TE-Logo.svg";
import { ReactComponent as ArrowBackIcon } from "../assets/ionic-ios-arrow-back.svg";
import CloseIcon from "@mui/icons-material/Close";
import { Stepper, Step, StepLabel } from "@mui/material";
import { ReactComponent as InfoCircle } from "../assets/Icon_awesome-info-circle.svg";
import { US_STATE } from "../types/UsState";
import { useDispatch } from "react-redux";
import { setBeneficiaryProfileForm } from "../redux/beneficiaryProfileFormSlice";
import { clearStore } from "../redux/store";
import { logoutCurrentUser } from "../user-auth/logoutUser";
import { EntityRegistrationDtoFactory } from "../api/models/EntityRegistrationDtoFactory";
import { RegistrationApiService } from "../api/registrationApiService";

const CustomIconButton = styled(IconButton)({
  margin: "0 10px",
});

const getFormDataFromStorage = () => {
  let beneficiaryProfileForm = JSON.parse(
    sessionStorage.getItem("asante:beneficiaryProfileForm"),
  );
  return beneficiaryProfileForm;
};

const NonProfitRegistrationForm = () => {
  const [formData, setFormData] = useState(
    getFormDataFromStorage() || {
      beneficiaryName: "",
      email: "",
      website: "",
      phoneNumber: "",
      locationCity: "",
      locationState: "",
      shopUrl: "",
      socialMedia: "",
      ein: "",
      teamMemberEmail: "",
    },
  );

  const [state, setState] = useState("");

  const [activeStep, setActiveStep] = useState(0);

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleNext = () => {
    // save just in case..?
    dispatch(setBeneficiaryProfileForm({ selected: formData }));
    // double check validation?
    // if valid:
    let valid = true;
    // check each field from formData
    // determine if valid
    // highlight red if not vali

    // check validation for each field
    // 1. required fields
    // 2. ein is a number of length 10
    if (valid) {
      // clearStore(false);
      const success = true; // register();
      if (success) navigate(`/register/welcome`);
    } else {
      // highlight invalid fields
    }
  };

  const register = () => {
    // collect registration data from session storage
    // let userId = sessionStorage.get("userId")
    const userId = "c6aaceba-2300-481a-a5fe-7b547ec5a131";
    const size = sessionStorage.getItem("asante:selectedSize", "");
    // entityType = sessionStorage.getItem("asante:selectedOption")
    const causes = sessionStorage
      .getItem("asante:selectedCauses", [])
      .split(",");
    const profileForm = getFormDataFromStorage();
    const beneficiaryRegistrationDto =
      EntityRegistrationDtoFactory.createOrganizationRegistrationDto(
        "beneficiary",
        userId,
        size,
        causes,
        profileForm,
      );
    let success = false;
    const registrationApiClient = new RegistrationApiService();
    registrationApiClient.registerBusiness(beneficiaryRegistrationDto);
    return success;
  };

  const handleChange = (prop) => (event) => {
    setFormData({ ...formData, [prop]: event.target.value });
  };

  const handleBackClick = () => {
    dispatch(setBeneficiaryProfileForm({ selected: formData }));
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

  const highlightClass = styles["highlight-non-profit"];

  const nonprofitSteps = ["Mission", "Size", "Basics"];

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
            <span className={highlightClass}>Non-profit</span>
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
      <Box sx={{ width: "100%", maxWidth: 400, margin: "0 auto", mt: -7 }}>
        <Stepper activeStep={activeStep} alternativeLabel>
          {nonprofitSteps.map((label, index) => (
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
          <Box width="70%">
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
              Nonprofit Name *
            </Typography>
            <TextField
              variant="outlined"
              required
              fullWidth
              id="beneficiaryName"
              placeholder="Enter the name of your nonprofit here"
              name="beneficiaryName"
              autoComplete="nonprofit-Name"
              value={formData.beneficiaryName}
              onChange={handleChange("beneficiaryName")}
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
                },
                classes: {
                  input: styles.customPlaceholder,
                },
              }}
            />
          </Box>
          <Box width="70%" mb={1}>
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
              Nonprofit Email *
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="email"
              placeholder="Enter your nonprofit email here"
              name="email"
              autoComplete="email"
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
          <Box width="70%" mb={1}>
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
              Nonprofit Website{" "}
              <span style={{ fontSize: "22px", color: "#000", opacity: 0.59 }}>
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
              autoComplete="business-website"
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
              <span style={{ fontSize: "22px", color: "#000", opacity: 0.59 }}>
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
              Non profit Location*{" "}
              <span>
                <Tooltip title="Information about non-profit location">
                  <IconButton size="small">
                    <InfoCircle></InfoCircle>
                  </IconButton>
                </Tooltip>
              </span>
            </Typography>
            <Box
              width="100%"
              sx={{ display: "flex", gap: 2, marginTop: "5px" }}
            >
              <TextField
                variant="outlined"
                required
                fullwWidth
                id="city-location"
                placeholer="Enter city of where your nonprofit is located"
                name="location-city"
                value={formData.locationCity}
                placeholder="City"
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
                  },
                  classes: {
                    input: styles.customPlaceholder,
                  },
                }}
              />
              <Box width="30%" mb={2}>
                <FormControl fullWidth variant="outlined">
                  <InputLabel
                    id="state-select-label"
                    sx={{
                      color: "#D6D6D6",
                      fontFamily: "Helvetica Neue",
                      fontSize: "22px",
                      fontStyle: "normal",
                      fontWeight: "400",
                      lineHeight: "normal",
                      opacity: 1,
                    }}
                  >
                    State
                  </InputLabel>
                  <Select
                    value={state}
                    onChange={(e) => setState(e.target.value)}
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
                      <MenuItem value={key}>{value}</MenuItem>
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
              <span style={{ fontSize: "22px", color: "#000", opacity: 0.59 }}>
                (optional for now)
              </span>
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              fullWidth
              placeholder="Enter linkedln/instagram and other links"
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
              EIN{" "}
              <span style={{ fontSize: "22px", color: "#000", opacity: 0.59 }}>
                (optional for now)
              </span>
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="ein"
              placeholder="Enter Employee Identification Number here"
              name="ein"
              autoComplete="ein"
              value={formData.ein}
              onChange={handleChange("ein")}
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
              placeholder="Enter email here"
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
        // onClick={handleNext()}
      >
        <Button
          variant="contained"
          sx={{
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

export default NonProfitRegistrationForm;
