import { CognitoUser } from "amazon-cognito-identity-js";

export const resendAuthenticationCode = (email, userPool) => {
  const cognitoUserData = {
    Username: email,
    Pool: userPool,
  };
  const cognitoUser = new CognitoUser(cognitoUserData);
  cognitoUser.resendConfirmationCode((error) => {
    // console.log("error resending confirmation code", error);
  });
};
