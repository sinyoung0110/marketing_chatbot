"""
경쟁사 분석 도구
"""
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

class CompetitorAnalysisTool:
    """경쟁사 데이터 분석 도구"""

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def analyze(self, competitor_data: Dict) -> Dict:
        """
        경쟁사 데이터 분석

        Args:
            competitor_data: 웹 검색 결과

        Returns:
            분석 결과 (공통 포인트, 고객 불만, 가격 포지셔닝, 시각적 패턴)
        """
        if not competitor_data.get("results"):
            return {
                "common_points": [],
                "customer_complaints": [],
                "price_positioning": None,
                "visual_patterns": [],
                "summary": "경쟁사 데이터 없음"
            }

        # 검색 결과 텍스트 추출
        texts = []
        for result in competitor_data["results"]:
            if "error" not in result:
                texts.append(f"제목: {result.get('title', '')}\n내용: {result.get('snippet', '')}")

        combined_text = "\n\n".join(texts[:10])  # 최대 10개만 분석

        # LLM으로 인사이트 추출
        system_prompt = """당신은 e-커머스 경쟁 분석 전문가입니다.
제공된 경쟁 상품 정보를 분석하여 다음을 추출하세요:

1. **공통 셀링 포인트**: 여러 경쟁사가 강조하는 공통 특징 (3-5개)
2. **고객 불만 사항**: 리뷰나 Q&A에서 언급되는 문제점 (3-5개)
3. **가격 포지셔닝**: 경쟁사의 평균 가격대 및 전략
4. **시각적 패턴**: 상세페이지에서 자주 사용되는 이미지 스타일이나 레이아웃

JSON 형식으로 답변하세요."""

        user_prompt = f"""경쟁 상품 정보:

{combined_text}

위 정보를 분석하여 인사이트를 추출해주세요."""

        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])

            # JSON 파싱 시도
            import json
            import re

            content = response.content
            # JSON 블록 추출
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                insights = json.loads(json_match.group())
            else:
                # JSON이 아니면 기본 구조 반환
                insights = self._parse_text_response(content)

            return insights

        except Exception as e:
            print(f"[CompetitorAnalysis] 분석 오류: {e}")
            return {
                "common_points": ["품질 강조", "빠른 배송", "가성비"],
                "customer_complaints": ["사이즈 불만", "포장 문제"],
                "price_positioning": "중가",
                "visual_patterns": ["제품 단독 이미지", "사용 장면"],
                "summary": f"분석 중 오류 발생: {str(e)}"
            }

    def _parse_text_response(self, text: str) -> Dict:
        """텍스트 응답을 파싱하여 딕셔너리로 변환"""
        return {
            "common_points": self._extract_list(text, "공통"),
            "customer_complaints": self._extract_list(text, "불만"),
            "price_positioning": self._extract_text(text, "가격"),
            "visual_patterns": self._extract_list(text, "시각"),
            "summary": text[:200]
        }

    def _extract_list(self, text: str, keyword: str) -> List[str]:
        """텍스트에서 리스트 추출"""
        import re
        pattern = rf'{keyword}[^:]*:\s*(.+?)(?:\n\n|\Z)'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            items = re.findall(r'[-•]\s*(.+)', match.group(1))
            return items[:5]
        return []

    def _extract_text(self, text: str, keyword: str) -> str:
        """텍스트에서 특정 섹션 추출"""
        import re
        pattern = rf'{keyword}[^:]*:\s*(.+?)(?:\n\n|\Z)'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()[:100]
        return ""
