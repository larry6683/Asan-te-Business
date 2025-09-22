import React from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import store from "./redux/store";
import App from "./App";

// Get the root element from the DOM
const container = document.getElementById("root");

// Create a root using the container
const root = createRoot(container);

// Render your app
root.render(
  <Provider store={store}>
    <App />
  </Provider>,
);
