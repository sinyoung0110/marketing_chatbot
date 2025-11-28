import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Alert,
  CircularProgress,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import {
  PlayArrow,
  Assessment,
  Description,
  Chat,
  CheckCircle,
  ExpandMore,
  Lightbulb,
  TrendingUp,
  UploadFile
} from '@mui/icons-material';

const BACKEND_URL = 'http://localhost:8000';

const UnifiedWorkflow = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);

  // Step 0: 상품 정보
  const [productInfo, setProductInfo] = useState({
    product_name: '',
    category: '',
    keywords: '',
    target_customer: '',
    platforms: ['coupang', 'naver']
  });

  // Step 1: SWOT 결과
  const [swotResult, setSwotResult] = useState(null);
  const [swotOptions, setSwotOptions] = useState({
    search_depth: 'advanced',
    days: null,
    include_reviews: true
  });

  // Step 2: 상세페이지 결과
  const [detailResult, setDetailResult] = useState(null);
  const [detailOptions, setDetailOptions] = useState({
    platform: 'coupang',
    tone: '친근한',
    image_style: 'real'
  });

  // Step 0: 워크플로우 시작
  // 파일 업로드 처리
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        setProductInfo({
          product_name: data.product_name || data.name || '',
          category: data.category || '',
          keywords: Array.isArray(data.keywords) ? data.keywords.join(', ') : data.keywords || '',
          target_customer: data.target_customer || data.target || '',
          platforms: data.platforms || ['coupang', 'naver']
        });
        setUploadedFile(file.name);
        alert('✅ 파일이 성공적으로 로드되었습니다!');
      } catch (error) {
        alert('파일 형식이 올바르지 않습니다. JSON 형식이어야 합니다.');
      }
    };
    reader.readAsText(file);
  };

  const handleStart = async () => {
    if (!productInfo.product_name || !productInfo.category) {
      alert('상품명과 카테고리를 입력하세요');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/unified/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_name: productInfo.product_name,
          category: productInfo.category,
          keywords: productInfo.keywords.split(',').map(k => k.trim()).filter(k => k),
          target_customer: productInfo.target_customer,
          platforms: productInfo.platforms
        })
      });

      if (!response.ok) throw new Error('서버 오류');

      const data = await response.json();
      setSessionId(data.session_id);
      setActiveStep(1);
      console.log('세션 생성:', data);
    } catch (error) {
      alert('오류: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // Step 1: SWOT 분석 실행
  const handleExecuteSwot = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/unified/execute-swot`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          ...swotOptions
        })
      });

      if (!response.ok) throw new Error('SWOT 분석 실패');

      const data = await response.json();
      setSwotResult(data);
      setActiveStep(2);
      console.log('SWOT 완료:', data);
    } catch (error) {
      alert('SWOT 분석 오류: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // Step 2: 상세페이지 생성
  const handleExecuteDetail = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/unified/execute-detail`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          ...detailOptions
        })
      });

      if (!response.ok) throw new Error('상세페이지 생성 실패');

      const data = await response.json();
      setDetailResult(data);
      setActiveStep(3);
      console.log('상세페이지 완료:', data);
    } catch (error) {
      alert('상세페이지 생성 오류: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setActiveStep(0);
    setSessionId(null);
    setSwotResult(null);
    setDetailResult(null);
    setProductInfo({
      product_name: '',
      category: '',
      keywords: '',
      target_customer: '',
      platforms: ['coupang', 'naver']
    });
  };

  return (
    <Container maxWidth="lg">
      <Paper elevation={3} sx={{ p: 4, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <TrendingUp sx={{ fontSize: 40, mr: 2, color: 'primary.main' }} />
          <Box>
            <Typography variant="h4" gutterBottom>
              🚀 통합 워크플로우
            </Typography>
            <Typography variant="body2" color="text.secondary">
              한 번 입력하면 SWOT 분석 → 상세페이지 생성 → 챗봇 상담까지 자동!
            </Typography>
          </Box>
        </Box>

        {sessionId && (
          <Alert severity="success" sx={{ mb: 2 }}>
            <strong>세션 ID:</strong> {sessionId}
          </Alert>
        )}

        {/* 프로그레스 */}
        {loading && <LinearProgress sx={{ mb: 2 }} />}

        <Stepper activeStep={activeStep} orientation="vertical">
          {/* Step 0: 상품 정보 입력 */}
          <Step>
            <StepLabel
              icon={<Lightbulb />}
              optional={<Typography variant="caption">한 번만 입력!</Typography>}
            >
              상품 정보 입력
            </StepLabel>
            <StepContent>
              <Box sx={{ mb: 2 }}>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="상품명 *"
                      value={productInfo.product_name}
                      onChange={(e) =>
                        setProductInfo({ ...productInfo, product_name: e.target.value })
                      }
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="카테고리 *"
                      value={productInfo.category}
                      onChange={(e) =>
                        setProductInfo({ ...productInfo, category: e.target.value })
                      }
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="키워드 (쉼표로 구분)"
                      value={productInfo.keywords}
                      onChange={(e) =>
                        setProductInfo({ ...productInfo, keywords: e.target.value })
                      }
                      placeholder="건강, 바삭, 저칼로리"
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="타겟 고객"
                      value={productInfo.target_customer}
                      onChange={(e) =>
                        setProductInfo({ ...productInfo, target_customer: e.target.value })
                      }
                      placeholder="20-30대 헬스족"
                    />
                  </Grid>
                </Grid>

                <Alert severity="info" sx={{ mt: 2 }}>
                  💡 이 정보는 모든 단계에서 자동으로 사용됩니다. 다시 입력할 필요 없습니다!
                </Alert>

                {/* 파일 업로드 옵션 */}
                <Accordion sx={{ mt: 2 }}>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <UploadFile sx={{ mr: 1 }} />
                      <Typography>파일로 정보 업로드 (선택)</Typography>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Alert severity="info" sx={{ mb: 2 }}>
                      JSON 형식의 파일을 업로드하면 자동으로 입력됩니다.<br/>
                      예시: {`{ "product_name": "에어프라이어 감자칩", "category": "간식", "keywords": ["건강", "바삭"], "target_customer": "20-30대" }`}
                    </Alert>
                    <Button
                      variant="outlined"
                      component="label"
                      startIcon={<UploadFile />}
                      fullWidth
                    >
                      JSON 파일 선택
                      <input
                        type="file"
                        hidden
                        accept=".json"
                        onChange={handleFileUpload}
                      />
                    </Button>
                    {uploadedFile && (
                      <Alert severity="success" sx={{ mt: 1 }}>
                        ✅ {uploadedFile} 로드 완료
                      </Alert>
                    )}
                  </AccordionDetails>
                </Accordion>
              </Box>

              <Button
                variant="contained"
                onClick={handleStart}
                disabled={loading}
                startIcon={<PlayArrow />}
                size="large"
              >
                시작하기
              </Button>
            </StepContent>
          </Step>

          {/* Step 1: SWOT 분석 */}
          <Step>
            <StepLabel icon={<Assessment />}>SWOT + 3C 분석</StepLabel>
            <StepContent>
              <Box sx={{ mb: 2 }}>
                <Alert severity="success" sx={{ mb: 2 }}>
                  ✅ 상품 정보가 자동으로 로드되었습니다!
                  <br />
                  <strong>{productInfo.product_name}</strong> ({productInfo.category})
                </Alert>

                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Typography>고급 옵션</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Grid container spacing={2}>
                      <Grid item xs={12} md={4}>
                        <TextField
                          select
                          fullWidth
                          size="small"
                          label="검색 상세도"
                          value={swotOptions.search_depth}
                          onChange={(e) =>
                            setSwotOptions({ ...swotOptions, search_depth: e.target.value })
                          }
                          SelectProps={{ native: true }}
                        >
                          <option value="basic">기본</option>
                          <option value="advanced">상세 (권장)</option>
                        </TextField>
                      </Grid>
                      <Grid item xs={12} md={4}>
                        <TextField
                          select
                          fullWidth
                          size="small"
                          label="검색 기간"
                          value={swotOptions.days || ''}
                          onChange={(e) =>
                            setSwotOptions({
                              ...swotOptions,
                              days: e.target.value ? parseInt(e.target.value) : null
                            })
                          }
                          SelectProps={{ native: true }}
                        >
                          <option value="">전체</option>
                          <option value="30">최근 30일</option>
                          <option value="90">최근 90일</option>
                        </TextField>
                      </Grid>
                    </Grid>
                  </AccordionDetails>
                </Accordion>

                {swotResult && (
                  <Card sx={{ mt: 2, bgcolor: 'success.light' }}>
                    <CardContent>
                      <Typography variant="h6" sx={{ color: 'white', mb: 1 }}>
                        ✅ SWOT 분석 완료!
                      </Typography>
                      <Typography variant="body2" sx={{ color: 'white' }}>
                        {swotResult.competitor_count}개의 경쟁사 상품을 분석했습니다
                      </Typography>
                      <Button
                        variant="contained"
                        color="inherit"
                        sx={{ mt: 2 }}
                        onClick={() => window.open(`${BACKEND_URL}${swotResult.html_url}`, '_blank')}
                      >
                        분석 보고서 열기
                      </Button>
                    </CardContent>
                  </Card>
                )}
              </Box>

              <Box sx={{ display: 'flex', gap: 2 }}>
                {!swotResult ? (
                  <Button
                    variant="contained"
                    color="success"
                    onClick={handleExecuteSwot}
                    disabled={loading}
                    startIcon={<Assessment />}
                    size="large"
                  >
                    SWOT 분석 실행
                  </Button>
                ) : (
                  <>
                    <Button
                      variant="outlined"
                      onClick={() => {
                        const url = swotResult.html_url.startsWith('http')
                          ? swotResult.html_url
                          : `${BACKEND_URL}${swotResult.html_url}`;
                        window.open(url, '_blank');
                      }}
                      size="large"
                    >
                      분석 결과 다시 보기
                    </Button>
                    <Button
                      variant="contained"
                      onClick={() => setActiveStep(2)}
                      startIcon={<Description />}
                      size="large"
                    >
                      다음 단계
                    </Button>
                  </>
                )}
              </Box>
            </StepContent>
          </Step>

          {/* Step 2: 상세페이지 생성 */}
          <Step>
            <StepLabel icon={<Description />}>상세페이지 생성</StepLabel>
            <StepContent>
              <Box sx={{ mb: 2 }}>
                <Alert severity="success" sx={{ mb: 2 }}>
                  ✅ SWOT 분석 결과가 자동으로 반영됩니다!
                  <br />
                  경쟁사 리뷰 인사이트, 강점 키워드 등이 자동으로 활용됩니다.
                </Alert>

                <Grid container spacing={2}>
                  <Grid item xs={12} md={4}>
                    <TextField
                      select
                      fullWidth
                      label="플랫폼"
                      value={detailOptions.platform}
                      onChange={(e) =>
                        setDetailOptions({ ...detailOptions, platform: e.target.value })
                      }
                      SelectProps={{ native: true }}
                    >
                      <option value="coupang">쿠팡</option>
                      <option value="naver">네이버</option>
                    </TextField>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <TextField
                      select
                      fullWidth
                      label="톤앤매너"
                      value={detailOptions.tone}
                      onChange={(e) =>
                        setDetailOptions({ ...detailOptions, tone: e.target.value })
                      }
                      SelectProps={{ native: true }}
                    >
                      <option value="친근한">친근한</option>
                      <option value="전문적">전문적</option>
                      <option value="감성적">감성적</option>
                    </TextField>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <TextField
                      select
                      fullWidth
                      label="이미지 스타일"
                      value={detailOptions.image_style}
                      onChange={(e) =>
                        setDetailOptions({ ...detailOptions, image_style: e.target.value })
                      }
                      SelectProps={{ native: true }}
                    >
                      <option value="real">사실적</option>
                      <option value="minimal">미니멀</option>
                      <option value="vibrant">화려한</option>
                    </TextField>
                  </Grid>
                </Grid>

                {detailResult && (
                  <Card sx={{ mt: 2, bgcolor: 'success.light' }}>
                    <CardContent>
                      <Typography variant="h6" sx={{ color: 'white', mb: 1 }}>
                        ✅ 상세페이지 생성 완료!
                      </Typography>
                      <Grid container spacing={1} sx={{ mt: 1 }}>
                        <Grid item xs={12} md={6}>
                          <Button
                            variant="contained"
                            color="inherit"
                            fullWidth
                            onClick={() => window.open(`${BACKEND_URL}${detailResult.html_url}`, '_blank')}
                          >
                            HTML 보기
                          </Button>
                        </Grid>
                        <Grid item xs={12} md={6}>
                          <Button
                            variant="contained"
                            color="inherit"
                            fullWidth
                            onClick={() => window.open(`${BACKEND_URL}${detailResult.markdown_url}`, '_blank')}
                          >
                            Markdown 보기
                          </Button>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                )}
              </Box>

              <Box sx={{ display: 'flex', gap: 2 }}>
                {!detailResult ? (
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleExecuteDetail}
                    disabled={loading}
                    startIcon={<Description />}
                    size="large"
                  >
                    상세페이지 생성
                  </Button>
                ) : (
                  <>
                    <Button
                      variant="outlined"
                      onClick={() => window.open(`${BACKEND_URL}${detailResult.html_url}`, '_blank')}
                      size="large"
                    >
                      HTML 다시 보기
                    </Button>
                    <Button
                      variant="outlined"
                      onClick={() => window.open(`${BACKEND_URL}${detailResult.markdown_url}`, '_blank')}
                      size="large"
                    >
                      Markdown 다시 보기
                    </Button>
                    <Button
                      variant="contained"
                      onClick={() => setActiveStep(3)}
                      startIcon={<CheckCircle />}
                      size="large"
                    >
                      완료
                    </Button>
                  </>
                )}
              </Box>
            </StepContent>
          </Step>

          {/* Step 3: 완료 */}
          <Step>
            <StepLabel icon={<CheckCircle />}>완료!</StepLabel>
            <StepContent>
              <Alert severity="success" sx={{ mb: 2 }}>
                <Typography variant="h6" gutterBottom>
                  🎉 모든 단계가 완료되었습니다!
                </Typography>
                <Typography variant="body2">
                  • SWOT + 3C 분석 완료<br />
                  • 상세페이지 생성 완료<br />
                  • 이제 챗봇 탭에서 마케팅 전략 상담을 받아보세요!
                </Typography>
              </Alert>

              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button variant="contained" onClick={handleReset} size="large">
                  새 프로젝트 시작
                </Button>
                <Button
                  variant="outlined"
                  onClick={() => window.open('/chatbot', '_self')}
                  startIcon={<Chat />}
                  size="large"
                >
                  챗봇 상담하기
                </Button>
              </Box>
            </StepContent>
          </Step>
        </Stepper>

        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
            <CircularProgress />
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default UnifiedWorkflow;
