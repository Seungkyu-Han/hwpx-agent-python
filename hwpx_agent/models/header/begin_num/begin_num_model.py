from pydantic import BaseModel, Field


class BeginNumModel(BaseModel):
    """
    문서 내에서 각종 객체들의 시작 번호 정보를 가지고 있는 요소
    """

    page: int = Field(default=1, description="페이지 시작 번호")
    footnote: int = Field(default=1, description="각주 시작 번호")
    end_note: int = Field(default=1, description="미주 시작 번호")
    pic: int = Field(default=1, description="그림 시작 번호")
    tbl: int = Field(default=1, description="표 시작 번호")
    equation: int = Field(default=1, description="수식 시작 번호")