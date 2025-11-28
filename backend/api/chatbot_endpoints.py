"""
마케팅 전략 챗봇 엔드포인트
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

router = APIRouter()

class ChatMessage(BaseModel):
    """채팅 메시지"""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    """채팅 요청"""
    message: str
    conversation_history: List[Dict] = []  # role, content
    session_context: Optional[Dict] = None  # 세션 컨텍스트 (SWOT, 상세페이지 등)

class QuickActionRequest(BaseModel):
    """빠른 작업 요청"""
    action: str  # 'generate_page', 'analyze_swot', 'suggest_keywords'
    product_info: Dict

# 마케팅 전략 시스템 프롬프트
MARKETING_SYSTEM_PROMPT = """당신은 전문 마케팅 전략가이자 e-커머스 컨설턴트입니다.

역할:
1. 상품 마케팅 전략 제안
2. SWOT/3C 분석 해석 및 인사이트 제공
3. 상세페이지 구성 조언
4. 타겟 고객 분석
5. 경쟁사 대응 전략

답변 스타일:
- 구체적이고 실행 가능한 조언
- 데이터 기반 인사이트
- 간결하고 명확한 표현
- 필요시 단계별 가이드 제공

특별 기능:
사용자가 요청하면 다음 작업을 수행할 수 있습니다:
- "/상세페이지 생성" → 상세페이지 자동 생성
- "/SWOT 분석" → 경쟁사 분석 시작
- "/키워드 추천" → SEO 키워드 제안
- "/가격 전략" → 가격 포지셔닝 조언
"""

@router.post("/chat")
async def chat_with_bot(request: ChatRequest):
    """
    마케팅 챗봇과 대화 (세션 컨텍스트 활용)
    """
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # 메시지 히스토리 구성
        messages = [SystemMessage(content=MARKETING_SYSTEM_PROMPT)]

        # 세션 컨텍스트 추가 (SWOT 분석, 상세페이지 정보)
        if request.session_context:
            context_parts = []

            product_info = request.session_context.get('product_info', {})
            if product_info:
                context_parts.append(f"상품명: {product_info.get('product_name', '')}")
                context_parts.append(f"카테고리: {product_info.get('category', '')}")
                if product_info.get('keywords'):
                    keywords = product_info['keywords']
                    if isinstance(keywords, list):
                        context_parts.append(f"키워드: {', '.join(keywords)}")

            # RAG에서 SWOT 정보 자동 로드
            if product_info.get('product_name'):
                try:
                    from utils.rag_manager import get_rag_manager
                    rag_manager = get_rag_manager()
                    swot_docs = rag_manager.get_context_for_product(
                        product_name=product_info['product_name'],
                        category=product_info.get('category')
                    )
                    if swot_docs:
                        context_parts.append(f"\n[SWOT 분석 결과]\n{swot_docs}")
                except Exception as e:
                    print(f"[Chatbot] RAG 로드 실패 (무시): {e}")

            if context_parts:
                context_text = "\n\n=== 현재 프로젝트 정보 ===\n" + "\n".join(context_parts)
                messages.append(SystemMessage(content=context_text))

        # 이전 대화 추가
        for msg in request.conversation_history[-10:]:  # 최근 10개만
            if msg.get('role') == "user":
                messages.append(HumanMessage(content=msg.get('content', '')))
            elif msg.get('role') == "assistant":
                messages.append(AIMessage(content=msg.get('content', '')))

        # 현재 메시지
        messages.append(HumanMessage(content=request.message))

        # LLM 호출
        response = llm.invoke(messages)

        return {
            "response": response.content,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        import traceback
        print(f"[Chatbot] 오류: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quick-action")
async def execute_quick_action(request: QuickActionRequest):
    """
    빠른 작업 실행
    """
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        if request.action == "suggest_keywords":
            # SEO 키워드 추천
            prompt = f"""
상품 정보:
- 이름: {request.product_info.get('name', '')}
- 카테고리: {request.product_info.get('category', '')}

위 상품에 적합한 SEO 키워드 10개를 추천하세요.
검색량이 높고 경쟁이 낮은 롱테일 키워드 포함.

JSON 형식으로 답변:
{{"keywords": ["키워드1", "키워드2", ...]}}
"""

        elif request.action == "analyze_target":
            # 타겟 고객 분석
            prompt = f"""
상품: {request.product_info.get('name', '')}

이 상품의 주요 타겟 고객을 3가지 페르소나로 분석하세요:
1. 인구통계학적 특성
2. 구매 동기
3. 페인 포인트

JSON 형식으로 답변.
"""

        elif request.action == "price_strategy":
            # 가격 전략
            prompt = f"""
상품: {request.product_info.get('name', '')}
현재 가격: {request.product_info.get('price', '미정')}

가격 전략을 제안하세요:
1. 포지셔닝 (고가/중가/저가)
2. 근거
3. 프로모션 아이디어

JSON 형식으로 답변.
"""

        else:
            raise HTTPException(status_code=400, detail="알 수 없는 작업")

        response = llm.invoke([
            SystemMessage(content=MARKETING_SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ])

        return {
            "action": request.action,
            "result": response.content,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"[Quick Action] 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/suggestions")
async def get_suggestions(product_name: str, category: str):
    """
    상품 기반 마케팅 제안
    """
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        prompt = f"""
상품: {product_name}
카테고리: {category}

이 상품의 마케팅 전략을 간략히 제안하세요:
1. 핵심 셀링 포인트 3가지
2. 주요 타겟 고객
3. 추천 플랫폼 (쿠팡/네이버/11번가 등)
4. 가격대 제안

간결하고 실행 가능하게 작성하세요.
"""

        response = llm.invoke([
            SystemMessage(content=MARKETING_SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ])

        return {
            "suggestions": response.content,
            "product_name": product_name,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"[Suggestions] 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def _format_context(context: Dict) -> str:
    """컨텍스트를 텍스트로 포맷"""
    parts = []

    if "product_name" in context:
        parts.append(f"상품명: {context['product_name']}")

    if "category" in context:
        parts.append(f"카테고리: {context['category']}")

    if "swot_analysis" in context:
        parts.append(f"\n최근 SWOT 분석 결과 있음")

    if "price_range" in context:
        parts.append(f"가격대: {context['price_range']}")

    return "\n".join(parts)

def _detect_quick_actions(content: str) -> List[str]:
    """응답에서 빠른 작업 버튼 감지"""
    actions = []

    keywords = {
        "상세페이지": "generate_page",
        "SWOT": "analyze_swot",
        "키워드": "suggest_keywords",
        "가격": "price_strategy",
        "타겟": "analyze_target"
    }

    for keyword, action in keywords.items():
        if keyword in content:
            actions.append(action)

    return list(set(actions))[:3]  # 최대 3개
