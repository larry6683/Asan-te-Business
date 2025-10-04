export class UserData {
  constructor(
    sub,
    cognitoUsername,
    email,
    emailVerified,
    mailingListSignup,
    userType,
  ) {
    this.sub = sub;
    this.cognitoUsername = cognitoUsername;
    this.email = email;
    this.emailVerified = emailVerified;
    this.mailingListSignup = mailingListSignup;
    this.userType = userType;
  }
}

export const createUserDataFromIdTokenPayload = (payload) => {
  return new UserData(
    payload.sub,
    payload["cognito:username"],
    payload.email,
    payload.email_verified,
    payload["custom:mailing_list_signup"],
    payload["custom:user_type"],
  );
};

export const setUserDataInStorage = (userData) => {
  const json = JSON.stringify(userData);
  sessionStorage.setItem("asante:userData", json);
};

export const getUserDataFromStorage = () => {
  JSON.parse(sessionStorage.getItem("asante:userData"), {});
};
