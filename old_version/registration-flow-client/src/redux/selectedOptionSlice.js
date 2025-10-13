import { createSlice } from "@reduxjs/toolkit";

export const selectedOptionSlice = createSlice({
  name: "selectedOption",
  initialState: {
    selected: sessionStorage.getItem("asante:selectedOption") || "",
    image: sessionStorage.getItem("asante:selectedImage") || "",
  },
  reducers: {
    setSelectedOption: (state, action) => {
      state.selected = action.payload.selected;
      state.image = action.payload.image;
      sessionStorage.setItem("asante:selectedOption", action.payload.selected);
      sessionStorage.setItem("asante:selectedImage", action.payload.image);
    },
  },
});

export const { setSelectedOption } = selectedOptionSlice.actions;

export default selectedOptionSlice.reducer;
