# 📚 마케팅 AI 어시스턴트 API 문서 (Swagger)

## 🔗 Swagger UI 접속 방법

백엔드 서버 실행 후, 다음 URL로 접속하면 **인터랙티브 API 문서**를 확인할 수 있습니다:

```
http://localhost:8000/docs
```

**또는 ReDoc 스타일:**

```
http://localhost:8000/redoc
```

---

## 📋 API 엔드포인트 목록

### 1️⃣ SWOT Analysis (SWOT + 3C 분석)

#### **POST /api/swot/search** - 경쟁사 상품 검색 ✨ 개선됨

**고급 검색 옵션이 포함된 경쟁사 상품 검색**

##### Request Body

```json
{
  "query": "에어프라이어 감자칩",
  "platforms": ["coupang", "naver"],
  "max_results": 15,
  "search_depth": "advanced",
  "days": 30,
  "include_reviews": true
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `query` | string | ✅ | 검색어 |
| `platforms` | array | ✅ | 검색 플랫폼 ["coupang", "naver", "11st"] |
| `max_results` | integer | ❌ | 최대 결과 수 (기본: 10) |
| `search_depth` | string | ❌ | "basic" 또는 "advanced" (기본: "advanced") |
| `days` | integer | ❌ | 최근 N일 이내 결과만 (null이면 전체) |
| `include_reviews` | boolean | ❌ | 리뷰 포함 여부 (기본: true) |

##### Response

```json
{
  "results": [
    {
      "platform": "coupang",
      "title": "ABC 감자칩 1kg",
      "url": "https://www.coupang.com/...",
      "snippet": "바삭바삭한 감자칩...",
      "score": 0.95,
      "timestamp": "2025-11-26T10:00:00",
      "reviews": [
        {
          "text": "정말 바삭해요!",
          "platform": "coupang"
        },
        {
          "text": "칼로리가 낮아서 좋아요",
          "platform": "coupang"
        }
      ],
      "review_count": 18
    }
  ],
  "search_engine": "tavily",
  "search_options": {
    "depth": "advanced",
    "days": 30,
    "include_content": true
  },
  "search_metadata": {
    "query": "에어프라이어 감자칩",
    "platforms": ["coupang", "naver"],
    "search_depth": "advanced",
    "days": 30,
    "include_reviews": true,
    "timestamp": "2025-11-26T10:00:00",
    "total_results": 15
  }
}
```

##### 주요 개선 사항

- ✅ **검색 상세도 선택**: "advanced"는 더 상세한 정보 제공
- ✅ **검색 기간 필터**: 최근 N일 이내 결과만 검색
- ✅ **리뷰 자동 수집**: 각 상품의 리뷰(최대 20개) 자동 추출

---

#### **POST /api/swot/analyze** - SWOT + 3C 분석 실행

**경쟁사 검색 결과를 바탕으로 SWOT + 3C 분석 수행**

##### Request Body

```json
{
  "product_name": "바삭 감자칩",
  "category": "간식",
  "keywords": ["건강", "저칼로리", "바삭"],
  "target": "20-30대 헬스족",
  "search_results": null
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `product_name` | string | ✅ | 분석할 상품명 |
| `category` | string | ✅ | 상품 카테고리 |
| `keywords` | array | ❌ | 키워드 리스트 |
| `target` | string | ❌ | 타겟 고객 |
| `search_results` | array | ❌ | 검색 결과 (null이면 자동 검색) |

##### Response

```json
{
  "analysis": {
    "swot": {
      "strengths": ["100% 국산 감자", "저칼로리", "바삭한 식감"],
      "weaknesses": ["신규 브랜드", "유통망 부족"],
      "opportunities": ["건강 간식 트렌드", "온라인 판매 성장"],
      "threats": ["경쟁사 다수", "가격 경쟁"]
    },
    "three_c": {
      "company": {
        "strengths": ["품질", "가격"],
        "positioning": "프리미엄 건강 간식"
      },
      "customer": {
        "needs": ["건강", "맛", "편의성"],
        "segments": ["헬스족", "직장인"]
      },
      "competitor": {
        "main_competitors": ["A사", "B사"],
        "strategies": ["저가 공략", "대량 판매"]
      }
    },
    "price_analysis": {
      "lowest_price": 3000,
      "average_price": 5500,
      "highest_price": 8000,
      "top_5_lowest": [...]
    },
    "insights": [
      "💪 핵심 강점: 100% 국산 신선한 감자 사용",
      "🎯 시장 기회: 건강 간식 시장의 성장세",
      "💰 경쟁 가격대: 3,000원 ~ 8,000원 (평균 5,500원)"
    ]
  },
  "html_url": "/projects/swot_abc123/analysis.html",
  "project_id": "swot_abc123",
  "search_results_count": 12
}
```

##### 분석 항목

1. **SWOT 분석**
   - Strengths (강점)
   - Weaknesses (약점)
   - Opportunities (기회)
   - Threats (위협)

2. **3C 분석**
   - Company (자사)
   - Customer (고객)
   - Competitor (경쟁사)

3. **가격 분석**
   - 최저/평균/최고 가격
   - 상위 5개 최저가 상품

4. **인사이트**
   - 핵심 마케팅 포인트

---

#### **POST /api/swot/refine-search** - 검색 결과 재검색

**특정 URL을 제외하고 재검색**

##### Request Body

```json
{
  "original_query": "감자칩",
  "refined_query": "감자칩",
  "platforms": ["coupang", "naver"],
  "exclude_urls": [
    "https://www.coupang.com/product/123",
    "https://smartstore.naver.com/product/456"
  ],
  "max_results": 15
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `original_query` | string | ✅ | 원본 검색어 |
| `refined_query` | string | ✅ | 수정된 검색어 |
| `platforms` | array | ✅ | 검색 플랫폼 |
| `exclude_urls` | array | ❌ | 제외할 URL 리스트 |
| `max_results` | integer | ❌ | 최대 결과 수 |

##### Response

```json
{
  "results": [...],
  "search_metadata": {
    "original_query": "감자칩",
    "refined_query": "감자칩",
    "excluded_count": 2,
    "timestamp": "2025-11-26T10:30:00",
    "total_results": 13
  }
}
```

---

#### **POST /api/swot/generate-from-swot** - 원클릭 상세페이지 생성 🚀 NEW

**SWOT 분석 결과를 활용하여 상세페이지를 자동 생성**

##### Request Body

```json
{
  "product_name": "바삭 감자칩",
  "category": "간식",
  "swot_analysis": {
    "swot": {
      "strengths": ["100% 국산", "저칼로리"],
      "weaknesses": ["신규 브랜드"],
      "opportunities": ["건강 트렌드"],
      "threats": ["경쟁 심화"]
    },
    "three_c": {
      "customer": {
        "needs": ["건강", "맛"]
      }
    }
  },
  "search_results": [
    {
      "title": "경쟁사 상품",
      "reviews": [
        {"text": "바삭해요", "platform": "coupang"}
      ]
    }
  ],
  "platform": "coupang"
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `product_name` | string | ✅ | 상품명 |
| `category` | string | ✅ | 카테고리 |
| `swot_analysis` | object | ✅ | SWOT+3C 분석 결과 |
| `search_results` | array | ✅ | 경쟁사 검색 결과 (리뷰 포함) |
| `platform` | string | ❌ | "coupang" 또는 "naver" (기본: "coupang") |

##### Response

```json
{
  "success": true,
  "message": "SWOT 분석 결과를 활용하여 바삭 감자칩 상세페이지가 생성되었습니다",
  "result": {
    "md_url": "/projects/proj_xyz789/detail.md",
    "html_url": "/projects/proj_xyz789/detail.html",
    "images": [
      "/projects/proj_xyz789/images/main_20251126_120000.jpg",
      "/projects/proj_xyz789/images/usage_20251126_120001.jpg"
    ],
    "project_id": "proj_xyz789"
  },
  "used_swot_data": true,
  "used_review_data": true
}
```

##### 자동화 워크플로우

1. **SWOT 결과 반영**
   - 강점 → 제품 특장점
   - 기회 → 마케팅 포인트
   - 경쟁사 약점 → 우리 강점

2. **리뷰 인사이트 활용**
   - 경쟁사 리뷰 분석
   - 고객 니즈 추출
   - 긍정/부정 포인트

3. **키워드 자동 추출**
   - SWOT 강점
   - 고객 니즈

4. **콘텐츠 자동 생성**
   - AI 카피 생성
   - DALL-E 3 이미지
   - MD/HTML 파일

##### 시간 단축 효과

- **기존**: 검색(15분) + 분석(5분) + 수동 입력(5분) + 생성(5분) = **30분**
- **개선**: 검색(5분) + 분석(5분) + 원클릭(3분) = **13분** (**57% 단축!**)

---

#### **POST /api/swot/summarize** - 문서 요약

**URL 또는 텍스트 내용을 요약**

##### Request Parameters

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `url` | string | ✅ | 요약할 URL |
| `content` | string | ❌ | 텍스트 내용 (없으면 URL에서 가져옴) |

##### Response

```json
{
  "url": "https://...",
  "summary": "주요 제품 특징: ...\n가격 정보: ...\n고객 리뷰: ...",
  "timestamp": "2025-11-26T10:45:00"
}
```

---

### 2️⃣ Detail Page (상세페이지 생성)

#### **POST /api/generate/detailpage** - 상세페이지 생성

**AI 기반 상세페이지 자동 생성**

##### Request Body

```json
{
  "product_name": "프리미엄 감자칩",
  "category": "간식",
  "keywords": ["건강", "저칼로리", "바삭"],
  "target_audience": "20-30대 헬스족",
  "platform": "coupang",
  "generate_images": true
}
```

##### Response

```json
{
  "project_id": "proj_abc123",
  "md_url": "/projects/proj_abc123/detail.md",
  "html_url": "/projects/proj_abc123/detail.html",
  "analysis_url": "/projects/proj_abc123/analysis.html",
  "images": [
    "/projects/proj_abc123/images/main_20251126.jpg"
  ]
}
```

---

### 3️⃣ Marketing Chatbot (마케팅 챗봇)

#### **POST /api/chatbot/chat** - 챗봇 대화

**AI 마케팅 전략 상담**

##### Request Body

```json
{
  "message": "감자칩 마케팅 전략 알려줘",
  "history": [],
  "context": {
    "name": "바삭 감자칩",
    "category": "간식"
  }
}
```

##### Response

```json
{
  "message": "감자칩 마케팅 전략은...",
  "timestamp": "2025-11-26T11:00:00",
  "quick_actions": ["suggest_keywords", "price_strategy", "analyze_target"]
}
```

---

#### **POST /api/chatbot/quick-action** - 빠른 작업 실행

**키워드 추천, 가격 전략, 타겟 분석**

##### Request Body

```json
{
  "action": "suggest_keywords",
  "product_info": {
    "name": "바삭 감자칩",
    "category": "간식"
  }
}
```

| action | 설명 |
|--------|------|
| `suggest_keywords` | SEO 키워드 10개 추천 |
| `price_strategy` | 가격 전략 제안 |
| `analyze_target` | 타겟 고객 3가지 페르소나 분석 |

##### Response

```json
{
  "result": "추천 키워드:\n1. 건강 간식\n2. 저칼로리...",
  "timestamp": "2025-11-26T11:05:00"
}
```

---

#### **GET /api/chatbot/suggestions** - 추천 질문 가져오기

##### Response

```json
{
  "suggestions": [
    "마케팅 전략을 알려줘",
    "타겟 고객은 누구일까?",
    "가격은 어떻게 설정해야 할까?",
    "SEO 키워드를 추천해줘"
  ]
}
```

---

## 🔄 전체 워크플로우 예시

### 시나리오: "에어프라이어 감자칩" 신제품 출시

```
1. POST /api/swot/search
   {
     "query": "에어프라이어 감자칩",
     "platforms": ["coupang", "naver"],
     "max_results": 15,
     "search_depth": "advanced",
     "days": 30,
     "include_reviews": true
   }
   → 15개 경쟁 상품 + 리뷰 수집

2. (선택) POST /api/swot/refine-search
   {
     "exclude_urls": ["https://..."],
     ...
   }
   → 불필요한 URL 제외하고 재검색

3. POST /api/swot/analyze
   {
     "product_name": "바삭 감자칩",
     "category": "간식",
     "search_results": [...]
   }
   → SWOT + 3C 분석 완료
   → HTML 보고서 생성

4. POST /api/swot/generate-from-swot 🚀
   {
     "product_name": "바삭 감자칩",
     "swot_analysis": {...},
     "search_results": [...]
   }
   → 원클릭 상세페이지 생성!
   → SWOT + 리뷰 인사이트 자동 반영
```

---

## 🎯 Swagger UI 사용법

### 1. 서버 실행

```bash
cd backend
python3 main.py
```

### 2. Swagger UI 접속

브라우저에서 열기:
```
http://localhost:8000/docs
```

### 3. API 테스트

1. **엔드포인트 선택** → 클릭
2. **"Try it out"** 버튼 클릭
3. **Request Body 입력** (예시 자동 채워짐)
4. **"Execute"** 버튼 클릭
5. **Response 확인**

### 4. 주요 기능

- ✅ **인터랙티브 테스트**: 브라우저에서 바로 API 호출
- ✅ **자동 완성**: Request Body 예시 자동 제공
- ✅ **실시간 응답**: Response 즉시 확인
- ✅ **스키마 확인**: 모든 필드 타입 및 설명 제공
- ✅ **cURL 커맨드 복사**: 터미널에서 사용 가능

---

## 📚 추가 리소스

### OpenAPI JSON

```
http://localhost:8000/openapi.json
```

### ReDoc 스타일 문서

```
http://localhost:8000/redoc
```

---

## 💡 프론트엔드 개발자를 위한 팁

### 1. 검색 → 분석 → 생성 플로우

```javascript
// 1. 검색 (고급 옵션 포함)
const searchResponse = await fetch('http://localhost:8000/api/swot/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "에어프라이어 감자칩",
    platforms: ["coupang", "naver"],
    search_depth: "advanced",
    days: 30,
    include_reviews: true
  })
});
const searchData = await searchResponse.json();

// 2. SWOT 분석
const analysisResponse = await fetch('http://localhost:8000/api/swot/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    product_name: "바삭 감자칩",
    category: "간식",
    search_results: searchData.results
  })
});
const analysisData = await analysisResponse.json();

// 3. 원클릭 생성 🚀
const generateResponse = await fetch('http://localhost:8000/api/swot/generate-from-swot', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    product_name: "바삭 감자칩",
    category: "간식",
    swot_analysis: analysisData.analysis,
    search_results: searchData.results,
    platform: "coupang"
  })
});
const result = await generateResponse.json();

// 결과 사용
console.log('생성된 파일:', result.result.md_url);
console.log('SWOT 데이터 사용:', result.used_swot_data);
console.log('리뷰 데이터 사용:', result.used_review_data);
```

### 2. UI 컴포넌트 제안

```jsx
// 고급 검색 옵션 UI
<Accordion>
  <AccordionSummary>고급 검색 옵션</AccordionSummary>
  <AccordionDetails>
    <Select label="검색 상세도" value={searchDepth}>
      <option value="basic">기본</option>
      <option value="advanced">상세 (권장)</option>
    </Select>

    <Select label="검색 기간" value={days}>
      <option value="">전체</option>
      <option value="7">최근 7일</option>
      <option value="30">최근 30일</option>
      <option value="90">최근 90일</option>
    </Select>

    <Checkbox checked={includeReviews} label="리뷰 포함" />
  </AccordionDetails>
</Accordion>

// 원클릭 생성 버튼
<Button
  variant="contained"
  color="secondary"
  startIcon={<AutoAwesome />}
  onClick={handleGenerateFromSwot}
>
  🚀 원클릭 상세페이지 생성
</Button>
```

---

## 🎉 요약

이제 프론트엔드 개발자는 다음을 활용할 수 있습니다:

1. ✅ **Swagger UI** (http://localhost:8000/docs)
   - 인터랙티브 API 테스트
   - 자동 완성 및 예시 제공
   - 실시간 응답 확인

2. ✅ **상세한 API 문서**
   - 모든 엔드포인트 설명
   - Request/Response 예시
   - 필드별 타입 및 설명

3. ✅ **개선된 SWOT 기능**
   - 고급 검색 옵션 (기간, 상세도, 리뷰)
   - 원클릭 상세페이지 생성
   - 리뷰 기반 인사이트

4. ✅ **프론트엔드 코드 예시**
   - JavaScript fetch 예시
   - UI 컴포넌트 제안

**모든 준비 완료! 🚀**
