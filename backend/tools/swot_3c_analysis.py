"""
SWOT + 3C 분석 도구
"""
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import json
import re


class SWOT3CAnalysisTool:
    """SWOT + 3C 분석 전문 도구"""

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def analyze(self, product_input: Dict, competitor_data: Dict) -> Dict:
        """
        SWOT + 3C 통합 분석

        Args:
            product_input: 자사 상품 정보
            competitor_data: 경쟁사 검색 결과

        Returns:
            SWOT + 3C 분석 결과
        """
        # 경쟁사 데이터 추출
        competitor_texts = self._extract_competitor_texts(competitor_data)

        # SWOT 분석
        swot = self._analyze_swot(product_input, competitor_texts)

        # 3C 분석
        three_c = self._analyze_3c(product_input, competitor_texts)

        # 가격 분석
        price_analysis = self._analyze_prices(competitor_data)

        # 핵심 인사이트
        insights = self._generate_insights(swot, three_c, price_analysis)

        return {
            "swot": swot,
            "three_c": three_c,
            "price_analysis": price_analysis,
            "insights": insights,
            "competitor_count": len([r for r in competitor_data.get("results", []) if "error" not in r])
        }

    def _extract_competitor_texts(self, competitor_data: Dict) -> List[str]:
        """경쟁사 데이터에서 텍스트 추출"""
        texts = []
        for result in competitor_data.get("results", []):
            if "error" not in result:
                text = f"""
                제품명: {result.get('title', '')}
                URL: {result.get('url', '')}
                설명: {result.get('snippet', '')}
                플랫폼: {result.get('platform', '')}
                """
                texts.append(text)
        return texts[:15]  # 최대 15개

    def _analyze_swot(self, product_input: Dict, competitor_texts: List[str]) -> Dict:
        """SWOT 분석 수행"""
        system_prompt = """당신은 마케팅 전략 전문가입니다.
제공된 자사 상품과 경쟁사 정보를 바탕으로 SWOT 분석을 수행하세요.

SWOT 분석 항목:
1. Strengths (강점): 자사 상품의 경쟁 우위 요소
2. Weaknesses (약점): 개선이 필요한 부분
3. Opportunities (기회): 시장에서 활용 가능한 기회
4. Threats (위협): 경쟁사나 시장 환경의 위협 요소

각 항목당 3-5개씩 구체적으로 작성하고, JSON 형식으로 답변하세요."""

        user_prompt = f"""
자사 상품 정보:
- 상품명: {product_input.get('product_name', '')}
- 카테고리: {product_input.get('category', '')}
- 키워드: {', '.join(product_input.get('keywords', []))}
- 타겟: {product_input.get('target', '')}

경쟁사 상품 정보:
{chr(10).join(competitor_texts[:10])}

위 정보를 바탕으로 SWOT 분석을 수행해주세요.
"""

        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])

            content = response.content
            swot = self._parse_json_response(content)

            if not swot or not isinstance(swot, dict):
                return {
                    "strengths": ["분석 데이터 부족"],
                    "weaknesses": ["경쟁사 정보 부족"],
                    "opportunities": ["시장 조사 필요"],
                    "threats": ["경쟁 심화"]
                }

            return swot

        except Exception as e:
            print(f"[SWOT Analysis] 분석 오류: {e}")
            return {
                "strengths": ["분석 오류"],
                "weaknesses": ["데이터 부족"],
                "opportunities": ["추가 조사 필요"],
                "threats": ["경쟁 심화"]
            }

    def _analyze_3c(self, product_input: Dict, competitor_texts: List[str]) -> Dict:
        """3C 분석 수행"""
        system_prompt = """당신은 비즈니스 전략 전문가입니다.
3C 분석 프레임워크를 사용하여 분석하세요.

3C 분석 항목:
1. Company (자사): 자사의 강점, 자원, 역량
2. Customer (고객): 타겟 고객의 니즈, 페인 포인트, 구매 동기
3. Competitor (경쟁사): 주요 경쟁사의 전략, 강점, 약점

각 항목당 3-5개씩 구체적으로 작성하고, JSON 형식으로 답변하세요."""

        user_prompt = f"""
자사 상품 정보:
- 상품명: {product_input.get('product_name', '')}
- 카테고리: {product_input.get('category', '')}
- 타겟: {product_input.get('target', '')}

경쟁사 상품 정보:
{chr(10).join(competitor_texts[:10])}

위 정보를 바탕으로 3C 분석을 수행해주세요.
"""

        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])

            content = response.content
            three_c = self._parse_json_response(content)

            if not three_c or not isinstance(three_c, dict):
                return {
                    "company": ["자사 분석 필요"],
                    "customer": ["고객 조사 필요"],
                    "competitor": ["경쟁사 분석 필요"]
                }

            return three_c

        except Exception as e:
            print(f"[3C Analysis] 분석 오류: {e}")
            return {
                "company": ["분석 오류"],
                "customer": ["데이터 부족"],
                "competitor": ["추가 조사 필요"]
            }

    def _analyze_prices(self, competitor_data: Dict) -> Dict:
        """가격 분석"""
        prices = []
        price_info = []

        for result in competitor_data.get("results", []):
            if "error" in result:
                continue

            # 제목이나 설명에서 가격 추출 시도
            text = f"{result.get('title', '')} {result.get('snippet', '')}"
            found_prices = self._extract_prices(text)

            for price in found_prices:
                prices.append(price)
                price_info.append({
                    "price": price,
                    "product": result.get('title', ''),
                    "url": result.get('url', ''),
                    "platform": result.get('platform', '')
                })

        if not prices:
            return {
                "min_price": None,
                "max_price": None,
                "avg_price": None,
                "price_range": "가격 정보 없음",
                "lowest_product": None,
                "all_prices": []
            }

        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)

        # 최저가 상품 찾기
        lowest_product = next((p for p in price_info if p["price"] == min_price), None)

        return {
            "min_price": min_price,
            "max_price": max_price,
            "avg_price": round(avg_price, 0),
            "price_range": f"{min_price:,}원 ~ {max_price:,}원",
            "lowest_product": lowest_product,
            "all_prices": sorted(price_info, key=lambda x: x["price"])[:10]
        }

    def _extract_prices(self, text: str) -> List[int]:
        """텍스트에서 가격 추출"""
        # 가격 패턴: 10,000원, 10000원, 만원 등
        patterns = [
            r'(\d{1,3}(?:,\d{3})+)원',  # 10,000원
            r'(\d{4,})원',  # 10000원
            r'(\d{1,3}(?:,\d{3})+)\s*won',  # 영문
        ]

        prices = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    price = int(match.replace(',', ''))
                    # 합리적인 가격 범위만 (100원 ~ 10,000,000원)
                    if 100 <= price <= 10000000:
                        prices.append(price)
                except:
                    pass

        return prices

    def _generate_insights(self, swot: Dict, three_c: Dict, price_analysis: Dict) -> List[str]:
        """핵심 인사이트 생성"""
        insights = []

        # SWOT 기반 인사이트
        if swot.get("strengths"):
            insights.append(f"💪 핵심 강점: {swot['strengths'][0]}")

        if swot.get("opportunities"):
            insights.append(f"🎯 시장 기회: {swot['opportunities'][0]}")

        # 가격 기반 인사이트
        if price_analysis.get("min_price"):
            insights.append(
                f"💰 경쟁 가격대: {price_analysis['price_range']} (평균 {price_analysis['avg_price']:,}원)"
            )

            if price_analysis.get("lowest_product"):
                insights.append(
                    f"🏷️ 최저가: {price_analysis['lowest_product']['product']} - {price_analysis['min_price']:,}원"
                )

        # 고객 니즈
        if three_c.get("customer"):
            insights.append(f"👥 고객 니즈: {three_c['customer'][0]}")

        return insights

    def _parse_json_response(self, content: str) -> Dict:
        """JSON 응답 파싱"""
        try:
            # JSON 블록 추출
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # JSON이 아니면 None 반환
                return None
        except:
            return None
