import { createSlice } from "@reduxjs/toolkit";

export const businessProfileFormSlice = createSlice({
  name: "businessProfileForm",
  initialState: {
    selected:
      sessionStorage.getItem("asante:businessProfileForm") ||
      JSON.stringify({
        businessName: "",
        email: "",
        website: "",
        phoneNumber: "",
        locationCity: "",
        locationState: "",
        socialMedia: "",
        ein: "",
        teamMemberEmail: "",
      }),
  },
  reducers: {
    setBusinessProfileForm: (state, action) => {
      let json = JSON.stringify(action.payload.selected);
      state.selected = json;
      sessionStorage.setItem("asante:businessProfileForm", json);
    },
  },
});

export const { setBusinessProfileForm: setBusinessProfileForm } =
  businessProfileFormSlice.actions;

export default businessProfileFormSlice.reducer;
