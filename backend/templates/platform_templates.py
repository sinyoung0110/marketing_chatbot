"""
플랫폼별 템플릿 관리자
"""
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

class PlatformTemplateManager:
    """플랫폼별 템플릿 관리"""

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def assemble_content(
        self,
        product_input: Dict,
        selling_points: List[Dict],
        competitor_insights: Dict
    ) -> Dict:
        """
        플랫폼별 콘텐츠 조합

        Returns:
            섹션별 콘텐츠 딕셔너리
        """
        platforms = product_input.get("platforms", ["coupang"])

        content_sections = {
            "headline": self._generate_headline(product_input, selling_points),
            "summary": self._generate_summary(product_input, selling_points),
            "selling_points": self._format_selling_points(selling_points),
            "problem_solution": self._generate_problem_solution(product_input, selling_points),
            "specs": self._format_specs(product_input),
            "usage_guide": self._generate_usage_guide(product_input),
            "comparison": self._generate_comparison(product_input, competitor_insights),
            "faq": self._generate_faq(product_input),
            "cta": self._generate_cta(platforms)
        }

        # 플랫폼별 최적화
        for platform in platforms:
            content_sections[f"{platform}_optimized"] = self._optimize_for_platform(
                content_sections, platform
            )

        return content_sections

    def _generate_headline(self, product_input: Dict, selling_points: List[Dict]) -> str:
        """헤드라인 생성"""
        product_name = product_input["product_name"]
        summary = product_input.get("summary", "")

        # 첫 번째 셀링 포인트 활용
        main_point = selling_points[0]["title"] if selling_points else "프리미엄 품질"

        return f"{product_name} - {main_point}, {summary}"

    def _generate_summary(self, product_input: Dict, selling_points: List[Dict]) -> str:
        """요약 생성"""
        return product_input.get("summary", "")

    def _format_selling_points(self, selling_points: List[Dict]) -> List[Dict]:
        """셀링 포인트 포맷팅"""
        return selling_points

    def _generate_problem_solution(
        self,
        product_input: Dict,
        selling_points: List[Dict]
    ) -> Dict:
        """문제-해결-증거 섹션 생성"""
        system_prompt = """고객의 문제점을 제시하고 제품이 어떻게 해결하는지, 그 증거는 무엇인지 작성하세요.

형식:
- 문제: 고객이 겪는 구체적인 문제
- 해결: 제품이 제공하는 해결책
- 증거: 신뢰할 수 있는 근거 (테스트 결과, 인증, 리뷰 등)"""

        user_prompt = f"""상품: {product_input['product_name']}
카테고리: {product_input['category']}
주요 특징: {selling_points[0] if selling_points else {}}

문제-해결-증거 구조로 작성해주세요."""

        try:
            response = self.llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])

            content = response.content

            return {
                "problem": self._extract_section(content, "문제"),
                "solution": self._extract_section(content, "해결"),
                "evidence": self._extract_section(content, "증거")
            }

        except Exception as e:
            print(f"[Template] 문제-해결 생성 오류: {e}")
            return {
                "problem": "기존 제품의 불편함",
                "solution": f"{product_input['product_name']}로 간편하게 해결",
                "evidence": "고객 만족도 90% 이상"
            }

    def _format_specs(self, product_input: Dict) -> Dict:
        """스펙 테이블 포맷팅"""
        specs = product_input.get("specs", {})
        specs["제조국"] = product_input.get("manufacture_country", "")
        if product_input.get("manufacture_date"):
            specs["제조일"] = product_input["manufacture_date"]

        return specs

    def _generate_usage_guide(self, product_input: Dict) -> List[str]:
        """사용 방법 가이드 생성"""
        # 카테고리별 기본 사용법
        category = product_input.get("category", "")

        if "푸드" in category or "식품" in category:
            return [
                "제품을 개봉합니다",
                "권장량을 확인합니다",
                "조리 또는 바로 섭취합니다",
                "남은 제품은 밀봉하여 보관합니다"
            ]
        elif "전자" in category:
            return [
                "전원을 연결합니다",
                "전원 버튼을 눌러 작동시킵니다",
                "사용 후 전원을 끕니다",
                "정기적으로 청소합니다"
            ]
        else:
            return [
                "제품을 개봉하여 확인합니다",
                "사용 설명서를 참고합니다",
                "올바른 방법으로 사용합니다",
                "사용 후 보관합니다"
            ]

    def _generate_comparison(
        self,
        product_input: Dict,
        competitor_insights: Dict
    ) -> Dict:
        """경쟁사 비교 테이블 생성"""
        return {
            "headers": ["항목", "경쟁사A", "우리 제품"],
            "rows": [
                {
                    "item": "품질",
                    "competitor": "보통",
                    "ours": "**프리미엄**"
                },
                {
                    "item": "원산지",
                    "competitor": "수입",
                    "ours": f"**{product_input.get('manufacture_country', '국산')}**"
                },
                {
                    "item": "가격",
                    "competitor": "고가",
                    "ours": "**합리적**"
                }
            ]
        }

    def _generate_faq(self, product_input: Dict) -> List[Dict]:
        """FAQ 생성"""
        category = product_input.get("category", "")

        faqs = [
            {
                "question": "배송은 얼마나 걸리나요?",
                "answer": "주문 후 평균 2-3일 소요됩니다. (도서산간 지역 제외)"
            },
            {
                "question": "교환/반품이 가능한가요?",
                "answer": "수령 후 7일 이내 미개봉 상품에 한해 가능합니다."
            }
        ]

        # 카테고리별 FAQ 추가
        if "푸드" in category:
            faqs.append({
                "question": "유통기한은 얼마나 되나요?",
                "answer": f"제조일로부터 {product_input.get('specs', {}).get('유통기한', '6개월')}입니다."
            })

        return faqs

    def _generate_cta(self, platforms: List[str]) -> Dict:
        """플랫폼별 CTA 생성"""
        cta_texts = {
            "coupang": "지금 구매하면 **쿠팡 단독 특가** — 한정수량!",
            "naver": "**네이버 스토어 단독 혜택** — 오늘만 할인!"
        }

        return {
            platform: cta_texts.get(platform, "지금 바로 구매하세요!")
            for platform in platforms
        }

    def _optimize_for_platform(self, content_sections: Dict, platform: str) -> Dict:
        """플랫폼별 최적화"""
        if platform == "coupang":
            return {
                "title_length": 150,  # 쿠팡 권장 제목 길이
                "summary_position": "top",  # 상단 요약 강조
                "cta": content_sections["cta"].get("coupang", "")
            }
        elif platform == "naver":
            return {
                "title_length": 100,
                "summary_position": "top",
                "keyword_density": "high",  # 검색 최적화
                "cta": content_sections["cta"].get("naver", "")
            }
        else:
            return {"cta": "지금 구매하세요!"}

    def _extract_section(self, text: str, keyword: str) -> str:
        """텍스트에서 특정 섹션 추출"""
        import re
        pattern = rf'{keyword}[^:]*:\s*(.+?)(?:\n|$)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return f"{keyword} 내용"
