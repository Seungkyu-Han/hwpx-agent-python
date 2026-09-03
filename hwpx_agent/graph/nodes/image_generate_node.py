import asyncio
import base64

from langchain_core.runnables import RunnableConfig

from hwpx_agent.exceptions import AgentConfigException, HwpxEmptyException
from hwpx_agent.graph.state import State
from hwpx_agent.models import HwpxModel, HwpxImageModel
from hwpx_agent.tools import ImageGenerateAgent


async def image_generate_node(
        state: State,
        config: RunnableConfig,
) -> dict[str, HwpxModel]:
    configurable = config.get("configurable", {})

    image_generate_agent: ImageGenerateAgent | None = configurable.get("image_generate_agent")

    if not image_generate_agent:
        raise AgentConfigException("image_generate_agent must be provided")

    if not isinstance(image_generate_agent, ImageGenerateAgent):
        raise AgentConfigException("image_generate_agent must be an instance of ImageGenerateAgent")

    if not state.hwpx_model:
        raise HwpxEmptyException("hwpx_model must be provided when request image generate")

    async def process_image(hwpx_image: HwpxImageModel, image_generate_agent_: ImageGenerateAgent):
        raw_bytes: bytes = await image_generate_agent_.execute(hwpx_image.image_prompt)
        hwpx_image.base64_image = base64.b64encode(raw_bytes).decode("utf-8")

    hwpx_image_models: list[HwpxImageModel] = [
        content
        for content in state.hwpx_model.contents
        if isinstance(content, HwpxImageModel)
    ]

    image_tasks = [
        process_image(content, image_generate_agent)
        for content in hwpx_image_models
        if content.image_prompt and content.base64_image is None
    ]

    if image_tasks:
        await asyncio.gather(*image_tasks)

    return {
        "hwpx_model": state.hwpx_model
    }