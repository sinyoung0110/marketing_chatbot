# SellFlow AI - 마케팅 자동화 챗봇 시스템

AI 기반 e-커머스 마케팅 자동화 플랫폼으로, SWOT 분석부터 상세페이지 생성, 챗봇 상담까지 통합된 워크플로우를 제공합니다.

## 📋 프로젝트 개요

### 주요 기능
1. **통합 워크플로우**: 한 번 입력으로 SWOT 분석 → 상세페이지 생성 → 챗봇 상담까지 자동 연계
2. **SWOT + 3C 분석**: 경쟁사 자동 분석 및 시각화된 HTML 보고서 생성
3. **AI 상세페이지 생성**: 카테고리별 맞춤형 상세페이지 및 이미지 자동 생성
4. **마케팅 챗봇**: 프로젝트 컨텍스트 기반 실시간 마케팅 전략 상담

### 기술 스택
- **Backend**: FastAPI, Python 3.12
- **Frontend**: React, Material-UI
- **AI/LLM**: LangChain, OpenAI GPT-4o-mini, DALL-E 3
- **검색**: Tavily API, DuckDuckGo
- **벡터 DB**: ChromaDB

## 🚀 프로젝트 실행 방법

### 사전 요구사항
- Python 3.12 이상
- Node.js 18 이상
- npm

### 1. API 키 발급

#### OpenAI API 키 (필수)
1. [OpenAI Platform](https://platform.openai.com/) 접속
2. 회원가입 후 로그인
3. 우측 상단 프로필 → "API keys" 클릭
4. "Create new secret key" 버튼 클릭
5. 생성된 키 복사 (한 번만 표시되므로 안전한 곳에 보관)

#### Tavily API 키 (선택 - 고급 검색 기능용)
1. [Tavily](https://tavily.com/) 접속
2. 회원가입 후 로그인
3. Dashboard에서 API 키 발급
4. 무료 플랜: 월 1,000회 검색 가능

### 2. 환경 설정

#### Backend 설정
```bash
# 백엔드 디렉토리로 이동
cd backend

# 가상환경 생성 (선택사항이지만 권장)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows

# 패키지 설치
pip3 install -r requirements.txt

# .env 파일 생성
cp .env.example .env

# .env 파일 편집 (발급받은 API 키 입력)
# 텍스트 에디터로 .env 파일 열기:
# nano .env
# 또는
# vi .env

# 아래 내용 입력:
# OPENAI_API_KEY=발급받은_OpenAI_키
# TAVILY_API_KEY=발급받은_Tavily_키 (선택)
```

#### Frontend 설정
```bash
# 새 터미널을 열고 프론트엔드 디렉토리로 이동
cd frontend

# 패키지 설치
npm install
```

### 3. 실행

#### Backend 실행 (첫 번째 터미널)
```bash
cd backend
python3 main.py
```
서버가 `http://localhost:8000`에서 실행됩니다.
"Application startup complete" 메시지가 표시되면 성공입니다.

#### Frontend 실행 (두 번째 터미널)
```bash
cd frontend
npm start
```
브라우저가 자동으로 `http://localhost:3000`에서 열립니다.

## 📁 프로젝트 구조

```
marketing_chatbot/
├── backend/
│   ├── api/                    # API 엔드포인트
│   ├── agents/                 # AI 에이전트 워크플로우
│   ├── tools/                  # 핵심 도구
│   ├── templates/              # HTML 템플릿
│   ├── utils/                  # 유틸리티
│   ├── main.py                 # FastAPI 서버 엔트리포인트
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/             # React 페이지 컴포넌트
│   │   └── App.js
│   ├── package.json
│   └── public/
├── projects/                   # 생성된 프로젝트 저장소 (자동 생성)
└── README.md
```

## 🔑 API 키 보안

**⚠️ 중요**: `.env` 파일은 절대 GitHub에 업로드하지 마세요!

- `.env.example` 파일을 복사하여 `.env` 파일 생성
- API 키는 `.env` 파일에만 저장
- `.gitignore`에 `.env` 파일이 포함되어 있어 자동으로 Git에서 제외됨

## 💡 사용 방법

### 1. 통합 워크플로우
1. `http://localhost:3000` 접속
2. 상품 정보 입력 (상품명, 카테고리, 키워드 등)
3. "워크플로우 시작" 클릭
4. SWOT + 3C 분석 실행
5. 분석 결과 확인 및 수정 (선택)
6. 상세페이지 생성
7. 챗봇에서 마케팅 전략 상담

### 2. SWOT 분석
- 자동으로 경쟁사 검색 및 리뷰 분석
- 강점, 약점, 기회, 위협 자동 도출
- HTML 보고서로 결과 확인

### 3. 상세페이지 생성
- 카테고리별 최적화된 템플릿 자동 선택 (뷰티, 식품, 패션, 전자제품 등)
- 셀링 포인트 기반 맞춤형 이미지 자동 생성
- 경쟁사 비교 테이블 포함

### 4. 마케팅 챗봇
- 프로젝트 컨텍스트 기반 실시간 상담
- 상세페이지 수정 요청 가능
- 예시: "상세페이지 제목을 ABC로 바꿔줘"

## ⚠️ 주의사항

### 파일 경로
- 모든 파일 경로는 **상대경로** 사용
- 프로젝트 루트 디렉토리를 기준으로 동작
- **절대경로 사용 없음** - 별도 수정 불필요

### 데이터 폴더
- `projects/`: 생성된 HTML, 이미지 등이 자동으로 저장됨 (자동 생성)
- `backend/data/chroma_store/`: 벡터 데이터베이스 (자동 생성)
- `backend/sessions/`: 프로젝트 세션 정보 (자동 생성)

**참고**: 첫 실행 시 ChromaDB가 비어있어 챗봇이 과거 프로젝트를 기억하지 못하지만, 새로 생성한 프로젝트는 정상적으로 저장되고 챗봇에서 사용 가능합니다.

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

# 포트 충돌 확인
lsof -i :8000  # 8000번 포트 사용 확인
lsof -i :3000  # 3000번 포트 사용 확인
```

### 패키지 설치 오류
```bash
# pip 업그레이드
pip3 install --upgrade pip

# 가상환경 재생성
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### ChromaDB 오류
```bash
# ChromaDB 폴더 삭제 후 재시작
rm -rf chromadb
python3 main.py  # 자동으로 재생성됨
```

## 📦 생성되는 파일

프로젝트 실행 시 자동으로 생성되는 파일/폴더:
- `projects/<session_id>/`: 각 프로젝트별 저장소
  - `swot_analysis_<timestamp>.html`: SWOT 분석 결과
  - `detail_page_<timestamp>.html`: 상세페이지
  - `images/`: 생성된 이미지 파일
- `chromadb/`: 벡터 데이터베이스

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

---

## 📞 추가 정보

### 개발 환경
- macOS Sonoma / Windows 10/11
- Python 3.12.0
- Node.js 18.17.0
- npm 9.6.7

### 권장 브라우저
- Chrome 최신 버전
- Safari 최신 버전
- Firefox 최신 버전

### 성능
- SWOT 분석: 평균 30-60초
- 상세페이지 생성: 평균 60-90초 (이미지 생성 포함)
- 챗봇 응답: 평균 2-5초
