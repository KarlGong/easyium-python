from element import Element

__author__ = 'karl.gong'


class StaticElement(Element):
    def __init__(self, parent, locator):
        Element.__init__(self, parent)
        self.__element = None
        self.__locator = locator

    def _selenium_context(self):
        if self.__element is None:
            self._refresh()
        return self.__element

    def _web_element(self):
        if self.__element is None:
            self._refresh()
        return self.__element

    def _refresh(self):
        self.__element = self.get_parent()._find_web_element(self.__locator)

    def persist(self):
        self.get_parent().persist()

    def __str__(self):
        if self.__element is None:
            element_id = None
        else:
            element_id = self.__element.id
        return "%s\n|- StaticElement [WebElement: %s][Locator: %s]" % (self.get_parent(), element_id, self.__locator)
