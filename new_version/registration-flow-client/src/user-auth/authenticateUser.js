import { authenticateUser } from "../authentication/authenticateUser.js";
import {
  createUserDataFromIdTokenPayload,
  setUserDataInStorage,
} from "../authentication/userData.js";
import { AsanteUsersUserPool } from "./asanteUsersUserPool.js";

export const getUserAuthenticationTokenAndSaveInStorage = (
  email,
  password,
  successCallback,
  errorCallback,
) => {
  const userpool = AsanteUsersUserPool;
  let success = false;
  authenticateUser(
    userpool,
    email,
    password,
    (result) => {
      const idToken = result.getIdToken();
      const refreshToken = result.getRefreshToken();
      const accessToken = result.getAccessToken();
      // console.log(idToken.getJwtToken());
      // console.log(accessToken.getJwtToken())
      setAccessJwtInStorage(accessToken.getJwtToken());
      setRefreshTokenInStorage(refreshToken.getToken());

      const userData = createUserDataFromIdTokenPayload(idToken.payload);
      setUserDataInStorage(userData);
      if (successCallback) successCallback(userData);
    },
    (error) => {
      success = false;
      if (errorCallback) errorCallback(error);
    },
  );
  return success;
};

export const setAccessJwtInStorage = (jwt) => {
  // console.log(jwt);
  sessionStorage.setItem("asante:accessJwt", jwt);
};

export const getAccessJwtFromStorage = () => {
  return sessionStorage.getItem("asante:accessJwt", "");
};

export const setRefreshTokenInStorage = (refreshToken) => {
  sessionStorage.setItem("asante:refreshToken", refreshToken);
};

export const getRefreshTokenFromStorage = () => {
  return sessionStorage.getItem("asante:refreshToken", "");
};
