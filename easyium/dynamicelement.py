from exceptions import NotPersistException, LatePersistException
from element import Element


__author__ = 'karl.gong'


class DynamicElement(Element):
    def __init__(self, parent, web_element, identifier):
        Element.__init__(self, parent)
        self.__element = web_element
        self.__locator = None
        self.__identifier = identifier

    def _selenium_context(self):
        return self.__element

    def _web_element(self):
        return self.__element

    def _refresh(self):
        if self.__locator is None:
            raise NotPersistException("persist() was not invoked so this Element cannot auto-refresh.\n%s" % self)
        self.__element = self.get_parent()._find_web_element(self.__locator)

    def persist(self):
        self.get_parent().persist()

        try:
            if self.__locator is None:
                self.__locator = self.__identifier(self)
        except NotPersistException:
            raise LatePersistException(
                "Trying to persist() a stale element. Try invoking persist() earlier.\n%s" % self)

    def __str__(self):
        return "%s\n|- DynamicElement [WebElement: %s][Locator: %s][Identifier: %s]" % (
            self.get_parent(), self.__element.id, self.__locator, self.__identifier.__name__)
