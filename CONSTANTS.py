# instagram login credentials
bot_username = "your_bot's_username"
bot_password = "your_bot's_password"

# ============= CUSTOMIZE ============= #
# empty string = no prefix
# prefix can be any length, but can only consist of alphanumeric characters
command_prefix = '!'
admin_handles = ["your_handle_here"] # users that can run admin commands on the bot (i.e., turn on/off, toggle notifications, etc.)

target_channel = "name"

# messages sent after connecting/disconnecting with the chat
startup_message = "hello :alien:"
quit_message = "goodbye :alien:"

# ===== CUSTOMIZE BUILTIN COMMANDS ===== #
# to change the command syntax, change the values to whatever (don't change the keys!).

builtin_commands = {
    'on_help': 'help',
}

admin_commands = {
    '_deactivate': 'quit'
}

# ============= INTERNAL ============== #
# don't modify anything beyond here.

instagram_home = "https://www.instagram.com/"
onetap_url = "https://www.instagram.com/accounts/onetap/"
dms_url = "https://www.instagram.com/direct/inbox/"
base_url = 'https://www.instagram.com/accounts/login/'

humanization_delay = 0.1

command_default_setting = {
    'use_prefix': True,
    'help_desc': None
}
