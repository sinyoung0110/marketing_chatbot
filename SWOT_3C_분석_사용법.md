# 📊 SWOT + 3C 분석 기능 사용 가이드

## 🎯 개요

이 시스템은 **인터넷 실시간 검색**을 통해 경쟁 상품을 분석하고, **SWOT + 3C 분석**을 자동으로 수행하여 마케팅 전략을 제공합니다.

## ✨ 주요 기능

### 1. **실시간 인터넷 검색** (Tavily API)
- ✅ Tavily API를 사용한 고급 웹 검색
- ✅ 쿠팡, 네이버 스토어 등 플랫폼별 검색
- ✅ 최신 경쟁 상품 정보 자동 수집

### 2. **SWOT 분석**
- **Strengths (강점)**: 자사 상품의 경쟁 우위 요소
- **Weaknesses (약점)**: 개선이 필요한 부분
- **Opportunities (기회)**: 시장에서 활용 가능한 기회
- **Threats (위협)**: 경쟁사나 시장 환경의 위협

### 3. **3C 분석**
- **Company (자사)**: 자사의 강점, 자원, 역량
- **Customer (고객)**: 타겟 고객의 니즈, 페인 포인트
- **Competitor (경쟁사)**: 주요 경쟁사의 전략, 강점, 약점

### 4. **가격 분석**
- 💰 최저가 상품 자동 탐색
- 💰 평균 가격대 분석
- 💰 가격 경쟁력 비교
- 💰 플랫폼별 가격 정보

### 5. **시각화 리포트**
- 📈 아름다운 HTML 보고서 자동 생성
- 📊 핵심 인사이트 요약
- 🎨 그라데이션 디자인으로 전문적인 프레젠테이션

---

## 🚀 사용 방법

### 1단계: 환경 설정

`.env` 파일에 API 키 설정:

```env
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

### 2단계: 필수 패키지 설치

```bash
pip install tavily-python
```

### 3단계: API 호출

```bash
curl -X POST http://localhost:8000/api/generate \\
  -H "Content-Type: application/json" \\
  -d '{
    "product_name": "에어프라이어 전용 바삭감자칩",
    "category": "간식",
    "keywords": ["에어프라이어", "저칼로리", "간편"],
    "target": "건강 간식을 찾는 30-40대",
    "platforms": ["coupang", "naver"],
    "allow_web_search": true
  }'
```

### 4단계: 결과 확인

API 응답에서 `analysis_url`을 확인하여 HTML 보고서를 엽니다:

```json
{
  "markdown_url": "/projects/proj_xxx/detail.md",
  "html_url": "/projects/proj_xxx/detail.html",
  "analysis_url": "/projects/proj_xxx/analysis.html",  // ← 이 파일 열기!
  "images": [...]
}
```

---

## 📁 생성되는 파일

각 프로젝트마다 다음 파일들이 생성됩니다:

```
backend/projects/proj_xxx/
├── detail.md              # 상품 상세페이지 (마크다운)
├── detail.html            # 상품 상세페이지 (HTML)
├── analysis.html          # ⭐ SWOT + 3C 분석 보고서
└── images/                # 생성된 이미지들
```

---

## 🎨 분석 보고서 예시

`analysis.html` 파일을 브라우저로 열면 다음과 같은 섹션들을 볼 수 있습니다:

### 📌 핵심 인사이트
```
💪 핵심 강점: 100% 국산 신선한 감자 사용
🎯 시장 기회: 건강 간식 시장의 성장세
💰 경쟁 가격대: 3,000원 ~ 8,000원 (평균 5,500원)
🏷️ 최저가: ABC 감자칩 - 3,000원
```

### 📈 SWOT 분석
- **강점 카드**: 자사 상품의 경쟁력
- **약점 카드**: 개선이 필요한 영역
- **기회 카드**: 시장 공략 포인트
- **위협 카드**: 대응 전략이 필요한 요소

### 🔍 3C 분석
- **자사**: 우리 제품의 핵심 역량
- **고객**: 타겟 고객의 니즈와 페인 포인트
- **경쟁사**: 경쟁 상품의 전략 및 약점

### 💰 가격 분석
- 최저가/평균가/최고가 카드
- 상위 5개 최저가 상품 테이블
- 플랫폼별 가격 링크

---

## 🔧 커스터마이징

### 검색 플랫폼 추가

`backend/tools/web_search.py`에서 도메인 추가:

```python
def _get_platform_domain(self, platform: str) -> str:
    domains = {
        "coupang": "coupang.com",
        "naver": "smartstore.naver.com",
        "11st": "11st.co.kr",
        "gmarket": "gmarket.co.kr",  # 추가
    }
    return domains.get(platform, platform)
```

### 분석 항목 조정

`backend/tools/swot_3c_analysis.py`에서 프롬프트 수정:

```python
system_prompt = """당신은 마케팅 전략 전문가입니다.
제공된 자사 상품과 경쟁사 정보를 바탕으로 SWOT 분석을 수행하세요.

각 항목당 5-7개씩 구체적으로 작성하세요."""  # 개수 조정 가능
```

---

## 🎯 활용 예시

### 1. 신상품 출시 전 시장 조사
```json
{
  "product_name": "프리미엄 유기농 그래놀라",
  "category": "시리얼",
  "platforms": ["coupang", "naver", "11st"]
}
```

### 2. 기존 상품 가격 전략 수립
```json
{
  "product_name": "무선 블루투스 이어폰",
  "category": "전자기기",
  "platforms": ["coupang"]
}
```

### 3. 경쟁사 분석 리포트 생성
- API 호출 → `analysis.html` 다운로드 → 팀 공유

---

## ❓ 문제 해결

### Tavily API 오류
```
[WebSearch] Tavily 패키지 없음, DuckDuckGo 사용
```

**해결**: `pip install tavily-python`

### 가격 정보 없음
```
가격 정보를 찾을 수 없습니다.
```

**원인**: 검색 결과에 가격 정보가 없거나 형식이 다름
**해결**: 더 구체적인 검색어 사용 (예: "감자칩 가격")

### 분석 결과가 부실함
```
데이터 없음
```

**원인**: 경쟁사 검색 결과가 부족함
**해결**:
1. `max_results` 값 증가 (기본 10 → 20)
2. 검색어 조정
3. 플랫폼 추가

---

## 📊 분석 품질 향상 팁

### ✅ 검색어 최적화
- ❌ 나쁜 예: "상품"
- ✅ 좋은 예: "에어프라이어 전용 감자칩"

### ✅ 플랫폼 다양화
```json
{
  "platforms": ["coupang", "naver", "11st", "gmarket"]
}
```

### ✅ 키워드 구체화
```json
{
  "keywords": [
    "무첨가",
    "저칼로리",
    "에어프라이어 전용",
    "100% 국산"
  ]
}
```

---

## 🎉 완성!

이제 당신의 마케팅 챗봇은:

1. ✅ **실시간 인터넷 검색** (Tavily)
2. ✅ **SWOT 분석** 자동 생성
3. ✅ **3C 분석** 자동 생성
4. ✅ **가격 비교** 및 최저가 탐색
5. ✅ **아름다운 HTML 보고서** 생성

을 모두 수행할 수 있습니다! 🚀

---

## 📞 지원

문제가 있거나 궁금한 점이 있으면:
1. `backend/agents/workflow.py` - 워크플로우 로직
2. `backend/tools/swot_3c_analysis.py` - SWOT/3C 분석
3. `backend/tools/web_search.py` - 웹 검색
4. `backend/tools/analysis_visualizer.py` - HTML 생성

파일들을 참고하세요!
