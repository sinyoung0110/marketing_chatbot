import React, { useState, useRef, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Card,
  CardContent,
  Avatar,
  IconButton,
  Chip,
  Grid,
  CircularProgress,
  Alert
} from '@mui/material';
import {
  Send,
  SmartToy,
  Person,
  Lightbulb,
  TrendingUp,
  AttachMoney,
  Description,
  Assessment,
  Chat,
  Info
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = 'http://localhost:8000';

const MarketingChatbot = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '안녕하세요! 저는 AI 마케팅 전략가입니다. 어떤 도움이 필요하신가요?\n\n💡 예시 질문:\n- "에어프라이어 감자칩 마케팅 전략 알려줘"\n- "가격 전략 추천해줘"\n- "SEO 키워드 추천해줘"',
      timestamp: new Date().toISOString()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [productContext, setProductContext] = useState(null);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 메시지 전송
  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await fetch(`${BACKEND_URL}/api/chatbot/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: inputMessage,
          history: messages.slice(-10),
          context: productContext
        })
      });

      const data = await response.json();

      const assistantMessage = {
        role: 'assistant',
        content: data.message,
        timestamp: data.timestamp,
        quick_actions: data.quick_actions
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('챗봇 오류:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: '죄송합니다. 오류가 발생했습니다: ' + error.message,
          timestamp: new Date().toISOString()
        }
      ]);
    }

    setLoading(false);
  };

  // 빠른 작업 실행
  const handleQuickAction = async (action) => {
    if (action === 'generate_page') {
      navigate('/');
      return;
    }

    if (action === 'analyze_swot') {
      navigate('/swot');
      return;
    }

    if (!productContext?.name) {
      alert('먼저 상품 정보를 설정하세요 (우측 상단)');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${BACKEND_URL}/api/chatbot/quick-action`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: action,
          product_info: { name: productContext.name, category: productContext.category }
        })
      });

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.result,
          timestamp: data.timestamp
        }
      ]);
    } catch (error) {
      console.error('빠른 작업 오류:', error);
    }

    setLoading(false);
  };

  // 추천 질문
  const suggestedQuestions = [
    '마케팅 전략을 알려줘',
    '타겟 고객은 누구일까?',
    '가격은 어떻게 설정해야 할까?',
    'SEO 키워드를 추천해줘'
  ];

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 2 }}>
        <Alert severity="info" icon={<Info />}>
          💡 <strong>팁:</strong> "🚀 통합 워크플로우"에서 프로젝트를 완료하면 해당 컨텍스트를 자동으로 불러와 상담할 수 있습니다!
        </Alert>
      </Box>

      <Grid container spacing={3}>
        {/* 채팅 영역 */}
        <Grid item xs={12} md={8}>
          <Paper elevation={3} sx={{ height: 'calc(100vh - 200px)', display: 'flex', flexDirection: 'column' }}>
            {/* 헤더 */}
            <Box sx={{ p: 2, bgcolor: 'primary.main', color: 'white', display: 'flex', alignItems: 'center' }}>
              <Chat sx={{ mr: 1 }} />
              <Box>
                <Typography variant="h6">
                  💬 AI 마케팅 전략가
                </Typography>
                <Typography variant="caption">
                  실시간 마케팅 조언 및 전략 제안
                </Typography>
              </Box>
            </Box>

            {/* 메시지 영역 */}
            <Box
              sx={{
                flexGrow: 1,
                overflow: 'auto',
                p: 2,
                bgcolor: '#f5f5f5'
              }}
            >
              {messages.map((msg, index) => (
                <Box
                  key={index}
                  sx={{
                    display: 'flex',
                    justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                    mb: 2
                  }}
                >
                  {msg.role === 'assistant' && (
                    <Avatar sx={{ bgcolor: 'primary.main', mr: 1 }}>
                      <SmartToy />
                    </Avatar>
                  )}

                  <Box
                    sx={{
                      maxWidth: '70%',
                      bgcolor: msg.role === 'user' ? 'primary.main' : 'white',
                      color: msg.role === 'user' ? 'white' : 'text.primary',
                      borderRadius: 2,
                      p: 2,
                      boxShadow: 1
                    }}
                  >
                    <Typography
                      variant="body1"
                      sx={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}
                    >
                      {msg.content}
                    </Typography>

                    {/* 빠른 작업 버튼 */}
                    {msg.quick_actions && msg.quick_actions.length > 0 && (
                      <Box sx={{ mt: 2 }}>
                        {msg.quick_actions.map((action) => (
                          <Chip
                            key={action}
                            label={
                              action === 'generate_page'
                                ? '상세페이지 생성 →'
                                : action === 'analyze_swot'
                                ? 'SWOT 분석 →'
                                : action === 'suggest_keywords'
                                ? '키워드 추천'
                                : action === 'price_strategy'
                                ? '가격 전략'
                                : '타겟 분석'
                            }
                            onClick={() => handleQuickAction(action)}
                            sx={{ mr: 1, mt: 1 }}
                            color="primary"
                            variant="outlined"
                          />
                        ))}
                      </Box>
                    )}

                    <Typography variant="caption" sx={{ display: 'block', mt: 1, opacity: 0.7 }}>
                      {new Date(msg.timestamp).toLocaleTimeString()}
                    </Typography>
                  </Box>

                  {msg.role === 'user' && (
                    <Avatar sx={{ bgcolor: 'secondary.main', ml: 1 }}>
                      <Person />
                    </Avatar>
                  )}
                </Box>
              ))}

              {loading && (
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: 'primary.main', mr: 1 }}>
                    <SmartToy />
                  </Avatar>
                  <Box sx={{ bgcolor: 'white', borderRadius: 2, p: 2 }}>
                    <CircularProgress size={20} />
                    <Typography variant="body2" sx={{ ml: 1, display: 'inline' }}>
                      생각 중...
                    </Typography>
                  </Box>
                </Box>
              )}

              <div ref={messagesEndRef} />
            </Box>

            {/* 입력 영역 */}
            <Box sx={{ p: 2, bgcolor: 'white', borderTop: 1, borderColor: 'divider' }}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <TextField
                  fullWidth
                  placeholder="메시지를 입력하세요..."
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                  multiline
                  maxRows={3}
                />
                <IconButton
                  color="primary"
                  onClick={handleSendMessage}
                  disabled={loading || !inputMessage.trim()}
                  sx={{ alignSelf: 'flex-end' }}
                >
                  <Send />
                </IconButton>
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* 사이드바 */}
        <Grid item xs={12} md={4}>
          <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              💡 추천 질문
            </Typography>
            {suggestedQuestions.map((q, idx) => (
              <Button
                key={idx}
                variant="outlined"
                fullWidth
                sx={{ mb: 1, justifyContent: 'flex-start' }}
                onClick={() => setInputMessage(q)}
              >
                {q}
              </Button>
            ))}
          </Paper>

          <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              🚀 빠른 작업
            </Typography>

            <Button
              variant="contained"
              fullWidth
              startIcon={<Lightbulb />}
              onClick={() => handleQuickAction('suggest_keywords')}
              sx={{ mb: 1 }}
            >
              키워드 추천
            </Button>

            <Button
              variant="contained"
              fullWidth
              startIcon={<AttachMoney />}
              onClick={() => handleQuickAction('price_strategy')}
              sx={{ mb: 1 }}
            >
              가격 전략
            </Button>

            <Button
              variant="contained"
              fullWidth
              startIcon={<TrendingUp />}
              onClick={() => handleQuickAction('analyze_target')}
              sx={{ mb: 1 }}
            >
              타겟 분석
            </Button>

            <Button
              variant="outlined"
              fullWidth
              startIcon={<Description />}
              onClick={() => navigate('/')}
              sx={{ mb: 1 }}
            >
              상세페이지 생성하기
            </Button>

            <Button
              variant="outlined"
              fullWidth
              startIcon={<Assessment />}
              onClick={() => navigate('/swot')}
            >
              SWOT 분석하기
            </Button>
          </Paper>

          <Paper elevation={3} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              📦 상품 정보
            </Typography>

            <TextField
              fullWidth
              size="small"
              label="상품명"
              value={productContext?.name || ''}
              onChange={(e) =>
                setProductContext({ ...productContext, name: e.target.value })
              }
              sx={{ mb: 1 }}
            />

            <TextField
              fullWidth
              size="small"
              label="카테고리"
              value={productContext?.category || ''}
              onChange={(e) =>
                setProductContext({ ...productContext, category: e.target.value })
              }
            />

            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
              * 빠른 작업 사용 시 필요합니다
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default MarketingChatbot;
