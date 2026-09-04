from hwpx import HwpxDocument
from langchain_core.runnables import RunnableConfig

from .exceptions import HwpxEmptyException
from .graph import build_graph, State
from .tools import ImageGenerateAgent, HwpxTemplateAgent


class HwpxAgent:

    """
    Represents an agent responsible for generating HWPX documents based on user prompts.

    This class facilitates generating HWPX documents by employing internal agents for
    image generation and HWPX templates. It utilizes a graph-based approach to process
    prompts and produce structured document outputs.

    :ivar graph: The graph used to process and invoke generation logic.
    :type graph: Any
    """

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

        """
        Generates an HWPX document template based on the provided prompt.
        This asynchronous method invokes a graph-based
        process to produce a structured HWPX output, integrating configurations for
        image and template generation agents.

        :param prompt: The text input used to guide the template generation.
        :param is_image_generate: A boolean flag indicating whether images should
            be generated alongside the HWPX document. Defaults to False.
        :return: The generated HWPX document resulting from the given prompt and
            configuration.
        :rtype: HwpxDocument
        :raises HwpxEmptyException: If the resulting HWPX document is None.
        :raises AgentConfigException: If the image or template agents are not configured.
        """

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
