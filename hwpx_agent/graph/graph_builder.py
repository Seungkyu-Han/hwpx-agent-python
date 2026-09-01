from typing import Callable, Coroutine, Any, Literal

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
        hwpx_template_agent: Callable[[str], Coroutine[Any, Any, HwpxModel]],
        image_generate_agent: Callable[[HwpxModel], Coroutine[Any, Any, HwpxModel]],
) -> CompiledStateGraph:
    builder = StateGraph(State)

    async def hwpx_template_node(state: State) -> dict[str, HwpxModel]:
        result = await hwpx_template_agent(state.prompt)
        return {
            "hwpx_model": result,
        }

    async def image_generate_node(state: State) -> dict[str, HwpxModel]:
        result = await image_generate_agent(state.hwpx_model)
        return {
            "hwpx_model": result
        }

    builder.add_node("hwpx_template_node", hwpx_template_node)
    builder.add_node("image_generate_node", image_generate_node)

    builder.add_edge(START, "hwpx_template_node")
    builder.add_conditional_edges(
        "hwpx_template_node",
        route_image_generate_node,
        {
            "image_generate_node": "image_generate_node",
            "_end": END,
        }
    )

    builder.add_edge("image_generate_node", END)

    return builder.compile()
