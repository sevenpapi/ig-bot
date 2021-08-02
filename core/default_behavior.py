import CONSTANTS

command_help_key = {}

def on_help(msg):
    def stringize(cmd, cmd_help):
        return "!" + cmd + " - " + cmd_help
    listraw = [stringize(x, command_help_key[x]) for x in command_help_key.keys() if command_help_key[x] is not None]
    listraw.append('\n' + stringize(CONSTANTS.builtin_commands['on_help'], "Show all commands"))
    c_list = "\n".join(listraw)
    return "Commands:\n\n" + c_list
