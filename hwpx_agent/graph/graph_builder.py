from typing import Callable, Literal

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from hwpx_agent.graph.state import State
from hwpx_agent.models import HwpxModel, hwpx_model


def route_image_generate_node(state: State) -> Literal["image_generate_node", "_end"]:
    if state.is_image_generate:
        return "image_generate_node"
    else:
        return "_end"


def build_graph(
        hwpx_template_agent: Callable[[str], HwpxModel],
        image_generate_agent: Callable[[HwpxModel], HwpxModel],
) -> CompiledStateGraph:
    builder = StateGraph(State)

    def hwpx_template_node(state: State) -> dict:
        return {
            hwpx_model: hwpx_template_agent(state.prompt),
        }

    def image_generate_node(state: State) -> dict:
        return {
            hwpx_model: image_generate_agent(state.hwpx_model),
        }

    builder.add_node("hwpx_template_node", hwpx_template_node)
    builder.add_node("image_generate_node", image_generate_node)

    builder.add_edge(START, "hwpx_template_node")
    builder.add_conditional_edges(
        "hwpx_template_node",
        route_image_generate_node,
        {
            "image_generate_node": "hwpx_template_node",
            "_end": END,
        }
    )

    return builder.compile()
