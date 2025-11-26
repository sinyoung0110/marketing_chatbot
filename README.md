# 🎯 마케팅 AI 어시스턴트 v2.0

> AI 기반 상세페이지 생성 & SWOT+3C 분석 플랫폼

쿠팡·네이버 스토어 전용 상세페이지를 AI로 자동 생성하고, 실시간 경쟁사 분석을 통해 마케팅 전략을 제공하는 올인원 플랫폼입니다.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![React](https://img.shields.io/badge/react-18.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## ✨ 주요 기능

### 📝 페이지 1: 상세페이지 자동 생성
- **AI 기반 콘텐츠 생성**: LangChain + LangGraph 멀티 에이전트 워크플로우
- **실사 같은 이미지**: DALL-E 3로 덜 AI스러운, 자연스러운 제품 이미지 생성
- **플랫폼 최적화**: 쿠팡/네이버 스토어 규격에 맞춘 템플릿
- **다양한 출력 형식**: Markdown, HTML, 이미지 파일

### 📊 페이지 2: SWOT + 3C 분석
- **실시간 경쟁사 검색**: Tavily API로 최신 상품 정보 수집
- **검색 결과 편집**: URL 체크박스 선택 후 제외하고 재검색 가능
- **SWOT 분석**: 강점, 약점, 기회, 위협 자동 분석
- **3C 분석**: 자사, 고객, 경쟁사 전략 분석
- **가격 비교**: 최저가 상품 탐색 및 가격대 분석
- **문서 요약**: 경쟁사 URL 내용 자동 요약
- **시각화 보고서**: 아름다운 HTML 보고서 생성

### 💬 페이지 3: 마케팅 전략 챗봇
- **AI 마케팅 컨설턴트**: 실시간 전략 상담
- **빠른 작업**:
  - SEO 키워드 추천
  - 타겟 고객 분석
  - 가격 전략 제안
- **페이지 연동**: 챗봇에서 바로 상세페이지 생성/SWOT 분석으로 이동

---

## 🎨 스크린샷

### 네비게이션
```
┌─────────────────────────────────────────┐
│  🎯 마케팅 AI 어시스턴트            v2.0 │
│  [상세페이지 생성] [SWOT+3C 분석] [챗봇] │
└─────────────────────────────────────────┘
```

### SWOT 분석 페이지
- 1️⃣ 경쟁사 검색 (Tavily)
- 2️⃣ 검색 결과 편집 (체크박스로 URL 제외)
- 3️⃣ 상품 정보 입력
- 4️⃣ SWOT + 3C 분석 실행
- ✅ 아름다운 HTML 보고서

---

## 📁 프로젝트 구조

```
marketing_chatbot/
├── backend/                    # FastAPI 백엔드
│   ├── main.py                # FastAPI 앱 진입점
│   ├── agents/
│   │   └── workflow.py        # LangGraph 워크플로우 (11개 노드)
│   ├── api/
│   │   ├── endpoints.py       # 상세페이지 생성 API
│   │   ├── swot_endpoints.py  # SWOT+3C 분석 API (신규)
│   │   └── chatbot_endpoints.py  # 마케팅 챗봇 API (신규)
│   ├── tools/
│   │   ├── web_search.py      # Tavily 웹 검색 (개선)
│   │   ├── competitor_analysis.py
│   │   ├── swot_3c_analysis.py    # SWOT+3C 분석기 (신규)
│   │   ├── analysis_visualizer.py # HTML 시각화 (신규)
│   │   ├── selling_point.py
│   │   ├── image_gen.py       # 더 사실적인 이미지 프롬프트
│   │   └── exporter.py
│   ├── templates/
│   │   └── platform_templates.py
│   ├── models/
│   │   └── schemas.py
│   └── utils/
│       └── rag_manager.py
├── frontend/                   # React 프론트엔드
│   ├── src/
│   │   ├── App.js             # React Router 설정
│   │   ├── components/
│   │   │   ├── Navigation.js  # 네비게이션 바 (신규)
│   │   │   ├── ProductInputForm.js
│   │   │   ├── PreviewPanel.js
│   │   │   └── ResultView.js  # SWOT 링크 추가
│   │   └── pages/
│   │       ├── DetailPageGenerator.js  # 페이지 1
│   │       ├── SwotAnalyzer.js        # 페이지 2 (신규)
│   │       └── MarketingChatbot.js    # 페이지 3 (신규)
│   └── package.json
├── projects/                   # 생성된 결과물
├── .env                       # API 키 설정
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 설치 및 실행

### 1. 저장소 클론

```bash
git clone https://github.com/sinyoung0110/marketing_chatbot.git
cd marketing_chatbot
```

### 2. 백엔드 설정

```bash
# Python 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 추가 패키지 (Tavily)
pip install tavily-python
```

### 3. 프론트엔드 설정

```bash
cd frontend
npm install
cd ..
```

### 4. 환경 변수 설정

`backend/.env` 파일 생성:

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. 실행

#### 백엔드 (터미널 1)

```bash
cd backend
python3 main.py
```

→ http://localhost:8000
→ API 문서: http://localhost:8000/docs

#### 프론트엔드 (터미널 2)

```bash
cd frontend
npm start
```

→ http://localhost:3000

---

## 📖 사용 방법

### 페이지 1: 상세페이지 생성

1. 상품 정보 입력 (상품명, 카테고리, 키워드 등)
2. 플랫폼 선택 (쿠팡/네이버)
3. 이미지 옵션 선택
4. "생성하기" 클릭
5. Markdown/HTML 다운로드

### 페이지 2: SWOT + 3C 분석

1. **검색**: "에어프라이어 감자칩" 입력
2. **플랫폼 선택**: 쿠팡, 네이버 체크
3. **검색 실행** → 15개 결과 확인
4. **URL 편집**: 불필요한 URL 체크박스 선택
5. **재검색**: "제외하고 재검색" 클릭
6. **상품 정보 입력**: 분석할 상품 정보 입력
7. **분석 실행** → HTML 보고서 다운로드

### 페이지 3: 마케팅 챗봇

1. 상품 정보 설정 (우측 사이드바)
2. 질문 입력: "감자칩 마케팅 전략 알려줘"
3. AI 응답 확인
4. 빠른 작업 버튼 클릭:
   - [키워드 추천]
   - [가격 전략]
   - [타겟 분석]
5. 다른 페이지로 바로 이동

---

## 🔧 API 엔드포인트

### 상세페이지 생성

```bash
POST /api/generate/detailpage
```

### SWOT + 3C 분석

```bash
POST /api/swot/search          # 경쟁사 검색
POST /api/swot/analyze         # SWOT+3C 분석
POST /api/swot/refine-search   # 재검색
POST /api/swot/summarize       # 문서 요약
```

### 마케팅 챗봇

```bash
POST /api/chatbot/chat         # 대화
POST /api/chatbot/quick-action # 빠른 작업
GET  /api/chatbot/suggestions  # 제안
```

---

## 🛠️ 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **LangChain**: LLM 애플리케이션 프레임워크
- **LangGraph**: 멀티 에이전트 오케스트레이션
- **Tavily**: 실시간 웹 검색 API
- **OpenAI GPT-4o-mini**: 텍스트 생성
- **DALL-E 3**: 이미지 생성

### Frontend
- **React 18**: UI 라이브러리
- **React Router v6**: 페이지 라우팅
- **Material-UI**: 컴포넌트 라이브러리

### AI/ML
- **GPT-4o-mini**: 마케팅 카피, SWOT 분석, 챗봇
- **DALL-E 3**: 사실적인 제품 이미지 생성
- **Tavily API**: 실시간 경쟁사 검색

---

## 🎯 v2.0 업데이트 내용

### ✅ 새로운 기능

1. **3페이지 구조**
   - 상세페이지 생성
   - SWOT + 3C 분석
   - 마케팅 챗봇

2. **실시간 웹 검색**
   - DuckDuckGo → Tavily API로 전환
   - 더 정확한 검색 결과

3. **SWOT + 3C 자동 분석**
   - 강점/약점/기회/위협
   - 자사/고객/경쟁사 분석
   - 가격 비교 및 최저가 탐색

4. **검색 결과 편집**
   - URL 체크박스 선택
   - 제외하고 재검색 기능

5. **마케팅 챗봇**
   - AI 전략 상담
   - 키워드 추천
   - 타겟 분석
   - 가격 전략

6. **이미지 개선**
   - 더 사실적인 프롬프트
   - Canon/Nikon 카메라 언급
   - Documentary style
   - 자연광 강조

7. **시각화 보고서**
   - 아름다운 HTML 디자인
   - 그라데이션 스타일
   - 핵심 인사이트 요약

---

## 📊 워크플로우

### 상세페이지 생성 (11개 노드)

```
InputCollector → RAG Loader → CompetitorSearch → CompetitorInsights
→ SWOT+3C Analysis → Visualize → SellingPoints → ContentAssembly
→ ImagePrompts → ImageGen → Export
```

### SWOT 분석 워크플로우

```
Search (Tavily) → Filter URLs → Refine Search → Analyze
→ Generate SWOT/3C → Visualize HTML
```

---

## 🎨 샘플 출력

### SWOT 분석 보고서 (HTML)

```html
📊 SWOT + 3C 분석 보고서
생성일: 2025-11-26

🎯 핵심 인사이트
💪 핵심 강점: 100% 국산 신선한 감자 사용
🎯 시장 기회: 건강 간식 시장의 성장세
💰 경쟁 가격대: 3,000원 ~ 8,000원 (평균 5,500원)
🏷️ 최저가: ABC 감자칩 - 3,000원

📈 SWOT 분석
[강점 카드] [약점 카드]
[기회 카드] [위협 카드]

🔍 3C 분석
[자사 카드] [고객 카드] [경쟁사 카드]

💰 가격 분석
[최저가/평균가/최고가]
[상위 5개 최저가 상품 테이블]
```

---

## 🔐 보안

- OpenAI/Tavily API 키는 `.env` 파일로 관리
- Git에 커밋 금지 (`.gitignore` 설정)
- 민감한 데이터는 로컬 저장만

---

## 🚧 향후 개선 계획

- [ ] 포스터 스타일 템플릿 (대형 이미지 중심)
- [ ] 분석 보고서 PDF 다운로드
- [ ] 챗봇 대화 저장 기능
- [ ] 플랫폼 자동 업로드 (API 연동)
- [ ] A/B 테스트 복수 버전 생성
- [ ] 다국어 지원

---

## 📄 라이선스

MIT License - 개인 및 상업적 사용 가능

---

## 👥 기여

기여를 환영합니다! Pull Request를 보내주세요.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 문의

프로젝트 관련 문의: [GitHub Issues](https://github.com/sinyoung0110/marketing_chatbot/issues)

---

## 🎉 감사합니다!

이 프로젝트는 AI 기반 마케팅 자동화를 목표로 개발되었습니다.
실무에서 바로 사용 가능한 수준의 품질을 제공합니다! 🚀
