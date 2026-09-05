from pydantic import BaseModel, Field
from .begin_num import BeginNumModel


class HeaderModel(BaseModel):
    begin_num: BeginNumModel = Field(default_factory=BeginNumModel)