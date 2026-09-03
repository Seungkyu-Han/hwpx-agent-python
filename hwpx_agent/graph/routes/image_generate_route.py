from typing import Literal

from hwpx_agent.graph.state import State


def image_generate_route(state: State) -> Literal["image_generate_node", "_next"]:
    if state.is_image_generate:
        return "image_generate_node"
    else:
        return "_next"