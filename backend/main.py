from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import uvicorn
import os

from api.endpoints import router as api_router
from api.swot_endpoints import router as swot_router
from api.chatbot_endpoints import router as chatbot_router

app = FastAPI(
    title="마케팅 AI 어시스턴트 API",
    description="""
## 🎯 마케팅 AI 어시스턴트 v2.0

AI 기반 상세페이지 생성 & SWOT+3C 분석 플랫폼

### 주요 기능

#### 📝 상세페이지 생성
- AI 기반 콘텐츠 생성 (LangChain + LangGraph)
- DALL-E 3 이미지 생성
- 쿠팡/네이버 플랫폼 최적화
- Markdown/HTML 출력

#### 📊 SWOT + 3C 분석
- **실시간 경쟁사 검색** (Tavily API)
- **고급 검색 옵션**: 검색 기간, 상세도, 리뷰 포함
- **리뷰 분석**: 경쟁사 리뷰 자동 수집 및 인사이트 생성
- **SWOT 분석**: 강점, 약점, 기회, 위협
- **3C 분석**: 자사, 고객, 경쟁사
- **가격 비교**: 최저가 탐색
- **원클릭 생성**: SWOT 결과로 바로 상세페이지 생성

#### 💬 마케팅 챗봇
- AI 전략 상담
- 키워드 추천
- 타겟 분석
- 가격 전략

### 기술 스택
- FastAPI + LangChain + LangGraph
- OpenAI GPT-4o-mini + DALL-E 3
- Tavily API (실시간 웹 검색)
- React 18 + Material-UI
""",
    version="2.0.0",
    contact={
        "name": "GitHub Repository",
        "url": "https://github.com/sinyoung0110/marketing_chatbot"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static 파일 서빙 (이미지, HTML 등)
projects_dir = os.path.join(os.path.dirname(__file__), "projects")
os.makedirs(projects_dir, exist_ok=True)
app.mount("/projects", StaticFiles(directory=projects_dir), name="projects")
print(f"[Static Files] /projects mounted to {projects_dir}")

# API 라우터 등록
app.include_router(api_router, prefix="/api", tags=["Detail Page"])
app.include_router(swot_router, prefix="/api/swot", tags=["SWOT Analysis"])
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["Marketing Chatbot"])

@app.get("/")
async def root():
    return {
        "message": "E-commerce Detail Page Generator API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
