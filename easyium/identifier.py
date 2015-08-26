__author__ = 'karl.gong'


class Identifier:
    @staticmethod
    def id(element):
        return "id=" + element.get_attribute("id")

    @staticmethod
    def class_name(element):
        return "class=" + element.get_attribute("class")

    @staticmethod
    def name(element):
        return "name=" + element.get_attribute("name")

    @staticmethod
    def link_text(element):
        return "link=" + element.get_text()