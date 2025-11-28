import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Paper,
  Typography,
  Grid
} from '@mui/material';

const ProductInputForm = ({ onSubmit, loading, initialData }) => {
  const [formData, setFormData] = useState({
    product_name: '',
    summary: '',
    category: '푸드',
    manufacture_country: '대한민국',
    manufacture_date: '',
    specs: {},
    keywords: [],
    target_customer: '',
    tone: '친근한',
    platforms: ['coupang'],
    image_options: {
      style: 'real',
      shots: ['main', 'usage']
    },
    competitor_links: [],
    allow_web_search: true
  });

  // initialData가 있으면 폼에 자동 입력
  useEffect(() => {
    if (initialData) {
      const keywordsArray = typeof initialData.keywords === 'string'
        ? initialData.keywords.split(',').map(k => k.trim()).filter(k => k)
        : initialData.keywords || [];

      setFormData(prev => ({
        ...prev,
        product_name: initialData.product_name || prev.product_name,
        category: initialData.category || prev.category,
        keywords: keywordsArray
      }));
    }
  }, [initialData]);

  const [currentKeyword, setCurrentKeyword] = useState('');
  const [specKey, setSpecKey] = useState('');
  const [specValue, setSpecValue] = useState('');

  const handleChange = (field) => (event) => {
    setFormData({ ...formData, [field]: event.target.value });
  };

  const handlePlatformChange = (platform) => (event) => {
    const platforms = event.target.checked
      ? [...formData.platforms, platform]
      : formData.platforms.filter((p) => p !== platform);
    setFormData({ ...formData, platforms });
  };

  const handleKeywordAdd = () => {
    if (currentKeyword.trim()) {
      setFormData({
        ...formData,
        keywords: [...formData.keywords, currentKeyword.trim()]
      });
      setCurrentKeyword('');
    }
  };

  const handleKeywordDelete = (keyword) => {
    setFormData({
      ...formData,
      keywords: formData.keywords.filter((k) => k !== keyword)
    });
  };

  const handleSpecAdd = () => {
    if (specKey.trim() && specValue.trim()) {
      setFormData({
        ...formData,
        specs: { ...formData.specs, [specKey.trim()]: specValue.trim() }
      });
      setSpecKey('');
      setSpecValue('');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Paper elevation={3} sx={{ p: 4 }}>
      <Typography variant="h5" gutterBottom>
        상품 정보 입력
      </Typography>

      <Box component="form" onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              required
              label="상품명"
              value={formData.product_name}
              onChange={handleChange('product_name')}
              placeholder="예: 에어프라이어용 바삭감자칩"
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              required
              label="한 줄 요약 (30자 이내)"
              value={formData.summary}
              onChange={handleChange('summary')}
              inputProps={{ maxLength: 30 }}
              helperText={`${formData.summary.length}/30`}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>카테고리</InputLabel>
              <Select
                value={formData.category}
                label="카테고리"
                onChange={handleChange('category')}
              >
                <MenuItem value="푸드">푸드</MenuItem>
                <MenuItem value="생활">생활</MenuItem>
                <MenuItem value="전자">전자</MenuItem>
                <MenuItem value="패션">패션</MenuItem>
                <MenuItem value="뷰티">뷰티</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="제조국"
              value={formData.manufacture_country}
              onChange={handleChange('manufacture_country')}
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="제품 스펙 (키)"
              value={specKey}
              onChange={(e) => setSpecKey(e.target.value)}
              placeholder="예: 중량"
            />
          </Grid>

          <Grid item xs={12}>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField
                fullWidth
                label="제품 스펙 (값)"
                value={specValue}
                onChange={(e) => setSpecValue(e.target.value)}
                placeholder="예: 120g"
              />
              <Button variant="outlined" onClick={handleSpecAdd}>
                추가
              </Button>
            </Box>
            <Box sx={{ mt: 2 }}>
              {Object.entries(formData.specs).map(([key, value]) => (
                <Chip
                  key={key}
                  label={`${key}: ${value}`}
                  sx={{ mr: 1, mb: 1 }}
                />
              ))}
            </Box>
          </Grid>

          <Grid item xs={12}>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <TextField
                fullWidth
                label="핵심 키워드"
                value={currentKeyword}
                onChange={(e) => setCurrentKeyword(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleKeywordAdd())}
                placeholder="키워드 입력 후 추가 버튼 클릭"
              />
              <Button variant="outlined" onClick={handleKeywordAdd}>
                추가
              </Button>
            </Box>
            <Box sx={{ mt: 2 }}>
              {formData.keywords.map((keyword) => (
                <Chip
                  key={keyword}
                  label={keyword}
                  onDelete={() => handleKeywordDelete(keyword)}
                  sx={{ mr: 1, mb: 1 }}
                />
              ))}
            </Box>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="타겟 고객"
              value={formData.target_customer}
              onChange={handleChange('target_customer')}
              placeholder="예: 20~30대, 다이어터"
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>톤</InputLabel>
              <Select
                value={formData.tone}
                label="톤"
                onChange={handleChange('tone')}
              >
                <MenuItem value="전문적">전문적</MenuItem>
                <MenuItem value="친근한">친근한</MenuItem>
                <MenuItem value="감성적">감성적</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="subtitle2" gutterBottom>
              플랫폼 선택
            </Typography>
            <FormGroup row>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.platforms.includes('coupang')}
                    onChange={handlePlatformChange('coupang')}
                  />
                }
                label="쿠팡"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.platforms.includes('naver')}
                    onChange={handlePlatformChange('naver')}
                  />
                }
                label="네이버 스토어"
              />
            </FormGroup>
          </Grid>

          <Grid item xs={12}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={formData.allow_web_search}
                  onChange={(e) =>
                    setFormData({ ...formData, allow_web_search: e.target.checked })
                  }
                />
              }
              label="자동 웹 검색 허용 (경쟁사 분석)"
            />
          </Grid>

          <Grid item xs={12}>
            <Button
              type="submit"
              variant="contained"
              size="large"
              fullWidth
              disabled={!formData.product_name || !formData.summary || formData.platforms.length === 0}
            >
              미리보기
            </Button>
          </Grid>
        </Grid>
      </Box>
    </Paper>
  );
};

export default ProductInputForm;
