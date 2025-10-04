import { createSlice } from "@reduxjs/toolkit";

export const beneficiaryProfileFormSlice = createSlice({
  name: "beneficiaryProfileForm",
  initialState: {
    selected:
      sessionStorage.getItem("asante:beneficiaryProfileForm") ||
      JSON.stringify({
        beneficiaryName: "",
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
    setBeneficiaryProfileForm: (state, action) => {
      let json = JSON.stringify(action.payload.selected);
      state.selected = json;
      sessionStorage.setItem("asante:beneficiaryProfileForm", json);
    },
  },
});

export const { setBeneficiaryProfileForm: setBeneficiaryProfileForm } =
  beneficiaryProfileFormSlice.actions;

export default beneficiaryProfileFormSlice.reducer;
