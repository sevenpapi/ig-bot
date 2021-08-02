import inspect
import core.default_behavior as default_behavior
from CONSTANTS import command_default_setting, builtin_commands

prefixless_commands = []
builtin_command_key = {
    'on_help': default_behavior.on_help
}

for key, val in builtin_commands.items():
    assert key in builtin_command_key
    builtin_command_key[val] = builtin_command_key[key]

command_key = {} # tracks commands that use prefixes

def validate_cmd_function(func, arg_len):
    assert callable(func)
    func_params = inspect.getfullargspec(func)
    assert isinstance(arg_len, int)
    assert len(func_params[0]) == arg_len

def command_factory(**kwargs):

    for key, val in command_default_setting.items():
        kwargs.setdefault(key, val)

    def cmd(func):
        validate_cmd_function(func, 1)
        command_key[func.__name__] = func
        default_behavior.command_help_key[func.__name__] = kwargs["help_desc"]
        return func

    if kwargs["use_prefix"]:
        return cmd

    def cmd_prefixless(func):
        validate_cmd_function(func, 1)
        prefixless_commands.append(func)
        return func

    return cmd_prefixless

def override_default(func):
    assert callable(func)

    new_func_params = inspect.getfullargspec(func)
    try:
        old_func_params = inspect.getfullargspec(builtin_command_key[func.__name__])
    except KeyError:
        pass # does not override any default functions.
    assert len(new_func_params[0]) == len(old_func_params[0])

    builtin_command_key[func.__name__] = func
    return func
