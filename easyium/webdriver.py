from selenium.webdriver import Ie, Firefox, Chrome, Opera, Safari, PhantomJS
from selenium.common.exceptions import NoAlertPresentException

from context import Context
from exceptions import UnsupportedWebDriverTypeException
from waits.waiter import wait_for
from config import DEFAULT, default_page_load_timeout, default_script_timeout, default_wait_element_interval, \
    default_wait_element_timeout

__author__ = 'karl.gong'


class WebDriverType:
    IE = "ie"
    FIREFOX = "firefox"
    CHROME = "chrome"
    OPERA = "opera"
    SAFARI = "safari"
    PHANTOMJS = "phantomjs"
    ANDROID = "android"
    IOS = "ios"

    _BROWSER = [IE, FIREFOX, CHROME, OPERA, SAFARI, PHANTOMJS]
    _MOBILE = [ANDROID, IOS]
    _ALL = _BROWSER + _MOBILE


class WebDriver(Context):
    def __init__(self, web_driver_type=WebDriverType.CHROME, page_load_timeout=DEFAULT, script_timeout=DEFAULT,
                 wait_element_interval=DEFAULT, wait_element_timeout=DEFAULT, **kwargs):
        Context.__init__(self)
        self.__web_driver_type = web_driver_type.lower()
        if self.__web_driver_type == WebDriverType.IE:
            self.__web_driver = Ie(**kwargs)
        elif self.__web_driver_type == WebDriverType.FIREFOX:
            self.__web_driver = Firefox(**kwargs)
        elif self.__web_driver_type == WebDriverType.CHROME:
            self.__web_driver = Chrome(**kwargs)
        elif self.__web_driver_type == WebDriverType.OPERA:
            self.__web_driver = Opera(**kwargs)
        elif self.__web_driver_type == WebDriverType.SAFARI:
            self.__web_driver = Safari(**kwargs)
        elif self.__web_driver_type == WebDriverType.PHANTOMJS:
            self.__web_driver = PhantomJS(**kwargs)
        elif self.__web_driver_type in WebDriverType._MOBILE:
            from appium.webdriver.webdriver import WebDriver as Mobile
            self.__web_driver = Mobile(**kwargs)
        else:
            raise UnsupportedWebDriverTypeException("The web driver type [%s] is not supported." % web_driver_type)
        self.set_page_load_timeout(default_page_load_timeout if page_load_timeout == DEFAULT else page_load_timeout)
        self.set_script_timeout(default_script_timeout if script_timeout == DEFAULT else script_timeout)
        self.wait_element_interval = default_wait_element_interval if wait_element_interval == DEFAULT else wait_element_interval
        self.wait_element_timeout = default_wait_element_timeout if wait_element_timeout == DEFAULT else wait_element_timeout

    def _web_driver(self):
        return self.__web_driver

    def _selenium_context(self):
        return self.__web_driver

    def get_web_driver(self):
        return self

    def get_web_driver_type(self):
        return self.__web_driver_type

    def before_startup(self, method):
        self.__web_driver.start_client = method

    def after_shutdown(self, method):
        self.__web_driver.stop_client = method

    def start_session(self, desired_capabilities, profile=None):
        self.__web_driver.start_session(desired_capabilities, profile)

    def maximize_window(self):
        self.__web_driver.maximize_window()

    def set_page_load_timeout(self, timeout):
        self.__web_driver.set_page_load_timeout(timeout / 1000.0)

    def set_script_timeout(self, timeout):
        self.__web_driver.set_script_timeout(timeout / 1000.0)

    def execute_script(self, script, *args):
        return self.__web_driver.execute_script(script, *args)

    def execute_async_script(self, script, *args):
        return self.__web_driver.execute_async_script(script, *args)

    def open(self, url):
        self.__web_driver.get(url)

    def get_title(self):
        return self.__web_driver.title

    def refresh(self):
        self.__web_driver.refresh()

    def back(self):
        self.__web_driver.back()

    def forward(self):
        self.__web_driver.forward()

    def quit(self):
        self.__web_driver.quit()

    def get_current_url(self):
        return self.__web_driver.current_url

    def get_page_source(self):
        return self.__web_driver.page_source

    def switch_to_frame(self, frame_reference):
        self.__web_driver.switch_to.frame(frame_reference)

    def switch_to_parent_frame(self):
        self.__web_driver.switch_to.parent_frame()

    def switch_to_default_content(self):
        self.__web_driver.switch_to.default_content()

    def get_alert(self):
        return self.__web_driver.switch_to.alert

    def is_alert_present(self):
        try:
            alert = self.__web_driver.switch_to.alert
            return True
        except NoAlertPresentException:
            return False

    def wait_for_alert_present(self):
        wait_for(self.is_alert_present)

    def get_cookies(self):
        return self.__web_driver.get_cookies()

    def get_cookie(self, name):
        return self.__web_driver.get_cookie(name)

    def delete_cookie(self, name):
        self.__web_driver.delete_cookie(name)

    def delete_all_cookies(self):
        self.__web_driver.delete_all_cookies()

    def add_cookie(self, cookie_dict):
        self.__web_driver.add_cookie(cookie_dict)

    def get_desired_capabilities(self):
        return self.__web_driver.desired_capabilities

    def get_screenshot_as_file(self, filename):
        return self.__web_driver.get_screenshot_as_file(filename)

    def get_screenshot_as_png(self):
        return self.__web_driver.get_screenshot_as_png()

    def get_screenshot_as_base64(self):
        return self.__web_driver.get_screenshot_as_base64()

    save_screenshot = get_screenshot_as_file

    def get_current_window_handle(self):
        return self.__web_driver.current_window_handle

    def get_window_handles(self):
        return self.__web_driver.window_handles

    def switch_to_window(self, window_reference):
        self.__web_driver.switch_to.window(window_reference)

    def close_window(self, window_reference="current"):
        if window_reference == "current":
            self.__web_driver.close()
        else:
            current_window = self.get_current_window_handle()
            self.switch_to_window(window_reference)
            self.__web_driver.close()
            self.switch_to_window(current_window)

    def set_window_size(self, width, height, window_reference="current"):
        self.__web_driver.set_window_size(width, height, window_reference)

    def get_window_size(self, window_reference="current"):
        return self.__web_driver.get_window_size(window_reference)

    def set_window_position(self, x, y, window_reference="current"):
        self.__web_driver.set_window_position(x, y, window_reference)

    def get_window_position(self, window_reference="current"):
        return self.__web_driver.get_window_position(window_reference)

    def get_orientation(self):
        return self.__web_driver.orientation

    def set_orientation(self, value):
        self.__web_driver = value

    def get_application_cache(self):
        return self.__web_driver.application_cache

    def get_log_types(self):
        return self.__web_driver.log_types

    def get_log(self, log_type):
        return self.__web_driver.get_log(log_type)

    def __str__(self):
        return "Browser [WebDriver: %s][SessionId: %s]" % (self.__web_driver.name, self.__web_driver.session_id)
