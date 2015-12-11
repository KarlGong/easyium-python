from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, WebDriverException

from .locator import locator_to_by_value
from .identifier import Identifier
from .waiter import Waiter
from .config import DEFAULT
from . import exceptions

__author__ = 'karl.gong'


class Context:
    def __init__(self):
        pass

    def get_web_driver(self):
        pass

    def get_web_driver_type(self):
        pass

    def get_wait_interval(self):
        pass

    def get_wait_timeout(self):
        pass

    def get_pre_wait_time(self):
        pass

    def get_post_wait_time(self):
        pass

    def waiter(self, interval=DEFAULT, timeout=DEFAULT, pre_wait_time=DEFAULT, post_wait_time=DEFAULT):
        """
            Get a Waiter instance.

        :param interval: the wait interval (in milliseconds), default value is web driver's wait interval
        :param timeout: the wait timeout (in milliseconds), default value is web driver's wait timeout
        :param pre_wait_time: the pre wait time (in milliseconds), default value is web driver's pre wait time
        :param post_wait_time: the post wait time (in milliseconds), default value is web driver's post wait time
        """
        _interval = self.get_wait_interval() if interval == DEFAULT else interval
        _timeout = self.get_wait_timeout() if timeout == DEFAULT else timeout
        _pre_wait_time = self.get_pre_wait_time() if pre_wait_time == DEFAULT else pre_wait_time
        _post_wait_time = self.get_post_wait_time() if post_wait_time == DEFAULT else post_wait_time
        return Waiter(_interval, _timeout, _pre_wait_time, _post_wait_time)

    def _selenium_context(self):
        pass

    def _refresh(self):
        pass

    def persist(self):
        pass

    def _find_selenium_element(self, locator):
        by, value = locator_to_by_value(locator)
        try:
            try:
                return self._selenium_context().find_element(by, value)
            except StaleElementReferenceException:
                self._refresh()
                return self._selenium_context().find_element(by, value)
        except NoSuchElementException:
            raise exceptions.NoSuchElementException("Cannot find element by [%s] under:\n%s\n" % (locator, self))
        except WebDriverException as wde:
            raise exceptions.EasyiumException("%s\n%s" % (wde.msg, self))

    def find_element(self, locator, identifier=Identifier.id):
        """
            Find a DynamicElement under this context immediately.
            If this context is not existing, it will raise NoSuchElementException.

        :param locator:
            the locator of this element (relative to parent context).
            The format of locator is: "by=value", the possible values of "by" are::

                "id": By.ID
                "xpath": By.XPATH
                "link": By.LINK_TEXT
                "partial_link": By.PARTIAL_LINK_TEXT
                "name": By.NAME
                "tag": By.TAG_NAME
                "class": By.CLASS_NAME
                "css": By.CSS_SELECTOR
                "ios_uiautomation": MobileBy.IOS_UIAUTOMATION
                "android_uiautomation": MobileBy.ANDROID_UIAUTOMATOR
                "accessibility_id": MobileBy.ACCESSIBILITY_ID
        :param identifier:
            the identifier is a function to generate the locator of the found element, you can get the standard ones in class Identifier.
            Otherwise, you can create one like this::

                context.find_element("class=food", lambda e: "xpath=.//div[@attr='%s']" % e.get_attribute("attr"))
        :return: the DynamicElement found by locator
        """
        # import the DynamicElement here to avoid cyclic dependency
        from .dynamicelement import DynamicElement

        by, value = locator_to_by_value(locator)
        try:
            try:
                return DynamicElement(self, self._selenium_context().find_element(by, value), locator, identifier)
            except StaleElementReferenceException:
                self._refresh()
                return DynamicElement(self, self._selenium_context().find_element(by, value), locator, identifier)
        except NoSuchElementException:
            raise exceptions.NoSuchElementException("Cannot find element by [%s] under:\n%s\n" % (locator, self))
        except WebDriverException as wde:
            raise exceptions.EasyiumException("%s\n%s" % (wde.msg, self))

    def find_elements(self, locator, identifier=Identifier.id):
        """
            Find DynamicElement list under this context immediately.
            If this context is not existing, it will raise NoSuchElementException.

        :param locator:
            the locator of this element (relative to parent context).
            The format of locator is: "by=value", the possible values of "by" are::

                "id": By.ID
                "xpath": By.XPATH
                "link": By.LINK_TEXT
                "partial_link": By.PARTIAL_LINK_TEXT
                "name": By.NAME
                "tag": By.TAG_NAME
                "class": By.CLASS_NAME
                "css": By.CSS_SELECTOR
                "ios_uiautomation": MobileBy.IOS_UIAUTOMATION
                "android_uiautomation": MobileBy.ANDROID_UIAUTOMATOR
                "accessibility_id": MobileBy.ACCESSIBILITY_ID
        :param identifier:
            the identifier is a function to generate the locator of the found elements, you can get the standard ones in class Identifier.
            Otherwise, you can create one like this::

                context.find_elements("class=food", lambda e: "xpath=.//div[@attr='%s']" % e.get_attribute("attr"))
        :return: the DynamicElement list found by locator
        """
        # import the DynamicElement here to avoid cyclic dependency
        from .dynamicelement import DynamicElement

        by, value = locator_to_by_value(locator)
        try:
            try:
                selenium_elements = self._selenium_context().find_elements(by, value)
            except StaleElementReferenceException:
                self._refresh()
                selenium_elements = self._selenium_context().find_elements(by, value)
        except WebDriverException as wde:
            raise exceptions.EasyiumException("%s\n%s" % (wde.msg, self))

        elements = []
        for selenium_element in selenium_elements:
            elements.append(DynamicElement(self, selenium_element, locator, identifier))
        return elements

    def get_screenshot_as_file(self, filename):
        pass

    def get_screenshot_as_png(self):
        pass

    def get_screenshot_as_base64(self):
        pass