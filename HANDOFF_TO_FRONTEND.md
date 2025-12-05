# 🎨 프론트엔드 개발자 인수인계 문서

## 📋 요약

마케팅 AI 챗봇 백엔드 API가 완성되어 Render에 배포되었습니다.
이제 프론트엔드에서 이 API를 호출하여 서비스를 구현하면 됩니다.

---

## 🌐 배포된 백엔드 정보

### API Base URL
```
https://marketing-chatbot-ta6f.onrender.com
```

### API 문서 (Swagger UI)
```
https://marketing-chatbot-ta6f.onrender.com/docs
```

**Swagger UI에서 모든 API를 직접 테스트할 수 있습니다!**

---

## 📚 필수 문서

### 1. API 상세 문서
**파일**: `API_DOCUMENTATION.md`

- 모든 엔드포인트의 Request/Response 예시
- 필드 설명, 에러 코드
- 사용 시나리오 3가지
- 총 20개+ 엔드포인트 문서화

### 2. 프로젝트 README
**파일**: `README.md`

- 프로젝트 개요
- 기술 스택
- 로컬 개발 환경 설정 방법

### 3. 배포 가이드
**파일**: `DEPLOY_GUIDE.md`

- Render 배포 상세 가이드
- 트러블슈팅

---

## 🔑 환경변수 설정

프론트엔드 프로젝트에 `.env` 파일 생성:

### React 프로젝트
```bash
REACT_APP_BACKEND_URL=https://marketing-chatbot-ta6f.onrender.com
```

### Next.js 프로젝트
```bash
NEXT_PUBLIC_BACKEND_URL=https://marketing-chatbot-ta6f.onrender.com
```

### Vue.js 프로젝트
```bash
VUE_APP_BACKEND_URL=https://marketing-chatbot-ta6f.onrender.com
```

---

## 🚀 주요 API 엔드포인트

### 1. 통합 워크플로우 (권장)

#### 세션 생성
```javascript
POST /api/unified/start

// Request
{
  "product_name": "바삭 감자칩",
  "category": "간식",
  "keywords": ["건강", "저칼로리"],
  "target_customer": "20-30대 헬스족",
  "platforms": ["coupang", "naver"]
}

// Response
{
  "session_id": "sess_xxx...",
  "message": "✅ 세션이 생성되었습니다!",
  "next_step": "swot",
  "product_info": {...}
}
```

#### PDF 파싱
```javascript
POST /api/unified/parse-pdf

// Request (multipart/form-data)
file: PDF 파일 (최대 50MB)

// Response
{
  "success": true,
  "product_name": "추출된 상품명",
  "category": "추출된 카테고리",
  "keywords": ["키워드1", "키워드2"],
  ...
}
```

#### SWOT 분석 실행
```javascript
POST /api/unified/execute-swot

// Request
{
  "session_id": "sess_xxx...",
  "search_depth": "advanced",
  "days": 90,
  "include_reviews": true
}

// Response
{
  "session_id": "sess_xxx...",
  "analysis_result": {
    "swot": {...},
    "three_c": {...},
    "price_analysis": {...}
  },
  "html_url": "/outputs/sess_xxx/analysis.html",
  "competitor_count": 15
}
```

#### 상세페이지 생성
```javascript
POST /api/unified/execute-detail

// Request
{
  "session_id": "sess_xxx...",
  "platform": "coupang",
  "tone": "친근한",
  "image_style": "real"
}

// Response
{
  "session_id": "sess_xxx...",
  "markdown_url": "/outputs/sess_xxx/detail.md",
  "html_url": "/outputs/sess_xxx/detail.html",
  "images": ["https://dalle-image-1.png", ...]
}
```

### 2. 챗봇
```javascript
POST /api/chatbot/chat

// Request
{
  "message": "이 상품의 타겟 고객은?",
  "conversation_history": [
    {"role": "user", "content": "안녕?"},
    {"role": "assistant", "content": "안녕하세요!"}
  ],
  "session_context": {
    "product_info": {...}
  },
  "session_id": "sess_xxx..."
}

// Response
{
  "response": "20-30대 건강을 중시하는 소비자입니다...",
  "timestamp": "2024-12-05T..."
}
```

---

## 💻 프론트엔드 구현 예시

### React + Axios
```javascript
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL;

// 세션 생성
const createSession = async (productInfo) => {
  const response = await axios.post(`${API_URL}/api/unified/start`, productInfo);
  return response.data;
};

// SWOT 분석
const executeSwot = async (sessionId) => {
  const response = await axios.post(`${API_URL}/api/unified/execute-swot`, {
    session_id: sessionId,
    search_depth: 'advanced',
    days: 90,
    include_reviews: true
  });
  return response.data;
};

// 상세페이지 생성
const generateDetailPage = async (sessionId) => {
  const response = await axios.post(`${API_URL}/api/unified/execute-detail`, {
    session_id: sessionId,
    platform: 'coupang',
    tone: '친근한',
    image_style: 'real'
  });
  return response.data;
};
```

### Fetch API
```javascript
const API_URL = process.env.REACT_APP_BACKEND_URL;

// 세션 생성
async function createSession(productInfo) {
  const response = await fetch(`${API_URL}/api/unified/start`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(productInfo)
  });

  if (!response.ok) {
    throw new Error('API 오류');
  }

  return await response.json();
}
```

---

## ⚠️ 중요 주의사항

### 1. 첫 요청 시 로딩 처리 필수

Render 무료 플랜은 15분 비활성 시 sleep됩니다.
**첫 요청은 1분 정도 걸릴 수 있습니다.**

```javascript
const [loading, setLoading] = useState(false);
const [loadingMessage, setLoadingMessage] = useState('');

const handleSubmit = async () => {
  setLoading(true);
  setLoadingMessage('서버 연결 중입니다... (최대 1분 소요)');

  try {
    const result = await createSession(productInfo);
    setLoadingMessage('요청 처리 중...');
    // ...
  } catch (error) {
    console.error(error);
  } finally {
    setLoading(false);
  }
};
```

### 2. 에러 핸들링

```javascript
try {
  const response = await fetch(`${API_URL}/api/unified/start`, {...});

  if (!response.ok) {
    const error = await response.json();
    alert(`오류: ${error.detail}`);
    return;
  }

  const data = await response.json();
  // 성공 처리
} catch (error) {
  console.error('네트워크 오류:', error);
  alert('서버 연결에 실패했습니다. 잠시 후 다시 시도해주세요.');
}
```

### 3. CORS 설정

**백엔드에서 이미 CORS를 모든 origin에 허용했습니다.**

현재 설정:
```python
allow_origins=["*"]  # 모든 도메인 허용
```

프로덕션 배포 시 특정 도메인만 허용하려면 백엔드 수정 필요:
```python
allow_origins=[
  "https://your-frontend.vercel.app",
  "https://your-frontend.netlify.app"
]
```

### 4. HTML/이미지 URL 처리

API 응답의 URL은 상대경로입니다:
```javascript
// API 응답
{
  "html_url": "/outputs/sess_xxx/analysis.html",
  "images": ["https://dalle-image-1.png"]
}

// 프론트에서 처리
const fullHtmlUrl = `${API_URL}${html_url}`;  // 절대 URL로 변환
const imageUrl = images[0];  // 이미지는 이미 절대 URL
```

### 5. 파일 다운로드

```javascript
const downloadFile = (url) => {
  const fullUrl = url.startsWith('http')
    ? url
    : `${API_URL}${url}`;

  window.open(fullUrl, '_blank');
};
```

---

## 🧪 API 테스트 방법

### 1. Swagger UI 사용 (가장 쉬움)
1. https://marketing-chatbot-ta6f.onrender.com/docs 접속
2. 원하는 엔드포인트 클릭
3. "Try it out" 클릭
4. Request body 입력
5. "Execute" 클릭
6. 응답 확인

### 2. curl 명령어
```bash
# 세션 생성
curl -X POST https://marketing-chatbot-ta6f.onrender.com/api/unified/start \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "테스트 상품",
    "category": "테스트",
    "keywords": ["테스트"],
    "target_customer": "테스트",
    "platforms": ["coupang"]
  }'
```

### 3. Postman
1. Postman 설치
2. 새 Request 생성
3. URL: `https://marketing-chatbot-ta6f.onrender.com/api/unified/start`
4. Method: POST
5. Body → raw → JSON
6. Request body 입력
7. Send

---

## 📊 API 응답 시간

### 평균 응답 시간 (Render 무료 플랜)
- 세션 생성: 1-2초
- PDF 파싱: 5-10초
- SWOT 분석: 40-70초 (경쟁사 검색 + AI 분석)
- 상세페이지 생성: 70-120초 (AI 카피 + DALL-E 이미지)
- 챗봇 응답: 3-7초

### Sleep 후 첫 요청
- 서버 웨이크업: 60-90초 추가

**로딩 UI를 꼭 구현하세요!**

---

## 🎨 UI/UX 권장사항

### 1. 로딩 상태
```javascript
// 단계별 로딩 메시지
const loadingMessages = {
  'start': '세션을 생성하는 중입니다...',
  'swot': 'SWOT 분석 중입니다... (약 1분 소요)',
  'detail': '상세페이지 생성 중입니다... (약 2분 소요)',
  'chat': 'AI가 답변을 생성하는 중입니다...'
};
```

### 2. 진행률 표시
```javascript
// SWOT 분석 중
<LinearProgress />
<Typography>경쟁사 검색 중... (30초)</Typography>

// 상세페이지 생성 중
<CircularProgress variant="determinate" value={progress} />
<Typography>이미지 생성 중... ({currentImage}/5)</Typography>
```

### 3. 에러 메시지
```javascript
// 사용자 친화적 에러 메시지
const errorMessages = {
  400: '입력 정보를 확인해주세요.',
  404: '세션을 찾을 수 없습니다. 다시 시작해주세요.',
  500: '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.',
  timeout: '요청 시간이 초과되었습니다. 네트워크 연결을 확인해주세요.'
};
```

### 4. 성공 피드백
```javascript
// 각 단계 완료 시
<Alert severity="success">
  ✅ SWOT 분석이 완료되었습니다!
</Alert>
```

---

## 🔒 보안 주의사항

### 1. API 키는 백엔드에만
- **절대 프론트엔드에 OpenAI API 키를 넣지 마세요!**
- 모든 AI 기능은 백엔드 API를 통해서만 호출

### 2. 환경변수 관리
```bash
# .env 파일은 Git에 커밋하지 않기
# .gitignore에 추가
.env
.env.local
```

### 3. 프로덕션 배포 시
- Vercel/Netlify 환경변수에 `REACT_APP_BACKEND_URL` 설정
- HTTPS만 사용

---

## 📱 반응형 디자인 고려사항

### 모바일 최적화
- SWOT 분석 결과: 테이블 대신 카드 형태
- 상세페이지 미리보기: 스크롤 가능한 iframe
- 챗봇: 하단 고정 입력창

### 태블릿
- 2단 레이아웃 (입력폼 + 결과)
- 사이드바 네비게이션

---

## 🐛 알려진 이슈 및 해결방법

### 1. "No module named 'langchain_chroma'" 에러
**해결됨**: 최신 코드에 반영됨

### 2. Sleep 후 첫 요청 실패
**해결방법**:
- 타임아웃을 2분으로 설정
- 재시도 로직 구현

```javascript
const fetchWithRetry = async (url, options, retries = 1) => {
  try {
    const response = await fetch(url, {
      ...options,
      timeout: 120000  // 2분
    });
    return response;
  } catch (error) {
    if (retries > 0) {
      console.log('재시도 중...');
      return fetchWithRetry(url, options, retries - 1);
    }
    throw error;
  }
};
```

### 3. CORS 에러
**해결됨**: 백엔드에서 모든 origin 허용

---

## 📦 배포된 백엔드 정보

### GitHub 레포지토리
```
https://github.com/sinyoung0110/marketing_chatbot
```

### Render 대시보드
- https://dashboard.render.com
- 백엔드 개발자가 접근 권한 있음

### 환경변수 (Render에 설정됨)
- `OPENAI_API_KEY`: ✅ 설정됨
- `TAVILY_API_KEY`: ✅ 설정됨
- `PYTHON_VERSION`: 3.11.9

### 자동 재배포
- GitHub에 push하면 자동으로 재배포됨
- 약 3-5분 소요
- Render 대시보드에서 로그 확인 가능

---

## 🎯 개발 우선순위 제안

### Phase 1: 기본 기능 (1주)
1. ✅ 세션 생성 UI
2. ✅ SWOT 분석 실행 UI
3. ✅ 결과 표시 (HTML iframe)

### Phase 2: 고급 기능 (1주)
4. ✅ PDF 업로드 기능
5. ✅ 상세페이지 생성 UI
6. ✅ 로딩 상태 고도화

### Phase 3: 부가 기능 (1주)
7. ✅ 챗봇 UI
8. ✅ 결과 다운로드
9. ✅ 반응형 디자인

---

## 📞 문의 및 지원

### 백엔드 관련 문제
1. **API 오류**: Swagger UI에서 직접 테스트
2. **응답 형식 변경 필요**: `API_DOCUMENTATION.md` 참고
3. **새 기능 요청**: GitHub Issues 등록

### 문서
- **API 문서**: `API_DOCUMENTATION.md`
- **배포 가이드**: `DEPLOY_GUIDE.md`
- **README**: `README.md`

### Swagger UI (실시간 API 테스트)
```
https://marketing-chatbot-ta6f.onrender.com/docs
```

---

## ✅ 체크리스트

프론트엔드 개발 시작 전:

- [ ] `.env` 파일 생성 및 `REACT_APP_BACKEND_URL` 설정
- [ ] `API_DOCUMENTATION.md` 읽기
- [ ] Swagger UI에서 API 테스트해보기
- [ ] 첫 요청 시 로딩 UI 구현 계획
- [ ] 에러 핸들링 전략 수립
- [ ] CORS 설정 확인

---

## 🚀 시작하기

```javascript
// 1. 환경변수 설정
// .env 파일 생성
REACT_APP_BACKEND_URL=https://marketing-chatbot-ta6f.onrender.com

// 2. 첫 API 호출 테스트
const testAPI = async () => {
  const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/health`);
  const data = await response.json();
  console.log(data);  // { "status": "healthy", "timestamp": "..." }
};

testAPI();
```

---

**이제 프론트엔드 개발을 시작하세요! 🎨**

**질문이 있으면 Swagger UI를 먼저 확인하고, API_DOCUMENTATION.md를 참고하세요.**

---

**작성일**: 2024-12-05
**백엔드 버전**: v1.0.0
**API URL**: https://marketing-chatbot-ta6f.onrender.com
