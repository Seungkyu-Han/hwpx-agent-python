from agents import Agent, Runner, ModelSettings
from hwpx import HwpxDocument

from hwpx_agent.models import HwpxModel
from hwpx_agent.transformers import model_to_hwpx


class HwpxAgent:
    _SYSTEM_PROMPT: str = """
    당신은 HWPX 파일 생성기입니다.
    
    사용자의 프롬프트를 바탕으로 파일을 생성해주세요
    """

    def __init__(
            self,
            model: str,
    ):
        self._agent = Agent(
            name="hwpx-agent",
            instructions=self._SYSTEM_PROMPT,
            model=model,
            output_type=HwpxModel,
            model_settings=ModelSettings(
                temperature=0.5,
            )
        )

    async def generate_template(
            self,
            prompt: str,
    ) -> HwpxDocument:
        result = await Runner.run(self._agent, prompt)

        hwpx_model = result.final_output

        return model_to_hwpx(hwpx_model=hwpx_model)
