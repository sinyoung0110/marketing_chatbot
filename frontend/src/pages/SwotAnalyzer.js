import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  Box,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Checkbox,
  CircularProgress,
  Alert,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import {
  Search,
  Delete,
  Refresh,
  Assessment,
  Link as LinkIcon,
  ExpandMore,
  CheckCircle
} from '@mui/icons-material';

const BACKEND_URL = 'http://localhost:8000';

const SwotAnalyzer = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [platforms, setPlatforms] = useState(['coupang', 'naver']);
  const [searchResults, setSearchResults] = useState([]);
  const [excludedUrls, setExcludedUrls] = useState(new Set());
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [productInfo, setProductInfo] = useState({
    name: '',
    category: '',
    keywords: '',
    target: ''
  });

  // 검색 실행
  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/swot/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: searchQuery,
          platforms: platforms,
          max_results: 15
        })
      });

      const data = await response.json();
      setSearchResults(data.results || []);
      console.log('검색 완료:', data);
    } catch (error) {
      console.error('검색 오류:', error);
      alert('검색 실패: ' + error.message);
    }
    setLoading(false);
  };

  // URL 제외/포함 토글
  const toggleExclude = (url) => {
    const newExcluded = new Set(excludedUrls);
    if (newExcluded.has(url)) {
      newExcluded.delete(url);
    } else {
      newExcluded.add(url);
    }
    setExcludedUrls(newExcluded);
  };

  // 재검색
  const handleRefineSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/swot/refine-search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          original_query: searchQuery,
          refined_query: searchQuery,
          platforms: platforms,
          exclude_urls: Array.from(excludedUrls),
          max_results: 15
        })
      });

      const data = await response.json();
      setSearchResults(data.results || []);
      setExcludedUrls(new Set());
      console.log('재검색 완료:', data);
    } catch (error) {
      console.error('재검색 오류:', error);
      alert('재검색 실패: ' + error.message);
    }
    setLoading(false);
  };

  // SWOT 분석 실행
  const handleAnalyze = async () => {
    if (!productInfo.name || !productInfo.category) {
      alert('상품명과 카테고리를 입력하세요');
      return;
    }

    setLoading(true);
    try {
      const selectedResults = searchResults.filter(
        r => !excludedUrls.has(r.url)
      );

      const response = await fetch(`${BACKEND_URL}/api/swot/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_name: productInfo.name,
          category: productInfo.category,
          keywords: productInfo.keywords.split(',').map(k => k.trim()),
          target: productInfo.target,
          search_results: selectedResults
        })
      });

      const data = await response.json();
      setAnalysisResult(data);
      console.log('분석 완료:', data);
    } catch (error) {
      console.error('분석 오류:', error);
      alert('분석 실패: ' + error.message);
    }
    setLoading(false);
  };

  const platformOptions = [
    { value: 'coupang', label: '쿠팡' },
    { value: 'naver', label: '네이버' },
    { value: '11st', label: '11번가' }
  ];

  return (
    <Container maxWidth="xl">
      <Paper elevation={3} sx={{ p: 4, mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          📊 SWOT + 3C 분석기
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          경쟁사 상품을 검색하고, 결과를 수정하여 SWOT + 3C 분석을 수행합니다
        </Typography>

        <Grid container spacing={3}>
          {/* 검색 섹션 */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  1️⃣ 경쟁사 검색
                </Typography>

                <TextField
                  fullWidth
                  label="검색어 (예: 에어프라이어 감자칩)"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  sx={{ mb: 2 }}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" gutterBottom>
                    검색 플랫폼:
                  </Typography>
                  {platformOptions.map((platform) => (
                    <Chip
                      key={platform.value}
                      label={platform.label}
                      onClick={() => {
                        setPlatforms((prev) =>
                          prev.includes(platform.value)
                            ? prev.filter((p) => p !== platform.value)
                            : [...prev, platform.value]
                        );
                      }}
                      color={platforms.includes(platform.value) ? 'primary' : 'default'}
                      sx={{ mr: 1 }}
                    />
                  ))}
                </Box>

                <Button
                  variant="contained"
                  startIcon={<Search />}
                  onClick={handleSearch}
                  disabled={loading || !searchQuery}
                  fullWidth
                >
                  검색하기
                </Button>
              </CardContent>
            </Card>
          </Grid>

          {/* 검색 결과 */}
          {searchResults.length > 0 && (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6">
                      2️⃣ 검색 결과 ({searchResults.length}개)
                    </Typography>
                    <Button
                      size="small"
                      startIcon={<Refresh />}
                      onClick={handleRefineSearch}
                      disabled={loading || excludedUrls.size === 0}
                    >
                      제외하고 재검색 ({excludedUrls.size})
                    </Button>
                  </Box>

                  <Alert severity="info" sx={{ mb: 2 }}>
                    제외할 URL을 체크하고 '제외하고 재검색' 버튼을 클릭하세요
                  </Alert>

                  <List>
                    {searchResults.map((result, index) => (
                      <ListItem
                        key={index}
                        sx={{
                          bgcolor: excludedUrls.has(result.url) ? 'action.selected' : 'transparent',
                          borderRadius: 1,
                          mb: 1
                        }}
                      >
                        <Checkbox
                          checked={excludedUrls.has(result.url)}
                          onChange={() => toggleExclude(result.url)}
                        />
                        <ListItemText
                          primary={result.title}
                          secondary={
                            <>
                              <Typography variant="caption" display="block">
                                {result.snippet?.substring(0, 100)}...
                              </Typography>
                              <Chip
                                label={result.platform}
                                size="small"
                                sx={{ mt: 0.5, mr: 1 }}
                              />
                              <a
                                href={result.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                style={{ fontSize: '0.75rem' }}
                              >
                                링크 열기 ↗
                              </a>
                            </>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          )}

          {/* 상품 정보 입력 */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  3️⃣ 분석할 상품 정보
                </Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="상품명"
                      value={productInfo.name}
                      onChange={(e) =>
                        setProductInfo({ ...productInfo, name: e.target.value })
                      }
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="카테고리"
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
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="타겟 고객"
                      value={productInfo.target}
                      onChange={(e) =>
                        setProductInfo({ ...productInfo, target: e.target.value })
                      }
                    />
                  </Grid>
                </Grid>

                <Button
                  variant="contained"
                  color="success"
                  startIcon={<Assessment />}
                  onClick={handleAnalyze}
                  disabled={loading || searchResults.length === 0}
                  fullWidth
                  sx={{ mt: 2 }}
                  size="large"
                >
                  SWOT + 3C 분석 실행
                </Button>
              </CardContent>
            </Card>
          </Grid>

          {/* 분석 결과 */}
          {analysisResult && (
            <Grid item xs={12}>
              <Card sx={{ bgcolor: 'success.light' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <CheckCircle sx={{ mr: 1, color: 'white' }} />
                    <Typography variant="h6" sx={{ color: 'white' }}>
                      ✅ 분석 완료!
                    </Typography>
                  </Box>

                  <Alert severity="success" sx={{ mb: 2 }}>
                    {analysisResult.search_results_count}개의 경쟁사 상품을 분석했습니다
                  </Alert>

                  <Button
                    variant="contained"
                    startIcon={<LinkIcon />}
                    onClick={() => window.open(`${BACKEND_URL}${analysisResult.html_url}`, '_blank')}
                    fullWidth
                  >
                    분석 보고서 열기
                  </Button>

                  {/* 인사이트 미리보기 */}
                  {analysisResult.analysis?.insights && (
                    <Box sx={{ mt: 3 }}>
                      <Typography variant="h6" gutterBottom sx={{ color: 'white' }}>
                        핵심 인사이트:
                      </Typography>
                      {analysisResult.analysis.insights.map((insight, idx) => (
                        <Alert key={idx} severity="info" sx={{ mb: 1 }}>
                          {insight}
                        </Alert>
                      ))}
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>

        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
            <CircularProgress />
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default SwotAnalyzer;
