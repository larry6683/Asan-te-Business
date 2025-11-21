import React, { useEffect, useState } from "react";
import { 
  Box, 
  Typography, 
  Button, 
  Paper, 
  Avatar, 
  Divider, 
  CircularProgress, 
  Card, 
  CardContent, 
  Grid,
  Chip
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import PersonIcon from '@mui/icons-material/Person';
import BusinessIcon from '@mui/icons-material/Business';
import VolunteerActivismIcon from '@mui/icons-material/VolunteerActivism';
import EmailIcon from '@mui/icons-material/Email';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import LanguageIcon from '@mui/icons-material/Language';
import { grpcService } from "../api/grpcService";

// ✅ Import Logout Dependencies
import { logoutUser } from "../authentication/logoutUser";
import { AsanteUsersUserPool } from "../user-auth/asanteUsersUserPool"; 

const UserProfile = () => {
  const navigate = useNavigate();
  
  const user = useSelector((state) => state.user) || JSON.parse(sessionStorage.getItem("asante:user") || "{}");
  const [entityData, setEntityData] = useState(null);
  const [loading, setLoading] = useState(true);

  // ✅ ADDED: Handle Logout Logic
  const handleLogout = () => {
    console.log("Logging out from Profile...");
    
    const performLocalLogout = () => {
      sessionStorage.clear(); // Clear all session data
      navigate("/"); // Redirect to Login
    };

    if (user.email) {
      logoutUser(
        AsanteUsersUserPool, 
        user.email, 
        (msg) => {
          console.log("Cognito Logout Success:", msg);
          performLocalLogout();
        },
        (err) => {
          console.error("Cognito Logout Error:", err);
          performLocalLogout(); // Force logout locally even if API fails
        }
      );
    } else {
      performLocalLogout();
    }
  };

  useEffect(() => {
    const fetchEntityDetails = async () => {
      const token = sessionStorage.getItem("asante:accessJwt");
      const businessId = sessionStorage.getItem("asante:businessId");
      const beneficiaryId = sessionStorage.getItem("asante:beneficiaryId");

      try {
        if (businessId) {
          const response = await grpcService.getBusiness(businessId, token);
          const business = response.getBusiness();
          
          setEntityData({
            type: "Business",
            role: "Administrator",
            name: business.getBusinessName(),
            description: business.getBusinessDescription(),
            city: business.getLocationCity(),
            state: business.getLocationState(),
            website: business.getWebsiteUrl(),
            size: business.getBusinessSize()
          });
        } else if (beneficiaryId) {
          const response = await grpcService.getBeneficiary(beneficiaryId, token);
          const beneficiary = response.getBeneficiary();
          
          setEntityData({
            type: "Non-Profit",
            role: "Administrator",
            name: beneficiary.getBeneficiaryName(),
            description: beneficiary.getBeneficiaryDescription(),
            city: beneficiary.getLocationCity(),
            state: beneficiary.getLocationState(),
            website: beneficiary.getWebsiteUrl(),
            size: beneficiary.getBeneficiarySize()
          });
        }
      } catch (error) {
        console.error("Error fetching entity details:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchEntityDetails();
  }, []);

  return (
    <Box sx={{ p: 4, display: "flex", flexDirection: "column", alignItems: "center", backgroundColor: "#F4F6F8", minHeight: "100vh" }}>
      
      <Paper 
        elevation={3} 
        sx={{ 
          maxWidth: 800, 
          width: "100%", 
          borderRadius: "20px", 
          overflow: "hidden",
          mb: 4 
        }}
      >
        {/* Header Section */}
        <Box sx={{ 
          background: "linear-gradient(to right, #6271AE, #9ACDDA)", 
          p: 4, 
          display: "flex", 
          alignItems: "center",
          color: "white"
        }}>
          <Avatar sx={{ width: 80, height: 80, bgcolor: "white", color: "#6271AE", mr: 3 }}>
            <PersonIcon sx={{ fontSize: 50 }} />
          </Avatar>
          <Box>
            <Typography variant="h4" fontWeight="bold">
              {user.email ? user.email.split('@')[0] : "User Profile"}
            </Typography>
            <Typography variant="subtitle1" sx={{ opacity: 0.9, display: "flex", alignItems: "center", gap: 1 }}>
              <EmailIcon fontSize="small" /> {user.email}
            </Typography>
          </Box>
        </Box>

        {/* Content Section */}
        <Box sx={{ p: 4 }}>
          {loading ? (
            <Box display="flex" justifyContent="center" p={4}>
              <CircularProgress />
            </Box>
          ) : entityData ? (
            <Grid container spacing={4}>
              <Grid item xs={12}>
                <Card variant="outlined" sx={{ borderRadius: "15px" }}>
                  <CardContent>
                    <Box display="flex" justifyContent="space-between" alignItems="flex-start">
                      <Box display="flex" alignItems="center" gap={2} mb={2}>
                        <Avatar sx={{ bgcolor: entityData.type === 'Business' ? '#e3f2fd' : '#e8f5e9', color: entityData.type === 'Business' ? '#1976d2' : '#2e7d32' }}>
                          {entityData.type === 'Business' ? <BusinessIcon /> : <VolunteerActivismIcon />}
                        </Avatar>
                        <Box>
                          <Typography variant="h5" fontWeight="bold">{entityData.name}</Typography>
                          <Chip label={entityData.type} size="small" color={entityData.type === 'Business' ? "primary" : "success"} variant="outlined" />
                        </Box>
                      </Box>
                    </Box>

                    <Divider sx={{ my: 2 }} />

                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="body2" color="textSecondary">Description</Typography>
                        <Typography variant="body1" paragraph>
                          {entityData.description || "No description provided."}
                        </Typography>
                      </Grid>
                      
                      <Grid item xs={12} sm={6}>
                        <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
                          <Box>
                            <Typography variant="body2" color="textSecondary">Location</Typography>
                            <Typography variant="body1" display="flex" alignItems="center" gap={1}>
                              <LocationOnIcon fontSize="small" color="action"/> 
                              {entityData.city}, {entityData.state}
                            </Typography>
                          </Box>
                          
                          {entityData.website && (
                            <Box>
                              <Typography variant="body2" color="textSecondary">Website</Typography>
                              <Typography variant="body1" display="flex" alignItems="center" gap={1}>
                                <LanguageIcon fontSize="small" color="action"/> 
                                <a href={entityData.website} target="_blank" rel="noreferrer" style={{ color: "#6271AE", textDecoration: "none" }}>
                                  {entityData.website}
                                </a>
                              </Typography>
                            </Box>
                          )}

                          <Box>
                            <Typography variant="body2" color="textSecondary">Organization Size</Typography>
                            <Typography variant="body1">{entityData.size}</Typography>
                          </Box>
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          ) : (
            <Typography variant="body1" color="textSecondary" align="center">
              No organization linked to this account.
            </Typography>
          )}

          {/* ✅ Action Buttons */}
          <Box mt={4} display="flex" justifyContent="center" gap={2}>
            <Button 
              variant="contained" 
              onClick={() => navigate('/home')}
              sx={{ 
                borderRadius: "28px", 
                textTransform: "none",
                px: 4,
                py: 1,
                background: "linear-gradient(to right, #6271AE, #9ACDDA)"
              }}
            >
              Back to Dashboard
            </Button>

            {/* Logout Button */}
            <Button 
              variant="outlined" 
              onClick={handleLogout}
              sx={{ 
                borderRadius: "28px", 
                textTransform: "none",
                px: 4,
                py: 1,
                borderColor: "#6271AE",
                color: "#6271AE",
                "&:hover": {
                  backgroundColor: "#F5F5F5",
                  borderColor: "#5B6BB0",
                },
              }}
            >
              Logout
            </Button>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default UserProfile;