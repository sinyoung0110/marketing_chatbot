# 🎯 마케팅 AI 어시스턴트 API 문서

## 📋 목차
- [개요](#개요)
- [인증](#인증)
- [Base URL](#base-url)
- [통합 워크플로우 API](#1-통합-워크플로우-api)
- [SWOT 분석 API](#2-swot-분석-api)
- [챗봇 API](#3-챗봇-api)
- [상세페이지 생성 API](#4-상세페이지-생성-api)
- [에러 코드](#에러-코드)

---

## 개요

마케팅 AI 어시스턴트 API는 상품 마케팅을 위한 SWOT 분석, 상세페이지 생성, AI 챗봇 기능을 제공합니다.

### 기술 스택
- FastAPI + Python 3.x
- OpenAI GPT-4o-mini + DALL-E 3
- LangChain + LangGraph
- Tavily API (웹 검색)

### Swagger UI
- **개발 환경**: `http://localhost:8000/docs`
- **프로덕션**: `https://your-domain.com/docs`

---

## 인증

현재 버전은 인증이 필요하지 않습니다. (v1.0)

> ⚠️ 프로덕션 배포 시 API Key 또는 JWT 인증 추가 권장

---

## Base URL

| 환경 | URL |
|------|-----|
| 로컬 개발 | `http://localhost:8000` |
| 프로덕션 | `https://your-backend.onrender.com` |

---

## 1. 통합 워크플로우 API

세션 기반으로 SWOT 분석 → 상세페이지 생성을 한 번에 처리하는 워크플로우

### 1.1 세션 생성

**Endpoint:** `POST /api/unified/start`

**설명:** 상품 정보를 입력하고 세션을 생성합니다.

**Request Body:**
```json
{
  "product_name": "바삭 감자칩",
  "category": "간식",
  "keywords": ["건강", "저칼로리", "바삭"],
  "target_customer": "20-30대 헬스족",
  "platforms": ["coupang", "naver"]
}
```

**Response:** `200 OK`
```json
{
  "session_id": "sess_a1b2c3d4",
  "message": "✅ 세션이 생성되었습니다! (sess_a1b2c3d4)",
  "next_step": "swot",
  "product_info": {
    "product_name": "바삭 감자칩",
    "category": "간식",
    "keywords": ["건강", "저칼로리", "바삭"],
    "target_customer": "20-30대 헬스족",
    "platforms": ["coupang", "naver"]
  }
}
```

**필드 설명:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| product_name | string | ✅ | 상품명 |
| category | string | ✅ | 카테고리 (예: 간식, 전자제품) |
| keywords | array[string] | ❌ | 키워드 리스트 (기본: []) |
| target_customer | string | ❌ | 타겟 고객 (기본: "") |
| platforms | array[string] | ❌ | 플랫폼 (기본: ["coupang", "naver"]) |

---

### 1.2 PDF 파싱

**Endpoint:** `POST /api/unified/parse-pdf`

**설명:** PDF 파일에서 상품 정보를 자동 추출합니다.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (PDF 파일, 최대 50MB)

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "PDF 파싱 완료",
  "product_name": "프리미엄 에어프라이어 감자칩",
  "category": "간식",
  "keywords": ["건강", "저칼로리", "국산"],
  "target_customer": "건강을 중시하는 20-30대",
  "platforms": ["coupang", "naver"]
}
```

**에러:**
- `400`: PDF 파일이 아니거나 텍스트 추출 실패
- `413`: 파일 크기 초과 (50MB)

---

### 1.3 SWOT 분석 실행

**Endpoint:** `POST /api/unified/execute-swot`

**설명:** 세션의 상품 정보로 경쟁사 검색 + SWOT+3C 분석을 실행합니다.

**Request Body:**
```json
{
  "session_id": "sess_a1b2c3d4",
  "search_depth": "advanced",
  "days": 90,
  "include_reviews": true,
  "search_platforms": ["coupang", "naver", "news", "blog"],
  "sort_by": "popular"
}
```

**필드 설명:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| session_id | string | ✅ | - | 세션 ID |
| search_depth | string | ❌ | "advanced" | 검색 상세도 (basic/advanced) |
| days | integer | ❌ | 90 | 최근 N일 이내 검색 (null=전체) |
| include_reviews | boolean | ❌ | true | 리뷰 포함 여부 |
| search_platforms | array[string] | ❌ | ["coupang",...] | 검색 플랫폼 |
| sort_by | string | ❌ | "popular" | 정렬 기준 |

**Response:** `200 OK`
```json
{
  "session_id": "sess_a1b2c3d4",
  "analysis_result": {
    "swot": {
      "strengths": ["100% 국산 감자", "저칼로리 (120kcal)"],
      "weaknesses": ["신규 브랜드 인지도 부족"],
      "opportunities": ["건강 간식 트렌드 증가"],
      "threats": ["대형 브랜드 경쟁 심화"]
    },
    "three_c": {
      "company": {
        "positioning": "프리미엄 건강 간식",
        "strengths": ["국산 원료", "저칼로리"]
      },
      "customer": {
        "needs": ["건강", "맛", "가격"],
        "segments": ["20-30대", "헬스족"]
      },
      "competitor": {
        "leaders": ["오리온", "농심"],
        "gaps": ["건강 이미지 부족"]
      }
    },
    "price_analysis": {
      "average": 4500,
      "min": 3500,
      "max": 6500
    }
  },
  "html_url": "/outputs/sess_a1b2c3d4/analysis.html",
  "competitor_count": 15,
  "next_step": "detail"
}
```

---

### 1.4 상세페이지 생성

**Endpoint:** `POST /api/unified/execute-detail`

**설명:** SWOT 결과를 반영하여 상세페이지를 생성합니다.

**Request Body:**
```json
{
  "session_id": "sess_a1b2c3d4",
  "platform": "coupang",
  "tone": "친근한",
  "image_style": "real"
}
```

**필드 설명:**
| 필드 | 타입 | 필수 | 기본값 | 옵션 |
|------|------|------|--------|------|
| session_id | string | ✅ | - | - |
| platform | string | ❌ | "coupang" | coupang, naver |
| tone | string | ❌ | "친근한" | 친근한, 전문적인, 감성적인 |
| image_style | string | ❌ | "real" | real, illustration, minimal |

**Response:** `200 OK`
```json
{
  "session_id": "sess_a1b2c3d4",
  "markdown_url": "/outputs/sess_a1b2c3d4/detail.md",
  "html_url": "/outputs/sess_a1b2c3d4/detail.html",
  "images": [
    "https://dalle-generated-image-1.png",
    "https://dalle-generated-image-2.png"
  ],
  "next_step": "chat"
}
```

---

### 1.5 세션 조회

**Endpoint:** `GET /api/unified/session/{session_id}`

**설명:** 세션의 현재 진행 상태를 조회합니다.

**Path Parameters:**
- `session_id`: 세션 ID (string)

**Response:** `200 OK`
```json
{
  "session_id": "sess_a1b2c3d4",
  "created_at": "2024-12-05T10:30:00",
  "updated_at": "2024-12-05T10:35:00",
  "current_step": "detail",
  "completed_steps": ["start", "swot"],
  "product_info": {
    "product_name": "바삭 감자칩",
    "category": "간식"
  },
  "has_swot": true,
  "has_detail": true,
  "swot_result": {
    "html_url": "/outputs/sess_a1b2c3d4/analysis.html"
  },
  "detail_result": {
    "html_url": "/outputs/sess_a1b2c3d4/detail.html",
    "markdown_url": "/outputs/sess_a1b2c3d4/detail.md"
  },
  "chat_count": 0
}
```

**에러:**
- `404`: 세션을 찾을 수 없음

---

### 1.6 콘텐츠 섹션 수정

**Endpoint:** `POST /api/unified/update-content-sections`

**설명:** SWOT 또는 상세페이지의 특정 섹션을 수정하고 HTML을 재생성합니다.

**Request Body:**
```json
{
  "session_id": "sess_a1b2c3d4",
  "step": "swot",
  "updated_sections": {
    "swot": {
      "strengths": ["100% 국산 감자", "저칼로리 120kcal", "무첨가 제조"]
    }
  }
}
```

**또는 (상세페이지 수정):**
```json
{
  "session_id": "sess_a1b2c3d4",
  "step": "detail",
  "updated_sections": {
    "headline": "건강한 간식의 새로운 기준",
    "summary": "100% 국산 감자로 만든 프리미엄 감자칩"
  }
}
```

**필드 설명:**
| 필드 | 타입 | 필수 | 옵션 |
|------|------|------|------|
| session_id | string | ✅ | - |
| step | string | ✅ | swot, detail |
| updated_sections | object | ✅ | 수정할 필드 |

**Response:** `200 OK`
```json
{
  "session_id": "sess_a1b2c3d4",
  "html_url": "/outputs/sess_a1b2c3d4/analysis.html",
  "message": "SWOT 분석이 업데이트되었습니다"
}
```

---

### 1.7 세션 목록 조회

**Endpoint:** `GET /api/unified/sessions`

**설명:** 모든 세션 목록을 조회합니다.

**Response:** `200 OK`
```json
{
  "total": 3,
  "sessions": [
    {
      "session_id": "sess_a1b2c3d4",
      "created_at": "2024-12-05T10:30:00",
      "product_name": "바삭 감자칩"
    },
    {
      "session_id": "sess_e5f6g7h8",
      "created_at": "2024-12-05T09:00:00",
      "product_name": "프리미엄 초콜릿"
    }
  ]
}
```

---

### 1.8 세션 삭제

**Endpoint:** `DELETE /api/unified/session/{session_id}`

**설명:** 세션을 삭제합니다.

**Response:** `200 OK`
```json
{
  "message": "세션 sess_a1b2c3d4가 삭제되었습니다"
}
```

---

## 2. SWOT 분석 API

독립적으로 SWOT 분석을 실행할 수 있는 API (세션 없이 사용 가능)

### 2.1 경쟁사 검색

**Endpoint:** `POST /api/swot/search`

**설명:** 경쟁사 상품을 웹에서 검색합니다.

**Request Body:**
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

**필드 설명:**
| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| query | string | ✅ | - | 검색어 |
| platforms | array[string] | ❌ | ["coupang", "naver"] | 플랫폼 |
| max_results | integer | ❌ | 10 | 최대 결과 수 |
| search_depth | string | ❌ | "advanced" | basic/advanced |
| days | integer | ❌ | null | 최근 N일 이내 |
| include_reviews | boolean | ❌ | true | 리뷰 포함 여부 |

**Response:** `200 OK`
```json
{
  "results": [
    {
      "title": "오리온 포카칩 오리지널 66g",
      "url": "https://www.coupang.com/vp/products/...",
      "content": "바삭한 감자칩, 국내산 감자 100%",
      "platform": "coupang",
      "price": 3500,
      "reviews": [
        "맛있어요!",
        "바삭바삭하고 좋습니다"
      ],
      "review_count": 2
    }
  ],
  "search_metadata": {
    "query": "에어프라이어 감자칩",
    "platforms": ["coupang", "naver"],
    "search_depth": "advanced",
    "days": 30,
    "include_reviews": true,
    "timestamp": "2024-12-05T10:30:00",
    "total_results": 15
  }
}
```

---

### 2.2 SWOT+3C 분석

**Endpoint:** `POST /api/swot/analyze`

**설명:** 검색 결과를 바탕으로 SWOT+3C 분석을 수행합니다.

**Request Body:**
```json
{
  "product_name": "바삭 감자칩",
  "category": "간식",
  "keywords": ["건강", "저칼로리"],
  "target": "20-30대 헬스족",
  "search_results": null
}
```

**필드 설명:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| product_name | string | ✅ | 상품명 |
| category | string | ✅ | 카테고리 |
| keywords | array[string] | ❌ | 키워드 |
| target | string | ❌ | 타겟 고객 |
| search_results | array | ❌ | 검색 결과 (null이면 자동 검색) |

**Response:** `200 OK`
```json
{
  "analysis": {
    "swot": {
      "strengths": [...],
      "weaknesses": [...],
      "opportunities": [...],
      "threats": [...]
    },
    "three_c": {
      "company": {...},
      "customer": {...},
      "competitor": {...}
    },
    "price_analysis": {
      "average": 4500,
      "min": 3500,
      "max": 6500
    }
  },
  "html_url": "/outputs/swot_xyz123/analysis.html",
  "project_id": "swot_xyz123",
  "search_results_count": 15
}
```

---

### 2.3 재검색

**Endpoint:** `POST /api/swot/refine-search`

**설명:** 특정 URL을 제외하고 재검색합니다.

**Request Body:**
```json
{
  "original_query": "감자칩",
  "refined_query": "프리미엄 감자칩",
  "platforms": ["coupang", "naver"],
  "exclude_urls": [
    "https://www.coupang.com/product/123",
    "https://smartstore.naver.com/product/456"
  ],
  "max_results": 15
}
```

**Response:** `200 OK`
```json
{
  "results": [...],
  "search_metadata": {
    "original_query": "감자칩",
    "refined_query": "프리미엄 감자칩",
    "excluded_count": 2,
    "timestamp": "2024-12-05T10:30:00",
    "total_results": 13
  }
}
```

---

### 2.4 SWOT로 상세페이지 생성

**Endpoint:** `POST /api/swot/generate-from-swot`

**설명:** SWOT 분석 결과를 활용하여 상세페이지를 생성합니다.

**Request Body:**
```json
{
  "product_name": "바삭 감자칩",
  "category": "간식",
  "swot_analysis": {
    "swot": {...},
    "three_c": {...}
  },
  "search_results": [...],
  "platform": "coupang"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "SWOT 분석 결과를 활용하여 바삭 감자칩 상세페이지 생성 준비 완료",
  "data": {
    "product_name": "바삭 감자칩",
    "category": "간식",
    "keywords": ["100% 국산", "저칼로리", "건강"],
    "swot_insights": {...},
    "review_insights": {...}
  },
  "used_swot_data": true,
  "used_review_data": true,
  "redirect_to": "/"
}
```

---

## 3. 챗봇 API

마케팅 전략 상담을 위한 AI 챗봇

### 3.1 채팅

**Endpoint:** `POST /api/chatbot/chat`

**설명:** AI 챗봇과 대화합니다.

**Request Body:**
```json
{
  "message": "감자칩 마케팅 전략을 알려줘",
  "conversation_history": [
    {
      "role": "user",
      "content": "안녕?"
    },
    {
      "role": "assistant",
      "content": "안녕하세요! 무엇을 도와드릴까요?"
    }
  ],
  "session_context": {
    "product_info": {
      "product_name": "바삭 감자칩",
      "category": "간식",
      "keywords": ["건강", "저칼로리"]
    }
  },
  "session_id": "sess_a1b2c3d4"
}
```

**필드 설명:**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| message | string | ✅ | 사용자 메시지 |
| conversation_history | array | ❌ | 대화 히스토리 (최근 10개) |
| session_context | object | ❌ | 세션 컨텍스트 (상품 정보 등) |
| session_id | string | ❌ | 세션 ID |

**Response:** `200 OK`
```json
{
  "response": "감자칩 마케팅은 다음 전략을 추천합니다:\n1. 건강 이미지 강조\n2. SNS 인플루언서 협업\n3. 샘플링 이벤트",
  "timestamp": "2024-12-05T10:30:00"
}
```

**상세페이지 수정 요청 시:**
```json
{
  "response": "✅ 상세페이지가 수정되었습니다!\n\n수정된 내용:\n{\"headline\": \"새로운 제목\"}",
  "timestamp": "2024-12-05T10:30:00",
  "html_url": "/outputs/sess_a1b2c3d4/detail.html",
  "action_type": "detail_page_updated"
}
```

---

### 3.2 빠른 작업

**Endpoint:** `POST /api/chatbot/quick-action`

**설명:** 키워드 추천, 타겟 분석 등 빠른 작업을 실행합니다.

**Request Body:**
```json
{
  "action": "suggest_keywords",
  "product_info": {
    "name": "바삭 감자칩",
    "category": "간식"
  }
}
```

**액션 타입:**
- `suggest_keywords`: SEO 키워드 추천
- `analyze_target`: 타겟 고객 분석
- `price_strategy`: 가격 전략

**Response:** `200 OK`
```json
{
  "action": "suggest_keywords",
  "result": "{\"keywords\": [\"건강 간식\", \"저칼로리 감자칩\", \"에어프라이어 과자\", ...]}",
  "timestamp": "2024-12-05T10:30:00"
}
```

---

### 3.3 마케팅 제안

**Endpoint:** `GET /api/chatbot/suggestions`

**설명:** 상품 기반 마케팅 제안을 받습니다.

**Query Parameters:**
- `product_name` (string, required): 상품명
- `category` (string, required): 카테고리

**예시:** `GET /api/chatbot/suggestions?product_name=바삭 감자칩&category=간식`

**Response:** `200 OK`
```json
{
  "suggestions": "## 핵심 셀링 포인트\n1. 100% 국산 감자\n2. 저칼로리 건강 간식\n3. 바삭한 식감\n\n## 주요 타겟 고객\n20-30대 건강 관심층\n\n## 추천 플랫폼\n쿠팡, 네이버 스마트스토어\n\n## 가격대 제안\n4,000-5,000원",
  "product_name": "바삭 감자칩",
  "category": "간식",
  "timestamp": "2024-12-05T10:30:00"
}
```

---

## 4. 상세페이지 생성 API

독립적으로 상세페이지를 생성하는 API (레거시, 통합 워크플로우 사용 권장)

### 4.1 상세페이지 생성

**Endpoint:** `POST /api/generate/detailpage`

**설명:** 상품 정보로 상세페이지를 생성합니다.

**Request Body:**
```json
{
  "product_name": "바삭 감자칩",
  "category": "간식",
  "keywords": ["건강", "저칼로리", "바삭"],
  "target": "20-30대 헬스족",
  "platforms": ["coupang"],
  "tone": "친근한",
  "image_options": {
    "style": "real",
    "shots": ["main", "detail1", "detail2"]
  }
}
```

**Response:** `200 OK`
```json
{
  "project_id": "proj_xyz123",
  "markdown_url": "/projects/proj_xyz123/detail.md",
  "html_url": "/projects/proj_xyz123/detail.html",
  "images": [
    "https://dalle-image-1.png",
    "https://dalle-image-2.png"
  ],
  "meta": {
    "generated_at": "2024-12-05T10:30:00",
    "platform": "coupang",
    "status": "completed"
  }
}
```

---

### 4.2 프로젝트 상태 조회

**Endpoint:** `GET /api/project/{project_id}/status`

**Response:** `200 OK`
```json
{
  "project_id": "proj_xyz123",
  "status": "completed"
}
```

**상태 값:**
- `processing`: 생성 중
- `completed`: 완료
- `failed`: 실패

---

### 4.3 프로젝트 목록

**Endpoint:** `GET /api/projects`

**Response:** `200 OK`
```json
{
  "projects": [
    {
      "project_id": "proj_xyz123",
      "status": "completed"
    },
    {
      "project_id": "proj_abc456",
      "status": "processing"
    }
  ]
}
```

---

## 5. 정적 파일 API

생성된 파일에 접근하는 엔드포인트

### 5.1 프로젝트 파일

**Endpoint:** `GET /projects/{project_id}/{filename}`

**예시:**
- `GET /projects/proj_xyz123/detail.html`
- `GET /projects/proj_xyz123/detail.md`

---

### 5.2 출력 파일 (SWOT)

**Endpoint:** `GET /outputs/{session_id}/{filename}`

**예시:**
- `GET /outputs/sess_a1b2c3d4/analysis.html`
- `GET /outputs/sess_a1b2c3d4/detail.html`

---

## 에러 코드

| 상태 코드 | 설명 |
|-----------|------|
| 200 | 성공 |
| 400 | 잘못된 요청 (필수 필드 누락, 유효하지 않은 값) |
| 404 | 리소스를 찾을 수 없음 (세션, 프로젝트) |
| 413 | 파일 크기 초과 (PDF 업로드 시) |
| 500 | 서버 내부 오류 (AI API 오류, DB 오류 등) |

### 에러 응답 형식

```json
{
  "detail": "세션을 찾을 수 없습니다"
}
```

---

## 6. 헬스 체크

### 6.1 루트

**Endpoint:** `GET /`

**Response:** `200 OK`
```json
{
  "message": "E-commerce Detail Page Generator API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### 6.2 헬스 체크

**Endpoint:** `GET /health`

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2024-12-05T10:30:00"
}
```

---

## 7. 사용 시나리오

### 시나리오 1: 완전 자동 워크플로우

```
1. POST /api/unified/start
   → session_id 받기

2. POST /api/unified/execute-swot
   → SWOT 분석 완료

3. POST /api/unified/execute-detail
   → 상세페이지 생성 완료

4. POST /api/chatbot/chat (session_id 포함)
   → AI 상담
```

### 시나리오 2: PDF 업로드

```
1. POST /api/unified/parse-pdf
   → 상품 정보 자동 추출

2. POST /api/unified/start (추출된 정보 사용)
   → 세션 생성

3. 이후 시나리오 1과 동일
```

### 시나리오 3: 독립 SWOT 분석

```
1. POST /api/swot/search
   → 경쟁사 검색

2. POST /api/swot/analyze (검색 결과 포함)
   → SWOT 분석

3. POST /api/swot/generate-from-swot
   → 상세페이지 생성
```

---

## 8. 개발 가이드

### CORS 설정

현재 모든 origin 허용 (`allow_origins=["*"]`)

프로덕션 배포 시 수정 필요:
```python
allow_origins=["https://your-frontend.vercel.app"]
```

### 환경변수

백엔드 배포 시 필요한 환경변수:

```bash
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

### 프론트엔드 환경변수

```bash
REACT_APP_BACKEND_URL=https://your-backend.onrender.com
```

### 로컬 개발

```bash
# 백엔드
cd backend
uvicorn main:app --reload --port 8000

# 프론트엔드
cd frontend
npm start
```

---

## 9. 변경 이력

| 버전 | 날짜 | 변경사항 |
|------|------|----------|
| 1.0.0 | 2024-12-05 | 초기 릴리스 |

---

## 10. 지원

- **Swagger UI**: `/docs`
- **GitHub**: https://github.com/sinyoung0110/marketing_chatbot
- **라이선스**: MIT

---

**문서 작성일**: 2024-12-05
**API 버전**: v1.0.0
**작성자**: Claude Code
