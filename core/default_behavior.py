import config

active_channel = None
command_help_key = {}

def on_help(msg):

    def stringize(cmd, cmd_help):
        return "!" + cmd + " - " + cmd_help

    cmd_list = [stringize(x, command_help_key[x]) for x in command_help_key.keys() if command_help_key[x] is not None]
    appendix_list = [stringize(config.builtin_commands[key], config.help_defaults[key]) for key in config.help_defaults.keys() if config.help_defaults[key] is not None]

    out_list = "\n".join(cmd_list + ['\n\n'] + appendix_list)
    return "Commands:\n\n" + out_list

def on_everyone(msg):
    out = ""
    for member in active_channel.members:
        if member != config.bot_username:
            out += "@" + member + " "
    return out
