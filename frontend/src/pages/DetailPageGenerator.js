import React, { useState, useEffect } from 'react';
import { Container, Paper, Typography, Box, Alert } from '@mui/material';
import { useLocation } from 'react-router-dom';
import { Description, Info } from '@mui/icons-material';
import ProductInputForm from '../components/ProductInputForm';
import ResultView from '../components/ResultView';
import PreviewPanel from '../components/PreviewPanel';

const DetailPageGenerator = () => {
  const location = useLocation();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [swotData, setSwotData] = useState(null);

  // SWOT 페이지에서 넘어온 데이터 처리
  useEffect(() => {
    if (location.state?.fromSwot && location.state?.swotData) {
      setSwotData(location.state.swotData);
      console.log('SWOT 데이터 수신:', location.state.swotData);
    }
  }, [location]);

  const handleGenerate = async (formData) => {
    setLoading(true);
    try {
      const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${BACKEND_URL}/api/generate/detailpage`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`서버 오류: ${response.status} - ${JSON.stringify(errorData.detail)}`);
      }

      const data = await response.json();
      setResult(data);
      console.log('생성 완료:', data);
    } catch (error) {
      console.error('생성 오류:', error);
      alert('생성 오류: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
  };

  return (
    <Container maxWidth="xl">
      <Paper elevation={3} sx={{ p: 4, mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Description sx={{ fontSize: 40, mr: 2, color: 'primary.main' }} />
          <Box>
            <Typography variant="h4" gutterBottom>
              📝 상세페이지 자동 생성
            </Typography>
            <Typography variant="body2" color="text.secondary">
              AI가 상품 정보를 분석하여 쿠팡/네이버 스토어용 상세페이지를 자동 생성합니다
            </Typography>
          </Box>
        </Box>

        <Alert severity="info" icon={<Info />} sx={{ mb: 2 }}>
          💡 <strong>팁:</strong> "🚀 통합 워크플로우" 탭을 사용하면 SWOT 분석 결과가 자동으로 반영됩니다!
        </Alert>

        {swotData && (
          <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSwotData(null)}>
            <strong>✅ SWOT 분석 데이터가 준비되었습니다!</strong><br/>
            상품명: {swotData.product_name}<br/>
            카테고리: {swotData.category}<br/>
            추출된 키워드: {swotData.keywords?.join(', ')}<br/>
            <br/>
            💡 아래 폼에 키워드가 자동으로 입력됩니다. 추가 정보를 입력하고 생성하세요!
          </Alert>
        )}

        {!result ? (
          <>
            <ProductInputForm
              onSubmit={handleGenerate}
              loading={loading}
              initialData={swotData ? {
                product_name: swotData.product_name,
                category: swotData.category,
                keywords: swotData.keywords?.join(', ') || ''
              } : null}
            />
            {loading && <PreviewPanel />}
          </>
        ) : (
          <ResultView result={result} onReset={handleReset} />
        )}
      </Paper>
    </Container>
  );
};

export default DetailPageGenerator;
