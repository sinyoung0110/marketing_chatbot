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
        self.project_dir = f"projects/{project_id}"

    def generate_html(
        self,
        analysis_result: Dict,
        product_input: Dict,
        competitor_data: Dict = None,
        review_insights: Dict = None
    ) -> str:
        """
        SWOT + 3C 분석 결과를 HTML로 생성

        Args:
            analysis_result: SWOT + 3C 분석 결과
            product_input: 상품 입력 정보
            competitor_data: 경쟁사 검색 데이터
            review_insights: 리뷰 분석 인사이트

        Returns:
            HTML 파일 경로
        """
        os.makedirs(self.project_dir, exist_ok=True)

        html_content = self._build_html(
            analysis_result,
            product_input,
            competitor_data,
            review_insights
        )

        # HTML 파일 저장
        html_path = f"{self.project_dir}/analysis.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"[AnalysisVisualizer] HTML 생성 완료: {html_path}")
        return html_path

    def _build_html(
        self,
        analysis: Dict,
        product_input: Dict,
        competitor_data: Dict = None,
        review_insights: Dict = None
    ) -> str:
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
            background: #f5f5f5;
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border: 1px solid #e0e0e0;
        }}

        .header {{
            background: #000;
            color: white;
            padding: 30px 40px;
            border-bottom: 1px solid #333;
        }}

        .header h1 {{
            font-size: 1.8em;
            margin-bottom: 8px;
            font-weight: 600;
        }}

        .header .subtitle {{
            font-size: 1em;
            opacity: 0.8;
        }}

        .header .date {{
            font-size: 0.85em;
            opacity: 0.6;
            margin-top: 8px;
        }}

        .insights {{
            background: #fafafa;
            padding: 25px 40px;
            border-bottom: 1px solid #e0e0e0;
        }}

        .insights h2 {{
            font-size: 1.3em;
            margin-bottom: 15px;
            color: #000;
            font-weight: 600;
        }}

        .insight-item {{
            background: white;
            padding: 12px 15px;
            margin-bottom: 8px;
            border: 1px solid #e0e0e0;
            border-left: 3px solid #000;
            font-size: 0.95em;
            line-height: 1.6;
        }}

        .content {{
            padding: 30px 40px;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section-title {{
            font-size: 1.5em;
            margin-bottom: 20px;
            font-weight: 600;
            color: #000;
            border-bottom: 2px solid #000;
            padding-bottom: 10px;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }}

        .card {{
            background: white;
            padding: 20px;
            border: 1px solid #e0e0e0;
        }}

        .card-title {{
            font-size: 1.2em;
            margin-bottom: 12px;
            color: #000;
            font-weight: 600;
            padding-bottom: 8px;
            border-bottom: 1px solid #e0e0e0;
        }}

        .card-content ul {{
            list-style: none;
            padding-left: 0;
        }}

        .card-content li {{
            padding: 8px 0;
            border-bottom: 1px solid #f5f5f5;
            color: #333;
            line-height: 1.5;
            font-size: 0.95em;
        }}

        .card-content li:last-child {{
            border-bottom: none;
        }}

        .card-content li:before {{
            content: "• ";
            color: #000;
            font-weight: bold;
            margin-right: 6px;
        }}

        .price-section {{
            background: #fafafa;
            color: #000;
            padding: 25px;
            border: 1px solid #e0e0e0;
            margin-bottom: 25px;
        }}

        .price-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 15px;
        }}

        .price-card {{
            background: white;
            padding: 15px;
            text-align: center;
            border: 1px solid #e0e0e0;
        }}

        .price-label {{
            font-size: 0.85em;
            color: #666;
            margin-bottom: 8px;
        }}

        .price-value {{
            font-size: 1.5em;
            font-weight: 600;
            color: #000;
        }}

        .product-table {{
            width: 100%;
            margin-top: 15px;
            border-collapse: collapse;
            background: white;
            border: 1px solid #e0e0e0;
        }}

        .product-table th {{
            background: #000;
            color: white;
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9em;
        }}

        .product-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
            color: #333;
            font-size: 0.9em;
        }}

        .product-table tr:last-child td {{
            border-bottom: none;
        }}

        .product-link {{
            color: #000;
            text-decoration: none;
            font-weight: 500;
        }}

        .product-link:hover {{
            text-decoration: underline;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 8px;
            background: #000;
            color: white;
            font-size: 0.8em;
            font-weight: 500;
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

            {self._build_competitor_links_section(competitor_data) if competitor_data else ""}

            {self._build_review_summary_section(review_insights) if review_insights else ""}
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

    def _build_competitor_links_section(self, competitor_data: Dict) -> str:
        """경쟁사 상품 링크 섹션"""
        if not competitor_data or not competitor_data.get("results"):
            return ""

        results = competitor_data.get("results", [])
        total_count = len(results)

        links_html = ""
        for idx, result in enumerate(results[:20], 1):  # 최대 20개만 표시
            platform = result.get("platform", "기타")
            title = result.get("title", "제목 없음")
            url = result.get("url", "#")
            snippet = result.get("snippet", "")[:150]  # 스니펫 150자 제한

            links_html += f"""
            <div class="competitor-link-item">
                <div class="link-header">
                    <span class="link-number">{idx}</span>
                    <span class="link-platform">{platform}</span>
                </div>
                <div class="link-title">
                    <a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a>
                </div>
                <div class="link-snippet">{snippet}</div>
            </div>
            """

        return f"""
        <div class="section">
            <h2 class="section-title">🔗 분석한 경쟁사 상품 ({total_count}개)</h2>
            <div class="competitor-links-container">
                {links_html}
            </div>
            <style>
                .competitor-links-container {{
                    display: grid;
                    gap: 15px;
                }}
                .competitor-link-item {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 4px solid #667eea;
                    transition: all 0.3s ease;
                }}
                .competitor-link-item:hover {{
                    transform: translateX(5px);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }}
                .link-header {{
                    display: flex;
                    gap: 10px;
                    margin-bottom: 10px;
                    align-items: center;
                }}
                .link-number {{
                    background: #667eea;
                    color: white;
                    width: 30px;
                    height: 30px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                    font-weight: bold;
                    font-size: 0.9em;
                }}
                .link-platform {{
                    background: #e9ecef;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 0.9em;
                    font-weight: 600;
                    color: #495057;
                }}
                .link-title {{
                    margin-bottom: 10px;
                }}
                .link-title a {{
                    color: #333;
                    text-decoration: none;
                    font-size: 1.1em;
                    font-weight: 600;
                }}
                .link-title a:hover {{
                    color: #667eea;
                    text-decoration: underline;
                }}
                .link-snippet {{
                    color: #6c757d;
                    font-size: 0.95em;
                    line-height: 1.5;
                }}
            </style>
        </div>
        """

    def _build_review_summary_section(self, review_insights: Dict) -> str:
        """리뷰 종합 섹션"""
        if not review_insights:
            return ""

        # 리뷰 인사이트 추출
        positive_points = review_insights.get("positive_points", [])
        negative_points = review_insights.get("negative_points", [])
        recommendations = review_insights.get("recommendations", [])
        sentiment_summary = review_insights.get("sentiment_summary", "")

        positive_html = ""
        for point in positive_points[:5]:
            positive_html += f"<li class='positive-item'>✅ {point}</li>"

        negative_html = ""
        for point in negative_points[:5]:
            negative_html += f"<li class='negative-item'>⚠️ {point}</li>"

        recommendations_html = ""
        for rec in recommendations[:5]:
            recommendations_html += f"<li class='recommendation-item'>💡 {rec}</li>"

        return f"""
        <div class="section">
            <h2 class="section-title">💬 고객 리뷰 종합</h2>

            {f'<div class="review-summary"><p>{sentiment_summary}</p></div>' if sentiment_summary else ''}

            <div class="review-grid">
                <div class="review-box positive-box">
                    <h3>👍 긍정적 반응</h3>
                    <ul>{positive_html if positive_html else '<li>데이터 없음</li>'}</ul>
                </div>

                <div class="review-box negative-box">
                    <h3>👎 부정적 반응</h3>
                    <ul>{negative_html if negative_html else '<li>데이터 없음</li>'}</ul>
                </div>
            </div>

            {f'<div class="recommendations-box"><h3>📌 개선 제안</h3><ul>{recommendations_html}</ul></div>' if recommendations_html else ''}

            <style>
                .review-summary {{
                    background: #e7f3ff;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    font-size: 1.1em;
                    line-height: 1.6;
                }}
                .review-grid {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 20px;
                    margin-bottom: 20px;
                }}
                .review-box {{
                    padding: 25px;
                    border-radius: 10px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                .positive-box {{
                    background: #d4edda;
                    border-left: 5px solid #28a745;
                }}
                .negative-box {{
                    background: #f8d7da;
                    border-left: 5px solid #dc3545;
                }}
                .review-box h3 {{
                    margin-bottom: 15px;
                    font-size: 1.3em;
                }}
                .review-box ul {{
                    list-style: none;
                    padding: 0;
                }}
                .review-box li {{
                    padding: 10px;
                    margin-bottom: 8px;
                    background: white;
                    border-radius: 5px;
                    font-size: 1em;
                }}
                .recommendations-box {{
                    background: #fff3cd;
                    border-left: 5px solid #ffc107;
                    padding: 25px;
                    border-radius: 10px;
                }}
                .recommendations-box h3 {{
                    margin-bottom: 15px;
                    font-size: 1.3em;
                }}
                .recommendations-box ul {{
                    list-style: none;
                    padding: 0;
                }}
                .recommendations-box li {{
                    padding: 10px;
                    margin-bottom: 8px;
                    background: white;
                    border-radius: 5px;
                    font-size: 1em;
                }}
                @media (max-width: 768px) {{
                    .review-grid {{
                        grid-template-columns: 1fr;
                    }}
                }}
            </style>
        </div>
        """
