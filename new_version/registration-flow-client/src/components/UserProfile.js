import React, { useEffect, useState } from "react";
import { 
  Box, Typography, Button, Paper, Avatar, Divider, CircularProgress, 
  Card, CardContent, Grid, Chip, Stack, useTheme, useMediaQuery
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
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import LogoutIcon from '@mui/icons-material/Logout';
import ContactMailIcon from '@mui/icons-material/ContactMail';
import { grpcService } from "../api/grpcService";
import styles from "./UserProfile.module.css";

const UserProfile = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
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
          const causesList = entity.getCausesList ? entity.getCausesList() : [];
          const socialsList = entity.getSocialMediaLinksList ? entity.getSocialMediaLinksList() : [];

          setEntityData({
            type: type,
            name: type === "Business" ? entity.getBusinessName() : entity.getBeneficiaryName(),
            email: entity.getEmail(),
            description: type === "Business" ? entity.getBusinessDescription() : entity.getBeneficiaryDescription(),
            city: entity.getLocationCity(),
            state: entity.getLocationState(),
            website: entity.getWebsiteUrl(),
            size: type === "Business" ? entity.getBusinessSize() : entity.getBeneficiarySize(),
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
    <div className={styles.pageContainer}>
      <Paper elevation={0} className={styles.profileCard}>
        
        {/* Header Section */}
        <div className={styles.header}>
          <Grid container alignItems="center" spacing={3}>
            <Grid item>
              <Avatar className={styles.avatarContainer}>
                <PersonIcon sx={{ fontSize: { xs: 40, md: 60 } }} />
              </Avatar>
            </Grid>
            <Grid item xs>
              <Typography variant={isMobile ? "h5" : "h3"} fontWeight="800" sx={{ letterSpacing: "-0.5px" }}>
                {user.email || "User Profile"}
              </Typography>
              
              {entityData?.email && (
                <div className={styles.emailTag}>
                  <ContactMailIcon fontSize="small" />
                  <Typography variant="body2" fontWeight="500">
                    {entityData.type}: {entityData.email}
                  </Typography>
                </div>
              )}
            </Grid>
            
            {/* Desktop Buttons */}
            {!isMobile && (
              <Grid item>
                <Stack direction="row" spacing={2}>
                  <Button 
                    variant="contained" 
                    startIcon={<ArrowBackIcon />}
                    onClick={() => navigate('/home')}
                    className={`${styles.actionButton} ${styles.headerActions}`}
                  >
                    Dashboard
                  </Button>
                  <Button 
                    variant="contained" 
                    startIcon={<LogoutIcon />}
                    onClick={handleLogout}
                    className={`${styles.actionButton} ${styles.logoutButton}`}
                  >
                    Logout
                  </Button>
                </Stack>
              </Grid>
            )}
          </Grid>
        </div>

        <Box className={styles.contentSection}>
          {loading ? (
            <Box display="flex" justifyContent="center" p={8}>
              <CircularProgress size={60} thickness={4} sx={{ color: "#6271AE" }} />
            </Box>
          ) : entityData ? (
            <Grid container spacing={4}>
              {/* Main Content Column */}
              <Grid item xs={12} md={8}>
                <Box mb={4}>
                  <div className={styles.entityHeader}>
                    <Avatar 
                      className={styles.entityAvatar}
                      sx={{ 
                        bgcolor: entityData.type === 'Business' ? '#e3f2fd' : '#e8f5e9', 
                        color: entityData.type === 'Business' ? '#1976d2' : '#2e7d32' 
                      }}
                    >
                      {entityData.type === 'Business' ? <BusinessIcon fontSize="large" /> : <VolunteerActivismIcon fontSize="large" />}
                    </Avatar>
                    <Box>
                      <Typography variant="h4" fontWeight="bold" color="#333">{entityData.name}</Typography>
                      <Chip 
                        label={entityData.type} 
                        size="small" 
                        sx={{ mt: 0.5, fontWeight: 600, bgcolor: entityData.type === 'Business' ? '#e3f2fd' : '#e8f5e9', color: entityData.type === 'Business' ? '#1976d2' : '#2e7d32' }} 
                      />
                    </Box>
                  </div>
                  
                  <Card variant="outlined" className={styles.descriptionCard}>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" gutterBottom fontWeight="600" color="text.primary">About</Typography>
                      <Typography variant="body1" color="text.secondary" sx={{ lineHeight: 1.7 }}>
                        {entityData.description || "No description provided for this organization."}
                      </Typography>
                    </CardContent>
                  </Card>
                </Box>

                {entityData.causes && entityData.causes.length > 0 && (
                  <Box mb={4}>
                    <Typography variant="h6" gutterBottom fontWeight="600" color="text.primary" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <FavoriteIcon color="error" fontSize="small"/> Causes & Categories
                    </Typography>
                    <Box display="flex" flexWrap="wrap" gap={1.5}>
                      {entityData.causes.map((cause, idx) => (
                        <Chip 
                          key={idx} 
                          label={cause.name} 
                          className={styles.chipCustom}
                          sx={{ 
                            bgcolor: cause.rank === "PRIMARY" ? "rgba(98, 113, 174, 0.1)" : "transparent",
                            border: "1px solid",
                            borderColor: cause.rank === "PRIMARY" ? "#6271AE" : "#e0e0e0",
                            color: cause.rank === "PRIMARY" ? "#6271AE" : "text.secondary"
                          }} 
                        />
                      ))}
                    </Box>
                  </Box>
                )}
              </Grid>

              {/* Sidebar Info Column */}
              <Grid item xs={12} md={4}>
                <div className={styles.sidebar}>
                  <Typography variant="h6" fontWeight="700" mb={3} color="#6271AE">Details</Typography>
                  
                  <Stack spacing={3}>
                    <Box>
                      <Typography variant="caption" fontWeight="bold" color="text.secondary" textTransform="uppercase">Location</Typography>
                      <Typography variant="body1" fontWeight="500" display="flex" alignItems="center" gap={1} mt={0.5}>
                        <LocationOnIcon fontSize="small" sx={{ color: "#6271AE" }}/> {entityData.city}, {entityData.state}
                      </Typography>
                    </Box>

                    <Divider light />

                    <Box>
                      <Typography variant="caption" fontWeight="bold" color="text.secondary" textTransform="uppercase">Organization Size</Typography>
                      <Typography variant="body1" fontWeight="500" mt={0.5}>
                        {entityData.size}
                      </Typography>
                    </Box>

                    <Divider light />

                    {/* Links Section */}
                    <Box>
                      <Typography variant="caption" fontWeight="bold" color="text.secondary" textTransform="uppercase">Connect</Typography>
                      <Stack spacing={1.5} mt={1}>
                        {entityData.website && (
                          <Button 
                            href={entityData.website} 
                            target="_blank" 
                            startIcon={<LanguageIcon />}
                            className={styles.linkButton}
                          >
                            Website
                          </Button>
                        )}
                        
                        {entityData.shopUrl && (
                          <Button 
                            href={entityData.shopUrl} 
                            target="_blank" 
                            variant="contained"
                            startIcon={<StorefrontIcon />}
                            className={styles.shopButton}
                          >
                            Visit Shop
                          </Button>
                        )}

                        {entityData.socialMedia && entityData.socialMedia.map((link, idx) => (
                          <Button 
                            key={idx}
                            href={link} 
                            target="_blank" 
                            startIcon={<ShareIcon />}
                            className={styles.linkButton}
                          >
                            Social Media
                          </Button>
                        ))}
                      </Stack>
                    </Box>
                  </Stack>
                </div>
              </Grid>
            </Grid>
          ) : (
            <Paper sx={{ p: 6, textAlign: "center", borderRadius: "20px", bgcolor: "#fafafa", border: "2px dashed #e0e0e0" }}>
              <Typography variant="h6" color="textSecondary">No organization profile linked yet.</Typography>
              <Button variant="contained" sx={{ mt: 2, borderRadius: "20px" }} onClick={() => navigate('/home')}>
                Go to Dashboard
              </Button>
            </Paper>
          )}

          {/* Mobile Action Buttons */}
          {isMobile && (
            <Box mt={4} display="flex" flexDirection="column" gap={2}>
              <Button variant="outlined" fullWidth onClick={() => navigate('/home')} className={styles.actionButton}>
                Back to Dashboard
              </Button>
              <Button variant="contained" fullWidth onClick={handleLogout} className={`${styles.actionButton} ${styles.logoutButton}`}>
                Logout
              </Button>
            </Box>
          )}
        </Box>
      </Paper>
    </div>
  );
};

export default UserProfile;