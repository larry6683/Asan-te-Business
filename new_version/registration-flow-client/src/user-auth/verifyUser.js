import { CognitoUser } from "amazon-cognito-identity-js";
import { AsanteUsersUserPool } from "./asanteUsersUserPool";

export const verifyUser = (email, code, successCallback, errorCallback) => {
  if (AsanteUsersUserPool) {
    const cognitoUser = new CognitoUser({
      Username: email,
      Pool: AsanteUsersUserPool,
    });

    cognitoUser.confirmRegistration(code, true, (err, result) => {
      if (err) {
        // ✅ FIXED: Only call error callback, NOT success callback
        console.error("Verification failed:", err);
        if (errorCallback) errorCallback(err);
      } else {
        console.log("Verification successful:", result);
        if (successCallback) successCallback();
      }
    });
  }
};