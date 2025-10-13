export class AuthenticationToken {
  constructor(id_token, jwtToken, expiration, refresh_token) {
    this.id_token = id_token;
    this.access_token = {
      jwtToken: jwtToken,
      expiration: expiration,
    };
    this.refresh_token = refresh_token;
  }
}

export const getTokenFromStorage = () => {
  const authTokenJson = sessionStorage.getItem("asante:authToken");
  if (authTokenJson) {
    try {
      const authTokenObject = JSON.parse(authTokenJson);
      return new AuthenticationToken(
        authTokenObject["id_token"],
        authTokenObject["access_token"]["jwtToken"],
        authTokenObject["access_token"]["expiration"],
        authTokenObject["refresh_token"],
      );
    } catch {}
  }
  // unable to get / parse token
  return null;
};

export const setTokenInStorage = (authToken) => {
  const authTokenJson = JSON.stringify(authToken);
  sessionStorage.setItem("asante:authToken", authTokenJson);
};
