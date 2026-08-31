from pydantic import BaseModel

from hwpx_agent.models.hwpx_image_model import HwpxImageModel
from hwpx_agent.models.hwpx_table_model import HwpxTableModel
from hwpx_agent.models.hwpx_heading_model import HwpxHeadingModel
from hwpx_agent.models.hwpx_paragraph_model import HwpxParagraphModel


class HwpxModel(BaseModel):
    contents: list[
        HwpxHeadingModel | HwpxParagraphModel | HwpxTableModel | HwpxImageModel
    ]