"""
프로젝트 세션 관리 시스템
사용자가 한 번 입력한 데이터를 자동으로 이어서 사용
"""
from typing import Dict, Optional, Any
from datetime import datetime
import uuid
import json
import os


class ProjectSession:
    """단일 프로젝트 세션 (SWOT → 상세페이지 → 챗봇)"""

    def __init__(self, session_id: str = None):
        self.session_id = session_id or f"proj_{uuid.uuid4().hex[:8]}"
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

        # 각 단계별 데이터
        self.product_info: Dict[str, Any] = {}
        self.swot_result: Optional[Dict] = None
        self.competitor_data: Optional[Dict] = None
        self.review_insights: Optional[Dict] = None
        self.detail_page_result: Optional[Dict] = None
        self.chat_history: list = []

        # 진행 상태
        self.current_step: str = "init"  # init → swot → detail → chat
        self.completed_steps: list = []

    def update_product_info(self, product_info: Dict):
        """상품 정보 업데이트"""
        self.product_info.update(product_info)
        self.updated_at = datetime.now().isoformat()

    def set_swot_result(self, swot_result: Dict, competitor_data: Dict):
        """SWOT 분석 결과 저장"""
        self.swot_result = swot_result
        self.competitor_data = competitor_data
        self.current_step = "swot"
        if "swot" not in self.completed_steps:
            self.completed_steps.append("swot")
        self.updated_at = datetime.now().isoformat()

    def set_review_insights(self, review_insights: Dict):
        """리뷰 인사이트 저장"""
        self.review_insights = review_insights
        self.updated_at = datetime.now().isoformat()

    def set_detail_page_result(self, detail_page_result: Dict):
        """상세페이지 생성 결과 저장"""
        self.detail_page_result = detail_page_result
        self.current_step = "detail"
        if "detail" not in self.completed_steps:
            self.completed_steps.append("detail")
        self.updated_at = datetime.now().isoformat()

    def add_chat_message(self, role: str, content: str):
        """챗봇 대화 추가"""
        self.chat_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.current_step = "chat"
        if "chat" not in self.completed_steps:
            self.completed_steps.append("chat")
        self.updated_at = datetime.now().isoformat()

    def get_context_for_chat(self) -> str:
        """챗봇을 위한 컨텍스트 생성"""
        context_parts = [f"상품명: {self.product_info.get('product_name', '')}"]

        if self.product_info.get('category'):
            context_parts.append(f"카테고리: {self.product_info['category']}")

        if self.product_info.get('keywords'):
            context_parts.append(f"키워드: {', '.join(self.product_info['keywords'])}")

        if self.swot_result:
            context_parts.append("\n[SWOT 분석 완료]")
            if "swot" in self.swot_result:
                context_parts.append(f"강점: {', '.join(self.swot_result['swot'].get('strengths', [])[:3])}")

        if self.review_insights:
            context_parts.append("\n[리뷰 인사이트]")
            context_parts.append(str(self.review_insights))

        return "\n".join(context_parts)

    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "product_info": self.product_info,
            "swot_result": self.swot_result,
            "competitor_data": self.competitor_data,
            "review_insights": self.review_insights,
            "detail_page_result": self.detail_page_result,
            "chat_history": self.chat_history,
            "current_step": self.current_step,
            "completed_steps": self.completed_steps
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "ProjectSession":
        """딕셔너리에서 복원"""
        session = cls(session_id=data.get("session_id"))
        session.created_at = data.get("created_at", session.created_at)
        session.updated_at = data.get("updated_at", session.updated_at)
        session.product_info = data.get("product_info", {})
        session.swot_result = data.get("swot_result")
        session.competitor_data = data.get("competitor_data")
        session.review_insights = data.get("review_insights")
        session.detail_page_result = data.get("detail_page_result")
        session.chat_history = data.get("chat_history", [])
        session.current_step = data.get("current_step", "init")
        session.completed_steps = data.get("completed_steps", [])
        return session


class SessionManager:
    """세션 관리자 (메모리 기반)"""

    def __init__(self):
        self.sessions: Dict[str, ProjectSession] = {}
        self.sessions_dir = os.path.join(os.path.dirname(__file__), "..", "sessions")
        os.makedirs(self.sessions_dir, exist_ok=True)

    def create_session(self) -> ProjectSession:
        """새 세션 생성"""
        session = ProjectSession()
        self.sessions[session.session_id] = session
        self._save_session(session)
        return session

    def get_session(self, session_id: str) -> Optional[ProjectSession]:
        """세션 조회 (메모리 → 파일)"""
        # 메모리 캐시 확인
        if session_id in self.sessions:
            return self.sessions[session_id]

        # 파일에서 로드
        session = self._load_session(session_id)
        if session:
            self.sessions[session_id] = session
        return session

    def update_session(self, session: ProjectSession):
        """세션 업데이트"""
        self.sessions[session.session_id] = session
        self._save_session(session)

    def delete_session(self, session_id: str):
        """세션 삭제"""
        if session_id in self.sessions:
            del self.sessions[session_id]

        # 파일 삭제
        session_file = os.path.join(self.sessions_dir, f"{session_id}.json")
        if os.path.exists(session_file):
            os.remove(session_file)

    def list_sessions(self) -> list:
        """모든 세션 목록"""
        return [s.to_dict() for s in self.sessions.values()]

    def _save_session(self, session: ProjectSession):
        """세션을 파일로 저장"""
        session_file = os.path.join(self.sessions_dir, f"{session.session_id}.json")
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session.to_dict(), f, ensure_ascii=False, indent=2)

    def _load_session(self, session_id: str) -> Optional[ProjectSession]:
        """파일에서 세션 로드"""
        session_file = os.path.join(self.sessions_dir, f"{session_id}.json")
        if os.path.exists(session_file):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return ProjectSession.from_dict(data)
            except:
                return None
        return None


# 싱글톤 인스턴스
_session_manager = None


def get_session_manager() -> SessionManager:
    """세션 매니저 싱글톤 조회"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
