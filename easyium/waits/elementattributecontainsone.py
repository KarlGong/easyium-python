__author__ = 'karl.gong'


class ElementAttributeContainsOne:
    def __init__(self, element, attribute, *values):
        self.__element = element
        self.__attribute = attribute
        self.__values = values

    def occurred(self):
        attribute_value = self.__element.get_attribute(self.__attribute)
        for value in self.__values:
            if attribute_value.find(value) != -1:
                return True
        return False

    def __str__(self):
        return "ElementAttributeContainsOne [element: \n%s\n][attribute: %s][values: %s]" % (
            self.__element, self.__attribute, self.__values)
