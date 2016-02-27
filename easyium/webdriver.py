from selenium.webdriver import Ie, Firefox, Chrome, Opera, Safari, Edge, PhantomJS, ActionChains
from selenium.common.exceptions import NoAlertPresentException

from .alert import Alert
from .context import Context
from .enumeration import WebDriverType
from .waiter import WebDriverWaitFor
from .exceptions import UnsupportedWebDriverTypeException
from .config import DEFAULT, default_config
from .decorator import SupportedBy

__author__ = 'karl.gong'


class WebDriver(Context):
    def __init__(self, web_driver_type=WebDriverType.CHROME, page_load_timeout=DEFAULT, script_timeout=DEFAULT,
                 wait_interval=DEFAULT, wait_timeout=DEFAULT, pre_wait_time=DEFAULT, post_wait_time=DEFAULT, **kwargs):
        """
            Creates a new instance of the WebDriver.

        :param web_driver_type: the web driver type
        :param page_load_timeout: the page load timeout (in milliseconds), default value is from default_config.web_driver_page_load_timeout
        :param script_timeout: the script timeout (in milliseconds), default value is from default_config.web_driver_script_timeout
        :param wait_interval: the wait interval (in milliseconds), default value is from default_config.web_driver_wait_interval
        :param wait_timeout: the wait timeout (in milliseconds), default value is from default_config.web_driver_wait_timeout
        :param pre_wait_time: the pre wait time (in milliseconds), default value is from default_config.web_driver_pre_wait_time
        :param post_wait_time: the post wait time (in milliseconds), default value is from default_config.web_driver_post_wait_time
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
        elif self.__web_driver_type == WebDriverType.EDGE:
            self.__selenium_web_driver = Edge(**kwargs)
        elif self.__web_driver_type == WebDriverType.PHANTOMJS:
            self.__selenium_web_driver = PhantomJS(**kwargs)
        elif self.__web_driver_type in WebDriverType._MOBILE:
            from appium.webdriver.webdriver import WebDriver as Mobile
            self.__selenium_web_driver = Mobile(**kwargs)
        else:
            raise UnsupportedWebDriverTypeException("The web driver type [%s] is not supported." % web_driver_type)
        self.set_page_load_timeout(default_config.web_driver_page_load_timeout if page_load_timeout == DEFAULT else page_load_timeout)
        self.set_script_timeout(default_config.web_driver_script_timeout if script_timeout == DEFAULT else script_timeout)
        self.__wait_interval = default_config.web_driver_wait_interval if wait_interval == DEFAULT else wait_interval
        self.__wait_timeout = default_config.web_driver_wait_timeout if wait_timeout == DEFAULT else wait_timeout
        self.__pre_wait_time = default_config.web_driver_pre_wait_time if pre_wait_time == DEFAULT else pre_wait_time
        self.__post_wait_time = default_config.web_driver_post_wait_time if post_wait_time == DEFAULT else post_wait_time

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

    def create_action_chains(self):
        """
            Create a new ActionChains instance.
        """
        return ActionChains(self._selenium_web_driver())

    @SupportedBy(WebDriverType._MOBILE)
    def create_touch_action(self):
        """
            Create a new TouchAction instance.
        """
        from appium.webdriver.common.touch_action import TouchAction
        return TouchAction(self._selenium_web_driver())

    @SupportedBy(WebDriverType._MOBILE)
    def create_multi_action(self):
        """
            Create a new MultiAction instance.
        """
        from appium.webdriver.common.multi_action import MultiAction
        return MultiAction(self._selenium_web_driver())

    def get_wait_interval(self):
        return self.__wait_interval

    def get_wait_timeout(self):
        return self.__wait_timeout

    def get_pre_wait_time(self):
        return self.__pre_wait_time

    def get_post_wait_time(self):
        return self.__post_wait_time

    def wait_for(self, interval=DEFAULT, timeout=DEFAULT, pre_wait_time=DEFAULT, post_wait_time=DEFAULT):
        """
            Get a WebDriverWaitFor instance.

        :param interval: the wait interval (in milliseconds), default value is web driver's wait interval
        :param timeout: the wait timeout (in milliseconds), default value is web driver's wait timeout
        :param pre_wait_time: the pre wait time (in milliseconds), default value is web driver's pre wait time
        :param post_wait_time: the post wait time (in milliseconds), default value is web driver's post wait time
        """
        _interval = self.get_wait_interval() if interval == DEFAULT else interval
        _timeout = self.get_wait_timeout() if timeout == DEFAULT else timeout
        _pre_wait_time = self.get_pre_wait_time() if pre_wait_time == DEFAULT else pre_wait_time
        _post_wait_time = self.get_post_wait_time() if post_wait_time == DEFAULT else post_wait_time
        return WebDriverWaitFor(self, _interval, _timeout, _pre_wait_time, _post_wait_time)

    @SupportedBy(WebDriverType._BROWSER)
    def maximize_window(self):
        """
            Maximizes the current window that webdriver is using
        """
        self.__selenium_web_driver.maximize_window()

    def set_page_load_timeout(self, timeout):
        """
            Set the amount of time to wait for a page load to complete before throwing an error.

        :param timeout: The amount of time to wait
        """
        self.__selenium_web_driver.set_page_load_timeout(timeout / 1000.0)

    def set_script_timeout(self, timeout):
        """
            Set the amount of time that the script should wait during an execute_async_script call before throwing an error.

        :param timeout: The amount of time to wait
        """
        self.__selenium_web_driver.set_script_timeout(timeout / 1000.0)

    def execute_script(self, script, *args):
        """
            Synchronously Executes JavaScript in the current window/frame.

        :param script: The JavaScript to execute
        :param args: Any applicable arguments for your JavaScript
        :return: the return value of JavaScript
        """
        from .element import Element

        converted_args = []
        for arg in args:
            if isinstance(arg, Element):
                converted_args.append(arg._selenium_element())
            else:
                converted_args.append(arg)

        return self.__selenium_web_driver.execute_script(script, *converted_args)

    def execute_async_script(self, script, *args):
        """
            Asynchronously Executes JavaScript in the current window/frame.

        :param script: The JavaScript to execute
        :param args: Any applicable arguments for your JavaScript
        :return: the return value of JavaScript
        """
        from .element import Element

        converted_args = []
        for arg in args:
            if isinstance(arg, Element):
                converted_args.append(arg._selenium_element())
            else:
                converted_args.append(arg)

        return self.__selenium_web_driver.execute_async_script(script, *converted_args)

    def open(self, url):
        """
            Loads a web page in the current browser session.

        :param url: the url to be open
        """
        self.__selenium_web_driver.get(url)

    get = open

    def get_title(self):
        """
            Returns the title of the current page.
        """
        return self.__selenium_web_driver.title

    def refresh(self):
        """
            Refreshes the current page.
        """
        self.__selenium_web_driver.refresh()

    def back(self):
        """
            Goes one step backward in the browser history.
        """
        self.__selenium_web_driver.back()

    def forward(self):
        """
            Goes one step forward in the browser history.
        """
        self.__selenium_web_driver.forward()

    def quit(self):
        """
            Quits the driver and closes every associated window.
        """
        self.__selenium_web_driver.quit()

    def get_current_url(self):
        """
            Gets the URL of the current page.
        """
        return self.__selenium_web_driver.current_url

    def get_page_source(self):
        """
            Gets the source of the current page.
        """
        return self.__selenium_web_driver.page_source

    @SupportedBy(WebDriverType._MOBILE)
    def get_contexts(self):
        """
            Returns the contexts within the current session.
        """
        return self.__selenium_web_driver.contexts

    @SupportedBy(WebDriverType._MOBILE)
    def get_current_context(self):
        """
            Returns the current context of the current session.
        """
        return self.__selenium_web_driver.current_context

    @SupportedBy(WebDriverType._MOBILE)
    def switch_to_context(self, context_name):
        """
            Sets the context for the current session.

        :param context_name: The name of the context to switch to

        :Usage:
            driver.switch_to.context('WEBVIEW_1')
        """
        self.__selenium_web_driver.switch_to.context(context_name)

    def switch_to_frame(self, frame_reference):
        """
            Switches focus to the specified frame, by index, name, or element.

        :param frame_reference: the name of the window to switch to, an integer representing the index,
                            or a element that is an (i)frame to switch to.

        :Usage:
            driver.switch_to_frame('frame_name')
            driver.switch_to_frame(1)
            driver.switch_to_frame(StaticElement(driver, "tag=iframe"))
        """
        from .element import Element

        if isinstance(frame_reference, Element):
            frame_reference.wait_for().exists()
            self.__selenium_web_driver.switch_to.frame(frame_reference._selenium_element())
        else:
            self.__selenium_web_driver.switch_to.frame(frame_reference)

    def switch_to_parent_frame(self):
        """
            Switches focus to the parent context. If the current context is the top
            level browsing context, the context remains unchanged.
        """
        self.__selenium_web_driver.switch_to.parent_frame()

    def switch_to_default_content(self):
        """
            Switch focus to the default frame.
        """
        self.__selenium_web_driver.switch_to.default_content()

    switch_to_default_frame = switch_to_default_content

    def get_alert(self):
        """
            Switches focus to an alert on the page.

        :return: the Alert instance
        """
        self.wait_for().alert_present()
        return Alert(self.__selenium_web_driver.switch_to.alert)

    switch_to_alert = get_alert

    def is_alert_present(self):
        """
            Return whether the alert is present on the page or not.
        """
        try:
            alert_text = self.__selenium_web_driver.switch_to.alert.text
            return True
        except NoAlertPresentException:
            return False

    def get_cookies(self):
        """
            Returns a set of dictionaries, corresponding to cookies visible in the current session.
        """
        return self.__selenium_web_driver.get_cookies()

    def get_cookie(self, name):
        """
            Get a single cookie by name. Returns the cookie if found, None if not.

        :param name: the cookie name
        """
        return self.__selenium_web_driver.get_cookie(name)

    def add_cookie(self, cookie_dict):
        """
            Adds a cookie to your current session.

        :param cookie_dict: A dictionary object, with required keys - "name" and "value";
            optional keys - "path", "domain", "secure", "expiry"

        Usage:
            driver.add_cookie({'name' : 'foo', 'value' : 'bar'})
            driver.add_cookie({'name' : 'foo', 'value' : 'bar', 'path' : '/'})
            driver.add_cookie({'name' : 'foo', 'value' : 'bar', 'path' : '/', 'secure':True})
        """
        self.__selenium_web_driver.add_cookie(cookie_dict)

    def delete_cookie(self, name):
        """
            Deletes a single cookie with the given name.

        :param name: the cookie name
        """
        self.__selenium_web_driver.delete_cookie(name)

    def delete_all_cookies(self):
        """
            Delete all cookies in the scope of the session.
        """
        self.__selenium_web_driver.delete_all_cookies()

    def get_desired_capabilities(self):
        """
            Returns the drivers current desired capabilities being used.
        """
        return self.__selenium_web_driver.desired_capabilities

    def get_screenshot_as_file(self, filename):
        """
            Gets the screenshot of the current window. Returns False if there is
           any IOError, else returns True. Use full paths in your filename.

        :param filename: The full path you wish to save your screenshot to.

        :Usage:
            driver.get_screenshot_as_file('/Screenshots/foo.png')
        """
        return self.__selenium_web_driver.get_screenshot_as_file(filename)

    def get_screenshot_as_png(self):
        """
            Gets the screenshot of the current window as a binary data.

        :Usage:
            driver.get_screenshot_as_png()
        """
        return self.__selenium_web_driver.get_screenshot_as_png()

    def get_screenshot_as_base64(self):
        """
            Gets the screenshot of the current window as a base64 encoded string
            which is useful in embedded images in HTML.

        :Usage:
            driver.get_screenshot_as_base64()
        """
        return self.__selenium_web_driver.get_screenshot_as_base64()

    save_screenshot = get_screenshot_as_file

    def get_current_window_handle(self):
        """
            Returns the handle of the current window.
        """
        return self.__selenium_web_driver.current_window_handle

    def get_window_handles(self):
        """
            Returns the handles of all windows within the current session.
        """
        return self.__selenium_web_driver.window_handles

    def switch_to_window(self, window_reference):
        """
            Switches focus to the specified window.

        :param window_reference: The name or window handle of the window to switch to.

        :Usage:
            driver.switch_to_window('main')
        """
        self.__selenium_web_driver.switch_to.window(window_reference)

    def switch_to_new_window(self, previous_window_handles):
        """
            Switch to the new opened window.

        :param previous_window_handles: the window handles before opening new window

        :Usage:
            previous_window_handles = driver.get_window_handles()
            StaticElement(driver, "id=open-new-window").click() # open the new window
            driver.switch_to_new_window(previous_window_handles)
        """
        new_window_handles = {"inner": []}
        def get_new_window_handles():
            new_window_handles["inner"] = [handle for handle in self.get_window_handles() if handle not in previous_window_handles]
            return new_window_handles["inner"]

        def new_window_opened():
            return len(get_new_window_handles()) > 0

        self.waiter().wait_for(new_window_opened)
        self.switch_to_window(new_window_handles["inner"][0])

    def close_window(self, window_reference="current"):
        """
            Close the specified window.

        :param window_reference: The name or window handle of the window to close,
                    default is current window.
        """
        if window_reference == "current" or window_reference == self.get_current_window_handle():
            self.__selenium_web_driver.close()
        else:
            current_window_handle = self.get_current_window_handle()
            self.switch_to_window(window_reference)
            self.__selenium_web_driver.close()
            self.switch_to_window(current_window_handle)

    def set_window_size(self, width, height, window_reference="current"):
        """
            Sets the width and height of the specified window.

        :param width: the width in pixels to set the window to
        :param height: the height in pixels to set the window to
        :param window_reference: The name or window handle of the window to set,
                    default is current window.

        :Usage:
            driver.set_window_size(800,600)
        """
        self.__selenium_web_driver.set_window_size(width, height, window_reference)

    def get_window_size(self, window_reference="current"):
        """
            Gets the width and height of the specified window.

        :param window_reference: The name or window handle of the window to get,
                    default is current window.
        """
        return self.__selenium_web_driver.get_window_size(window_reference)

    def set_window_position(self, x, y, window_reference="current"):
        """
            Sets the x, y position of the specified window.

        :param x: the x-coordinate in pixels to set the window position
        :param y: the y-coordinate in pixels to set the window position
        :param window_reference: The name or window handle of the window to set,
                    default is current window.

        :Usage:
            driver.set_window_position(0,0)
        """
        self.__selenium_web_driver.set_window_position(x, y, window_reference)

    def get_window_position(self, window_reference="current"):
        """
            Gets the x, y position of the specified window.

        :param window_reference: The name or window handle of the window to get,
                    default is current window.
        """
        return self.__selenium_web_driver.get_window_position(window_reference)

    @SupportedBy(WebDriverType._MOBILE)
    def get_orientation(self):
        """
            Gets the current orientation of the device
        """
        return self.__selenium_web_driver.orientation

    @SupportedBy(WebDriverType._MOBILE)
    def set_orientation(self, value):
        """
            Sets the current orientation of the device

        :param value: orientation to set it to, allowed_values: LANDSCAPE, PORTRAIT
        """
        self.__selenium_web_driver.orientation = value.upper()

    def get_application_cache(self):
        """
            Returns a ApplicationCache Object to interact with the browser app cache.
        """
        return self.__selenium_web_driver.application_cache

    def get_log_types(self):
        """
            Gets a list of the available log types.
        """
        return self.__selenium_web_driver.log_types

    def get_log(self, log_type):
        """
            Gets the log for a given log type

        :param log_type: type of log that which will be returned

        :Usage:
            driver.get_log('browser')
            driver.get_log('driver')
            driver.get_log('client')
            driver.get_log('server')
        """
        return self.__selenium_web_driver.get_log(log_type)

    @SupportedBy(WebDriverType._MOBILE)
    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        """
            Swipe from one point to another point, for an optional duration.

        :param start_x: x-coordinate at which to start
        :param start_y: y-coordinate at which to start
        :param end_x: x-coordinate at which to stop
        :param end_y: y-coordinate at which to stop
        :param duration: time to take the swipe, in ms.

        :Usage:
            driver.swipe(100, 100, 100, 400)
        """
        self.__selenium_web_driver.swipe(start_x, start_y, end_x, end_y, duration)

    @SupportedBy(WebDriverType._MOBILE)
    def flick(self, start_x, start_y, end_x, end_y):
        """
            Flick from one point to another point.

        :param start_x - x-coordinate at which to start
        :param start_y - y-coordinate at which to start
        :param end_x - x-coordinate at which to stop
        :param end_y - y-coordinate at which to stop

        :Usage:
            driver.flick(100, 100, 100, 400)
        """
        self.__selenium_web_driver.flick(start_x, start_y, end_x, end_y)

    @SupportedBy(WebDriverType._MOBILE)
    def scroll(self, direction):
        """
            Scrolls the device to direction.
            It will try to scroll in the first element of type scroll view, table or collection view it finds.
            If you want to scroll in element, please use Element.scroll(direction)

        :param direction: the direction to scroll, the possible values are: up, down, left, right
        """
        scroll_params = {
            "direction": direction
        }
        self.execute_script("mobile: scroll", scroll_params)

    @SupportedBy(WebDriverType._MOBILE)
    def hide_keyboard(self, key_name=None, key=None, strategy=None):
        """
            Hides the software keyboard on the device. In iOS, use `key_name` to press
            a particular key, or `strategy`. In Android, no parameters are used.

        :param key_name: key to press
        :param key: key to press
        :param strategy: strategy for closing the keyboard (e.g., `tapOutside`)
        """
        self.__selenium_web_driver.hide_keyboard(key_name, key, strategy)

    @SupportedBy(WebDriverType.ANDROID)
    def key_event(self, keycode, metastate=None):
        """
            Sends a keycode to the device. Android only. Possible keycodes can be
            found in http://developer.android.com/reference/android/view/KeyEvent.html.

        :param keycode: the keycode to be sent to the device
        :param metastate: meta information about the keycode being sent
        """
        self.__selenium_web_driver.keyevent(keycode, metastate)

    @SupportedBy(WebDriverType.ANDROID)
    def press_keycode(self, keycode, metastate=None):
        """
            Sends a keycode to the device. Android only. Possible keycodes can be
            found in http://developer.android.com/reference/android/view/KeyEvent.html.

        :param keycode: the keycode to be sent to the device
        :param metastate: meta information about the keycode being sent
        """
        self.__selenium_web_driver.press_keycode(keycode, metastate)

    @SupportedBy(WebDriverType.ANDROID)
    def long_press_keycode(self, keycode, metastate=None):
        """
            Sends a long press of keycode to the device. Android only. Possible keycodes can be
            found in http://developer.android.com/reference/android/view/KeyEvent.html.

        :param keycode: the keycode to be sent to the device
        :param metastate: meta information about the keycode being sent
        """
        self.__selenium_web_driver.long_press_keycode(keycode, metastate)

    @SupportedBy(WebDriverType._MOBILE)
    def pull_file(self, path):
        """
            Retrieves the file at `path`. Returns the file's content encoded as Base64.

        :param path: the path to the file on the device
        """
        return self.__selenium_web_driver.pull_file(path)

    @SupportedBy(WebDriverType._MOBILE)
    def pull_folder(self, path):
        """
            Retrieves a folder at `path`. Returns the folder's contents zipped and encoded as Base64.

         :param path: the path to the folder on the device
        """
        return self.__selenium_web_driver.pull_folder(path)

    @SupportedBy(WebDriverType._MOBILE)
    def push_file(self, path, base64data):
        """
            Puts the data, encoded as Base64, in the file specified as `path`.

        :param path: the path on the device
        :param base64data: data, encoded as Base64, to be written to the file
        """
        self.__selenium_web_driver.push_file(path, base64data)

    @SupportedBy(WebDriverType._MOBILE)
    def app_strings(self, language=None, string_file=None):
        """
            Returns the application strings from the device for the specified language.

        :param language: strings language code
        :param string_file: the name of the string file to query
        """
        return self.__selenium_web_driver.app_strings(language, string_file)

    @SupportedBy(WebDriverType._MOBILE)
    def install_app(self, app_path):
        """
            Install the application found at `app_path` on the device.

        :param app_path: the local or remote path to the application to install
        """
        self.__selenium_web_driver.install_app(app_path)

    @SupportedBy(WebDriverType._MOBILE)
    def is_app_installed(self, bundle_id):
        """
            Checks whether the application specified by `bundle_id` is installed on the device.

        :param bundle_id: the id of the application to query
        """
        return self.__selenium_web_driver.is_app_installed(bundle_id)

    @SupportedBy(WebDriverType._MOBILE)
    def remove_app(self, app_id):
        """
            Remove the specified application from the device.

        :param app_id: the application id to be removed
        """
        self.__selenium_web_driver.remove_app(app_id)

    @SupportedBy(WebDriverType._MOBILE)
    def launch_app(self):
        """
            Start on the device the application specified in the desired capabilities.
        """
        self.__selenium_web_driver.launch_app()

    @SupportedBy(WebDriverType._MOBILE)
    def close_app(self):
        """
            Stop the running application, specified in the desired capabilities, on the device.
        """
        self.__selenium_web_driver.close_app()

    @SupportedBy(WebDriverType._MOBILE)
    def reset_app(self):
        """
            Resets the current application on the device.
        """
        self.__selenium_web_driver.reset()

    @SupportedBy(WebDriverType._MOBILE)
    def background_app(self, duration):
        """
            Puts the application in the background on the device for a certain duration.

         :param duration: the duration for the application to remain in the background, in ms.
        """
        self.__selenium_web_driver.background_app(duration / 1000.0)

    @SupportedBy(WebDriverType.ANDROID)
    def get_current_activity(self):
        """
            Retrieves the current activity on the device.
        """
        return self.__selenium_web_driver.current_activity

    @SupportedBy(WebDriverType.ANDROID)
    def start_activity(self, app_package, app_activity, app_wait_package=DEFAULT, app_wait_activity=DEFAULT,
                       intent_action=DEFAULT, intent_category=DEFAULT, intent_flags=DEFAULT,
                       optional_intent_arguments=DEFAULT, stop_app_on_reset=DEFAULT):
        """
            Opens an arbitrary activity during a test. If the activity belongs to
            another application, that application is started and the activity is opened.

            This is an Android-only method.

        :param app_package: The package containing the activity to start.
        :param app_activity: The activity to start.
        :param app_wait_package: Begin automation after this package starts.
        :param app_wait_activity: Begin automation after this activity starts.
        :param intent_action: Intent to start.
        :param intent_category: Intent category to start.
        :param intent_flags: Flags to send to the intent.
        :param optional_intent_arguments: Optional arguments to the intent.
        :param stop_app_on_reset: Whether the app should be stopped on reset or not
        """
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
        """
            Ends the coverage collection and pull the coverage.ec file from the device.
            Android only.

            See https://github.com/appium/appium/blob/master/docs/en/android_coverage.md

         :param intent: description of operation to be performed
         :param path: path to coverage.ec file to be pulled from the device
        """
        self.__selenium_web_driver.end_test_coverage(intent, path)

    @SupportedBy(WebDriverType.IOS)
    def lock(self, duration):
        """
            Lock the device for a certain period of time. iOS only.

        :param duration: the duration to lock the device, in ms.
        """
        self.__selenium_web_driver.lock(duration / 1000.0)

    @SupportedBy(WebDriverType._MOBILE)
    def shake(self):
        """
            Shake the device.
        """
        self.__selenium_web_driver.shake()

    @SupportedBy(WebDriverType.ANDROID)
    def open_notifications(self):
        """
            Open notification shade in Android (API Level 18 and above)
        """
        self.__selenium_web_driver.open_notifications()

    @SupportedBy(WebDriverType.ANDROID)
    def get_network_connection(self):
        """
            Returns an integer bitmask specifying the network connection type.
            Android only.
            Possible values are available through the enumeration `appium.webdriver.ConnectionType`
        """
        return self.__selenium_web_driver.network_connection

    @SupportedBy(WebDriverType.ANDROID)
    def set_network_connection(self, connection_type):
        """
            Sets the network connection type. Android only.
            Possible values::
                Value (Alias)      | Data | Wifi | Airplane Mode
                -------------------------------------------------
                0 (None)           | 0    | 0    | 0
                1 (Airplane Mode)  | 0    | 0    | 1
                2 (Wifi only)      | 0    | 1    | 0
                4 (Data only)      | 1    | 0    | 0
                6 (All network on) | 1    | 1    | 0
            These are available through the enumeration `appium.webdriver.ConnectionType`

         :param connection_type: a member of the enum appium.webdriver.ConnectionType
        """
        self.__selenium_web_driver.set_network_connection(connection_type)

    @SupportedBy(WebDriverType.ANDROID)
    def get_available_ime_engines(self):
        """
            Get the available input methods for an Android device. Package and
            activity are returned (e.g., ['com.android.inputmethod.latin/.LatinIME'])
            Android only.
        """
        return self.__selenium_web_driver.available_ime_engines

    @SupportedBy(WebDriverType.ANDROID)
    def is_ime_service_active(self):
        """
            Checks whether the device has IME service active. Returns True/False.
            Android only.
        """
        return self.__selenium_web_driver.is_ime_active()

    @SupportedBy(WebDriverType.ANDROID)
    def active_ime_engine(self, engine):
        """
            Activates the given IME engine on the device.
            Android only.

        :param engine: the package and activity of the IME engine to activate (e.g., 'com.android.inputmethod.latin/.LatinIME')
        """
        self.__selenium_web_driver.activate_ime_engine(engine)

    @SupportedBy(WebDriverType.ANDROID)
    def deactivate_current_ime_engine(self):
        """
            Deactivates the currently active IME engine on the device.
            Android only.
        """
        self.__selenium_web_driver.deactivate_ime_engine()

    @SupportedBy(WebDriverType.ANDROID)
    def get_current_ime_engine(self):
        """
            Returns the activity and package of the currently active IME engine (e.g., 'com.android.inputmethod.latin/.LatinIME').
            Android only.
        """
        return self.__selenium_web_driver.active_ime_engine

    @SupportedBy(WebDriverType._MOBILE)
    def get_settings(self):
        """
            Returns the appium server Settings for the current session.
            Do not get Settings confused with Desired Capabilities, they are
            separate concepts. See https://github.com/appium/appium/blob/master/docs/en/advanced-concepts/settings.md
        """
        return self.__selenium_web_driver.get_settings()

    @SupportedBy(WebDriverType._MOBILE)
    def update_settings(self, settings):
        """
            Set settings for the current session.
            For more on settings, see: https://github.com/appium/appium/blob/master/docs/en/advanced-concepts/settings.md

        :param settings: dictionary of settings to apply to the current test session
        """
        self.__selenium_web_driver.update_settings(settings)

    @SupportedBy(WebDriverType.ANDROID)
    def toggle_location_services(self):
        """
            Toggle the location services on the device. Android only.
        """
        self.__selenium_web_driver.toggle_location_services()

    @SupportedBy(WebDriverType._MOBILE)
    def set_location(self, latitude, longitude, altitude):
        """
            Set the location of the device

        :param latitude: String or numeric value between -90.0 and 90.00
        :param longitude: String or numeric value between -180.0 and 180.0
        :param altitude: String or numeric value
        """
        self.__selenium_web_driver.set_location(latitude, longitude, altitude)

    def __str__(self):
        return "WebDriver <WebDriverType: %s><SessionId: %s>" % (self.__web_driver_type, self.__selenium_web_driver.session_id)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()


Browser = WebDriver
