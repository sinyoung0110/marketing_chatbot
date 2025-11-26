from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class ProductInput(BaseModel):
    """상품 입력 데이터 모델"""
    product_name: str = Field(..., description="상품명")
    summary: str = Field(..., max_length=30, description="한 줄 요약 (30자 이내)")
    category: str = Field(..., description="카테고리 (푸드/생활/전자 등)")
    manufacture_country: str = Field(..., description="제조국")
    manufacture_date: Optional[str] = Field(None, description="제조일")
    specs: Dict[str, str] = Field(..., description="제품 주요 스펙 (키:값)")
    keywords: List[str] = Field(..., description="핵심 키워드")
    target_customer: Optional[str] = Field(None, description="타겟 고객")
    tone: str = Field(default="친근한", description="톤 (전문적/친근한/감성적)")
    platforms: List[str] = Field(..., description="플랫폼 선택 (coupang/naver)")
    image_options: Dict[str, Any] = Field(
        default={"style": "real", "shots": ["main", "usage", "infographic"]},
        description="이미지 옵션"
    )
    competitor_links: Optional[List[str]] = Field(None, description="경쟁사 링크")
    allow_web_search: bool = Field(default=True, description="자동 웹 검색 허용")

class ImagePrompt(BaseModel):
    """이미지 프롬프트 모델"""
    type: str = Field(..., description="이미지 타입 (main/usage/infographic)")
    prompt: str = Field(..., description="이미지 생성 프롬프트")
    size: str = Field(default="1000x1000", description="이미지 크기")

class GeneratedContent(BaseModel):
    """생성된 콘텐츠 모델"""
    project_id: str
    markdown_url: str
    html_url: str
    images: List[str]
    meta: Dict[str, Any]

class ProjectMeta(BaseModel):
    """프로젝트 메타 정보"""
    generated_at: str
    platform: str
    status: str = Field(default="completed", description="생성 상태")

class SellingPoint(BaseModel):
    """셀링 포인트 모델"""
    title: str
    description: str
    evidence: Optional[str] = None

class CompetitorInsight(BaseModel):
    """경쟁사 인사이트 모델"""
    common_points: List[str]
    customer_complaints: List[str]
    price_positioning: Optional[str] = None
    visual_patterns: List[str]

class DetailPageResponse(BaseModel):
    """상세페이지 생성 응답 모델"""
    project_id: str
    markdown_url: str
    html_url: str
    images: List[str]
    meta: ProjectMeta
