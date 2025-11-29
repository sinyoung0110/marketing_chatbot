import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Box,
  Typography
} from '@mui/material';
import Navigation from './components/Navigation';
import DetailPageGenerator from './pages/DetailPageGenerator';
import SwotAnalyzer from './pages/SwotAnalyzer';
import MarketingChatbot from './pages/MarketingChatbot';
import UnifiedWorkflow from './pages/UnifiedWorkflow';

const theme = createTheme({
  palette: {
    primary: {
      main: '#0f766e',  // 딥그린 메인
      light: '#14b8a6',
      dark: '#115e59',  // 호버/강조 컬러
    },
    secondary: {
      main: '#0f766e',
      light: '#14b8a6',
      dark: '#115e59',
    },
    success: {
      main: '#0f766e',
      light: '#14b8a6',
    },
    error: {
      main: '#d9534f',  // 경고/에러
    },
    background: {
      default: '#fafdfb',  // 전체 배경 (약간 따뜻한 화이트)
      paper: '#ffffff',    // 카드/섹션 배경
    },
    text: {
      primary: '#0f1720',   // 기본 텍스트 (다크 네이비 느낌)
      secondary: '#6b7280', // 보조 텍스트
    },
    divider: '#e6eef0',  // 라인
  },
  typography: {
    fontFamily: '"Pretendard", "Noto Sans KR", sans-serif',
    h1: {
      fontSize: '28px',
      fontWeight: 700,
      color: '#0f1720',
      margin: '0 0 12px',
    },
    h2: {
      fontSize: '22px',
      fontWeight: 700,
      color: '#0f1720',
      margin: '0 0 12px',
    },
    h3: {
      fontSize: '18px',
      fontWeight: 700,
      color: '#0f1720',
      margin: '0 0 12px',
    },
    body1: {
      fontSize: '16px',
      margin: '10px 0',
      color: '#0f1720',
      lineHeight: 1.6,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '10px',
          textTransform: 'none',
          fontWeight: 700,
          padding: '12px 20px',
          transition: 'background 0.15s',
        },
        contained: {
          boxShadow: 'none',
          '&:hover': {
            boxShadow: 'none',
            backgroundColor: '#115e59',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          boxShadow: '0 6px 18px rgba(15,118,110,0.03)',
          border: '1px solid #e6eef0',
          backgroundColor: '#ffffff',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#fafdfb',
          borderBottom: '1px solid #e6eef0',
          boxShadow: 'none',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: '10px',
            backgroundColor: '#fff',
            '& fieldset': {
              borderColor: '#e6eef0',
            },
          },
        },
      },
    },
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#fafdfb',
          color: '#0f1720',
          lineHeight: 1.6,
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', display: 'flex', flexDirection: 'column' }}>
          <Navigation />

          <Box sx={{ flex: 1 }}>
            <Routes>
              <Route path="/" element={<UnifiedWorkflow />} />
              <Route path="/detail" element={<DetailPageGenerator />} />
              <Route path="/swot" element={<SwotAnalyzer />} />
              <Route path="/chatbot" element={<MarketingChatbot />} />
            </Routes>
          </Box>

          {/* Footer */}
          <Box sx={{
            bgcolor: 'background.paper',
            borderTop: '1px solid',
            borderColor: 'divider',
            py: 3,
            px: 3,
            mt: 5
          }}>
            <Typography variant="body2" color="text.secondary" align="center" sx={{ fontSize: '14px' }}>
              © 2025 SellFlow AI - All rights reserved
            </Typography>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
