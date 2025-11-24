import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import Box from "@mui/material/Box";
import Typography from '@mui/material/Typography';
import styles from "./Login.module.css";
import { 
  TextField, 
  Link, 
  InputAdornment, 
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
  CircularProgress,
  Alert
} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { getUserAuthenticationTokenAndSaveInStorage } from "../user-auth/authenticateUser";
import { setEmailID } from "../redux/emailSlice";
import { setUser } from "../redux/userSlice";
import { clearStore } from "../redux/store";
import { setSelectedOption } from "../redux/selectedOptionSlice";
import { USER_TYPE } from "../types/userType";
import { UserApiService } from "../api/userApiService";
import { grpcService } from "../api/grpcService";
// ✅ Import analytics service
import { analyticsService } from "../api/analyticsService";

// ✅ Import Forgot Password Logic
import { initiateForgotPassword, confirmForgotPassword } from "../user-auth/forgotPassword";

import BusinessImage from "../assets/business.png";
import ConsumerImage from "../assets/consumer.png";
import NonprofitImage from "../assets/nonprofit.png";
import { CookieFactory } from "../cookies/cookieFactory";
import { redirectUrls } from "../web-data/redirectUrls"

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [invalidCredentials, setInvalidCredentials] = useState(false);
  const [emailEmpty, setEmailEmpty] = useState(false);
  const [passwordEmpty, setPasswordEmpty] = useState(false);

  // --- Forgot Password State ---
  const [forgotPasswordOpen, setForgotPasswordOpen] = useState(false);
  const [fpStage, setFpStage] = useState("request"); // 'request' | 'reset' | 'success'
  const [fpEmail, setFpEmail] = useState("");
  const [fpCode, setFpCode] = useState("");
  const [fpNewPassword, setFpNewPassword] = useState("");
  const [fpConfirmPassword, setFpConfirmPassword] = useState("");
  const [fpLoading, setFpLoading] = useState(false);
  const [fpError, setFpError] = useState(null);
  // -----------------------------

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleClickShowPassword = () => setShowPassword(!showPassword);
  const handleMouseDownPassword = (event) => event.preventDefault();

  const validateForm = () => {
    let valid = true;
    if (email.length === 0) {
      valid = false;
      setEmailEmpty(true);
    }
    if (password.length === 0) {
      valid = false;
      setPasswordEmpty(true);
    }
    return valid;
  };

  const getImageForType = (type) => {
    switch (type) {
      case "Business":
        return BusinessImage;
      case "Non-Profit":
        return NonprofitImage;
      case "Consumer":
        return ConsumerImage;
      default:
        return ConsumerImage;
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!validateForm()) return;
    
    let registrationOption = null;
    getUserAuthenticationTokenAndSaveInStorage(
      email,
      password,
      // success callback
      (result) => {
        registrationOption = getRegistrationOptionFromUserData(result);
        getUserIdAndContinue(registrationOption);
      },
      (error) => {
        if (error.name === "UserNotConfirmedException") {
          dispatch(setEmailID(email));
          navigate(`/register/verification`);
        } else {
          setInvalidCredentials(true);
        }
      },
    );
  };

  const getRegistrationOptionFromUserData = (userData) => {
    let option = "";
    let image = "";
    if (userData.userType === USER_TYPE.BUSINESS_ADMIN) {
      option = "Business";
      image = BusinessImage;
    } else if (userData.userType === USER_TYPE.BENEFICIARY_ADMIN) {
      option = "Non-Profit";
      image = NonprofitImage;
    } else if (userData.userType === USER_TYPE.CONSUMER) {
      option = "Consumer";
      image = ConsumerImage;
    }
    return { registeringAs: option, registeringAsImage: image };
  };

  const getUserIdAndContinue = async (registrationOption) => {
    if (registrationOption) {
      dispatch(setSelectedOption({
        selected: registrationOption.registeringAs,
        image: registrationOption.registeringAsImage,
      }));
      dispatch(setEmailID(email));
      
      const userApiService = new UserApiService();
      
      try {
        // Get user from database
        const userResponse = await userApiService.getUserByEmail(email);
        
        console.log('📧 User retrieved:', userResponse.data.attributes.email);
        
        const user = {
          id: userResponse.data.id,
          email: userResponse.data.attributes.email,
          userType: userResponse.data.attributes.userType,
        };
        
        // Save user to Redux and session
        dispatch(setUser(user));
        sessionStorage.setItem("asante:user", JSON.stringify(user));

        // ✅ ADDED: Update Analytics with User Identity
        console.log("📊 Linking session to user in analytics...");
        await analyticsService.trackStep(1); 
        
        // Check if user has a business/beneficiary in the database
        const token = sessionStorage.getItem("asante:accessJwt");
        
        // ✅ FIXED LOGIC: Default assumes we need to register, unless we find an entity
        let entityFound = false; 

        if (registrationOption.registeringAs === "Business") {
          console.log('🔍 Checking if business exists for:', email);
          
          try {
            const businessResponse = await grpcService.getBusinessByUserEmail(email, token);
            const hasBusiness = businessResponse.getHasBusiness();
            
            console.log('✅ Business check result:', hasBusiness);
            
            if (hasBusiness) {
              entityFound = true; // Business exists!
              const business = businessResponse.getBusiness();
              const businessId = business.getId();
              
              console.log('🏢 Business found:', business.getBusinessName(), 'ID:', businessId);
              sessionStorage.setItem("asante:businessId", businessId);
              CookieFactory.createAppCookieFromDataOrStorage(
                user, 
                { entityType: "business", entityId: businessId }
              );
            }
          } catch (error) {
            console.error('Error checking business:', error);
          }
          
        } else if (registrationOption.registeringAs === "Non-Profit") {
          console.log('🔍 Checking if beneficiary exists for:', email);
          
          try {
            const beneficiaryResponse = await grpcService.getBeneficiaryByUserEmail(email, token);
            const hasBeneficiary = beneficiaryResponse.getHasBeneficiary();
            
            console.log('✅ Beneficiary check result:', hasBeneficiary);
            
            if (hasBeneficiary) {
              entityFound = true; // Beneficiary exists!
              const beneficiary = beneficiaryResponse.getBeneficiary();
              const beneficiaryId = beneficiary.getId();
              
              console.log('💚 Beneficiary found:', beneficiary.getBeneficiaryName(), 'ID:', beneficiaryId);
              sessionStorage.setItem("asante:beneficiaryId", beneficiaryId);
              CookieFactory.createAppCookieFromDataOrStorage(
                user,
                { entityType: "beneficiary", entityId: beneficiaryId }
              );
            }
          } catch (error) {
            console.error('Error checking beneficiary:', error);
          }
        } else {
            // Consumers always go to home
            entityFound = true;
        }
        
        // ✅ FIXED: Navigate based on whether Entity was found
        if (entityFound) {
            console.log('✅ Login successful & Entity found - navigating to /home');
            navigate('/home');
        } else {
            console.log('⚠️ User exists but no Entity found - resuming registration flow...');
            navigate('/register/causes');
        }
        
      } catch (error) {
        console.error('❌ Error during login flow:', error);
        
        try {
          const errorJson = JSON.parse(error.message);
          if (errorJson.errors) {
            errorJson.errors.forEach((value) => {
              if (value.errorCode === 250) {
                // User doesn't exist in our database, create them
                createUserAndContinue(email, registrationOption);
              }
            });
          }
        } catch (error2) {
          setInvalidCredentials(true);
        } 
      }
    } else {
      setInvalidCredentials(true);
    }
  };

  // ✅ UPDATED: Now accepts registrationOption to determine user type
  const createUserAndContinue = (email, registrationOption) => {
    // Determine the backend User Type string
    let backendUserType = "CONSUMER"; // Default
    
    if (registrationOption?.registeringAs === "Business") {
        backendUserType = "BUSINESS";
    } else if (registrationOption?.registeringAs === "Non-Profit") {
        backendUserType = "BENEFICIARY";
    }

    const userApiService = new UserApiService();
    
    // ✅ FIXED: Passing all 5 arguments required by UserApiService
    userApiService.createUser(
      email,
      backendUserType, // 2. User Type
      false,           // 3. Mailing List (default false)
      (response) => {  // 4. Success Callback
        const user = {
          id: response.data.id,
          email: response.data.attributes.email,
          userType: response.data.attributes.userType,
        };
        dispatch(setUser(user));
        sessionStorage.setItem("asante:user", JSON.stringify(user));
        
        // Track analytics
        analyticsService.trackStep(1);

        // New user always goes to registration flow
        console.log(`✅ New user created (${backendUserType}). Navigating to registration...`);
        navigate(`/register/causes`);
      },
      (error) => {     // 5. Failure Callback
        console.error("Failed to create user during login:", error);
        clearStore(true);
        setInvalidCredentials(true);
      }
    );
  };

  // --- Forgot Password Handlers ---
  const handleOpenForgotPassword = () => {
    setFpEmail(email); // Pre-fill email from login form
    setFpStage("request");
    setFpError(null);
    setForgotPasswordOpen(true);
  };

  const handleCloseForgotPassword = () => {
    setForgotPasswordOpen(false);
    // Reset state after animation finishes
    setTimeout(() => {
      setFpStage("request");
      setFpCode("");
      setFpNewPassword("");
      setFpConfirmPassword("");
      setFpError(null);
    }, 300);
  };

  const handleRequestCode = () => {
    if (!fpEmail) {
      setFpError("Please enter your email address.");
      return;
    }
    setFpLoading(true);
    setFpError(null);

    initiateForgotPassword(
      fpEmail,
      () => {
        setFpLoading(false);
        setFpStage("reset");
      },
      (err) => {
        setFpLoading(false);
        setFpError(err.message || "Failed to send verification code.");
      }
    );
  };

  const handleResetPassword = () => {
    if (!fpCode || !fpNewPassword || !fpConfirmPassword) {
      setFpError("Please fill in all fields.");
      return;
    }
    if (fpNewPassword !== fpConfirmPassword) {
      setFpError("Passwords do not match.");
      return;
    }
    // Basic length check, Cognito will enforce complexity
    if (fpNewPassword.length < 8) {
      setFpError("Password must be at least 8 characters.");
      return;
    }

    setFpLoading(true);
    setFpError(null);

    confirmForgotPassword(
      fpEmail,
      fpCode,
      fpNewPassword,
      () => {
        setFpLoading(false);
        setFpStage("success");
        // Optional: Pre-fill password field on login
        setPassword(fpNewPassword);
      },
      (err) => {
        setFpLoading(false);
        setFpError(err.message || "Failed to reset password.");
      }
    );
  };
  // --------------------------------

  return (
    <div className={styles.loginContainer}>
      <Box className={styles.loginBox}>
        <div className={styles.asanteTitle}>
          AsanTe
        </div>
        <div className={styles.welcomeText}>
          Welcome!
        </div>
        <Box
          component="form"
          className={styles.formContainer}
          onSubmit={handleSubmit}
        >
          <div className={styles.inputGroup}>
            <TextField
              required
              fullWidth
              id="email"
              label="Email"
              name="email"
              autoComplete="email"
              autoFocus
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                setEmailEmpty(false);
                setInvalidCredentials(false);
              }}
              error={emailEmpty || invalidCredentials}
              helperText={
                emailEmpty
                  ? "Email is required"
                  : invalidCredentials
                    ? "Invalid email or password"
                    : ""
              }
              className={styles.textField}
            />
          </div>
          <div className={styles.inputGroup}>
            <TextField
              required
              fullWidth
              name="password"
              label="Password"
              type={showPassword ? "text" : "password"}
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setPasswordEmpty(false);
                setInvalidCredentials(false);
              }}
              error={passwordEmpty || invalidCredentials}
              helperText={
                passwordEmpty
                  ? "Password is required"
                  : invalidCredentials
                    ? ""
                    : ""
              }
              className={styles.textField}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={handleClickShowPassword}
                      onMouseDown={handleMouseDownPassword}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          </div>
          <button type="submit" className={styles.loginButton}>
            Log in
          </button>
          <p className={styles.signupText}>
            Don't have an account?{" "}
            <Link href={`/register`} className={styles.signupLink}>
              Create Account
            </Link>
          </p>
          <Link 
            component="button" 
            variant="body2" 
            onClick={handleOpenForgotPassword}
            className={styles.forgotPasswordLink}
            sx={{ textDecoration: 'none', fontSize: '16px' }}
          >
            Forgot Password?
          </Link>
        </Box>
      </Box>

      {/* --- Forgot Password Dialog --- */}
      <Dialog open={forgotPasswordOpen} onClose={handleCloseForgotPassword} maxWidth="xs" fullWidth>
        <DialogTitle sx={{ fontFamily: '"Helvetica Neue", sans-serif', fontWeight: 'bold', color: '#5B6BB0' }}>
          {fpStage === "request" && "Reset Password"}
          {fpStage === "reset" && "Set New Password"}
          {fpStage === "success" && "Success!"}
        </DialogTitle>
        <DialogContent>
          {fpError && <Alert severity="error" sx={{ mb: 2 }}>{fpError}</Alert>}
          
          {fpStage === "request" && (
            <>
              <DialogContentText sx={{ mb: 2, fontFamily: '"Helvetica Neue", sans-serif' }}>
                Enter your email address and we'll send you a verification code to reset your password.
              </DialogContentText>
              <TextField
                autoFocus
                margin="dense"
                id="fp-email"
                label="Email Address"
                type="email"
                fullWidth
                variant="outlined"
                value={fpEmail}
                onChange={(e) => setFpEmail(e.target.value)}
              />
            </>
          )}

          {fpStage === "reset" && (
            <>
              <DialogContentText sx={{ mb: 2, fontFamily: '"Helvetica Neue", sans-serif' }}>
                Check your email for the verification code.
              </DialogContentText>
              <TextField
                margin="dense"
                id="fp-code"
                label="Verification Code"
                type="text"
                fullWidth
                variant="outlined"
                value={fpCode}
                onChange={(e) => setFpCode(e.target.value)}
                sx={{ mb: 2 }}
              />
              <TextField
                margin="dense"
                id="fp-new-password"
                label="New Password"
                type="password"
                fullWidth
                variant="outlined"
                value={fpNewPassword}
                onChange={(e) => setFpNewPassword(e.target.value)}
                sx={{ mb: 2 }}
              />
              <TextField
                margin="dense"
                id="fp-confirm-password"
                label="Confirm New Password"
                type="password"
                fullWidth
                variant="outlined"
                value={fpConfirmPassword}
                onChange={(e) => setFpConfirmPassword(e.target.value)}
              />
            </>
          )}

          {fpStage === "success" && (
            <DialogContentText sx={{ fontFamily: '"Helvetica Neue", sans-serif', color: 'green', fontWeight: 500 }}>
              Your password has been reset successfully. You can now log in with your new password.
            </DialogContentText>
          )}
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          {fpStage !== "success" && (
            <Button onClick={handleCloseForgotPassword} sx={{ color: '#888' }}>
              Cancel
            </Button>
          )}
          
          {fpStage === "request" && (
            <Button 
              onClick={handleRequestCode} 
              variant="contained" 
              disabled={fpLoading}
              sx={{ bgcolor: '#5B6BB0', '&:hover': { bgcolor: '#4A5895' } }}
            >
              {fpLoading ? <CircularProgress size={24} color="inherit" /> : "Send Code"}
            </Button>
          )}

          {fpStage === "reset" && (
            <Button 
              onClick={handleResetPassword} 
              variant="contained"
              disabled={fpLoading}
              sx={{ bgcolor: '#5B6BB0', '&:hover': { bgcolor: '#4A5895' } }}
            >
              {fpLoading ? <CircularProgress size={24} color="inherit" /> : "Reset Password"}
            </Button>
          )}

          {fpStage === "success" && (
            <Button 
              onClick={handleCloseForgotPassword} 
              variant="contained"
              sx={{ bgcolor: '#5B6BB0', '&:hover': { bgcolor: '#4A5895' } }}
            >
              Back to Login
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default Login;