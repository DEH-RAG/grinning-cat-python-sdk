from typing import Dict, Any

from grinning_cat_python_sdk.builders.base import BaseBuilder
from grinning_cat_python_sdk.models.dtos import MemoryPoint


class MemoryPointBuilder(BaseBuilder):
    def __init__(self):
        self.content: str = ""
        self.metadata: Dict[str, Any] = {}

    @staticmethod
    def create():
        return MemoryPointBuilder()

    def set_content(self, content: str):
        self.content = content
        return self

    def set_metadata(self, metadata: Dict[str, Any]):
        self.metadata = metadata
        return self

    def build(self):
        return MemoryPoint(self.content, self.metadata)