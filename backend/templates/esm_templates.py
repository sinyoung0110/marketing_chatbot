"""
ESM+ / 스마트스토어 / 쿠팡 호환 상세페이지 템플릿 생성기
"""

def generate_esm_html(content_sections: dict, images: list, product_input: dict) -> str:
    """
    ESM+ 가이드라인 준수 HTML 템플릿 생성
    카테고리별로 적합한 템플릿 자동 선택
    """
    category = product_input.get('category', '').lower()

    # 카테고리별 템플릿 분기
    if any(kw in category for kw in ['의류', '패션', '옷', '셔츠', '바지', '원피스', '가방', '신발']):
        return _clothing_template(content_sections, images, product_input)
    elif any(kw in category for kw in ['식품', '음식', '간식', '과자', '음료']):
        return _food_template(content_sections, images, product_input)
    else:
        return _general_template(content_sections, images, product_input)


def _clothing_template(content_sections: dict, images: list, product_input: dict) -> str:
    """의류 전용 ESM+ 템플릿"""
    product_name = product_input.get('product_name', 'PRODUCT_TITLE')
    selling_points = content_sections.get('selling_points', [])[:3]
    specs = content_sections.get('specs', {})
    summary = content_sections.get('summary', '한 줄 USP 문구')
    detailed_desc = content_sections.get('detailed_description', {}).get('content', '제품 상세 소개')

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

<!-- 6. 구매 안내 -->
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
    detailed_desc = content_sections.get('detailed_description', {}).get('content', '제품 상세 소개')
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

<!-- 7. 구매 안내 -->
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
    detailed_desc = content_sections.get('detailed_description', {}).get('content', '상세 소개')

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
</div>
</body>
</html>"""

    return html
