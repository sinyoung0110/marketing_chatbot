"""
이미지 생성 도구
"""
from typing import Dict
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ImageGenerationTool:
    """이미지 생성 도구"""

    def __init__(self):
        self.project_dir = "projects"

    def create_prompt(self, product_name: str, shot_type: str, style: str = "real") -> str:
        """
        이미지 생성 프롬프트 생성

        Args:
            product_name: 상품명
            shot_type: 촬영 타입 (main/usage/infographic/detail)
            style: 스타일 (real/lifestyle/illustration)

        Returns:
            이미지 생성 프롬프트
        """
        prompts = {
            "main": {
                "real": f"Professional product photography of {product_name}, clean white studio background, soft diffused lighting from 45-degree angle, minimal shadows, photorealistic, sharp focus, shot with Canon EOS R5, 85mm lens, f/2.8, commercial catalog style, no artificial effects",
                "lifestyle": f"Authentic lifestyle photograph of {product_name} on modern kitchen counter with natural morning light through window, real wooden table texture, subtle imperfections, shot with natural grain, candid style, not overly polished",
                "illustration": f"Simple line drawing of {product_name}, hand-drawn style with slight imperfections, minimal colors, sketch-like quality"
            },
            "usage": {
                "real": f"Documentary-style photograph of hands naturally holding and using {product_name}, real skin texture visible, natural home environment with lived-in details, soft window light, shot with 50mm lens, photojournalistic style, authentic moment",
                "lifestyle": f"Candid photograph of {product_name} being used in real daily life scenario, natural imperfect lighting, slight motion blur, genuine moment captured, real people in comfortable clothing, warm and relatable atmosphere",
                "illustration": f"Step-by-step usage diagram with simple hand-drawn icons, minimal color palette, clear but not overly polished"
            },
            "infographic": {
                "real": f"Clean comparison chart for {product_name}, simple typography, real product photos (not 3D renders), professional but not overly designed, white background, clear hierarchy",
                "lifestyle": f"Before-and-after comparison showing {product_name} in use, real photography, natural settings, documentary style",
                "illustration": f"Simple infographic with hand-drawn elements, minimal colors, information-focused design"
            },
            "detail": {
                "real": f"Macro photograph of {product_name} showing real material texture, natural lighting reveals authentic surface details, shot with macro lens, photorealistic grain, no artificial enhancements, true-to-life colors",
                "lifestyle": f"Close-up detail shot of {product_name} in natural use context, shallow depth of field, real environment in background, authentic worn-in look if applicable",
                "illustration": f"Technical line drawing showing {product_name} details, engineering-drawing style, minimal shading"
            }
        }

        return prompts.get(shot_type, {}).get(style, prompts["main"]["real"])

    def generate(self, prompt: str, project_id: str, image_type: str = "main") -> str:
        """
        이미지 생성 - DALL-E 우선, 실패 시 플레이스홀더

        Args:
            prompt: 이미지 생성 프롬프트
            project_id: 프로젝트 ID
            image_type: 이미지 타입

        Returns:
            생성된 이미지 경로
        """
        # OpenAI API 키 확인
        api_key = os.getenv("OPENAI_API_KEY")

        if api_key:
            print(f"[ImageGen] DALL-E로 이미지 생성 시도: {image_type}")
            try:
                return self.generate_with_dalle(prompt, project_id, image_type)
            except Exception as e:
                print(f"[ImageGen] DALL-E 실패, 플레이스홀더 사용: {e}")
        else:
            print(f"[ImageGen] API 키 없음, 플레이스홀더 생성")

        # 플레이스홀더 생성
        image_dir = os.path.join(self.project_dir, project_id, "images")
        os.makedirs(image_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{image_type}_{timestamp}.jpg"
        image_path = os.path.join(image_dir, image_filename)

        self._create_placeholder_image(image_path, prompt)

        return f"/projects/{project_id}/images/{image_filename}"

    def _create_placeholder_image(self, path: str, prompt: str):
        """플레이스홀더 이미지 생성 (개발용)"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import textwrap

            # 기본 이미지 생성
            img = Image.new('RGB', (1000, 1000), color=(240, 240, 245))
            draw = ImageDraw.Draw(img)

            # 텍스트 추가
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
            except:
                font = ImageFont.load_default()

            # 프롬프트를 여러 줄로 나누기
            wrapped_text = textwrap.fill(prompt[:200], width=40)

            # 텍스트 그리기
            bbox = draw.textbbox((0, 0), wrapped_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            position = ((1000 - text_width) // 2, (1000 - text_height) // 2)
            draw.text(position, wrapped_text, fill=(100, 100, 120), font=font)

            # 워터마크
            draw.text((10, 960), "Preview Image", fill=(150, 150, 150), font=font)

            # 저장
            img.save(path, "JPEG", quality=85)

        except Exception as e:
            print(f"[ImageGen] 플레이스홀더 생성 실패: {e}")
            # 빈 파일이라도 생성
            with open(path, 'w') as f:
                f.write(f"Image placeholder: {prompt}")

    def generate_with_dalle(self, prompt: str, project_id: str, image_type: str) -> str:
        """
        DALL-E를 사용한 실제 이미지 생성

        환경변수 OPENAI_API_KEY 필요
        """
        from openai import OpenAI
        import requests

        print(f"\n{'='*60}")
        print(f"[DALL-E DEBUG] 이미지 생성 시작")
        print(f"{'='*60}")
        print(f"📝 Image Type: {image_type}")
        print(f"📝 Project ID: {project_id}")
        print(f"📝 Prompt: {prompt[:100]}...")

        # 클라이언트 생성
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"🔑 API Key: {api_key[:20]}...{api_key[-10:] if api_key else 'None'}")

        client = OpenAI(api_key=api_key)

        # DALL-E 이미지 생성
        print(f"\n🎨 DALL-E API 호출 중...")
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )

            print(f"✅ DALL-E 응답 받음")
            print(f"📊 Response Type: {type(response)}")
            print(f"📊 Response Data: {response.data}")

            if not response.data or len(response.data) == 0:
                raise ValueError("DALL-E가 이미지를 생성하지 않았습니다")

            image_url = response.data[0].url
            print(f"🔗 Image URL: {image_url[:50]}...")

        except Exception as api_error:
            print(f"❌ DALL-E API 오류: {api_error}")
            print(f"오류 타입: {type(api_error)}")
            raise

        # 이미지 디렉토리 생성
        image_dir = os.path.join(self.project_dir, project_id, "images")
        os.makedirs(image_dir, exist_ok=True)
        print(f"📁 이미지 디렉토리: {image_dir}")
        print(f"📁 디렉토리 존재: {os.path.exists(image_dir)}")

        # 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{image_type}_{timestamp}.png"
        image_path = os.path.join(image_dir, image_filename)
        print(f"💾 저장 경로: {image_path}")

        # URL에서 이미지 다운로드
        print(f"\n📥 이미지 다운로드 중...")
        try:
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()

            print(f"✅ 다운로드 완료")
            print(f"📊 Content Type: {img_response.headers.get('Content-Type')}")
            print(f"📊 Content Length: {len(img_response.content)} bytes")

            # 파일 저장
            with open(image_path, 'wb') as f:
                f.write(img_response.content)

            print(f"💾 파일 저장 완료")
            print(f"📊 파일 존재: {os.path.exists(image_path)}")
            print(f"📊 파일 크기: {os.path.getsize(image_path)} bytes")

        except Exception as download_error:
            print(f"❌ 다운로드 오류: {download_error}")
            raise

        # 반환 경로
        return_path = f"/projects/{project_id}/images/{image_filename}"
        print(f"\n✅ 이미지 생성 완료")
        print(f"🔗 반환 경로: {return_path}")
        print(f"{'='*60}\n")

        return return_path
