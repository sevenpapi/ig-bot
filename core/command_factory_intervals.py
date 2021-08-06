import inspect
from datetime import datetime, timedelta
from core.exceptions import IntervalCommandArgumentException, KeywordArgumentException

interval_commands = [] ## all interval commands

class IntervalCommand():
    def __init__(self, f_response, enabled, timedelta, toggle_command): # interval defined in seconds
        self.enabled = enabled
        self.ready = False
        self.f_response = f_response #function used to handle what the response is
        self.interval = timedelta
        self.next_call = datetime.now() + timedelta
        self.toggle_command = toggle_command

    def __str__(self):
        odict = {
            'ready': self.ready,
            'callable response': self.f_response.__name__,
            'interval': self.interval,
            'next_call': self.next_call,
        }
        return str(odict)

    def process_msg(self, msg):
        func_params = inspect.getfullargspec(self.f_response)
        param_len = len(func_params[0])
        if param_len == 1:
            return self.f_response(self)
        return self.f_response(self, msg)

    def on_check(self, msg):
        d_now = datetime.now()
        if d_now > self.next_call:
            diff = d_now - self.next_call
            if diff > self.interval:
                self.next_call += diff - (diff % self.interval)
            self.next_call += self.interval
            self.ready = self.enabled
        if self.ready and (ready_response := self.process_msg(msg)) is not None:
            self.ready = False
            return (ready_response, self)
        return None

def interval_command_factory(**kwargs):

    interval_command_default_setting = {
        'enabled': True,
        'interval': timedelta(minutes=5), #5 min
        'toggle_command': None
    }

    for k, v in interval_command_default_setting.items():
        kwargs.setdefault(k, v)

    def interval_cmd(func):
        assert callable(func)
        func_params = inspect.getfullargspec(func)
        param_len = len(func_params[0])
        if param_len != 1 and param_len != 2: # make sure takes in self object
            raise IntervalCommandArgumentException(func)

        exclude_kwarg_check = ['toggle_command']

        for arg in kwargs.keys():
            if not isinstance(interval_command_default_setting[arg], type(kwargs[arg])) and arg not in exclude_kwarg_check:
                giv = str(type(kwargs[arg]))
                exp = str(type(interval_command_default_setting[arg]))
                raise KeywordArgumentException(func, arg, giv, exp)

        interval_commands.append(IntervalCommand(func, kwargs['enabled'], kwargs['interval'], kwargs['toggle_command']))
        return func

    return interval_cmd

def on_loop_interval_check(msg):
    response_out = []
    for command in interval_commands:
        res = command.on_check(msg)
        if res is not None:
            response_out.append(res)
    return response_out
