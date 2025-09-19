import { createSlice } from "@reduxjs/toolkit";

export const selectedCausesSlice = createSlice({
  name: "selectedCauses",
  initialState: {
    selected: sessionStorage.getItem("asante:selectedCauses") || [],
  },
  reducers: {
    setSelectedCauses: (state, action) => {
      state.selected = action.payload;
      sessionStorage.setItem("asante:selectedCauses", action.payload.selected);
    },
  },
});

export const { setSelectedCauses: setSelectedCauses } =
  selectedCausesSlice.actions;

export default selectedCausesSlice.reducer;
