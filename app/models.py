from pydantic import BaseModel


class SummarizeRequest(BaseModel):
    text: str
    max_words: int = 100


class SummarizeResponse(BaseModel):
    summary: str
    word_count: int


class ClassifyRequest(BaseModel):
    text: str
    labels: list[str]


class ClassifyResponse(BaseModel):
    label: str
    reason: str