import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import Box from "@mui/material/Box";
import Typography from '@mui/material/Typography';
import styles from "./Login.module.css";
import { TextField, Link, InputAdornment, IconButton } from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { getUserAuthenticationTokenAndSaveInStorage } from "../user-auth/authenticateUser";
import { setEmailID } from "../redux/emailSlice";
import { setUser } from "../redux/userSlice";
import { clearStore } from "../redux/store";
import { setSelectedOption } from "../redux/selectedOptionSlice";
import { USER_TYPE } from "../types/userType";
import { UserApiService } from "../api/userApiService";

import BusinessImage from "../assets/business.png";
import ConsumerImage from "../assets/consumer.png";
import NonprofitImage from "../assets/nonprofit.png";
import { CookieFactory } from "../cookies/cookieFactory";
import { redirectUrls } from "../web-data/redirectUrls"

const Login = () => {
  clearStore(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [invalidCredentials, setInvalidCredentials] = useState(false);
  const [emailEmpty, setEmailEmpty] = useState(false);
  const [passwordEmpty, setPasswordEmpty] = useState(false);

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

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!validateForm()) return;
    let registrationOption = null;
    getUserAuthenticationTokenAndSaveInStorage(
      email,
      password,
      // success callback
      // the auth token has already been saved
      // big future TODO is to separate out all of this tangled code. :(
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

  const getUserIdAndContinue = (registrationOption) => {
    if (registrationOption) {
      dispatch(setSelectedOption({
        selected: registrationOption.registeringAs,
        image: registrationOption.registeringAsImage,
      }));
      dispatch(setEmailID(email));
      const userApiService = new UserApiService();
      userApiService.getUserByEmail(email)
        .then((response) => {

            // 🔍 ADD ALL THIS LOGGING:
          console.log('🔍 Full response:', response);
          console.log('🔍 response.data:', response.data);
          console.log('🔍 response.data.relationships:', response.data.relationships);
          console.log('🔍 Session businessId:', sessionStorage.getItem("asante:businessId"));
          console.log('🔍 Session beneficiaryId:', sessionStorage.getItem("asante:beneficiaryId"));
          const user = {
            id: response.data.id,
            email: response.data.attributes.email,
            userType: response.data.attributes.userType,
          };
          if (response.data.relationships) {
            const relationships = response.data.relationships;

            // this indicates a user has already registered a business
            // or belongs to one.
            let entityType = ""
            let entityId = ""
            if (relationships.businesses) {
              const entity = relationships.businesses.data[0];
              entityType = "business"
              entityId = entity.id;
            } else if (relationships.beneficiaries) {
              const entity = relationships.beneficiaries.data[0];
              entityType = "business"
              entityId = entity.id;
            }
            CookieFactory.createAppCookieFromDataOrStorage(
              user, { entityType: entityType, entityId: entityId }
            )
            // navigate to profile.
            window.location.href = `${redirectUrls.portal}/profile`;
          } else {
            dispatch(setUser(user));
          
            sessionStorage.setItem("asante:user", JSON.stringify(user));
            navigate(`/register/causes`);
          }
        })
        .catch((error) => {
          try {
            const errorJson = JSON.parse(error.message);
            if (errorJson.errors) {
              errorJson.errors.forEach((value) => {
                if (value.errorCode === 250) {
                  createUserAndContinue(email);
                }
              });
            }
          } catch (error2) {
            setInvalidCredentials(true);
          } 
        });
    } else {
      setInvalidCredentials(true);
    }
  };

  const createUserAndContinue = (email) => {
    const userApiService = new UserApiService();
    userApiService.createUser(
      email,
      (response) => {
        const user = {
          id: response.data.id,
          email: response.data.attributes.email,
          userType: response.data.attributes.userType,
        };
        dispatch(setUser(user));
        sessionStorage.setItem("asante:user", JSON.stringify(user));
        navigate(`/register/causes`);
      },
      (error) => {
        clearStore(true);
        setInvalidCredentials(true);
      }
    );
  };

  return (
    <div className={styles.container}>
      <Box className={styles.box}>
        <div className={styles.imageContainer}></div>
        <div className={styles.textSecondary}>
          Log in to <span className={styles.highlight}>ASANTe</span> portal
        </div>
        <Box
          component="form"
          onSubmit={handleSubmit}
          className={styles.formContainer}
        >
          <div className={styles.inputWrapper}>
            <label htmlFor="email" className={styles.inputLabel}>
              Email
              {invalidCredentials && <span className={styles.errorText}> Invalid Credentials</span>}
              {emailEmpty && <span className={styles.errorText}> Email required</span>}
            </label>
            <TextField
              variant="outlined"
              fullWidth
              id="email"
              placeholder="Enter email address here"
              name="email"
              autoComplete="email"
              autoFocus
              value={email}
              onChange={(e) => {
                setInvalidCredentials(false);
                setEmailEmpty(false);
                setEmail(e.target.value);
              }}
              className={styles.inputField}
              InputProps={{
                classes: { root: styles.inputRoot, input: styles.input },
              }}
            />
          </div>
          <div className={styles.inputWrapper}>
            <label htmlFor="password" className={styles.inputLabel}>
              Password
              {passwordEmpty && <span className={styles.errorText}> Password required</span>}
            </label>
            <TextField
              variant="outlined"
              fullWidth
              name="password"
              placeholder="Enter a strong password here"
              type={showPassword ? "text" : "password"}
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => {
                setInvalidCredentials(false);
                setPasswordEmpty(false);
                setPassword(e.target.value);
              }}
              className={styles.inputField}
              InputProps={{
                classes: { root: styles.inputRoot, input: styles.input },
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
          <Link href="#" className={styles.forgotPasswordLink}>
            Forgot Password?
          </Link>
        </Box>
      </Box>
    </div>
  );
};

export default Login;