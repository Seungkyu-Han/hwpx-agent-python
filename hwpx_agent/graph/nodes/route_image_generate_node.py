from typing import Literal

from hwpx_agent.graph import State


def route_image_generate_node(state: State) -> Literal["image_generate_node", "_end"]:
    if state.is_image_generate:
        return "image_generate_node"
    else:
        return "_end"