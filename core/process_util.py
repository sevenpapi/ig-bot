import colorama
import importlib
import logs.console as console
from config import plugins, local_debug
from core.exceptions import PluginImportError, PluginNameException, DuplicateGlobalCommandException
from core.bot_engine import Bot

import commands # initialize custom commands
import behavior # initialize overridden behavior

# check for duplicate commands
from core.notification_factory import notifications
from core.command_factory_intervals import interval_commands
from core.command_factory import command_key, builtin_command_key

for plugin in plugins:
    try:
        if not isinstance(plugin, str):
            raise PluginNameException(plugin)
        plugin_name = "plugins." + plugin
        importlib.import_module(plugin_name)
    except ModuleNotFoundError:
        raise PluginImportError(plugin_name)

all_commands = ([n.toggle_command for n in notifications] +
               [i.toggle_command for i in interval_commands] +
               [k for k in command_key.keys()] + [k for k in builtin_command_key.keys()])

while len(all_commands) > 0:
    c_cmd = all_commands.pop()
    if c_cmd in all_commands:
        raise DuplicateGlobalCommandException(c_cmd)

def run():
    colorama.init()
    bot = Bot()
    try:
        bot.driver_init()
        bot.initialize()
        bot.main_listener()
        bot.quit()
    except KeyboardInterrupt:
        console.log(console.WARNING, "KeyboardInterrupt; quitting application.")
        bot.quit()
    colorama.deinit()
