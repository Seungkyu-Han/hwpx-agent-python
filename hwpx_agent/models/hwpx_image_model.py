import base64

from pydantic import BaseModel, Field


class HwpxImageModel(BaseModel):
    base64_image: str = Field(
        ...,
        description="Base64로 인코딩된 이미지 문자열"
    )

    @property
    def buffer(self) -> bytes:
        return base64.b64decode(self.base64_image)