"""
통합 워크플로우 엔드포인트
한 번 입력하면 SWOT → 상세페이지 → 챗봇까지 자동 연계
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import uuid
import os

from langchain_openai import ChatOpenAI
from utils.project_session import get_session_manager, ProjectSession
from tools.web_search import WebSearchTool
from tools.swot_3c_analysis import SWOT3CAnalysisTool
from tools.analysis_visualizer import AnalysisVisualizer
from tools.review_analyzer import ReviewAnalyzer
from agents.workflow import DetailPageGenerator

router = APIRouter()


class UnifiedStartRequest(BaseModel):
    """통합 워크플로우 시작 요청"""
    product_name: str
    category: str
    keywords: List[str] = []
    target_customer: str = ""
    platforms: List[str] = ["coupang", "naver"]


class UnifiedStartResponse(BaseModel):
    """통합 워크플로우 시작 응답"""
    session_id: str
    message: str
    next_step: str
    product_info: Dict


class SwotExecuteRequest(BaseModel):
    """SWOT 분석 실행 요청"""
    session_id: str
    search_depth: str = "advanced"
    days: Optional[int] = None
    include_reviews: bool = True


class SwotExecuteResponse(BaseModel):
    """SWOT 분석 실행 응답"""
    session_id: str
    analysis_result: Dict
    html_url: str
    competitor_count: int
    next_step: str


class DetailPageExecuteRequest(BaseModel):
    """상세페이지 생성 요청"""
    session_id: str
    platform: str = "coupang"
    tone: str = "친근한"
    image_style: str = "real"


class DetailPageExecuteResponse(BaseModel):
    """상세페이지 생성 응답"""
    session_id: str
    markdown_url: str
    html_url: str
    images: List[str]
    next_step: str


@router.post(
    "/start",
    summary="🚀 통합 워크플로우 시작",
    description="""
    **한 번 입력으로 SWOT → 상세페이지 → 챗봇까지 자동 연계**

    ### 💡 핵심 기능
    - 상품 정보를 한 번만 입력
    - 세션 ID를 통해 모든 단계에서 자동으로 데이터 재사용
    - 중복 입력 제거, UX 대폭 개선

    ### 📋 워크플로우
    1. `/unified/start` → 세션 생성 및 상품 정보 저장
    2. `/unified/execute-swot` → SWOT 분석 (자동으로 상품 정보 사용)
    3. `/unified/execute-detail` → 상세페이지 생성 (SWOT 결과 자동 반영)
    4. 챗봇에서 상담 (세션 컨텍스트 자동 로드)

    ### ⏱️ 시간 단축
    - 기존: 각 페이지마다 정보 입력 (5분 × 3 = 15분)
    - 개선: 한 번만 입력 (5분 + 0 + 0 = 5분)
    """,
    response_model=UnifiedStartResponse
)
async def start_unified_workflow(request: UnifiedStartRequest):
    """통합 워크플로우 시작"""
    try:
        # 세션 생성
        session_manager = get_session_manager()
        session = session_manager.create_session()

        # 상품 정보 저장
        product_info = {
            "product_name": request.product_name,
            "category": request.category,
            "keywords": request.keywords,
            "target_customer": request.target_customer,
            "platforms": request.platforms
        }
        session.update_product_info(product_info)
        session_manager.update_session(session)

        return {
            "session_id": session.session_id,
            "message": f"✅ 세션이 생성되었습니다! ({session.session_id})",
            "next_step": "swot",
            "product_info": product_info
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/execute-swot",
    summary="📊 SWOT 분석 실행",
    description="""
    **세션 기반 자동 SWOT 분석**

    - 세션에서 자동으로 상품 정보 로드
    - 재입력 불필요
    - 경쟁사 검색 + SWOT+3C 분석 + 리뷰 인사이트 자동 생성
    """,
    response_model=SwotExecuteResponse
)
async def execute_swot_analysis(request: SwotExecuteRequest):
    """SWOT 분석 실행 (세션 기반)"""
    try:
        # 세션 조회
        session_manager = get_session_manager()
        session = session_manager.get_session(request.session_id)

        if not session:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")

        # 상품 정보 자동 로드
        product_info = session.product_info
        if not product_info.get("product_name"):
            raise HTTPException(status_code=400, detail="상품 정보가 없습니다")

        # 경쟁사 검색
        web_search = WebSearchTool()
        search_query = f"{product_info['product_name']} {product_info['category']}"
        competitor_data = web_search.search(
            query=search_query,
            platforms=product_info.get("platforms", ["coupang", "naver"]),
            max_results=15,
            search_depth=request.search_depth,
            days=request.days,
            include_raw_content=request.include_reviews
        )

        # SWOT 분석
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))
        analyzer = SWOT3CAnalysisTool(llm)
        analysis_result = analyzer.analyze(
            product_input=product_info,
            competitor_data=competitor_data
        )

        # 리뷰 인사이트 (옵션)
        review_insights = None
        if request.include_reviews:
            review_analyzer = ReviewAnalyzer()
            all_reviews = []
            for result in competitor_data.get("results", []):
                if "reviews" in result:
                    all_reviews.extend(result["reviews"])

            if all_reviews:
                review_analysis = review_analyzer.analyze_reviews(
                    reviews=all_reviews,
                    product_name=product_info["product_name"]
                )
                review_insights = review_analyzer.generate_marketing_insights(
                    review_analysis=review_analysis,
                    product_input=product_info
                )

        # HTML 시각화
        visualizer = AnalysisVisualizer(session.session_id)
        html_path = visualizer.generate_html(
            analysis_result=analysis_result,
            product_input=product_info
        )

        # 세션에 저장
        session.set_swot_result(analysis_result, competitor_data)
        if review_insights:
            session.set_review_insights(review_insights)
        session_manager.update_session(session)

        # RAG에 SWOT 분석 저장 (챗봇이 활용할 수 있도록)
        try:
            from utils.rag_manager import get_rag_manager
            rag_manager = get_rag_manager()
            rag_manager.add_swot_analysis(
                product_name=product_info["product_name"],
                swot_analysis=analysis_result,
                metadata={
                    "category": product_info.get("category"),
                    "session_id": session.session_id
                }
            )
            print(f"[RAG] SWOT 분석 저장 완료: {product_info['product_name']}")
        except Exception as e:
            print(f"[RAG] SWOT 저장 실패 (무시): {e}")

        return {
            "session_id": session.session_id,
            "analysis_result": analysis_result,
            "html_url": html_path,
            "competitor_count": len(competitor_data.get("results", [])),
            "next_step": "detail"
        }

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/execute-detail",
    summary="📝 상세페이지 생성",
    description="""
    **SWOT 결과를 자동 반영한 상세페이지 생성**

    - 세션에서 상품 정보, SWOT 결과 자동 로드
    - 경쟁사 리뷰 인사이트 자동 반영
    - AI 기반 마케팅 카피 + DALL-E 3 이미지 생성
    """,
    response_model=DetailPageExecuteResponse
)
async def execute_detail_page(request: DetailPageExecuteRequest):
    """상세페이지 생성 (세션 기반)"""
    try:
        # 세션 조회
        session_manager = get_session_manager()
        session = session_manager.get_session(request.session_id)

        if not session:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")

        # 상품 정보 로드
        product_info = session.product_info.copy()

        # SWOT 결과가 있으면 자동 반영
        if session.swot_result:
            # SWOT 강점 → 키워드 추가
            swot_keywords = []
            if session.swot_result.get("swot", {}).get("strengths"):
                swot_keywords = session.swot_result["swot"]["strengths"][:3]

            # 기존 키워드와 병합
            existing_keywords = product_info.get("keywords", [])
            if isinstance(existing_keywords, str):
                existing_keywords = [k.strip() for k in existing_keywords.split(",")]
            product_info["keywords"] = list(set(existing_keywords + swot_keywords))

            # SWOT 인사이트 추가
            product_info["swot_insights"] = session.swot_result

        # 리뷰 인사이트 반영
        if session.review_insights:
            product_info["review_insights"] = session.review_insights

        # 플랫폼, 톤 설정
        product_info["platforms"] = [request.platform]
        product_info["tone"] = request.tone
        product_info["image_options"] = {
            "style": request.image_style,
            "shots": ["main", "usage", "infographic"]
        }

        # ProductInput 형식으로 변환
        from models.schemas import ProductInput
        product_input = ProductInput(**product_info)

        # 상세페이지 생성
        generator = DetailPageGenerator(session.session_id)
        result = generator.generate(product_input)

        # 세션에 저장
        session.set_detail_page_result(result)
        session_manager.update_session(session)

        return {
            "session_id": session.session_id,
            "markdown_url": result["markdown_url"],
            "html_url": result["html_url"],
            "images": result["images"],
            "next_step": "chat"
        }

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/session/{session_id}",
    summary="세션 조회",
    description="세션 ID로 현재 진행 상황 조회"
)
async def get_session_status(session_id: str):
    """세션 상태 조회"""
    try:
        session_manager = get_session_manager()
        session = session_manager.get_session(session_id)

        if not session:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")

        return {
            "session_id": session.session_id,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
            "current_step": session.current_step,
            "completed_steps": session.completed_steps,
            "product_info": session.product_info,
            "has_swot": session.swot_result is not None,
            "has_detail": session.detail_page_result is not None,
            "chat_count": len(session.chat_history)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/sessions",
    summary="모든 세션 목록",
    description="생성된 모든 세션 조회"
)
async def list_all_sessions():
    """모든 세션 목록"""
    try:
        session_manager = get_session_manager()
        sessions = session_manager.list_sessions()
        return {
            "total": len(sessions),
            "sessions": sessions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    "/session/{session_id}",
    summary="세션 삭제",
    description="세션 삭제"
)
async def delete_session(session_id: str):
    """세션 삭제"""
    try:
        session_manager = get_session_manager()
        session_manager.delete_session(session_id)
        return {"message": f"세션 {session_id}가 삭제되었습니다"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
