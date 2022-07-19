# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import json

class PersistTerminalCommandHistoryPlugin(
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin
):
    def _get_file(self):
        return self.get_plugin_data_folder() + "/command_history.json"

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(persistedCmdHistory=[])

    def on_settings_save(self, data):
        with open(self._get_file(), "w") as outfile:
            json.dump(data, outfile)
    
    def on_settings_load(self):
        with open(self._get_file(), "r") as infile:
            data = json.load(infile)
            if data is not None:
                return data
            return self.get_settings_defaults()

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/persist_terminal_command_history.js"],
        }

    ##~~ Softwareupdate hook

    def get_update_information(self):
        return {
            "persist_terminal_command_history": {
                "displayName": "Persist Terminal Command History Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "nivekmai",
                "repo": "OctoPrint-PersistTerminalCommandHistory",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/nivekmai/OctoPrint-PersistTerminalCommandHistory/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Persist Terminal Command History Plugin"

__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PersistTerminalCommandHistoryPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
