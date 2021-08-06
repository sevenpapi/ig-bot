import config
import emoji
import core.default_behavior as default_behavior
import core.admin_util as admin_util
from bs4 import BeautifulSoup
from time import sleep
from core.INTERNAL import HUMANIZATION_DELAY, WEBDRIVER_CHROME, WEBDRIVER_FIREFOX
from core.chat_class import Chat
from core.chrome_util import chrome_send_text_to_elem
from core.message_class import Message
from core.command_parser import msg_parser, prefixless_parser
from core.webdriver_util import get_webdriver
from core.notification_factory import on_loop_notif_check, notifications
from core.command_factory_intervals import on_loop_interval_check, interval_commands
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import logs.console as console

dms_url = "https://www.instagram.com/direct/inbox/"
base_url = 'https://www.instagram.com/accounts/login/'

def ensure_running(func):
    def f_ensure(self):
        if self.enabled:
            return func(self)
        console.log(console.WARNING, "Quit prematurely. Skipping process '" + func.__name__ + "'.")
    return f_ensure

def await_timeout(on_timeout, on_noelement):
    def dec_f(func):
        def wait_f(self):
            unhandler_handler = lambda x : ("Unhandled exception at " + func.__name__ if x == "" else x)
            on_timeout_p = unhandler_handler(on_timeout)
            on_noelement_p = unhandler_handler(on_noelement)
            try:
                func(self)
                return
            except TimeoutException:
                console.log(console.TIMEOUT, on_timeout_p)
            except NoSuchElementException:
                console.log(console.TIMEOUT, on_noelement_p)
            self.quit()
        return wait_f
    return dec_f

class Bot():
    # f
    def __init__(self):
        console.log(console.START, "Initializing instagram bot.")
        self.driver = None
        self.username = config.bot_username
        self.password = config.bot_password
        self.enabled = True
        self.running = False
        self.msg_textarea = None
        self.scroller_element = None
        self.listener_delay = 0.25

    def driver_init(self):
        console.log(console.START, "Setting webdriver...")
        self.driver = get_webdriver()
        console.log(console.NAVIGATION, "Verify user agent: " + str(self.driver.execute_script("return navigator.userAgent;")))
        console.log(console.SUCCESS, "Webdriver set.")
        self.wait = WebDriverWait(self.driver, 10)
        console.log(console.SUCCESS, "Startup success.")

    def initialize(self):
        self.log_in()
        self.assert_login()
        self.dm_setup()
        self.open_chat_details()
        self.parse_chat_details()
        self.close_chat_details()
        self.locate_message_text_area()
        self.locate_message_scroller()

    def send_message(self, message):
        if self.msg_textarea is not None:
            message = emoji.emojize(str(message))
            msgs_out = message.split('\n')

            for msg_line in msgs_out:
                if config.browser_mode == WEBDRIVER_FIREFOX:
                    self.msg_textarea.send_keys(msg_line)
                    self.msg_textarea.send_keys(Keys.SHIFT, Keys.ENTER)
                elif config.browser_mode == WEBDRIVER_CHROME: #no support for emojis
                    chrome_send_text_to_elem(self, msg_line)
                    self.msg_textarea.send_keys(Keys.SHIFT, Keys.ENTER)
            self.msg_textarea.send_keys(Keys.RETURN),
            sleep(HUMANIZATION_DELAY)
        else:
            console.log(console.ERROR, "Target textarea is None.")
            self.quit()

    @ensure_running
    @await_timeout("Login error. Failed to locate login textarea elements.", "Login error. Failed to locate login textarea elements within form.")
    def login_fill_input(self):
        # form_class = "HmktE"
        form_class = "EPjEi"
        input_class = "_2hvTZ"

        console.log(console.ELEMENT_FIND, "Attempting login to account '" + self.username + "'.")
        form = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, form_class)))
        input_boxes = form.find_elements_by_class_name(input_class)
        if len(input_boxes) < 2:
            raise NoSuchElementException()
        username_input_box = input_boxes[0]
        password_input_box = input_boxes[1]

        username_input_box.send_keys(self.username)
        password_input_box.send_keys(self.password)
        console.log(console.SUCCESS, "Keys entered into login boxes.")

    @ensure_running
    @await_timeout("Login error. Failed to submit login info elements.", "")
    def login_hit_submit(self):
        console.log(console.ELEMENT_FIND, "Attempting to submit login credentials for '" + self.username + "'.")
        login_button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "L3NKy")))
        login_button.click()
        console.log(console.SUCCESS, "Submitted login credentials.")

    @ensure_running
    @await_timeout("Login error: could not get login failure reason. Try again later.", "")
    def find_error(self):
        error_alert = self.wait.until(EC.presence_of_element_located((By.ID, "slfErrorAlert")))
        console.log(console.ERROR, "Login error: '" + error_alert.text + "'")
        self.quit()

    @ensure_running
    @await_timeout("Failed to locate chat details button.", "")
    def open_chat_details(self):
        console.log(console.ELEMENT_FIND, "Attempting to locate chat details button...")
        details_div = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "PjuAP")))
        console.log(console.SUCCESS, "Details button found.")
        details_button = details_div.find_element_by_class_name("wpO6b")
        details_button.click()
        console.log(console.NAVIGATION, "Clicked details button. Navigating to users list.")

    @ensure_running
    @await_timeout("Unable to collect chat data.", "Unable to collect chat data.")
    def parse_chat_details(self):
        console.log(console.ELEMENT_FIND, "Attempting to collect user data for target chat...")
        console.log(console.ELEMENT_FIND, "Attempting to find user data <div> element...")
        user_list_bigdiv = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_9XapR")))
        console.log(console.SUCCESS, "User data found.")
        console.log(console.ELEMENT_FIND, "Parsing for member names...")
        members_list = user_list_bigdiv.find_elements_by_class_name("-qQT3")
        members_names = [m.find_element_by_class_name("qyrsm").text for m in members_list]
        default_behavior.active_channel = Chat(config.target_channel, members_names)
        console.log(console.SUCCESS, "Successfully collected data on chat: " + str(default_behavior.active_channel) + ".")

    @ensure_running
    @await_timeout("Failed to close user detail list div element.", "")
    def close_chat_details(self):
        console.log(console.ELEMENT_FIND, "Attempting to find exit button for user data <div> element...")
        details_div = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Eyjts")))
        console.log(console.SUCCESS, "Exit button div located successfully.")
        console.log(console.ELEMENT_FIND, "Attempting to find button element.")
        details_button = details_div.find_element_by_class_name("ZQScA")
        console.log(console.SUCCESS, "Exit button located successfully.")
        details_button.click()
        console.log(console.SUCCESS, "Exit button clicked successfully.")

    @ensure_running
    @await_timeout("Failed to locate message textarea element.", "Failed to locate message textarea element.")
    def locate_message_text_area(self):
        console.log(console.ELEMENT_FIND, "Attempting to find message textbox <div>...")
        textarea_raw = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "X3a-9")))
        console.log(console.SUCCESS, "Found message textbox <div>.")
        console.log(console.ELEMENT_FIND, "Attempting to find message textbox element...")
        self.msg_textarea = textarea_raw.find_element_by_tag_name("textarea")
        console.log(console.SUCCESS, "Found message textbox.")

    @ensure_running
    def locate_message_scroller(self):
        try:
            scr_tmp = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "frMpI")))
            self.scroller_element = scr_tmp
        except TimeoutException:
            console.log(console.TIMEOUT, "Failed to find scroller element for messages.")
            self.quit()

    @ensure_running
    def main_listener(self):
        last_sender = None
        console.log(console.TRIGGER, "Sending startup message '" + config.startup_message + "' to chat.")
        self.send_message(config.startup_message)

        while self.enabled:
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", self.scroller_element)
            last_sender = self.listen(last_sender)
            sleep(self.listener_delay)

        console.log(console.QUIT, "Bot has been terminated by administrator.")

    def listen(self, last_sender):
        recent_msg = self.get_recent_message(last_sender)
        if recent_msg.sender != last_sender:
            last_sender = recent_msg.sender

        if last_sender in config.admin_handles:
            admin_util.listen_admin(self, recent_msg, notifications, interval_commands)

        if self.running and self.enabled:
            if last_sender is not None:
                self.listen_while_run(recent_msg)
            self.listen_periodic(recent_msg)
        return last_sender

    def listen_while_run(self, recent_msg):
        def generic_send(response):
            console.log(console.TRIGGER, "Bot response triggered by @" + recent_msg.sender + ". Sending message '" + response + "'.")
            self.send_message(response)

        if (response := msg_parser(recent_msg)) is not None:
            generic_send(response)
        else:
            for response in prefixless_parser(recent_msg):
                generic_send(response)

    def listen_periodic(self, recent_msg):
        intervaled_messages = on_loop_interval_check(recent_msg)
        notification_messages = on_loop_notif_check()

        for message in intervaled_messages:
            console.log(console.TRIGGER, "Sending interval message. Content: '" + message[0] + "'. Details: " + str(message[1]))
            self.send_message(message[0])

        for notif in notification_messages:
            console.log(console.NOTIFICATION, "Sending notification '" + notif[0] + "'. Details: " + str(notif[1]))
            self.send_message(notif[0])

    def get_recent_message(self, last_known_sender):
        msg_soup = BeautifulSoup(self.get_raw_msgs(), 'html.parser')
        outer_divs = msg_soup.findAll('div', class_=["_7UhW9", "JRTzd"])
        if len(outer_divs) > 0 and outer_divs[-1].text.strip() == "Typing...":
            outer_divs.pop()

        filtered_msgs = [div for div in outer_divs if "uL8Hv" not in div["class"] and "KV-D4" not in div["class"]]
        if len(filtered_msgs) < 2: #no messages exist
            return None

        recent_body = filtered_msgs[-1]
        if "VdURK" in recent_body["class"]: #own message
            return Message(None, recent_body.text)

        recent_sender = filtered_msgs[-2]
        if "PIoXz" in recent_sender["class"]:
            last_known_sender = recent_sender.text

        return Message(last_known_sender, recent_body.text)

    @ensure_running
    def get_raw_msgs(self):
        message_elems_xpath = "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div"
        try:
            message_elems = self.wait.until(EC.presence_of_element_located((By.XPATH, message_elems_xpath)))
        except TimeoutException:
            console.log(console.TIMEOUT, "Failed to find message collection element.")
            return None
        return message_elems.get_attribute("innerHTML")

    def assert_dm_channel_presence(self, a_class):
        #assert presence of at least 1 dm channel
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, a_class)))
            return True
        except TimeoutException:
            console.log(console.TIMEOUT, "Failed to find any dm channel.")
            self.quit()
            return False

    def find_channel_elems(self, a_class):
        try:
            dm_column = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "N9abW")))
            dm_channels_elements = dm_column.find_elements_by_class_name(a_class)
            if len(dm_channels_elements) == 0:
                raise NoSuchElementException()
            return dm_channels_elements
        except TimeoutException:
            console.log(console.TIMEOUT, "Failed to find DM column.")
        except NoSuchElementException:
            console.log(console.TIMEOUT, "Failed to find DM channel elements.")
        return None

    @ensure_running
    def dm_setup(self):
        self.driver.get(dms_url)
        self.clear_notifs()
        a_class = "-qQT3"
        if self.assert_dm_channel_presence(a_class) and isinstance((dm_channels_elements := self.find_channel_elems(a_class)), list):
            for channel in dm_channels_elements:
                if self.parse_channel(channel):
                    return

    def parse_channel(self, channel):
        try:
            channel_name = None
            channel_name = channel.find_elements_by_class_name("_7UhW9")
            if len(channel_name) == 0:
                raise NoSuchElementException()

            channel_name = channel_name[0].text
            if channel_name == config.target_channel:
                channel.click()
                console.log(console.SUCCESS, "Successfully connected to DM channel '" + str(channel_name) + "'.")
                return True
        except NoSuchElementException:
            console.log(console.ERROR, "No channel names matched that of the target channel. Check for typos and/or try again.")
            self.quit()
        return False

    @ensure_running
    def log_in(self):
        console.log(console.NAVIGATION, "Navigating to login page.")
        self.driver.get(base_url)
        self.login_fill_input()
        self.login_hit_submit()

    @ensure_running
    def assert_login(self):
        try:
            self.wait.until(lambda driver: self.driver.current_url != base_url)
            console.log(console.SUCCESS, "Logged in to " + str(self.username))
        except TimeoutException:
            console.log(console.WARNING, "Failed to log in to instagram. Attempting to check if you have been rate limited...")
            self.find_error()

    @ensure_running
    def clear_notifs(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "HoLwm"))).click()
        except TimeoutException:
            console.log(console.WARNING, "No notification popup found at " + self.driver.current_url)

    def quit(self):
        console.log(console.QUIT, "Attempting to quit...")
        if self.driver == None:
            console.log(console.QUIT, "Skipping quit procedure (quit() called before webdriver was initialized).")
            return
        if self.enabled:
            self.enabled = False
            console.log(console.QUIT, "Quit at URL = " + self.driver.current_url)
            console.log(console.QUIT, "Closing driver.")
            self.driver.quit()
            console.log(console.QUIT, "Quit successfully.")
        else:
            console.log(console.WARNING, "'quit()' was called more than once.")
