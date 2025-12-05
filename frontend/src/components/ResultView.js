import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Link
} from '@mui/material';
import { Download, ContentCopy, RestartAlt, CheckCircle } from '@mui/icons-material';

const ResultView = ({ result, onReset }) => {
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

  const handleDownload = (url) => {
    const fullUrl = url.startsWith('http') ? url : `${BACKEND_URL}${url}`;
    window.open(fullUrl, '_blank');
  };

  const handleCopyLink = (url) => {
    const fullUrl = url.startsWith('http') ? url : `${BACKEND_URL}${url}`;
    navigator.clipboard.writeText(fullUrl);
    alert('링크가 복사되었습니다!');
  };

  const getFullUrl = (url) => {
    return url?.startsWith('http') ? url : `${BACKEND_URL}${url}`;
  };

  return (
    <Paper elevation={3} sx={{ p: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <CheckCircle sx={{ fontSize: 80, color: 'success.main', mb: 2 }} />
        <Typography variant="h4" gutterBottom>
          생성 완료!
        </Typography>
        <Typography variant="body1" color="text.secondary">
          상세페이지가 성공적으로 생성되었습니다.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📝 Markdown 파일
              </Typography>
              <Typography variant="body2" color="text.secondary">
                편집 가능한 마크다운 형식
              </Typography>
              <Link
                href={getFullUrl(result.markdown_url)}
                target="_blank"
                sx={{ display: 'block', mt: 2 }}
              >
                {result.markdown_url}
              </Link>
            </CardContent>
            <CardActions>
              <Button
                size="small"
                startIcon={<Download />}
                onClick={() => handleDownload(result.markdown_url)}
              >
                다운로드
              </Button>
              <Button
                size="small"
                startIcon={<ContentCopy />}
                onClick={() => handleCopyLink(result.markdown_url)}
              >
                링크 복사
              </Button>
            </CardActions>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🌐 HTML 파일
              </Typography>
              <Typography variant="body2" color="text.secondary">
                바로 사용 가능한 HTML 형식
              </Typography>
              <Link
                href={getFullUrl(result.html_url)}
                target="_blank"
                sx={{ display: 'block', mt: 2 }}
              >
                {result.html_url}
              </Link>
            </CardContent>
            <CardActions>
              <Button
                size="small"
                startIcon={<Download />}
                onClick={() => handleDownload(result.html_url)}
              >
                다운로드
              </Button>
              <Button
                size="small"
                startIcon={<ContentCopy />}
                onClick={() => handleCopyLink(result.html_url)}
              >
                링크 복사
              </Button>
            </CardActions>
          </Card>
        </Grid>

        {result.analysis_url && (
          <Grid item xs={12}>
            <Card sx={{ bgcolor: 'primary.light', color: 'white' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ color: 'white' }}>
                  📊 SWOT + 3C 분석 보고서
                </Typography>
                <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.9)' }}>
                  경쟁사 분석, 가격 비교, 전략 인사이트 포함
                </Typography>
                <Link
                  href={getFullUrl(result.analysis_url)}
                  target="_blank"
                  sx={{ display: 'block', mt: 2, color: 'white', fontWeight: 'bold' }}
                >
                  {result.analysis_url}
                </Link>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  startIcon={<Download />}
                  onClick={() => handleDownload(result.analysis_url)}
                  sx={{ color: 'white' }}
                >
                  분석 보고서 열기
                </Button>
                <Button
                  size="small"
                  startIcon={<ContentCopy />}
                  onClick={() => handleCopyLink(result.analysis_url)}
                  sx={{ color: 'white' }}
                >
                  링크 복사
                </Button>
              </CardActions>
            </Card>
          </Grid>
        )}

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                🖼️ 생성된 이미지
              </Typography>
              <Grid container spacing={2}>
                {result.images && result.images.map((img, index) => (
                  <Grid item xs={12} sm={6} md={4} key={index}>
                    <Box
                      sx={{
                        width: '100%',
                        height: 200,
                        bgcolor: 'grey.200',
                        borderRadius: 1,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}
                    >
                      <img
                        src={getFullUrl(img)}
                        alt={`생성 이미지 ${index + 1}`}
                        style={{
                          maxWidth: '100%',
                          maxHeight: '100%',
                          objectFit: 'contain'
                        }}
                        onError={(e) => {
                          console.error('이미지 로드 실패:', img);
                          e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="200"%3E%3Crect fill="%23ddd" width="200" height="200"/%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" fill="%23999"%3E이미지 로드 실패%3C/text%3E%3C/svg%3E';
                        }}
                      />
                    </Box>
                    <Link href={getFullUrl(img)} target="_blank" sx={{ display: 'block', mt: 1, fontSize: '0.875rem' }}>
                      이미지 {index + 1}
                    </Link>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Box sx={{ textAlign: 'center', mt: 3 }}>
            <Button
              variant="contained"
              size="large"
              startIcon={<RestartAlt />}
              onClick={onReset}
            >
              새로 만들기
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default ResultView;
