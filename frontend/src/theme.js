/**
 * Deep Green Theme Configuration
 */
export const deepGreenTheme = {
  colors: {
    bg: '#fafdfb',          // 전체 배경 (약간 따뜻한 화이트)
    surface: '#ffffff',     // 카드/섹션 배경
    text: '#0f1720',        // 기본 텍스트 (다크 네이비 느낌)
    muted: '#6b7280',       // 보조 텍스트
    border: '#e6eef0',      // 라인
    theme: '#0f766e',       // 딥그린 메인
    accent: '#115e59',      // 호버/강조 컬러
    danger: '#d9534f',      // 경고/에러
    success: '#059669',     // 성공
    warning: '#f59e0b'      // 경고
  },

  typography: {
    fontFamily: "'Pretendard', 'Noto Sans KR', sans-serif",
    h1: { fontSize: '28px', fontWeight: 700 },
    h2: { fontSize: '22px', fontWeight: 700 },
    h3: { fontSize: '18px', fontWeight: 600 },
    body: { fontSize: '16px', lineHeight: 1.6 }
  },

  spacing: {
    xs: '8px',
    sm: '12px',
    md: '16px',
    lg: '24px',
    xl: '32px'
  },

  borderRadius: {
    sm: '8px',
    md: '10px',
    lg: '12px'
  },

  shadow: {
    card: '0 6px 18px rgba(15,118,110,0.03)',
    hover: '0 8px 24px rgba(15,118,110,0.08)'
  }
};

export const globalStyles = `
  :root {
    --bg: ${deepGreenTheme.colors.bg};
    --surface: ${deepGreenTheme.colors.surface};
    --text: ${deepGreenTheme.colors.text};
    --muted: ${deepGreenTheme.colors.muted};
    --border: ${deepGreenTheme.colors.border};
    --theme: ${deepGreenTheme.colors.theme};
    --accent: ${deepGreenTheme.colors.accent};
    --danger: ${deepGreenTheme.colors.danger};
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: ${deepGreenTheme.typography.fontFamily};
    line-height: 1.6;
  }
`;
