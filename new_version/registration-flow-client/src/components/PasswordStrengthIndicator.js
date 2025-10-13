import React from "react";
import styles from "./PasswordStrengthIndicator.module.css";
import { Typography } from "@mui/material";

const getPasswordStrength = (password) => {
  let strength = 0;
  if (password.length >= 8) strength += 1;
  if (/[A-Z]/.test(password)) strength += 1;
  if (/[0-9]/.test(password)) strength += 1;
  if (/[^A-Za-z0-9]/.test(password)) strength += 1;
  return strength;
};

const getStrengthLabel = (strength) => {
  switch (strength) {
    case 0:
      return "Very Weak";
    case 1:
      return "Weak";
    case 2:
      return "Fair";
    case 3:
      return "Good";
    case 4:
      return "Strong";
    default:
      return "Very Weak";
  }
};

const PasswordStrengthIndicator = ({ password }) => {
  const strength = getPasswordStrength(password);
  const strengthLabel = getStrengthLabel(strength);
  const isStrong = strength === 4;

  if (isStrong) return null; // Hide the indicator if the password is strong

  return (
    <div className={styles.strengthIndicatorContainer}>
      <Typography
        sx={{
          fontFamily: '"Helvetica Neue", sans-serif',
          fontSize: "18px",
          marginLeft: "8px",
          marginBottom: "8px",
          marginTop: "5px",
        }}
      >
        Password Strength:{" "}
        <span style={{ color: strength === 0 ? "red" : "green" }}>
          {strengthLabel}
        </span>
      </Typography>
      <div className={styles.strengthBars}>
        {[...Array(4)].map((_, index) => (
          <div
            key={index}
            style={{
              backgroundColor: index < strength ? "green" : "grey",
            }}
          />
        ))}
      </div>
      <ul className={styles.suggestions}>
        <li style={{ color: password.length >= 8 ? "green" : "grey" }}>
          Password is at least 8 characters
        </li>
        <li style={{ color: /[A-Z]/.test(password) ? "green" : "grey" }}>
          Include at least 1 UPPERCASE letter
        </li>
        <li style={{ color: /[0-9]/.test(password) ? "green" : "grey" }}>
          Include at least 1 number
        </li>
        <li style={{ color: /[^A-Za-z0-9]/.test(password) ? "green" : "grey" }}>
          Include Special Character
        </li>
      </ul>
    </div>
  );
};

export default PasswordStrengthIndicator;
