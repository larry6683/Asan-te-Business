import React from "react";
import { Box, Typography, Button, Paper } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";

const UserProfile = () => {
  const navigate = useNavigate();
  // Try to get user from Redux or Session
  const user = useSelector((state) => state.user) || JSON.parse(sessionStorage.getItem("asante:user") || "{}");

  return (
    <Box sx={{ p: 4, display: "flex", flexDirection: "column", alignItems: "center", mt: 8 }}>
      <Paper elevation={3} sx={{ p: 4, maxWidth: 600, width: "100%", textAlign: "center", borderRadius: "20px" }}>
        <Typography variant="h4" gutterBottom sx={{ color: "#6271AE", fontWeight: "bold" }}>
          User Profile
        </Typography>
        
        <Typography variant="h6" sx={{ mt: 2 }}>
          Welcome back,
        </Typography>
        
        <Typography variant="body1" sx={{ fontSize: "1.2rem", color: "#555", mb: 4 }}>
          {user.email || "User"}
        </Typography>

        <Button 
          variant="outlined" 
          onClick={() => navigate('/home')}
          sx={{ borderRadius: "20px", textTransform: "none" }}
        >
          Back to Home
        </Button>
      </Paper>
    </Box>
  );
};

export default UserProfile;