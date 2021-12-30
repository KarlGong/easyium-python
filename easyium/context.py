from typing import Union, Callable, List, TYPE_CHECKING

from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from appium.webdriver.webelement import WebElement as AppiumElement
from selenium.common.exceptions import StaleElementReferenceException as SeleniumStaleElementReferenceException, NoSuchElementException as SeleniumNoSuchElementException, \
    InvalidSelectorException as SeleniumInvalidSelectorException, WebDriverException as SeleniumWebDriverException

from .exceptions import InvalidLocatorException, NoSuchElementException, EasyiumException, TimeoutException, ElementTimeoutException
from .identifier import Identifier
from .locator import locator_to_by_value
from .waiter import Waiter, WebDriverWaitFor, ElementWaitFor

if TYPE_CHECKING:
    from .dynamic_element import DynamicElement
    from .web_driver import WebDriver, WebDriverInfo


class Context:
    def __init__(self):
        self.__wait_interval = None
        self.__wait_timeout = None

    def get_web_driver(self) -> "WebDriver":
        pass

    def get_web_driver_info(self) -> "WebDriverInfo":
        pass

    def _selenium_context(self) -> Union[AppiumWebDriver, AppiumElement]:
        pass

    def _refresh(self):
        pass

    def persist(self):
        pass

    def get_screenshot_as_file(self, filename: str) -> bool:
        pass

    def save_screenshot(self, filename: str) -> bool:
        pass

    def get_screenshot_as_png(self) -> bytes:
        pass

    def get_screenshot_as_base64(self) -> str:
        pass

    def get_wait_interval(self) -> int:
        """
            Get the wait interval of this context.
            If the wait interval for element is not set, return the driver's wait interval.

        :return: the wait interval
        """
        if self.__wait_interval is not None:
            return self.__wait_interval
        return self.get_web_driver().get_wait_interval()

    def set_wait_interval(self, interval: int):
        """
            Set the wait interval of this context.

        :param interval: the new wait interval (in milliseconds)
        """
        self.__wait_interval = interval

    def get_wait_timeout(self) -> int:
        """
            Get the wait timeout of this context.
            If the wait timeout for element is not set, return the driver's wait timeout.

        :return: the wait timeout
        """
        if self.__wait_timeout is not None:
            return self.__wait_timeout
        return self.get_web_driver().get_wait_timeout()

    def set_wait_timeout(self, timeout: int):
        """
            Set the wait timeout of this context.

        :param timeout: the new wait timeout (in milliseconds)
        """
        self.__wait_timeout = timeout

    def wait_for(self, interval=None, timeout=None) -> Union[ElementWaitFor, WebDriverWaitFor]:
        pass

    def waiter(self, interval: int = None, timeout: int = None):
        """
            Get a Waiter instance.

        :param interval: the wait interval (in milliseconds). If None, use context's wait interval.
        :param timeout: the wait timeout (in milliseconds). If None, use context's wait interval.
        """
        _interval = self.get_wait_interval() if interval is None else interval
        _timeout = self.get_wait_timeout() if timeout is None else timeout
        return Waiter(_interval, _timeout)

    def _find_selenium_element(self, locator: str) -> AppiumElement:
        by, value = locator_to_by_value(locator)
        try:
            try:
                return self._selenium_context().find_element(by, value)
            except SeleniumStaleElementReferenceException:
                self._refresh()
                return self._selenium_context().find_element(by, value)
        except SeleniumInvalidSelectorException:
            raise InvalidLocatorException("The value <%s> of locator <%s> is not a valid expression." % (value, locator), self)
        except SeleniumNoSuchElementException:
            raise NoSuchElementException("Cannot find element by <%s> under:" % locator, self)
        except SeleniumWebDriverException as wde:
            raise EasyiumException(wde.msg, self)

    def has_child(self, locator: str) -> bool:
        """
            Whether this context has a child element.

        :param locator:
            the locator (relative to this context) of the child element.
            The format of locator is: "by=value", the possible values of "by" are::

                "id": By.ID
                "xpath": By.XPATH
                "link": By.LINK_TEXT
                "partial_link": By.PARTIAL_LINK_TEXT
                "name": By.NAME
                "tag": By.TAG_NAME
                "class": By.CLASS_NAME
                "css": By.CSS_SELECTOR
                "ios_pre": MobileBy.IOS_PREDICATE
                "ios_ui": MobileBy.IOS_UIAUTOMATION
                "ios_class": MobileBy.IOS_CLASS_CHAIN
                "android_ui": MobileBy.ANDROID_UIAUTOMATOR
                "android_tag": MobileBy.ANDROID_VIEWTAG
                "android_data": MobileBy.ANDROID_DATA_MATCHER
                "acc_id": MobileBy.ACCESSIBILITY_ID
                "custom": MobileBy.CUSTOM
        :return: whether this context has a child element.
        """
        return self.find_element(locator) is not None

    def find_element(self, locator: str, identifier: Callable[["DynamicElement"], str] = Identifier.id, condition: Callable[["DynamicElement"], bool] = lambda element: True) \
            -> "DynamicElement":
        """
            Find a DynamicElement under this context.
            Note: if no element is found, None will be returned.

        :param locator:
            the locator (relative to this context) of the element to be found.
            The format of locator is: "by=value", the possible values of "by" are::

                "id": By.ID
                "xpath": By.XPATH
                "link": By.LINK_TEXT
                "partial_link": By.PARTIAL_LINK_TEXT
                "name": By.NAME
                "tag": By.TAG_NAME
                "class": By.CLASS_NAME
                "css": By.CSS_SELECTOR
                "ios_pre": MobileBy.IOS_PREDICATE
                "ios_ui": MobileBy.IOS_UIAUTOMATION
                "ios_class": MobileBy.IOS_CLASS_CHAIN
                "android_ui": MobileBy.ANDROID_UIAUTOMATOR
                "android_tag": MobileBy.ANDROID_VIEWTAG
                "android_data": MobileBy.ANDROID_DATA_MATCHER
                "acc_id": MobileBy.ACCESSIBILITY_ID
                "custom": MobileBy.CUSTOM
        :param identifier:
            the identifier is a function to generate the locator of the found element, you can get the standard ones in class Identifier.
            Otherwise, you can create one like this::

                context.find_element("class=foo", lambda e: "xpath=.//*[@bar='%s']" % e.get_attribute("bar"))
        :param condition:
            end finding element when the found element match the condition function.
            e.g., end finding element when the found element is not None

                context.find_element("class=foo", condition=lambda element: element)
        :return: the DynamicElement found by locator
        """
        # import the DynamicElement here to avoid cyclic dependency
        from .dynamic_element import DynamicElement

        by, value = locator_to_by_value(locator)
        element = {"inner": None}

        def _find_element():
            try:
                try:
                    element["inner"] = DynamicElement(self, self._selenium_context().find_element(by, value), locator, identifier)
                    return element["inner"]
                except (NoSuchElementException, SeleniumStaleElementReferenceException):
                    # Only Element can reach here
                    self.wait_for().exists()
                    element["inner"] = DynamicElement(self, self._selenium_context().find_element(by, value), locator, identifier)
                    return element["inner"]
            except SeleniumInvalidSelectorException:
                raise InvalidLocatorException("The value <%s> of locator <%s> is not a valid expression." % (value, locator), self)
            except SeleniumNoSuchElementException:
                element["inner"] = None
                return element["inner"]
            except SeleniumWebDriverException as wde:
                raise EasyiumException(wde.msg, self)

        try:
            self.waiter().wait_for(lambda: condition(_find_element()))
        except TimeoutException as e:
            if e.__class__ == ElementTimeoutException:
                # raised by self.wait_for().exists() in _find_element()
                raise
            raise TimeoutException("Timed out waiting for the found element by <%s> under:\n%s\nmatches condition <%s>." % (locator, self, condition.__name__))

        return element["inner"]

    def find_elements(self, locator: str, identifier: Callable[["DynamicElement"], str] = Identifier.id,
                      condition: Callable[[List["DynamicElement"]], bool] = lambda elements: True) \
            -> List["DynamicElement"]:
        """
            Find DynamicElement list under this context.
            Note: if no elements is found, empty list will be returned.

        :param locator:
            the locator (relative to this context) of the elements to be found.
            The format of locator is: "by=value", the possible values of "by" are::

                "id": By.ID
                "xpath": By.XPATH
                "link": By.LINK_TEXT
                "partial_link": By.PARTIAL_LINK_TEXT
                "name": By.NAME
                "tag": By.TAG_NAME
                "class": By.CLASS_NAME
                "css": By.CSS_SELECTOR
                "ios_pre": MobileBy.IOS_PREDICATE
                "ios_ui": MobileBy.IOS_UIAUTOMATION
                "ios_class": MobileBy.IOS_CLASS_CHAIN
                "android_ui": MobileBy.ANDROID_UIAUTOMATOR
                "android_tag": MobileBy.ANDROID_VIEWTAG
                "android_data": MobileBy.ANDROID_DATA_MATCHER
                "acc_id": MobileBy.ACCESSIBILITY_ID
                "custom": MobileBy.CUSTOM
        :param identifier:
            the identifier is a function to generate the locator of the found elements, you can get the standard ones in class Identifier.
            Otherwise, you can create one like this::

                context.find_elements("class=foo", identifier=lambda element: "xpath=.//*[@bar='%s']" % element.get_attribute("bar"))
        :param condition:
            end finding elements when the found element list match the condition function.
            e.g., end finding elements when the found element list is not empty

                context.find_elements("class=foo", condition=lambda elements: elements)
        :return: the DynamicElement list found by locator
        """
        # import the DynamicElement here to avoid cyclic dependency
        from .dynamic_element import DynamicElement

        by, value = locator_to_by_value(locator)
        elements = {"inner": []}

        def _find_elements():
            try:
                try:
                    selenium_elements = self._selenium_context().find_elements(by, value)
                    elements["inner"] = [DynamicElement(self, selenium_element, locator, identifier) for selenium_element in selenium_elements]
                    return elements["inner"]
                except (NoSuchElementException, SeleniumStaleElementReferenceException):
                    # Only Element can reach here
                    self.wait_for().exists()
                    selenium_elements = self._selenium_context().find_elements(by, value)
                    elements["inner"] = [DynamicElement(self, selenium_element, locator, identifier) for selenium_element in selenium_elements]
                    return elements["inner"]
            except SeleniumInvalidSelectorException:
                raise InvalidLocatorException("The value <%s> of locator <%s> is not a valid expression." % (value, locator), self)
            except SeleniumWebDriverException as wde:
                raise EasyiumException(wde.msg, self)

        try:
            self.waiter().wait_for(lambda: condition(_find_elements()))
        except TimeoutException as e:
            if e.__class__ == ElementTimeoutException:
                # raised by self.wait_for().exists() in _find_elements()
                raise
            raise TimeoutException("Timed out waiting for the found element list by <%s> under:\n%s\nmatches condition <%s>." % (locator, self, condition.__name__))

        return elements["inner"]
