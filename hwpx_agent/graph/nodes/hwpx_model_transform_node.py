from hwpx import HwpxDocument
from langchain_core.runnables import RunnableConfig

from hwpx_agent.exceptions import HwpxEmptyException, AgentConfigException
from hwpx_agent.graph import State
from hwpx_agent.transformers import model_to_hwpx


async def hwpx_model_transform_node(
        state: State,
        config: RunnableConfig,
) -> dict[str, HwpxDocument]:

    if not state.hwpx_model:
        raise HwpxEmptyException("")

    hwpx: HwpxDocument = model_to_hwpx(state.hwpx_model)

    return {
        'hwpx': hwpx,
    }

