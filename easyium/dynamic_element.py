from typing import Callable

from appium.webdriver.webelement import WebElement as AppiumElement

from .context import Context
from .element import Element
from .exceptions import NotPersistException, LatePersistException


class DynamicElement(Element):
    def __init__(self, parent: Context, selenium_element: AppiumElement, found_by, identifier: Callable[[Element], str]):
        Element.__init__(self, parent)
        # from element
        self._inner_selenium_element = selenium_element
        self._locator = None
        # self
        self.__found_by = found_by
        self.__identifier = identifier

    def _refresh(self):
        if self._locator is None:
            raise NotPersistException("persist() was not invoked so this Element cannot auto-refresh.", self)
        self._inner_selenium_element = None
        self._inner_selenium_element = self.get_parent()._find_selenium_element(self._locator)

    def persist(self):
        """
            Generate the locator of this element by identifier, so this element can auto-refresh.
        """
        self.get_parent().persist()

        try:
            if self._locator is None:
                self._locator = self.__identifier(self)
        except NotPersistException:
            raise LatePersistException(
                "Trying to persist() a stale element. Try invoking persist() earlier.", self)

    def __str__(self):
        if self._inner_selenium_element is None:
            return "%s\n|- DynamicElement <SeleniumElement: %s><Locator: %s><FoundBy: %s>" % (
                self.get_parent(), None, self._locator, self.__found_by)
        else:
            return "%s\n|- DynamicElement <SeleniumElementId: %s><Locator: %s><FoundBy: %s>" % (
                self.get_parent(), self._inner_selenium_element.id, self._locator, self.__found_by)
