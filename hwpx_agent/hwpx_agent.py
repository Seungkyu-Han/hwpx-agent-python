from hwpx import HwpxDocument
from langchain_core.runnables import RunnableConfig

from .exceptions import HwpxEmptyException
from .graph import build_graph, State
from .tools import ImageGenerateAgent, HwpxTemplateAgent


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

        self._hwpx_template_agent = HwpxTemplateAgent(
            model=model,
        )

        self.graph = build_graph()


    async def generate_template(
            self,
            prompt: str,
            is_image_generate: bool = False,
    ) -> HwpxDocument:
        state: State = State(
            prompt=prompt,
            is_image_generate=is_image_generate,
            hwpx_model=None,
            hwpx=None,
        )

        result_dict = await self.graph.ainvoke(state, config=RunnableConfig(
            configurable={
                "image_generate_agent": self._image_generate_agent,
                "hwpx_template_agent": self._hwpx_template_agent,
            }
        ))

        final_state: State = State(**result_dict)

        hwpx = final_state.hwpx

        if hwpx is None:
            raise HwpxEmptyException("hwpx is None")
        else:
            return hwpx
