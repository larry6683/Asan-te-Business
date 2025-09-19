import { createSlice } from "@reduxjs/toolkit";

export const userSlice = createSlice({
  name: "user",
  initialState: {
    user:
      sessionStorage.getItem("asante:user") ||
      JSON.stringify({
        id: "",
        email: "",
        userType: "",
      }),
  },
  reducers: {
    setUser: (state, action) => {
      // console.log("setuser");
      let json = JSON.stringify(action.payload);
      state.user = json;
      sessionStorage.setItem("asante:user", json);
      // console.log("userIdSlice", json);
    },
  },
});

export const { setUser: setUser } = userSlice.actions;

export default userSlice.reducer;
