/*
 * View model for OctoPrint-PersistTerminalCommandHistory
 *
 * Author: Kevin Christensen
 * License: AGPLv3
 */
$(function () {
    function PersistTerminalCommandHistory(parameters) {
        var self = this;
        var LOG_TAG = "OctoPrint-PersistTerminalCommandHistory";

        self.settingsViewModel = parameters[0];
        self.terminalViewModel = parameters[1];
        self.onBeforeBinding = function () {
            if (self.settingsViewModel.settings.plugins.persist_terminal_command_history) {
                self.terminalViewModel.cmdHistory = self.settingsViewModel.settings.plugins.persist_terminal_command_history.persistedCmdHistory();
                self.terminalViewModel.cmdHistoryIdx = self.terminalViewModel.cmdHistory.length;
                self._log('history set', self.terminalViewModel.cmdHistory);
            } else {
                self._warn('history does not exist');
            }
        }

        self.onAllBound = function () {
            self.oldVal = '';
            // Wait for terminal to set `command` to empty, since that means a command was sent
            self.terminalViewModel.command.subscribe(function (nextVal) {
                self._log("command", nextVal);
                if (self.oldVal != '' && nextVal == '') {
                    self._saveHistory();
                }
                self.oldVal = nextVal;
            });

        }

        self._saveHistory = function () {
            self._log("saving history", self.terminalViewModel.cmdHistory);
            OctoPrint.settings.savePluginSettings(
                'persist_terminal_command_history', 
                { 
                    'persistedCmdHistory': self.terminalViewModel.cmdHistory 
                });
        }

        self._log = function (...logs) {
            console.debug(LOG_TAG, ...logs);
        }
        self._warn = function (...warnings) {
            console.warn(LOG_TAG, ...warnings);
        }
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: PersistTerminalCommandHistory,
        dependencies: ["settingsViewModel", "terminalViewModel"],
        elements: []
    });

});
