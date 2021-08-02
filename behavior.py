from core.command_factory import override_default
from core.default_behavior import command_help_key

# uncomment below to override the default behavior of the [help] command ('!help' by default)
# @override_default
# def on_help(msg):
#     print(command_help_key)
#     return "Define custom behavior for builtin 'on_help' command here!"

# you can also completely disable builtin functions like so
# @override_default
# def on_help(msg):
#     return None
