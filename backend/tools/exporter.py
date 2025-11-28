"""
콘텐츠 내보내기 도구 (Markdown, HTML, ZIP)
"""
import os
import re
from typing import Dict, List, Tuple
from datetime import datetime

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
        md.append(f"**한줄요약:** {content_sections.get('summary', '')} (제조국: {product_input.get('manufacture_country', '')})")
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
        """HTML 형식 생성 - 미니멀 화이트&블랙 디자인"""
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='ko'>",
            "<head>",
            "    <meta charset='UTF-8'>",
            "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            f"    <title>{product_input['product_name']} - 상세페이지</title>",
            "    <style>",
            "        body { font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background: #f5f5f5; }",
            "        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px 60px; }",
            "        h1 { color: #000; border-bottom: 2px solid #000; padding-bottom: 15px; font-size: 2em; font-weight: 700; margin: 0 0 20px 0; }",
            "        h2 { color: #000; margin-top: 50px; margin-bottom: 20px; font-size: 1.5em; font-weight: 600; padding-bottom: 10px; border-bottom: 1px solid #e0e0e0; }",
            "        h3 { color: #333; font-size: 1.2em; font-weight: 600; margin-top: 30px; margin-bottom: 15px; }",
            "        p { color: #333; margin: 15px 0; }",
            "        .selling-point { background: #fff; padding: 20px; margin: 15px 0; border: 1px solid #e0e0e0; }",
            "        .selling-point strong { color: #000; font-size: 1.1em; display: block; margin-bottom: 8px; }",
            "        table { width: 100%; border-collapse: collapse; margin: 20px 0; border: 1px solid #e0e0e0; }",
            "        th, td { border: 1px solid #e0e0e0; padding: 12px 15px; text-align: left; }",
            "        th { background: #000; color: white; font-weight: 600; }",
            "        tr:nth-child(even) { background: #fafafa; }",
            "        .highlight-row { background: #f0f0f0 !important; font-weight: 600; }",
            "        .cta { background: #000; color: white; padding: 25px; text-align: center; font-size: 1.3em; margin-top: 50px; font-weight: 600; }",
            "        img { max-width: 100%; height: auto; margin: 20px 0; }",
            "        .review-card { background: #fafafa; padding: 20px; margin: 15px 0; border-left: 3px solid #000; }",
            "        .review-rating { color: #000; font-size: 1.1em; margin-bottom: 10px; }",
            "        .review-author { color: #666; font-size: 0.9em; font-weight: 500; margin-top: 10px; }",
            "        .nutrition-table { background: white; }",
            "        .nutrition-table th { background: #000; color: white; }",
            "        .promotion-box { background: #fafafa; padding: 25px; border: 1px solid #e0e0e0; margin: 20px 0; }",
            "        .promotion-item { font-size: 1em; margin: 10px 0; padding: 10px 0; border-bottom: 1px solid #e0e0e0; }",
            "        .promotion-item:last-child { border-bottom: none; }",
            "        .bar-chart { display: flex; align-items: flex-end; height: 250px; gap: 15px; margin: 30px 0; border-bottom: 2px solid #000; padding-bottom: 10px; }",
            "        .bar { flex: 1; background: #000; position: relative; }",
            "        .bar.our-product { background: #333; }",
            "        .bar-label { position: absolute; bottom: -30px; width: 100%; text-align: center; font-size: 0.9em; color: #333; }",
            "        .bar-value { position: absolute; top: -25px; width: 100%; text-align: center; font-weight: 600; color: #000; }",
            "    </style>",
            "</head>",
            "<body>",
            "<div class='container'>"
        ]

        # 헤드라인
        html_parts.append(f"    <h1>{content_sections.get('headline', product_input['product_name'])}</h1>")
        html_parts.append(f"    <p><strong>한줄요약:</strong> {content_sections.get('summary', '')} (제조국: {product_input.get('manufacture_country', '')})</p>")

        # 메인 이미지
        if images:
            main_image = next((img for img in images if "main" in img), images[0])
            html_parts.append(f"    <img src='{main_image}' alt='메인 이미지'>")

        # 셀링 포인트
        html_parts.append("    <h2>핵심 셀링포인트</h2>")
        for sp in content_sections.get("selling_points", []):
            evidence = f" — {sp.get('evidence', '')}" if sp.get('evidence') else ""
            html_parts.append("    <div class='selling-point'>")
            html_parts.append(f"        <strong>{sp['title']}</strong>{evidence}<br>")
            html_parts.append(f"        {sp['description']}")
            html_parts.append("    </div>")

        # 스펙
        html_parts.append("    <h2>제품 상세정보</h2>")
        html_parts.append("    <table>")
        for key, value in content_sections.get("specs", {}).items():
            html_parts.append(f"        <tr><th>{key}</th><td>{value}</td></tr>")
        html_parts.append("    </table>")

        # 상세 설명 (마크다운 렌더링)
        detailed_desc = content_sections.get("detailed_description", {})
        if detailed_desc.get("content"):
            html_parts.append("    <h2>상품 상세 설명</h2>")
            rendered_content = self._render_markdown(detailed_desc['content'])
            html_parts.append(f"    <div>{rendered_content}</div>")

        # 영양 정보 (테이블로 변환)
        nutrition = content_sections.get("nutrition_info", {})
        if nutrition.get("has_nutrition"):
            html_parts.append("    <h2>영양 정보 (100g 기준)</h2>")
            nutrition_table = self._parse_nutrition_to_table(nutrition['content'])
            html_parts.append(f"    {nutrition_table}")

        # 고객 후기
        reviews = content_sections.get("customer_reviews", {})
        if reviews:
            html_parts.append("    <h2>고객 후기</h2>")
            html_parts.append(f"    <p><strong>⭐ 평균 평점: {reviews.get('average_rating', 0)}/5.0</strong> ({reviews.get('total_reviews', 0)}개 리뷰)</p>")

            for review in reviews.get("reviews", []):
                stars = "⭐" * review["rating"]
                html_parts.append("    <div class='review-card'>")
                html_parts.append(f"        <div class='review-rating'>{stars}</div>")
                html_parts.append(f"        <p>{review['text']}</p>")
                html_parts.append(f"        <div class='review-author'>- {review['author']}</div>")
                html_parts.append("    </div>")

        # 레시피 제안 (마크다운 렌더링)
        recipes = content_sections.get("recipe_suggestions", {})
        if recipes.get("has_recipes"):
            html_parts.append("    <h2>추천 레시피</h2>")
            rendered_recipes = self._render_markdown(recipes['content'])
            html_parts.append(f"    <div>{rendered_recipes}</div>")

        # 비교 차트 (3개 이상일 때만 표시)
        comparison_chart = content_sections.get("comparison_chart", {})
        if comparison_chart.get("our_product"):
            competitors = comparison_chart.get("competitors", [])
            total_products = 1 + len(competitors)  # 우리 제품 + 경쟁사

            # 3개 이상일 때만 표시
            if total_products >= 3:
                html_parts.append("    <h2>제품 비교</h2>")

                # 테이블 형식
                html_parts.append("    <table>")
                html_parts.append("        <tr><th>제품명</th><th>가격</th><th>품질</th><th>배송</th><th>평점</th></tr>")

                our = comparison_chart["our_product"]
                html_parts.append(f"        <tr class='highlight-row'>")
                html_parts.append(f"            <td><strong>{our['name']}</strong></td>")
                html_parts.append(f"            <td>{our['price']}</td>")
                html_parts.append(f"            <td>{our['quality']}</td>")
                html_parts.append(f"            <td>{our['delivery']}</td>")
                html_parts.append(f"            <td>{our['rating']} ⭐</td>")
                html_parts.append("        </tr>")

                for comp in competitors:
                    html_parts.append("        <tr>")
                    html_parts.append(f"            <td>{comp['name']}</td>")
                    html_parts.append(f"            <td>{comp['price']}</td>")
                    html_parts.append(f"            <td>{comp['quality']}</td>")
                    html_parts.append(f"            <td>{comp['delivery']}</td>")
                    html_parts.append(f"            <td>{comp['rating']} ⭐</td>")
                    html_parts.append("        </tr>")

                html_parts.append("    </table>")

                # 2D 막대 차트 (호버 효과 없음)
                html_parts.append("    <h3>평점 비교</h3>")
                html_parts.append("    <div class='bar-chart'>")

                # 우리 제품 막대
                our_height = int(our['rating'] / 5.0 * 100)
                html_parts.append(f"        <div class='bar our-product' style='height: {our_height}%;'>")
                html_parts.append(f"            <div class='bar-value'>{our['rating']}⭐</div>")
                html_parts.append(f"            <div class='bar-label'>{our['name'][:10]}</div>")
                html_parts.append("        </div>")

                # 경쟁사 막대
                for comp in competitors:
                    comp_height = int(comp['rating'] / 5.0 * 100)
                    html_parts.append(f"        <div class='bar' style='height: {comp_height}%;'>")
                    html_parts.append(f"            <div class='bar-value'>{comp['rating']}⭐</div>")
                    html_parts.append(f"            <div class='bar-label'>{comp['name']}</div>")
                    html_parts.append("        </div>")

                html_parts.append("    </div>")

        # 프로모션
        promotion = content_sections.get("promotion", {})
        if promotion:
            html_parts.append("    <h2>🎁 특별 혜택</h2>")
            html_parts.append("    <div class='promotion-box'>")
            for promo in promotion.get("promotions", []):
                html_parts.append(f"        <div class='promotion-item'>{promo}</div>")
            html_parts.append(f"        <p style='text-align: center; font-size: 1.1em; margin-top: 20px;'><strong>{promotion.get('cta', '')}</strong></p>")
            html_parts.append("    </div>")

        # 소셜 미디어 섹션 제거됨

        # CTA
        platforms = product_input.get("platforms", ["coupang"])
        cta_text = content_sections.get("cta", {}).get(platforms[0], "지금 구매하세요!")
        html_parts.append(f"    <div class='cta'>{cta_text}</div>")

        html_parts.extend([
            "</div>",  # .container 닫기
            "</body>",
            "</html>"
        ])

        return "\n".join(html_parts)

    def create_zip(self) -> str:
        """프로젝트를 ZIP 파일로 압축"""
        import zipfile

        zip_path = f"{self.project_dir}.zip"

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.project_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(self.project_dir))
                    zipf.write(file_path, arcname)

        return f"/projects/{self.project_id}.zip"
