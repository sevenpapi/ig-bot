class BadWebdriverException(Exception):
    # webdriver other than chrome or firefox
    def __init__(self, attempted_driver_input):
        self.message = "Invalid webdriver in config.browser_mode: '" + str(attempted_driver_input) + "' is not a valid webdriver."
        super().__init__(self.message)

class BuiltinBadOverrideException(Exception):
    # When user tries to override a builtin function that does not exist
    def __init__(self, func):
        self.message = "No such builtin function '" + func.__name__ + "'."
        super().__init__(self.message)

class BuiltinCommandConflictException(Exception):
    # When user defines a command that conflicts with a builtin command
    def __init__(self, user_func):
        self.message = "Name of user defined command '" + user_func.__name__ + "' conflicts with a builtin command."
        super().__init__(self.message)

class BuiltinOverrideArgumentException(Exception):
    # When user tries to override a builtin function with wrong number of arguments
    def __init__(self, func):
        self.message = "Argument profile for '" + func.__name__ + "' does not match that of the corresponding builtin function."
        super().__init__(self.message)

class CommandParameterException(Exception):
    # When user defines a command with more than 1 argument
    def __init__(self, func):
        self.message = "User defined command '" + func.__name__ + "' takes in a number of arguments not equal to 1."
        super().__init__(self.message)

class DuplicateCommandException(Exception):
    # When user defines a command that conflicts with another user-defined command
    def __init__(self, func):
        self.message = "There are more than one user-defined commands with name '" + func.__name__ + "'."
        super().__init__(self.message)

class DuplicateGlobalCommandException(Exception):
    # When user defines a command that conflicts with another user-defined command
    def __init__(self, name):
        self.message = "Overlap of commands/togglecommands with name '" + name + "'."
        super().__init__(self.message)

class IntervalCommandArgumentException(Exception):
    # When an interval command is defined with a number of parameters other than 1 or 2
    def __init__(self, func):
        self.message = "User defined interval command '" + func.__name__ + "' takes in a number of arguments not equal to 1 or 2."
        super().__init__(self.message)

class KeywordArgumentException(Exception):
    # When user defines kwargs that are unexpected
    def __init__(self, func, kwarg, given_type, expected_type):
        self.message = "Keyword argument '" + kwarg + "' for user defined command '" + func.__name__ + "' expected type '" + expected_type + "' but recieved type '" + given_type + "'."
        super().__init__(self.message)

class NotificationArgumentException(Exception):
    # When a notification function has nonzero number of arguments
    def __init__(self, func):
        self.message = "User defined notification procedure '" + func.__name__ + "' takes in a non-zero number of arguments (expected 0)."
        super().__init__(self.message)

class PluginImportError(Exception):
    # When a plugin in config is not found
    def __init__(self, plugin_name):
        self.message = "A problem occured while importing plugin named '" + plugin_name + "'. Verify that all plugin names in 'config.plugins' are correct, and verify that there are no typos in the import lines within the plugin modules."
        super().__init__(self.message)

class PluginNameException(Exception):
    # When a plugin in config is not found
    def __init__(self, plugin_name):
        self.message = "A plugin was given with type " + str(type(plugin_name)) + ". Ensure that all plugins in the 'config.plugins' list are of type 'str'."
        super().__init__(self.message)
