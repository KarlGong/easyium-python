from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

from .locator import locator_to_by_value
from .identifier import Identifier
from . import exceptions


__author__ = 'karl.gong'


class Context:
    def __init__(self):
        pass

    def get_web_driver(self):
        pass

    def _selenium_context(self):
        pass

    def persist(self):
        pass

    def _refresh(self):
        pass

    def _find_web_element(self, locator):
        by, value = locator_to_by_value(locator)
        try:
            try:
                return self._selenium_context().find_element(by, value)
            except StaleElementReferenceException:
                self._refresh()
                return self._selenium_context().find_element(by, value)
        except NoSuchElementException:
            raise exceptions.NoSuchElementException("Cannot find element by [%s] under:\n%s\n" % (locator, self))

    def find_element(self, locator, identifier=Identifier.id):
        # import the DynamicElement here to avoid cyclic dependency
        from .dynamicelement import DynamicElement

        by, value = locator_to_by_value(locator)
        try:
            try:
                return DynamicElement(self, self._selenium_context().find_element(by, value), identifier)
            except StaleElementReferenceException:
                self._refresh()
                return DynamicElement(self, self._selenium_context().find_element(by, value), identifier)
        except NoSuchElementException:
            raise exceptions.NoSuchElementException("Cannot find element by [%s] under:\n%s\n" % (locator, self))

    def find_elements(self, locator, identifier=Identifier.id):
        # import the DynamicElement here to avoid cyclic dependency
        from .dynamicelement import DynamicElement

        by, value = locator_to_by_value(locator)
        try:
            web_elements = self._selenium_context().find_elements(by, value)
        except StaleElementReferenceException:
            self._refresh()
            web_elements = self._selenium_context().find_elements(by, value)

        elements = []
        for web_element in web_elements:
            elements.append(DynamicElement(self, web_element, identifier))
        return elements

