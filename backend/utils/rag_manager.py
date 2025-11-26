"""
RAG 시스템 관리자 - 기존 상품 데이터 벡터화 및 검색
"""
import os
from typing import List, Dict
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

class RAGManager:
    """RAG 시스템 관리"""

    def __init__(self, persist_directory: str = "data/chroma_store"):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)

        # Embeddings 초기화
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Chroma vectorstore 초기화
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings,
            collection_name="product_pages"
        )

    def add_product(
        self,
        product_name: str,
        content: str,
        metadata: Dict = None
    ):
        """
        상품 데이터 추가

        Args:
            product_name: 상품명
            content: 상세페이지 콘텐츠
            metadata: 메타데이터 (카테고리, 플랫폼 등)
        """
        if metadata is None:
            metadata = {}

        metadata["product_name"] = product_name

        doc = Document(
            page_content=content,
            metadata=metadata
        )

        self.vectorstore.add_documents([doc])
        print(f"[RAG] 상품 추가됨: {product_name}")

    def search_similar_products(
        self,
        query: str,
        k: int = 3,
        filter_dict: Dict = None
    ) -> List[Document]:
        """
        유사 상품 검색

        Args:
            query: 검색 쿼리
            k: 반환할 결과 수
            filter_dict: 필터 조건 (예: {"category": "푸드"})

        Returns:
            유사 상품 문서 리스트
        """
        if filter_dict:
            results = self.vectorstore.similarity_search(
                query,
                k=k,
                filter=filter_dict
            )
        else:
            results = self.vectorstore.similarity_search(query, k=k)

        return results

    def get_context_for_product(
        self,
        product_name: str,
        category: str = None
    ) -> str:
        """
        상품에 대한 RAG 컨텍스트 생성

        Args:
            product_name: 상품명
            category: 카테고리 (필터링용)

        Returns:
            컨텍스트 문자열
        """
        query = f"{product_name} {category if category else ''}"

        filter_dict = {"category": category} if category else None

        similar_docs = self.search_similar_products(
            query,
            k=3,
            filter_dict=filter_dict
        )

        if not similar_docs:
            return "관련 상품 데이터 없음"

        # 컨텍스트 조합
        context_parts = []
        for i, doc in enumerate(similar_docs, 1):
            context_parts.append(f"## 유사 상품 {i}")
            context_parts.append(f"상품명: {doc.metadata.get('product_name', '알 수 없음')}")
            context_parts.append(f"내용: {doc.page_content[:300]}...")
            context_parts.append("")

        return "\n".join(context_parts)

    def load_sample_data(self):
        """샘플 데이터 로드 (개발용)"""
        # PDF에서 추출한 샘플 데이터 추가
        samples = [
            {
                "product_name": "제디터 정육 스테이크용 한우 (300g)",
                "category": "푸드",
                "content": """제디터 정육의 스테이크용 한우는 우리나라에서 최상급의 한우만을 선별하여
가공한 제품으로 최상의 품질과 맛을 보증합니다. 청결한 시스템에서 가공·포장되어 별다른 손질 없이도
안심하고 바로 조리할 수 있습니다. 1등급 이상 한우만을 엄선하였습니다.

Check Point:
- 최상의 품질: 믿음직한 1+ 한우만을 엄선하였습니다
- 최선의 맛과 육질: 부드러운 육질과 풍부한 식감을 선사합니다
- 풍부한 영양소: 단백질, 철분, 아미노산 등 다양한 영양소를 지닌 한우

사용부위: 안심
원산지: 국내산
등급: 1+

제디터 정육's Story:
오랜 세월동안 권위있는 이름으로 알려져 있는 브랜드입니다. 한우의 특별한 맛과 영양의 가치를
강조하며, 고객들에게 더욱 특별한 식사 경험을 선사하고자 항상 노력합니다.""",
                "metadata": {"category": "푸드", "platform": "쿠팡"}
            },
            {
                "product_name": "제디터 키즈 레깅스",
                "category": "패션",
                "content": """편한데 예쁘기까지? 엄마도 아이도 만족해요!

예쁜 컬러에 신축성 좋은 제디터 키즈 레깅스는 엄마도 아이도 너무 만족하는 아이템이에요!
만 2세부터 7세까지 사이즈가 준비되어 있습니다!

Point 1: 움직임 많은 우리 아이에게 딱 쫙쫙 늘어나는 신축성
Point 2: 어느 상황에나 입힐 수 있는 다양한 컬러
Point 3: 안심하고 입히세요 - 안심 항균 소재

4가지 색상: 멜란지 그레이, 스카이 블루, 라이트 퍼플, 핫핑크

상품 주문 전, 상세사이즈를 확인해주세요!""",
                "metadata": {"category": "패션", "platform": "네이버"}
            }
        ]

        for sample in samples:
            self.add_product(
                product_name=sample["product_name"],
                content=sample["content"],
                metadata=sample["metadata"]
            )

        print(f"[RAG] {len(samples)}개 샘플 데이터 로드 완료")

    def clear_all_data(self):
        """모든 데이터 삭제 (주의!)"""
        # Chroma의 모든 데이터 삭제
        self.vectorstore.delete_collection()
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="product_pages"
        )
        print("[RAG] 모든 데이터 삭제됨")


# 전역 RAG 매니저 인스턴스
_rag_manager = None

def get_rag_manager() -> RAGManager:
    """RAG 매니저 싱글톤 가져오기"""
    global _rag_manager
    if _rag_manager is None:
        _rag_manager = RAGManager()
    return _rag_manager
