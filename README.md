# SellFlow AI - 마케팅 자동화 챗봇 시스템

AI 기반 e-커머스 마케팅 자동화 플랫폼으로, SWOT 분석부터 상세페이지 생성, 챗봇 상담까지 통합된 워크플로우를 제공합니다.

## 📋 프로젝트 개요

### 주요 기능
1. **통합 워크플로우**: 한 번 입력으로 SWOT 분석 → 상세페이지 생성 → 챗봇 상담까지 자동 연계
2. **SWOT + 3C 분석**: 경쟁사 자동 분석 및 시각화된 HTML 보고서 생성
3. **AI 상세페이지 생성**: 카테고리별 맞춤형 상세페이지 및 이미지 자동 생성
4. **마케팅 챗봇**: 프로젝트 컨텍스트 기반 실시간 마케팅 전략 상담
5. **PDF 파싱**: PDF 파일 업로드로 상품 정보 자동 추출

### 기술 스택
- **Backend**: FastAPI, Python 3.11
- **Frontend**: React 18, Material-UI
- **AI/LLM**: LangChain, LangGraph, OpenAI GPT-4o-mini, DALL-E 3
- **검색**: Tavily API, DuckDuckGo
- **벡터 DB**: ChromaDB
- **배포**: Render (Backend), Vercel/Netlify (Frontend)

---

## 🚀 로컬 개발 환경 설정

### 사전 요구사항
- Python 3.11 이상
- Node.js 18 이상
- npm 또는 yarn
- Git

### 1. 프로젝트 클론

```bash
git clone https://github.com/sinyoung0110/marketing_chatbot.git
cd marketing_chatbot
```

### 2. API 키 발급

#### OpenAI API 키 (필수)
1. [OpenAI Platform](https://platform.openai.com/) 접속
2. 회원가입 후 로그인
3. 우측 상단 프로필 → "API keys" 클릭
4. "Create new secret key" 버튼 클릭
5. 생성된 키 복사 (한 번만 표시되므로 안전한 곳에 보관)

   ```
   sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

#### Tavily API 키 (선택 - 고급 검색 기능용)
1. [Tavily](https://tavily.com/) 접속
2. 회원가입 후 로그인
3. Dashboard에서 API 키 발급
4. 무료 플랜: 월 1,000회 검색 가능

   ```
   tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

### 3. Backend 설정

```bash
# 백엔드 디렉토리로 이동
cd backend

# 가상환경 생성 (권장)
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows

# 패키지 설치
pip install -r requirements.txt

# .env 파일 생성
cp .env.example .env

# .env 파일 편집 (발급받은 API 키 입력)
nano .env  # 또는 원하는 에디터 사용
```

**`.env` 파일 내용:**
```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### 4. Frontend 설정

```bash
# 새 터미널을 열고 프론트엔드 디렉토리로 이동
cd frontend

# 패키지 설치
npm install

# .env 파일 생성
cp .env.example .env
```

**`frontend/.env` 파일 내용 (로컬 개발용):**
```bash
REACT_APP_BACKEND_URL=http://localhost:8000
```

---

### 5. 실행

#### Backend 실행 (첫 번째 터미널)
```bash
cd backend
python3 main.py
```

서버가 `http://localhost:8000`에서 실행됩니다.

**성공 메시지:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**API 문서 확인:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Frontend 실행 (두 번째 터미널)
```bash
cd frontend
npm start
```

브라우저가 자동으로 `http://localhost:3000`에서 열립니다.

---

## 🌐 프로덕션 배포

### Backend 배포 (Render)

자세한 내용은 [DEPLOY_GUIDE.md](./DEPLOY_GUIDE.md) 참고

**간단 요약:**

1. GitHub에 코드 푸시
2. [Render](https://render.com) 가입 및 GitHub 연동
3. "New Web Service" 생성
4. 레포지토리 선택 (`marketing_chatbot`)
5. 설정:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free
6. 환경변수 추가:
   - `OPENAI_API_KEY`: 발급받은 OpenAI 키
   - `TAVILY_API_KEY`: 발급받은 Tavily 키
7. 배포 완료!

**배포된 URL 예시:**
```
https://marketing-chatbot-ta6f.onrender.com
```

### Frontend 배포 (Vercel/Netlify)

**Vercel 예시:**

1. [Vercel](https://vercel.com) 가입
2. GitHub 레포지토리 연결
3. Root Directory: `frontend`
4. 환경변수 추가:
   ```
   REACT_APP_BACKEND_URL=https://your-backend.onrender.com
   ```
5. 배포!

---

## 📁 프로젝트 구조

```
marketing_chatbot/
├── backend/
│   ├── api/                    # API 엔드포인트
│   │   ├── endpoints.py        # 기본 상세페이지 API
│   │   ├── swot_endpoints.py   # SWOT 분석 API
│   │   ├── chatbot_endpoints.py # 챗봇 API
│   │   └── unified_endpoints.py # 통합 워크플로우 API
│   ├── agents/                 # AI 에이전트 워크플로우
│   │   └── workflow.py         # LangGraph 워크플로우
│   ├── tools/                  # 핵심 도구
│   │   ├── web_search.py       # Tavily 검색
│   │   ├── swot_3c_analysis.py # SWOT+3C 분석
│   │   ├── review_analyzer.py  # 리뷰 분석
│   │   └── exporter.py         # 파일 내보내기
│   ├── templates/              # HTML 템플릿
│   ├── utils/                  # 유틸리티
│   │   ├── rag_manager.py      # ChromaDB RAG
│   │   └── project_session.py  # 세션 관리
│   ├── models/                 # Pydantic 스키마
│   ├── main.py                 # FastAPI 서버 엔트리포인트
│   ├── requirements.txt        # Python 패키지
│   └── .env.example            # 환경변수 예시
├── frontend/
│   ├── src/
│   │   ├── pages/             # React 페이지 컴포넌트
│   │   │   ├── UnifiedWorkflow.js    # 통합 워크플로우
│   │   │   ├── SwotAnalyzer.js       # SWOT 분석
│   │   │   ├── MarketingChatbot.js   # 챗봇
│   │   │   └── DetailPageGenerator.js
│   │   ├── components/        # 재사용 컴포넌트
│   │   └── App.js
│   ├── package.json
│   ├── .env.example           # 환경변수 예시
│   └── public/
├── projects/                   # 생성된 파일 저장소 (자동 생성)
├── render.yaml                 # Render 배포 설정
├── runtime.txt                 # Python 버전 명시
├── API_DOCUMENTATION.md        # API 상세 문서
├── DEPLOY_GUIDE.md            # 배포 가이드
└── README.md
```

---

## 🔑 API 키 보안

**⚠️ 중요**: `.env` 파일은 절대 GitHub에 업로드하지 마세요!

- `.env.example` 파일을 복사하여 `.env` 파일 생성
- API 키는 `.env` 파일에만 저장
- `.gitignore`에 `.env` 파일이 포함되어 있어 자동으로 Git에서 제외됨

---

## 💡 사용 방법

### 1. 통합 워크플로우 (권장)

1. `http://localhost:3000` 접속
2. "통합 워크플로우" 페이지 이동
3. **방법 A: 직접 입력**
   - 상품명, 카테고리, 키워드 등 입력
   - "워크플로우 시작" 클릭
4. **방법 B: PDF 업로드**
   - PDF 파일 업로드 (상품 정보 자동 추출)
   - "워크플로우 시작" 클릭
5. **SWOT 분석 실행**
   - 경쟁사 자동 검색
   - SWOT+3C 분석
   - HTML 보고서 다운로드
6. **상세페이지 생성**
   - SWOT 결과 자동 반영
   - AI 이미지 생성
   - HTML/Markdown 다운로드
7. **챗봇 상담**
   - 마케팅 전략 질문
   - 상세페이지 수정 요청

### 2. 독립 SWOT 분석

1. "SWOT 분석" 페이지 이동
2. 검색 키워드 입력 (예: "에어프라이어 감자칩")
3. 검색 옵션 설정:
   - 플랫폼: 쿠팡, 네이버, 뉴스, 블로그
   - 검색 기간: 최근 30일, 90일 등
   - 리뷰 포함 여부
4. "검색" 클릭 → 경쟁사 리스트 확인
5. "SWOT+3C 분석" 클릭 → 보고서 생성

### 3. 독립 상세페이지 생성

1. "상세페이지 생성" 페이지 이동
2. 상품 정보 입력
3. 플랫폼 선택 (쿠팡/네이버)
4. 톤 앤 매너 선택 (친근한/전문적인/감성적인)
5. 생성 클릭

### 4. 마케팅 챗봇

1. "챗봇" 페이지 이동
2. 세션 ID 입력 (통합 워크플로우에서 생성됨)
3. 질문 입력:
   - "이 상품의 타겟 고객은 누구인가요?"
   - "가격 전략을 추천해주세요"
   - "상세페이지 제목을 ABC로 바꿔줘"

---

## 📚 API 문서

### Swagger UI (인터랙티브)
- 로컬: http://localhost:8000/docs
- 프로덕션: https://your-backend.onrender.com/docs

### 상세 API 문서
[API_DOCUMENTATION.md](./API_DOCUMENTATION.md) 참고

**주요 엔드포인트:**
- `POST /api/unified/start` - 세션 생성
- `POST /api/unified/parse-pdf` - PDF 파싱
- `POST /api/unified/execute-swot` - SWOT 분석
- `POST /api/unified/execute-detail` - 상세페이지 생성
- `POST /api/chatbot/chat` - 챗봇 대화

---

## ⚠️ 주의사항

### ChromaDB
- 첫 실행 시 ChromaDB가 비어있어 챗봇이 과거 프로젝트를 기억하지 못함
- 새로 생성한 프로젝트는 정상적으로 저장됨
- **Render 배포 시**: 재배포하면 ChromaDB 초기화됨 (핵심 기능에는 영향 없음)

### Render 무료 플랜 제한
- **15분 비활성 시 sleep**: 첫 요청 시 약 1분 대기
- **파일 저장**: 재배포 시 생성된 파일 삭제됨
- **해결책**: 프론트에서 "로딩 중..." 메시지 표시

### 파일 경로
- 모든 파일 경로는 **상대경로** 사용
- 프로젝트 루트 디렉토리를 기준으로 동작

---

## 🐛 문제 해결

### "OPENAI_API_KEY not found" 오류
```bash
# .env 파일이 backend/ 디렉토리에 있는지 확인
ls backend/.env

# 없으면 생성
cd backend
cp .env.example .env
nano .env  # API 키 입력
```

### Frontend가 Backend에 연결되지 않음
```bash
# Backend가 실행 중인지 확인
# 터미널에 "Application startup complete" 메시지가 있어야 함

# 환경변수 확인
cat frontend/.env
# REACT_APP_BACKEND_URL이 올바른지 확인

# 프론트 재시작 (.env 변경 시 필수!)
cd frontend
npm start
```

### 포트 충돌
```bash
# 포트 사용 확인
lsof -i :8000  # 백엔드
lsof -i :3000  # 프론트엔드

# 프로세스 종료
kill -9 <PID>
```

### 패키지 설치 오류
```bash
# pip 업그레이드
pip install --upgrade pip

# 가상환경 재생성
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Render 배포 실패
```bash
# Python 버전 확인
cat runtime.txt  # python-3.11.9 여야 함

# requirements.txt 확인
cat backend/requirements.txt

# Render 로그 확인 (대시보드)
```

### PDF 업로드 오류
- 파일 크기: 최대 50MB
- OCR 라이브러리 필요: `pytesseract`, `pdf2image`
- 일반 텍스트 추출 실패 시 자동으로 OCR 시도

---

## 📦 생성되는 파일

프로젝트 실행 시 자동으로 생성되는 파일/폴더:

### 로컬 개발
- `backend/projects/<session_id>/`: 각 세션별 저장소
  - `analysis.html`: SWOT 분석 결과
  - `detail.html`: 상세페이지 HTML
  - `detail.md`: 상세페이지 Markdown
  - `images/`: 생성된 이미지 (DALL-E)
- `backend/data/chroma_store/`: ChromaDB 벡터 데이터
- `backend/sessions/`: 세션 정보 JSON 파일

### Render 배포
- 파일은 임시 저장됨 (재배포 시 삭제)
- 이미지는 DALL-E URL로 제공됨 (영구 저장)

---

## 🚀 성능

### 로컬 실행
- SWOT 분석: 평균 30-60초
- 상세페이지 생성: 평균 60-90초 (이미지 생성 포함)
- 챗봇 응답: 평균 2-5초

### Render 무료 플랜
- SWOT 분석: 평균 40-70초
- 상세페이지 생성: 평균 70-120초
- 챗봇 응답: 평균 3-7초
- **첫 요청 (sleep 후)**: 60-90초 추가 대기

---

## 📞 지원 및 문서

### 문서
- **API 문서**: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **배포 가이드**: [DEPLOY_GUIDE.md](./DEPLOY_GUIDE.md)
- **Swagger UI**: http://localhost:8000/docs

### 지원
- **GitHub**: https://github.com/sinyoung0110/marketing_chatbot
- **Issues**: https://github.com/sinyoung0110/marketing_chatbot/issues

---

## 📄 라이선스

MIT License

---

## 🛠️ 개발 환경

### 권장 사양
- **OS**: macOS, Windows 10/11, Linux
- **Python**: 3.11.0 이상
- **Node.js**: 18.17.0 이상
- **RAM**: 최소 4GB (8GB 권장)
- **디스크**: 최소 2GB 여유 공간

### 권장 브라우저
- Chrome 최신 버전 (권장)
- Safari 최신 버전
- Firefox 최신 버전
- Edge 최신 버전

### IDE 추천
- **Backend**: VS Code, PyCharm
- **Frontend**: VS Code
- **필수 확장**: Python, ESLint, Prettier

---

## 🎯 다음 단계

1. **로컬 개발 완료 후**: [DEPLOY_GUIDE.md](./DEPLOY_GUIDE.md) 참고하여 Render 배포
2. **프론트엔드 배포**: Vercel 또는 Netlify에 배포
3. **커스터마이징**: 템플릿, 프롬프트 수정하여 자신만의 서비스 구축
4. **API 연동**: 다른 프론트엔드에서 API 사용 ([API_DOCUMENTATION.md](./API_DOCUMENTATION.md) 참고)

---

**Happy Coding! 🚀**
