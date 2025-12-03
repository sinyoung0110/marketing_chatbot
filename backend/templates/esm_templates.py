"""
ESM+ / 스마트스토어 / 쿠팡 호환 상세페이지 템플릿 생성기
"""
import re

def _markdown_to_html(text: str) -> str:
    """마크다운을 HTML로 변환 (가독성 최대화)"""
    if not text:
        return ""

    # 헤더 변환 (##### 부터 # 까지 모두 처리, 아이콘 제거)
    text = re.sub(r'^##### (.+)$', r'<h5 style="font-size:16px;font-weight:600;margin:16px 0 8px;color:#555;border-left:3px solid var(--accent);padding-left:10px">\1</h5>', text, flags=re.MULTILINE)
    text = re.sub(r'^#### (.+)$', r'<h4 style="font-size:18px;font-weight:600;margin:20px 0 10px;color:#444;border-left:3px solid var(--accent);padding-left:10px">\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h3 style="font-size:20px;font-weight:600;margin:24px 0 12px;color:#333;border-left:4px solid var(--accent);padding-left:12px">\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2 style="font-size:24px;font-weight:700;margin:32px 0 16px;color:#222">\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1 style="font-size:28px;font-weight:700;margin:28px 0 20px;color:#111">\1</h1>', text, flags=re.MULTILINE)

    # 볼드 변환 (색상 제거, 자연스럽게)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong style="font-weight:700">\1</strong>', text)

    # 리스트 변환 (박스형 디자인)
    lines = text.split('\n')
    result_lines = []
    in_list = False

    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result_lines.append('<ul style="margin:20px 0;padding:0;list-style:none">')
                in_list = True
            item = line.strip()[2:]  # "- " 제거
            result_lines.append(f'  <li style="margin:12px 0;padding:14px 18px;background:#f9fafb;border-left:4px solid var(--accent);border-radius:8px;line-height:1.7;font-size:16px">✓ {item}</li>')
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)

    if in_list:
        result_lines.append('</ul>')

    text = '\n'.join(result_lines)

    # 단락 변환 (여백 증가, 가독성 강화)
    paragraphs = text.split('\n\n')
    html_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if para and not para.startswith('<'):
            para = f'<p style="margin:20px 0;line-height:1.9;font-size:17px;color:#333">{para}</p>'
        elif para.startswith('<p>'):
            # 이미 <p> 태그가 있으면 스타일 추가
            para = para.replace('<p>', '<p style="margin:20px 0;line-height:1.9;font-size:17px;color:#333">')
        html_paragraphs.append(para)

    return '\n'.join(html_paragraphs)

def generate_esm_html(content_sections: dict, images: list, product_input: dict) -> str:
    """
    ESM+ 가이드라인 준수 HTML 템플릿 생성
    카테고리를 자동 감지하여 최적 템플릿 선택
    """
    category = product_input.get('category', '').lower()
    product_name = product_input.get('product_name', '').lower()

    # 카테고리 자동 감지
    detected_category = _detect_category(category, product_name)

    print(f"[ESM Template] 감지된 카테고리: {detected_category}")

    # 감지된 카테고리에 따라 범용 템플릿 생성 (동적 섹션)
    return _universal_template(content_sections, images, product_input, detected_category)


def _detect_category(category: str, product_name: str) -> str:
    """카테고리 자동 감지"""
    combined = f"{category} {product_name}".lower()

    # 카테고리별 키워드 매핑
    category_keywords = {
        'beauty': ['뷰티', '화장품', '스킨케어', '메이크업', '립', '세럼', '크림', '팩', '마스크', '클렌징', '선크림', '토너', '에센스', '로션', '쿠션', '파운데이션'],
        'fashion': ['의류', '패션', '옷', '셔츠', '바지', '원피스', '가방', '신발', '액세서리', '모자', '스카프'],
        'food': ['식품', '음식', '간식', '과자', '음료', '고기', '육류', '생선', '채소', '과일'],
        'electronics': ['전자', '가전', '스마트폰', '노트북', '태블릿', '이어폰', '헤드폰', '카메라'],
        'home': ['가구', '인테리어', '주방', '생활용품', '침구', '수납'],
        'sports': ['스포츠', '운동', '헬스', '요가', '등산', '자전거'],
        'baby': ['유아', '아기', '베이비', '어린이', '키즈'],
        'pet': ['반려동물', '펫', '강아지', '고양이', '애완'],
    }

    for cat_type, keywords in category_keywords.items():
        if any(kw in combined for kw in keywords):
            return cat_type

    return 'general'


def _clothing_template(content_sections: dict, images: list, product_input: dict) -> str:
    """의류 전용 ESM+ 템플릿"""
    product_name = product_input.get('product_name', 'PRODUCT_TITLE')
    selling_points = content_sections.get('selling_points', [])[:3]
    specs = content_sections.get('specs', {})
    summary = content_sections.get('summary', '한 줄 USP 문구')
    detailed_desc_raw = content_sections.get('detailed_description', {}).get('content', '제품 상세 소개')
    detailed_desc = _markdown_to_html(detailed_desc_raw)

    # 이미지 할당
    main_img = images[0] if images else 'https://via.placeholder.com/860x1000'
    detail_imgs = (images[1:6] + ['https://via.placeholder.com/428x428']*5)[:5]

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{product_name}</title>
<style>
:root{{--bg:#fff;--sub:#f8f9fa;--text:#111827;--line:#e5e7eb}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Pretendard','Noto Sans KR',sans-serif;color:var(--text);background:var(--sub);line-height:1.6}}
.wrap{{max-width:860px;margin:0 auto;background:var(--bg);padding:20px}}
h1{{font-size:32px;font-weight:700;margin:20px 0}}
h2{{font-size:26px;font-weight:700;margin:40px 0 24px;border-bottom:2px solid #000;padding-bottom:10px}}
h3{{font-size:22px;font-weight:600;margin:24px 0 16px}}
p{{font-size:18px;margin:15px 0}}
.section{{padding:28px 0;border-bottom:1px solid var(--line)}}

.intro{{text-align:center}}
.hero-img{{width:100%;max-width:860px;border-radius:12px}}
.usp-list{{display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin:20px 0}}
.usp{{background:#fafafa;border:1px solid var(--line);padding:12px 18px;border-radius:10px;font-size:16px}}

.detail-block{{display:flex;gap:20px;align-items:center;margin:32px 0}}
.detail-block .img{{width:50%}}
.detail-block img{{width:100%;border-radius:12px}}
.detail-block .txt{{width:50%}}

table{{width:100%;border-collapse:collapse;margin:20px 0;border:1px solid var(--line)}}
th,td{{border:1px solid var(--line);padding:12px;text-align:left}}
th{{background:var(--sub);font-weight:600}}

@media(max-width:760px){{
.detail-block{{flex-direction:column}}
.detail-block .img,.detail-block .txt{{width:100%}}
h1{{font-size:28px}}
h2{{font-size:22px}}
p{{font-size:16px}}
}}
</style>
</head>
<body>
<div class="wrap">

<!-- 1. 인트로 -->
<section class="section intro">
  <img src="{main_img}" alt="{product_name}" class="hero-img">
  <h1>{product_name}</h1>
  <p style="font-size:18px;color:#555">{summary}</p>
  <div class="usp-list">
"""

    for sp in selling_points:
        html += f'    <div class="usp">{sp.get("title", "")}</div>\n'

    html += f"""  </div>
</section>

<!-- 2. 제품 소개 -->
<section class="section">
  <h2>제품 소개</h2>
  <p>{detailed_desc}</p>
</section>

<!-- 3. 상품상세 (지그재그 5세트) -->
<section class="section">
  <h2>제품 디테일 포인트</h2>
"""

    # 지그재그 레이아웃
    details = [
        ("소재 & 품질", "프리미엄 소재로 착용감이 우수합니다"),
        ("디자인", "세련되고 실용적인 디자인"),
        ("활용도", "다양한 스타일링 가능"),
        ("내구성", "꼼꼼한 마감 처리"),
        ("관리", "세탁 및 보관 방법")
    ]

    for idx, (title, desc) in enumerate(details):
        img = detail_imgs[idx]
        direction = '' if idx % 2 == 0 else 'style="flex-direction:row-reverse"'
        html += f"""
  <div class="detail-block" {direction}>
    <div class="img"><img src="{img}" alt="{title}" title="{title}"></div>
    <div class="txt">
      <h3>{idx+1:02d}. {title}</h3>
      <p>{desc}</p>
    </div>
  </div>
"""

    html += """</section>

<!-- 4. 사이즈 정보 -->
<section class="section">
  <h2>사이즈 정보</h2>
  <table>
    <thead>
      <tr><th>사이즈</th><th>총장(cm)</th><th>가슴/허리(cm)</th><th>어깨(cm)</th></tr>
    </thead>
    <tbody>
      <tr><td>S</td><td>65</td><td>88</td><td>40</td></tr>
      <tr><td>M</td><td>67</td><td>92</td><td>42</td></tr>
      <tr><td>L</td><td>69</td><td>96</td><td>44</td></tr>
      <tr><td>XL</td><td>71</td><td>100</td><td>46</td></tr>
    </tbody>
  </table>
  <p style="font-size:15px;color:#666">* 재는 방식에 따라 ± 1~3cm 오차 발생 가능</p>
</section>

<!-- 5. 소재 & 사양 -->
<section class="section">
  <h2>소재 & 제품 사양</h2>
  <table>
"""

    for key, value in specs.items():
        html += f"    <tr><th>{key}</th><td>{value}</td></tr>\n"

    html += """  </table>
</section>
"""

    # 상품 비교 섹션 - N/A 값 필터링
    comparison_chart = content_sections.get("comparison_chart", {})
    if comparison_chart.get("our_product") and comparison_chart.get("competitors"):
        # N/A, None, 빈값이 없는 경쟁사만 필터링
        valid_competitors = []
        for comp in comparison_chart.get("competitors", []):
            if all(comp.get(k) not in [None, "N/A", "n/a", "", 0] for k in ['name', 'price', 'quality', 'delivery', 'rating']):
                valid_competitors.append(comp)

        # 유효한 경쟁사가 있을 때만 테이블 생성
        if valid_competitors:
            html += """
<!-- 6. 제품 비교 -->
<section class="section">
  <h2>제품 비교</h2>
  <table>
    <thead>
      <tr><th>제품명</th><th>가격</th><th>품질</th><th>배송</th><th>평점</th></tr>
    </thead>
    <tbody>
"""
            our = comparison_chart["our_product"]
            html += f"""
      <tr style="background:#f8f9fa;border-left:3px solid #495057">
        <td><strong>{our['name']}</strong></td>
        <td><strong>{our['price']}</strong></td>
        <td><strong>{our['quality']}</strong></td>
        <td><strong>{our['delivery']}</strong></td>
        <td><strong>{our['rating']} ⭐</strong></td>
      </tr>
"""
            for comp in valid_competitors:
                html += f"""
      <tr>
        <td>{comp['name']}</td>
        <td>{comp['price']}</td>
        <td>{comp['quality']}</td>
        <td>{comp['delivery']}</td>
        <td>{comp['rating']} ⭐</td>
      </tr>
"""
            html += """    </tbody>
  </table>
</section>
"""

    html += """
<!-- 7. 구매 안내 -->
<section class="section">
  <h2>구매 전 확인사항</h2>
  <ul style="font-size:16px;color:#666;padding-left:20px;line-height:1.8">
    <li>개봉 후 교환/반품 제한 있음</li>
    <li>수작업 계측으로 1~3cm 오차 가능</li>
    <li>모니터 환경에 따른 색상 차이 있음</li>
  </ul>
  <h3 style="margin-top:20px">고객센터</h3>
  <p style="font-size:15px;color:#666">☎ 1234-5678 | 평일 10:00~17:00</p>
</section>

</div>
</body>
</html>"""

    return html


def _food_template(content_sections: dict, images: list, product_input: dict) -> str:
    """식품 전용 ESM+ 템플릿"""
    product_name = product_input.get('product_name', 'PRODUCT_TITLE')
    selling_points = content_sections.get('selling_points', [])[:3]
    specs = content_sections.get('specs', {})
    summary = content_sections.get('summary', '한 줄 USP 문구')
    detailed_desc_raw = content_sections.get('detailed_description', {}).get('content', '제품 상세 소개')
    detailed_desc = _markdown_to_html(detailed_desc_raw)
    nutrition = content_sections.get('nutrition_info', {})

    main_img = images[0] if images else 'https://via.placeholder.com/860x1000'
    detail_imgs = (images[1:6] + ['https://via.placeholder.com/428x428']*5)[:5]

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{product_name}</title>
<style>
:root{{--bg:#fff;--sub:#f8f9fa;--text:#111827;--line:#e5e7eb;--highlight:#fff7f0}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Pretendard','Noto Sans KR',sans-serif;color:var(--text);background:var(--sub);line-height:1.6}}
.wrap{{max-width:860px;margin:0 auto;background:var(--bg);padding:20px}}
h1{{font-size:32px;font-weight:700;margin:20px 0}}
h2{{font-size:26px;font-weight:700;margin:40px 0 24px;border-bottom:2px solid #000;padding-bottom:10px}}
h3{{font-size:22px;font-weight:600;margin:24px 0 16px}}
p{{font-size:18px;margin:15px 0}}
.section{{padding:28px 0;border-bottom:1px solid var(--line)}}

.intro{{text-align:center}}
.hero-img{{width:100%;max-width:860px;border-radius:12px}}
.usp-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;margin:24px 0}}
.usp{{padding:20px;background:#fafafa;border:1px solid var(--line);border-radius:12px;text-align:center}}

.highlight{{padding:20px;background:var(--highlight);border:2px solid #f7c59f;border-radius:12px;margin:24px 0}}

.detail-block{{display:flex;gap:20px;align-items:center;margin:32px 0}}
.detail-block .img{{width:50%}}
.detail-block img{{width:100%;border-radius:12px}}
.detail-block .txt{{width:50%}}

table{{width:100%;border-collapse:collapse;margin:20px 0;border:1px solid var(--line)}}
th,td{{border:1px solid var(--line);padding:12px}}
th{{background:var(--sub);font-weight:600;text-align:left}}
td{{text-align:left}}

@media(max-width:760px){{
.detail-block{{flex-direction:column}}
.detail-block .img,.detail-block .txt{{width:100%}}
.usp-grid{{grid-template-columns:1fr}}
h1{{font-size:28px}}
h2{{font-size:22px}}
}}
</style>
</head>
<body>
<div class="wrap">

<!-- 1. 인트로 -->
<section class="section intro">
  <img src="{main_img}" alt="{product_name}" class="hero-img">
  <h1>{product_name}</h1>
  <p style="font-size:18px;color:#555">{summary}</p>

  <div class="usp-grid">
"""

    labels = ["신선한 원재료", "영양 균형", "간편 섭취"]
    for idx, sp in enumerate(selling_points):
        title = sp.get('title', labels[idx] if idx < len(labels) else '특징')
        desc = sp.get('description', '')
        html += f"""    <div class="usp">
      <h3 style="margin-bottom:8px">{title}</h3>
      <p style="font-size:16px;color:#555">{desc}</p>
    </div>
"""

    html += f"""  </div>
</section>

<!-- 2. 제품 소개 -->
<section class="section">
  <h2>제품 소개</h2>
  <p>{detailed_desc}</p>
</section>

<!-- 3. 원재료 정보 -->
<section class="section">
  <div class="highlight">
    <h2 style="color:#d5723c;margin-top:0">원재료 정보</h2>
    <ul style="font-size:18px;color:#555;padding-left:20px;line-height:1.8">
      <li>원재료 1: 국내산 신선 재료</li>
      <li>원재료 2: 무첨가 천연 성분</li>
      <li>원재료 3: HACCP 인증 공장</li>
      <li>보존료/인공첨가물 무첨가</li>
    </ul>
  </div>
</section>
"""

    # 영양성분표
    if nutrition.get('has_nutrition'):
        html += """
<!-- 4. 영양성분표 -->
<section class="section">
  <h2>영양성분표</h2>
  <table>
    <thead>
      <tr><th>영양성분</th><th>1회 제공량</th><th>함량</th><th>%기준치</th></tr>
    </thead>
    <tbody>
      <tr><td>열량</td><td>100g</td><td>200kcal</td><td>10%</td></tr>
      <tr><td>단백질</td><td>100g</td><td>10g</td><td>18%</td></tr>
      <tr><td>지방</td><td>100g</td><td>5g</td><td>9%</td></tr>
      <tr><td>탄수화물</td><td>100g</td><td>30g</td><td>12%</td></tr>
      <tr><td>나트륨</td><td>100g</td><td>50mg</td><td>3%</td></tr>
    </tbody>
  </table>
  <p style="font-size:14px;color:#666">* 1회 제공량 기준</p>
</section>
"""

    # 지그재그 상세
    html += """
<!-- 5. 상품상세 -->
<section class="section">
  <h2>제품 디테일 포인트</h2>
"""

    details = [
        ("맛과 식감", "신선하고 자연스러운 맛"),
        ("영양 성분", "균형 잡힌 영양 구성"),
        ("제조 공정", "위생적 제조 환경"),
        ("보관 방법", "신선도 유지 보관법"),
        ("섭취 방법", "간편하게 즐기기")
    ]

    for idx, (title, desc) in enumerate(details):
        img = detail_imgs[idx]
        direction = '' if idx % 2 == 0 else 'style="flex-direction:row-reverse"'
        html += f"""
  <div class="detail-block" {direction}>
    <div class="img"><img src="{img}" alt="{title}" title="{title}"></div>
    <div class="txt">
      <h3>{idx+1:02d}. {title}</h3>
      <p>{desc}</p>
    </div>
  </div>
"""

    html += """</section>

<!-- 6. 식품 정보 -->
<section class="section">
  <h2>식품 정보</h2>
  <table>
"""

    for key, value in specs.items():
        html += f"    <tr><th>{key}</th><td>{value}</td></tr>\n"

    html += """  </table>
</section>
"""

    # 레시피 제안 섹션 (식품인 경우)
    recipes = content_sections.get("recipe_suggestions", {})
    if recipes.get("has_recipes"):
        html += f"""
<!-- 7. 레시피 제안 -->
<section class="section">
  <h2>추천 레시피</h2>
  <div style="background:#fff7f0;padding:20px;border-radius:12px;border:1px solid #f7c59f">
    {_markdown_to_html(recipes.get("content", ""))}
  </div>
</section>
"""

    html += """
<!-- 8. 구매 안내 -->
<section class="section">
  <h2>구매 전 확인사항</h2>
  <ul style="font-size:16px;color:#666;padding-left:20px;line-height:1.8">
    <li>개봉 후 교환/반품 제한 있음</li>
    <li>유통기한 및 보관방법 확인 필수</li>
    <li>알레르기 정보 확인 권장</li>
  </ul>
  <h3 style="margin-top:20px">고객센터</h3>
  <p style="font-size:15px;color:#666">☎ 1234-5678 | 평일 10:00~17:00</p>
</section>

</div>
</body>
</html>"""

    return html


def _general_template(content_sections: dict, images: list, product_input: dict) -> str:
    """일반 상품 템플릿"""
    product_name = product_input.get('product_name', 'PRODUCT_TITLE')
    selling_points = content_sections.get('selling_points', [])[:3]
    specs = content_sections.get('specs', {})
    summary = content_sections.get('summary', 'USP 문구')
    detailed_desc_raw = content_sections.get('detailed_description', {}).get('content', '상세 소개')
    detailed_desc = _markdown_to_html(detailed_desc_raw)

    main_img = images[0] if images else 'https://via.placeholder.com/860x1000'

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{product_name}</title>
<style>
:root{{--bg:#fff;--sub:#f8f9fa;--text:#111827;--line:#e5e7eb}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Pretendard','Noto Sans KR',sans-serif;color:var(--text);background:var(--sub);line-height:1.6}}
.wrap{{max-width:860px;margin:0 auto;background:var(--bg);padding:20px}}
h1{{font-size:32px;font-weight:700;margin:20px 0}}
h2{{font-size:26px;font-weight:700;margin:40px 0 24px}}
p{{font-size:18px;margin:15px 0}}
table{{width:100%;border-collapse:collapse;margin:20px 0}}
th,td{{border:1px solid var(--line);padding:12px}}
th{{background:var(--sub)}}
</style>
</head>
<body>
<div class="wrap">
  <img src="{main_img}" style="width:100%;border-radius:12px" alt="{product_name}">
  <h1>{product_name}</h1>
  <p>{summary}</p>
  <h2>제품 소개</h2>
  <p>{detailed_desc}</p>
  <h2>제품 사양</h2>
  <table>
"""

    for key, value in specs.items():
        html += f"    <tr><th>{key}</th><td>{value}</td></tr>\n"

    html += """  </table>
"""

    # 상품 비교 섹션 - N/A 값 필터링
    comparison_chart = content_sections.get("comparison_chart", {})
    if comparison_chart.get("our_product") and comparison_chart.get("competitors"):
        # N/A, None, 빈값이 없는 경쟁사만 필터링
        valid_competitors = []
        for comp in comparison_chart.get("competitors", []):
            if all(comp.get(k) not in [None, "N/A", "n/a", "", 0] for k in ['name', 'price', 'quality', 'delivery', 'rating']):
                valid_competitors.append(comp)

        # 유효한 경쟁사가 있을 때만 테이블 생성
        if valid_competitors:
            html += """
  <h2>제품 비교</h2>
  <table>
    <thead>
      <tr><th>제품명</th><th>가격</th><th>품질</th><th>배송</th><th>평점</th></tr>
    </thead>
    <tbody>
"""
            our = comparison_chart["our_product"]
            html += f"""
      <tr style="background:#f8f9fa;border-left:3px solid #495057">
        <td><strong>{our['name']}</strong></td>
        <td><strong>{our['price']}</strong></td>
        <td><strong>{our['quality']}</strong></td>
        <td><strong>{our['delivery']}</strong></td>
        <td><strong>{our['rating']} ⭐</strong></td>
      </tr>
"""
            for comp in valid_competitors:
                html += f"""
      <tr>
        <td>{comp['name']}</td>
        <td>{comp['price']}</td>
        <td>{comp['quality']}</td>
        <td>{comp['delivery']}</td>
        <td>{comp['rating']} ⭐</td>
      </tr>
"""
            html += """    </tbody>
  </table>
"""

    html += """
</div>
</body>
</html>"""

    return html


def _beauty_template(content_sections: dict, images: list, product_input: dict) -> str:
    """뷰티/화장품 전용 ESM+ 템플릿"""
    product_name = product_input.get('product_name', 'PRODUCT_TITLE')
    selling_points = content_sections.get('selling_points', [])[:3]
    specs = content_sections.get('specs', {})
    summary = content_sections.get('summary', '한 줄 USP 문구')
    detailed_desc_raw = content_sections.get('detailed_description', {}).get('content', '제품 상세 소개')
    detailed_desc = _markdown_to_html(detailed_desc_raw)

    # 이미지 할당
    main_img = images[0] if images else 'https://via.placeholder.com/860x1000'
    detail_imgs = (images[1:6] + ['https://via.placeholder.com/428x428']*5)[:5]

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{product_name}</title>
<style>
:root{{--bg:#fff;--sub:#fef9f6;--text:#111827;--line:#f0e5de;--accent:#d4a574}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Pretendard','Noto Sans KR',sans-serif;color:var(--text);background:var(--sub);line-height:1.6}}
.wrap{{max-width:860px;margin:0 auto;background:var(--bg);padding:20px}}
h1{{font-size:32px;font-weight:700;margin:20px 0;color:#8b6f47}}
h2{{font-size:26px;font-weight:700;margin:40px 0 24px;border-bottom:2px solid var(--accent);padding-bottom:10px;color:#8b6f47}}
h3{{font-size:22px;font-weight:600;margin:24px 0 16px}}
p{{font-size:18px;margin:15px 0}}
.section{{padding:28px 0;border-bottom:1px solid var(--line)}}

.intro{{text-align:center}}
.hero-img{{width:100%;max-width:860px;border-radius:12px}}
.benefit-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;margin:24px 0}}
.benefit{{padding:20px;background:var(--sub);border:2px solid var(--accent);border-radius:12px;text-align:center}}
.benefit h3{{color:var(--accent);margin-bottom:12px}}

.highlight{{padding:24px;background:linear-gradient(135deg,#fef9f6 0%,#f8ede3 100%);border:2px solid var(--accent);border-radius:12px;margin:24px 0}}

.detail-block{{display:flex;gap:20px;align-items:center;margin:32px 0}}
.detail-block .img{{width:50%}}
.detail-block img{{width:100%;border-radius:12px}}
.detail-block .txt{{width:50%}}

table{{width:100%;border-collapse:collapse;margin:20px 0;border:1px solid var(--line)}}
th,td{{border:1px solid var(--line);padding:12px;text-align:left}}
th{{background:var(--sub);font-weight:600}}

.ingredient-list{{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0}}
.ingredient{{background:var(--sub);border:1px solid var(--accent);padding:8px 16px;border-radius:20px;font-size:14px}}

@media(max-width:760px){{
.detail-block{{flex-direction:column}}
.detail-block .img,.detail-block .txt{{width:100%}}
.benefit-grid{{grid-template-columns:1fr}}
h1{{font-size:28px}}
h2{{font-size:22px}}
p{{font-size:16px}}
}}
</style>
</head>
<body>
<div class="wrap">

<!-- 1. 인트로 -->
<section class="section intro">
  <img src="{main_img}" alt="{product_name}" class="hero-img">
  <h1>{product_name}</h1>
  <p style="font-size:18px;color:#8b6f47">{summary}</p>

  <div class="benefit-grid">
"""

    benefit_labels = ["피부 효능", "주요 성분", "사용감"]
    for idx, sp in enumerate(selling_points):
        title = sp.get('title', benefit_labels[idx] if idx < len(benefit_labels) else '특징')
        desc = sp.get('description', '')
        html += f"""    <div class="benefit">
      <h3>{title}</h3>
      <p style="font-size:16px;color:#555">{desc}</p>
    </div>
"""

    html += f"""  </div>
</section>

<!-- 2. 제품 소개 -->
<section class="section">
  <h2>제품 소개</h2>
  <p>{detailed_desc}</p>
</section>

<!-- 3. 핵심 성분 -->
<section class="section">
  <div class="highlight">
    <h2 style="color:#8b6f47;margin-top:0">핵심 성분</h2>
    <div class="ingredient-list">
      <div class="ingredient">✓ 주요 성분 1</div>
      <div class="ingredient">✓ 주요 성분 2</div>
      <div class="ingredient">✓ 주요 성분 3</div>
      <div class="ingredient">✓ 피부 친화 성분</div>
      <div class="ingredient">✓ 자극 최소화</div>
    </div>
    <p style="font-size:16px;color:#666;margin-top:16px">피부 타입을 고려한 안전한 성분으로 구성되었습니다.</p>
  </div>
</section>

<!-- 4. 사용 방법 & 효과 (지그재그) -->
<section class="section">
  <h2>사용 방법 & 효과</h2>
"""

    usage_details = [
        ("STEP 1. 준비", "깨끗하게 세안한 피부에 준비합니다"),
        ("STEP 2. 적용", "적당량을 덜어 피부에 골고루 펴 발라줍니다"),
        ("STEP 3. 흡수", "가볍게 두드려 흡수시킵니다"),
        ("STEP 4. 마무리", "다음 스킨케어 단계로 넘어갑니다"),
        ("기대 효과", "지속적인 사용으로 건강한 피부를 경험하세요")
    ]

    for idx, (title, desc) in enumerate(usage_details):
        img = detail_imgs[idx] if idx < len(detail_imgs) else detail_imgs[-1]
        direction = '' if idx % 2 == 0 else 'style="flex-direction:row-reverse"'
        html += f"""
  <div class="detail-block" {direction}>
    <div class="img"><img src="{img}" alt="{title}" title="{title}"></div>
    <div class="txt">
      <h3>{title}</h3>
      <p>{desc}</p>
    </div>
  </div>
"""

    html += """</section>

<!-- 5. 제품 정보 -->
<section class="section">
  <h2>제품 정보</h2>
  <table>
"""

    for key, value in specs.items():
        html += f"    <tr><th>{key}</th><td>{value}</td></tr>\n"

    html += """  </table>
</section>
"""

    # 상품 비교 섹션 - N/A 값 필터링
    comparison_chart = content_sections.get("comparison_chart", {})
    if comparison_chart.get("our_product") and comparison_chart.get("competitors"):
        # N/A, None, 빈값이 없는 경쟁사만 필터링
        valid_competitors = []
        for comp in comparison_chart.get("competitors", []):
            if all(comp.get(k) not in [None, "N/A", "n/a", "", 0] for k in ['name', 'price', 'quality', 'delivery', 'rating']):
                valid_competitors.append(comp)

        # 유효한 경쟁사가 있을 때만 테이블 생성
        if valid_competitors:
            html += """
<!-- 6. 제품 비교 -->
<section class="section">
  <h2>제품 비교</h2>
  <table>
    <thead>
      <tr><th>제품명</th><th>가격</th><th>품질</th><th>배송</th><th>평점</th></tr>
    </thead>
    <tbody>
"""
            our = comparison_chart["our_product"]
            html += f"""
      <tr style="background:var(--sub);border-left:3px solid var(--accent)">
        <td><strong>{our['name']}</strong></td>
        <td><strong>{our['price']}</strong></td>
        <td><strong>{our['quality']}</strong></td>
        <td><strong>{our['delivery']}</strong></td>
        <td><strong>{our['rating']} ⭐</strong></td>
      </tr>
"""
            for comp in valid_competitors:
                html += f"""
      <tr>
        <td>{comp['name']}</td>
        <td>{comp['price']}</td>
        <td>{comp['quality']}</td>
        <td>{comp['delivery']}</td>
        <td>{comp['rating']} ⭐</td>
      </tr>
"""
            html += """    </tbody>
  </table>
</section>
"""

    html += """
<!-- 7. 사용 주의사항 -->
<section class="section">
  <h2>사용 주의사항</h2>
  <ul style="font-size:16px;color:#666;padding-left:20px;line-height:1.8">
    <li>화장품 사용 시 또는 사용 후 직사광선에 의하여 사용부위가 붉은 반점, 부어오름 또는 가려움증 등의 이상 증상이나 부작용이 있는 경우 전문의 등과 상담하시기 바랍니다</li>
    <li>상처가 있는 부위 등에는 사용을 자제해주세요</li>
    <li>보관 및 취급 시 주의사항: 어린이의 손이 닿지 않는 곳에 보관</li>
    <li>직사광선을 피해서 보관</li>
  </ul>
  <h3 style="margin-top:20px">고객센터</h3>
  <p style="font-size:15px;color:#666">☎ 1234-5678 | 평일 10:00~17:00</p>
</section>

</div>
</body>
</html>"""

    return html


def _universal_template(content_sections: dict, images: list, product_input: dict, category_type: str) -> str:
    """모든 카테고리에 범용적으로 대응하는 동적 템플릿"""

    # 카테고리별 색상 및 스타일 설정
    styles = _get_category_styles(category_type)

    product_name = product_input.get('product_name', 'PRODUCT_TITLE')
    selling_points = content_sections.get('selling_points', [])[:3]
    specs = content_sections.get('specs', {})
    summary = content_sections.get('summary', '한 줄 USP 문구')
    detailed_desc_raw = content_sections.get('detailed_description', {}).get('content', '제품 상세 소개')
    detailed_desc = _markdown_to_html(detailed_desc_raw)

    # 이미지 할당
    main_img = images[0] if images else 'https://via.placeholder.com/860x1000'
    detail_imgs = (images[1:6] + ['https://via.placeholder.com/428x428']*5)[:5]

    html = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{product_name}</title>
<style>
:root{{
  --bg:{styles['bg']};
  --sub:{styles['sub']};
  --text:{styles['text']};
  --line:{styles['line']};
  --accent:{styles['accent']};
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Pretendard','Noto Sans KR',sans-serif;color:var(--text);background:var(--sub);line-height:1.6}}
.wrap{{max-width:860px;margin:0 auto;background:var(--bg);padding:20px}}
h1{{font-size:32px;font-weight:700;margin:20px 0;color:{styles['h1_color']}}}
h2{{font-size:26px;font-weight:700;margin:40px 0 24px;border-bottom:2px solid var(--accent);padding-bottom:10px;color:{styles['h2_color']}}}
h3{{font-size:22px;font-weight:600;margin:24px 0 16px}}
p{{font-size:18px;margin:15px 0}}
.section{{padding:28px 0;border-bottom:1px solid var(--line)}}

.intro{{text-align:center}}
.hero-img{{width:100%;max-width:860px;border-radius:12px}}
.benefit-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;margin:24px 0}}
.benefit{{padding:20px;background:var(--sub);border:2px solid var(--accent);border-radius:12px;text-align:center}}
.benefit h3{{color:var(--accent);margin-bottom:12px}}

.highlight{{padding:28px 24px;background:{styles['highlight_bg']};border:2px solid var(--accent);border-radius:12px;margin:24px 0;box-shadow:0 2px 8px rgba(0,0,0,0.08)}}

.detail-block{{display:flex;gap:20px;align-items:center;margin:32px 0}}
.detail-block .img{{width:50%}}
.detail-block img{{width:100%;border-radius:12px}}
.detail-block .txt{{width:50%}}

table{{width:100%;border-collapse:collapse;margin:20px 0;border:1px solid var(--line)}}
th,td{{border:1px solid var(--line);padding:12px;text-align:left}}
th{{background:var(--sub);font-weight:600}}

@media(max-width:760px){{
.detail-block{{flex-direction:column}}
.detail-block .img,.detail-block .txt{{width:100%}}
.benefit-grid{{grid-template-columns:1fr}}
h1{{font-size:28px}}
h2{{font-size:22px}}
p{{font-size:16px}}
}}
</style>
</head>
<body>
<div class="wrap">

<!-- 1. 인트로 -->
<section class="section intro">
  <img src="{main_img}" alt="{product_name}" class="hero-img">
  <h1>{product_name}</h1>
  <p style="font-size:18px;color:{styles['summary_color']}">{summary}</p>

  <div class="benefit-grid">
"""

    # 셀링 포인트 동적 생성
    for sp in selling_points:
        title = sp.get('title', '특징')
        desc = sp.get('description', '')
        html += f"""    <div class="benefit">
      <h3>{title}</h3>
      <p style="font-size:16px;color:#555">{desc}</p>
    </div>
"""

    html += f"""  </div>
</section>

<!-- 2. 제품 소개 -->
<section class="section">
  <h2>제품 소개</h2>
  <div style="padding:24px;background:#fff;border:1px solid #e5e7eb;border-radius:12px;margin:24px 0">
    {detailed_desc}
  </div>
</section>
"""

    # 카테고리별 특수 섹션 동적 추가
    html += _generate_category_specific_sections(content_sections, category_type, styles)

    # 3. 제품 디테일 (지그재그 레이아웃)
    html += f"""
<!-- 제품 디테일 포인트 -->
<section class="section">
  <h2>{_get_detail_section_title(category_type)}</h2>
"""

    # 동적 디테일 포인트 생성
    detail_points = _generate_detail_points(category_type, selling_points)

    for idx, (title, desc) in enumerate(detail_points[:5]):
        img = detail_imgs[idx] if idx < len(detail_imgs) else detail_imgs[-1]
        direction = '' if idx % 2 == 0 else 'style="flex-direction:row-reverse"'
        html += f"""
  <div class="detail-block" {direction}>
    <div class="img"><img src="{img}" alt="{title}" title="{title}"></div>
    <div class="txt">
      <h3>{title}</h3>
      <p>{desc}</p>
    </div>
  </div>
"""

    html += """</section>

<!-- 제품 정보 -->
<section class="section">
  <h2>제품 정보</h2>
  <table>
"""

    for key, value in specs.items():
        html += f"    <tr><th>{key}</th><td>{value}</td></tr>\n"

    html += """  </table>
</section>
"""

    # 상품 비교 섹션 - N/A 값 필터링
    comparison_chart = content_sections.get("comparison_chart", {})
    if comparison_chart.get("our_product") and comparison_chart.get("competitors"):
        valid_competitors = []
        for comp in comparison_chart.get("competitors", []):
            if all(comp.get(k) not in [None, "N/A", "n/a", "", 0] for k in ['name', 'price', 'quality', 'delivery', 'rating']):
                valid_competitors.append(comp)

        if valid_competitors:
            html += """
<!-- 제품 비교 -->
<section class="section">
  <h2>제품 비교</h2>
  <table>
    <thead>
      <tr><th>제품명</th><th>가격</th><th>품질</th><th>배송</th><th>평점</th></tr>
    </thead>
    <tbody>
"""
            our = comparison_chart["our_product"]
            html += f"""
      <tr style="background:var(--sub);border-left:3px solid var(--accent)">
        <td><strong>{our['name']}</strong></td>
        <td><strong>{our['price']}</strong></td>
        <td><strong>{our['quality']}</strong></td>
        <td><strong>{our['delivery']}</strong></td>
        <td><strong>{our['rating']} ⭐</strong></td>
      </tr>
"""
            for comp in valid_competitors:
                html += f"""
      <tr>
        <td>{comp['name']}</td>
        <td>{comp['price']}</td>
        <td>{comp['quality']}</td>
        <td>{comp['delivery']}</td>
        <td>{comp['rating']} ⭐</td>
      </tr>
"""
            html += """    </tbody>
  </table>
</section>
"""

    # FAQ 섹션
    faq = content_sections.get('faq', [])
    if faq:
        html += """
<!-- 자주 묻는 질문 -->
<section class="section">
  <h2>자주 묻는 질문 (FAQ)</h2>
"""
        for q in faq:
            html += f"""
  <div style="margin:20px 0">
    <h3 style="font-size:18px;color:var(--accent)">Q: {q['question']}</h3>
    <p style="margin-left:20px;color:#666">A: {q['answer']}</p>
  </div>
"""
        html += """</section>
"""

    # 마지막 섹션 - 주의사항 & 고객센터
    html += f"""
<!-- 구매 안내 -->
<section class="section">
  <h2>구매 전 확인사항</h2>
  {_generate_notice_section(category_type)}
  <h3 style="margin-top:20px">고객센터</h3>
  <p style="font-size:15px;color:#666">☎ 1234-5678 | 평일 10:00~17:00</p>
</section>

</div>
</body>
</html>"""

    return html


def _get_category_styles(category_type: str) -> dict:
    """카테고리별 스타일 설정"""
    styles_map = {
        'beauty': {
            'bg': '#fff',
            'sub': '#fef9f6',
            'text': '#111827',
            'line': '#f0e5de',
            'accent': '#d4a574',
            'h1_color': '#8b6f47',
            'h2_color': '#8b6f47',
            'summary_color': '#8b6f47',
            'highlight_bg': 'linear-gradient(135deg,#fef9f6 0%,#f8ede3 100%)'
        },
        'food': {
            'bg': '#fff',
            'sub': '#f8f9fa',
            'text': '#111827',
            'line': '#e5e7eb',
            'accent': '#f7c59f',
            'h1_color': '#111',
            'h2_color': '#111',
            'summary_color': '#555',
            'highlight_bg': '#fff7f0'
        },
        'fashion': {
            'bg': '#fff',
            'sub': '#f8f9fa',
            'text': '#111827',
            'line': '#e5e7eb',
            'accent': '#495057',
            'h1_color': '#000',
            'h2_color': '#000',
            'summary_color': '#555',
            'highlight_bg': '#f8f9fa'
        },
        'electronics': {
            'bg': '#fff',
            'sub': '#f0f4f8',
            'text': '#111827',
            'line': '#d1dce5',
            'accent': '#3b82f6',
            'h1_color': '#1e40af',
            'h2_color': '#1e40af',
            'summary_color': '#3b82f6',
            'highlight_bg': '#eff6ff'
        },
        'general': {
            'bg': '#fff',
            'sub': '#f8f9fa',
            'text': '#111827',
            'line': '#e5e7eb',
            'accent': '#6c757d',
            'h1_color': '#111',
            'h2_color': '#111',
            'summary_color': '#555',
            'highlight_bg': '#f8f9fa'
        }
    }

    return styles_map.get(category_type, styles_map['general'])


def _generate_category_specific_sections(content_sections: dict, category_type: str, styles: dict) -> str:
    """카테고리별 특수 섹션 생성"""
    html = ""

    # 뷰티: 핵심 성분
    if category_type == 'beauty':
        html += f"""
<!-- 핵심 성분 -->
<section class="section">
  <div class="highlight">
    <h2 style="color:{styles['h2_color']};margin-top:0">핵심 성분</h2>
    <p style="font-size:16px;color:#666">피부 타입을 고려한 안전한 성분으로 구성되었습니다.</p>
  </div>
</section>
"""

    # 식품: 영양 정보
    elif category_type == 'food':
        nutrition = content_sections.get('nutrition_info', {})
        if nutrition.get('has_nutrition'):
            html += f"""
<!-- 영양 정보 -->
<section class="section">
  <div class="highlight">
    <h2 style="color:{styles['h2_color']};margin-top:0">영양 정보</h2>
    {_markdown_to_html(nutrition.get('content', ''))}
  </div>
</section>
"""

    return html


def _get_detail_section_title(category_type: str) -> str:
    """카테고리별 디테일 섹션 제목"""
    titles = {
        'beauty': '사용 방법 & 효과',
        'fashion': '제품 디테일 포인트',
        'food': '제품 특징',
        'electronics': '기능 & 스펙',
        'general': '제품 상세'
    }
    return titles.get(category_type, '제품 상세')


def _generate_detail_points(category_type: str, selling_points: list) -> list:
    """카테고리별 디테일 포인트 동적 생성"""

    # selling_points를 활용하여 동적으로 생성 (실제로 있는 것만 사용)
    if selling_points and len(selling_points) > 0:
        points = []
        for idx, sp in enumerate(selling_points[:5]):
            title = sp.get('title', '').strip()
            desc = sp.get('description', '').strip()

            # 제목과 설명이 모두 있는 경우만 추가
            if title and desc:
                points.append((title, desc))

        # 실제로 있는 셀링 포인트만 반환 (빈 값으로 채우지 않음)
        if points:
            return points

    # selling_points가 없거나 유효한 것이 없으면 카테고리별 기본값
    category_points = {
        'beauty': [
            ("STEP 1. 준비", "깨끗하게 세안한 피부에 준비합니다"),
            ("STEP 2. 적용", "적당량을 덜어 피부에 골고루 펴 발라줍니다"),
            ("STEP 3. 흡수", "가볍게 두드려 흡수시킵니다"),
            ("STEP 4. 마무리", "다음 스킨케어 단계로 넘어갑니다"),
            ("기대 효과", "지속적인 사용으로 건강한 피부를 경험하세요")
        ],
        'fashion': [
            ("소재 & 품질", "프리미엄 소재로 착용감이 우수합니다"),
            ("디자인", "세련되고 실용적인 디자인"),
            ("활용도", "다양한 스타일링 가능"),
            ("내구성", "꼼꼼한 마감 처리"),
            ("관리", "세탁 및 보관 방법")
        ],
        'food': [
            ("맛과 식감", "신선하고 자연스러운 맛"),
            ("영양 성분", "균형 잡힌 영양 구성"),
            ("제조 공정", "위생적 제조 환경"),
            ("보관 방법", "신선도 유지 보관법"),
            ("섭취 방법", "간편하게 즐기기")
        ],
        'electronics': [
            ("핵심 기능", "최신 기술 적용"),
            ("성능", "뛰어난 성능과 속도"),
            ("호환성", "다양한 기기와 호환"),
            ("내구성", "오래 사용할 수 있는 품질"),
            ("A/S", "안심 보증 서비스")
        ],
        'general': [
            ("품질", "우수한 품질"),
            ("기능", "실용적인 기능"),
            ("디자인", "세련된 디자인"),
            ("가성비", "합리적인 가격"),
            ("만족도", "높은 고객 만족도")
        ]
    }

    return category_points.get(category_type, category_points['general'])


def _generate_notice_section(category_type: str) -> str:
    """카테고리별 주의사항 생성"""

    notices = {
        'beauty': """
  <ul style="font-size:16px;color:#666;padding-left:20px;line-height:1.8">
    <li>화장품 사용 시 또는 사용 후 직사광선에 의하여 사용부위가 붉은 반점, 부어오름 또는 가려움증 등의 이상 증상이나 부작용이 있는 경우 전문의 등과 상담하시기 바랍니다</li>
    <li>상처가 있는 부위 등에는 사용을 자제해주세요</li>
    <li>보관 및 취급 시 주의사항: 어린이의 손이 닿지 않는 곳에 보관</li>
    <li>직사광선을 피해서 보관</li>
  </ul>
""",
        'food': """
  <ul style="font-size:16px;color:#666;padding-left:20px;line-height:1.8">
    <li>개봉 후 교환/반품 제한 있음</li>
    <li>유통기한 및 보관방법 확인 필수</li>
    <li>알레르기 정보 확인 권장</li>
    <li>직사광선을 피하고 서늘한 곳에 보관</li>
  </ul>
""",
        'fashion': """
  <ul style="font-size:16px;color:#666;padding-left:20px;line-height:1.8">
    <li>개봉 후 교환/반품 제한 있음</li>
    <li>수작업 계측으로 1~3cm 오차 가능</li>
    <li>모니터 환경에 따른 색상 차이 있음</li>
    <li>세탁 시 주의사항 확인 필수</li>
  </ul>
""",
        'general': """
  <ul style="font-size:16px;color:#666;padding-left:20px;line-height:1.8">
    <li>개봉 후 교환/반품 제한 있음</li>
    <li>제품 특성상 약간의 오차 발생 가능</li>
    <li>사용 전 사용설명서 확인 필수</li>
    <li>제품 보증 기간 및 A/S 정책 확인</li>
  </ul>
"""
    }

    return notices.get(category_type, notices['general'])
