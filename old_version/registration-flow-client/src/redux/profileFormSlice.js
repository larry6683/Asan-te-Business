import { createSlice } from "@reduxjs/toolkit";

export const profileFormSlice = createSlice({
  name: "profileForm",
  initialState: {
    selected:
      sessionStorage.getItem("asante:profileForm") ||
      JSON.stringify({
        name: "",
        email: "",
        website: "",
        phoneNumber: "",
        locationCity: "",
        locationState: "",
        socialMedia: "",
        shopUrl: "",
        teamMemberEmail: "",
        ein: ""
      }),
  },
  reducers: {
    setProfileForm: (state, action) => {
      let json = JSON.stringify(action.payload.selected);
      state.selected = json;
      sessionStorage.setItem("asante:profileForm", json);
    },
  },
});

export const { setProfileForm: setProfileForm } =
  profileFormSlice.actions;

export default profileFormSlice.reducer;
