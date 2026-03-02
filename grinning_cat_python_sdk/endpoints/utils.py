from typing import List, Dict

from grinning_cat_python_sdk.endpoints.base import AbstractEndpoint
from grinning_cat_python_sdk.models.api.admins import (
    ResetOutput,
    AgentClonedOutput,
    AgentCreatedOutput,
    AgentOutput,
    AgentUpdatedOutput,
)
from grinning_cat_python_sdk.utils import deserialize


class UtilsEndpoint(AbstractEndpoint):
    def __init__(self, client: "GrinningCatClient"):
        super().__init__(client)
        self.prefix = "/utils"

    def post_factory_reset(self) -> ResetOutput:
        """
        Reset the system to the factory settings.
        :return: ResetOutput, the details of the reset.
        """
        return self.post_json(self.format_url("/factory/reset/"), self.system_id, output_class=ResetOutput)

    def get_agents(self) -> List[AgentOutput]:
        """
        Get a list of all agents.
        :return: List[AgentOutput], the ID and the metadata of the agents.
        """
        response = self.get_http_client(agent_id=self.system_id).get(self.format_url("/agents/"))
        response.raise_for_status()

        return [deserialize(item, AgentOutput) for item in response.json()]

    def post_agent_create(self, agent_id: str, metadata: Dict | None = None) -> AgentCreatedOutput:
        """
        Create a new agent.
        :param agent_id: The ID of the agent.
        :param metadata: The metadata of the agent.
        :return: AgentCreatedOutput, the details of the agent.
        """
        payload = {"agent_id": agent_id}
        if metadata is not None:
            payload["metadata"] = metadata  # type: ignore

        return self.post_json(
            self.format_url("/agents/create/"),
            self.system_id,
            output_class=AgentCreatedOutput,
            payload=payload,
        )

    def post_agent_reset(self, agent_id: str) -> ResetOutput:
        """
        Reset an agent to the factory settings.
        :param agent_id: The ID of the agent.
        :return: ResetOutput, the details of the reset.
        """
        return self.post_json(self.format_url("/agents/reset/"), agent_id, output_class=ResetOutput)

    def post_agent_destroy(self, agent_id: str) -> ResetOutput:
        """
        Destroy an agent.
        :param agent_id: The ID of the agent.
        :return: ResetOutput, the details of the reset.
        """
        return self.post_json(self.format_url("/agents/destroy/"), agent_id, output_class=ResetOutput)

    def post_agent_clone(self, agent_id: str, new_agent_id: str) -> AgentClonedOutput:
        """
        Destroy an agent.
        :param agent_id: The ID of the agent.
        :param new_agent_id: The ID of the new cloned agent.
        :return: AgentClonedOutput, the details of the cloning.
        """
        return self.post_json(
            self.format_url("/agents/clone/"),
            agent_id,
            payload={"agent_id": new_agent_id},
            output_class=AgentClonedOutput,
        )

    def put_agent(self, agent_id: str, metadata: Dict) -> AgentUpdatedOutput:
        """
        Update the metadata of an agent.
        :param agent_id: The ID of the agent.
        :param metadata: The new metadata for the agent.
        :return: AgentUpdatedOutput, the details of the update.
        """
        return self.put(
            self.format_url("/agents/"),
            agent_id,
            payload={"metadata": metadata},
            output_class=AgentUpdatedOutput,
        )
