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
            분석 결과 (공통 포인트, 고객 불만, 가격 포지셔닝, 시각적 패턴, 경쟁사 리스트)
        """
        if not competitor_data.get("results"):
            return {
                "common_points": [],
                "customer_complaints": [],
                "price_positioning": None,
                "visual_patterns": [],
                "competitors": [],  # 경쟁사 리스트 추가
                "summary": "경쟁사 데이터 없음"
            }

        # 검색 결과 텍스트 추출 + 경쟁사 정보 수집
        texts = []
        competitors = []
        for idx, result in enumerate(competitor_data["results"][:5]):  # 최대 5개
            if "error" not in result:
                texts.append(f"제품 {idx+1}: {result.get('title', '')}\n설명: {result.get('snippet', '')}")

                # 경쟁사 정보 추출 (웹 검색 결과에서)
                competitors.append({
                    "name": result.get("title", "").split("-")[0].strip()[:30],  # 제목에서 상품명 추출
                    "price": self._extract_price(result.get("snippet", "")),
                    "delivery": "2-3일",  # 기본값
                    "rating": self._extract_rating(result.get("snippet", ""))
                })

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

            # 경쟁사 리스트 추가
            insights["competitors"] = competitors

            return insights

        except Exception as e:
            print(f"[CompetitorAnalysis] 분석 오류: {e}")
            return {
                "common_points": ["품질 강조", "빠른 배송", "가성비"],
                "customer_complaints": ["사이즈 불만", "포장 문제"],
                "price_positioning": "중가",
                "visual_patterns": ["제품 단독 이미지", "사용 장면"],
                "competitors": competitors,  # 경쟁사 리스트 포함
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

    def _extract_price(self, text: str) -> str:
        """텍스트에서 가격 추출"""
        import re
        # 가격 패턴: 숫자 + 원, 숫자,숫자원 등
        price_patterns = [
            r'(\d{1,3}(?:,\d{3})*)\s*원',
            r'(\d{1,3}(?:\.\d{3})*)\s*원',
            r'(\d+)\s*원'
        ]
        for pattern in price_patterns:
            match = re.search(pattern, text)
            if match:
                price = match.group(1).replace(',', '').replace('.', '')
                return f"{int(price):,}원"
        return "N/A"

    def _extract_rating(self, text: str) -> float:
        """텍스트에서 평점 추출"""
        import re
        # 평점 패턴: 4.5점, 별점 4.2, rating 4.3 등
        rating_patterns = [
            r'(\d\.\d)\s*점',
            r'별점\s*(\d\.\d)',
            r'rating\s*(\d\.\d)',
            r'평점\s*(\d\.\d)'
        ]
        for pattern in rating_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1))
        return 4.0  # 기본값
