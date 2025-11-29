"""
콘텐츠 내보내기 도구 (Markdown, HTML, ZIP)
"""
import os
import re
from typing import Dict, List, Tuple
from templates.esm_templates import generate_esm_html

class ContentExporter:
    """콘텐츠 내보내기"""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.project_dir = os.path.join("projects", project_id)
        os.makedirs(self.project_dir, exist_ok=True)

    def export(
        self,
        content_sections: Dict,
        images: List[str],
        product_input: Dict
    ) -> Tuple[str, str]:
        """
        Markdown 및 HTML 파일 생성

        Returns:
            (markdown_path, html_path)
        """
        # Markdown 생성
        markdown_content = self._generate_markdown(content_sections, images, product_input)
        markdown_path = os.path.join(self.project_dir, "detail.md")

        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        # HTML 생성
        html_content = self._generate_html(content_sections, images, product_input)
        html_path = os.path.join(self.project_dir, "detail.html")

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return (f"/projects/{self.project_id}/detail.md",
                f"/projects/{self.project_id}/detail.html")

    def _generate_markdown(
        self,
        content_sections: Dict,
        images: List[str],
        product_input: Dict
    ) -> str:
        """Markdown 형식 생성"""
        md = []

        # 제목
        md.append(f"# {content_sections.get('headline', product_input['product_name'])}")
        md.append("\n---\n")

        # 핵심 셀링포인트
        md.append("## 핵심 셀링포인트")
        for i, sp in enumerate(content_sections.get("selling_points", []), 1):
            evidence = f" — {sp.get('evidence', '')}" if sp.get('evidence') else ""
            md.append(f"{i}. **{sp['title']}**{evidence}")
            md.append(f"   {sp['description']}\n")

        md.append("\n---\n")

        # 문제-해결-증거
        ps = content_sections.get("problem_solution", {})
        if ps:
            md.append("## 구매를 망설이는 고객님께")
            md.append(f"- 문제: {ps.get('problem', '')}")
            md.append(f"- 해결: {ps.get('solution', '')}")
            md.append(f"- 증거: {ps.get('evidence', '')}")
            md.append("\n---\n")

        # 제품 상세정보
        md.append("## 제품 상세정보")
        for key, value in content_sections.get("specs", {}).items():
            md.append(f"- {key}: {value}")
        md.append("\n---\n")

        # 사용방법 (이미지 포함)
        md.append("## 사용방법 (이미지 포함)")
        for i, step in enumerate(content_sections.get("usage_guide", []), 1):
            md.append(f"{i}. {step}")

        # 이미지 삽입
        if images:
            usage_image = next((img for img in images if "usage" in img), images[0])
            md.append(f"\n![사용 설명]({usage_image})")

        md.append("\n---\n")

        # 경쟁사 비교
        comparison = content_sections.get("comparison", {})
        if comparison:
            md.append("## 경쟁사 비교")
            headers = comparison.get("headers", ["항목", "경쟁사A", "우리 제품"])
            md.append(f"| {' | '.join(headers)} |")
            md.append(f"|{'---|' * len(headers)}")

            for row in comparison.get("rows", []):
                md.append(f"| {row['item']} | {row['competitor']} | {row['ours']} |")

            md.append("\n---\n")

        # FAQ
        md.append("## 자주 묻는 질문(FAQ)")
        for faq in content_sections.get("faq", []):
            md.append(f"**Q: {faq['question']}**")
            md.append(f"A: {faq['answer']}\n")

        md.append("\n---\n")

        # 상세 설명
        detailed_desc = content_sections.get("detailed_description", {})
        if detailed_desc.get("content"):
            md.append("## 상품 상세 설명")
            md.append(detailed_desc["content"])
            md.append("\n---\n")

        # 영양 정보
        nutrition = content_sections.get("nutrition_info", {})
        if nutrition.get("has_nutrition"):
            md.append("## 영양 정보 (100g 기준)")
            md.append(nutrition["content"])
            md.append("\n---\n")

        # 고객 후기
        reviews = content_sections.get("customer_reviews", {})
        if reviews:
            md.append("## 고객 후기")
            md.append(f"⭐ 평균 평점: {reviews.get('average_rating', 0)}/5.0 ({reviews.get('total_reviews', 0)}개 리뷰)")
            md.append("")
            for review in reviews.get("reviews", []):
                stars = "⭐" * review["rating"]
                md.append(f"{stars} **{review['author']}**")
                md.append(f"{review['text']}\n")
            md.append("\n---\n")

        # 레시피 제안
        recipes = content_sections.get("recipe_suggestions", {})
        if recipes.get("has_recipes"):
            md.append("## 추천 레시피")
            md.append(recipes["content"])
            md.append("\n---\n")

        # 비교 차트
        comparison_chart = content_sections.get("comparison_chart", {})
        if comparison_chart.get("our_product"):
            md.append("## 제품 비교")
            md.append("| 제품명 | 가격 | 품질 | 배송 | 평점 |")
            md.append("|--------|------|------|------|------|")

            our = comparison_chart["our_product"]
            md.append(f"| **{our['name']}** | {our['price']} | {our['quality']} | {our['delivery']} | {our['rating']} ⭐ |")

            for comp in comparison_chart.get("competitors", []):
                md.append(f"| {comp['name']} | {comp['price']} | {comp['quality']} | {comp['delivery']} | {comp['rating']} ⭐ |")

            md.append("\n---\n")

        # 프로모션
        promotion = content_sections.get("promotion", {})
        if promotion:
            md.append("## 🎁 특별 혜택")
            for promo in promotion.get("promotions", []):
                md.append(f"- {promo}")
            md.append(f"\n**{promotion.get('cta', '')}**")
            md.append("\n---\n")

        # 소셜 미디어 섹션 제거됨

        # CTA
        platforms = product_input.get("platforms", ["coupang"])
        cta_text = content_sections.get("cta", {}).get(platforms[0], "지금 구매하세요!")
        md.append(f"## CTA")
        md.append(cta_text)

        return "\n".join(md)

    def _render_markdown(self, text: str) -> str:
        """마크다운 텍스트를 HTML로 변환"""
        # 헤더 변환 (## -> <h2>, ### -> <h3>)
        text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)

        # 볼드 변환 (** -> <strong>)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

        # 줄바꿈 처리
        text = text.replace('\n', '<br>')

        return text

    def _parse_nutrition_to_table(self, nutrition_content: str) -> str:
        """영양 정보 텍스트를 테이블로 파싱"""
        lines = nutrition_content.strip().split('\n')
        table_html = "<table class='nutrition-table'>"
        table_html += "<tr><th>영양소</th><th>함량</th></tr>"

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # "칼로리: 250kcal" 형식 파싱
            if ':' in line:
                parts = line.split(':', 1)
                nutrient = parts[0].strip().replace('-', '').strip()
                value = parts[1].strip()
                table_html += f"<tr><td>{nutrient}</td><td>{value}</td></tr>"

        table_html += "</table>"
        return table_html

    def _generate_html(
        self,
        content_sections: Dict,
        images: List[str],
        product_input: Dict
    ) -> str:
        """HTML 형식 생성 - ESM+ 가이드라인 준수"""
        # ESM+ 템플릿 사용
        return generate_esm_html(content_sections, images, product_input)

    def create_zip(self) -> str:
        """프로젝트를 ZIP 파일로 압축"""
        import zipfile

        zip_path = f"{self.project_dir}.zip"

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.project_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(self.project_dir))
                    zipf.write(file_path, arcname)

        return f"/projects/{self.project_id}.zip"
