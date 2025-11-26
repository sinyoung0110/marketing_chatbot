"""
리뷰 분석 도구 - 쿠팡/네이버 상품 리뷰 수집 및 분석
"""
from typing import Dict, List
import re
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class ReviewAnalyzer:
    """리뷰 분석기 - 경쟁 상품 리뷰를 수집하고 인사이트 추출"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    def extract_reviews_from_content(self, raw_content: str, url: str) -> List[Dict]:
        """
        HTML 콘텐츠에서 리뷰 추출

        Args:
            raw_content: 원본 HTML 콘텐츠
            url: 상품 URL

        Returns:
            추출된 리뷰 리스트
        """
        reviews = []

        # 쿠팡 리뷰 패턴
        if "coupang.com" in url:
            # 간단한 텍스트 기반 추출 (실제로는 BeautifulSoup 등 사용 권장)
            review_patterns = [
                r'\"review-content\">([^<]+)<',
                r'\"sdp-review__article__list__review__content\">([^<]+)<'
            ]

            for pattern in review_patterns:
                matches = re.findall(pattern, raw_content)
                for match in matches:
                    if len(match) > 10:  # 너무 짧은 텍스트 제외
                        reviews.append({
                            "text": match.strip(),
                            "platform": "coupang"
                        })

        # 네이버 스마트스토어 리뷰 패턴
        elif "smartstore.naver.com" in url:
            review_patterns = [
                r'\"reviewContent\":\"([^\"]+)\"',
                r'class=\"review-text\">([^<]+)<'
            ]

            for pattern in review_patterns:
                matches = re.findall(pattern, raw_content)
                for match in matches:
                    if len(match) > 10:
                        reviews.append({
                            "text": match.strip(),
                            "platform": "naver"
                        })

        return reviews[:20]  # 최대 20개

    def analyze_reviews(self, reviews: List[Dict], product_name: str) -> Dict:
        """
        리뷰 분석 - 긍정/부정, 주요 키워드, 고객 니즈 파악

        Args:
            reviews: 리뷰 리스트
            product_name: 상품명

        Returns:
            분석 결과
        """
        if not reviews:
            return {
                "summary": "리뷰를 찾을 수 없습니다.",
                "positive_points": [],
                "negative_points": [],
                "key_features": [],
                "customer_needs": []
            }

        # 리뷰 텍스트 합치기
        review_texts = "\n".join([f"- {r['text']}" for r in reviews[:15]])

        prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 상품 리뷰 분석 전문가입니다.
주어진 리뷰들을 분석하여 다음을 추출하세요:

1. 긍정적 평가 (3-5개)
2. 부정적 평가 (2-3개)
3. 자주 언급되는 주요 기능/특징 (3-5개)
4. 고객이 원하는 것 (니즈) (3-5개)

JSON 형식으로 반환:
{{
  "positive_points": ["항목1", "항목2", ...],
  "negative_points": ["항목1", "항목2", ...],
  "key_features": ["특징1", "특징2", ...],
  "customer_needs": ["니즈1", "니즈2", ...]
}}"""),
            ("user", "상품: {product_name}\n\n리뷰:\n{reviews}")
        ])

        try:
            response = self.llm.invoke(
                prompt.format_messages(product_name=product_name, reviews=review_texts)
            )

            # JSON 파싱
            import json
            result = json.loads(response.content)
            result["summary"] = f"{len(reviews)}개의 리뷰를 분석했습니다."

            return result

        except Exception as e:
            print(f"[ReviewAnalyzer] 리뷰 분석 오류: {e}")
            return {
                "summary": f"리뷰 분석 중 오류 발생: {e}",
                "positive_points": [],
                "negative_points": [],
                "key_features": [],
                "customer_needs": []
            }

    def generate_marketing_insights(self, review_analysis: Dict, product_input: Dict) -> str:
        """
        리뷰 분석 결과를 바탕으로 마케팅 인사이트 생성

        Args:
            review_analysis: 리뷰 분석 결과
            product_input: 자사 상품 정보

        Returns:
            마케팅 인사이트 텍스트
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 마케팅 전략가입니다.
경쟁사 리뷰 분석 결과를 바탕으로 자사 상품의 차별화 포인트와 마케팅 전략을 제안하세요.

다음 관점에서 분석:
1. 경쟁사의 약점을 우리 강점으로 전환
2. 고객이 원하는 것을 우리 상품에서 강조
3. 경쟁사가 놓친 니즈 발굴
4. 구체적인 카피/문구 제안

간결하고 실용적으로 작성하세요."""),
            ("user", """자사 상품: {product_name} ({category})
타겟: {target}

경쟁사 리뷰 분석:
긍정 평가: {positive}
부정 평가: {negative}
주요 기능: {features}
고객 니즈: {needs}

마케팅 인사이트를 제공하세요.""")
        ])

        try:
            response = self.llm.invoke(prompt.format_messages(
                product_name=product_input.get("name", ""),
                category=product_input.get("category", ""),
                target=product_input.get("target_audience", ""),
                positive=", ".join(review_analysis.get("positive_points", [])),
                negative=", ".join(review_analysis.get("negative_points", [])),
                features=", ".join(review_analysis.get("key_features", [])),
                needs=", ".join(review_analysis.get("customer_needs", []))
            ))

            return response.content

        except Exception as e:
            print(f"[ReviewAnalyzer] 인사이트 생성 오류: {e}")
            return "인사이트 생성 중 오류가 발생했습니다."
