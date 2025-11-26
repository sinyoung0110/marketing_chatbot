"""
셀링 포인트 생성 도구
"""
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import json

class SellingPointGenerator:
    """셀링 포인트 생성기"""

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def generate(self, product_input: Dict, competitor_insights: Dict) -> List[Dict]:
        """
        USP (Unique Selling Points) 생성

        Args:
            product_input: 상품 입력 정보
            competitor_insights: 경쟁사 인사이트

        Returns:
            셀링 포인트 리스트 (3-6개)
        """
        system_prompt = """당신은 e-커머스 마케팅 카피라이터입니다.
상품 정보와 경쟁사 분석을 바탕으로 강력한 USP(Unique Selling Points)를 생성하세요.

각 셀링 포인트는:
1. **간결한 제목** (5-10자)
2. **설명** (20-40자)
3. **증거/근거** (선택적, 있으면 신뢰도 향상)

형식 (JSON):
[
  {
    "title": "셀링 포인트 제목",
    "description": "구체적인 설명",
    "evidence": "증거나 데이터 (선택)"
  }
]

원칙:
- 경쟁사와 차별화되는 점 강조
- 고객 불만을 해결하는 포인트 우선
- 구체적인 숫자나 사실 활용
- 감성적 + 이성적 균형"""

        user_prompt = f"""상품 정보:
- 이름: {product_input['product_name']}
- 카테고리: {product_input['category']}
- 주요 스펙: {product_input.get('specs', {})}
- 키워드: {product_input.get('keywords', [])}
- 제조국: {product_input.get('manufacture_country', '알 수 없음')}

경쟁사 인사이트:
- 공통 포인트: {competitor_insights.get('common_points', [])}
- 고객 불만: {competitor_insights.get('customer_complaints', [])}
- 가격 포지셔닝: {competitor_insights.get('price_positioning', '중가')}

3-6개의 강력한 USP를 생성해주세요."""

        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])

            content = response.content

            # JSON 추출
            import re
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                selling_points = json.loads(json_match.group())
                return selling_points[:6]  # 최대 6개
            else:
                # JSON이 아니면 기본값 반환
                return self._create_default_selling_points(product_input)

        except Exception as e:
            print(f"[SellingPoint] 생성 오류: {e}")
            return self._create_default_selling_points(product_input)

    def _create_default_selling_points(self, product_input: Dict) -> List[Dict]:
        """기본 셀링 포인트 생성"""
        specs = product_input.get('specs', {})
        keywords = product_input.get('keywords', [])

        selling_points = [
            {
                "title": "최상의 품질",
                "description": f"{product_input['manufacture_country']} 제조로 품질 보증",
                "evidence": f"{product_input.get('manufacture_country', '국내')} 생산"
            },
            {
                "title": "합리적 가격",
                "description": "가성비 최고의 선택",
                "evidence": None
            }
        ]

        # 스펙 기반 추가
        for key, value in list(specs.items())[:2]:
            selling_points.append({
                "title": key,
                "description": f"{key}: {value}",
                "evidence": value
            })

        # 키워드 기반 추가
        for keyword in keywords[:2]:
            selling_points.append({
                "title": keyword,
                "description": f"{keyword} 특화 제품",
                "evidence": None
            })

        return selling_points[:6]
