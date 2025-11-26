"""
API 테스트 스크립트
"""
import requests
import json

# 1. 헬스 체크
print("=" * 50)
print("1. 헬스 체크")
print("=" * 50)
response = requests.get("http://localhost:8000/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# 2. 상세페이지 생성 테스트
print("\n" + "=" * 50)
print("2. 상세페이지 생성 테스트")
print("=" * 50)

test_data = {
    "product_name": "에어프라이어 전용 바삭감자칩",
    "summary": "기름 없이도 바삭한, 건강 간식",
    "category": "푸드",
    "manufacture_country": "대한민국",
    "manufacture_date": "2025-01-01",
    "specs": {
        "중량": "120g",
        "유통기한": "9개월",
        "칼로리": "420kcal/100g"
    },
    "keywords": ["에어프라이어", "저칼로리", "간식"],
    "target_customer": "20~30대 다이어터",
    "tone": "친근한",
    "platforms": ["coupang", "naver"],
    "image_options": {
        "style": "real",
        "shots": ["main", "usage"]
    },
    "allow_web_search": True
}

print(f"Request data:")
print(json.dumps(test_data, indent=2, ensure_ascii=False))

try:
    response = requests.post(
        "http://localhost:8000/api/generate/detailpage",
        json=test_data,
        timeout=60
    )

    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\nSuccess!")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\nError:")
        print(response.text)

except Exception as e:
    print(f"\nException: {e}")
