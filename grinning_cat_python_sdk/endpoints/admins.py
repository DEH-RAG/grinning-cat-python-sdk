from grinning_cat_python_sdk.endpoints.base import AbstractEndpoint, MultipartPayload
from grinning_cat_python_sdk.models.api.admins import (
    PluginInstallOutput,
    PluginInstallFromRegistryOutput,
    PluginDetailsOutput,
    PluginDeleteOutput,
)
from grinning_cat_python_sdk.models.api.nested.plugins import PluginSettingsOutput
from grinning_cat_python_sdk.models.api.plugins import PluginCollectionOutput, PluginsSettingsOutput, PluginToggleOutput
from grinning_cat_python_sdk.utils import file_attributes


class AdminsEndpoint(AbstractEndpoint):
    def __init__(self, client: "GrinningCatClient"):
        super().__init__(client)
        self.prefix = "/plugins"

    def get_available_plugins(self, plugin_name: str | None = None) -> PluginCollectionOutput:
        """
        Get a list of all available plugins.
        :param plugin_name: The name of the plugin.
        :return: PluginCollectionOutput, the details of the plugins.
        """
        return self.get(
            self.format_url("/installed"),
            self.system_id,
            output_class=PluginCollectionOutput,
            query={"query": plugin_name} if plugin_name else None,
        )

    def post_install_plugin_from_zip(self, path_zip: str) -> PluginInstallOutput:
        payload = MultipartPayload()

        with open(path_zip, "rb") as file:
            payload.files = [("file", file_attributes(path_zip, file))]
            result = self.post_multipart(
                self.format_url("/install/upload"),
                self.system_id,
                output_class=PluginInstallOutput,
                payload=payload,
            )
        return result

    def post_install_plugin_from_registry(self, url: str) -> PluginInstallFromRegistryOutput:
        """
        Install a new plugin from a registry. The plugin is installed asynchronously.
        :param url: The URL of the plugin.
        :return: PluginInstallFromRegistryOutput, the details of the installation.
        """
        return self.post_json(
            self.format_url("/install/registry"),
            self.system_id,
            output_class=PluginInstallFromRegistryOutput,
            payload={"url": url},
        )

    def get_plugins_settings(self) -> PluginsSettingsOutput:
        """
        Get the default settings of all the plugins.

        The system-level plugin settings routes moved into the ``mgmt_message``
        plugin (GET ``/mgmt_message/settings``, SYSTEM READ): the list is served
        as a single-entry ``PluginsSettingsOutput`` for backward compatibility.

        :return: PluginsSettingsOutput, the details of the settings.
        """
        entry = self.get("/mgmt_message/settings", self.system_id, output_class=PluginSettingsOutput)
        return PluginsSettingsOutput(settings=[entry.model_dump()])

    def get_plugin_settings(self, plugin_id: str) -> PluginSettingsOutput:
        """
        Get the default settings of a specific plugin.

        The system-level plugin settings routes moved into the ``mgmt_message``
        plugin; the read now goes to GET ``/mgmt_message/settings`` (SYSTEM
        READ), so this method serves the global ``mgmt_message`` settings
        regardless of ``plugin_id`` (kept for signature compatibility).

        :param plugin_id: The ID of the plugin (unused, kept for compatibility).
        :return: PluginSettingsOutput, the details of the settings.
        """
        return self.get("/mgmt_message/settings", self.system_id, output_class=PluginSettingsOutput)

    def get_plugin_details(self, plugin_id: str) -> PluginDetailsOutput:
        """
        Get the details of a specific plugin.
        :param plugin_id: The ID of the plugin.
        :return: PluginDetailsOutput, the details of the plugin.
        """
        return self.get(self.format_url(f"/system/details/{plugin_id}"), self.system_id, output_class=PluginDetailsOutput)

    def delete_plugin(self, plugin_id: str) -> PluginDeleteOutput:
        """
        Delete a specific plugin.
        :param plugin_id: The ID of the plugin.
        :return: PluginDeleteOutput, the details of the plugin.
        """
        return self.delete(self.format_url(f"/uninstall/{plugin_id}"), self.system_id, output_class=PluginDeleteOutput)

    def put_toggle_plugin(self, plugin_id: str) -> PluginToggleOutput:
        """
        This endpoint toggles a plugin, on a system level
        :param plugin_id: The id of the plugin to toggle
        :return: PluginToggleOutput, the toggled plugin
        """
        return self.put(
            self.format_url(f"/system/toggle/{plugin_id}"),
            self.system_id,
            output_class=PluginToggleOutput,
        )
