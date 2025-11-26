"""
SWOT + 3C 분석 결과 시각화 도구
"""
from typing import Dict
import os
from datetime import datetime


class AnalysisVisualizer:
    """분석 결과를 HTML로 시각화"""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.project_dir = f"backend/projects/{project_id}"

    def generate_html(self, analysis_result: Dict, product_input: Dict) -> str:
        """
        SWOT + 3C 분석 결과를 HTML로 생성

        Args:
            analysis_result: SWOT + 3C 분석 결과
            product_input: 상품 입력 정보

        Returns:
            HTML 파일 경로
        """
        os.makedirs(self.project_dir, exist_ok=True)

        html_content = self._build_html(analysis_result, product_input)

        # HTML 파일 저장
        html_path = f"{self.project_dir}/analysis.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"[AnalysisVisualizer] HTML 생성 완료: {html_path}")
        return html_path

    def _build_html(self, analysis: Dict, product_input: Dict) -> str:
        """HTML 콘텐츠 생성"""
        swot = analysis.get("swot", {})
        three_c = analysis.get("three_c", {})
        price = analysis.get("price_analysis", {})
        insights = analysis.get("insights", [])

        return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SWOT + 3C 분석 - {product_input.get('product_name', '상품')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .header .date {{
            font-size: 0.9em;
            opacity: 0.7;
            margin-top: 10px;
        }}

        .insights {{
            background: #f8f9fa;
            padding: 30px;
            border-bottom: 2px solid #e9ecef;
        }}

        .insights h2 {{
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #333;
        }}

        .insight-item {{
            background: white;
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            font-size: 1.1em;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .content {{
            padding: 40px;
        }}

        .section {{
            margin-bottom: 50px;
        }}

        .section-title {{
            font-size: 2em;
            margin-bottom: 20px;
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}

        .card {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        }}

        .card-title {{
            font-size: 1.5em;
            margin-bottom: 15px;
            color: #667eea;
            font-weight: bold;
        }}

        .card-content ul {{
            list-style: none;
            padding-left: 0;
        }}

        .card-content li {{
            padding: 10px 0;
            border-bottom: 1px solid #e9ecef;
            color: #495057;
            line-height: 1.6;
        }}

        .card-content li:last-child {{
            border-bottom: none;
        }}

        .card-content li:before {{
            content: "✓ ";
            color: #667eea;
            font-weight: bold;
            margin-right: 8px;
        }}

        .price-section {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
        }}

        .price-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 20px;
        }}

        .price-card {{
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            backdrop-filter: blur(10px);
        }}

        .price-label {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }}

        .price-value {{
            font-size: 2em;
            font-weight: bold;
        }}

        .product-table {{
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
        }}

        .product-table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
        }}

        .product-table td {{
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
            color: #495057;
        }}

        .product-table tr:hover {{
            background: #f8f9fa;
        }}

        .product-link {{
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }}

        .product-link:hover {{
            text-decoration: underline;
        }}

        .badge {{
            display: inline-block;
            padding: 5px 10px;
            background: #667eea;
            color: white;
            border-radius: 5px;
            font-size: 0.85em;
        }}

        @media (max-width: 768px) {{
            .grid, .price-grid {{
                grid-template-columns: 1fr;
            }}

            .header h1 {{
                font-size: 1.8em;
            }}

            .content {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 SWOT + 3C 분석 보고서</h1>
            <div class="subtitle">{product_input.get('product_name', '상품 분석')}</div>
            <div class="date">생성일: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}</div>
        </div>

        {self._build_insights_section(insights)}

        <div class="content">
            {self._build_swot_section(swot)}

            {self._build_3c_section(three_c)}

            {self._build_price_section(price)}
        </div>
    </div>
</body>
</html>"""

    def _build_insights_section(self, insights: list) -> str:
        """핵심 인사이트 섹션"""
        if not insights:
            return ""

        items = "\n".join([f'<div class="insight-item">{insight}</div>' for insight in insights])

        return f"""
        <div class="insights">
            <h2>🎯 핵심 인사이트</h2>
            {items}
        </div>
        """

    def _build_swot_section(self, swot: Dict) -> str:
        """SWOT 분석 섹션"""
        strengths = self._build_list(swot.get("strengths", []))
        weaknesses = self._build_list(swot.get("weaknesses", []))
        opportunities = self._build_list(swot.get("opportunities", []))
        threats = self._build_list(swot.get("threats", []))

        return f"""
        <div class="section">
            <h2 class="section-title">📈 SWOT 분석</h2>
            <div class="grid">
                <div class="card">
                    <div class="card-title">💪 Strengths (강점)</div>
                    <div class="card-content">
                        {strengths}
                    </div>
                </div>
                <div class="card">
                    <div class="card-title">⚠️ Weaknesses (약점)</div>
                    <div class="card-content">
                        {weaknesses}
                    </div>
                </div>
                <div class="card">
                    <div class="card-title">🎯 Opportunities (기회)</div>
                    <div class="card-content">
                        {opportunities}
                    </div>
                </div>
                <div class="card">
                    <div class="card-title">🚨 Threats (위협)</div>
                    <div class="card-content">
                        {threats}
                    </div>
                </div>
            </div>
        </div>
        """

    def _build_3c_section(self, three_c: Dict) -> str:
        """3C 분석 섹션"""
        company = self._build_list(three_c.get("company", []))
        customer = self._build_list(three_c.get("customer", []))
        competitor = self._build_list(three_c.get("competitor", []))

        return f"""
        <div class="section">
            <h2 class="section-title">🔍 3C 분석</h2>
            <div class="grid">
                <div class="card">
                    <div class="card-title">🏢 Company (자사)</div>
                    <div class="card-content">
                        {company}
                    </div>
                </div>
                <div class="card">
                    <div class="card-title">👥 Customer (고객)</div>
                    <div class="card-content">
                        {customer}
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-title">⚔️ Competitor (경쟁사)</div>
                <div class="card-content">
                    {competitor}
                </div>
            </div>
        </div>
        """

    def _build_price_section(self, price: Dict) -> str:
        """가격 분석 섹션"""
        if not price.get("min_price"):
            return """
            <div class="section">
                <h2 class="section-title">💰 가격 분석</h2>
                <p style="color: #6c757d;">가격 정보를 찾을 수 없습니다.</p>
            </div>
            """

        min_price = price.get("min_price", 0)
        max_price = price.get("max_price", 0)
        avg_price = price.get("avg_price", 0)

        # 최저가 상품 테이블
        products_html = ""
        if price.get("all_prices"):
            rows = []
            for i, product in enumerate(price["all_prices"][:5], 1):
                badge = '<span class="badge">최저가</span>' if i == 1 else ""
                rows.append(f"""
                <tr>
                    <td>{i}</td>
                    <td><a href="{product['url']}" target="_blank" class="product-link">{product['product']}</a></td>
                    <td>{product['platform']}</td>
                    <td><strong>{product['price']:,}원</strong> {badge}</td>
                </tr>
                """)

            products_html = f"""
            <table class="product-table">
                <thead>
                    <tr>
                        <th width="50">순위</th>
                        <th>상품명</th>
                        <th width="100">플랫폼</th>
                        <th width="150">가격</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(rows)}
                </tbody>
            </table>
            """

        return f"""
        <div class="section">
            <h2 class="section-title">💰 가격 분석</h2>
            <div class="price-section">
                <div class="price-grid">
                    <div class="price-card">
                        <div class="price-label">최저가</div>
                        <div class="price-value">{min_price:,}원</div>
                    </div>
                    <div class="price-card">
                        <div class="price-label">평균가</div>
                        <div class="price-value">{avg_price:,}원</div>
                    </div>
                    <div class="price-card">
                        <div class="price-label">최고가</div>
                        <div class="price-value">{max_price:,}원</div>
                    </div>
                </div>
            </div>
            {products_html}
        </div>
        """

    def _build_list(self, items: list) -> str:
        """리스트 HTML 생성"""
        if not items:
            return "<ul><li>데이터 없음</li></ul>"

        list_items = "\n".join([f"<li>{item}</li>" for item in items])
        return f"<ul>{list_items}</ul>"
