from typing import List

from grinning_cat_python_sdk.builders.base import BaseBuilder
from grinning_cat_python_sdk.models.dtos import Why


class WhyBuilder(BaseBuilder):
    def __init__(self):
        self.input: str | None = None
        self.intermediate_steps: List | None = []
        self.memory: List | None = []

    @staticmethod
    def create() -> "WhyBuilder":
        return WhyBuilder()

    def set_input(self, input: str | None = None) -> "WhyBuilder":
        self.input = input
        return self

    def set_intermediate_steps(self, intermediate_steps: List | None = None) -> "WhyBuilder":
        self.intermediate_steps = intermediate_steps or []
        return self

    def set_memory(self, memory: List | None = None) -> "WhyBuilder":
        self.memory = memory or []
        return self

    def build(self) -> Why:
        return Why(
            input=self.input,
            intermediate_steps=self.intermediate_steps,
            memory=self.memory,
        )
