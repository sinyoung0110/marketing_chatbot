import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box, Tabs, Tab } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { Description, Assessment, Chat, TrendingUp, AutoAwesome } from '@mui/icons-material';

const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const getTabValue = () => {
    if (location.pathname === '/') return 0;
    if (location.pathname === '/detail') return 1;
    if (location.pathname === '/swot') return 2;
    if (location.pathname === '/chatbot') return 3;
    return 0;
  };

  const handleChange = (event, newValue) => {
    const routes = ['/', '/detail', '/swot', '/chatbot'];
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
            sx={{
              color: 'text.primary',
              fontWeight: 'bold',
              '&.Mui-selected': { color: 'primary.main' }
            }}
          />
          <Tab
            icon={<Description />}
            iconPosition="start"
            label="상세페이지"
            sx={{ color: 'text.primary', '&.Mui-selected': { color: 'primary.main' } }}
          />
          <Tab
            icon={<Assessment />}
            iconPosition="start"
            label="SWOT 분석"
            sx={{ color: 'text.primary', '&.Mui-selected': { color: 'primary.main' } }}
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
