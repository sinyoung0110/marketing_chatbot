"""
통합 워크플로우 엔드포인트
한 번 입력하면 SWOT → 상세페이지 → 챗봇까지 자동 연계
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import uuid
import os
import json
import tempfile

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
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
    search_platforms: Optional[List[str]] = None  # 검색 플랫폼
    sort_by: str = "popular"  # 정렬 기준


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

        # 검색 플랫폼이 지정되지 않으면 기본값 사용
        search_platforms = request.search_platforms or ['coupang', 'naver', 'news', 'blog']

        # 기본적으로 최근 90일 이내 데이터만 검색 (품절/중단 상품 제외)
        search_days = request.days if request.days else 90

        competitor_data = web_search.search(
            query=search_query,
            platforms=product_info.get("platforms", ["coupang", "naver"]),
            max_results=15,
            search_depth=request.search_depth,
            days=search_days,  # 최근 데이터만
            include_raw_content=request.include_reviews,
            search_platforms=search_platforms,
            sort_by=request.sort_by
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
            product_input=product_info,
            competitor_data=competitor_data,
            review_insights=review_insights
        )

        # 파일 경로를 URL 경로로 변환
        # html_path: projects/proj_xxx/analysis.html
        # url_path: /outputs/proj_xxx/analysis.html
        html_url = html_path.replace("projects/", "/outputs/")

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
            "html_url": html_url,
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
            "shots": ["main", "detail1", "detail2", "detail3", "detail4", "detail5"]
        }

        # ProductInput 형식으로 변환
        from models.schemas import ProductInput
        product_input = ProductInput(**product_info)

        # 상세페이지 생성
        generator = DetailPageGenerator(session.session_id)
        result = generator.generate(product_input)

        # 세션에 저장 (content_sections 포함)
        session.set_detail_page_result(result, result.get("content_sections"))
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


class UpdateContentSectionsRequest(BaseModel):
    """콘텐츠 섹션 업데이트 요청"""
    session_id: str
    step: str  # "swot" 또는 "detail"
    updated_sections: Dict[str, Any]


@router.post(
    "/update-content-sections",
    summary="📝 콘텐츠 섹션 업데이트",
    description="""
    **섹션별로 수정된 내용을 반영하여 HTML 재생성**

    - SWOT: strengths, weaknesses, opportunities, threats 수정 가능
    - 상세페이지: headline, summary, detailed_description 등 수정 가능
    - 수정된 내용으로 새 HTML 파일 생성
    """
)
async def update_content_sections(request: UpdateContentSectionsRequest):
    """콘텐츠 섹션 업데이트 및 HTML 재생성"""
    try:
        session_manager = get_session_manager()
        session = session_manager.get_session(request.session_id)

        if not session:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")

        if request.step == "swot":
            # SWOT 분석 업데이트
            if not session.swot_result:
                raise HTTPException(status_code=400, detail="SWOT 분석 결과가 없습니다")

            # 기존 SWOT 결과 복사
            updated_swot = session.swot_result.copy()

            # 업데이트된 섹션 반영
            if "swot" in request.updated_sections:
                for key, value in request.updated_sections["swot"].items():
                    if key in updated_swot.get("swot", {}):
                        updated_swot["swot"][key] = value

            # HTML 재생성
            visualizer = AnalysisVisualizer(session.session_id)
            html_path = visualizer.generate_html(
                analysis_result=updated_swot,
                product_input=session.product_info,
                competitor_data=session.competitor_data or {},
                review_insights=session.review_insights
            )

            html_url = html_path.replace("projects/", "/outputs/")

            # 세션 업데이트
            session.set_swot_result(updated_swot, session.competitor_data)
            session_manager.update_session(session)

            return {
                "session_id": session.session_id,
                "html_url": html_url,
                "message": "SWOT 분석이 업데이트되었습니다"
            }

        elif request.step == "detail":
            # 상세페이지 업데이트
            if not session.detail_page_result or not session.content_sections:
                raise HTTPException(status_code=400, detail="상세페이지 결과가 없습니다")

            # 기존 content_sections 복사
            content_sections = session.content_sections.copy()

            # 업데이트된 섹션 병합
            content_sections.update(request.updated_sections)

            # HTML 재생성
            from tools.exporter import ContentExporter
            exporter = ContentExporter(session.session_id)

            markdown_path, html_path = exporter.export(
                content_sections=content_sections,
                images=session.detail_page_result.get("images", []),
                product_input=session.product_info
            )

            # 세션 업데이트
            session.update_content_sections(content_sections)
            updated_result = session.detail_page_result.copy()
            updated_result["html_url"] = html_path
            updated_result["markdown_url"] = markdown_path
            session.set_detail_page_result(updated_result, content_sections)
            session_manager.update_session(session)

            return {
                "session_id": session.session_id,
                "html_url": html_path,
                "markdown_url": markdown_path,
                "message": "상세페이지가 업데이트되었습니다"
            }
        else:
            raise HTTPException(status_code=400, detail="step은 'swot' 또는 'detail'이어야 합니다")

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

        # SWOT 결과 정보
        swot_info = None
        if session.swot_result:
            swot_info = {
                "html_url": f"/outputs/{session.session_id}/analysis.html"
            }

        # 상세페이지 결과 정보
        detail_info = None
        if session.detail_page_result:
            detail_info = {
                "html_url": session.detail_page_result.get("html_url"),
                "markdown_url": session.detail_page_result.get("markdown_url")
            }

        return {
            "session_id": session.session_id,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
            "current_step": session.current_step,
            "completed_steps": session.completed_steps,
            "product_info": session.product_info,
            "has_swot": session.swot_result is not None,
            "has_detail": session.detail_page_result is not None,
            "swot_result": swot_info,
            "detail_result": detail_info,
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


class UpdateSwotRequest(BaseModel):
    """SWOT 수정 요청"""
    session_id: str
    swot_updates: Dict[str, Any]  # {"strengths": [...], "weaknesses": [...]}


@router.post(
    "/update-swot",
    summary="✏️ SWOT 분석 수정",
    description="""
    **세션의 SWOT 분석 결과를 수정합니다**

    - 챗봇 대화 없이 직접 SWOT 데이터 업데이트
    - 수정된 내용은 세션에 저장되어 챗봇이 참조 가능
    - HTML 보고서 자동 재생성
    """
)
async def update_swot_analysis(request: UpdateSwotRequest):
    """SWOT 분석 직접 수정"""
    try:
        # 세션 조회
        session_manager = get_session_manager()
        session = session_manager.get_session(request.session_id)

        if not session:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")

        if not session.swot_result:
            raise HTTPException(status_code=400, detail="SWOT 분석 결과가 없습니다")

        # SWOT 결과 업데이트
        current_swot = session.swot_result.get("swot", {})
        current_swot.update(request.swot_updates)
        session.swot_result["swot"] = current_swot

        # HTML 재생성
        visualizer = AnalysisVisualizer(session.session_id)
        html_path = visualizer.generate_html(
            analysis_result=session.swot_result,
            product_input=session.product_info,
            competitor_data=session.competitor_data,
            review_insights=session.review_insights
        )

        # 세션 저장
        session_manager.update_session(session)

        html_url = html_path.replace("projects/", "/outputs/")

        return {
            "success": True,
            "message": "SWOT 분석이 수정되었습니다",
            "html_url": html_url,
            "updated_swot": current_swot
        }

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/parse-pdf",
    summary="📄 PDF 파일 파싱",
    description="""
    **PDF 파일에서 상품 정보 추출**

    - PDF 파일을 업로드하면 AI가 자동으로 상품 정보 추출
    - 추출 항목: 상품명, 카테고리, 키워드, 타겟 고객
    - 통합 워크플로우에서 바로 사용 가능
    """
)
async def parse_pdf_file(file: UploadFile = File(...)):
    """PDF 파일에서 상품 정보 추출 (최대 50MB)"""
    try:
        # PDF 파일 검증
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다")

        # 파일 크기 확인 (50MB 제한)
        content = await file.read()
        file_size_mb = len(content) / (1024 * 1024)

        if file_size_mb > 50:
            raise HTTPException(
                status_code=400,
                detail=f"파일 크기가 너무 큽니다 ({file_size_mb:.1f}MB). 최대 50MB까지 업로드 가능합니다."
            )

        print(f"[PDF Upload] 파일명: {file.filename}, 크기: {file_size_mb:.2f}MB")

        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            # PDF 텍스트 추출 (PyMuPDF 사용)
            import fitz  # PyMuPDF
            pdf_text = ""
            pdf_doc = fitz.open(tmp_path)

            print(f"[PDF Parse] PDF 페이지 수: {len(pdf_doc)}")

            for page_num, page in enumerate(pdf_doc):
                page_text = page.get_text()
                pdf_text += page_text + "\n"
                print(f"[PDF Parse] 페이지 {page_num + 1}: {len(page_text)} 문자 추출 (일반 텍스트)")

            pdf_doc.close()

            print(f"[PDF Parse] 전체 추출된 텍스트 길이: {len(pdf_text.strip())} 문자")

            # 텍스트가 비어있거나 너무 적으면 OCR 시도
            if len(pdf_text.strip()) < 50:
                print(f"[PDF Parse] 일반 텍스트 추출 실패 또는 부족 ({len(pdf_text.strip())} 문자). OCR 시도...")

                try:
                    from pdf2image import convert_from_path
                    import pytesseract
                    from PIL import Image

                    # PDF를 이미지로 변환 (해상도 300 DPI)
                    print(f"[PDF OCR] PDF를 이미지로 변환 중...")
                    images = convert_from_path(tmp_path, dpi=300)
                    print(f"[PDF OCR] {len(images)}개 이미지 변환 완료")

                    # OCR로 각 페이지에서 텍스트 추출 (한국어 + 영어)
                    ocr_text = ""
                    for i, image in enumerate(images):
                        print(f"[PDF OCR] 페이지 {i + 1} OCR 처리 중...")
                        # 한국어(kor) + 영어(eng) 동시 인식
                        page_ocr_text = pytesseract.image_to_string(image, lang='kor+eng')
                        ocr_text += page_ocr_text + "\n"
                        print(f"[PDF OCR] 페이지 {i + 1}: {len(page_ocr_text)} 문자 추출 (OCR)")

                    print(f"[PDF OCR] 전체 OCR 텍스트 길이: {len(ocr_text.strip())} 문자")

                    if len(ocr_text.strip()) > 50:
                        pdf_text = ocr_text
                        print(f"[PDF OCR] OCR 성공! 추출된 텍스트 첫 200자:\n{ocr_text[:200]}")
                    else:
                        raise HTTPException(
                            status_code=400,
                            detail=f"PDF에서 텍스트를 추출할 수 없습니다 (OCR 결과: {len(ocr_text.strip())} 문자). PDF에 읽을 수 있는 텍스트나 이미지가 포함되어 있는지 확인해주세요."
                        )

                except ImportError as ie:
                    print(f"[PDF OCR] OCR 라이브러리 오류: {ie}")
                    raise HTTPException(
                        status_code=500,
                        detail="OCR 라이브러리가 설치되지 않았습니다. pytesseract와 pdf2image가 필요합니다."
                    )
                except Exception as ocr_error:
                    print(f"[PDF OCR] OCR 오류: {ocr_error}")
                    raise HTTPException(
                        status_code=400,
                        detail=f"OCR 처리 실패: {str(ocr_error)}"
                    )
            else:
                print(f"[PDF Parse] 일반 텍스트 추출 성공! 첫 200자:\n{pdf_text[:200]}")

            # LLM으로 구조화된 정보 추출
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.3,
                api_key=os.getenv("OPENAI_API_KEY")
            )

            extraction_prompt = f"""
다음 PDF 텍스트에서 상품 마케팅에 필요한 정보를 추출하세요.

PDF 텍스트:
{pdf_text[:3000]}

아래 JSON 형식으로 정보를 추출하세요. 정보가 없으면 빈 문자열이나 빈 배열을 사용하세요:

{{
  "product_name": "상품명",
  "category": "카테고리",
  "keywords": ["키워드1", "키워드2", "키워드3"],
  "target_customer": "타겟 고객층",
  "platforms": ["coupang", "naver"]
}}

**중요**:
- product_name: 가장 중요한 상품명 (브랜드명 포함)
- category: 상품 카테고리 (예: 식품, 전자제품, 패션 등)
- keywords: 상품의 특징을 나타내는 키워드 3-5개
- target_customer: 주요 타겟 고객층 (예: 20-30대 여성, 직장인 등)
- platforms: 판매 플랫폼 (coupang, naver 등)

JSON만 반환하세요.
"""

            response = llm.invoke([
                SystemMessage(content="당신은 상품 정보 추출 전문가입니다. PDF에서 마케팅에 필요한 정보를 정확히 추출합니다."),
                HumanMessage(content=extraction_prompt)
            ])

            # JSON 파싱
            result_text = response.content.strip()

            # JSON 코드 블록 제거
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]

            result_text = result_text.strip()

            # JSON 파싱
            product_info = json.loads(result_text)

            # 기본값 설정
            if not product_info.get("product_name"):
                raise HTTPException(status_code=400, detail="PDF에서 상품명을 찾을 수 없습니다")

            if not product_info.get("category"):
                product_info["category"] = "기타"

            if not product_info.get("keywords"):
                product_info["keywords"] = []

            if not product_info.get("target_customer"):
                product_info["target_customer"] = ""

            if not product_info.get("platforms"):
                product_info["platforms"] = ["coupang", "naver"]

            return {
                "success": True,
                "message": "PDF 파싱 완료",
                **product_info
            }

        finally:
            # 임시 파일 삭제
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"AI 응답 파싱 실패: {str(e)}")
    except HTTPException:
        # HTTPException은 그대로 전달
        raise
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[PDF Parse] 오류 발생:")
        print(error_trace)

        # 사용자에게 더 자세한 에러 메시지 제공
        error_msg = str(e)
        if "fitz" in error_msg or "PyMuPDF" in error_msg:
            error_msg = "PDF 파일을 읽을 수 없습니다. 파일이 손상되었거나 암호화되어 있을 수 있습니다."
        elif "OPENAI_API_KEY" in error_msg:
            error_msg = "OpenAI API 키가 설정되지 않았습니다."
        elif len(error_msg) > 200:
            error_msg = error_msg[:200] + "..."

        raise HTTPException(status_code=500, detail=f"PDF 분석 실패: {error_msg}")


class UpdateMarkdownRequest(BaseModel):
    """마크다운 업데이트 요청"""
    session_id: str
    markdown_content: str
    step: str  # 'swot' or 'detail'


@router.post(
    "/update-markdown",
    summary="✏️ 마크다운 콘텐츠 수정",
    description="""
    **마크다운 편집 후 저장 API**

    - 사용자가 편집한 마크다운을 저장
    - HTML을 자동으로 재생성
    - 다음 단계에서도 수정된 내용 반영
    """
)
async def update_markdown(request: UpdateMarkdownRequest):
    """마크다운 콘텐츠 업데이트 및 HTML 재생성"""
    session_manager = get_session_manager()
    session = session_manager.get_session(request.session_id)

    if not session:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")

    try:
        # 세션에서 프로젝트 경로 가져오기
        project_id = f"proj_{request.session_id[:8]}"
        project_dir = os.path.join("backend", "projects", project_id)
        os.makedirs(project_dir, exist_ok=True)

        # 마크다운 파일 저장
        if request.step == 'swot':
            md_filename = "analysis.md"
            html_filename = "analysis.html"
        else:
            md_filename = "detail.md"
            html_filename = "detail.html"

        md_path = os.path.join(project_dir, md_filename)
        html_path = os.path.join(project_dir, html_filename)

        # 마크다운 저장
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(request.markdown_content)

        # HTML 재생성 (간단한 마크다운 -> HTML 변환)
        import markdown
        html_content = markdown.markdown(request.markdown_content, extensions=['tables', 'fenced_code'])

        # HTML 템플릿으로 래핑
        full_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{'SWOT+3C 분석' if request.step == 'swot' else '상세페이지'}</title>
    <style>
        body {{
            font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
            line-height: 1.6;
            max-width: 860px;
            margin: 0 auto;
            padding: 20px;
            background: #fafdfb;
            color: #0f1720;
        }}
        h1, h2, h3 {{
            color: #0f766e;
            border-bottom: 2px solid #e6eef0;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #e6eef0;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: #0f766e;
            color: white;
        }}
        code {{
            background: #f8f9fa;
            padding: 2px 6px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""

        # HTML 저장
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

        # 세션 데이터 업데이트
        if request.step == 'swot':
            session.data['swot_analysis'] = {
                'markdown_updated': True,
                'html_url': f"/outputs/{project_id}/{html_filename}"
            }
        else:
            session.data['detail_page'] = {
                'markdown_updated': True,
                'html_url': f"/outputs/{project_id}/{html_filename}",
                'markdown_url': f"/outputs/{project_id}/{md_filename}"
            }

        session_manager.save_session(session)

        return {
            "success": True,
            "message": "마크다운이 성공적으로 업데이트되었습니다",
            "html_url": f"/outputs/{project_id}/{html_filename}",
            "markdown_url": f"/outputs/{project_id}/{md_filename}"
        }

    except Exception as e:
        import traceback
        print(f"[Markdown Update] 오류: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"마크다운 업데이트 실패: {str(e)}")
