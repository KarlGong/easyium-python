from .context import Context
from .element import Element


class StaticElement(Element):
    def __init__(self, parent: Context, locator: str):
        """
            Creates a new instance of the StaticElement.

        :param parent: the parent context
        :param locator:
            the locator of this element (relative to parent context).
            The format of locator is: "by=value", the possible values of "by" are::

                "id": By.ID
                "xpath": By.XPATH
                "link": By.LINK_TEXT
                "partial_link": By.PARTIAL_LINK_TEXT
                "name": By.NAME
                "tag": By.TAG_NAME
                "class": By.CLASS_NAME
                "css": By.CSS_SELECTOR
                "ios_pre": MobileBy.IOS_PREDICATE
                "ios_ui": MobileBy.IOS_UIAUTOMATION
                "ios_class": MobileBy.IOS_CLASS_CHAIN
                "android_ui": MobileBy.ANDROID_UIAUTOMATOR
                "android_tag": MobileBy.ANDROID_VIEWTAG
                "android_data": MobileBy.ANDROID_DATA_MATCHER
                "acc_id": MobileBy.ACCESSIBILITY_ID
                "custom": MobileBy.CUSTOM
        """
        Element.__init__(self, parent)
        # from element
        self._inner_selenium_element = None
        self._locator = locator

    def _refresh(self):
        self._inner_selenium_element = None
        self._inner_selenium_element = self.get_parent()._find_selenium_element(self._locator)

    def persist(self):
        self.get_parent().persist()

    def __str__(self):
        if self._inner_selenium_element is None:
            return "%s\n|- StaticElement <SeleniumElement: %s><Locator: %s>" % (
                self.get_parent(), None, self._locator)
        else:
            return "%s\n|- StaticElement <SeleniumElementId: %s><Locator: %s>" % (
                self.get_parent(), self._inner_selenium_element.id, self._locator)
