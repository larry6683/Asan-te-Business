import { configureStore } from "@reduxjs/toolkit";
import selectedOptionReducer from "./selectedOptionSlice";
import emailReducer from "./emailSlice";
import selectedSizeReducer from "./selectedSizeSlice";
import selectedCausesReducer from "./selectedCausesSlice";
// import businessProfileFormReducer from "./businessProfileFormSlice";
import profileFormReducer from "./profileFormSlice";

const store = configureStore({
  reducer: {
    email: emailReducer,
    selectedOption: selectedOptionReducer,
    selectedSize: selectedSizeReducer,
    selectedCauses: selectedCausesReducer,
    // businessProfileForm: businessProfileFormReducer,
    profileForm: profileFormReducer,
  },
});

export default store;

export const clearStore = (clearUser = false) => {
  if (clearUser) sessionStorage.removeItem("asante:userData");
  sessionStorage.removeItem("asante:selectedCauses");
  sessionStorage.removeItem("asante:selectedSize");
  sessionStorage.removeItem("asante:selectedOption");
  sessionStorage.removeItem("asante:emailId");
  // sessionStorage.removeItem("asante:businessProfileForm");
  sessionStorage.removeItem("asante:profileForm");
  sessionStorage.removeItem("asante:authToken");
  sessionStorage.removeItem("asante:userData");
  sessionStorage.removeItem("asante:businessId");
  sessionStorage.removeItem("asante:user");
  sessionStorage.removeItem("asante:accessJwt");
  sessionStorage.removeItem("asante:refreshToken")
};
