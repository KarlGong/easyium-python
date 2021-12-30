import time
from typing import Callable

from selenium.common.exceptions import NoSuchElementException as SeleniumNoSuchElementException, StaleElementReferenceException as SeleniumStaleElementReferenceException, \
    WebDriverException as SeleniumWebDriverException
from selenium.webdriver.common.by import By

from .decorator import SupportedBy
from .element import Element
from .enumeration import WebDriverPlatform
from .exceptions import TimeoutException, ElementTimeoutException, WebDriverTimeoutException
from .web_driver import WebDriver


class Waiter:
    def __init__(self, interval: int = 1000, timeout: int = 30000):
        """
            Create a Waiter instance.

        :param interval: the wait interval (in milliseconds)
        :param timeout: the wait timeout (in milliseconds)
        """
        self.__interval = interval
        self.__timeout = timeout

    def wait_for(self, condition_function: Callable[[*any], bool], *function_args, **function_kwargs):
        """
            Wait for the condition.

        :param condition_function: the condition function
        :param function_args: the args for condition_function
        :param function_kwargs: the kwargs for condition_function
        """
        start_time = time.time() * 1000.0

        if condition_function(*function_args, **function_kwargs):
            return

        while (time.time() * 1000.0 - start_time) <= self.__timeout:
            time.sleep(self.__interval / 1000.0)
            if condition_function(*function_args, **function_kwargs):
                return

        raise TimeoutException("Timed out waiting for <%s>." % condition_function.__name__)


class ElementWaitFor:
    def __init__(self, element: Element, interval: int, timeout: int):
        self.__element = element
        self.__desired_occurrence = True
        self.__interval = interval
        self.__timeout = timeout

    def _get_element(self) -> Element:
        return self.__element

    def __wait_for(self, element_condition: "ElementCondition", interval: int, timeout: int) -> Waiter:
        def is_element_condition_occurred():
            return element_condition.occurred() == self.__desired_occurrence

        try:
            Waiter(interval, timeout).wait_for(is_element_condition_occurred)
        except TimeoutException:
            raise ElementTimeoutException(
                "Timed out waiting for <%s> to be <%s>." % (element_condition, self.__desired_occurrence))

    def not_(self) -> "ElementWaitFor":
        """
            Wait for not.
        """
        self.__desired_occurrence = not self.__desired_occurrence
        return self

    def exists(self):
        """
            Wait for this element exists.
        """
        self.__wait_for(ElementExistence(self.__element), self.__interval, self.__timeout)

    def visible(self):
        """
            Wait for this element visible.
        """
        self.__wait_for(ElementVisible(self.__element), self.__interval, self.__timeout)

    def text_equals(self, text: str):
        """
            Wait for this element's text equals the expected text.

        :param text: the expected text

        :Usage:
            # wait for text not empty
            StaticElement(driver, "id=change_text").wait_for().not_().text_equals("")
        """
        start_time = time.time() * 1000.0
        self.__element.wait_for(self.__interval, self.__timeout).exists()
        rest_timeout = start_time + self.__timeout - time.time() * 1000.0
        self.__wait_for(ElementTextEquals(self.__element, text), self.__interval, rest_timeout)

    def attribute_equals(self, attribute: str, value: str):
        """
            Wait for this element's attribute value equals the expected value.

        :param attribute: the attribute of this element.
        :param value: the expected value.

        :Usage:
            element.wait_for().attribute_equals("class", "foo bar")
        """
        start_time = time.time() * 1000.0
        self.__element.wait_for(self.__interval, self.__timeout).exists()
        rest_timeout = start_time + self.__timeout - time.time() * 1000.0
        self.__wait_for(ElementAttributeEquals(self.__element, attribute, value), self.__interval, rest_timeout)

    def attribute_contains_one(self, attribute: str, *values: str):
        """
            Wait for this element's attribute value contains one of the value list.

        :param attribute: the attribute of this element.
        :param values: the expected value list.

        :Usage:
            element.wait_for().attribute_contains_one("class", "foo", "bar")
            element.wait_for().attribute_contains_one("class", ["foo", "bar"])
            element.wait_for().attribute_contains_one("class", ("foo", "bar"))
        """
        start_time = time.time() * 1000.0
        self.__element.wait_for(self.__interval, self.__timeout).exists()
        rest_timeout = start_time + self.__timeout - time.time() * 1000.0
        self.__wait_for(ElementAttributeContainsOne(self.__element, attribute, *values), self.__interval, rest_timeout)

    def attribute_contains_all(self, attribute: str, *values: str):
        """
            Wait for this element's attribute value contains all of the value list.

        :param attribute: the attribute of this element.
        :param values: the expected value list.

        :Usage:
            element.wait_for().attribute_contains_all("class", "foo", "bar")
            element.wait_for().attribute_contains_all("class", ["foo", "bar"])
            element.wait_for().attribute_contains_all("class", ("foo", "bar"))
        """
        start_time = time.time() * 1000.0
        self.__element.wait_for(self.__interval, self.__timeout).exists()
        rest_timeout = start_time + self.__timeout - time.time() * 1000.0
        self.__wait_for(ElementAttributeContainsAll(self.__element, attribute, *values), self.__interval, rest_timeout)


class ElementCondition:
    def occurred(self):
        pass


class ElementExistence(ElementCondition):
    def __init__(self, element: Element):
        self.__element = element

    def occurred(self) -> bool:
        return self.__element.exists()

    def __str__(self):
        return "ElementExistence [\n%s\n]" % self.__element


class ElementVisible(ElementCondition):
    def __init__(self, element: Element):
        self.__element = element

    def occurred(self) -> bool:
        return self.__element.is_displayed()

    def __str__(self):
        return "ElementVisible [\n%s\n]" % self.__element


class ElementTextEquals(ElementCondition):
    def __init__(self, element: Element, text: str):
        self.__element = element
        self.__text = text

    def occurred(self) -> bool:
        return self.__element._selenium_element().text == self.__text

    def __str__(self):
        return "ElementTextEquals [element: \n%s\n][text: %s]" % (self.__element, self.__text)


class ElementAttributeEquals(ElementCondition):
    def __init__(self, element: Element, attribute: str, value: str):
        self.__element = element
        self.__attribute = attribute
        self.__value = value

    def occurred(self) -> bool:
        return self.__element._selenium_element().get_attribute(self.__attribute) == self.__value

    def __str__(self):
        return "ElementAttributeEquals [element: \n%s\n][attribute: %s][value: %s]" % (
            self.__element, self.__attribute, self.__value)


class ElementAttributeContainsOne(ElementCondition):
    def __init__(self, element: Element, attribute: str, *values: str):
        self.__element = element
        self.__attribute = attribute
        self.__values = []
        for value in values:
            if isinstance(value, (tuple, list)):
                self.__values.extend(value)
            else:
                self.__values.append(value)

    def occurred(self) -> bool:
        attribute_value = self.__element._selenium_element().get_attribute(self.__attribute)
        for value in self.__values:
            if value in attribute_value:
                return True
        return False

    def __str__(self):
        return "ElementAttributeContainsOne [element: \n%s\n][attribute: %s][values: %s]" % (
            self.__element, self.__attribute, self.__values)


class ElementAttributeContainsAll(ElementCondition):
    def __init__(self, element: Element, attribute: str, *values: str):
        self.__element = element
        self.__attribute = attribute
        self.__values = []
        for value in values:
            if isinstance(value, (tuple, list)):
                self.__values.extend(value)
            else:
                self.__values.append(value)

    def occurred(self) -> bool:
        attribute_value = self.__element._selenium_element().get_attribute(self.__attribute)
        for value in self.__values:
            if value not in attribute_value:
                return False
        return True

    def __str__(self):
        return "ElementAttributeContainsAll [element: \n%s\n][attribute: %s][values: %s]" % (
            self.__element, self.__attribute, self.__values)


class WebDriverWaitFor:
    def __init__(self, web_driver: WebDriver, interval: int, timeout: int):
        self.__web_driver = web_driver
        self.__desired_occurrence = True
        self.__waiter = Waiter(interval, timeout)

    def _get_web_driver(self) -> WebDriver:
        return self.__web_driver

    def __wait_for(self, web_driver_condition: "WebDriverCondition"):
        def is_web_driver_condition_occurred():
            return web_driver_condition.occurred() == self.__desired_occurrence

        try:
            self.__waiter.wait_for(is_web_driver_condition_occurred)
        except TimeoutException:
            raise WebDriverTimeoutException(
                "Timed out waiting for <%s> to be <%s>." % (web_driver_condition, self.__desired_occurrence))

    def not_(self) -> "WebDriverWaitFor":
        """
            Wait for not.
        """
        self.__desired_occurrence = not self.__desired_occurrence
        return self

    def alert_present(self):
        """
            Wait for the alert present.
        """
        self.__wait_for(AlertPresent(self.__web_driver))

    def text_present(self, text: str):
        """
            Wait for the text present.

        :param text: the text to wait
        """
        self.__wait_for(TextPresent(self.__web_driver, text))

    def url_equals(self, url: str):
        """
            Wait for the url equals expected url.

        :param url: the expected url

        :Usage:
            # wait for url changed
            previous_url = driver.get_current_url()
            StaticElement(driver, "id=change_url").click() # url changed
            driver.wait_for().not_().url_equals(previous_url)
        """
        self.__wait_for(URLEquals(self.__web_driver, url))

    def reloaded(self, indicator: Element):
        """
            Wait for the page to be refreshed / redirected.

        :param indicator: the indicator element, it should be a DynamicElement

        :Usage:
            # usually we use body as indicator, the indicator should be DynamicElement
            indicator = driver.find_element("tag=body")
            StaticElement(driver, "id=reload_after_2_seconds").click() # reload after 2 seconds
            driver.wait_for().reloaded(indicator)
        """
        self.__wait_for(Reloaded(self.__web_driver, indicator))

    @SupportedBy(WebDriverPlatform.ANDROID)
    def activity_present(self, activity: str):
        """
            Wait for the activity present.

        :param activity: the activity to wait
        """
        self.__wait_for(ActivityPresent(self.__web_driver, activity))

    @SupportedBy(WebDriverPlatform._MOBILE)
    def context_available(self, context_partial_name: str):
        """
            Wait for the context available.

        :param context_partial_name: the partial name of the context
        """
        self.__wait_for(ContextAvailable(self.__web_driver, context_partial_name))


class WebDriverCondition:
    def occurred(self):
        pass


class AlertPresent(WebDriverCondition):
    def __init__(self, web_driver: WebDriver):
        self.__web_driver = web_driver

    def occurred(self) -> bool:
        try:
            alert_text = self.__web_driver._selenium_web_driver().switch_to.alert.text
            return True
        except SeleniumWebDriverException as e:
            return False

    def __str__(self):
        return "AlertPresent [\n%s\n]" % self.__web_driver


class TextPresent(WebDriverCondition):
    def __init__(self, web_driver: WebDriver, text: str):
        self.__web_driver = web_driver
        self.__text = text

    def occurred(self) -> bool:
        try:
            self.__web_driver._selenium_web_driver().find_element(By.XPATH, "//*[contains(., '%s')]" % self.__text)
            return True
        except SeleniumNoSuchElementException:
            return False

    def __str__(self):
        return "TextPresent [webdriver: \n%s\n][text: %s]" % (self.__web_driver, self.__text)


class URLEquals(WebDriverCondition):
    def __init__(self, web_driver: WebDriver, url: str):
        self.__web_driver = web_driver
        self.__url = url

    def occurred(self) -> bool:
        return self.__web_driver._selenium_web_driver().current_url == self.__url

    def __str__(self):
        return "URLEquals [webdriver: \n%s\n][url: %s]" % (self.__web_driver, self.__url)


class Reloaded(WebDriverCondition):
    def __init__(self, web_driver: WebDriver, indicator: Element):
        self.__web_driver = web_driver
        self.__indicator = indicator

    def occurred(self) -> bool:
        try:
            self.__indicator._selenium_element().is_displayed()
            return False
        except SeleniumStaleElementReferenceException:
            return True

    def __str__(self):
        return "Reloaded [\n%s\n]" % self.__web_driver


class ActivityPresent(WebDriverCondition):
    def __init__(self, web_driver: WebDriver, activity: str):
        self.__web_driver = web_driver
        self.__activity = activity

    def occurred(self) -> bool:
        return self.__web_driver._selenium_web_driver().current_activity == self.__activity

    def __str__(self):
        return "ActivityPresent [webdriver: \n%s\n][activity: %s]" % (self.__web_driver, self.__activity)


class ContextAvailable(WebDriverCondition):
    def __init__(self, web_driver: WebDriver, context_partial_name: str):
        self.__web_driver = web_driver
        self.__context_partial_name = context_partial_name

    def occurred(self) -> bool:
        try:
            contexts = self.__web_driver._selenium_web_driver().contexts
            return len([context for context in contexts if self.__context_partial_name in context]) > 0
        except SeleniumWebDriverException as e:
            return False

    def __str__(self):
        return "ContextAvailable [webdriver: \n%s\n][context partial name: %s]" % (
            self.__web_driver, self.__context_partial_name)
