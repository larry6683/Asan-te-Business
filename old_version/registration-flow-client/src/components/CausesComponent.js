import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import {
  Box,
  Button,
  Checkbox,
  FormControlLabel,
  Grid,
  Typography,
  IconButton,
  Avatar,
  useMediaQuery,
} from "@mui/material";
import CommunityImage from "../assets/causes2.png";
import SocialImage from "../assets/causes1.png";
import InnovationImage from "../assets/causes4.png";
import EnvironmentImage from "../assets/causes3.png";
import styles from "./CausesComponent.module.css";
import { styled } from "@mui/system";
import FoodIcon from "../assets/food_icon@2x.png";
import DropIcon from "../assets/drop@2x.png";
import MoonIcon from "../assets/moon@2x.png";
import PlusIcon from "../assets/plus.png";
import CloseIcon from "@mui/icons-material/Close";
import logo from "../assets/TE-Logo.svg";
import ToolboxIcon from "../assets/toolbox@2x.png";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { Stepper, Step, StepLabel } from "@mui/material";
import { ReactComponent as ArrowBackIcon } from "../assets/ionic-ios-arrow-back.svg";
import { setSelectedCauses } from "../redux/selectedCausesSlice";
import { logoutCurrentUser } from "../user-auth/logoutUser";
import { setSelectedOption } from "../redux/selectedOptionSlice";
import { clearStore } from "../redux/store";

const getSelectedOptionOrSetIfNotPresent = () => {
  let selectedOption = sessionStorage.getItem("asante:selectedOption") || "";
  if (!selectedOption) {
    selectedOption = "Business";
    sessionStorage.setItem("asante:selectedOption", "Business");
  }
  return selectedOption;
};

const CausesComponent = () => {
  const [selectedCausesLocal, setSelectedCausesLocal] = useState([]);
  const [isEmergencyChecked, setIsEmergencyChecked] = useState(false);
  const [isVisible, setIsVisible] = useState(true);
  const selectedOption = useSelector((state) => state.selectedOption);
  const [selectedType, setSelectedType] = useState("");
  const [activeStep, setActiveStep] = useState(0);
  const [causesSelectedCount, setSelectedCausesCount] = useState(0);

  // New state for Non-Profit flow
  const [selectedPrimaryCause, setSelectedPrimaryCause] = useState(null);
  const [isSelectingPrimary, setIsSelectingPrimary] = useState(true);
  const [selectedSupportingCauses, setSelectedSupportingCauses] = useState([]);

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const isTablet = useMediaQuery('(max-width:1024px)');
  const isMobile = useMediaQuery('(max-width:768px)');

  const isNonProfit = selectedOption.selected === "Non-Profit";

  useEffect(() => {
    const selectedOption = getSelectedOptionOrSetIfNotPresent();
    if (selectedOption) {
      setSelectedType(selectedOption);
    }
    
    // Load saved causes from session storage
    const savedCausesStr = sessionStorage.getItem("asante:selectedCauses");
    if (savedCausesStr) {
      try {
        const savedCauses = JSON.parse(savedCausesStr);
 
        if (selectedOption === "Business") {
          // Handles businesss flow
          const businessCauses = savedCauses.filter(cause => cause.rank === "UNRANKED" && cause.name !== "Emergency Relief").map(cause => cause.name);
          const emergencySelected = savedCauses.some(cause => cause.name === "Emergency Relief");

          setSelectedCausesLocal(businessCauses);
          setIsEmergencyChecked(emergencySelected);

          // Ensure at least 3 selections (or 2 if emergency relief is selected)
          const minimumRequiredSelections = emergencySelected ? 2 : 3;
          setSelectedCausesCount(Math.max(businessCauses.length, minimumRequiredSelections));

        } else if (selectedOption === "Non-Profit") {
          // Handle NP flow
          const primaryCause = savedCauses.find(cause => cause.rank === "PRIMARY");
          const supportingCauses = savedCauses.filter(cause => cause.rank === "SUPPORTING");
          
          if (primaryCause) {
            setSelectedPrimaryCause(primaryCause.name);
            setIsSelectingPrimary(false);
          }
          
          setSelectedSupportingCauses(supportingCauses.map(cause => cause.name));
          setSelectedCausesCount(supportingCauses.length);
        }
      } catch (e) {
        console.error("Error parsing saved causes:", e);
      }
    }
  }, []);

  const handleNext = () => {
    let causesToSave = [];
    
    if (isNonProfit) {
      if (selectedPrimaryCause) {
        causesToSave.push({
          name: selectedPrimaryCause,
          rank: "PRIMARY"
        });
      }

      selectedSupportingCauses.forEach(cause => {
        causesToSave.push({
          name: cause,
          rank: "SUPPORTING"
        });
      });

      // If still selecting primary, move to supporting selection
      if (isSelectingPrimary && selectedPrimaryCause) {
        setIsSelectingPrimary(false);
        return;
      }
    } else {
      // Format causes for Business
      causesToSave = [...selectedCausesLocal].map(cause => ({
        name: cause,
        rank: "UNRANKED"
      }));
      
      if (isEmergencyChecked) { // Only add Emergency Relief if it's explicitly checked
        causesToSave.push({
          name: "Emergency Relief",
          rank: "UNRANKED"
        });
      }
    }
    dispatch(setSelectedCauses({ selected: causesToSave }));
    sessionStorage.setItem("asante:selectedCauses", JSON.stringify(causesToSave));
    navigate(`/register/sizeoptionselection`);
  };

  const handleSelectAll = (sectionItems, isChecked) => {
    if (!isNonProfit) {
      if (isChecked) {
        setSelectedCausesLocal((prev) => [
          ...prev,
          ...sectionItems.filter((item) => !prev.includes(item)),
        ]);
      } else {
        setSelectedCausesLocal((prev) =>
          prev.filter((item) => !sectionItems.includes(item)),
        );
      }
    }
  };

  const handleCheckboxChange = (item) => {
    if (isNonProfit) {
      if (isSelectingPrimary) {
        // Selecting primary cause
        setSelectedPrimaryCause(selectedPrimaryCause === item ? null : item);
      } else {
        // Selecting supporting causes
        if (item === selectedPrimaryCause) return; // Can't select primary cause as supporting
        
        if (selectedSupportingCauses.includes(item)) {
          // Remove the item if it's already selected
          setSelectedSupportingCauses(prev => prev.filter(cause => cause !== item));
          setSelectedCausesCount(prev => prev - 1);
        } else {

          // Add new item and remove oldest if exceeding 2
          setSelectedSupportingCauses(prev => {
            if (prev.length >= 2) {
              return [...prev.slice(1), item];
            }
            return [...prev, item];
          });
          setSelectedCausesCount(prev => prev < 2 ? prev + 1 : prev);
        }
      }
    } else {
      // Original business logic
      if (selectedCausesLocal.includes(item)) {
        setSelectedCausesCount((prev) => prev - 1);
        setSelectedCausesLocal((prev) =>
          prev.filter((option) => option !== item),
        );
      } else {
        setSelectedCausesCount((prev) => prev + 1);
        setSelectedCausesLocal((prev) => [...prev, item]);
      }
    }
  };



  const handleBack = () => {
    if (isNonProfit && !isSelectingPrimary) {
      // Go back to primary cause selection
      setIsSelectingPrimary(true);
      setSelectedSupportingCauses([]);
      setSelectedCausesCount(0);
    } else {
      clearStore();
      navigate(`/`);
    }
  };

  const sections = [
    {
      title: "Community",
      items: [
        "Homelessness",
        "Events & Advocacy",
        "First Responders",
        "Disadvantaged Populations",
        "Schools & Teachers",
      ],
      image: CommunityImage,
      background: "gradient-purple",
      buttonBackground: "rgba(0, 0, 0, 0.27)",
    },
    {
      title: "Social",
      items: [
        "Sports",
        "Arts",
        "Education",
        "Social Justice",
        "Mental Health & Wellbeing",
      ],
      image: SocialImage,
      background: "gradient-pink-orange",
      buttonBackground: "rgba(0, 0, 0, 0.27)",
    },
    {
      title: "Innovation/Entrepreneurship",
      items: [
        "Youth Empowerment",
        "Social Innovation",
        "Sustainable Innovation",
        "Social Entrepreneurship",
      ],
      image: InnovationImage,
      background: "gradient-blue",
      buttonBackground: "rgba(0, 0, 0, 0.27)",
    },
    {
      title: "Environment",
      items: [
        "Droughts & Fire Management",
        "Climate Advocacy",
        "Climate Refugees",
        "Water Sustainability",
      ],
      image: EnvironmentImage,
      background: "gradient-green",
      buttonBackground: "rgba(0, 0, 0, 0.27)",
    },
  ];

  const CustomButton = styled(Button)(({ theme }) => ({
    flex: "0 0 auto",
    top: "-75px",
    right: "-5px",
    fontFamily: "Helvetica Neue, sans-serif",
    fontSize: "18px",
    fontWeight: "400",
    textTransform: "none",
    borderRadius: "4px",
    background: "rgba(0, 0, 0, 0.27)",
    width: "109.145px",
    height: "31.202px",
    color: "white",
    "&:hover": {
      backgroundColor: "rgba(0, 0, 0, 0.4)",
    },
    "& .MuiTouchRipple-root": {
      color: "rgba(255, 255, 255, 0.9)",
    },
  }));

  const CustomCheckbox = styled(Checkbox)({
    color: "white",
    "&.Mui-checked": {
      color: "white",
    },
    "& .MuiSvgIcon-root": {
      fontSize: 24,
      border: "2 solid white",
      borderRadius: 2,
    },
  });

  const BackButton = styled(Typography)({
    color: "#918C8C",
    fontFamily: '"Helvetica Neue", sans-serif',
    fontSize: "25px",
    display: "flex",
    marginLeft: "8px",
    alignItems: "center",
  });

  const handleClose = () => {
    // setIsVisible(false);
    const navigateToLogin = () =>
      setTimeout(() => {
        navigate(`/`);
      }, 300);
    logoutCurrentUser(navigateToLogin, navigateToLogin);
  };

  const handleBackClick = () => {
    clearStore();
    navigate(`/`);
  };

  const highlightClass =
    selectedOption.selected === "Business"
      ? styles["highlight-business"]
      : selectedOption.selected === "Consumer"
        ? styles["highlight-consumer"]
        : selectedOption.selected === "Non-Profit"
          ? styles["highlight-non-profit"]
          : "";

  const businessSteps = ["Causes", "Size", "Basics"];
  const nonprofitSteps = ["Mission", "Size", "Basics"];

  const getInstructionText = () => {
    if (isNonProfit) {
      if (isSelectingPrimary) {
        return "What PRIMARY area is your mission aligned with?";
      }
      return "What SECONDARY area is your mission aligned with?";
    }
    return selectedType === "Business" 
      ? "What non-profit sub-categories do you CARE about supporting?"
      : "What causes do you CARE most about?";
  };

  const getSubText = () => {
    if (isNonProfit) {
      if (isSelectingPrimary) {
        return "(2 secondary choices are available on the next screen)";
      }
      return "(max 2 choices, can edit later in PROFILE)";
    }
    return selectedType === "Business"
      ? "(choose min 3, you can edit later in PROFILE)"
      : "(Pick at least 4, you can edit your choices later in PROFILE)";
  };


  const handleEmergencyChange = () => {
    const updatedEmergencyState = !isEmergencyChecked;
    setIsEmergencyChecked(updatedEmergencyState);
  
    if (isNonProfit) {
      if (isSelectingPrimary) {
        // Set primary cause directly
        setSelectedPrimaryCause(updatedEmergencyState ? "Emergency Relief" : null);
      } else {
        // Update supporting causes
        setSelectedSupportingCauses((prev) => {
          if (updatedEmergencyState) {
            if (!prev.includes("Emergency Relief")) {
              // Add Emergency Relief if not already in the array
              return [...prev, "Emergency Relief"].slice(-2); // Ensure max 2 choices
            }
          } else {
            // Remove Emergency Relief
            return prev.filter((cause) => cause !== "Emergency Relief");
          }
          return prev;
        });
        // Adjust counter
        setSelectedCausesCount((prev) =>
          updatedEmergencyState ? Math.min(prev + 1, 2) : Math.max(prev - 1, 0)
        );
      }
    } else {
      // Business flow adjustments (no changes needed)
      if (updatedEmergencyState) {
        setSelectedCausesCount((prev) => Math.max(prev, 2));
      } else {
        setSelectedCausesCount((prev) => Math.max(prev, 3));
      }
    }
  };

  const isNextEnabled = () => {
    if (isNonProfit) {
      if (isSelectingPrimary) {
        return selectedPrimaryCause !== null;
      }
      return selectedSupportingCauses.length <= 2;
    }
    
    // Business logic
    const regularCausesCount = selectedCausesLocal.length;
    const isEmergencySelected = isEmergencyChecked;
    
    if (isEmergencySelected) {
      // If emergency relief is selected, require 2 additional causes
      return regularCausesCount >= 2;
    } else {
      // Without emergency relief, require at least 3 causes
      return regularCausesCount >= 3;
    }
  };

  const getCheckboxStatus = (item) => {
    if (isNonProfit) {
      if (isSelectingPrimary) {
        return {
          checked: selectedPrimaryCause === item,
          disabled: false
        };
      }
      return {
        checked: selectedSupportingCauses.includes(item) || item === selectedPrimaryCause,
        disabled: item === selectedPrimaryCause 
      };
    }
    return {
      checked: selectedCausesLocal.includes(item),
      disabled: false
    };
  };


  return (
    <Box className={styles.container}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          padding: "10px",
          marginBottom: "20px",
          position: "relative",
        }}
      >
        <Box 
          className={styles.backContainer}
          // onClick={handleBackClick}
          onClick={handleBack}
          sx={{ transform: "translateY(-25px) translateX(-18px)" }}
        >
          <ArrowBackIcon />
          <Typography
            variant="body1"
            sx={{
              color: "#918C8C",
              fontFamily: '"Helvetica Neue", sans-serif',
              fontSize: "25px",
              marginLeft: "5px",
            }}
          >
            Back
          </Typography>
        </Box>
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            // flex: 1,
          }}
        >
          <Avatar
            alt="Company Logo"
            src={logo}
            sx={{
              width: 88,
              height: 88,
              marginRight: "16px",
            }}
          />
          <Typography
            variant="body1"
            sx={{
              color: "#000",
              fontFamily: "Helvetica Neue",
              fontSize: isMobile ? "24px" : "30px",
              fontStyle: "normal",
              fontWeight: 400,
              lineHeight: "normal",
              textAlign: "center",
            }}
          >
            You are registering as a{" "}
            <span className={highlightClass}>{selectedOption.selected}</span>
          </Typography>
        </Box>
        <IconButton
          sx={{
            color: "#000",
            // position: "absolute",
            // top: "1px",
            // right: "1px",
            transform: "translateY(-50px) translateX(330px)",
          }}
          onClick={handleClose}
        >
          <CloseIcon />
        </IconButton>
      </Box>
      {selectedType === "Business" && (
        <Box
          sx={{ width: "100%", maxWidth: 400, margin: "0 auto", mb: 2, mt: -5 }}
        >
          <Stepper activeStep={activeStep} alternativeLabel>
            {businessSteps.map((label, index) => (
              <Step key={label} active={index === 0}>
                <StepLabel>
                  <Typography
                    variant="body1"
                    sx={{
                      fontSize: index === 0 ? "16px" : "14px",
                      fontWeight: index === 0 ? 700 : 400,
                      color: index === 0 ? "#000" : "#A0A0A0",
                    }}
                  >
                    {label}
                  </Typography>
                </StepLabel>
              </Step>
            ))}
          </Stepper>
        </Box>
      )}

      {selectedType === "Non-Profit" && (
        <Box
          sx={{ width: "100%", maxWidth: 400, margin: "0 auto", mb: 2, mt: -5 }}
        >
          <Stepper alternativeLabel>
            {nonprofitSteps.map((label, index) => (
              <Step key={label} active={index === 0}>
                <StepLabel>
                  <Typography
                    variant="body1"
                    sx={{
                      fontSize: index === 0 ? "16px" : "14px",
                      fontWeight: index === 0 ? 700 : 400,
                      color: index === 0 ? "#000" : "#A0A0A0",
                    }}
                  >
                    {label}
                  </Typography>
                </StepLabel>
              </Step>
            ))}
          </Stepper>
        </Box>
      )}

      <Typography
        sx={{
          marginBottom: 1,
          /* marginLeft: isTablet ? 2 : 14,*/
          marginLeft: 7,
          color: "#000",
          fontFamily: "Helvetica Neue",
          fontSize: isMobile ? "20px" : "25px",
          fontStyle: "normal",
          fontWeight: 400,
          lineHeight: "normal",
          /* textAlign: isMobile ? "center" : "left",*/
        }}
      >
        {getInstructionText()}{" "}
        <span
          style={{
            marginBottom: 1,
            color: "#7E7E7E",
            opacity: 0.49,
            fontFamily: "Helvetica Neue",
            fontSize: "22px",
            fontStyle: "normal",
            fontWeight: 400,
            lineHeight: "normal",
          }}
        >
          {getSubText()}
        </span>
      </Typography>

      {/* <Box sx={{ width: "100%", maxWidth: isTablet ? 950 : 1185, margin: "0 auto" }}> */}
      <Box sx={{ width: "100%", maxWidth: 1185 }}>
        <Grid container spacing={2} justifyContent="center" alignItems="stretch">
          {sections.map((section, index) => (
            <Grid item xs={12} sm={6} key={index}>
              <Box
                className={`${styles.optionContainer} ${styles[section.background]}`}
                sx={{
                  borderTopLeftRadius: section.title === "Community" ? "20px" : "0px",
                  borderTopRightRadius: section.title === "Social" ? "20px" : "0px",
                }}
              >
                <Box className={styles.imageContainer}>
                  <img
                    src={section.image}
                    alt={section.title}
                    className={styles.optionImage}
                  />
                </Box>
                <Box className={styles.checkboxContainer}>
                  <Typography variant="h6" className={styles.optionTitle}>
                    {section.title === "Innovation/Entrepreneurship" ? (
                      <span className={styles.splitTitle}>
                        <span className={styles.firstPart}>Innovation/</span>
                        <span className={styles.secondPart}>Entrepreneurship</span>
                      </span>
                    ) : (
                      section.title
                    )}
                  </Typography>
                  {section.items.map((item, idx) => {
                    const { checked, disabled } = getCheckboxStatus(item);
                    return (
                      <FormControlLabel
                       key={idx}
                        control={
                          <CustomCheckbox
                            // checked={selectedCausesLocal.includes(item)}
                            checked={checked}
                            onChange={() => handleCheckboxChange(item)}
                            disabled={disabled}
                          />
                        }
                        label={item}
                        className={styles.checkboxLabel}
                      />
                    );
                  })}
                </Box>
                {!isNonProfit && (
                  <CustomButton
                    // className={styles.selectAllButton}
                    onClick={() =>
                      handleSelectAll(
                        section.items,
                        !section.items.every((item) => selectedCausesLocal.includes(item))
                      )
                    }
                    style={{ background: section.buttonBackground }}
                  >
                    Select All
                  </CustomButton>
                )}
              </Box>
            </Grid>
          ))}
        </Grid>
      </Box>

      <Box
        className={styles.emergencyRelief}
        sx={{
          borderBottomLeftRadius: "20px",
          borderBottomRightRadius: "20px",
          mt: 2,
          // padding: isMobile ? "15px" : "20px",
        }}
      >
        <FormControlLabel
          control={
            <CustomCheckbox
              checked={
                isNonProfit 
                  ? (
                      getCheckboxStatus("Emergency Relief").checked
                    )
                  : isEmergencyChecked
              }
              disabled={
                isNonProfit
                  ? (
                      getCheckboxStatus("Emergency Relief").disabled
                  )
                : false
              }

              onChange={handleEmergencyChange}
            />
          }
          label={
            <Typography
              variant="body1"
              sx={{
                color: "#FFF",
                fontFamily: "Helvetica Neue",
                fontSize: "20px",
                fontStyle: "normal",
                fontWeight: 700,
                lineHeight: "normal",
              }}
            >
              Emergency Relief
            </Typography>
          }
        />
        <Box className={styles.iconsContainer}>
          <img src={FoodIcon} alt="Food Icon" className={styles.icon} />
          <img src={DropIcon} alt="Water Icon" className={styles.icon} />
          <img src={PlusIcon} alt="Medical Icon" className={styles.icon} />
          <img src={MoonIcon} alt="Shelter Icon" className={styles.icon} />
          <img src={ToolboxIcon} alt="Supplies Icon" className={styles.icon} />
        </Box>
      </Box>
      
      <Box className={styles.nextButton}>
        <Button
          variant="contained"
          sx={{
            background: "linear-gradient(to right, #6271AE, #9ACDDA)",
            borderRadius: "56px",
            color: "#FFF",
            fontSize: isMobile ? "18px" : "20px",
            fontWeight: 600,
            width: isMobile ? "100%" : "287px",
            height: "56px",
            textTransform: "none",
          }}
          // disabled={causesSelectedCount < 3}
          disabled={!isNextEnabled()}
          onClick={handleNext}
        >
          {/* Next */}
          {isNonProfit && isSelectingPrimary ? "Next: Supporting Causes" : "Next"}
        </Button>
      </Box>
    </Box>
  );
};

export default CausesComponent;
