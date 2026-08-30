from pydantic import BaseModel, Field

class HwpxHeadingModel(BaseModel):
    text: str = Field(
        description="번호 표기(접두사)를 제외한 순수 헤딩/문단 제목 텍스트"
    )

    level: int = Field(
        ge=1,
        le=8,
        description=(
            "문서의 제목/문단 번호 체계 레벨 (1~8).\n"
            "각 레벨에 따른 접두사 형식:\n"
            "Level 1: '1.' (예: 1.)\n"
            "Level 2: '가.' (예: 가.)\n"
            "Level 3: '1)' (예: 1))\n"
            "Level 4: '가)' (예: 가))\n"
            "Level 5: '(1)' (예: (1))\n"
            "Level 6: '(가)' (예: (가))\n"
            "Level 7: '①' (원형 숫자, 예: ①)\n"
            "Level 8: '㉮' (원형 한글, 예: ㉮)"
        )
    )