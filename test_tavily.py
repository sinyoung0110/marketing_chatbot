"""Tavily 검색 테스트"""
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

# Tavily API 키 확인
tavily_key = os.getenv("TAVILY_API_KEY")
print(f"Tavily API Key: {tavily_key[:20]}..." if tavily_key else "No key found")

# Tavily 검색 테스트
try:
    from tavily import TavilyClient

    client = TavilyClient(api_key=tavily_key)
    print("\n✅ Tavily 클라이언트 생성 성공")

    # 간단한 검색 테스트
    print("\n🔍 검색 테스트: '에어프라이어 감자칩 site:coupang.com'")

    result = client.search(
        query="에어프라이어 감자칩 site:coupang.com",
        max_results=3
    )

    print(f"\n✅ 검색 성공! 결과 개수: {len(result.get('results', []))}")

    for i, item in enumerate(result.get('results', [])[:3], 1):
        print(f"\n{i}. {item.get('title', 'No title')}")
        print(f"   URL: {item.get('url', '')}")
        print(f"   내용: {item.get('content', '')[:100]}...")

except ImportError as e:
    print(f"\n❌ Tavily 패키지 없음: {e}")
    print("설치: pip install tavily-python")

except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
