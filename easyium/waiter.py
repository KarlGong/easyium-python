import time

from selenium.common.exceptions import NoAlertPresentException

from .config import DEFAULT, default_config
from .exceptions import TimeoutException, ElementTimeoutException, WebDriverTimeoutException, NoSuchElementException

__author__ = 'karl.gong'


class Waiter:
    def __init__(self, interval=DEFAULT, timeout=DEFAULT, pre_wait_time=DEFAULT, post_wait_time=DEFAULT):
        """
            Create a Waiter instance.

        :param interval: the wait interval (in milliseconds), default value is from default_config.waiter_wait_interval
        :param timeout: the wait timeout (in milliseconds), default value is from default_config.waiter_wait_timeout
        :param pre_wait_time: the pre wait time (in milliseconds), default value is from default_config.waiter_pre_wait_time
        :param post_wait_time: the post wait time (in milliseconds), default value is from default_config.waiter_post_wait_time
        """
        self.__interval = default_config.waiter_wait_interval if interval == DEFAULT else interval
        self.__timeout = default_config.waiter_wait_timeout if timeout == DEFAULT else timeout
        self.__pre_wait_time = default_config.waiter_pre_wait_time if pre_wait_time == DEFAULT else pre_wait_time
        self.__post_wait_time = default_config.waiter_post_wait_time if post_wait_time == DEFAULT else post_wait_time

    def wait_for(self, condition_function, *function_args, **function_kwargs):
        """
            Wait for the condition.

        :param condition_function: the condition function
        :param function_args: the args for condition_function
        :param function_kwargs: the kwargs for condition_function
        """
        time.sleep(self.__pre_wait_time / 1000.0)

        start_time = time.time() * 1000.0

        if condition_function(*function_args, **function_kwargs):
            time.sleep(self.__post_wait_time / 1000.0)
            return

        while (time.time() * 1000.0 - start_time) <= self.__timeout:
            time.sleep(self.__interval / 1000.0)
            if condition_function(*function_args, **function_kwargs):
                time.sleep(self.__post_wait_time / 1000.0)
                return

        raise TimeoutException("Timed out waiting for <%s>." % condition_function.__name__)


class ElementWaitFor:
    def __init__(self, element, interval, timeout, pre_wait_time, post_wait_time):
        self.__element = element
        self.__desired_occurrence = True
        self.__waiter = Waiter(interval, timeout, pre_wait_time, post_wait_time)

    def __wait_for(self, element_condition):
        def is_element_condition_occurred():
            return element_condition.occurred() == self.__desired_occurrence

        try:
            self.__waiter.wait_for(is_element_condition_occurred)
        except TimeoutException:
            raise ElementTimeoutException(
                "Timed out waiting for <%s> to be <%s>." % (element_condition, self.__desired_occurrence))

    def not_(self):
        """
            Wait for not.
        """
        self.__desired_occurrence = not self.__desired_occurrence
        return self

    def exists(self):
        """
            Wait for this element exists.
        """
        self.__wait_for(ElementExistence(self.__element))

    def visible(self):
        """
            Wait for this element visible.
        """
        self.__wait_for(ElementVisible(self.__element))

    def attribute_equals(self, attribute, value):
        """
            Wait for this element's attribute value equals the value.

        :param attribute: the attribute of this element.
        :param value: the expected value.

        :Usage:
            element.wait_for().attribute_equals("class", "foo bar")
        """
        self.__wait_for(ElementAttributeEquals(self.__element, attribute, value))

    def attribute_contains_one(self, attribute, *values):
        """
            Wait for this element's attribute value contains one of the value list.

        :param attribute: the attribute of this element.
        :param values: the expected value list.

        :Usage:
            element.wait_for().attribute_contains_one("class", "foo", "bar")
            element.wait_for().attribute_contains_one("class", ["foo", "bar"])
            element.wait_for().attribute_contains_one("class", ("foo", "bar"))
        """
        self.__wait_for(ElementAttributeContainsOne(self.__element, attribute, *values))

    def attribute_contains_all(self, attribute, *values):
        """
            Wait for this element's attribute value contains all of the value list.

        :param attribute: the attribute of this element.
        :param values: the expected value list.

        :Usage:
            element.wait_for().attribute_contains_all("class", "foo", "bar")
            element.wait_for().attribute_contains_all("class", ["foo", "bar"])
            element.wait_for().attribute_contains_all("class", ("foo", "bar"))
        """
        self.__wait_for(ElementAttributeContainsAll(self.__element, attribute, *values))


class ElementExistence:
    def __init__(self, element):
        self.__element = element

    def occurred(self):
        return self.__element.exists()

    def __str__(self):
        return "ElementExistence [\n%s\n]" % self.__element


class ElementVisible:
    def __init__(self, element):
        self.__element = element

    def occurred(self):
        return self.__element.is_displayed()

    def __str__(self):
        return "ElementVisible [\n%s\n]" % self.__element

class ElementAttributeEquals:
    def __init__(self, element, attribute, value):
        self.__element = element
        self.__attribute = attribute
        self.__value = value

    def occurred(self):
        return self.__element.exists() and self.__element._selenium_element().get_attribute(self.__attribute) == self.__value

    def __str__(self):
        return "ElementAttributeEquals [element: \n%s\n][attribute: %s][value: %s]" % (
            self.__element, self.__attribute, self.__value)

class ElementAttributeContainsOne:
    def __init__(self, element, attribute, *values):
        self.__element = element
        self.__attribute = attribute
        self.__values = []
        for value in values:
            if isinstance(value, (tuple, list)):
                self.__values.extend(value)
            else:
                self.__values.append(value)

    def occurred(self):
        if not self.__element.exists():
            return False
        attribute_value = self.__element._selenium_element().get_attribute(self.__attribute)
        for value in self.__values:
            if value in attribute_value:
                return True
        return False

    def __str__(self):
        return "ElementAttributeContainsOne [element: \n%s\n][attribute: %s][values: %s]" % (
            self.__element, self.__attribute, self.__values)


class ElementAttributeContainsAll:
    def __init__(self, element, attribute, *values):
        self.__element = element
        self.__attribute = attribute
        self.__values = []
        for value in values:
            if isinstance(value, (tuple, list)):
                self.__values.extend(value)
            else:
                self.__values.append(value)

    def occurred(self):
        if not self.__element.exists():
            return False
        attribute_value = self.__element._selenium_element().get_attribute(self.__attribute)
        for value in self.__values:
            if value not in attribute_value:
                return False
        return True

    def __str__(self):
        return "ElementAttributeContainsAll [element: \n%s\n][attribute: %s][values: %s]" % (
            self.__element, self.__attribute, self.__values)


class WebDriverWaitFor:
    def __init__(self, web_driver, interval, timeout, pre_wait_time, post_wait_time):
        self.__web_driver = web_driver
        self.__desired_occurrence = True
        self.__waiter = Waiter(interval, timeout, pre_wait_time, post_wait_time)

    def __wait_for(self, web_driver_condition):
        def is_web_driver_condition_occurred():
            return web_driver_condition.occurred() == self.__desired_occurrence

        try:
            self.__waiter.wait_for(is_web_driver_condition_occurred)
        except TimeoutException:
            raise WebDriverTimeoutException(
                "Timed out waiting for <%s> to be <%s>." % (web_driver_condition, self.__desired_occurrence))

    def not_(self):
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

    def text_present(self, text):
        """
            Wait for the text present.

        :param text: the text to wait
        """
        self.__wait_for(TextPresent(self.__web_driver, text))

    def url_changed(self, previous_url):
        """
            Wait for the url changed.

        :param previous_url: the url before url changed

        :Usage:
            previous_url = driver.get_current_url()
            StaticElement(driver, "id=change_url").click() # url changed
            driver.wait_for().url_changed(previous_url)
        """
        self.__wait_for(URLChanged(self.__web_driver, previous_url))


class AlertPresent:
    def __init__(self, web_driver):
        self.__web_driver = web_driver

    def occurred(self):
        try:
            alert_text = self.__web_driver._selenium_web_driver().switch_to.alert.text
            return True
        except NoAlertPresentException:
            return False

    def __str__(self):
        return "AlertPresent [\n%s\n]" % self.__web_driver


class TextPresent:
    def __init__(self, web_driver, text):
        self.__web_driver = web_driver
        self.__text = text

    def occurred(self):
        try:
            self.__web_driver.find_element("xpath=//*[contains(text(), '%s')]" % self.__text)
            return True
        except NoSuchElementException:
            return False

    def __str__(self):
        return "TextPresent [webdriver: \n%s\n][text: %s]" % (self.__web_driver, self.__text)


class URLChanged:
    def __init__(self, web_driver, previous_url):
        self.__web_driver = web_driver
        self.__previous_url = previous_url

    def occurred(self):
        return self.__web_driver.get_current_url() != self.__previous_url

    def __str__(self):
        return "URLChanged [\n%s\n]" % self.__web_driver
