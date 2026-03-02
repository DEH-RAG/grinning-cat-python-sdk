from typing import Dict, List, Any
from pydantic import BaseModel, Field, model_validator


class MemoryPoint(BaseModel):
    content: str
    metadata: Dict[str, Any]


class MessageBase(BaseModel):
    text: str
    image: str | bytes | None = None


class Message(MessageBase):
    metadata: Dict[str, Any] | None = None


class SettingInput(BaseModel):
    name: str
    value: Dict[str, Any]
    category: str | None = None


class Why(BaseModel):
    input: str | None = None
    intermediate_steps: List | None = Field(default_factory=list)
    memory: List | None = Field(default_factory=list)


class FilterSource(BaseModel):
    source: str | None = None
    hash: str | None = None

    @model_validator(mode="after")
    def validate_source_or_hash(self):
        assert self.source or self.hash, "Either source or hash must be provided"
        return self