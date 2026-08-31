from pydantic import BaseModel, Field

from hwpx_agent.models.hwpx_table_element_model import HwpxTableElementModel


class HwpxTableModel(BaseModel):
    rows: int = Field(
        ...,
        gt=0,
        description="표 전체의 총 행(Row) 수",
        examples=[5]
    )
    cols: int = Field(
        ...,
        gt=0,
        description="표 전체의 총 열(Column) 수",
        examples=[3]
    )
    elements: list[HwpxTableElementModel] = Field(
        default_factory=list,
        description="표 내부를 구성하는 개별 셀(HwpxTableElementModel) 객체들의 리스트"
    )
