import React, { useState, useRef, useEffect } from "react";
import { Box, Typography, TextField, Link, Button } from "@mui/material";
import styles from "./VerificationComponent.module.css";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { verifyUser } from "../user-auth/verifyUser";
import { resendUserVerificationCode } from "../user-auth/resendUserAuthenticationCode";
import { USER_TYPE } from "../types/userType";
import { analyticsService } from "../api/analyticsService";

const VerificationComponent = () => {
  const email = useSelector((state) => state.email.address);
  const selectedOption = useSelector((state) => state.selectedOption);
  const [verificationCode, setVerificationCode] = useState(Array(6).fill(""));
  const [successMessage, setSuccessMessage] = useState(""); // New state for feedback
  const refs = useRef([]);
  const navigate = useNavigate();
  const dispatch = useDispatch();

  useEffect(() => {
    refs.current = verificationCode.map(
      (_, i) => refs.current[i] || React.createRef(),
    );
  }, [verificationCode]);

  // Shared logic to handle successful verification
  const handleVerificationSuccess = () => {
    // 1. Track analytics
    analyticsService.completeStep(2, 3);

    // 2. Show feedback
    setSuccessMessage("Verification Successful! Redirecting to login...");

    // 3. Navigate to Login after a short delay
    // CRITICAL FIX: User MUST log in to generate Session Data and DB Record
    setTimeout(() => {
        navigate("/"); 
    }, 1500);
  };

  const handleChange = (e, index) => {
    const { value } = e.target;
    if (/^[0-9]$/.test(value) || value === "") {
      const newCode = [...verificationCode];
      newCode[index] = value;
      setVerificationCode(newCode);

      if (value !== "" && index < 5 && refs.current[index + 1]) {
        refs.current[index + 1].focus();
      }

      const codeStr = newCode.join("");
      if (codeStr.length === 6) {
        verifyUser(
          email,
          codeStr,
          handleVerificationSuccess, // Use the fixed handler
          (err) => {
            console.error("error callback", err);
          },
        );
      }
    }
  };

  const handleKeyDown = (e, index) => {
    if (e.key === "Backspace" && verificationCode[index] === "") {
      if (index > 0 && refs.current[index - 1]) {
        refs.current[index - 1].focus();
      }
    }
  };

  const handleResendCode = () => {
    resendUserVerificationCode(email);
  };

  const handleUseDifferentEmail = () => {
     navigate('/register');
  };

  const handlePaste = (event) => {
    const pastedText = event.clipboardData.getData("text");
    if (pastedText.length === 6 && /^\d{6}$/.test(pastedText)) {
      const arr = Array.from(pastedText);
      setVerificationCode(arr);
      const codeStr = arr.join("");
      
      verifyUser(
        email,
        codeStr,
        handleVerificationSuccess, // Use the fixed handler
        (err) => {
          console.error("error callback", err);
        },
      );
    }
    event.preventDefault();
  };

  return (
    <Box className={styles.container}>
      <div className={styles.imageContainer} />
      
      {/* Success Message Overlay */}
      {successMessage ? (
        <Box sx={{ textAlign: 'center', marginTop: '50px' }}>
            <Typography variant="h5" color="primary">
                ✅ {successMessage}
            </Typography>
        </Box>
      ) : (
        <>
            <Typography
                variant="h5"
                gutterBottom
                sx={{
                color: "#000",
                fontFamily: "Helvetica Neue, sans-serif",
                fontSize: "25px",
                fontWeight: 700,
                marginBottom: "25px",
                }}
            >
                Check your inbox
            </Typography>
            <Typography
                variant="body2"
                sx={{
                color: "#888",
                opacity: 0.6,
                fontFamily: "Helvetica Neue, sans-serif",
                fontSize: "20px",
                fontWeight: 400,
                textAlign: "center",
                marginBottom: "45px",
                }}
            >
                Please enter the code and verify
                <br />
                your email: {email}
            </Typography>
            
            <Box className={styles.codeInputContainer}>
                {verificationCode.map((digit, index) => (
                <TextField
                    key={index}
                    value={digit}
                    onChange={(e) => handleChange(e, index)}
                    onKeyDown={(e) => handleKeyDown(e, index)}
                    onPaste={handlePaste}
                    inputProps={{
                    maxLength: 1,
                    autoComplete: "one-time-code",
                    }}
                    inputRef={(ref) => (refs.current[index] = ref)}
                    sx={{
                    width: "50px",
                    height: "40px",
                    textAlign: "center",
                    borderRadius: "8px",
                    "& .MuiOutlinedInput-root": {
                        borderRadius: "8px",
                    },
                    marginBottom: "12px",
                    }}
                />
                ))}
            </Box>
            
             <Typography
                variant="body2"
                sx={{
                color: "#A0A0A0",
                fontFamily: "Helvetica Neue, sans-serif",
                fontSize: "16px",
                fontWeight: 305,
                textAlign: "center",
                }}
            >
                Did not receive code yet? Did you check spam?
            </Typography>
            <Typography variant="body2" sx={{ marginBottom: "30px" }}>
                <Link href="#" onClick={handleResendCode} sx={{ color: "#7182B3", fontSize: "16px" }}>
                Resend code
                </Link>
            </Typography>
            <Typography variant="body2">
                <Link href="#" onClick={handleUseDifferentEmail} sx={{ color: "#909090", fontSize: "16px", textDecoration: "underline" }}>
                Use a Different Email?
                </Link>
            </Typography>
        </>
      )}
    </Box>
  );
};

export default VerificationComponent;