from pydantic import BaseModel

from hwpx_agent.models import HwpxModel


class State(BaseModel):
    prompt: str
    is_image_generate: bool
    hwpx_model: HwpxModel
