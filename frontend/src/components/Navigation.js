import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box, Tabs, Tab } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { Description, Assessment, Chat } from '@mui/icons-material';

const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const getTabValue = () => {
    if (location.pathname === '/') return 0;
    if (location.pathname === '/swot') return 1;
    if (location.pathname === '/chatbot') return 2;
    return 0;
  };

  const handleChange = (event, newValue) => {
    const routes = ['/', '/swot', '/chatbot'];
    navigate(routes[newValue]);
  };

  return (
    <AppBar position="sticky" sx={{ mb: 3 }}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 0, mr: 4, fontWeight: 'bold' }}>
          🎯 마케팅 AI 어시스턴트
        </Typography>

        <Tabs
          value={getTabValue()}
          onChange={handleChange}
          textColor="inherit"
          indicatorColor="secondary"
          sx={{ flexGrow: 1 }}
        >
          <Tab
            icon={<Description />}
            iconPosition="start"
            label="상세페이지 생성"
            sx={{ color: 'white', '&.Mui-selected': { color: 'white' } }}
          />
          <Tab
            icon={<Assessment />}
            iconPosition="start"
            label="SWOT + 3C 분석"
            sx={{ color: 'white', '&.Mui-selected': { color: 'white' } }}
          />
          <Tab
            icon={<Chat />}
            iconPosition="start"
            label="마케팅 챗봇"
            sx={{ color: 'white', '&.Mui-selected': { color: 'white' } }}
          />
        </Tabs>

        <Box>
          <Typography variant="caption" sx={{ opacity: 0.8 }}>
            v2.0
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navigation;
