from pydantic import BaseModel, Field, field_validator
from typing import Literal


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000, description="The user's question")
    conversation_history: list[Message] = Field(
        default_factory=list,
        max_length=20,
        description="Previous turns in the conversation (max 20)",
    )

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Message must not be blank or whitespace only")
        return v.strip()


class ChatResponse(BaseModel):
    reply: str = Field(..., description="The agent's response")
    model: str = Field(..., description="The model used to generate the response")
    in_scope: bool = Field(..., description="Whether the question was within the knowledge domain")


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    version: str