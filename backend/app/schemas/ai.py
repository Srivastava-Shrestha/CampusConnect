from pydantic import BaseModel


class ClubFinderRequest(BaseModel):
    interest_text: str = ""


class ChatMessage(BaseModel):
    role: str          # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    reply: str
