from .element import Element

__author__ = 'karl.gong'


class StaticElement(Element):
    def __init__(self, parent, locator):
        Element.__init__(self, parent)
        self.__selenium_element = None
        self.__locator = locator

    def _selenium_context(self):
        if self.__selenium_element is None:
            self._refresh()
        return self.__selenium_element

    def _selenium_element(self):
        if self.__selenium_element is None:
            self._refresh()
        return self.__selenium_element

    def _refresh(self):
        self.__selenium_element = self.get_parent()._find_selenium_element(self.__locator)

    def persist(self):
        self.get_parent().persist()

    def __str__(self):
        if self.__selenium_element is None:
            element_id = None
        else:
            element_id = self.__selenium_element.id
        return "%s\n|- StaticElement [WebElement: %s][Locator: %s]" % (self.get_parent(), element_id, self.__locator)
