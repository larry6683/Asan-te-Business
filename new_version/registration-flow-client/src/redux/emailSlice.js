import { createSlice } from "@reduxjs/toolkit";

export const emailSlice = createSlice({
  name: "email",
  initialState: {
    address: sessionStorage.getItem("asante:emailId") || "",
  },
  reducers: {
    setEmailID: (state, action) => {
      state.address = action.payload;
      sessionStorage.setItem("asante:emailId", action.payload);
    },
  },
});

export const { setEmailID } = emailSlice.actions;

export default emailSlice.reducer;
