import { CognitoUser, AuthenticationDetails } from "amazon-cognito-identity-js";

export const authenticateUser = (
  userpool,
  email,
  password,
  successCallback,
  errorCallback,
  newPasswordrequiredCallback,
) => {
  const cognitoUserData = {
    Username: email,
    Pool: userpool,
  };
  const cognitoUser = new CognitoUser(cognitoUserData);
  const authenticationDetails = new AuthenticationDetails({
    Username: email,
    Password: password,
  });
  cognitoUser.authenticateUser(authenticationDetails, {
    onSuccess: (result) => successCallback(result),
    onFailure: (error) => errorCallback(error),
    newPasswordrequired: (data) => {
      if (newPasswordrequiredCallback) {
        newPasswordrequiredCallback(data);
      }
    },
  });
};
