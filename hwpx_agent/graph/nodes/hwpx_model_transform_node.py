from hwpx import HwpxDocument

from hwpx_agent.exceptions import HwpxEmptyException
from hwpx_agent.graph import State
from hwpx_agent.transformers import model_to_hwpx


async def hwpx_model_transform_node(
        state: State,
) -> dict[str, HwpxDocument]:

    if not state.hwpx_model:
        raise HwpxEmptyException("")

    hwpx = model_to_hwpx(state.hwpx_model)

    return {
        'hwpx': hwpx,
    }

