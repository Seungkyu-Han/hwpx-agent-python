from hwpx import HwpxDocument
from langchain_core.runnables import RunnableConfig

from hwpx_agent.exceptions import HwpxEmptyException, AgentConfigException
from hwpx_agent.graph.state import State
from hwpx_agent.transformers import model_to_hwpx


async def hwpx_model_transform_node(
        state: State,
        config: RunnableConfig,
) -> dict[str, HwpxDocument]:

    if not state.hwpx_model:
        raise HwpxEmptyException("hwpx_model must be provided when request image generate")

    hwpx: HwpxDocument = model_to_hwpx(state.hwpx_model)

    return {
        'hwpx': hwpx,
    }

