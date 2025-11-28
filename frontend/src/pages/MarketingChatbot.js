import React, { useState, useRef, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Avatar,
  IconButton,
  Chip,
  CircularProgress,
  Alert,
  Collapse
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
  Info,
  ExpandMore,
  ExpandLess
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = 'http://localhost:8000';

const MarketingChatbot = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '안녕하세요! 저는 AI 마케팅 전략가입니다. 어떤 도움이 필요하신가요?',
      timestamp: new Date().toISOString(),
      showQuickActions: true
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [sessionContext, setSessionContext] = useState(null);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  // 세션 ID를 로컬스토리지에서 가져오기 (통합 워크플로우에서 저장)
  useEffect(() => {
    const savedSessionId = localStorage.getItem('current_session_id');
    if (savedSessionId) {
      loadSessionContext(savedSessionId);
    }
  }, []);

  const loadSessionContext = async (sessionId) => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/unified/session/${sessionId}`);
      if (response.ok) {
        const data = await response.json();
        setSessionContext(data);

        // 환영 메시지 업데이트
        setMessages([{
          role: 'assistant',
          content: `안녕하세요! "${data.product_info?.product_name}" 프로젝트의 마케팅 전략가입니다.\n\n✅ SWOT 분석: ${data.has_swot ? '완료' : '미완료'}\n✅ 상세페이지: ${data.has_detail ? '완료' : '미완료'}\n\n프로젝트 정보를 바탕으로 상담해드리겠습니다. 무엇이 궁금하신가요?`,
          timestamp: new Date().toISOString(),
          showQuickActions: true
        }]);
      }
    } catch (error) {
      console.log('세션 로드 실패 (무시):', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const suggestedQuestions = [
    '마케팅 전략을 알려줘',
    '타겟 고객은 누구일까?',
    '가격은 어떻게 설정해야 할까?',
    'SEO 키워드를 추천해줘'
  ];

  const quickActions = [
    { id: 'suggest_keywords', label: '💡 키워드 추천', icon: <Lightbulb /> },
    { id: 'price_strategy', label: '💰 가격 전략', icon: <AttachMoney /> },
    { id: 'analyze_target', label: '📊 타겟 분석', icon: <TrendingUp /> }
  ];

  const navigationActions = [
    { id: 'go_unified', label: '🚀 통합 워크플로우', path: '/' },
    { id: 'go_detail', label: '📝 상세페이지 생성', path: '/detail' },
    { id: 'go_swot', label: '📊 SWOT 분석', path: '/swot' }
  ];

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = inputMessage;
    setInputMessage('');
    setShowSuggestions(false);

    setMessages((prev) => [
      ...prev,
      {
        role: 'user',
        content: userMessage,
        timestamp: new Date().toISOString()
      }
    ]);

    setLoading(true);

    try {
      const response = await fetch(`${BACKEND_URL}/api/chatbot/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          conversation_history: messages.map((m) => ({
            role: m.role,
            content: m.content
          })),
          session_context: sessionContext // 세션 컨텍스트 전달
        })
      });

      if (!response.ok) {
        throw new Error('서버 응답 오류');
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.response || data.message || '응답을 생성할 수 없습니다.',
          timestamp: data.timestamp || new Date().toISOString()
        }
      ]);
    } catch (error) {
      console.error('챗봇 오류:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: '죄송합니다. 오류가 발생했습니다. 다시 시도해주세요.',
          timestamp: new Date().toISOString()
        }
      ]);
    }

    setLoading(false);
  };

  const handleQuickAction = (actionId) => {
    setInputMessage(
      actionId === 'suggest_keywords' ? '키워드 추천해줘' :
      actionId === 'price_strategy' ? '가격 전략 추천해줘' :
      '타겟 고객 분석해줘'
    );
  };

  const handleNavigation = (path) => {
    navigate(path);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 2 }}>
        <Alert severity="info" icon={<Info />}>
          💡 <strong>팁:</strong> "🚀 통합 워크플로우"에서 프로젝트를 완료하면 해당 컨텍스트를 자동으로 불러와 상담할 수 있습니다!
        </Alert>
      </Box>

      <Paper elevation={3} sx={{ height: 'calc(100vh - 200px)', display: 'flex', flexDirection: 'column' }}>
        {/* 헤더 */}
        <Box sx={{ p: 2, bgcolor: 'primary.main', color: 'white', display: 'flex', alignItems: 'center' }}>
          <Chat sx={{ mr: 1 }} />
          <Box>
            <Typography variant="h6">💬 AI 마케팅 전략가</Typography>
            <Typography variant="caption">실시간 마케팅 조언 및 전략 제안</Typography>
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
          {/* 추천 질문 (처음에만 표시) */}
          {messages.length === 1 && showSuggestions && (
            <Box sx={{ mb: 3 }}>
              <Paper sx={{ p: 2, bgcolor: 'white' }}>
                <Typography variant="subtitle2" gutterBottom color="text.secondary">
                  💡 추천 질문
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {suggestedQuestions.map((q, idx) => (
                    <Chip
                      key={idx}
                      label={q}
                      onClick={() => setInputMessage(q)}
                      variant="outlined"
                      sx={{ cursor: 'pointer' }}
                    />
                  ))}
                </Box>
              </Paper>
            </Box>
          )}

          {/* 메시지들 */}
          {messages.map((msg, index) => (
            <Box key={index} sx={{ mb: 2 }}>
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'
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
                  <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                    {msg.content}
                  </Typography>

                  {/* 첫 메시지에 빠른 작업 버튼 */}
                  {index === 0 && msg.showQuickActions && (
                    <Box sx={{ mt: 2, borderTop: 1, borderColor: 'divider', pt: 2 }}>
                      <Typography variant="caption" color="text.secondary" gutterBottom display="block">
                        🚀 빠른 작업
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                        {quickActions.map((action) => (
                          <Chip
                            key={action.id}
                            label={action.label}
                            onClick={() => handleQuickAction(action.id)}
                            color="primary"
                            variant="outlined"
                            sx={{ cursor: 'pointer' }}
                          />
                        ))}
                      </Box>

                      <Typography variant="caption" color="text.secondary" gutterBottom display="block">
                        📍 다른 기능으로 이동
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                        {navigationActions.map((action) => (
                          <Chip
                            key={action.id}
                            label={action.label}
                            onClick={() => handleNavigation(action.path)}
                            color="secondary"
                            variant="outlined"
                            sx={{ cursor: 'pointer' }}
                          />
                        ))}
                      </Box>
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
            </Box>
          ))}

          {loading && (
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Avatar sx={{ bgcolor: 'primary.main', mr: 1 }}>
                <SmartToy />
              </Avatar>
              <Box sx={{ bgcolor: 'white', borderRadius: 2, p: 2, display: 'flex', alignItems: 'center' }}>
                <CircularProgress size={20} />
                <Typography variant="body2" sx={{ ml: 1 }}>
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
    </Container>
  );
};

export default MarketingChatbot;
