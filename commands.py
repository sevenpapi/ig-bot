from core.command_factory import command_factory
from core.command_factory_intervals import interval_command_factory #todo: rework to use datetime.timedelta
from core.notifications import notification_factory

from datetime import datetime, timedelta
# bot will respond with the returned value
# return None --> no response from the bot

# use the @command_factory decorator to define custom commands
@command_factory(help_desc="This will show up as the description when '!help' is used.")
def test(msg):
    return "This is the response message to '!test'."

@command_factory()
def test2(msg):
    return "This is the response message to '!test2'. This has no description for '!help', so it won't show up."

# you can also define behavior for what happens for general messages that ARE NOT prefixed
@command_factory(use_prefix=False)
def poob(msg):
    if "poob" in msg.content:
        return "This will be the response to ALL messages containing the string 'poob'."
    return None # If the message does not contain 'poob', then there will be no reply.

# notification runs for the first time at [first_run],
# and runs again at an interval of [delta].
# if first_run is before the current time,
# it will just run at the most recent time
# it was supposed to, given delta.
# toggle whether it runs using [CONSTANTS.command_prefix][toggle_command]
# ('!toggleme' by default in this example)
@notification_factory(
    first_run=datetime(2021, 8, 1, hour=17, minute=48, second=30),
    delta=timedelta(hours=1),
    toggle_command='toggleme'
)
def my_notification():
    return "This will be sent every hour!"

# upon returning a non-None value, the function will
# not be called again until [interval] seconds later.
# good for sparingly-used comedic interjections in response
# to a specific sender or message content.
@interval_command_factory(interval=10)
def interval_test(self, msg):
    if msg.sender == 'joebob':
        return "Hello Joebob!"
    return None
