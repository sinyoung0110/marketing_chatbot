import React, { useState, useRef, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Box,
  Avatar,
  IconButton,
  Chip,
  CircularProgress,
  Button
} from '@mui/material';
import {
  Send,
  SmartToy,
  Person,
  Lightbulb,
  TrendingUp,
  AttachMoney,
  Visibility
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const BACKEND_URL = 'http://localhost:8000';

const MarketingChatbot = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '안녕하세요. SellFlow AI 마케팅 전략 어시스턴트입니다.\n\n상품 마케팅 전략, 키워드 분석, 가격 전략 등 마케팅 관련 모든 질문에 답변드리겠습니다. 무엇을 도와드릴까요?',
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

  const loadSessionContext = async (sessionId, isInitialLoad = true) => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/unified/session/${sessionId}`);
      if (response.ok) {
        const data = await response.json();
        setSessionContext(data);

        // 초기 로드일 때만 환영 메시지 설정 (대화 중에는 메시지 유지)
        if (isInitialLoad) {
          setMessages([{
            role: 'assistant',
            content: `"${data.product_info?.product_name}" 프로젝트 컨텍스트를 불러왔습니다.\n\nSWOT 분석: ${data.has_swot ? '완료' : '미완료'}\n상세페이지: ${data.has_detail ? '완료' : '미완료'}\n\n프로젝트 정보를 바탕으로 마케팅 전략을 제안해드리겠습니다. 무엇을 도와드릴까요?`,
            timestamp: new Date().toISOString(),
            showQuickActions: true
          }]);
        }
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
    { id: 'suggest_keywords', label: '키워드 추천', icon: <Lightbulb /> },
    { id: 'price_strategy', label: '가격 전략', icon: <AttachMoney /> },
    { id: 'analyze_target', label: '타겟 분석', icon: <TrendingUp /> }
  ];

  const navigationActions = [
    { id: 'go_unified', label: '통합 워크플로우', path: '/' },
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
          session_context: sessionContext, // 세션 컨텍스트 전달
          session_id: sessionContext?.session_id // 세션 ID 전달
        })
      });

      if (!response.ok) {
        throw new Error('서버 응답 오류');
      }

      const data = await response.json();

      // HTML URL이 포함된 응답인 경우 html_url과 action_type도 저장
      const newMessage = {
        role: 'assistant',
        content: data.response || data.message || '응답을 생성할 수 없습니다.',
        timestamp: data.timestamp || new Date().toISOString(),
        html_url: data.html_url, // HTML URL 저장
        action_type: data.action_type // 액션 타입 저장
      };

      setMessages((prev) => [...prev, newMessage]);

      // 세션 컨텍스트 새로고침 (상세페이지가 업데이트된 경우) - 메시지는 유지
      if (data.action_type === 'detail_page_updated' && sessionContext?.session_id) {
        await loadSessionContext(sessionContext.session_id, false); // isInitialLoad = false
      }
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

  const handleViewDocument = (type) => {
    if (type === 'swot' && sessionContext?.swot_result?.html_url) {
      window.open(`${BACKEND_URL}${sessionContext.swot_result.html_url}`, '_blank');
    } else if (type === 'detail' && sessionContext?.detail_result?.html_url) {
      window.open(`${BACKEND_URL}${sessionContext.detail_result.html_url}`, '_blank');
    }
  };

  return (
    <Container maxWidth="lg" sx={{ bgcolor: 'background.default', minHeight: 'calc(100vh - 200px)', py: 3 }}>
      <Paper elevation={3} sx={{ height: 'calc(100vh - 200px)', display: 'flex', flexDirection: 'column', bgcolor: 'background.paper' }}>
        {/* 헤더 */}
        <Box sx={{ p: 2, bgcolor: 'primary.main', color: 'white', display: 'flex', alignItems: 'center' }}>
          <SmartToy sx={{ mr: 1 }} />
          <Box>
            <Typography variant="h6">SellFlow AI 마케팅 전략 어시스턴트</Typography>
            <Typography variant="caption">실시간 마케팅 전략 분석 및 최적화 솔루션</Typography>
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
              <Paper sx={{ p: 2, bgcolor: 'white', '& .MuiAlert-icon': { color: 'primary.main' } }}>
                <Typography variant="subtitle2" gutterBottom color="primary.main" fontWeight={600}>
                  추천 질문
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
                    bgcolor: msg.role === 'user' ? 'background.default' : 'white',
                    color: msg.role === 'user' ? 'text.primary' : 'text.primary',
                    borderRadius: 2,
                    p: 2,
                    boxShadow: 1,
                    border: msg.role === 'user' ? '1px solid' : 'none',
                    borderColor: msg.role === 'user' ? 'divider' : 'transparent'
                  }}
                >
                  <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                    {msg.content}
                  </Typography>

                  {/* 첫 메시지에 빠른 작업 버튼 */}
                  {index === 0 && msg.showQuickActions && (
                    <Box sx={{ mt: 2, borderTop: 1, borderColor: 'divider', pt: 2 }}>
                      <Typography variant="caption" color="primary.main" gutterBottom display="block" fontWeight={600}>
                        빠른 작업
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

                      {/* 생성된 문서가 있으면 보기/수정 버튼 표시 */}
                      {sessionContext && (sessionContext.swot_result || sessionContext.detail_result) && (
                        <>
                          <Typography variant="caption" color="text.secondary" gutterBottom display="block" sx={{ mt: 2 }}>
                            📄 생성된 문서
                          </Typography>
                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                            {sessionContext.swot_result && (
                              <Button
                                size="small"
                                startIcon={<Visibility />}
                                onClick={() => handleViewDocument('swot')}
                                variant="outlined"
                                color="success"
                              >
                                SWOT 분석서 보기
                              </Button>
                            )}
                            {sessionContext.detail_result && (
                              <Button
                                size="small"
                                startIcon={<Visibility />}
                                onClick={() => handleViewDocument('detail')}
                                variant="outlined"
                                color="success"
                              >
                                상세페이지 보기
                              </Button>
                            )}
                          </Box>
                        </>
                      )}

                      <Typography variant="caption" color="primary.main" gutterBottom display="block" fontWeight={600}>
                        다른 기능으로 이동
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

              {/* HTML 링크가 있으면 버튼 표시 */}
              {msg.role === 'assistant' && msg.html_url && (
                <Box sx={{ display: 'flex', justifyContent: 'flex-start', mt: 1, ml: 6 }}>
                  <Button
                    variant="contained"
                    color="success"
                    size="small"
                    startIcon={<Visibility />}
                    onClick={() => window.open(`${BACKEND_URL}${msg.html_url}`, '_blank')}
                  >
                    📄 생성된 HTML 보기
                  </Button>
                </Box>
              )}
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
