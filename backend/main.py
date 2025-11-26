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
    title="E-commerce Marketing Assistant",
    description="AI 기반 상세페이지 생성 & SWOT+3C 분석 플랫폼",
    version="2.0.0"
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
