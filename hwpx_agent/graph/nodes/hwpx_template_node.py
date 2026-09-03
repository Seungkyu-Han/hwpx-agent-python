from langchain_core.runnables import RunnableConfig

from hwpx_agent.exceptions import AgentConfigException
from hwpx_agent.graph.state import State
from hwpx_agent.models import HwpxModel
from hwpx_agent.tools import HwpxTemplateAgent


async def hwpx_template_node(
        state: State,
        config: RunnableConfig,
) -> dict[str, HwpxModel]:
    configurable = config.get("configurable", {})

    hwpx_template_agent: HwpxTemplateAgent | None = configurable.get("hwpx_template_agent")

    if not hwpx_template_agent:
        raise AgentConfigException("hwpx_template_agent must be provided")

    if not isinstance(hwpx_template_agent, HwpxTemplateAgent):
        raise AgentConfigException("hwpx_template_agent must be an instance of HwpxTemplateAgent")

    hwpx_model: HwpxModel = await hwpx_template_agent.execute(state.prompt)

    return {
        "hwpx_model": hwpx_model
    }
