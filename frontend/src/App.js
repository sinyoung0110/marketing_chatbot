import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Box
} from '@mui/material';
import Navigation from './components/Navigation';
import DetailPageGenerator from './pages/DetailPageGenerator';
import SwotAnalyzer from './pages/SwotAnalyzer';
import MarketingChatbot from './pages/MarketingChatbot';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#ff6b6b',
    },
    success: {
      main: '#4caf50',
    },
  },
  typography: {
    fontFamily: '"Noto Sans KR", "Roboto", "Arial", sans-serif',
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ minHeight: '100vh', bgcolor: '#f5f5f5' }}>
          <Navigation />

          <Routes>
            <Route path="/" element={<DetailPageGenerator />} />
            <Route path="/swot" element={<SwotAnalyzer />} />
            <Route path="/chatbot" element={<MarketingChatbot />} />
          </Routes>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
