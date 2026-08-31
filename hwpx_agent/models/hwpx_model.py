from pydantic import BaseModel

from hwpx_agent.models.hwpx_heading_model import HwpxHeadingModel
from hwpx_agent.models.hwpx_paragraph_model import HwpxParagraphModel


class HwpxModel(BaseModel):
    contents: list[
        HwpxHeadingModel | HwpxParagraphModel
    ]