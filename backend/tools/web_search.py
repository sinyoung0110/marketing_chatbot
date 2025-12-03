"""
웹 검색 도구 - Tavily API 기반 고급 검색
"""
from typing import Dict, List
from datetime import datetime, timedelta
import os
import re
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

    def search(
        self,
        query: str,
        platforms: List[str],
        max_results: int = 10,
        search_depth: str = "advanced",
        days: int = None,
        include_raw_content: bool = False,
        search_platforms: List[str] = None,
        sort_by: str = "popular"
    ) -> Dict:
        """
        웹 검색 실행

        Args:
            query: 검색 쿼리
            platforms: 검색 대상 플랫폼 리스트 (판매 플랫폼)
            max_results: 최대 결과 수
            search_depth: 검색 상세도 ("basic" or "advanced")
            days: 최근 N일 이내 결과만 (Tavily 전용)
            include_raw_content: 원본 HTML 콘텐츠 포함 여부
            search_platforms: 검색 소스 (coupang, naver, news, blog)
            sort_by: 정렬 기준 (popular, recent, review)

        Returns:
            검색 결과 딕셔너리
        """
        if self.use_tavily:
            return self._search_with_tavily(
                query, platforms, max_results, search_depth, days,
                include_raw_content, search_platforms, sort_by
            )
        else:
            return self._search_with_duckduckgo(
                query, platforms, max_results, search_platforms, sort_by
            )

    def _search_with_tavily(
        self,
        query: str,
        platforms: List[str],
        max_results: int,
        search_depth: str = "advanced",
        days: int = None,
        include_raw_content: bool = False,
        search_platforms: List[str] = None,
        sort_by: str = "popular"
    ) -> Dict:
        """Tavily API로 검색"""
        # 검색 소스가 지정되지 않으면 기본값 사용
        if not search_platforms:
            search_platforms = ['coupang', 'naver']

        results = {
            "query": query,
            "platforms": platforms,
            "results": [],
            "search_engine": "tavily",
            "search_options": {
                "depth": search_depth,
                "days": days,
                "include_content": include_raw_content,
                "search_platforms": search_platforms,
                "sort_by": sort_by
            }
        }

        # 플랫폼별로 검색 (search_platforms 사용)
        for platform in search_platforms:
            # 플랫폼에 따라 쿼리 조정
            platform_query = self._build_platform_query(query, platform, sort_by)
            domain = self._get_platform_domain(platform)

            try:
                # Tavily 검색 옵션 설정
                search_params = {
                    "query": platform_query,
                    "max_results": max_results,
                    "search_depth": search_depth,
                    "include_raw_content": include_raw_content
                }

                # 도메인 필터 (쇼핑몰인 경우)
                if domain:
                    search_params["include_domains"] = [domain]

                # 검색 기간 설정 (Tavily는 days 파라미터 지원)
                if days:
                    search_params["days"] = days

                response = self.tavily.search(**search_params)

                for result in response.get("results", []):
                    result_data = {
                        "platform": platform,
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "snippet": result.get("content", ""),
                        "score": result.get("score", 0),
                        "timestamp": datetime.now().isoformat()
                    }

                    # 관련성 검증 (저품질 링크 필터링)
                    if not self._is_relevant_result(query, {"title": result_data["title"], "content": result_data["snippet"], "url": result_data["url"]}, platform):
                        continue

                    # 상세 콘텐츠 포함 (리뷰, 상세페이지 분석용)
                    if include_raw_content and "raw_content" in result:
                        result_data["raw_content"] = result["raw_content"]

                    results["results"].append(result_data)

            except Exception as e:
                print(f"[WebSearch] Tavily 검색 오류 ({platform}): {e}")
                results["results"].append({
                    "platform": platform,
                    "error": str(e)
                })

        return results

    def _search_with_duckduckgo(self, query: str, platforms: List[str], max_results: int, search_platforms: List[str] = None, sort_by: str = "popular") -> Dict:
        """DuckDuckGo로 검색 (fallback)"""
        results = {
            "query": query,
            "platforms": platforms,
            "results": [],
            "search_engine": "duckduckgo"
        }

        # search_platforms가 없으면 platforms 사용
        if not search_platforms:
            search_platforms = platforms

        for platform in search_platforms:
            platform_query = self._build_platform_query(query, platform, sort_by)

            try:
                search_results = list(self.ddgs.text(
                    platform_query,
                    max_results=max_results
                ))

                for result in search_results:
                    result_data = {
                        "platform": platform,
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", ""),
                        "timestamp": datetime.now().isoformat()
                    }

                    # 관련성 검증 (저품질 링크 필터링)
                    if not self._is_relevant_result(query, {"title": result_data["title"], "content": result_data["snippet"], "url": result_data["url"]}, platform):
                        continue

                    results["results"].append(result_data)

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
            "naver": "shopping.naver.com",  # 네이버 쇼핑
            "11st": "11st.co.kr",
            "news": None,  # 뉴스는 도메인 제한 없음
            "blog": None   # 블로그는 도메인 제한 없음
        }
        return domains.get(platform, platform)

    def _build_platform_query(self, query: str, platform: str, sort_by: str) -> str:
        """플랫폼과 정렬 기준에 맞는 검색 쿼리 생성"""
        # 쿠팡의 경우 실제 검색 URL 형식 사용
        if platform == "coupang":
            # URL 인코딩
            import urllib.parse
            encoded_query = urllib.parse.quote(query)

            # 정렬 파라미터 매핑
            sorter_map = {
                "popular": "saleCountDesc",  # 판매량순
                "recent": "latestAsc",        # 최신순
                "review": "scoreDesc",        # 쿠팡 랭킹순 (리뷰 포함)
                "price_low": "salePriceAsc",  # 낮은 가격순
                "price_high": "salePriceDesc" # 높은 가격순
            }
            sorter = sorter_map.get(sort_by, "scoreDesc")  # 기본값: 쿠팡 랭킹순

            # 쿠팡 검색 URL 형식 (component 파라미터 필수)
            coupang_url = f"https://www.coupang.com/np/search?component=&q={encoded_query}&sorter={sorter}"

            # 상품 상세 페이지 우선 검색
            platform_query = f"{query} site:coupang.com/vp/products"

            print(f"[WebSearch] 쿠팡 검색 URL 예시: {coupang_url}")
            print(f"[WebSearch] 쿠팡 검색 쿼리: {platform_query}")

        # 네이버 쇼핑의 경우 실제 검색 URL 형식 사용
        elif platform == "naver":
            import urllib.parse
            encoded_query = urllib.parse.quote(query)

            # 네이버 쇼핑 정렬 파라미터
            sort_map = {
                "popular": "popular",  # 인기순
                "recent": "date",      # 최신순
                "review": "review",    # 리뷰 많은 순
                "price_low": "price_asc",   # 낮은 가격순
                "price_high": "price_desc"  # 높은 가격순
            }
            sort_param = sort_map.get(sort_by, "popular")

            # 네이버 쇼핑 검색 URL 형식
            naver_url = f"https://search.shopping.naver.com/search/all?query={encoded_query}&sort={sort_param}"

            # 상품 상세 페이지 우선 검색 (smartstore 포함)
            platform_query = f"{query} site:smartstore.naver.com OR site:shopping.naver.com/catalog"

            print(f"[WebSearch] 네이버 쇼핑 검색 URL 예시: {naver_url}")
            print(f"[WebSearch] 네이버 검색 쿼리: {platform_query}")

        elif platform == "news":
            platform_query = f"{query} 뉴스"
            if sort_by == "recent":
                platform_query += " 최신"

        elif platform == "blog":
            platform_query = f"{query} 블로그 리뷰"
        else:
            platform_query = query
            domain = self._get_platform_domain(platform)
            if domain:
                platform_query = f"{platform_query} site:{domain}"

        return platform_query

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

    def _is_relevant_result(self, query: str, result: Dict, platform: str) -> bool:
        """검색 결과의 관련성 검증 (무관한 상품 및 저품질 링크 필터링)"""
        title = result.get("title", "").lower()
        snippet = result.get("content", "").lower()
        url = result.get("url", "")

        # 무효한 URL 패턴 체크 (확장)
        invalid_url_patterns = [
            r'trendshop\.shopping\.naver\.com/\w+/index',  # 네이버 스토어 메인
            r'shopping\.naver\.com/?$',  # 네이버 쇼핑 메인
            r'coupang\.com/?$',  # 쿠팡 메인
            r'coupang\.com/np/search',  # 쿠팡 검색 결과 페이지
            r'shopping\.naver\.com/search',  # 네이버 쇼핑 검색 결과 페이지
            r'/category/',  # 카테고리 페이지
            r'/event/',  # 이벤트 페이지
            r'/promotion/',  # 프로모션 페이지
            r'/best/',  # 베스트 상품 페이지
            r'/special/',  # 기획전 페이지
        ]

        for pattern in invalid_url_patterns:
            if re.search(pattern, url):
                print(f"[WebSearch] 저품질 URL 제외: {url[:80]}")
                return False

        # 저품질 제목 패턴 체크
        low_quality_title_patterns = [
            r'^\d+원$',  # "1000원" 같은 가격만 있는 제목
            r'^배송',  # "배송" 같은 키워드만
            r'^\s*$',  # 빈 제목
            r'쿠팡!',  # 쿠팡 광고
            r'^\d+개 상품',  # "100개 상품" 같은 검색 결과 집계
        ]

        for pattern in low_quality_title_patterns:
            if re.search(pattern, title):
                print(f"[WebSearch] 저품질 제목 제외: {title[:50]}")
                return False

        # 비정상 가격 패턴 체크 (1000원, 2500원 등)
        # 제목에 가격이 있으면 검증
        price_in_title = re.search(r'(\d{1,3}(?:,\d{3})*|\d+)원', title)
        if price_in_title:
            try:
                price = int(price_in_title.group(1).replace(',', ''))
                # 5000원 미만이면 의심스러운 상품
                if price < 5000:
                    print(f"[WebSearch] 비정상 가격({price}원) 제외: {title[:50]}")
                    return False
            except:
                pass

        # 쇼핑몰 플랫폼인 경우 상품 상세 페이지만 허용
        if platform == 'coupang':
            # 쿠팡은 /vp/products/ 경로만 허용
            if '/vp/products/' not in url:
                print(f"[WebSearch] 쿠팡 상품 페이지 아님: {url[:80]}")
                return False
        elif platform == 'naver':
            # 네이버는 smartstore나 catalog 경로만 허용
            if not ('smartstore.naver.com' in url or '/catalog/' in url):
                print(f"[WebSearch] 네이버 상품 페이지 아님: {url[:80]}")
                return False

        # 뉴스, 블로그는 관련성 검증 스킵
        if platform not in ['coupang', 'naver', '11st']:
            return True

        # 쿼리에서 핵심 키워드 추출 (첫 단어)
        query_words = query.lower().split()
        if not query_words:
            return True

        # 핵심 검색어 (첫 1-2 단어)
        main_keyword = query_words[0]

        # 제목 또는 설명에 핵심 키워드가 있는지 확인
        combined_text = f"{title} {snippet}"

        if main_keyword in combined_text:
            return True

        # 유사 키워드 매칭 (예: 가방 -> 백팩, 토트백)
        # 이 부분은 카테고리별로 확장 가능
        related_keywords = self._get_related_keywords(main_keyword)

        for keyword in related_keywords:
            if keyword in combined_text:
                return True

        # 핵심 키워드가 전혀 없으면 제외
        print(f"[WebSearch] 키워드 불일치 제외: '{main_keyword}' not in '{title[:50]}'")
        return False

    def _get_related_keywords(self, keyword: str) -> List[str]:
        """핵심 키워드의 관련 키워드 반환"""
        # 카테고리별 유사 키워드 매핑
        related_map = {
            "가방": ["백팩", "토트백", "크로스백", "숄더백", "파우치", "지갑", "백"],
            "신발": ["운동화", "스니커즈", "슬리퍼", "샌들", "부츠", "로퍼"],
            "의류": ["티셔츠", "셔츠", "바지", "청바지", "원피스", "자켓"],
            "전자제품": ["스마트폰", "노트북", "태블릿", "이어폰", "헤드폰"],
            "식품": ["간식", "음료", "과자", "음식", "먹거리"],
            "화장품": ["스킨케어", "메이크업", "클렌징", "크림", "세럼", "팩", "마스크", "토너", "에센스", "로션", "오일", "립", "파운데이션", "쿠션", "아이섀도우"],
            "뷰티": ["화장품", "스킨케어", "메이크업", "클렌징", "크림", "세럼", "팩", "마스크", "토너", "에센스", "로션", "미용", "뷰티템"],
            "립": ["립스틱", "립글로스", "립밤", "립틴트", "립"],
            "세럼": ["에센스", "앰플", "부스터", "세럼"],
            "크림": ["로션", "모이스처", "수분크림", "영양크림"],
            "클렌징": ["클렌저", "폼클렌징", "오일클렌징", "클렌징워터", "미셀라워터", "클렌징"],
            "팩": ["마스크팩", "시트팩", "수면팩", "워시오프팩", "팩"],
            "선크림": ["선블록", "자외선차단제", "썬케어", "선크림"],
        }

        return related_map.get(keyword, [keyword])
