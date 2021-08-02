import inspect

interval_commands = [] ## all interval commands

class IntervalCommand():
    def __init__(self, f_response, interval): # interval defined in seconds
        self.ready = False
        self.f_response = f_response #function used to handle what the response is
        self.interval = interval
        self.last_call = 0

    def __str__(self):
        odict = {
            'ready': self.ready,
            'callable response': self.f_response.__name__,
            'interval': self.interval,
            'last_call': self.last_call,
        }
        return str(odict)

def interval_command_factory(**kwargs):

    interval_command_default_setting = {
        'interval': 300 #5 min
    }

    def interval_cmd(func):
        assert callable(func)
        func_params = inspect.getfullargspec(func)
        param_len = len(func_params[0])
        assert param_len == 1 or param_len == 2 # make sure takes in self object

        for k, v in interval_command_default_setting.items():
            kwargs.setdefault(k, v)

        interval_commands.append(IntervalCommand(func, kwargs['interval']))
        return func

    return interval_cmd

def on_loop_interval_check(time, msg):
    response_out = []
    for command in interval_commands:
        if time % command.interval == 0 and command.last_call != time:
            command.ready = True

        if command.ready and (ready_response := process_msg(command, msg)) is not None:
            response_out.append(ready_response)
            print(command)
            command.ready = False
            command.last_call = time

    return response_out

def process_msg(cmd, msg):
    func_params = inspect.getfullargspec(cmd.f_response)
    param_len = len(func_params[0])
    if param_len == 1:
        return cmd.f_response(cmd)
    return cmd.f_response(cmd, msg)
