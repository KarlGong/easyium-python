from .exceptions import NotPersistException, LatePersistException
from .element import Element


class DynamicElement(Element):
    def __init__(self, parent, selenium_element, found_by, identifier):
        Element.__init__(self, parent)
        # from element
        self.__inner_selenium_element = selenium_element
        self.__locator = None
        # self
        self.__found_by = found_by
        self.__identifier = identifier

    def _refresh(self):
        if self.__locator is None:
            raise NotPersistException("persist() was not invoked so this Element cannot auto-refresh.", self)
        self.__inner_selenium_element = None
        self.__inner_selenium_element = self.get_parent()._find_selenium_element(self.__locator)

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
                "Trying to persist() a stale element. Try invoking persist() earlier.", self)

    def __str__(self):
        if self.__inner_selenium_element is None:
            return "%s\n|- DynamicElement <SeleniumElement: %s><Locator: %s><FoundBy: %s>" % (
                self.get_parent(), None, self.__locator, self.__found_by)
        else:
            return "%s\n|- DynamicElement <SeleniumElementId: %s><Locator: %s><FoundBy: %s>" % (
                self.get_parent(), self.__inner_selenium_element.id, self.__locator, self.__found_by)
