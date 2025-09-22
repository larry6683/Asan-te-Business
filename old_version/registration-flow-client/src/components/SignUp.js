import React, { useState } from "react";
import Box from "@mui/material/Box";
import styles from "./SignUp.module.css";
import { styled } from "@mui/material/styles";
import Button from "@mui/material/Button";
import { ReactComponent as ArrowBackIcon } from "../assets/ionic-ios-arrow-back.svg";
import Typography from "@mui/material/Typography";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import {
  TextField,
  Link,
  InputAdornment,
  IconButton,
  Checkbox,
} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import PasswordStrengthIndicator from "./PasswordStrengthIndicator";
import { signupUser } from "../user-auth/signupUser";
import { getUserAuthenticationTokenAndSaveInStorage } from "../user-auth/authenticateUser";
import { useDispatch } from "react-redux";
import { setEmailID } from "../redux/emailSlice";
import { USER_TYPE } from "../types/userType";
import validator from "validator";

const CustomButton = styled(Button)({
  width: "450px",
  height: "69px",
  borderRadius: "56px",
  background: "linear-gradient(to right, #6271AE, #9ACDDA)",
  color: "var(--barcolor, #FFF)",
  textTransform: "none",
  fontFamily: '"Helvetica Neue", sans-serif',
  fontSize: "28px",
  fontStyle: "bold",
  fontWeight: 700,
  lineHeight: "normal",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  marginTop: "10px",
  "&:hover": {
    background: "linear-gradient(90deg, #5B6BB0 0%, #8ACDDB 100%)",
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

const SignUp = () => {
  const [email, setEmail] = useState("");
  const [emailError, setEmailError] = useState(false);
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [agreeToMailingList, setAgreeToMailingList] = useState(true);
  const [passwordError, setPasswordError] = useState(false);
  const selectedOption = useSelector((state) => state.selectedOption);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const handleClickShowConfirmPassword = () => {
    setShowConfirmPassword(!showConfirmPassword);
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const handleBackClick = () => {
    navigate(`/`);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!validator.isEmail(email)) {
      setEmailError(true);
      return;
    }
    if (password !== confirmPassword) {
      setPasswordError(true);
      return;
    }

    // signup to user business admin userpool
    let entityType;
    if (selectedOption.selected === "Business") {
      entityType = USER_TYPE.BUSINESS_ADMIN;
    } else if (selectedOption.selected === "Consumer") {
      entityType = USER_TYPE.CONSUMER;
    } else if (selectedOption.selected === "Non-Profit") {
      entityType = USER_TYPE.BENEFICIARY_ADMIN;
    } else {
      console.error("signup: invalid pool selection");
    }

    if (entityType) {
      dispatch(setEmailID(email));
      // I don't think callbacks should be used like this
      // but I was running into a weird async issue with displaying result in console
      let signupSuccess = false;
      let authenticationSuccess = false;
      signupSuccess = signupUser(
        entityType,
        email,
        password,
        agreeToMailingList ? "true" : "false",
        () => {
          // console.log("sign-up success");
          navigate(`/register/verification`);
          signupSuccess = true;
        },
        (err) => {
          signupSuccess = false;
          // console.error("sign-up error", err);
        },
      );
    }
  };

  const highlightClass =
    selectedOption.selected === "Business"
      ? styles["highlight-business"]
      : selectedOption.selected === "Consumer"
        ? styles["highlight-consumer"]
        : selectedOption.selected === "Non-Profit"
          ? styles["highlight-non-profit"]
          : "";

  const formattedText =
    selectedOption.selected === "Non-Profit"
      ? "Non-Profit"
      : selectedOption.selected.toUpperCase();

  const getPasswordStrength = (password) => {
    let strength = 0;
    if (password.length >= 8) strength += 1;
    if (/[A-Z]/.test(password)) strength += 1;
    if (/[0-9]/.test(password)) strength += 1;
    if (/[^A-Za-z0-9]/.test(password)) strength += 1;
    return strength;
  };

  const strength = getPasswordStrength(password);

  return (
    <React.Fragment>
      <Box className={styles.box}>
        <Box onClick={handleBackClick} className={styles.backContainer}>
          <ArrowBackIcon />
          <BackButton>Back</BackButton>
        </Box>
        <Box
          component="img"
          src={selectedOption.image}
          alt={selectedOption.selected}
          className={styles.imageContainer}
        />
        <Typography
          variant="h5"
          gutterBottom
          sx={{
            marginTop: 2,
            color: "#000",
            fontFamily: "Helvetica Neue",
            fontSize: "30px",
            fontStyle: "normal",
            fontWeight: 400,
            lineHeight: "normal",
          }}
        >
          You are registering as a{" "}
          <span className={`${styles.highlight} ${highlightClass}`}>
            {formattedText}
          </span>
        </Typography>
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          marginTop={4}
          component="form"
          onSubmit={handleSubmit}
        >
          <Box width="100%">
            <Typography
              variant="body1"
              gutterBottom
              sx={{
                marginBottom: 0,
                color: "#000",
                fontFamily: "Helvetica Neue",
                fontSize: "25px",
                fontStyle: "normal",
                fontWeight: 400,
                lineHeight: "normal",
              }}
            >
              Email
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="email"
              placeholder="Enter your email address here"
              name="email"
              autoComplete="email"
              autoFocus
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                if (emailError) setEmailError(false);
              }}
              sx={{ width: "450px", height: "49px", borderRadius: "21px" }}
              InputProps={{
                style: {
                  borderRadius: "21px",
                },
                classes: {
                  input: styles.customPlaceholder,
                },
              }}
              error={emailError}
              helperText={emailError ? "Must be an email address." : ""}
            />
          </Box>
          <Box width="100%" mt={2} mb={2}>
            <Typography
              variant="body1"
              gutterBottom
              sx={{
                marginBottom: 0,
                color: "#000",
                fontFamily: "Helvetica Neue",
                fontSize: "25px",
                fontStyle: "normal",
                fontWeight: 400,
                lineHeight: "normal",
              }}
            >
              Password
            </Typography>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              placeholder="Enter your password here"
              type={showPassword ? "text" : "password"}
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              sx={{ width: "450px", height: "49px", borderRadius: "21px" }}
              InputProps={{
                style: {
                  borderRadius: "21px",
                },
                classes: {
                  input: styles.customPlaceholder,
                },
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={handleClickShowPassword}
                      onMouseDown={handleMouseDownPassword}
                      edge="end"
                      tabIndex={-1}
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          </Box>
          {password && strength < 4 ? (
            <PasswordStrengthIndicator password={password} />
          ) : (
            <React.Fragment>
              <Box width="100%" mt={0} mb={1}>
                <Typography
                  variant="body1"
                  gutterBottom
                  sx={{
                    marginBottom: 0,
                    color: "#000",
                    fontFamily: "Helvetica Neue",
                    fontSize: "25px",
                    fontStyle: "normal",
                    fontWeight: 400,
                    lineHeight: "normal",
                  }}
                >
                  Confirm Password
                </Typography>
                <TextField
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  name="confirmPassword"
                  placeholder="Re-enter your password to confirm"
                  type={showConfirmPassword ? "text" : "password"}
                  id="confirmPassword"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  sx={{ width: "450px", height: "49px", borderRadius: "21px" }}
                  InputProps={{
                    style: {
                      borderRadius: "21px",
                    },
                    classes: {
                      input: styles.customPlaceholder,
                    },
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          aria-label="toggle confirm password visibility"
                          onClick={handleClickShowConfirmPassword}
                          onMouseDown={handleMouseDownPassword}
                          edge="end"
                          tabIndex={-1}
                        >
                          {showConfirmPassword ? (
                            <VisibilityOff />
                          ) : (
                            <Visibility />
                          )}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                  error={passwordError}
                  helperText={passwordError ? "Passwords do not match." : ""}
                />
              </Box>
              <Box
                display="flex"
                alignItems="flex-start"
                sx={{ width: "100%", mb: 2, mt: 2 }}
              >
                <Checkbox
                  checked={agreeToMailingList}
                  onChange={(e) => setAgreeToMailingList(e.target.checked)}
                  color="primary"
                  sx={{ mt: -1.3 }}
                />
                <Box>
                  <Typography
                    sx={{
                      fontFamily: '"Helvetica Neue", sans-serif',
                      fontSize: "22px",
                      color: "#000",
                      lineHeight: "20px",
                    }}
                  >
                    I agree to join ASANTe’s mailing list
                  </Typography>
                  <Typography
                    sx={{
                      fontFamily: '"Helvetica Neue", sans-serif',
                      fontSize: "22px",
                      color: "#A0A0A0",
                      lineHeight: "20px",
                    }}
                  >
                    (promise no spam)
                  </Typography>
                </Box>
              </Box>
            </React.Fragment>
          )}
          <CustomButton type="submit">Sign Up</CustomButton>
          <Typography
            variant="body2"
            align="center"
            sx={{
              color: "#A0A0A0",
              fontFamily: "Helvetica Neue",
              fontSize: "22px",
              fontStyle: "normal",
              fontWeight: 400,
              lineHeight: "normal",
              marginTop: "10px",
            }}
          >
            Already a member?{" "}
            <Link
              href="/"
              sx={{
                color: "#7182B3",
                fontFamily: "Helvetica Neue",
                fontSize: "22px",
                fontStyle: "normal",
                fontWeight: 500,
                lineHeight: "normal",
                textDecorationLine: "underline",
                textDecorationColor: "#7182B3",
              }}
            >
              Log in
            </Link>
          </Typography>
          <Box
            sx={{
              color: "#A0A0A0",
              fontFamily: "Helvetica Neue",
              fontSize: "16px",
              fontStyle: "normal",
              fontWeight: 400,
              lineHeight: "normal",
              marginTop: "10px",
              maxWidth: "450px",
              textAlign: "center",
              marginBottom: "16px",
            }}
          >
            <Typography
              component="span"
              sx={{
                display: "block",
              }}
            >
              By signing up you are agreeing to
            </Typography>
            <Link
              href="#"
              sx={{
                color: "#7182B3",
                textDecoration: "underline",
                marginLeft: "5px",
              }}
            >
              ASANTe’s Privacy Policy
            </Link>
            {" and "}
            <Link
              href="#"
              sx={{
                color: "#7182B3",
                textDecoration: "underline",
                marginLeft: "5px",
              }}
            >
              Terms
            </Link>
          </Box>
        </Box>
      </Box>
    </React.Fragment>
  );
};

export default SignUp;
