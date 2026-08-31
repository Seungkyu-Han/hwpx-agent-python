from pydantic import BaseModel, Field


class HwpxTableElementModel(BaseModel):
    row: int = Field(
        ...,
        ge=0,
        description="셀의 행 인덱스 (0부터 시작하는 0-based index)",
        examples=[0],
    )
    col: int = Field(
        ...,
        ge=0,
        description="셀의 열 인덱스 (0부터 시작하는 0-based index)",
        examples=[0],
    )
    text: str = Field(
        ...,
        description="해당 셀 내부에 들어갈 텍스트 내용",
        examples=["항목명"],
    )
