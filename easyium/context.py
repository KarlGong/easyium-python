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

    def get_pre_wait_time(self):
        pass

    def get_wait_interval(self):
        pass

    def get_wait_timeout(self):
        pass

    def waiter(self, pre_wait_time=DEFAULT, interval=DEFAULT, timeout=DEFAULT):
        """"
            Get a Waiter instance.

        :param pre_wait_time: the pre wait time (in milliseconds), default value is web driver's pre wait time
        :param interval: the wait interval (in milliseconds), default value is web driver's wait interval
        :param timeout: the wait timeout (in milliseconds), default value is web driver's wait timeout
        """
        pre_wait_time = self.get_pre_wait_time() if pre_wait_time == DEFAULT else pre_wait_time
        interval = self.get_wait_interval() if interval == DEFAULT else interval
        timeout = self.get_wait_timeout() if timeout == DEFAULT else timeout
        return Waiter(pre_wait_time, interval, timeout)

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

        :param locator: the locator to find the DynamicElement (relative to parent context)
        :param identifier: the identifier to refresh the DynamicElement
        :return the DynamicElement found by locator
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

        :param locator: the locator to find the DynamicElement list (relative to parent context)
        :param identifier: the identifier to refresh the DynamicElement
        :return the DynamicElement list found by locator
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
