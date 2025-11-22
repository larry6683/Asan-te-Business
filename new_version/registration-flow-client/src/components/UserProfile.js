import React, { useEffect, useState } from "react";
import { 
  Box, Typography, Button, Paper, Avatar, Divider, CircularProgress, 
  Card, CardContent, Grid, Chip, Link as MuiLink, Stack
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import PersonIcon from '@mui/icons-material/Person';
import BusinessIcon from '@mui/icons-material/Business';
import VolunteerActivismIcon from '@mui/icons-material/VolunteerActivism';
import EmailIcon from '@mui/icons-material/Email';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import LanguageIcon from '@mui/icons-material/Language';
import StorefrontIcon from '@mui/icons-material/Storefront';
import ShareIcon from '@mui/icons-material/Share';
import FavoriteIcon from '@mui/icons-material/Favorite';
import { grpcService } from "../api/grpcService";
import { logoutUser } from "../authentication/logoutUser";
import { AsanteUsersUserPool } from "../user-auth/asanteUsersUserPool"; 

const UserProfile = () => {
  const navigate = useNavigate();
  
  const user = useSelector((state) => state.user) || JSON.parse(sessionStorage.getItem("asante:user") || "{}");
  const [entityData, setEntityData] = useState(null);
  const [loading, setLoading] = useState(true);

  const handleLogout = () => {
    sessionStorage.clear();
    window.location.href = "/";
  };

  useEffect(() => {
    const fetchEntityDetails = async () => {
      const token = sessionStorage.getItem("asante:accessJwt");
      const businessId = sessionStorage.getItem("asante:businessId");
      const beneficiaryId = sessionStorage.getItem("asante:beneficiaryId");

      try {
        let response, entity, type;
        if (businessId) {
          response = await grpcService.getBusiness(businessId, token);
          entity = response.getBusiness();
          type = "Business";
        } else if (beneficiaryId) {
          response = await grpcService.getBeneficiary(beneficiaryId, token);
          entity = response.getBeneficiary();
          type = "Non-Profit";
        }

        if (entity) {
          // Helper to safely get list
          const causesList = entity.getCausesList ? entity.getCausesList() : [];
          const socialsList = entity.getSocialMediaLinksList ? entity.getSocialMediaLinksList() : [];

          setEntityData({
            type: type,
            name: type === "Business" ? entity.getBusinessName() : entity.getBeneficiaryName(),
            description: type === "Business" ? entity.getBusinessDescription() : entity.getBeneficiaryDescription(),
            city: entity.getLocationCity(),
            state: entity.getLocationState(),
            website: entity.getWebsiteUrl(),
            size: type === "Business" ? entity.getBusinessSize() : entity.getBeneficiarySize(),
            
            // ✅ NEW FIELDS
            shopUrl: entity.getShopUrl(),
            socialMedia: socialsList,
            causes: causesList.map(c => ({ name: c.getName(), rank: c.getRank() }))
          });
        }
      } catch (error) {
        console.error("Error fetching details:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchEntityDetails();
  }, []);

  return (
    <Box sx={{ p: 4, display: "flex", flexDirection: "column", alignItems: "center", backgroundColor: "#F4F6F8", minHeight: "100vh" }}>
      <Paper elevation={3} sx={{ maxWidth: 900, width: "100%", borderRadius: "20px", overflow: "hidden", mb: 4 }}>
        
        {/* Header */}
        <Box sx={{ background: "linear-gradient(to right, #6271AE, #9ACDDA)", p: 4, display: "flex", alignItems: "center", color: "white" }}>
          <Avatar sx={{ width: 80, height: 80, bgcolor: "white", color: "#6271AE", mr: 3 }}>
            <PersonIcon sx={{ fontSize: 50 }} />
          </Avatar>
          <Box>
            <Typography variant="h4" fontWeight="bold">{user.email ? user.email.split('@')[0] : "User Profile"}</Typography>
            <Typography variant="subtitle1" sx={{ opacity: 0.9, display: "flex", alignItems: "center", gap: 1 }}>
              <EmailIcon fontSize="small" /> {user.email}
            </Typography>
          </Box>
        </Box>

        <Box sx={{ p: 4 }}>
          {loading ? (
            <Box display="flex" justifyContent="center" p={4}><CircularProgress /></Box>
          ) : entityData ? (
            <Grid container spacing={4}>
              <Grid item xs={12}>
                <Card variant="outlined" sx={{ borderRadius: "15px" }}>
                  <CardContent>
                    {/* Name & Type */}
                    <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                      <Box display="flex" alignItems="center" gap={2}>
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

                    <Grid container spacing={4}>
                      {/* Left Column: Description & Location */}
                      <Grid item xs={12} md={7}>
                        <Typography variant="subtitle2" color="textSecondary" gutterBottom>Description</Typography>
                        <Typography variant="body1" paragraph>
                          {entityData.description || "No description provided."}
                        </Typography>

                        <Typography variant="subtitle2" color="textSecondary" gutterBottom sx={{ mt: 2 }}>Location</Typography>
                        <Typography variant="body1" display="flex" alignItems="center" gap={1}>
                          <LocationOnIcon fontSize="small" color="action"/> {entityData.city}, {entityData.state}
                        </Typography>

                        {/* ✅ Causes Section */}
                        {entityData.causes && entityData.causes.length > 0 && (
                          <Box mt={3}>
                            <Typography variant="subtitle2" color="textSecondary" gutterBottom>Causes & Categories</Typography>
                            <Box display="flex" flexWrap="wrap" gap={1}>
                              {entityData.causes.map((cause, idx) => (
                                <Chip 
                                  key={idx} 
                                  icon={<FavoriteIcon fontSize="small" />} 
                                  label={cause.name} 
                                  size="small" 
                                  color="secondary" 
                                  variant={cause.rank === "PRIMARY" ? "filled" : "outlined"} 
                                />
                              ))}
                            </Box>
                          </Box>
                        )}
                      </Grid>
                      
                      {/* Right Column: Links & Contact */}
                      <Grid item xs={12} md={5}>
                        <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
                          
                          {/* Website */}
                          {entityData.website && (
                            <Box>
                              <Typography variant="subtitle2" color="textSecondary">Website</Typography>
                              <MuiLink href={entityData.website} target="_blank" rel="noreferrer" sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                                <LanguageIcon fontSize="small" /> {entityData.website}
                              </MuiLink>
                            </Box>
                          )}

                          {/* ✅ Store Link */}
                          {entityData.shopUrl && (
                            <Box>
                              <Typography variant="subtitle2" color="textSecondary">Online Store</Typography>
                              <MuiLink href={entityData.shopUrl} target="_blank" rel="noreferrer" sx={{ display: "flex", alignItems: "center", gap: 1, fontWeight: "bold", color: "#2e7d32" }}>
                                <StorefrontIcon fontSize="small" /> Visit Shop
                              </MuiLink>
                            </Box>
                          )}

                          {/* ✅ Social Media Links */}
                          {entityData.socialMedia && entityData.socialMedia.length > 0 && (
                            <Box>
                              <Typography variant="subtitle2" color="textSecondary">Social Media</Typography>
                              <Stack spacing={1}>
                                {entityData.socialMedia.map((link, idx) => (
                                  <MuiLink key={idx} href={link} target="_blank" rel="noreferrer" sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                                    <ShareIcon fontSize="small" /> {link}
                                  </MuiLink>
                                ))}
                              </Stack>
                            </Box>
                          )}

                          <Box>
                            <Typography variant="subtitle2" color="textSecondary">Size</Typography>
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
            <Typography variant="body1" color="textSecondary" align="center">No organization linked.</Typography>
          )}

          <Box mt={4} display="flex" justifyContent="center" gap={2}>
            <Button variant="contained" onClick={() => navigate('/home')} sx={{ borderRadius: "28px", textTransform: "none", px: 4 }}>
              Back to Dashboard
            </Button>
            <Button variant="outlined" onClick={handleLogout} sx={{ borderRadius: "28px", textTransform: "none", px: 4 }}>
              Logout
            </Button>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default UserProfile;