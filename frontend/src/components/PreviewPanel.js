import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Chip,
  Table,
  TableBody,
  TableRow,
  TableCell
} from '@mui/material';
import { ArrowBack, AutoAwesome } from '@mui/icons-material';

const PreviewPanel = ({ data, onGenerate, onBack }) => {
  return (
    <Paper elevation={3} sx={{ p: 4 }}>
      <Typography variant="h5" gutterBottom>
        입력 정보 미리보기
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12}>
          <Typography variant="h6" color="primary">
            {data.product_name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {data.summary}
          </Typography>
        </Grid>

        <Grid item xs={12} md={6}>
          <Table size="small">
            <TableBody>
              <TableRow>
                <TableCell><strong>카테고리</strong></TableCell>
                <TableCell>{data.category}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell><strong>제조국</strong></TableCell>
                <TableCell>{data.manufacture_country}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell><strong>타겟</strong></TableCell>
                <TableCell>{data.target_customer || '미지정'}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell><strong>톤</strong></TableCell>
                <TableCell>{data.tone}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </Grid>

        <Grid item xs={12} md={6}>
          <Typography variant="subtitle2" gutterBottom>
            제품 스펙
          </Typography>
          <Box>
            {Object.entries(data.specs).length > 0 ? (
              Object.entries(data.specs).map(([key, value]) => (
                <Chip
                  key={key}
                  label={`${key}: ${value}`}
                  size="small"
                  sx={{ mr: 1, mb: 1 }}
                />
              ))
            ) : (
              <Typography variant="body2" color="text.secondary">
                스펙 미입력
              </Typography>
            )}
          </Box>
        </Grid>

        <Grid item xs={12}>
          <Typography variant="subtitle2" gutterBottom>
            핵심 키워드
          </Typography>
          <Box>
            {data.keywords.map((keyword) => (
              <Chip
                key={keyword}
                label={keyword}
                color="primary"
                size="small"
                sx={{ mr: 1, mb: 1 }}
              />
            ))}
          </Box>
        </Grid>

        <Grid item xs={12}>
          <Typography variant="subtitle2" gutterBottom>
            플랫폼
          </Typography>
          <Box>
            {data.platforms.map((platform) => (
              <Chip
                key={platform}
                label={platform === 'coupang' ? '쿠팡' : '네이버 스토어'}
                color="secondary"
                size="small"
                sx={{ mr: 1, mb: 1 }}
              />
            ))}
          </Box>
        </Grid>

        <Grid item xs={12}>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'space-between', mt: 3 }}>
            <Button
              variant="outlined"
              startIcon={<ArrowBack />}
              onClick={onBack}
            >
              뒤로
            </Button>
            <Button
              variant="contained"
              size="large"
              startIcon={<AutoAwesome />}
              onClick={onGenerate}
            >
              상세페이지 생성
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default PreviewPanel;
