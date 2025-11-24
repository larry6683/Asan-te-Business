import { CognitoUser } from "amazon-cognito-identity-js";
import { AsanteUsersUserPool } from "./asanteUsersUserPool";

/**
 * Initiates the forgot password flow (sends verification code to email).
 * @param {string} email
 * @param {function} onSuccess
 * @param {function} onFailure
 */
export const initiateForgotPassword = (email, onSuccess, onFailure) => {
  const userData = {
    Username: email,
    Pool: AsanteUsersUserPool,
  };
  const cognitoUser = new CognitoUser(userData);

  cognitoUser.forgotPassword({
    onSuccess: function (data) {
      // successfully initiated
      if (onSuccess) onSuccess(data);
    },
    onFailure: function (err) {
      if (onFailure) onFailure(err);
    },
    // optional: inputVerificationCode is technically not needed here 
    // because we handle the second step manually in confirmPassword
  });
};

/**
 * Confirms the password reset using the verification code.
 * @param {string} email
 * @param {string} verificationCode
 * @param {string} newPassword
 * @param {function} onSuccess
 * @param {function} onFailure
 */
export const confirmForgotPassword = (
  email,
  verificationCode,
  newPassword,
  onSuccess,
  onFailure
) => {
  const userData = {
    Username: email,
    Pool: AsanteUsersUserPool,
  };
  const cognitoUser = new CognitoUser(userData);

  cognitoUser.confirmPassword(verificationCode, newPassword, {
    onSuccess: function () {
      if (onSuccess) onSuccess();
    },
    onFailure: function (err) {
      if (onFailure) onFailure(err);
    },
  });
};