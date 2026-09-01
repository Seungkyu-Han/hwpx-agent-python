import asyncio
import base64

from agents import Agent, Runner
from hwpx import HwpxDocument

from .exceptions import HwpxGenerateTemplateException
from .graph import build_graph, State
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
        )

        async def hwpx_template_func(prompt: str) -> HwpxModel:
            return await self._hwpx_template_func(prompt)

        async def image_generate_func(hwpx_model: HwpxModel) -> HwpxModel:
            return await self._image_generate_func(hwpx_model)

        self.graph = build_graph(
            hwpx_template_agent=hwpx_template_func,
            image_generate_agent=image_generate_func,
        )

    async def _hwpx_template_func(self, prompt: str) -> HwpxModel:
        result = await Runner.run(self._agent, prompt)
        return result.final_output

    async def _image_generate_func(self, hwpx_model: HwpxModel) -> HwpxModel:
        async def process_image(hwpx_image: HwpxImageModel):
            raw_bytes: bytes = await self._image_generate_agent.execute(hwpx_image.image_prompt)
            hwpx_image.base64_image = base64.b64encode(raw_bytes).decode("utf-8")

        hwpx_image_models: list[HwpxImageModel] = [content for content in hwpx_model.contents if
                                                   isinstance(content, HwpxImageModel)]

        image_tasks = [
            process_image(content)
            for content in hwpx_image_models
            if content.image_prompt and content.base64_image is None
        ]

        if image_tasks:
            await asyncio.gather(*image_tasks)

        return hwpx_model

    async def generate_template(
            self,
            prompt: str,
            is_image_generate: bool = False,
    ) -> HwpxDocument:
        state: State = State(
            prompt=prompt,
            is_image_generate=is_image_generate,
            hwpx_model=None,
        )

        result_dict = await self.graph.ainvoke(state)

        final_state: State = State(**result_dict)

        hwpx_model: HwpxModel | None = final_state.hwpx_model

        if not hwpx_model:
            raise HwpxGenerateTemplateException(message="hwpx 파일이 생성되지 않았습니다.")

        return model_to_hwpx(hwpx_model=hwpx_model)
