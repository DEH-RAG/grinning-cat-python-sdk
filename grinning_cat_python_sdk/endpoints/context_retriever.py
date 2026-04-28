from typing import Dict, Any

from grinning_cat_python_sdk.endpoints.base import AbstractEndpoint
from grinning_cat_python_sdk.models.api.factories import FactoryObjectSettingsOutput, FactoryObjectSettingOutput


class ContextRetrieverEndpoint(AbstractEndpoint):
    def __init__(self, client: "GrinningCatClient"):
        super().__init__(client)
        self.prefix = "/context_retriever"

    def get_context_retrievers_settings(self, agent_id: str) -> FactoryObjectSettingsOutput:
        """
        Get all context retrievers settings for the agent specified by agent_id
        :param agent_id: The agent id
        :return: FactoryObjectSettingsOutput, a list of context retrievers settings
        """
        return self.get(
            self.format_url("/settings"),
            agent_id,
            output_class=FactoryObjectSettingsOutput,
        )

    def get_context_retriever_settings(self, context_retriever: str, agent_id: str) -> FactoryObjectSettingOutput:
        """
        Get the context retriever settings for the context retriever specified by context_retriever and agent_id
        :param context_retriever: The name of the context retriever
        :param agent_id: The agent id
        :return: FactoryObjectSettingOutput, the large language model settings
        """
        return self.get(
            self.format_url(f"/settings/{context_retriever}"),
            agent_id,
            output_class=FactoryObjectSettingOutput,
        )

    def put_context_retriever_settings(
        self, context_retriever: str, agent_id: str, values: Dict[str, Any]
    ) -> FactoryObjectSettingOutput:
        """
        Update the context retriever settings for the context retriever specified by context_retriever and agent_id
        :param context_retriever: The name of the context retriever
        :param agent_id: The agent id
        :param values: The new settings
        :return: FactoryObjectSettingOutput, the updated context retriever settings
        """
        return self.put(
            self.format_url(f"/settings/{context_retriever}"),
            agent_id,
            output_class=FactoryObjectSettingOutput,
            payload=values,
        )
