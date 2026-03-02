from typing import Dict, Any
from pydantic import BaseModel

from grinning_cat_python_sdk.models.api.plugins import PluginToggleOutput


class AgentCreatedOutput(BaseModel):
    created: bool


class PluginDeleteOutput(BaseModel):
    deleted: str


class PluginDetailsOutput(BaseModel):
    data: Dict[str, Any]


class PluginInstallFromRegistryOutput(PluginToggleOutput):
    url: str
    info: str


class PluginInstallOutput(PluginToggleOutput):
    filename: str
    content_type: str


class ResetOutput(BaseModel):
    deleted_settings: bool
    deleted_memories: bool
    deleted_plugin_folders: bool


class AgentClonedOutput(BaseModel):
    cloned: bool = False


class AgentUpdatedOutput(BaseModel):
    updated: bool


class AgentOutput(BaseModel):
    agent_id: str
    metadata: Dict
