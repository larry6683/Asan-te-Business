import { CognitoUser } from "amazon-cognito-identity-js";

export const logoutUser = (userPool, email, successCallback, errorCallback) => {
  const cognitoUserData = {
    Username: email,
    Pool: userPool,
  };
  const cognitoUser = new CognitoUser(cognitoUserData);
  try {
    cognitoUser.globalSignOut({
      onSuccess: (message) => successCallback(message),
      onFailure: (error) => errorCallback(error),
    });
  } catch (e) {
    if (errorCallback) errorCallback(e);
  }
};
