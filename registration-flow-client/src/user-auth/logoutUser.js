import { AsanteUsersUserPool } from "./asanteUsersUserPool";
import { logoutUser } from "../authentication/logoutUser";
import { clearStore } from "../redux/store";
import {
  getUserDataFromStorage,
  setUserDataInStorage,
} from "../authentication/userData";

export const logoutCurrentUser = (successCallback, errorCallback) => {
  const userData = getUserDataFromStorage();
  if (userData && userData.email) {
    const email = userData.email;
    logoutUser(
      AsanteUsersUserPool,
      email,
      (message) => {
        // console.log("logoutSuccess");
        clearStore(true);
        successCallback(message);
      },
      (error) => {
        // console.error("logoutError", error);
        // automatically clear session storage just in case..
        setUserDataInStorage(null);
        clearStore(true);
        errorCallback(error);
      },
    );
  } else {
    errorCallback();
  }
};
