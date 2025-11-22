import React, { useEffect, useState } from 'react';
import { Box, Typography } from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';

const UserBanner = () => {
  const [email, setEmail] = useState('');

  useEffect(() => {
    const userStr = sessionStorage.getItem("asante:user");
    if (userStr) {
      try {
        const user = JSON.parse(userStr);
        setEmail(user.email);
      } catch (e) {
        console.error("Failed to parse user for banner", e);
      }
    }
  }, []);

  if (!email) return null;

  return (
    <Box 
      sx={{
        position: 'absolute',
        top: 10,
        left: '50%',
        transform: 'translateX(-50%)',
        backgroundColor: 'rgba(98, 113, 174, 0.1)', // Light purple tint
        padding: '4px 16px',
        borderRadius: '20px',
        display: 'flex',
        alignItems: 'center',
        gap: 1,
        zIndex: 1000 // Ensure it sits above other elements
      }}
    >
      <PersonIcon sx={{ fontSize: 16, color: '#6271AE' }} />
      <Typography variant="caption" sx={{ color: '#6271AE', fontWeight: 500 }}>
        Logged in as: {email}
      </Typography>
    </Box>
  );
};

export default UserBanner;