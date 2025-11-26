import React, { useState } from 'react';
import { Container, Paper, Typography, Box } from '@mui/material';
import ProductInputForm from '../components/ProductInputForm';
import ResultView from '../components/ResultView';
import PreviewPanel from '../components/PreviewPanel';

const DetailPageGenerator = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async (formData) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/generate/detailpage', {
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
        <Typography variant="h4" gutterBottom>
          📝 상세페이지 자동 생성
        </Typography>
        <Typography variant="body2" color="text.secondary" paragraph>
          AI가 상품 정보를 분석하여 쿠팡/네이버 스토어용 상세페이지를 자동 생성합니다
        </Typography>

        {!result ? (
          <>
            <ProductInputForm onSubmit={handleGenerate} loading={loading} />
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
