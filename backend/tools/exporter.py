"""
콘텐츠 내보내기 도구 (Markdown, HTML, ZIP)
"""
import os
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

        # CTA
        platforms = product_input.get("platforms", ["coupang"])
        cta_text = content_sections.get("cta", {}).get(platforms[0], "지금 구매하세요!")
        md.append(f"## CTA")
        md.append(cta_text)

        return "\n".join(md)

    def _generate_html(
        self,
        content_sections: Dict,
        images: List[str],
        product_input: Dict
    ) -> str:
        """HTML 형식 생성"""
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='ko'>",
            "<head>",
            "    <meta charset='UTF-8'>",
            "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            f"    <title>{product_input['product_name']} - 상세페이지</title>",
            "    <style>",
            "        body { font-family: 'Noto Sans KR', sans-serif; line-height: 1.8; max-width: 1200px; margin: 0 auto; padding: 20px; }",
            "        h1 { color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }",
            "        h2 { color: #555; margin-top: 40px; border-left: 5px solid #007bff; padding-left: 15px; }",
            "        .selling-point { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; }",
            "        .selling-point strong { color: #007bff; font-size: 1.2em; }",
            "        table { width: 100%; border-collapse: collapse; margin: 20px 0; }",
            "        th, td { border: 1px solid #ddd; padding: 12px; text-align: center; }",
            "        th { background: #007bff; color: white; }",
            "        .cta { background: #ff6b6b; color: white; padding: 20px; text-align: center; font-size: 1.3em; border-radius: 10px; margin-top: 40px; }",
            "        img { max-width: 100%; height: auto; border-radius: 8px; margin: 20px 0; }",
            "    </style>",
            "</head>",
            "<body>"
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

        # CTA
        platforms = product_input.get("platforms", ["coupang"])
        cta_text = content_sections.get("cta", {}).get(platforms[0], "지금 구매하세요!")
        html_parts.append(f"    <div class='cta'>{cta_text}</div>")

        html_parts.extend([
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
