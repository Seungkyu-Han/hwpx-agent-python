import base64
from typing import Literal

from agents import Agent, Runner
from openai import AsyncOpenAI
from pydantic import BaseModel, Field


class ImageGenerateAgentOutput(BaseModel):
    revised_prompt: str = Field(
        ...,
        description="DALL-E 3 이미지 생성을 위해 최적화된 상세한 영문 프롬프트"
    )
    size: Literal["1024x1024", "1792x1024", "1024x1792"] = Field(
        default="1024x1024",
        description="이미지 비율 및 해상도"
    )


class ImageGenerateAgent:
    PROMPT: str = (
        "당신은 HWPX 문서에 삽입할 고품질 이미지를 생성하는 전문가입니다.\n"
        "사용자의 요청(한국어 또는 영문)을 분석하여 gpt-image-2가 이해하기에 최적화된 "
        "상세한 영문 프롬프트(revised_prompt)와 적절한 해상도를 작성하세요."
    )

    def __init__(
            self,
            model: str,
    ):
        self._async_openai = AsyncOpenAI()
        self._agent = Agent(
            name="image generate agent",
            instructions=self.PROMPT,
            model=model,
            output_type=ImageGenerateAgentOutput,
        )

    async def execute(self, prompt: str) -> bytes:
        result = await Runner.run(
            self._agent, input=prompt,
        )

        output_data: ImageGenerateAgentOutput = result.final_output

        image_response = await self._async_openai.images.generate(
            model="gpt-image-2-2026-04-21",
            prompt=output_data.revised_prompt,
            size=output_data.size,
            n=1,
        )

        b64_data = image_response.data[0].b64_json
        if not b64_data:
            raise RuntimeError("이미지 생성 데이터를 받아오지 못했습니다.")

        return base64.b64decode(b64_data)
