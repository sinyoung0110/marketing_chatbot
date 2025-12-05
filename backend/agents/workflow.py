"""
LangGraph 기반 상세페이지 생성 워크플로우
"""
from typing import TypedDict, Dict, List
from typing_extensions import Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import operator
import os
from dotenv import load_dotenv

from models.schemas import ProductInput
from tools.web_search import WebSearchTool
from tools.competitor_analysis import CompetitorAnalysisTool
from tools.swot_3c_analysis import SWOT3CAnalysisTool
from tools.analysis_visualizer import AnalysisVisualizer
from tools.selling_point import SellingPointGenerator
from tools.image_gen import ImageGenerationTool
from tools.exporter import ContentExporter

load_dotenv()

class AgentState(TypedDict):
    """에이전트 상태 정의"""
    product_input: Dict
    project_id: str
    rag_context: str
    competitor_data: Dict
    competitor_insights: Dict
    swot_3c_analysis: Dict
    analysis_html_path: str
    selling_points: List[Dict]
    content_sections: Dict
    image_prompts: List[Dict]
    images: Annotated[List[str], operator.add]
    markdown_path: str
    html_path: str
    errors: Annotated[List[str], operator.add]

class DetailPageGenerator:
    """상세페이지 생성 워크플로우 관리자"""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,  # 비용 절감: 0.7 → 0.3
            max_tokens=2000,  # 비용 절감: 응답 길이 제한
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Tools 초기화
        self.web_search = WebSearchTool()
        self.competitor_analyzer = CompetitorAnalysisTool(self.llm)
        self.swot_3c_analyzer = SWOT3CAnalysisTool(self.llm)
        self.analysis_visualizer = AnalysisVisualizer(project_id)
        self.selling_point_gen = SellingPointGenerator(self.llm)
        self.image_gen = ImageGenerationTool()
        self.exporter = ContentExporter(project_id)

        # 워크플로우 그래프 생성
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        """LangGraph 워크플로우 구축"""
        workflow = StateGraph(AgentState)

        # 노드 추가
        workflow.add_node("input_collector", self.collect_input)
        workflow.add_node("rag_loader", self.load_rag_context)
        workflow.add_node("competitor_search", self.search_competitors)
        workflow.add_node("analyze_competitors", self.extract_insights)
        workflow.add_node("strategic_analysis", self.perform_swot_3c_analysis)
        workflow.add_node("visualize_analysis", self.visualize_analysis)
        workflow.add_node("generate_selling_points", self.generate_selling_points)
        workflow.add_node("content_assembly", self.assemble_content)
        workflow.add_node("build_image_prompts", self.build_image_prompts)
        workflow.add_node("image_generation", self.generate_images)
        workflow.add_node("export", self.export_content)

        # 엣지 정의 (순서)
        workflow.set_entry_point("input_collector")
        workflow.add_edge("input_collector", "rag_loader")
        workflow.add_edge("rag_loader", "competitor_search")
        workflow.add_edge("competitor_search", "analyze_competitors")
        workflow.add_edge("analyze_competitors", "strategic_analysis")
        workflow.add_edge("strategic_analysis", "visualize_analysis")
        workflow.add_edge("visualize_analysis", "generate_selling_points")
        workflow.add_edge("generate_selling_points", "content_assembly")
        workflow.add_edge("content_assembly", "build_image_prompts")
        workflow.add_edge("build_image_prompts", "image_generation")
        workflow.add_edge("image_generation", "export")
        workflow.add_edge("export", END)

        return workflow.compile()

    def generate(self, product_input: ProductInput) -> Dict:
        """상세페이지 생성 실행"""
        initial_state: AgentState = {
            "product_input": product_input.dict(),
            "project_id": self.project_id,
            "rag_context": "",
            "competitor_data": {},
            "competitor_insights": {},
            "swot_3c_analysis": {},
            "analysis_html_path": "",
            "selling_points": [],
            "content_sections": {},
            "image_prompts": [],
            "images": [],
            "markdown_path": "",
            "html_path": "",
            "errors": []
        }

        # 워크플로우 실행
        result = self.workflow.invoke(initial_state)

        return {
            "markdown_url": result["markdown_path"],
            "html_url": result["html_path"],
            "analysis_url": result["analysis_html_path"],
            "images": result["images"],
            "content_sections": result["content_sections"]
        }

    def collect_input(self, state: AgentState) -> AgentState:
        """1. 입력값 검증 및 구조화"""
        print(f"[InputCollector] 입력 데이터 검증 중...")
        # 입력 데이터는 이미 Pydantic으로 검증됨
        return state

    def load_rag_context(self, state: AgentState) -> AgentState:
        """2. RAG 컨텍스트 로드"""
        print(f"[RAG Loader] 기존 상품 데이터 로딩 중...")
        try:
            from utils.rag_manager import get_rag_manager

            product_input = state["product_input"]
            rag_manager = get_rag_manager()

            # 유사 상품 검색
            context = rag_manager.get_context_for_product(
                product_name=product_input["product_name"],
                category=product_input.get("category")
            )
            state["rag_context"] = context
        except Exception as e:
            print(f"[RAG Loader] RAG 로드 실패: {e}")
            state["rag_context"] = "기존 상품 데이터 없음"
        return state

    def search_competitors(self, state: AgentState) -> AgentState:
        """3. 경쟁사 검색"""
        print(f"[Competitor Search] 경쟁사 검색 중...")
        product_input = state["product_input"]

        # 웹 검색 실행
        if product_input.get("allow_web_search", True):
            search_results = self.web_search.search(
                query=f"{product_input['product_name']} {product_input['category']}",
                platforms=product_input.get("platforms", ["coupang", "naver"])
            )
            state["competitor_data"] = search_results
        else:
            state["competitor_data"] = {"results": []}

        return state

    def extract_insights(self, state: AgentState) -> AgentState:
        """4. 경쟁사 인사이트 추출"""
        print(f"[Competitor Insights] 경쟁사 분석 중...")
        insights = self.competitor_analyzer.analyze(state["competitor_data"])
        state["competitor_insights"] = insights
        return state

    def perform_swot_3c_analysis(self, state: AgentState) -> AgentState:
        """5. SWOT + 3C 분석 수행"""
        print(f"[SWOT + 3C Analysis] 전략 분석 중...")
        analysis = self.swot_3c_analyzer.analyze(
            product_input=state["product_input"],
            competitor_data=state["competitor_data"]
        )
        state["swot_3c_analysis"] = analysis
        return state

    def visualize_analysis(self, state: AgentState) -> AgentState:
        """6. 분석 결과 시각화"""
        print(f"[Visualizer] 분석 결과 HTML 생성 중...")
        html_path = self.analysis_visualizer.generate_html(
            analysis_result=state["swot_3c_analysis"],
            product_input=state["product_input"]
        )
        state["analysis_html_path"] = html_path
        return state

    def generate_selling_points(self, state: AgentState) -> AgentState:
        """7. 셀링 포인트 생성"""
        print(f"[Selling Points] 셀링 포인트 생성 중...")
        selling_points = self.selling_point_gen.generate(
            product_input=state["product_input"],
            competitor_insights=state["competitor_insights"]
        )
        state["selling_points"] = selling_points
        return state

    def assemble_content(self, state: AgentState) -> AgentState:
        """8. 콘텐츠 조합"""
        print(f"[Content Assembly] 콘텐츠 조합 중...")
        # 플랫폼별 템플릿에 맞춰 섹션 생성
        from templates.platform_templates import PlatformTemplateManager

        template_mgr = PlatformTemplateManager(self.llm)
        content_sections = template_mgr.assemble_content(
            product_input=state["product_input"],
            selling_points=state["selling_points"],
            competitor_insights=state["competitor_insights"]
        )
        state["content_sections"] = content_sections
        return state

    def build_image_prompts(self, state: AgentState) -> AgentState:
        """9. 이미지 프롬프트 생성 (셀링 포인트 기반)"""
        print(f"[Image Prompts] 이미지 프롬프트 생성 중...")
        product_input = state["product_input"]
        content_sections = state.get("content_sections", {})
        selling_points = content_sections.get("selling_points", [])
        image_options = product_input.get("image_options", {})

        prompts = []

        # 1. 메인 이미지 (필수)
        main_prompt = self.image_gen.create_prompt(
            product_name=product_input["product_name"],
            shot_type="main",
            style=image_options.get("style", "real")
        )
        prompts.append({
            "type": "main",
            "prompt": main_prompt,
            "size": "1000x1000"
        })

        # 2. 셀링 포인트 기반 이미지 생성 (최대 5개)
        for idx, sp in enumerate(selling_points[:5]):
            sp_title = sp.get("title", "")
            sp_desc = sp.get("description", "")

            # 셀링 포인트 내용이 있으면 맞춤형 프롬프트 생성
            if sp_title and sp_desc:
                custom_prompt = self._create_selling_point_image_prompt(
                    product_name=product_input["product_name"],
                    selling_point_title=sp_title,
                    selling_point_desc=sp_desc,
                    style=image_options.get("style", "real")
                )
                prompts.append({
                    "type": f"detail{idx+1}",
                    "prompt": custom_prompt,
                    "size": "800x800"
                })
            else:
                # 기본 디테일 이미지
                default_prompt = self.image_gen.create_prompt(
                    product_name=product_input["product_name"],
                    shot_type=f"detail{idx+1}",
                    style=image_options.get("style", "real")
                )
                prompts.append({
                    "type": f"detail{idx+1}",
                    "prompt": default_prompt,
                    "size": "800x800"
                })

        # 셀링 포인트가 5개 미만이면 기본 디테일 이미지로 채우기
        current_count = len(selling_points)
        if current_count < 5:
            for idx in range(current_count, 5):
                default_prompt = self.image_gen.create_prompt(
                    product_name=product_input["product_name"],
                    shot_type=f"detail{idx+1}",
                    style=image_options.get("style", "real")
                )
                prompts.append({
                    "type": f"detail{idx+1}",
                    "prompt": default_prompt,
                    "size": "800x800"
                })

        print(f"[Image Prompts] {len(prompts)}개 이미지 프롬프트 생성 완료 ({len(selling_points)}개 셀링 포인트 기반)")
        state["image_prompts"] = prompts
        return state

    def _create_selling_point_image_prompt(self, product_name: str, selling_point_title: str, selling_point_desc: str, style: str) -> str:
        """셀링 포인트에 맞는 이미지 프롬프트 생성"""
        style_settings = {
            "real": "Professional product photography, clean background, soft lighting, photorealistic, sharp focus",
            "lifestyle": "Authentic lifestyle photograph, natural environment, candid style, warm atmosphere",
            "illustration": "Simple illustration, hand-drawn style, minimal colors, clean design"
        }

        base_style = style_settings.get(style, style_settings["real"])

        prompt = f"""{base_style}. Show {product_name} demonstrating '{selling_point_title}': {selling_point_desc}. Visual composition that clearly illustrates this specific feature."""

        return prompt

    def generate_images(self, state: AgentState) -> AgentState:
        """10. 이미지 생성 (비용 절감을 위해 임시 비활성화)"""
        print(f"[Image Generation] 🔴 이미지 생성 SKIP (비용 절감 모드)")

        # ===== 비용 절감: DALL-E 이미지 생성 비활성화 =====
        # 활성화하려면 아래 주석을 해제하세요
        images = []
        # for prompt_data in state["image_prompts"]:
        #     image_path = self.image_gen.generate(
        #         prompt=prompt_data["prompt"],
        #         project_id=state["project_id"],
        #         image_type=prompt_data["type"]
        #     )
        #     images.append(image_path)
        # ===== 여기까지 =====

        state["images"] = images
        return state

    def export_content(self, state: AgentState) -> AgentState:
        """11. 콘텐츠 내보내기"""
        print(f"[Exporter] 콘텐츠 내보내기 중...")
        markdown_path, html_path = self.exporter.export(
            content_sections=state["content_sections"],
            images=state["images"],
            product_input=state["product_input"]
        )

        state["markdown_path"] = markdown_path
        state["html_path"] = html_path
        return state
