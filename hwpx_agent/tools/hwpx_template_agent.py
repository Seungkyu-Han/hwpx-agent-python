from agents import Agent, Runner

from hwpx_agent.models import HwpxModel


class HwpxTemplateAgent:
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
        )

    async def execute(self, prompt) -> HwpxModel:

        result = await Runner.run(
            self._agent,
            input=prompt,
        )

        return result.final_output