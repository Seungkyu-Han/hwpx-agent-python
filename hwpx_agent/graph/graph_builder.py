from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

from hwpx_agent.graph.nodes import (
    hwpx_template_node,
    image_generate_node,
    hwpx_model_transform_node,
)
from hwpx_agent.graph.routes import (
    image_generate_route
)
from hwpx_agent.graph.state import State


def build_graph() -> CompiledStateGraph:
    builder = StateGraph(State)

    builder.add_node("hwpx_template_node", hwpx_template_node)
    builder.add_node("image_generate_node", image_generate_node)
    builder.add_node("hwpx_model_transform_node", hwpx_model_transform_node)

    builder.add_edge(START, "hwpx_template_node")

    builder.add_conditional_edges(
        "hwpx_template_node",
        image_generate_route,
        {
            "image_generate_node": "image_generate_node",
            "_next": "hwpx_model_transform_node",
        }
    )

    builder.add_edge("image_generate_node", "hwpx_model_transform_node")


    builder.add_edge("hwpx_model_transform_node", END)

    return builder.compile()
