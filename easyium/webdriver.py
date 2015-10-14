from selenium.webdriver import Ie, Firefox, Chrome, Opera, Safari, PhantomJS
from selenium.common.exceptions import NoAlertPresentException

from .context import Context
from .waiter import WebDriverWaitFor
from .exceptions import UnsupportedWebDriverTypeException
from .config import DEFAULT, default_config
from .decorator import SupportedBy

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
                 pre_wait_time=DEFAULT, wait_interval=DEFAULT, wait_timeout=DEFAULT, **kwargs):
        """
            Creates a new instance of the WebDriver.

        :param web_driver_type: the web driver type
        :param page_load_timeout: the page load timeout (in milliseconds), default value is from default_config.web_driver_page_load_timeout
        :param script_timeout: the script timeout (in milliseconds), default value is from default_config.web_driver_script_timeout
        :param wait_interval: the wait interval (in milliseconds), default value is from default_config.web_driver_wait_interval
        :param wait_timeout: the wait timeout (in milliseconds), default value is from default_config.web_driver_wait_timeout
        :param kwargs: the keyword args for the web driver specified by web_driver_type
        """
        Context.__init__(self)
        self.__web_driver_type = web_driver_type.lower()
        if self.__web_driver_type == WebDriverType.IE:
            self.__selenium_web_driver = Ie(**kwargs)
        elif self.__web_driver_type == WebDriverType.FIREFOX:
            self.__selenium_web_driver = Firefox(**kwargs)
        elif self.__web_driver_type == WebDriverType.CHROME:
            self.__selenium_web_driver = Chrome(**kwargs)
        elif self.__web_driver_type == WebDriverType.OPERA:
            self.__selenium_web_driver = Opera(**kwargs)
        elif self.__web_driver_type == WebDriverType.SAFARI:
            self.__selenium_web_driver = Safari(**kwargs)
        elif self.__web_driver_type == WebDriverType.PHANTOMJS:
            self.__selenium_web_driver = PhantomJS(**kwargs)
        elif self.__web_driver_type in WebDriverType._MOBILE:
            from appium.webdriver.webdriver import WebDriver as Mobile
            self.__selenium_web_driver = Mobile(**kwargs)
        else:
            raise UnsupportedWebDriverTypeException("The web driver type [%s] is not supported." % web_driver_type)
        self.set_page_load_timeout(default_config.web_driver_page_load_timeout if page_load_timeout == DEFAULT else page_load_timeout)
        self.set_script_timeout(default_config.web_driver_script_timeout if script_timeout == DEFAULT else script_timeout)
        self.__pre_wait_time = default_config.web_driver_pre_wait_time if pre_wait_time == DEFAULT else pre_wait_time
        self.__wait_interval = default_config.web_driver_wait_interval if wait_interval == DEFAULT else wait_interval
        self.__wait_timeout = default_config.web_driver_wait_timeout if wait_timeout == DEFAULT else wait_timeout

    def _selenium_web_driver(self):
        return self.__selenium_web_driver

    def _selenium_context(self):
        return self.__selenium_web_driver

    def get_web_driver(self):
        return self

    get_browser = get_web_driver

    def get_web_driver_type(self):
        return self.__web_driver_type

    get_browser_type = get_web_driver_type

    def get_pre_wait_time(self):
        return self.__pre_wait_time

    def get_wait_interval(self):
        return self.__wait_interval

    def get_wait_timeout(self):
        return self.__wait_timeout

    def wait_for(self, interval=DEFAULT, timeout=DEFAULT):
        """
            Get a WebDriverWaitFor instance.

        :param interval: the wait interval (in milliseconds), default value is web driver's wait interval
        :param timeout: the wait timeout (in milliseconds), default value is web driver's wait timeout
        """
        interval = self.get_wait_interval() if interval == DEFAULT else interval
        timeout = self.get_wait_timeout() if timeout == DEFAULT else timeout
        return WebDriverWaitFor(self, interval, timeout)

    @SupportedBy(WebDriverType._BROWSER)
    def maximize_window(self):
        self.__selenium_web_driver.maximize_window()

    def set_page_load_timeout(self, timeout):
        self.__selenium_web_driver.set_page_load_timeout(timeout / 1000.0)

    def set_script_timeout(self, timeout):
        self.__selenium_web_driver.set_script_timeout(timeout / 1000.0)

    def execute_script(self, script, *args):
        from .element import Element

        converted_args = []
        for arg in args:
            if isinstance(arg, Element):
                converted_args.append(arg._selenium_element())
            else:
                converted_args.append(arg)

        return self.__selenium_web_driver.execute_script(script, *converted_args)

    def execute_async_script(self, script, *args):
        from .element import Element

        converted_args = []
        for arg in args:
            if isinstance(arg, Element):
                converted_args.append(arg._selenium_element())
            else:
                converted_args.append(arg)

        return self.__selenium_web_driver.execute_async_script(script, *converted_args)

    def open(self, url):
        self.__selenium_web_driver.get(url)

    get = open

    def get_title(self):
        return self.__selenium_web_driver.title

    def refresh(self):
        self.__selenium_web_driver.refresh()

    def back(self):
        self.__selenium_web_driver.back()

    def forward(self):
        self.__selenium_web_driver.forward()

    def quit(self):
        self.__selenium_web_driver.quit()

    def get_current_url(self):
        return self.__selenium_web_driver.current_url

    def get_page_source(self):
        return self.__selenium_web_driver.page_source

    @SupportedBy(WebDriverType._MOBILE)
    def get_contexts(self):
        return self.__selenium_web_driver.contexts

    @SupportedBy(WebDriverType._MOBILE)
    def get_current_context(self):
        return self.__selenium_web_driver.current_context

    @SupportedBy(WebDriverType._MOBILE)
    def switch_to_context(self, context_name):
        self.__selenium_web_driver.switch_to.context(context_name)

    def switch_to_frame(self, frame_reference):
        self.__selenium_web_driver.switch_to.frame(frame_reference)

    def switch_to_parent_frame(self):
        self.__selenium_web_driver.switch_to.parent_frame()

    def switch_to_default_content(self):
        self.__selenium_web_driver.switch_to.default_content()

    def get_alert(self):
        return self.__selenium_web_driver.switch_to.alert

    def is_alert_present(self):
        try:
            alert_text = self.__selenium_web_driver.switch_to.alert.text
            return True
        except NoAlertPresentException:
            return False

    def get_cookies(self):
        return self.__selenium_web_driver.get_cookies()

    def get_cookie(self, name):
        return self.__selenium_web_driver.get_cookie(name)

    def delete_cookie(self, name):
        self.__selenium_web_driver.delete_cookie(name)

    def delete_all_cookies(self):
        self.__selenium_web_driver.delete_all_cookies()

    def add_cookie(self, cookie_dict):
        self.__selenium_web_driver.add_cookie(cookie_dict)

    def get_desired_capabilities(self):
        return self.__selenium_web_driver.desired_capabilities

    def get_screenshot_as_file(self, filename):
        return self.__selenium_web_driver.get_screenshot_as_file(filename)

    def get_screenshot_as_png(self):
        return self.__selenium_web_driver.get_screenshot_as_png()

    def get_screenshot_as_base64(self):
        return self.__selenium_web_driver.get_screenshot_as_base64()

    save_screenshot = get_screenshot_as_file

    def get_current_window_handle(self):
        return self.__selenium_web_driver.current_window_handle

    def get_window_handles(self):
        return self.__selenium_web_driver.window_handles

    def switch_to_window(self, window_reference):
        self.__selenium_web_driver.switch_to.window(window_reference)

    def close_window(self, window_reference="current"):
        if window_reference == "current":
            self.__selenium_web_driver.close()
        else:
            current_window = self.get_current_window_handle()
            self.switch_to_window(window_reference)
            self.__selenium_web_driver.close()
            self.switch_to_window(current_window)

    def set_window_size(self, width, height, window_reference="current"):
        self.__selenium_web_driver.set_window_size(width, height, window_reference)

    def get_window_size(self, window_reference="current"):
        return self.__selenium_web_driver.get_window_size(window_reference)

    def set_window_position(self, x, y, window_reference="current"):
        self.__selenium_web_driver.set_window_position(x, y, window_reference)

    def get_window_position(self, window_reference="current"):
        return self.__selenium_web_driver.get_window_position(window_reference)

    def get_orientation(self):
        return self.__selenium_web_driver.orientation

    def set_orientation(self, value):
        self.__selenium_web_driver.orientation = value.upper()

    def get_application_cache(self):
        return self.__selenium_web_driver.application_cache

    def get_log_types(self):
        return self.__selenium_web_driver.log_types

    def get_log(self, log_type):
        return self.__selenium_web_driver.get_log(log_type)

    @SupportedBy(WebDriverType._MOBILE)
    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        self.__selenium_web_driver.swipe(start_x, start_y, end_x, end_y, duration)

    @SupportedBy(WebDriverType._MOBILE)
    def flick(self, start_x, start_y, end_x, end_y):
        self.__selenium_web_driver.flick(start_x, start_y, end_x, end_y)

    @SupportedBy(WebDriverType._MOBILE)
    def app_strings(self, language=None, string_file=None):
        return self.__selenium_web_driver.app_strings(language, string_file)

    @SupportedBy(WebDriverType._MOBILE)
    def reset_current_app(self):
        self.__selenium_web_driver.reset()

    @SupportedBy(WebDriverType._MOBILE)
    def hide_keyboard(self, key_name=None, key=None, strategy=None):
        self.__selenium_web_driver.hide_keyboard(key_name, key, strategy)

    @SupportedBy(WebDriverType.ANDROID)
    def key_event(self, key_code, meta_state=None):
        self.__selenium_web_driver.keyevent(key_code, meta_state)

    @SupportedBy(WebDriverType.ANDROID)
    def press_key(self, key_code, meta_state=None):
        self.__selenium_web_driver.press_keycode(key_code, meta_state)

    @SupportedBy(WebDriverType.ANDROID)
    def long_press_key(self, key_code, meta_state=None):
        self.__selenium_web_driver.long_press_keycode(key_code, meta_state)

    @SupportedBy(WebDriverType.ANDROID)
    def get_current_activity(self):
        return self.__selenium_web_driver.current_activity

    @SupportedBy(WebDriverType._MOBILE)
    def pull_file(self, path):
        return self.__selenium_web_driver.pull_file(path)

    @SupportedBy(WebDriverType._MOBILE)
    def pull_folder(self, path):
        return self.__selenium_web_driver.pull_folder(path)

    @SupportedBy(WebDriverType._MOBILE)
    def push_file(self, path, base64data):
        self.__selenium_web_driver.push_file(path, base64data)

    @SupportedBy(WebDriverType._MOBILE)
    def send_to_background(self, duration):
        self.__selenium_web_driver.background_app(duration / 1000.0)

    @SupportedBy(WebDriverType._MOBILE)
    def is_app_installed(self, bundle_id):
        return self.__selenium_web_driver.is_app_installed(bundle_id)

    @SupportedBy(WebDriverType._MOBILE)
    def install_app(self, app_path):
        self.__selenium_web_driver.install_app(app_path)

    @SupportedBy(WebDriverType._MOBILE)
    def remove_app(self, app_id):
        self.__selenium_web_driver.remove_app(app_id)

    @SupportedBy(WebDriverType._MOBILE)
    def launch_app(self):
        self.__selenium_web_driver.launch_app()

    @SupportedBy(WebDriverType._MOBILE)
    def close_app(self):
        self.__selenium_web_driver.close_app()

    @SupportedBy(WebDriverType.ANDROID)
    def start_activity(self, app_package, app_activity, app_wait_package=DEFAULT, app_wait_activity=DEFAULT,
                       intent_action=DEFAULT, intent_category=DEFAULT, intent_flags=DEFAULT,
                       optional_intent_arguments=DEFAULT, stop_app_on_reset=DEFAULT):
        options = {}
        if app_wait_package != DEFAULT:
            options["app_wait_package"] = app_wait_package
        if app_wait_activity != DEFAULT:
            options["app_wait_activity"] = app_wait_activity
        if intent_action != DEFAULT:
            options["intent_action"] = intent_action
        if intent_category != DEFAULT:
            options["intent_category"] = intent_category
        if intent_flags != DEFAULT:
            options["intent_flags"] = intent_flags
        if optional_intent_arguments != DEFAULT:
            options["optional_intent_arguments"] = optional_intent_arguments
        if stop_app_on_reset != DEFAULT:
            options["stop_app_on_reset"] = stop_app_on_reset

        self.__selenium_web_driver.start_activity(app_package, app_activity, **options)

    @SupportedBy(WebDriverType.ANDROID)
    def end_test_coverage(self, intent, path):
        self.__selenium_web_driver.end_test_coverage(intent, path)

    @SupportedBy(WebDriverType.IOS)
    def lock(self, duration):
        self.__selenium_web_driver.lock(duration / 1000.0)

    @SupportedBy(WebDriverType._MOBILE)
    def shake(self):
        self.__selenium_web_driver.shake()

    @SupportedBy(WebDriverType.ANDROID)
    def open_notifications(self):
        self.__selenium_web_driver.open_notifications()

    @SupportedBy(WebDriverType.ANDROID)
    def get_network_connection(self):
        return self.__selenium_web_driver.network_connection

    @SupportedBy(WebDriverType.ANDROID)
    def set_network_connection(self, connection_type):
        self.__selenium_web_driver.set_network_connection(connection_type)

    @SupportedBy(WebDriverType.ANDROID)
    def get_available_ime_engines(self):
        return self.__selenium_web_driver.available_ime_engines

    @SupportedBy(WebDriverType.ANDROID)
    def is_ime_service_active(self):
        return self.__selenium_web_driver.is_ime_active()

    @SupportedBy(WebDriverType.ANDROID)
    def active_ime_engine(self, engine):
        self.__selenium_web_driver.activate_ime_engine(engine)

    @SupportedBy(WebDriverType.ANDROID)
    def deactivate_current_ime_engine(self):
        self.__selenium_web_driver.deactivate_ime_engine()

    @SupportedBy(WebDriverType.ANDROID)
    def get_current_ime_engine(self):
        return self.__selenium_web_driver.active_ime_engine

    @SupportedBy(WebDriverType._MOBILE)
    def get_settings(self):
        return self.__selenium_web_driver.get_settings()

    @SupportedBy(WebDriverType._MOBILE)
    def update_settings(self, settings):
        self.__selenium_web_driver.update_settings(settings)

    @SupportedBy(WebDriverType.ANDROID)
    def toggle_location_services(self):
        self.__selenium_web_driver.toggle_location_services()

    @SupportedBy(WebDriverType._MOBILE)
    def set_location(self, latitude, longitude, altitude):
        self.__selenium_web_driver.set_location(latitude, longitude, altitude)

    def __str__(self):
        return "WebDriver [WebDriverType: %s][SessionId: %s]" % (self.__selenium_web_driver.name, self.__selenium_web_driver.session_id)


Browser = WebDriver
BrowserType = WebDriverType
