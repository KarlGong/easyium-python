from .exceptions import NotPersistException, LatePersistException
from .element import Element

__author__ = 'karl.gong'


class DynamicElement(Element):
    def __init__(self, parent, selenium_element, found_by, identifier):
        Element.__init__(self, parent)
        self.__selenium_element = selenium_element
        self.__locator = None
        self.__found_by = found_by
        self.__identifier = identifier

    def _selenium_context(self):
        return self.__selenium_element

    def _selenium_element(self):
        return self.__selenium_element

    def _refresh(self):
        if self.__locator is None:
            raise NotPersistException("persist() was not invoked so this Element cannot auto-refresh.\n%s" % self)
        self.__selenium_element = self.get_parent()._find_selenium_element(self.__locator)

    def persist(self):
        """
            Generate the locator of this element by identifier, so this element can auto-refresh.
        """
        self.get_parent().persist()

        try:
            if self.__locator is None:
                self.__locator = self.__identifier(self)
        except NotPersistException:
            raise LatePersistException(
                "Trying to persist() a stale element. Try invoking persist() earlier.\n%s" % self)

    def __str__(self):
        return "%s\n|- DynamicElement [SeleniumElement: %s][Locator: %s][FoundBy: %s]" % (
            self.get_parent(), self.__selenium_element.id, self.__locator, self.__found_by)
