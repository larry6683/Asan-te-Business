import { createSlice } from "@reduxjs/toolkit";

export const selectedSizeSlice = createSlice({
  name: "selectedSize",
  initialState: {
    selected: sessionStorage.getItem("asante:selectedSize") || "",
  },
  reducers: {
    setSelectedSize: (state, action) => {
      state.selected = action.payload;
      sessionStorage.setItem("asante:selectedSize", action.payload.selected);
    },
  },
});

export const { setSelectedSize: setSelectedSize } = selectedSizeSlice.actions;

export default selectedSizeSlice.reducer;
