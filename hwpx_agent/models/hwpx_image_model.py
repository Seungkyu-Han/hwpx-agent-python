from pydantic import BaseModel, Field


class HwpxImageModel(BaseModel):
    image_prompt: str = Field(
        ...,
        description="이미지 생성을 위한 구체적인 이미지 설명 프롬프트 (예: 'DNA 이중선 꼬임 구조 일러스트')"
    )

    base64_image: str | None = Field(default=None)
