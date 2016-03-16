from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, InvalidSelectorException, WebDriverException

from .locator import locator_to_by_value
from .identifier import Identifier
from .waiter import Waiter
from . import exceptions


class Context:
    def __init__(self):
        self.__wait_interval = None
        self.__wait_timeout = None

    def get_web_driver(self):
        pass

    def get_web_driver_type(self):
        pass

    def _selenium_context(self):
        pass

    def _refresh(self):
        pass

    def persist(self):
        pass

    def get_screenshot_as_file(self, filename):
        pass

    def get_screenshot_as_png(self):
        pass

    def get_screenshot_as_base64(self):
        pass

    def get_wait_interval(self):
        """
            Get the wait interval of this context.

        :return: the wait interval
        """
        return self.__wait_interval

    def set_wait_interval(self, interval):
        """
            Set the wait interval of this context.

        :param interval: the new wait interval (in milliseconds)
        """
        self.__wait_interval = interval

    def get_wait_timeout(self):
        """
            Get the wait timeout of this context.

        :return: the wait timeout
        """
        return self.__wait_timeout

    def set_wait_timeout(self, timeout):
        """
            Set the wait timeout of this context.

        :param timeout: the new wait timeout (in milliseconds)
        """
        self.__wait_timeout = timeout

    def wait_for(self, interval=None, timeout=None):
        pass

    def waiter(self, interval=None, timeout=None):
        """
            Get a Waiter instance.

        :param interval: the wait interval (in milliseconds). If None, use context's wait interval.
        :param timeout: the wait timeout (in milliseconds). If None, use context's wait interval.
        """
        _interval = interval if interval else self.get_wait_interval()
        _timeout = timeout if timeout else self.get_wait_timeout()
        return Waiter(_interval, _timeout)

    def _find_selenium_element(self, locator):
        by, value = locator_to_by_value(locator)
        try:
            try:
                return self._selenium_context().find_element(by, value)
            except StaleElementReferenceException:
                self._refresh()
                return self._selenium_context().find_element(by, value)
        except InvalidSelectorException:
            raise exceptions.InvalidLocatorException("The value <%s> of locator <%s> is not a valid expression." % (value, locator), self)
        except NoSuchElementException:
            raise exceptions.NoSuchElementException("Cannot find element by <%s> under:" % locator, self)
        except WebDriverException as wde:
            raise exceptions.EasyiumException(wde.msg, self)

    def has_child(self, locator):
        """
            Return whether this context has a child element.

        :param locator: the locator (relative to this context) of the child element
        :return: whether this context has a child element.
        """
        try:
            self.find_element(locator)
            return True
        except exceptions.NoSuchElementException:
            return False

    def find_element(self, locator, identifier=Identifier.id):
        """
            Find a DynamicElement under this context immediately.

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
                "ios_uiautomation": MobileBy.IOS_UIAUTOMATION
                "android_uiautomation": MobileBy.ANDROID_UIAUTOMATOR
                "accessibility_id": MobileBy.ACCESSIBILITY_ID
        :param identifier:
            the identifier is a function to generate the locator of the found element, you can get the standard ones in class Identifier.
            Otherwise, you can create one like this::

                context.find_element("class=food", lambda e: "xpath=.//*[@attr='%s']" % e.get_attribute("attr"))
        :return: the DynamicElement found by locator
        """
        # import the DynamicElement here to avoid cyclic dependency
        from .dynamicelement import DynamicElement

        by, value = locator_to_by_value(locator)
        try:
            try:
                return DynamicElement(self, self._selenium_context().find_element(by, value), locator, identifier)
            except (exceptions.NoSuchElementException, StaleElementReferenceException):
                # Only Element can reach here
                self.wait_for().exists()
                return DynamicElement(self, self._selenium_context().find_element(by, value), locator, identifier)
        except InvalidSelectorException:
            raise exceptions.InvalidLocatorException("The value <%s> of locator <%s> is not a valid expression." % (value, locator), self)
        except NoSuchElementException:
            raise exceptions.NoSuchElementException("Cannot find element by <%s> under:" % locator, self)
        except WebDriverException as wde:
            raise exceptions.EasyiumException(wde.msg, self)

    def find_elements(self, locator, identifier=Identifier.id, at_least=0):
        """
            Find DynamicElement list under this context immediately.

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
                "ios_uiautomation": MobileBy.IOS_UIAUTOMATION
                "android_uiautomation": MobileBy.ANDROID_UIAUTOMATOR
                "accessibility_id": MobileBy.ACCESSIBILITY_ID
        :param identifier:
            the identifier is a function to generate the locator of the found elements, you can get the standard ones in class Identifier.
            Otherwise, you can create one like this::

                context.find_elements("class=food", lambda e: "xpath=.//*[@attr='%s']" % e.get_attribute("attr"))
        :param at_least: end finding elements when the number of found elements is at least the given number.
        :return: the DynamicElement list found by locator
        """
        # import the DynamicElement here to avoid cyclic dependency
        from .dynamicelement import DynamicElement

        by, value = locator_to_by_value(locator)
        selenium_elements = {"inner": []}

        def find_selenium_elements():
            try:
                try:
                    selenium_elements["inner"] = self._selenium_context().find_elements(by, value)
                    return selenium_elements["inner"]
                except (exceptions.NoSuchElementException, StaleElementReferenceException):
                    # Only Element can reach here
                    self.wait_for().exists()
                    selenium_elements["inner"] = self._selenium_context().find_elements(by, value)
                    return selenium_elements["inner"]
            except InvalidSelectorException:
                raise exceptions.InvalidLocatorException("The value <%s> of locator <%s> is not a valid expression." % (value, locator), self)
            except WebDriverException as wde:
                raise exceptions.EasyiumException(wde.msg, self)

        try:
            self.waiter().wait_for(lambda : len(find_selenium_elements()) >= at_least)
        except exceptions.TimeoutException as e:
            if e.__class__ == exceptions.ElementTimeoutException:
                # raised by self.wait_for().exists() in find_selenium_elements()
                raise
            raise exceptions.TimeoutException("Timed out waiting for the number of found elements by <%s> under:\n%s\nto be at least <%s>." % (locator, self, at_least))

        return [DynamicElement(self, selenium_element, locator, identifier) for selenium_element in selenium_elements["inner"]]
