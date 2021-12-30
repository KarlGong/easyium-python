from typing import List, Union, TYPE_CHECKING

from appium.webdriver.clipboard_content_type import ClipboardContentType
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains, Ie as SeleniumIe, Firefox as SeleniumFirefox, Chrome as SeleniumChrome, Opera as SeleniumOpera, \
    Safari as SeleniumSafari, Edge as SeleniumEdge
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.html5.application_cache import ApplicationCache
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.options import Options as IeOptions
from selenium.webdriver.ie.service import Service as IeService
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.safari.service import Service as SafariService

from .alert import Alert
from .context import Context
from .decorator import SupportedBy
from .enumeration import WebDriverPlatform, WebDriverContext
from .waiter import WebDriverWaitFor

if TYPE_CHECKING:
    from .element import Element


class WebDriverInfo:
    def __init__(self, platform: WebDriverPlatform, context: WebDriverContext):
        self.platform = platform
        self.context = context


class WebDriver(Context):
    def __init__(self, selenium_web_driver: AppiumWebDriver, web_driver_info: WebDriverInfo):
        """
            Create a wrapper for selenium WebDriver.
        
        :param selenium_web_driver: the selenium web driver instance
        :param web_driver_info: the web driver info
        """
        Context.__init__(self)
        self.__selenium_web_driver = selenium_web_driver
        self.__web_driver_info = web_driver_info

        # set default wait interval and timeout
        self.set_wait_interval(1000)
        self.set_wait_timeout(30000)

    def _selenium_context(self) -> "AppiumWebDriver":
        return self.__selenium_web_driver

    def _selenium_web_driver(self) -> AppiumWebDriver:
        return self.__selenium_web_driver

    def get_web_driver(self) -> "WebDriver":
        """
            Get self.

        :return: self
        """
        return self

    def get_web_driver_info(self) -> WebDriverInfo:
        """
            Get current info of this web driver.

        :return: the web driver info
        """
        return self.__web_driver_info

    def get_desired_capabilities(self) -> dict:
        """
            Returns the drivers current desired capabilities being used.
        """
        return self._selenium_web_driver().capabilities

    def get_application_cache(self) -> ApplicationCache:
        """
            Returns a ApplicationCache Object to interact with the browser app cache.
        """
        return self._selenium_web_driver().application_cache

    def quit(self):
        """
            Quits the driver and closes every associated window.
        """
        self._selenium_web_driver().quit()

    def create_action_chains(self) -> ActionChains:
        """
            Create a new selenium.webdriver.common.ActionChains instance.
        """
        return ActionChains(self._selenium_web_driver())

    @SupportedBy(WebDriverPlatform._MOBILE)
    def create_touch_action(self) -> TouchAction:
        """
            Create a new appium.webdriver.common.TouchAction instance.
        """
        return TouchAction(self._selenium_web_driver())

    @SupportedBy(WebDriverPlatform._MOBILE)
    def create_multi_action(self) -> MultiAction:
        """
            Create a new appium.webdriver.common.MultiAction instance.
        """
        return MultiAction(self._selenium_web_driver())

    def wait_for(self, interval: int = None, timeout: int = None) -> WebDriverWaitFor:
        """
            Get a WebDriverWaitFor instance.

        :param interval: the wait interval (in milliseconds). If None, use driver's wait interval.
        :param timeout: the wait timeout (in milliseconds). If None, use driver's wait interval.
        """
        _interval = self.get_wait_interval() if interval is None else interval
        _timeout = self.get_wait_timeout() if timeout is None else timeout
        return WebDriverWaitFor(self, _interval, _timeout)

    # Timeouts

    def set_page_load_timeout(self, timeout: int):
        """
            Set the amount of time to wait for a page load to complete before throwing an error.

        :param timeout: The amount of time to wait (in milliseconds)
        """
        self._selenium_web_driver().set_page_load_timeout(timeout / 1000.0)

    def set_script_timeout(self, timeout: int):
        """
            Set the amount of time that the script should wait during an execute_async_script call before throwing an error.

        :param timeout: The amount of time to wait (in milliseconds)
        """
        self._selenium_web_driver().set_script_timeout(timeout / 1000.0)

    # Execute script

    def execute_script(self, script: str, *args) -> any:
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
                arg.wait_for().exists()
                converted_args.append(arg._selenium_element())
            else:
                converted_args.append(arg)

        return self._selenium_web_driver().execute_script(script, *converted_args)

    def execute_async_script(self, script: str, *args) -> any:
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
                arg.wait_for().exists()
                converted_args.append(arg._selenium_element())
            else:
                converted_args.append(arg)

        return self._selenium_web_driver().execute_async_script(script, *converted_args)

    # Orientation

    @SupportedBy(WebDriverPlatform._MOBILE)
    def get_orientation(self) -> str:
        """
            Gets the current orientation of the device
        """
        return self._selenium_web_driver().orientation

    @SupportedBy(WebDriverPlatform._MOBILE)
    def set_orientation(self, value: str):
        """
            Sets the current orientation of the device

        :param value: orientation to set it to, allowed_values: LANDSCAPE, PORTRAIT
        """
        self._selenium_web_driver().orientation = value.upper()

    # Geolocation

    @SupportedBy(WebDriverPlatform._MOBILE)
    def get_location(self) -> dict:
        """
            Retrieves the current location

        :return: A dictionary whose keys are
            - latitude (float)
            - longitude (float)
            - altitude (float)
        """
        return self._selenium_web_driver().location

    @SupportedBy(WebDriverPlatform._MOBILE)
    def set_location(self, latitude, longitude, altitude):
        """
            Set the location of the device

        :param latitude: String or numeric value between -90.0 and 90.00
        :param longitude: String or numeric value between -180.0 and 180.0
        :param altitude: String or numeric value
        """
        self._selenium_web_driver().set_location(latitude, longitude, altitude)

    # Logs

    def get_log_types(self) -> List[str]:
        """
            Gets a list of the available log types.
        """
        return self._selenium_web_driver().log_types

    def get_log(self, log_type: str) -> List[dict]:
        """
            Gets the log for a given log type

        :param log_type: type of log that which will be returned

        :Usage:
            driver.get_log('browser')
            driver.get_log('driver')
            driver.get_log('client')
            driver.get_log('server')
        """
        return self._selenium_web_driver().get_log(log_type)

    # Settings

    @SupportedBy(WebDriverPlatform._MOBILE)
    def get_settings(self) -> dict:
        """
            Returns the appium server Settings for the current session.
            Do not get Settings confused with Desired Capabilities, they are
            separate concepts. See https://github.com/appium/appium/blob/master/docs/en/advanced-concepts/settings.md
        """
        return self._selenium_web_driver().get_settings()

    @SupportedBy(WebDriverPlatform._MOBILE)
    def update_settings(self, settings: dict):
        """
            Set settings for the current session.
            For more on settings, see: https://github.com/appium/appium/blob/master/docs/en/advanced-concepts/settings.md

        :param settings: dictionary of settings to apply to the current test session
        """
        self._selenium_web_driver().update_settings(settings)

    # Activity

    @SupportedBy(WebDriverPlatform.ANDROID)
    def start_activity(self, app_package: str, app_activity: str, app_wait_package: str = None, app_wait_activity: str = None, intent_action: str = None,
                       intent_category: str = None, intent_flags: str = None, optional_intent_arguments: str = None, stop_app_on_reset: str = None):
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
        options = {
            "app_wait_package": app_wait_package,
            "app_wait_activity": app_wait_activity,
            "intent_action": intent_action,
            "intent_category": intent_category,
            "intent_flags": intent_flags,
            "optional_intent_arguments": optional_intent_arguments,
            "stop_app_on_reset": stop_app_on_reset
        }

        self._selenium_web_driver().start_activity(app_package, app_activity, **options)

    @SupportedBy(WebDriverPlatform.ANDROID)
    def get_current_activity(self) -> str:
        """
            Retrieves the current activity on the device.
        """
        return self._selenium_web_driver().current_activity

    @SupportedBy(WebDriverPlatform.ANDROID)
    def get_current_package(self) -> str:
        """
            Retrieves the current package running on the device.
        """
        return self._selenium_web_driver().current_package

    # App

    @SupportedBy(WebDriverPlatform._MOBILE)
    def install_app(self, app_path: str, replace: bool = True, timeout: int = 60000, allow_test_packages: bool = False, usd_sd_card: bool = False, grant_permissions: bool = False):
        """
            Install the application found at `app_path` on the device.

        :param app_path - the local or remote path to the application to install

        The following options are available for Android:
        :param replace: whether to reinstall/upgrade the package if it is already present on the device under test. True by default
        :param timeout: how much time to wait for the installation to complete. 60000ms by default.
        :param allow_test_packages: whether to allow installation of packages marked as test in the manifest. False by default
        :param usd_sd_card: whether to use the SD card to install the app. False by default
        :param grant_permissions: whether to automatically grant application permissions on Android 6+ after the installation completes. False by default
        """
        options = {
            "replace": replace,
            "timeout": timeout,
            "allowTestPackages": allow_test_packages,
            "useSdcard": usd_sd_card,
            "grantPermissions": grant_permissions
        }
        self._selenium_web_driver().install_app(app_path, **options)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def is_app_installed(self, bundle_id: str) -> bool:
        """
            Checks whether the application specified by `bundle_id` is installed on the device.

        :param bundle_id: the id of the application to query
        """
        return self._selenium_web_driver().is_app_installed(bundle_id)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def launch_app(self):
        """
            Start on the device the application specified in the desired capabilities.
        """
        self._selenium_web_driver().launch_app()

    @SupportedBy(WebDriverPlatform._MOBILE)
    def background_app(self, duration: int):
        """
            Puts the application in the background on the device for a certain duration.

         :param duration: the duration for the application to remain in the background, in ms.
        """
        self._selenium_web_driver().background_app(int(duration / 1000.0))

    @SupportedBy(WebDriverPlatform._MOBILE)
    def activate_app(self, app_id: str):
        """
            Activates the application if it is not running or is running in the background.

        :param app_id: the application id to be activated
        """
        self._selenium_web_driver().activate_app(app_id)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def close_app(self):
        """
            Stop the running application, specified in the desired capabilities, on the device.
        """
        self._selenium_web_driver().close_app()

    @SupportedBy(WebDriverPlatform._MOBILE)
    def terminate_app(self, app_id: str, timeout: int = 500) -> bool:
        """
            Terminates the application if it is running.

        :param app_id: the application id to be terminates

        The following options are available for Android:
        :param timeout: how much time to wait for the uninstall to complete. 500ms by default.

        :return: True if the app has been successfully terminated
        """
        options = {
            "timeout": timeout
        }
        return self._selenium_web_driver().terminate_app(app_id, **options)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def reset_app(self):
        """
            Resets the current application on the device.
        """
        self._selenium_web_driver().reset()

    @SupportedBy(WebDriverPlatform._MOBILE)
    def remove_app(self, app_id: str, keep_data: bool = False, timeout: int = 20000):
        """
            Remove the specified application from the device.

        :param app_id: the application id to be removed

        The following options are available for Android:
        :param keep_data: whether to keep application data and caches after it is uninstalled. False by default
        :param timeout: how much time to wait for the uninstall to complete. 20000ms by default.
        """
        options = {
            "keepData": keep_data,
            "timeout": timeout
        }
        self._selenium_web_driver().remove_app(app_id, **options)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def get_app_state(self, app_id: str) -> int:
        """
            Queries the state of the application.

        :param app_id: the application id to be queried

        :return: One of possible application state constants. See appium.webdriver.applicationstate.ApplicationState class for more details.
        """
        return self._selenium_web_driver().query_app_state(app_id)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def get_app_strings(self, language: str = None, string_file: str = None) -> dict:
        """
            Returns the application strings from the device for the specified language.

        :param language: strings language code
        :param string_file: the name of the string file to query
        """
        return self._selenium_web_driver().app_strings(language, string_file)

    @SupportedBy(WebDriverPlatform.ANDROID)
    def end_test_coverage(self, intent: str, path: str):
        """
            Ends the coverage collection and pull the coverage.ec file from the device.
            Android only.

            See https://github.com/appium/appium/blob/master/docs/en/android_coverage.md

         :param intent: description of operation to be performed
         :param path: path to coverage.ec file to be pulled from the device
        """
        self._selenium_web_driver().end_test_coverage(intent, path)

    # Files

    @SupportedBy(WebDriverPlatform._MOBILE)
    def push_file(self, destination_path: str, base64data: str = None, source_path: str = None):
        """
            Puts the data from the file at `source_path`, encoded as Base64, in the file specified as `path`.
            Specify either `base64data` or `source_path`, if both specified default to `source_path`

        :param destination_path: the location on the device/simulator where the local file contents should be saved
        :param base64data: file contents, encoded as Base64, to be written to the file on the device/simulator
        :param source_path: local file path for the file to be loaded on device
        """
        self._selenium_web_driver().push_file(destination_path, base64data, source_path)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def pull_file(self, path: str) -> str:
        """
            Retrieves the file at `path`. Returns the file's content encoded as Base64.

        :param path: the path to the file on the device
        """
        return self._selenium_web_driver().pull_file(path)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def pull_folder(self, path: str) -> str:
        """
            Retrieves a folder at `path`. Returns the folder's contents zipped and encoded as Base64.

         :param path: the path to the folder on the device
        """
        return self._selenium_web_driver().pull_folder(path)

    # Interactions todo: rotate

    @SupportedBy(WebDriverPlatform._MOBILE)
    def shake(self):
        """
            Shake the device.
        """
        self._selenium_web_driver().shake()

    @SupportedBy(WebDriverPlatform._MOBILE)
    def lock(self, duration: int = None):
        """
            Lock the device for a certain period of time.
            No changes are made if the device is already locked.

        :param duration: (optional) the duration to lock the device, in ms.
            The device is going to be locked forever until `unlock` is called if it equals or is less than zero,
            otherwise this call blocks until the timeout expires and unlocks the screen automatically.
        """
        self._selenium_web_driver().lock(int(duration / 1000.0))

    @SupportedBy(WebDriverPlatform.ANDROID)
    def unlock(self):
        """
            Unlock the device. No changes are made if the device is already unlocked.
        """
        self._selenium_web_driver().unlock()

    @SupportedBy(WebDriverPlatform.ANDROID)
    def is_locked(self) -> bool:
        """
            Checks whether the device is locked.

        :return: `True` if the device is locked
        """
        return self._selenium_web_driver().is_locked()

    @SupportedBy(WebDriverPlatform.IOS)
    def press_button(self, button_name: str):
        """
            Sends a physical button name to the device to simulate the user pressing. iOS only.
            Possible button names can be found in
            https://github.com/appium/WebDriverAgent/blob/master/WebDriverAgentLib/Categories/XCUIDevice%2BFBHelpers.h

        :param button_name: the button name to be sent to the device. volumeUp (real devices only), volumeDown (real device only), home
        """
        self._selenium_web_driver().press_button(button_name)

    # Keys

    @SupportedBy(WebDriverPlatform.ANDROID)
    def press_keycode(self, keycode: int, metastate: int = None, flags: int = None):
        """
            Sends a keycode to the device. Android only. Possible keycodes can be
            found in http://developer.android.com/reference/android/view/KeyEvent.html.

        :param keycode: the keycode to be sent to the device
        :param metastate: meta information about the keycode being sent
        :param flags: the set of key event flags
        """
        self._selenium_web_driver().press_keycode(keycode, metastate, flags)

    @SupportedBy(WebDriverPlatform.ANDROID)
    def long_press_keycode(self, keycode: int, metastate: int = None, flags: int = None):
        """
            Sends a long press of keycode to the device. Android only. Possible keycodes can be
            found in http://developer.android.com/reference/android/view/KeyEvent.html.

        :param keycode: the keycode to be sent to the device
        :param metastate: meta information about the keycode being sent
        :param flags: the set of key event flags
        """
        self._selenium_web_driver().long_press_keycode(keycode, metastate, flags)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def hide_keyboard(self, key_name: str = None, key: str = None, strategy: str = None):
        """
            Hides the software keyboard on the device. In iOS, use `key_name` to press
            a particular key, or `strategy`. In Android, no parameters are used.

        :param key_name: key to press
        :param key: key to press
        :param strategy: strategy for closing the keyboard (e.g., `tapOutside`)
        """
        self._selenium_web_driver().hide_keyboard(key_name, key, strategy)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def is_keyboard_shown(self) -> bool:
        """
            Attempts to detect whether a software keyboard is present.

        :return: Either True or False
        """
        return self._selenium_web_driver().is_keyboard_shown()

    @SupportedBy(WebDriverPlatform.ANDROID)
    def key_event(self, keycode: int, metastate: int = None):
        """
            Sends a keycode to the device. Android only. Possible keycodes can be
            found in http://developer.android.com/reference/android/view/KeyEvent.html.

        :param keycode: the keycode to be sent to the device
        :param metastate: meta information about the keycode being sent
        """
        self._selenium_web_driver().keyevent(keycode, metastate)

    # Network

    @SupportedBy(WebDriverPlatform.ANDROID)
    def toggle_location_services(self):
        """
            Toggle the location services on the device. Android only.
        """
        self._selenium_web_driver().toggle_location_services()

    @SupportedBy(WebDriverPlatform.ANDROID)
    def get_network_connection(self) -> int:
        """
            Returns an integer bitmask specifying the network connection type.
            Android only.
            Possible values are available through the enumeration `appium.webdriver.ConnectionType`
        """
        return self._selenium_web_driver().network_connection

    @SupportedBy(WebDriverPlatform.ANDROID)
    def set_network_connection(self, connection_type: int):
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
        self._selenium_web_driver().set_network_connection(connection_type)

    @SupportedBy(WebDriverPlatform.ANDROID)
    def set_network_speed(self, speed_type: str):
        """
            Set the network speed emulation. Android Emulator only.

        :param speed_type: The network speed type. A member of the const appium.webdriver.extensions.android.network.NetSpeed.
        """
        self._selenium_web_driver().set_network_speed(speed_type)

    # Performance Data

    @SupportedBy(WebDriverPlatform.ANDROID)
    def get_performance_data(self, package_name: str, data_type: str, data_read_timeout: int = None):
        """
            Returns the information of the system state which is supported to read as like cpu, memory, network traffic, and battery.

        :param package_name: The package name of the application
        :param data_type: The type of system state which wants to read.
            It should be one of the supported performance data types.
            Check `get_performance_data_types` for supported types
        :param data_read_timeout: The number of attempts to read
        :return: The data along to `data_type`

        :Usage:
            self.driver.get_performance_data('my.app.package', 'cpuinfo', 5)
        """
        return self._selenium_web_driver().get_performance_data(package_name, data_type, data_read_timeout)

    @SupportedBy(WebDriverPlatform.ANDROID)
    def get_performance_data_types(self) -> List[str]:
        """
            Returns the information types of the system state which is supported to read as like cpu, memory, network traffic, and battery.

        :return: Available data types
        """
        return self._selenium_web_driver().get_performance_data_types()

    # Simulator

    @SupportedBy(WebDriverPlatform.IOS)
    def perform_touch_id(self, match: bool):
        """
            Simulate touchId on iOS Simulator

        :param match: Simulates a successful touch (`True`) or a failed touch (`False`)
        """
        self._selenium_web_driver().touch_id(match)

    @SupportedBy(WebDriverPlatform.IOS)
    def toggle_touch_id_enrollment(self):
        """
            Toggle enroll touchId on iOS Simulator
        """
        self._selenium_web_driver().toggle_touch_id_enrollment()

    # System

    @SupportedBy(WebDriverPlatform.ANDROID)
    def get_system_bars(self) -> dict:
        """
            Retrieve visibility and bounds information of the status and navigation bars.

        :return: A dictionary whose keys are
            - statusBar
                - visible
                - x
                - y
                - width
                - height
            - navigationBar
                - visible
                - x
                - y
                - width
                - height
        """
        return self._selenium_web_driver().get_system_bars()

    @SupportedBy(WebDriverPlatform.ANDROID)
    def get_display_density(self) -> int:
        """
            Get the display density, Android only

        :return: The display density of the Android device(dpi)
        """
        return self._selenium_web_driver().get_display_density()

    @SupportedBy(WebDriverPlatform.ANDROID)
    def open_notifications(self):
        """
            Open notification shade in Android (API Level 18 and above)
        """
        self._selenium_web_driver().open_notifications()

    @SupportedBy(WebDriverPlatform._MOBILE)
    def get_device_time(self, format: str = None) -> str:
        """
            Returns the date and time from the device

        :param format: The set of format specifiers. Read https://momentjs.com/docs/ to get the full list of supported datetime format specifiers.
            If unset, return :func:`.device_time` as default format is `YYYY-MM-DDTHH:mm:ssZ`, which complies to ISO-8601

        :Usage:
            self.driver.get_device_time()
            self.driver.get_device_time("YYYY-MM-DD")
        """
        return self._selenium_web_driver().get_device_time(format)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def get_battery_info(self) -> dict:
        """
            Retrieves battery information for the device under test.

        :return: A dictionary containing the following entries
        - level: Battery level in range [0.0, 1.0], where 1.0 means 100% charge.
            Any value lower than 0 means the level cannot be retrieved
        - state: Platform-dependent battery state value.
            On iOS (XCUITest):
                - 1: Unplugged
                - 2: Charging
                - 3: Full
                Any other value means the state cannot be retrieved
            On Android (UIAutomator2):
                - 2: Charging
                - 3: Discharging
                - 4: Not charging
                - 5: Full
                Any other value means the state cannot be retrieved
        """
        return self._selenium_web_driver().battery_info

    # Power

    @SupportedBy(WebDriverPlatform.ANDROID)
    def set_power_capacity(self, percent: int):
        """
            Emulate power capacity change on the connected emulator.

        :param percent: The power capacity to be set. Can be set from 0 to 100
        """
        self._selenium_web_driver().set_power_capacity(percent)

    @SupportedBy(WebDriverPlatform.ANDROID)
    def set_power_ac(self, ac_state: str):
        """
            Emulate power state change on the connected emulator.

        :param ac_state: The power ac state to be set. A member of the const appium.webdriver.extensions.android.power.Power
        """
        self._selenium_web_driver().set_power_ac(ac_state)

    # GSM & SMS

    @SupportedBy(WebDriverPlatform.ANDROID)
    def make_gsm_call(self, phone_number: str, action: str):
        """
            Make GSM call (Emulator only)

        :param phone_number: The phone number to call to.
        :param action: The call action. A member of the const appium.webdriver.extensions.android.gsm.GsmCallActions

        :Usage:
            self.driver.make_gsm_call('5551234567', GsmCallActions.CALL)
        """
        self._selenium_web_driver().make_gsm_call(phone_number, action)

    @SupportedBy(WebDriverPlatform.ANDROID)
    def set_gsm_signal(self, strength: int):
        """
            Set GSM signal strength (Emulator only)

        :param strength: Signal strength. A member of the enum appium.webdriver.extensions.android.gsm.GsmSignalStrength

        :Usage:
            self.driver.set_gsm_signal(GsmSignalStrength.GOOD)
        """
        self._selenium_web_driver().set_gsm_signal(strength)

    @SupportedBy(WebDriverPlatform.ANDROID)
    def set_gsm_voice(self, state: str):
        """
            Set GSM voice state (Emulator only)

        :param state: State of GSM voice. A member of the const appium.webdriver.extensions.android.gsm.GsmVoiceState

        :Usage:
            self.driver.set_gsm_voice(GsmVoiceState.HOME)
        """
        self._selenium_web_driver().set_gsm_voice(state)

    @SupportedBy(WebDriverPlatform.ANDROID)
    def send_sms(self, phone_number: str, message: str):
        """
            Emulate send SMS event on the connected emulator.

        :param phone_number: The phone number of message sender
        :param message: The message to send

        :Usage:
            self.driver.send_sms('555-123-4567', 'Hey lol')
        """
        self._selenium_web_driver().send_sms(phone_number, message)

    # Authentication

    @SupportedBy(WebDriverPlatform.ANDROID)
    def perform_finger_print(self, finger_id: int):
        """
            Authenticate users by using their finger print scans on supported emulators. Android only.

        :param finger_id: Finger prints stored in Android Keystore system (from 1 to 10)
        """
        return self._selenium_web_driver().finger_print(finger_id)

    # Context

    @SupportedBy(WebDriverPlatform._MOBILE)
    def get_contexts(self) -> List[str]:
        """
            Returns the contexts within the current session.
        """
        return self._selenium_web_driver().contexts

    @SupportedBy(WebDriverPlatform._MOBILE)
    def get_current_context(self) -> str:
        """
            Returns the current context of the current session.
        """
        return self._selenium_web_driver().current_context

    @SupportedBy(WebDriverPlatform._MOBILE)
    def switch_to_context(self, context_partial_name: str):
        """
            Sets the context for the current session.

        :param context_partial_name: The partial name of the context to switch to

        :Usage:
            driver.switch_to_context('WEBVIEW_1')
        """
        if context_partial_name == "NATIVE_APP":
            self._selenium_web_driver().switch_to.context(context_partial_name)
            self.__web_driver_info.context = WebDriverContext.NATIVE_APP
        else:
            contexts = {"inner": []}

            def get_contexts(partial_name):
                try:
                    contexts["inner"] = [context for context in self.get_contexts() if partial_name in context]
                    return contexts["inner"]
                except WebDriverException as e:
                    return []

            def context_available(partial_name):
                return len(get_contexts(partial_name)) > 0

            self.waiter().wait_for(context_available, partial_name=context_partial_name)
            self._selenium_web_driver().switch_to.context(contexts["inner"][0])
            self.__web_driver_info.context = WebDriverContext.WEB_VIEW

    # Window

    def get_current_window_handle(self) -> str:
        """
            Returns the handle of the current window.
        """
        return self._selenium_web_driver().current_window_handle

    def get_window_handles(self) -> List[str]:
        """
            Returns the handles of all windows within the current session.
        """
        return self._selenium_web_driver().window_handles

    def switch_to_window(self, window_handle: str):
        """
            Switches focus to the specified window.

        :param window_handle: The name or window handle of the window to switch to.

        :Usage:
            driver.switch_to_window('main')
        """
        self._selenium_web_driver().switch_to.window(window_handle)

    def switch_to_new_window(self, previous_window_handles: List[str]):
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
            new_window_handles["inner"] = [handle for handle in self.get_window_handles() if
                                           handle not in previous_window_handles]
            return new_window_handles["inner"]

        def new_window_opened():
            return len(get_new_window_handles()) > 0

        self.waiter().wait_for(new_window_opened)
        self.switch_to_window(new_window_handles["inner"][0])

    def maximize_window(self):
        """
            Maximizes the current window that webdriver is using
        """
        self._selenium_web_driver().maximize_window()

    def fullscreen_window(self):
        """
            Invokes the window manager-specific 'full screen' operation
        """
        self._selenium_web_driver().fullscreen_window()

    def set_window_size(self, width: int, height: int, window_handle: str = "current"):
        """
            Sets the width and height of the specified window.

        :param width: the width in pixels to set the window to
        :param height: the height in pixels to set the window to
        :param window_handle: The name or window handle of the window to set, default is current window.

        :Usage:
            driver.set_window_size(800,600)
        """
        self._selenium_web_driver().set_window_size(width, height, window_handle)

    def get_window_size(self, window_handle: str = "current"):
        """
            Gets the width and height of the specified window.

        :param window_handle: The name or window handle of the window to get, default is current window.
        """
        return self._selenium_web_driver().get_window_size(window_handle)

    def set_window_position(self, x: int, y: int, window_handle: str = "current"):
        """
            Sets the x, y position of the specified window.

        :param x: the x-coordinate in pixels to set the window position
        :param y: the y-coordinate in pixels to set the window position
        :param window_handle: The name or window handle of the window to set, default is current window.

        :Usage:
            driver.set_window_position(0,0)
        """
        self._selenium_web_driver().set_window_position(x, y, window_handle)

    def get_window_position(self, window_handle: str = "current") -> dict:
        """
            Gets the x, y position of the specified window.

        :param window_handle: The name or window handle of the window to get, default is current window.
        """
        return self._selenium_web_driver().get_window_position(window_handle)

    def get_window_rect(self) -> dict:
        """
            Gets the x, y coordinates of the window as well as height and width of the current window.
        """
        return self._selenium_web_driver().get_window_rect()

    def set_window_rect(self, x: int = None, y: int = None, width: int = None, height: int = None):
        """
            Sets the x, y coordinates of the window as well as height and width of the current window.
        """
        self._selenium_web_driver().set_window_rect(x, y, width, height)

    def get_viewport_size(self) -> dict:
        """
            Gets the width and height of viewport.
        """
        return self._selenium_web_driver().execute_script("return {width: window.innerWidth, height: window.innerHeight};")

    def set_viewport_size(self, width: int, height: int):
        """
            Sets the width and height of viewport. When changes the viewport size, the window size will be also changed.

        :param width: the width in pixels to set viewport to
        :param height: the height in pixels to set viewport to
        """
        window_size = self._selenium_web_driver().execute_script("""
                return [window.outerWidth - window.innerWidth + arguments[0],
                  window.outerHeight - window.innerHeight + arguments[1]];
                """, width, height)
        self._selenium_web_driver().set_window_size(*window_size)

    def get_title(self) -> str:
        """
            Returns the title of the current page.
        """
        return self._selenium_web_driver().title

    def get_current_url(self) -> str:
        """
            Gets the URL of the current page.
        """
        return self._selenium_web_driver().current_url

    def get_page_source(self) -> str:
        """
            Gets the source of the current page.
        """
        return self._selenium_web_driver().page_source

    def close_window(self, window_handle: str = "current"):
        """
            Close the specified window.

        :param window_handle: The name or window handle of the window to close, default is current window.
        """
        if window_handle == "current" or window_handle == self.get_current_window_handle():
            self._selenium_web_driver().close()
        else:
            current_window_handle = self.get_current_window_handle()
            self.switch_to_window(window_handle)
            self._selenium_web_driver().close()
            self.switch_to_window(current_window_handle)

    # Navigation

    def get(self, url: str):
        """
            Loads a web page in the current browser session.

        :param url: the url to be open
        """
        self._selenium_web_driver().get(url)

    def refresh(self):
        """
            Refreshes the current page.
        """
        self._selenium_web_driver().refresh()

    def back(self):
        """
            Goes one step backward in the browser history.
        """
        self._selenium_web_driver().back()

    def forward(self):
        """
            Goes one step forward in the browser history.
        """
        self._selenium_web_driver().forward()

    # Storage

    def get_cookie(self, name: str) -> dict:
        """
            Get a single cookie by name. Returns the cookie if found, None if not.

        :param name: the cookie name
        """
        return self._selenium_web_driver().get_cookie(name)

    def get_cookies(self) -> List[dict]:
        """
            Returns a set of dictionaries, corresponding to cookies visible in the current session.
        """
        return self._selenium_web_driver().get_cookies()

    def add_cookie(self, cookie_dict: dict):
        """
            Adds a cookie to your current session.

        :param cookie_dict: A dictionary object, with required keys - "name" and "value";
            optional keys - "path", "domain", "secure", "expiry"

        Usage:
            driver.add_cookie({'name' : 'foo', 'value' : 'bar'})
            driver.add_cookie({'name' : 'foo', 'value' : 'bar', 'path' : '/'})
            driver.add_cookie({'name' : 'foo', 'value' : 'bar', 'path' : '/', 'secure':True})
        """
        self._selenium_web_driver().add_cookie(cookie_dict)

    def delete_cookie(self, name: str):
        """
            Deletes a single cookie with the given name.

        :param name: the cookie name
        """
        self._selenium_web_driver().delete_cookie(name)

    def delete_all_cookies(self):
        """
            Delete all cookies in the scope of the session.
        """
        self._selenium_web_driver().delete_all_cookies()

    # Frame

    def switch_to_frame(self, frame_reference: Union[int, str, "Element"]):
        """
            Switches focus to the specified frame, by index (zero-based), locator, or element.

        :param frame_reference: an integer representing the index, the locator of the frame to switch to,
                            or a element that is an (i)frame to switch to.

        :Usage:
            driver.switch_to_frame(1)
            driver.switch_to_frame("name=myIframe")
            driver.switch_to_frame(StaticElement(driver, "tag=iframe"))
        """
        from .element import Element
        from .static_element import StaticElement

        if isinstance(frame_reference, int):
            frame_element = StaticElement(self, "xpath=(.//iframe)[%s]" % (frame_reference + 1))
        elif isinstance(frame_reference, str):
            frame_element = StaticElement(self, frame_reference)
        elif isinstance(frame_reference, Element):
            frame_element = frame_reference
        else:
            raise ValueError("Frame reference type %s is not supported." % type(frame_reference))
        frame_element.wait_for().exists()
        self._selenium_web_driver().switch_to.frame(frame_element._selenium_element())

    def switch_to_parent_frame(self):
        """
            Switches focus to the parent context. If the current context is the top
            level browsing context, the context remains unchanged.
        """
        self._selenium_web_driver().switch_to.parent_frame()

    def switch_to_default_content(self):
        """
            Selects either the first frame on the page, or the main document when a page contains iframes.
        """
        self._selenium_web_driver().switch_to.default_content()

    # IME engine

    @SupportedBy(WebDriverPlatform.ANDROID)
    def get_available_ime_engines(self) -> List[str]:
        """
            Get the available input methods for an Android device. Package and
            activity are returned (e.g., ['com.android.inputmethod.latin/.LatinIME'])
            Android only.
        """
        return self._selenium_web_driver().available_ime_engines

    @SupportedBy(WebDriverPlatform.ANDROID)
    def is_ime_service_active(self) -> bool:
        """
            Checks whether the device has IME service active. Returns True/False.
            Android only.
        """
        return self._selenium_web_driver().is_ime_active()

    @SupportedBy(WebDriverPlatform.ANDROID)
    def active_ime_engine(self, engine: str):
        """
            Activates the given IME engine on the device.
            Android only.

        :param engine: the package and activity of the IME engine to activate (e.g., 'com.android.inputmethod.latin/.LatinIME')
        """
        self._selenium_web_driver().activate_ime_engine(engine)

    @SupportedBy(WebDriverPlatform.ANDROID)
    def deactivate_current_ime_engine(self):
        """
            Deactivates the currently active IME engine on the device.
            Android only.
        """
        self._selenium_web_driver().deactivate_ime_engine()

    @SupportedBy(WebDriverPlatform.ANDROID)
    def get_current_ime_engine(self) -> str:
        """
            Returns the activity and package of the currently active IME engine (e.g., 'com.android.inputmethod.latin/.LatinIME').
            Android only.
        """
        return self._selenium_web_driver().active_ime_engine

    # Alert

    def switch_to_alert(self) -> Alert:
        """
            Switches focus to an alert on the page.

        :return: the Alert instance
        """
        self.wait_for().alert_present()
        return Alert(self._selenium_web_driver().switch_to.alert)

    def get_alert(self) -> Alert:
        """
            Switches focus to an alert on the page.

        :return: the Alert instance
        """
        return self.switch_to_alert()

    def is_alert_present(self) -> bool:
        """
            Return whether the alert is present on the page or not.
        """
        try:
            alert_text = self._selenium_web_driver().switch_to.alert.text
            return True
        except WebDriverException as e:
            return False

    # Screenshot and recording

    def get_screenshot_as_file(self, filename: str) -> bool:
        """
            Gets the screenshot of the current window. Returns False if there is
           any IOError, else returns True. Use full paths in your filename.

        :param filename: The full path you wish to save your screenshot to.

        :Usage:
            driver.get_screenshot_as_file('/Screenshots/foo.png')
        """
        return self._selenium_web_driver().get_screenshot_as_file(filename)

    def save_screenshot(self, filename: str) -> bool:
        """
            Gets the screenshot of the current window. Returns False if there is any IOError, else returns True. Use full paths in your filename.

        :param filename: The full path you wish to save your screenshot to.

        :Usage:
            driver.save_screenshot('/Screenshots/foo.png')
        """
        return self.get_screenshot_as_file(filename)

    def get_screenshot_as_png(self) -> bytes:
        """
            Gets the screenshot of the current window as a binary data.

        :Usage:
            driver.get_screenshot_as_png()
        """
        return self._selenium_web_driver().get_screenshot_as_png()

    def get_screenshot_as_base64(self) -> str:
        """
            Gets the screenshot of the current window as a base64 encoded string
            which is useful in embedded images in HTML.

        :Usage:
            driver.get_screenshot_as_base64()
        """
        return self._selenium_web_driver().get_screenshot_as_base64()

    @SupportedBy(WebDriverPlatform._MOBILE)
    def start_recording_screen(self, remote_path: str = None, user: str = None, password: str = None, method: str = None, time_limit: int = None, forced_restart: bool = None,
                               file_field_name: str = None, form_fields: dict = None, headers: dict = None, video_quality: str = None, video_type: str = None,
                               video_fps: int = None, video_filters: str = None, video_scale: str = None, pixel_format: str = None, video_size: str = None, bit_rate: int = None,
                               bug_report: str = None, fps: int = None, capture_cursor: bool = None, capture_click: bool = None, device_id: int = None,
                               preset: str = None) -> bytes:
        """
            Start asynchronous screen recording process.

            +--------------+-----+---------+-----+-------+
            | Keyword Args | iOS | Android | Win | macOS |
            +==============+=====+=========+=====+=======+
            | remotePath   | O   | O       | O   | O     |
            +--------------+-----+---------+-----+-------+
            | user         | O   | O       | O   | O     |
            +--------------+-----+---------+-----+-------+
            | password     | O   | O       | O   | O     |
            +--------------+-----+---------+-----+-------+
            | method       | O   | O       | O   | O     |
            +--------------+-----+---------+-----+-------+
            | timeLimit    | O   | O       | O   | O     |
            +--------------+-----+---------+-----+-------+
            | forceRestart | O   | O       | O   | O     |
            +--------------+-----+---------+-----+-------+
            | fileFieldName| O   | O       | O   | O     |
            +--------------+-----+---------+-----+-------+
            | formFields   | O   | O       | O   | O     |
            +--------------+-----+---------+-----+-------+
            | headers      | O   | O       | O   | O     |
            +--------------+-----+---------+-----+-------+
            | videoQuality | O   |         |     |       |
            +--------------+-----+---------+-----+-------+
            | videoType    | O   |         |     |       |
            +--------------+-----+---------+-----+-------+
            | videoFps     | O   |         |     |       |
            +--------------+-----+---------+-----+-------+
            | videoFilter  | O   |         | O   | O     |
            +--------------+-----+---------+-----+-------+
            | videoScale   | O   |         |     |       |
            +--------------+-----+---------+-----+-------+
            | pixelFormat  | O   |         |     |       |
            +--------------+-----+---------+-----+-------+
            | videoSize    |     | O       |     |       |
            +--------------+-----+---------+-----+-------+
            | bitRate      |     | O       |     |       |
            +--------------+-----+---------+-----+-------+
            | bugReport    |     | O       |     |       |
            +--------------+-----+---------+-----+-------+
            | fps          |     |         | O   | O     |
            +--------------+-----+---------+-----+-------+
            | captureCursor|     |         | O   | O     |
            +--------------+-----+---------+-----+-------+
            | captureClicks|     |         | O   | O     |
            +--------------+-----+---------+-----+-------+
            | deviceId     |     |         |     | O     |
            +--------------+-----+---------+-----+-------+
            | preset       |     |         | O   | O     |
            +--------------+-----+---------+-----+-------+
            | audioInput   |     |         | O   |       |
            +--------------+-----+---------+-----+-------+

        :param remote_path: The remotePath upload option is the path to the remote location,
                where the resulting video from the previous screen recording should be uploaded.
                The following protocols are supported: http/https (multipart), ftp.
                Missing value (the default setting) means the content of the resulting
                file should be encoded as Base64 and passed as the endpoint response value, but
                an exception will be thrown if the generated media file is too big to
                fit into the available process memory.
                This option only has an effect if there is/was an active screen recording session
                and forced restart is not enabled (the default setting).
        :param user: The name of the user for the remote authentication.
                Only has an effect if both `remotePath` and `password` are set.
        :param password: The password for the remote authentication.
                Only has an effect if both `remotePath` and `user` are set.
        :param method: The HTTP method name ('PUT'/'POST'). PUT method is used by default.
                Only has an effect if `remotePath` is set.
        :param time_limit: The actual time limit of the recorded video in seconds.
                The default value for both iOS and Android is 180 seconds (3 minutes).
                The default value for macOS is 600 seconds (10 minutes).
                The maximum value for Android is 3 minutes.
                The maximum value for iOS is 10 minutes.
                The maximum value for macOS is 10000 seconds (166 minutes).
        :param forced_restart: Whether to ignore the result of previous capture and start a new recording
                immediately (`True` value). By default  (`False`) the endpoint will try to catch and
                return the result of the previous capture if it's still available.
        :param file_field_name: [multipart/form-data requests] The name of the form field
                containing the binary payload. "file" by default. (Since Appium 1.18.0)
        :param form_fields: [multipart/form-data requests] Additional form fields mapping. If any entry has
                the same key as `fileFieldName` then it is going to be ignored. (Since Appium 1.18.0)
        :param headers: [multipart/form-data requests] Headers mapping (Since Appium 1.18.0)

        :param video_quality: [iOS] The video encoding quality: 'low', 'medium', 'high', 'photo'. Defaults to 'medium'.
        :param video_type: [iOS] The format of the screen capture to be recorded.
                Available formats: Execute `ffmpeg -codecs` in the terminal to see the list of supported video codecs.
                'mjpeg' by default. (Since Appium 1.10.0)
        :param video_fps: [iOS] The Frames Per Second rate of the recorded video. Change this value if the
                resulting video is too slow or too fast. Defaults to 10. This can decrease the resulting file size.
        :param video_filters: [iOS, Win, macOS] The FFMPEG video filters to apply. These filters allow to scale,
                flip, rotate and do many other useful transformations on the source video stream. The format of the
                property must comply with https://ffmpeg.org/ffmpeg-filters.html. (Since Appium 1.15)
        :param video_scale: [iOS] The scaling value to apply. Read https://trac.ffmpeg.org/wiki/Scaling for
                possible values. No scale is applied by default. If videoFilters are set then the scale setting is
                effectively ignored. (Since Appium 1.10.0)
        :param pixel_format: [iOS] Output pixel format. Run `ffmpeg -pix_fmts` to list possible values.
                For Quicktime compatibility, set to "yuv420p" along with videoType: "libx264". (Since Appium 1.12.0)

        :param video_size: [Android] The video size of the generated media file. The format is WIDTHxHEIGHT.
                The default value is the device's native display resolution (if supported),
                1280x720 if not. For best results, use a size supported by your device's
                Advanced Video Coding (AVC) encoder.
        :param bit_rate: [Android] The video bit rate for the video, in megabits per second.
                The default value is 4. You can increase the bit rate to improve video quality,
                but doing so results in larger movie files.
        :param bug_report: [Android] Makes the recorder to display an additional information on the video overlay,
                such as a timestamp, that is helpful in videos captured to illustrate bugs.
                This option is only supported since API level 27 (Android P).

        :param fps: [Win, macOS] The count of frames per second in the resulting video.
                Increasing fps value also increases the size of the resulting video file and the CPU usage.
        :param capture_cursor: [Win, macOS] Whether to capture the mouse cursor while recording the screen.
                Disabled by default.
        :param capture_click: [Win, macOS] Whether to capture the click gestures while recording the screen.
                Disabled by default.
        :param device_id: [macOS] Screen device index to use for the recording.
                The list of available devices could be retrieved using
                `ffmpeg -f avfoundation -list_devices true -i` command.
                This option is mandatory and must be always provided.
        :param preset: [Win, macOS] A preset is a collection of options that will provide a certain encoding
                speed to compression ratio. A slower preset will provide better compression
                (compression is quality per filesize). This means that, for example, if you target a certain file size
                or constant bit rate, you will achieve better quality with a slower preset.
                Read https://trac.ffmpeg.org/wiki/Encode/H.264 for more details.
                Possible values are 'ultrafast', 'superfast', 'veryfast'(default), 'faster', 'fast', 'medium', 'slow',
                'slower', 'veryslow'

        :return: bytes: Base-64 encoded content of the recorded media if `stop_recording_screen` isn't called after previous `start_recording_screen`.
                Otherwise returns an empty string.
        """
        options = {
            "remotePath": remote_path,
            "user": user,
            "password": password,
            "method": method,
            "timeLimit": time_limit,
            "forcedRestart": forced_restart,
            "fileFieldName": file_field_name,
            "formFields": form_fields,
            "headers": headers,
            "videoQuality": video_quality,
            "videoType": video_type,
            "videoFps": video_fps,
            "videoFilters": video_filters,
            "videoScale": video_scale,
            "pixelFormat": pixel_format,
            "videoSize": video_size,
            "bitRate": bit_rate,
            "bugReport": bug_report,
            "fps": fps,
            "captureCursor": capture_cursor,
            "captureClick": capture_click,
            "deviceId": device_id,
            "preset": preset
        }
        return self._selenium_web_driver().start_recording_screen(**options)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def stop_recording_screen(self, remote_path: str = None, user: str = None, password: str = None, method: str = None, file_field_name: str = None,
                              form_fields: dict = None, headers: dict = None) -> bytes:
        """
            Gather the output from the previously started screen recording to a media file.
            
        :param remote_path: The remote_path upload option is the path to the remote location,
            where the resulting video should be uploaded.
            The following protocols are supported: http/https (multipart), ftp.
            Missing value (the default setting) means the content of the resulting
            file should be encoded as Base64 and passed as the endpoint response value, but
            an exception will be thrown if the generated media file is too big to
            fit into the available process memory.
        :param user: The name of the user for the remote authentication.
            Only has an effect if both `remote_path` and `password` are set.
        :param password: The password for the remote authentication.
            Only has an effect if both `remote_path` and `user` are set.
        :param method: The HTTP method name ('PUT'/'POST'). PUT method is used by default.
            Only has an effect if `remote_path` is set.
        :param file_field_name: [multipart/form-data requests] The name of the form field
            containing the binary payload. "file" by default. (Since Appium 1.18.0)
        :param form_fields: [multipart/form-data requests] Additional form fields mapping. If any entry has
            the same key as `fileFieldName` then it is going to be ignored. (Since Appium 1.18.0)
        :param headers: [multipart/form-data requests] Headers mapping (Since Appium 1.18.0)
        
        :return: Base-64 encoded content of the recorded media file or an empty string if the file has been successfully uploaded to a remote location
                (depends on the actual `remote_path` value).
        """
        options = {
            "remotePath": remote_path,
            "user": user,
            "password": password,
            "method": method,
            "fileFieldName": file_field_name,
            "formFields": form_fields,
            "headers": headers
        }
        return self._selenium_web_driver().stop_recording_screen(**options)

    # clipboard

    @SupportedBy(WebDriverPlatform._MOBILE)
    def set_clipboard(self, content: bytes, content_type: str = ClipboardContentType.PLAINTEXT, label: str = None):
        """
            Set the content of the system clipboard.

        :param content: The content to be set as bytearray string
        :param content_type: One of enum appium.webdriver.clipboard_content_type.ClipboardContentType items.
            Only ClipboardContentType.PLAINTEXT is supported on Android
        :param label: Optional label argument, which only works for Android
        """
        self._selenium_web_driver().set_clipboard(content, content_type, label)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def set_clipboard_text(self, text: str, label: str = None):
        """
            Copies the given text to the system clipboard.

        :param text: The text to be set
        :param label: Optional label argument, which only works for Android
        """
        self._selenium_web_driver().set_clipboard_text(text, label)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def get_clipboard(self, content_type: str = ClipboardContentType.PLAINTEXT) -> bytes:
        """
            Receives the content of the system clipboard.

        :param content_type: enum appium.webdriver.clipboard_content_type.ClipboardContentType items.
            Only ClipboardContentType.PLAINTEXT is supported on Android
        :return: Clipboard content as base64-encoded string or an empty string if the clipboard is empty
        """
        return self._selenium_web_driver().get_clipboard(content_type)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def get_clipboard_text(self) -> str:
        """
            Receives the text of the system clipboard.

        :return: The actual clipboard text or an empty string if the clipboard is empty
        """
        return self._selenium_web_driver().get_clipboard_text()

    # Touch Actions

    @SupportedBy(WebDriverPlatform._MOBILE)
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = None):
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
        self._selenium_web_driver().swipe(start_x, start_y, end_x, end_y, duration)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def flick(self, start_x: int, start_y: int, end_x: int, end_y: int):
        """
            Flick from one point to another point.

        :param start_x - x-coordinate at which to start
        :param start_y - y-coordinate at which to start
        :param end_x - x-coordinate at which to stop
        :param end_y - y-coordinate at which to stop

        :Usage:
            driver.flick(100, 100, 100, 400)
        """
        self._selenium_web_driver().flick(start_x, start_y, end_x, end_y)

    @SupportedBy(WebDriverPlatform._MOBILE)
    def scroll(self, direction: str):
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

    def scroll_to(self, element: "Element"):
        """
            Scrolls to the given element.

        :param element: the element to be scrolled to
        """
        element.scroll_into_view()

    def __str__(self):
        return "WebDriver <Platform: %s><Context: %s><SessionId: %s>" % (
            self.get_web_driver_info().platform, self.get_web_driver_info().context,
            self._selenium_web_driver().session_id)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()


class Ie(WebDriver):
    def __init__(self, service: IeService = None, options: IeOptions = None):
        """
            Creates a new instance of Ie.

        :param service: IE Service instance, providing service
        :param options: IE Options instance, providing additional options
        """
        web_driver_info = WebDriverInfo(WebDriverPlatform.PC, WebDriverContext.IE)
        selenium_web_driver = SeleniumIe(options=options, service=service)
        WebDriver.__init__(self, selenium_web_driver=selenium_web_driver, web_driver_info=web_driver_info)


class Firefox(WebDriver):
    def __init__(self, service: FirefoxService = None, options: FirefoxOptions = None):
        """
            Creates a new instance of Firefox.

        :param service: Firefox Service instance, providing service
        :param options: Firefox Options instance, providing additional options
        """
        web_driver_info = WebDriverInfo(WebDriverPlatform.PC, WebDriverContext.FIREFOX)
        selenium_web_driver = SeleniumFirefox(service=service, options=options)
        WebDriver.__init__(self, selenium_web_driver=selenium_web_driver, web_driver_info=web_driver_info)


class Chrome(WebDriver):
    def __init__(self, service: ChromeService = None, options: ChromeOptions = None):
        """
            Creates a new instance of Chrome.

        :param service: Chrome Service instance, providing service
        :param options: Chrome Options instance, providing additional options
        """
        web_driver_info = WebDriverInfo(WebDriverPlatform.PC, WebDriverContext.CHROME)
        selenium_web_driver = SeleniumChrome(service=service, options=options)
        WebDriver.__init__(self, selenium_web_driver=selenium_web_driver, web_driver_info=web_driver_info)


class Opera(WebDriver):
    def __init__(self, options: OperaOptions = None):
        """
            Creates a new instance of Opera.

        :param options: Opera Options instance, providing additional options
        """
        web_driver_info = WebDriverInfo(WebDriverPlatform.PC, WebDriverContext.OPERA)
        selenium_web_driver = SeleniumOpera(options=options)
        WebDriver.__init__(self, selenium_web_driver=selenium_web_driver, web_driver_info=web_driver_info)


class Safari(WebDriver):
    def __init__(self, service: SafariService = None, options: SafariOptions = None):
        """
            Creates a new instance of Safari.

        :param service: Safari Service instance, providing service
        :param options: Safari Options instance, providing additional options
        """
        web_driver_info = WebDriverInfo(WebDriverPlatform.PC, WebDriverContext.SAFARI)
        selenium_web_driver = SeleniumSafari(service=service, options=options)
        WebDriver.__init__(self, selenium_web_driver=selenium_web_driver, web_driver_info=web_driver_info)


class Edge(WebDriver):
    def __init__(self, service: EdgeService = None, options: EdgeOptions = None):
        """
            Creates a new instance of Edge.

        :param service: Edge Service instance, providing service
        :param options: Edge Options instance, providing additional options
        """
        web_driver_info = WebDriverInfo(WebDriverPlatform.PC, WebDriverContext.EDGE)
        selenium_web_driver = SeleniumEdge(service=service, options=options)
        WebDriver.__init__(self, selenium_web_driver=selenium_web_driver, web_driver_info=web_driver_info)


class Appium(WebDriver):
    def __init__(self, command_executor: str = "http://127.0.0.1:4444/wd/hub", desired_capabilities: dict = None,
                 browser_profile: str = None, proxy: object = None, keep_alive: bool = False,
                 direct_connection: bool = True, extensions=[], strict_ssl: bool = True):
        """
            Create a new driver that will issue commands using the wire protocol.

        :param command_executor: Either a string representing URL of the remote server or a custom remote_connection.RemoteConnection object. Defaults to 'http://127.0.0.1:4444/wd/hub'.
        :param desired_capabilities: A dictionary of capabilities to request when starting the browser session. Required parameter.
        :param browser_profile: A selenium.webdriver.firefox.firefox_profile.FirefoxProfile object. Only used if Firefox is requested. Optional.
        :param proxy: A selenium.webdriver.common.proxy.Proxy object. The browser session will be started with given proxy settings, if possible. Optional.
        :param keep_alive: Whether to configure remote_connection.RemoteConnection to use HTTP keep-alive. Defaults to False.
        """
        if "platformName" in desired_capabilities:
            platform = {
                "ios": WebDriverPlatform.IOS,
                "android": WebDriverPlatform.ANDROID
            }.get(desired_capabilities["platformName"].lower(), WebDriverPlatform.IOS)
        else:
            platform = WebDriverPlatform.IOS

        web_driver_info = WebDriverInfo(platform, WebDriverContext.NATIVE_APP)

        selenium_web_driver = AppiumWebDriver(command_executor=command_executor, desired_capabilities=desired_capabilities,
                                              browser_profile=browser_profile, proxy=proxy, keep_alive=keep_alive,
                                              direct_connection=direct_connection, extensions=extensions, strict_ssl=strict_ssl)
        # avoid that "autoWebview" in desired_capabilities affects the default context
        if web_driver_info.context == WebDriverContext.NATIVE_APP and selenium_web_driver.current_context != "NATIVE_APP":
            web_driver_info.context = WebDriverContext.WEB_VIEW

        WebDriver.__init__(self, selenium_web_driver=selenium_web_driver, web_driver_info=web_driver_info)
