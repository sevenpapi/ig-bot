import os
import core.INTERNAL as INTERNAL
from config import (browser_mode, local_debug, headless_debug, bin_path, driver_path,
    local_firefox_bin, local_firefox_driver,
    local_chrome_bin, local_chrome_driver)
from pathlib import Path
from selenium import webdriver
from core.exceptions import BadWebdriverException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

def get_webdriver():
    if browser_mode == INTERNAL.WEBDRIVER_FIREFOX:
        if local_debug:
            return get_geckodriver_options(
                exe_path=os.path.join(os.getcwd(), local_firefox_driver),
                bin_path=local_firefox_bin
            )
        return get_geckodriver_options(
            os.environ.get(driver_path),
            os.environ.get(bin_path)
        )
    elif browser_mode == INTERNAL.WEBDRIVER_CHROME:
        if local_debug:
            return get_chromedriver_options(
                exe_path=os.path.join(os.getcwd(), local_chrome_driver),
                bin_path=local_chrome_bin
            )
        return get_chromedriver_options(
            os.environ.get(driver_path),
            os.environ.get(bin_path)
        )
    raise BadWebdriverException(browser_mode)


def get_geckodriver_options(exe_path, bin_path):
    options = FirefoxOptions()
    options.headless = headless_debug
    options.binary_location = bin_path
    logpath = os.path.join(os.getcwd(), "logs/geckodriver.log")
    return webdriver.Firefox(options=options, executable_path=exe_path, log_path=logpath)

def get_chromedriver_options(exe_path, bin_path):
    options = ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    if headless_debug:
        options.add_argument("--headless");
    options.add_argument("--window-size=1920,1080")
    options.binary_location = bin_path
    driver_out = webdriver.Chrome(executable_path=exe_path, options=options, service_args=["--log-path=" + str(os.path.join(os.getcwd(), "logs/chromedriver.log"))])
    driver_out.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": INTERNAL.USER_AGENT_CHROME})
    return driver_out
