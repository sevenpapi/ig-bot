import inspect
from datetime import datetime, timedelta

notifications = []

class Notification():

    def __init__(self, func_run, first_run_datetime, delta_time, toggle_command):
        self.enabled = True
        self.func_run = func_run
        self.next_run_datetime = first_run_datetime
        self.delta_time = delta_time
        self.toggle_command = toggle_command

    def get_message_return(self, datetime_now):
        if datetime_now > self.next_run_datetime:
            diff = datetime_now - self.next_run_datetime
            if diff > self.delta_time:
                self.next_run_datetime += diff - (diff % self.delta_time)
            self.next_run_datetime += self.delta_time
            if self.enabled and diff < self.delta_time * 0.1:
                return self.func_run()
        return None

    def __str__(self):
        out = {
            "enabled": self.enabled,
            "func_run": self.func_run.__name__,
            "next_run_datetime": self.next_run_datetime,
            "delta_time": self.delta_time,
            "toggle_command": self.toggle_command
        }
        return str(out)

def on_loop_notif_check():
    notif_out = []
    c_time = datetime.now()
    for notif in notifications:
        notif_append = notif.get_message_return(c_time)
        if notif_append is not None:
            notif_out.append((notif_append, notif))
    return notif_out

def notification_factory(**kwargs):

    notification_default_setting = {
        'first_run': datetime.now() + timedelta(minutes=5),
        'delta': timedelta(hours=1),
        'toggle_command': None
    }

    for k, v in notification_default_setting.items():
        kwargs.setdefault(k, v)

    assert kwargs['toggle_command'] is not None

    def notification_cmd(func):
        assert callable(func)
        func_params = inspect.getfullargspec(func)
        assert len(func_params[0]) == 0

        notifications.append(Notification(func, kwargs['first_run'], kwargs['delta'], kwargs['toggle_command']))

        return func

    return notification_cmd
