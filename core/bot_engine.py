import CONSTANTS
import emoji
import commands # initialize custom commands
import behavior # initialize overridden behavior
from time import sleep
from threading import Thread
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from core.notifications import on_loop_notif_check, notifications
from core.message_class import Message
from core.command_parser import msg_parser
from core.command_factory_intervals import on_loop_interval_check
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

import logs.console as console

class Bot():

    def __init__(self, username, password):
        ex_path = str(Path(__file__).parent.joinpath('geckodriver.exe'))
        console.log(console.START, "Initializing instagram bot...")

        options = Options()
        options.headless = True

        logpath = str(Path(__file__).parent.parent.joinpath('logs').joinpath('geckodriver.log'))
        self.driver = webdriver.Firefox(options=options, executable_path=ex_path, log_path=logpath)
        self.wait = WebDriverWait(self.driver, 10)
        self.username = username
        self.password = password
        self.running = True
        self.elapsed = 0
        self.listener_delay = 0.5

    def initialize(self):
        self.driver.get(CONSTANTS.base_url)
        self.log_in()
        if not self.running: return
        self.dm_setup()
        if not self.running: return
        self.main_listener()

    def main_listener(self):

        msg_scroller_xpath = "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div"
        textarea_xpath = "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea"
        try:
            scroller_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, msg_scroller_xpath)))
            msg_textarea = self.wait.until(EC.presence_of_element_located((By.XPATH, textarea_xpath)))
        except TimeoutException:
            console.log(console.TIMEOUT, "Failed to find all necessary message box elements.")
            return

        def send_message(message):
            message = emoji.emojize(str(message))
            msgs_out = message.split('\n')

            for msg_line in msgs_out:
                msg_textarea.send_keys(msg_line)
                msg_textarea.send_keys(Keys.SHIFT, Keys.ENTER)
            msg_textarea.send_keys(Keys.RETURN)
            sleep(CONSTANTS.humanization_delay)

        console.log(console.TRIGGER, "Sending startup message '" + CONSTANTS.startup_message + "' to chat.")
        send_message(CONSTANTS.startup_message)

        last_sender = None

        time_thread = Thread(target = self.timer_thread)
        time_thread.setDaemon(True)
        time_thread.start()
        while self.running:
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroller_elem)
            recent_msg = self.get_recent_message(last_sender)

            if recent_msg.sender != last_sender:
                last_sender = recent_msg.sender

            is_sender_admin = recent_msg.sender in CONSTANTS.admin_handles
            is_message_deactivate = recent_msg.content == str(CONSTANTS.command_prefix) + CONSTANTS.admin_commands['_deactivate']
            self.running = not (is_sender_admin and is_message_deactivate)

            if last_sender is not None:
                if (response := msg_parser(recent_msg)) is not None:
                    console.log(console.TRIGGER, "Bot response triggered by " + last_sender + ". Sending message '" + response + "'.")
                    send_message(response)

                if is_sender_admin:
                    for n in notifications:
                        if recent_msg.content == str(CONSTANTS.command_prefix) + str(n.toggle_command):
                            n.enabled = not n.enabled
                            s_res = "Toggled notification '" + n.func_run.__name__ + "'. Re-enable with '" + str(CONSTANTS.command_prefix) + n.toggle_command + "'. "
                            console.log(console.WARNING, s_res + "Details: " + str(n))
                            send_message(s_res)

            intervaled_messages = on_loop_interval_check(self.elapsed, recent_msg)
            notification_messages = on_loop_notif_check()

            for message in intervaled_messages:
                console.log(console.TRIGGER, "Sending interval message. Content: '" + message + "'.")
                send_message(message)

            for notif in notification_messages:
                notification_body = notif[0]
                notification_obj = notif[1]
                console.log(console.NOTIFICATION, "Sending notification '" + notification_body + "'. Details: " + str(notification_obj))
                send_message(notification_body)

            sleep(self.listener_delay)

        send_message(CONSTANTS.quit_message)
        console.log(console.QUIT, "Bot has been terminated by administrator.")
        self.quit()

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


    def get_raw_msgs(self):
        message_elems_xpath = "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div"
        try:
            message_elems = self.wait.until(EC.presence_of_element_located((By.XPATH, message_elems_xpath)))
        except TimeoutException:
            console.log(console.TIMEOUT, "Failed to find message collection element.")
            return None
        return message_elems.get_attribute("innerHTML")

    def dm_setup(self):
        self.driver.get(CONSTANTS.dms_url)
        self.clear_notifs()

        first_dm_link_xpath = "/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[2]/div/div/div/div/div[1]/a"
        try: #validate existence of at least 1 dm channel
            self.wait.until(EC.presence_of_element_located((By.XPATH, first_dm_link_xpath)))
        except TimeoutException:
            console.log(console.TIMEOUT, "Failed to find any dm channel.")
            return

        dm_column_xpath = "/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[2]/div/div/div/div"
        dm_column = self.wait.until(EC.presence_of_element_located((By.XPATH, dm_column_xpath)))
        dm_channels_elements = dm_column.find_elements_by_xpath("./*")

        targ_channel = CONSTANTS.target_channel
        for channel in dm_channels_elements:
            try:
                channel_name = None
                try:
                    channel_name = channel.find_element_by_xpath(".//a/div/div[2]/div[1]/div/div/div/div").text.strip()
                except NoSuchElementException:
                    channel_name = channel.find_element_by_xpath(".//a/div/div[2]/div/div/div/div/div").text.strip()

                if channel_name == targ_channel:
                    channel_button = channel.find_element_by_xpath(".//a")
                    channel_button.click()
                    console.log(console.SUCCESS, "Successfully connected to DM channel '" + str(channel_name) + "'.")
                    return
            except NoSuchElementException:
                console.log(console.ERROR, "No channel names matched that of the target channel. Check for typos and/or try again.")
                self.quit()
                return


    def log_in(self):

        username_input_box_xpath = "/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input"
        password_input_box_xpath = "/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[2]/div/label/input"
        login_button_xpath = "/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button"

        try:
            console.log(console.ELEMENT_FIND, "Attempting login to account '" + self.username + "'.")
            username_input_box = self.wait.until(EC.presence_of_element_located((By.XPATH, username_input_box_xpath)))
            password_input_box = self.wait.until(EC.presence_of_element_located((By.XPATH, password_input_box_xpath)))
        except TimeoutException:
            console.log(console.TIMEOUT, "Unable to locate login textareas.")
            self.quit()
            return

        username_input_box.send_keys(self.username)
        password_input_box.send_keys(self.password)

        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath)))
        login_button.click()

        try:
            self.wait.until(lambda driver: self.driver.current_url != CONSTANTS.base_url)
            console.log(console.SUCCESS, "Logged in to " + str(self.username))
        except TimeoutException:
            is_rate_limited = False #implement this
            if is_rate_limited:
                console.log(console.ERROR, "Rate limited by instagram. Try again in a few minutes.")
            else:
                console.log(console.ERROR, "Failed to log in to instagram. Check your login credentials and try again.")
            self.quit()

        self.clear_notifs()

    def clear_notifs(self):
        targ_class = "HoLwm"
        try:
            not_now_button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, targ_class)))
            not_now_button.click()
            return
        except TimeoutException:
            console.log(console.WARNING, "Notifications were not found.")

    def timer_thread(self):
        while self.running:
            self.elapsed += 1
            sleep(1)

    def quit(self):
        self.running = False
        self.driver.quit()
