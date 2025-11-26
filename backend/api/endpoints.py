from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict
import uuid
from datetime import datetime

from models.schemas import ProductInput, DetailPageResponse, ProjectMeta
from agents.workflow import DetailPageGenerator

router = APIRouter()

# 진행 중인 작업 추적
active_jobs: Dict[str, str] = {}

@router.post("/generate/detailpage", response_model=DetailPageResponse)
def generate_detail_page(
    product_input: ProductInput,
    background_tasks: BackgroundTasks
):
    """
    상세페이지 생성 API

    Args:
        product_input: 상품 입력 데이터

    Returns:
        DetailPageResponse: 생성된 상세페이지 정보
    """
    project_id = None
    try:
        # 프로젝트 ID 생성
        project_id = f"proj_{uuid.uuid4().hex[:8]}"

        # 작업 상태 저장
        active_jobs[project_id] = "processing"

        # 상세페이지 생성기 초기화
        generator = DetailPageGenerator(project_id)

        # 상세페이지 생성
        result = generator.generate(product_input)

        # 작업 완료
        active_jobs[project_id] = "completed"

        return DetailPageResponse(
            project_id=project_id,
            markdown_url=result["markdown_url"],
            html_url=result["html_url"],
            images=result["images"],
            meta=ProjectMeta(
                generated_at=datetime.now().isoformat(),
                platform=",".join(product_input.platforms),
                status="completed"
            )
        )

    except Exception as e:
        if project_id and project_id in active_jobs:
            active_jobs[project_id] = "failed"
        print(f"[API ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/project/{project_id}/status")
async def get_project_status(project_id: str):
    """프로젝트 상태 조회"""
    if project_id not in active_jobs:
        raise HTTPException(status_code=404, detail="Project not found")

    return {
        "project_id": project_id,
        "status": active_jobs[project_id]
    }

@router.get("/projects")
async def list_projects():
    """프로젝트 목록 조회"""
    return {
        "projects": [
            {"project_id": pid, "status": status}
            for pid, status in active_jobs.items()
        ]
    }
