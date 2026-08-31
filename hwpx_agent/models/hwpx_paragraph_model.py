from pydantic import BaseModel, Field

from hwpx_agent.models.hwpx_style_model import HwpxStyleModel


class HwpxParagraphModel(BaseModel):

    text: str = Field(
        ...,
        description="문단의 본문 텍스트 내용"
    )

    style: HwpxStyleModel = Field(description="해당 본문의 스타일")