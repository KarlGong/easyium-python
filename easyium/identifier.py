class Identifier:
    id = staticmethod(lambda element: "id=" + element.get_attribute("id"))

    class_name = staticmethod(lambda element: "class=" + element.get_attribute("class"))

    name = staticmethod(lambda element: "name=" + element.get_attribute("name"))

    text = staticmethod(lambda element: "xpath=.//*[.='%s')]" % element.get_text())
