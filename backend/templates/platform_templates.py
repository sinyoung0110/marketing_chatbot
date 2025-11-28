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
            "cta": self._generate_cta(platforms),

            # 새로운 9가지 섹션 추가
            "product_gallery": self._generate_product_gallery(product_input),
            "detailed_description": self._generate_detailed_description(product_input),
            "nutrition_info": self._generate_nutrition_info(product_input),
            "customer_reviews": self._generate_customer_reviews(product_input, competitor_insights),
            "recipe_suggestions": self._generate_recipe_suggestions(product_input),
            "comparison_chart": self._generate_comparison_chart(product_input, competitor_insights),
            "promotion": self._generate_promotion(product_input),
            "social_media": self._generate_social_media(product_input)
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

    def _generate_product_gallery(self, product_input: Dict) -> Dict:
        """제품 사진 갤러리 섹션"""
        return {
            "title": "제품 갤러리",
            "images": [
                {"type": "main", "description": "메인 제품 사진"},
                {"type": "angle1", "description": "측면 사진"},
                {"type": "angle2", "description": "상단 사진"},
                {"type": "usage", "description": "사용 예시"},
                {"type": "packaging", "description": "포장 상태"}
            ]
        }

    def _generate_detailed_description(self, product_input: Dict) -> Dict:
        """상세 설명 생성"""
        prompt = f"""
상품명: {product_input['product_name']}
카테고리: {product_input['category']}

아래 내용을 포함한 상세한 상품 설명을 작성하세요:
1. 상품의 특성과 품질
2. 원산지 및 생산 과정
3. 관리 방법 및 보관 방법
4. 왜 이 상품이 특별한지

고객이 신뢰할 수 있도록 구체적이고 전문적으로 작성하세요."""

        response = self.llm.invoke([
            SystemMessage(content="당신은 전문 상품 설명 작가입니다."),
            HumanMessage(content=prompt)
        ])

        return {
            "title": "상품 상세 설명",
            "content": response.content
        }

    def _generate_nutrition_info(self, product_input: Dict) -> Dict:
        """영양 정보 생성"""
        category = product_input['category'].lower()

        # 식품 카테고리인 경우에만 영양 정보 생성
        if any(keyword in category for keyword in ['식품', '음식', '간식', '과자', '음료', '고기', '육류', '생선']):
            prompt = f"""
상품: {product_input['product_name']}

이 상품의 100g 기준 영양 성분표를 작성하세요:
- 칼로리 (kcal)
- 단백질 (g)
- 지방 (g)
- 탄수화물 (g)
- 당류 (g)
- 나트륨 (mg)

또한 이 상품이 건강에 미치는 긍정적인 영향을 2-3가지 작성하세요."""

            response = self.llm.invoke([
                SystemMessage(content="당신은 영양사입니다. 일반적인 영양 정보를 제공하세요."),
                HumanMessage(content=prompt)
            ])

            return {
                "title": "영양 정보 (100g 기준)",
                "content": response.content,
                "has_nutrition": True
            }
        else:
            return {"has_nutrition": False}

    def _generate_customer_reviews(self, product_input: Dict, competitor_insights: Dict) -> Dict:
        """고객 후기 생성"""
        reviews = []

        # 경쟁사 인사이트에서 긍정적인 포인트 추출
        positive_points = competitor_insights.get("positive_points", [])

        # 샘플 리뷰 생성 (실제로는 리뷰 크롤링 데이터 사용)
        sample_reviews = [
            {"rating": 5, "text": "정말 만족스러운 구매였습니다!", "author": "김**"},
            {"rating": 5, "text": "품질이 훌륭하네요. 재구매 의사 100%", "author": "이**"},
            {"rating": 4, "text": "가격 대비 좋아요. 추천합니다.", "author": "박**"},
            {"rating": 5, "text": "가족 모두 만족했어요!", "author": "최**"}
        ]

        return {
            "title": "고객 후기",
            "average_rating": 4.8,
            "total_reviews": 1247,
            "reviews": sample_reviews[:4]
        }

    def _generate_recipe_suggestions(self, product_input: Dict) -> Dict:
        """레시피 제안 생성"""
        category = product_input['category'].lower()

        # 식품 카테고리인 경우에만 레시피 생성
        if any(keyword in category for keyword in ['식품', '음식', '간식', '고기', '육류', '생선', '채소']):
            prompt = f"""
상품: {product_input['product_name']}

이 상품을 활용한 추천 레시피를 3가지 작성하세요:
1. 간단한 조리법 (5분 이내)
2. 인기 레시피
3. 특별한 날 레시피

각 레시피마다:
- 레시피 이름
- 주요 재료
- 간단한 조리 순서 (3-4단계)
- 함께 먹으면 좋은 사이드 메뉴"""

            response = self.llm.invoke([
                SystemMessage(content="당신은 요리 전문가입니다."),
                HumanMessage(content=prompt)
            ])

            return {
                "title": "추천 레시피",
                "content": response.content,
                "has_recipes": True
            }
        else:
            return {"has_recipes": False}

    def _generate_comparison_chart(self, product_input: Dict, competitor_insights: Dict) -> Dict:
        """비교 차트 생성"""
        product_name = product_input['product_name']

        # 경쟁사 데이터 추출
        competitors = []
        if competitor_insights and "competitor_summary" in competitor_insights:
            comp_summary = competitor_insights["competitor_summary"]
            # 샘플 경쟁사 데이터 (실제로는 SWOT 분석에서 가져옴)
            competitors = [
                {
                    "name": "경쟁사 A",
                    "price": "30,000원",
                    "quality": "중",
                    "delivery": "3-5일",
                    "rating": 4.2
                },
                {
                    "name": "경쟁사 B",
                    "price": "40,000원",
                    "quality": "상",
                    "delivery": "2-3일",
                    "rating": 4.5
                }
            ]

        # 우리 제품 데이터
        our_product = {
            "name": product_name,
            "price": "37,081원",
            "quality": "최상",
            "delivery": "1-2일 (무료배송)",
            "rating": 4.8
        }

        return {
            "title": "제품 비교",
            "our_product": our_product,
            "competitors": competitors,
            "chart_type": "table"  # 또는 "bar_chart"
        }

    def _generate_promotion(self, product_input: Dict) -> Dict:
        """프로모션 섹션 생성"""
        promotions = [
            "✨ 지금 구매하시면 무료 배송",
            "🎁 추가 10% 할인 쿠폰 제공",
            "⏰ 한정 수량 특가 진행 중"
        ]

        return {
            "title": "특별 혜택",
            "promotions": promotions,
            "cta": "지금 바로 구매하고 혜택 받기"
        }

    def _generate_social_media(self, product_input: Dict) -> Dict:
        """소셜 미디어 섹션 생성"""
        product_name = product_input['product_name']

        # 해시태그 생성
        hashtag = product_name.replace(" ", "")

        return {
            "title": "소셜 미디어",
            "hashtag": f"#{hashtag}",
            "message": f"이 제품을 구매하신 후 #{hashtag} 해시태그와 함께 사진을 공유해주세요!",
            "links": [
                {"platform": "Instagram", "url": "https://instagram.com"},
                {"platform": "Facebook", "url": "https://facebook.com"},
                {"platform": "카카오톡", "url": "https://kakaotalk.com"}
            ]
        }
