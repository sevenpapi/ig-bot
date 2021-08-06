import inspect
import core.INTERNAL as INTERNAL
import core.default_behavior as default_behavior
from core.exceptions import (BuiltinBadOverrideException,
BuiltinCommandConflictException,
BuiltinOverrideArgumentException,
CommandParameterException,
DuplicateCommandException,
KeywordArgumentException)
from config import builtin_commands

prefixless_commands = []
builtin_command_key = {
    INTERNAL.ON_HELP : default_behavior.on_help,
    INTERNAL.ON_EVERYONE : default_behavior.on_everyone
}

for key, val in builtin_commands.items():
    assert key in builtin_command_key
    builtin_command_key[val] = builtin_command_key[key]
    del builtin_command_key[key]

command_key = {} # tracks commands that use prefixes

def validate_cmd_function(func):
    assert callable(func)
    func_params = inspect.getfullargspec(func)
    if func.__name__ in command_key:
        raise DuplicateCommandException(func)
    if len(func_params[0]) != 1:
        raise CommandParameterException(func)
    if func.__name__ in builtin_command_key:
        raise BuiltinCommandConflictException(func)

def command_factory(**kwargs):

    command_default_setting = {
        'use_prefix': True,
        'help_desc': None
    }

    for key, val in command_default_setting.items():
        kwargs.setdefault(key, val)

    def validate_kwargs(func):
        exclude_kwarg_check = ['help_desc']
        for arg in kwargs.keys():
            if not isinstance(command_default_setting[arg], type(kwargs[arg])) and arg not in exclude_kwarg_check:
                giv = str(type(kwargs[arg]))
                exp = str(type(command_default_setting[arg]))
                raise KeywordArgumentException(func, arg, giv, exp)

    def cmd(func):
        validate_cmd_function(func)
        validate_kwargs(func)
        command_key[func.__name__] = func
        default_behavior.command_help_key[func.__name__] = kwargs["help_desc"]
        return func

    if kwargs["use_prefix"]:
        return cmd

    def cmd_prefixless(func):
        validate_cmd_function(func)
        validate_kwargs(func)
        prefixless_commands.append(func)
        return func

    return cmd_prefixless

def override_default(func):
    assert callable(func)

    new_func_params = inspect.getfullargspec(func)
    try:
        old_func_params = inspect.getfullargspec(builtin_command_key[func.__name__])
    except KeyError:
        raise BuiltinBadOverrideException(func)
    if len(new_func_params[0]) != len(old_func_params[0]):
        raise BuiltinOverrideArgumentException(func)

    builtin_command_key[func.__name__] = func
    return func
