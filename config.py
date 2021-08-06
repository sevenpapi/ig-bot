import core.INTERNAL as INTERNAL

# ============= BROWSER  ============= #
local_debug = True
headless_debug = False # MUST be true in deployment; set to false to show browser GUI during local testing.

browser_mode = INTERNAL.WEBDRIVER_CHROME

# the environment variable names containing the paths to browser binaries and drivers
bin_path = "CHROME_BIN"
driver_path = "CHROMEDRIVER_PATH"

# bin paths for local testing
local_firefox_bin = r"C:\Program Files\Mozilla Firefox\firefox.exe"
local_chrome_bin = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# relative to current working directory
local_firefox_driver = "geckodriver.exe"
local_chrome_driver = "chromedriver.exe"

# instagram login credentials
bot_username = "bot_username"
bot_password = "bot_password"

# ============= CUSTOMIZE ============= #
# empty string = no prefix
# prefix can be any length, but can only consist of alphanumeric characters

command_prefix = '!'
admin_handles = ["your_handle", "another_admin's_handle"] # users that can run admin commands on the bot (i.e., turn on/off, toggle notifications, etc.)

target_channel = "name_of_channel"

default_timezone = "America/Toronto" # only valid for timezones in pytz.all_timezones

# must not be blank
startup_message = "hello :alien:"
run_message = "hi :alien:"
quit_message = "bye :alien:"
kill_message = "goodbye :alien:"

# ============== PLUGINS  ============== #
# remove the plugins you do not want from the list
plugins = [
    "default.weather",
]

# ===== CUSTOMIZE BUILTIN COMMANDS ===== #
builtin_commands = {
    INTERNAL.ON_HELP : 'help',
    INTERNAL.ON_EVERYONE : 'everyone',
}

# setting a value to None will remove the help description
help_defaults = {
    INTERNAL.ON_HELP : 'Show all commands',
    INTERNAL.ON_EVERYONE : '@ everyone in the chat'
}

admin_commands = {
    INTERNAL._DEACTIVATE : 'deactivate', # stop bot from running completely
    INTERNAL._QUIT: 'quit', # stop bot from listening to non-administrative messages
    INTERNAL._RUN: 'run' # start bot's message listener
}
