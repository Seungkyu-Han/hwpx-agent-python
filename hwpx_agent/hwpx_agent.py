from agents import Agent, Runner, function_tool
from hwpx import HwpxDocument

from .models import HwpxModel
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

        @function_tool(
            name_override="image_generate_tool",
            description_override=(
                    "HWPX 문서 내에 삽입할 고품질 이미지를 생성하는 도구입니다.\n"
                    "문서 내용에 어울리는 시각 자료(예: 과학 일러스트, 개념도, 표지 이미지, 그래픽 등)가 필요할 때 이 툴을 호출하세요.\n"
                    "- Input (prompt): 생성하려는 이미지에 대한 구체적이고 상세한 설명 (한국어 또는 영어 가능).\n"
                    "- Output (bytes): 생성된 이미지의 바이너리 버퍼 데이터."
            )
        )
        async def image_generate_tool(prompt: str) -> bytes:
            """
            문서에 포함시킬 이미지를 생성하고 바이너리(bytes)로 반환합니다.

            :param prompt: 이미지 생성 주제, 스타일, 구도, 주요 오브젝트 등에 대한 자연어 상세 설명
            :return: PNG/JPEG 이미지 파일의 raw bytes 데이터
            """
            return await self._image_generate(prompt)

        self._agent = Agent(
            name="hwpx-agent",
            instructions=self._SYSTEM_PROMPT,
            model=model,
            output_type=HwpxModel,
            tools=[image_generate_tool],
        )

    async def _image_generate(self, prompt: str) -> bytes:
        return await self._image_generate_agent.execute(prompt)

    async def generate_template(
            self,
            prompt: str,
    ) -> HwpxDocument:
        result = await Runner.run(self._agent, prompt)

        hwpx_model = result.final_output

        return model_to_hwpx(hwpx_model=hwpx_model)
