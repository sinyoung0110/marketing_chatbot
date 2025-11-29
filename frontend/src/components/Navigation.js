import React from 'react';
import { AppBar, Toolbar, Typography, Box, Tabs, Tab } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { Chat, TrendingUp } from '@mui/icons-material';

const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // 통합 플랫폼('/')와 챗봇('/chatbot')만 남김
  const getTabValue = () => {
    if (location.pathname === '/') return 0;
    if (location.pathname === '/chatbot') return 1;
    return 0;
  };

  const handleChange = (event, newValue) => {
    const routes = ['/', '/chatbot'];
    navigate(routes[newValue]);
  };

  return (
    <AppBar position="sticky" sx={{ mb: 3 }}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 0, mr: 4, fontWeight: 'bold', color: 'primary.main' }}>
          SellFlow AI
        </Typography>

        <Tabs
          value={getTabValue()}
          onChange={handleChange}
          textColor="primary"
          indicatorColor="primary"
          sx={{ flexGrow: 1 }}
        >
          <Tab
            icon={<TrendingUp />}
            iconPosition="start"
            label="통합 워크플로우"
            sx={{ color: 'text.primary', fontWeight: 'bold', '&.Mui-selected': { color: 'primary.main' } }}
          />
          <Tab
            icon={<Chat />}
            iconPosition="start"
            label="챗봇"
            sx={{ color: 'text.primary', '&.Mui-selected': { color: 'primary.main' } }}
          />
        </Tabs>

        <Box>
          <Typography variant="caption" sx={{ opacity: 0.8, color: 'text.secondary' }}>
            v2.0
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navigation;
