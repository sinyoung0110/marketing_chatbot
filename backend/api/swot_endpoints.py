"""
SWOT + 3C 분석 전용 엔드포인트
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import uuid

from tools.web_search import WebSearchTool
from tools.swot_3c_analysis import SWOT3CAnalysisTool
from tools.analysis_visualizer import AnalysisVisualizer
from langchain_openai import ChatOpenAI
import os

router = APIRouter()

class SearchRequest(BaseModel):
    """검색 요청"""
    query: str
    platforms: List[str] = ["coupang", "naver"]
    max_results: int = 10
    date_range: Optional[str] = "최근 30일"

class AnalysisRequest(BaseModel):
    """분석 요청"""
    product_name: str
    category: str
    keywords: List[str] = []
    target: str = ""
    search_results: Optional[List[Dict]] = None

class RefineSearchRequest(BaseModel):
    """검색 결과 수정 및 재검색 요청"""
    original_query: str
    refined_query: str
    platforms: List[str]
    exclude_urls: List[str] = []
    max_results: int = 10

@router.post("/search")
async def search_competitors(request: SearchRequest):
    """
    경쟁사 상품 검색

    사용자가 검색어, 플랫폼, 기간을 지정하여 검색
    """
    try:
        web_search = WebSearchTool()

        print(f"[SWOT Search] 검색 시작: {request.query}")
        print(f"[SWOT Search] 플랫폼: {request.platforms}")
        print(f"[SWOT Search] 최대 결과: {request.max_results}")

        # 웹 검색 실행
        results = web_search.search(
            query=request.query,
            platforms=request.platforms,
            max_results=request.max_results
        )

        # 검색 메타데이터 추가
        results["search_metadata"] = {
            "query": request.query,
            "platforms": request.platforms,
            "date_range": request.date_range,
            "timestamp": datetime.now().isoformat(),
            "total_results": len(results.get("results", []))
        }

        return results

    except Exception as e:
        print(f"[SWOT Search] 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_competitors(request: AnalysisRequest):
    """
    SWOT + 3C 분석 수행

    검색 결과를 바탕으로 분석 실행
    """
    try:
        print(f"[SWOT Analysis] 분석 시작: {request.product_name}")

        # LLM 초기화
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # 분석기 초기화
        analyzer = SWOT3CAnalysisTool(llm)

        # 검색 결과가 없으면 새로 검색
        if not request.search_results:
            web_search = WebSearchTool()
            search_query = f"{request.product_name} {request.category}"
            competitor_data = web_search.search(
                query=search_query,
                platforms=["coupang", "naver"],
                max_results=15
            )
        else:
            competitor_data = {"results": request.search_results}

        # 분석 실행
        product_input = {
            "product_name": request.product_name,
            "category": request.category,
            "keywords": request.keywords,
            "target": request.target
        }

        analysis_result = analyzer.analyze(
            product_input=product_input,
            competitor_data=competitor_data
        )

        # 프로젝트 ID 생성
        project_id = f"swot_{uuid.uuid4().hex[:8]}"

        # HTML 시각화
        visualizer = AnalysisVisualizer(project_id)
        html_path = visualizer.generate_html(
            analysis_result=analysis_result,
            product_input=product_input
        )

        return {
            "analysis": analysis_result,
            "html_url": html_path,
            "project_id": project_id,
            "search_results_count": len(competitor_data.get("results", []))
        }

    except Exception as e:
        print(f"[SWOT Analysis] 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refine-search")
async def refine_search(request: RefineSearchRequest):
    """
    검색 결과 수정 및 재검색

    사용자가 검색어를 수정하거나 특정 URL을 제외하고 재검색
    """
    try:
        web_search = WebSearchTool()

        print(f"[SWOT Refine] 재검색 시작")
        print(f"[SWOT Refine] 원본 쿼리: {request.original_query}")
        print(f"[SWOT Refine] 수정 쿼리: {request.refined_query}")
        print(f"[SWOT Refine] 제외 URL: {len(request.exclude_urls)}개")

        # 재검색
        results = web_search.search(
            query=request.refined_query,
            platforms=request.platforms,
            max_results=request.max_results * 2  # 필터링을 위해 더 많이 검색
        )

        # 제외할 URL 필터링
        if request.exclude_urls:
            filtered_results = []
            for result in results.get("results", []):
                if result.get("url") not in request.exclude_urls:
                    filtered_results.append(result)

            results["results"] = filtered_results[:request.max_results]

        # 메타데이터 추가
        results["search_metadata"] = {
            "original_query": request.original_query,
            "refined_query": request.refined_query,
            "excluded_count": len(request.exclude_urls),
            "timestamp": datetime.now().isoformat(),
            "total_results": len(results.get("results", []))
        }

        return results

    except Exception as e:
        print(f"[SWOT Refine] 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize")
async def summarize_document(url: str, content: Optional[str] = None):
    """
    문서 요약

    URL 또는 텍스트 내용을 요약
    """
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage

        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # 내용이 없으면 URL에서 가져오기 (간단한 구현)
        if not content:
            content = f"URL: {url}"

        system_prompt = """당신은 마케팅 전문가입니다.
제공된 내용을 다음 관점에서 요약하세요:
1. 주요 제품 특징
2. 가격 정보
3. 고객 리뷰 하이라이트
4. 경쟁 우위 요소

간결하고 핵심만 추출하세요."""

        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"다음 내용을 요약하세요:\n\n{content[:3000]}")
        ])

        return {
            "url": url,
            "summary": response.content,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"[Summarize] 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))
