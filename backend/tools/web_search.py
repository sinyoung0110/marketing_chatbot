"""
웹 검색 도구 - Tavily API 기반 고급 검색
"""
from typing import Dict, List
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class WebSearchTool:
    """웹 검색 도구 - Tavily 기반"""

    def __init__(self):
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.use_tavily = bool(self.tavily_api_key)

        if self.use_tavily:
            try:
                from tavily import TavilyClient
                self.tavily = TavilyClient(api_key=self.tavily_api_key)
                print("[WebSearch] Tavily API 활성화")
            except ImportError:
                print("[WebSearch] Tavily 패키지 없음, DuckDuckGo 사용")
                from duckduckgo_search import DDGS
                self.ddgs = DDGS()
                self.use_tavily = False
        else:
            from duckduckgo_search import DDGS
            self.ddgs = DDGS()
            print("[WebSearch] DuckDuckGo 사용")

    def search(self, query: str, platforms: List[str], max_results: int = 10) -> Dict:
        """
        웹 검색 실행

        Args:
            query: 검색 쿼리
            platforms: 검색 대상 플랫폼 리스트
            max_results: 최대 결과 수

        Returns:
            검색 결과 딕셔너리
        """
        if self.use_tavily:
            return self._search_with_tavily(query, platforms, max_results)
        else:
            return self._search_with_duckduckgo(query, platforms, max_results)

    def _search_with_tavily(self, query: str, platforms: List[str], max_results: int) -> Dict:
        """Tavily API로 검색"""
        results = {
            "query": query,
            "platforms": platforms,
            "results": [],
            "search_engine": "tavily"
        }

        for platform in platforms:
            domain = self._get_platform_domain(platform)
            platform_query = f"{query} site:{domain}"

            try:
                # Tavily 검색 (더 정확한 결과)
                response = self.tavily.search(
                    query=platform_query,
                    max_results=max_results,
                    search_depth="advanced",
                    include_domains=[domain]
                )

                for result in response.get("results", []):
                    results["results"].append({
                        "platform": platform,
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "snippet": result.get("content", ""),
                        "score": result.get("score", 0),
                        "timestamp": datetime.now().isoformat()
                    })

            except Exception as e:
                print(f"[WebSearch] Tavily 검색 오류 ({platform}): {e}")
                results["results"].append({
                    "platform": platform,
                    "error": str(e)
                })

        return results

    def _search_with_duckduckgo(self, query: str, platforms: List[str], max_results: int) -> Dict:
        """DuckDuckGo로 검색 (fallback)"""
        results = {
            "query": query,
            "platforms": platforms,
            "results": [],
            "search_engine": "duckduckgo"
        }

        for platform in platforms:
            platform_query = f"{query} site:{self._get_platform_domain(platform)}"

            try:
                search_results = list(self.ddgs.text(
                    platform_query,
                    max_results=max_results
                ))

                for result in search_results:
                    results["results"].append({
                        "platform": platform,
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", ""),
                        "timestamp": datetime.now().isoformat()
                    })

            except Exception as e:
                print(f"[WebSearch] DuckDuckGo 검색 오류 ({platform}): {e}")
                results["results"].append({
                    "platform": platform,
                    "error": str(e)
                })

        return results

    def _get_platform_domain(self, platform: str) -> str:
        """플랫폼별 도메인 반환"""
        domains = {
            "coupang": "coupang.com",
            "naver": "smartstore.naver.com",
            "11st": "11st.co.kr"
        }
        return domains.get(platform, platform)

    def search_recent(self, query: str, days: int = 30) -> List[Dict]:
        """
        최근 N일 이내 검색 결과만 필터링

        Args:
            query: 검색 쿼리
            days: 최근 일수

        Returns:
            필터링된 검색 결과
        """
        # DuckDuckGo는 날짜 필터가 제한적이므로 결과를 후처리
        all_results = self.search(query, ["coupang", "naver"])

        # 최근 30일로 필터링 (실제로는 크롤링 날짜가 아닌 인덱싱 날짜)
        cutoff_date = datetime.now() - timedelta(days=days)

        filtered_results = []
        for result in all_results["results"]:
            # 타임스탬프가 있으면 확인
            if "timestamp" in result:
                result_date = datetime.fromisoformat(result["timestamp"])
                if result_date >= cutoff_date:
                    filtered_results.append(result)
            else:
                # 타임스탬프 없으면 일단 포함
                filtered_results.append(result)

        return filtered_results
