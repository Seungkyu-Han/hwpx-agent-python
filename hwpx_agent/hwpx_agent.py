import asyncio
import base64

from agents import Agent, Runner
from hwpx import HwpxDocument

from .models import HwpxModel, HwpxImageModel
from .tools import ImageGenerateAgent
from .transformers import model_to_hwpx


class HwpxAgent:
    _SYSTEM_PROMPT: str = """
    당신은 HWPX 파일 생성기입니다.
    
    사용자의 프롬프트를 바탕으로 파일을 생성해주세요
    """

    def __init__(
            self,
            model: str,
    ):
        self._image_generate_agent = ImageGenerateAgent(
            model=model,
        )

        self._agent = Agent(
            name="hwpx-agent",
            instructions=self._SYSTEM_PROMPT,
            model=model,
            output_type=HwpxModel,
            tools=[],
        )

    async def _image_generate(self, hwpx_image: HwpxImageModel) -> HwpxImageModel:
        if hwpx_image.image_prompt and not hwpx_image.base64_image:
            raw_bytes: bytes = await self._image_generate_agent.execute(hwpx_image.image_prompt)
            hwpx_image.base64_image = base64.b64encode(raw_bytes).decode("utf-8")
        return hwpx_image

    async def generate_template(
            self,
            prompt: str,
    ) -> HwpxDocument:
        result = await Runner.run(self._agent, prompt)

        hwpx_model = result.final_output

        image_tasks = [
            self._image_generate(content)
            for content in hwpx_model.contents
            if isinstance(content, HwpxImageModel)
        ]

        if image_tasks:
            await asyncio.gather(*image_tasks)

        return model_to_hwpx(hwpx_model=hwpx_model)
