from colorama import Fore, Back, Style
from datetime import datetime

SUCCESS = (Fore.GREEN, "SUCCESS")
WARNING = (Fore.YELLOW, "WARNING")
TIMEOUT = (Fore.RED, "TIMEOUT")
ERROR = (Back.RED, "ERROR")
TRIGGER = (Back.CYAN, "TRIGGER")
NOTIFICATION = (Back.GREEN, "NOTIFICATION")
NAVIGATION = (Fore.CYAN, "NAV")
ELEMENT_FIND = (Fore.CYAN, "ELEM_FIND")
START = (Fore.CYAN, "START")
QUIT = (Fore.LIGHTCYAN_EX, "QUIT")

def log(type, message):
    assert isinstance(type, tuple) and len(type) == 2
    color = type[0]
    msg_type = type[1]
    c_time = datetime.now()
    print(color + c_time.strftime("%m-%d-%Y %H:%M:%S") + ' [' + msg_type + '] : ' + message + Style.RESET_ALL)
