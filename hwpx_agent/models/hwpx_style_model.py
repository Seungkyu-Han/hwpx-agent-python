from pydantic import BaseModel, Field


class HwpxStyleModel(BaseModel):
    bold: bool = Field(
        default=False,
        description="글자 굵게 여부"
    )
    italic: bool = Field(
        default=False,
        description="글자 기울임(이탤릭) 여부"
    )
    underline: bool = Field(
        default=False,
        description="밑줄 설정 여부 (underline_shape 또는 underline_color 지정 시 True로 자동 전환)"
    )
    color: str | None = Field(
        default=None,
        description="글자 색상 (Hex 컬러 코드, 예: '#003366' 또는 '003366')"
    )
    font: str | None = Field(
        default=None,
        description="글꼴 이름 (예: '함초롬바탕', '나눔고딕')"
    )
    size: int | float | None = Field(
        default=None,
        ge=0,
        description="글자 크기 (pt 단위, 예: 10, 12.5)"
    )
    highlight: str | None = Field(
        default=None,
        description="형광펜 형광 색상 (Hex 컬러 코드)"
    )
    strike: bool | None = Field(
        default=None,
        description="취소선 여부 (strike_shape 지정 시 True로 자동 전환)"
    )
    underline_shape: str | None = Field(
        default=None,
        description="밑줄 종류 (예: 'SOLID', 'DASH', 'DOT' 등 OWPML 표준 선 종류)"
    )
    underline_color: str | None = Field(
        default=None,
        description="밑줄 색상 (Hex 컬러 코드)"
    )
    strike_shape: str | None = Field(
        default=None,
        description="취소선 종류 (OWPML 표준 선 종류)"
    )
    ratio: int | None = Field(
        default=None,
        ge=10,
        le=400,
        description="장평 (%) - 10% ~ 400% 사이의 정수"
    )
    letter_spacing: int | None = Field(
        default=None,
        ge=-50,
        le=100,
        description="자간 (%) - -50% ~ 100% 사이의 정수"
    )
    shadow: str | None = Field(
        default=None,
        description="음영/그림자 색상 (Hex 컬러 코드)"
    )
    script: Literal["sup", "sub"] | None = Field(
        default=None,
        description="첨자 설정 ('sup': 위첨자, 'sub': 아래첨자)"
    )
    outline: str | None = Field(
        default=None,
        description="외곽선 종류 (hc:LineType1 어휘에 해당하는 선 종류)"
    )
    emboss: bool | None = Field(
        default=None,
        description="양각 효과 여부"
    )
    engrave: bool | None = Field(
        default=None,
        description="음각 효과 여부"
    )
    base_char_pr_id: str | int | None = Field(
        default=None,
        description="기반이 될 기존 글자 모양 ID (선택 사항)"
    )