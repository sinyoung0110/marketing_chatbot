# 🚀 Render 백엔드 배포 가이드

## 📋 목차
1. [사전 준비](#1-사전-준비)
2. [GitHub 레포지토리 설정](#2-github-레포지토리-설정)
3. [Render 배포](#3-render-배포)
4. [환경변수 설정](#4-환경변수-설정)
5. [배포 확인](#5-배포-확인)
6. [프론트엔드 연결](#6-프론트엔드-연결)
7. [트러블슈팅](#7-트러블슈팅)

---

## 1. 사전 준비

### 필요한 것들
- ✅ GitHub 계정
- ✅ Render 계정 (무료) - https://render.com
- ✅ OpenAI API Key - https://platform.openai.com/api-keys
- ✅ Tavily API Key (선택) - https://tavily.com

### API Key 발급

#### OpenAI API Key (필수)
1. https://platform.openai.com 접속
2. 로그인 후 우측 상단 프로필 → "API keys" 클릭
3. "Create new secret key" 클릭
4. 이름 입력 후 생성
5. **생성된 키를 복사** (한 번만 표시됨!)

   ```
   sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

#### Tavily API Key (선택 - 고급 검색용)
1. https://tavily.com 접속
2. 회원가입 후 대시보드 접속
3. "API Keys" 메뉴에서 키 확인
4. 무료 플랜: 월 1,000회 검색 가능

   ```
   tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 2. GitHub 레포지토리 설정

### 2-1. 현재 코드를 GitHub에 푸시

터미널에서 실행:

```bash
# 현재 위치 확인
pwd
# /Users/sinyoung/marketing_chatbot

# Git 상태 확인
git status

# 변경사항 커밋
git add .
git commit -m "Add Render deployment configuration"

# GitHub에 푸시
git push origin main
```

### 2-2. GitHub 레포지토리 확인

브라우저에서 다음 파일들이 있는지 확인:
- ✅ `render.yaml` (루트 디렉토리)
- ✅ `backend/requirements.txt`
- ✅ `backend/main.py`
- ✅ `backend/.env.example`

---

## 3. Render 배포

### 3-1. Render 가입 및 로그인

1. https://render.com 접속
2. "Get Started for Free" 클릭
3. GitHub 계정으로 로그인 (권장)

### 3-2. New Web Service 생성

1. 대시보드에서 **"New +"** 버튼 클릭
2. **"Web Service"** 선택
3. GitHub 레포지토리 연결
   - "Connect a repository" 클릭
   - `marketing_chatbot` 레포지토리 선택
   - "Connect" 클릭

### 3-3. 서비스 설정

다음 정보를 입력:

| 항목 | 값 |
|------|-----|
| **Name** | `marketing-chatbot-backend` (원하는 이름) |
| **Region** | `Oregon (US West)` 또는 `Singapore` (한국과 가까움) |
| **Branch** | `main` |
| **Root Directory** | (비워둠) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r backend/requirements.txt` |
| **Start Command** | `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT` |

**Instance Type** 선택:
- ✅ **Free** 선택 (0$/month)
- 특징:
  - 750시간/월 무료
  - 15분 비활성 시 sleep
  - 512MB RAM

### 3-4. 고급 설정 (Advanced)

"Advanced" 버튼 클릭 후:

**Health Check Path** 설정:
```
/health
```

**Auto-Deploy** 설정:
- ✅ "Yes" 선택 (GitHub push 시 자동 재배포)

---

## 4. 환경변수 설정

### 4-1. Environment Variables 추가

Render 대시보드에서:

1. 왼쪽 메뉴에서 **"Environment"** 클릭
2. **"Add Environment Variable"** 클릭

다음 환경변수들을 추가:

#### 필수 환경변수

| Key | Value | 설명 |
|-----|-------|------|
| `OPENAI_API_KEY` | `sk-proj-xxx...` | OpenAI API 키 (1단계에서 발급) |
| `PYTHON_VERSION` | `3.11.0` | Python 버전 |

#### 선택 환경변수

| Key | Value | 설명 |
|-----|-------|------|
| `TAVILY_API_KEY` | `tvly-xxx...` | Tavily API 키 (고급 검색용) |

### 4-2. 저장 및 배포

1. **"Save Changes"** 클릭
2. 자동으로 재배포 시작됨
3. 로그 확인: **"Logs"** 탭에서 배포 진행 상황 확인

---

## 5. 배포 확인

### 5-1. 배포 상태 확인

Render 대시보드에서:

1. **"Logs"** 탭 클릭
2. 다음 메시지가 보이면 성공:
   ```
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:10000
   ```

3. **"Events"** 탭에서 "Deploy live" 확인

### 5-2. API 테스트

배포된 URL 확인:
```
https://marketing-chatbot-backend.onrender.com
```

브라우저에서 테스트:

#### 1. 루트 엔드포인트
```
https://your-app-name.onrender.com/
```

**예상 응답:**
```json
{
  "message": "E-commerce Detail Page Generator API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

#### 2. 헬스 체크
```
https://your-app-name.onrender.com/health
```

**예상 응답:**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-05T..."
}
```

#### 3. Swagger UI (API 문서)
```
https://your-app-name.onrender.com/docs
```

브라우저에서 열면 **인터랙티브 API 문서**가 표시됨!

### 5-3. 첫 API 호출 테스트

Swagger UI에서:

1. **POST /api/unified/start** 클릭
2. "Try it out" 클릭
3. Request body 입력:
   ```json
   {
     "product_name": "테스트 상품",
     "category": "테스트",
     "keywords": ["테스트"],
     "target_customer": "테스트 고객",
     "platforms": ["coupang"]
   }
   ```
4. "Execute" 클릭
5. 응답 확인:
   ```json
   {
     "session_id": "sess_xxx",
     "message": "✅ 세션이 생성되었습니다!",
     ...
   }
   ```

---

## 6. 프론트엔드 연결

### 6-1. 백엔드 URL 확인

Render 대시보드 상단에서 URL 복사:
```
https://marketing-chatbot-backend.onrender.com
```

### 6-2. 프론트 개발자에게 전달

다음 정보를 전달:

**API Base URL:**
```
https://marketing-chatbot-backend.onrender.com
```

**API 문서:**
- Swagger UI: `https://marketing-chatbot-backend.onrender.com/docs`
- API 정의서: `API_DOCUMENTATION.md` 파일

**환경변수 설정 방법 (프론트):**

React 프로젝트의 `.env` 파일:
```bash
REACT_APP_BACKEND_URL=https://marketing-chatbot-backend.onrender.com
```

Next.js 프로젝트:
```bash
NEXT_PUBLIC_BACKEND_URL=https://marketing-chatbot-backend.onrender.com
```

### 6-3. CORS 설정 확인

백엔드 코드 (`backend/main.py:61`)에서 CORS 설정 확인:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**프로덕션 권장 설정:**
```python
allow_origins=[
    "https://your-frontend.vercel.app",
    "https://your-frontend.netlify.app"
],
```

---

## 7. 트러블슈팅

### 문제 1: 배포 실패 (Build failed)

**증상:**
```
ERROR: Could not find a version that satisfies the requirement ...
```

**해결 방법:**
1. `backend/requirements.txt` 확인
2. Python 버전 확인 (환경변수 `PYTHON_VERSION=3.11.0`)
3. Render 대시보드에서 "Manual Deploy" → "Clear build cache & deploy"

---

### 문제 2: 서버가 시작되지 않음

**증상:**
```
ERROR: Application startup failed
```

**해결 방법:**
1. Render 로그 확인
2. 환경변수 확인 (`OPENAI_API_KEY` 등)
3. Start Command 확인:
   ```bash
   cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

---

### 문제 3: API 호출 시 500 에러

**증상:**
```json
{
  "detail": "Internal server error"
}
```

**해결 방법:**
1. Render 로그에서 에러 확인
2. 환경변수 확인 (특히 `OPENAI_API_KEY`)
3. Swagger UI (`/docs`)에서 개별 엔드포인트 테스트

---

### 문제 4: Sleep 문제 (15분 후 서버 다운)

**증상:**
- 15분 이상 요청 없으면 서버 sleep
- 다음 요청 시 ~1분 대기

**해결 방법 (무료 플랜):**

**방법 1: 프론트에서 로딩 표시**
```javascript
// 첫 API 호출 시
setLoading(true);
setMessage("서버를 깨우는 중입니다... (최대 1분 소요)");

const response = await fetch(`${API_URL}/api/unified/start`, {
  method: 'POST',
  ...
});
```

**방법 2: 헬스 체크 크론잡 설정 (외부 서비스)**

UptimeRobot (무료): https://uptimerobot.com
- 5분마다 `/health` 엔드포인트 호출
- Sleep 방지

**방법 3: 유료 플랜 ($7/월)**
- Sleep 없음
- 항상 켜져있음

---

### 문제 5: CORS 에러

**증상:**
```
Access to fetch at 'https://...' from origin 'http://localhost:3000'
has been blocked by CORS policy
```

**해결 방법:**

`backend/main.py` 수정:
```python
allow_origins=[
    "http://localhost:3000",  # 로컬 개발
    "https://your-frontend.vercel.app"  # 프로덕션
]
```

변경 후:
```bash
git add backend/main.py
git commit -m "Update CORS settings"
git push origin main
```

Render가 자동으로 재배포됨!

---

### 문제 6: 파일 업로드 실패 (PDF)

**증상:**
```
413 Request Entity Too Large
```

**해결 방법:**

Render 무료 플랜은 파일 업로드 제한이 있음 (보통 10MB)

`backend/main.py`에 크기 제한 추가:
```python
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/api/upload")
async def upload(file: UploadFile = File(..., max_size=10_000_000)):  # 10MB
    ...
```

---

## 8. 모니터링 및 관리

### 8-1. 로그 확인

Render 대시보드:
1. **"Logs"** 탭 클릭
2. 실시간 로그 확인
3. 에러 발생 시 자동으로 표시

### 8-2. 메트릭 확인

**"Metrics"** 탭에서:
- CPU 사용량
- 메모리 사용량
- 응답 시간
- 요청 수

### 8-3. 재배포

**수동 재배포:**
1. Render 대시보드에서 "Manual Deploy" 클릭
2. "Deploy latest commit" 클릭

**자동 재배포:**
- GitHub에 push하면 자동으로 재배포됨!

```bash
git add .
git commit -m "Update feature"
git push origin main
```

---

## 9. 비용 및 제한사항

### 무료 플랜 (Free)

**포함 사항:**
- ✅ 750시간/월 (약 31일)
- ✅ 512MB RAM
- ✅ 무제한 대역폭
- ✅ SSL 인증서 자동
- ✅ GitHub 자동 배포

**제한사항:**
- ⚠️ 15분 비활성 시 sleep
- ⚠️ 파일 저장 시 재배포 시 삭제
- ⚠️ 동시 요청 제한

### 유료 플랜 (Starter - $7/월)

**추가 혜택:**
- ✅ Sleep 없음 (항상 켜져있음)
- ✅ 더 많은 RAM (선택 가능)
- ✅ 우선 지원

---

## 10. 다음 단계

백엔드 배포 완료 후:

### 1. 프론트엔드 배포 (Vercel/Netlify)
- `DEPLOY_FRONTEND.md` 참고

### 2. 도메인 연결 (선택)
- Render 대시보드에서 "Custom Domain" 설정

### 3. 모니터링 설정
- Sentry, LogRocket 등 에러 트래킹 도구 연동

---

## 📞 지원

**문제 발생 시:**
1. Render 로그 확인
2. `API_DOCUMENTATION.md` 참고
3. Swagger UI로 API 테스트
4. GitHub Issues 등록

**유용한 링크:**
- Render 문서: https://render.com/docs
- FastAPI 문서: https://fastapi.tiangolo.com
- 프로젝트 API 문서: `API_DOCUMENTATION.md`

---

**작성일:** 2024-12-05
**작성자:** Claude Code
**버전:** 1.0.0
