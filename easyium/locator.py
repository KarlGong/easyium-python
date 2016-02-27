from selenium.webdriver.common.by import By

from .exceptions import InvalidLocatorException
from . import appium_installed

locator_to_by_map = {
    "id": By.ID,
    "xpath": By.XPATH,
    "link": By.LINK_TEXT,
    "partial_link": By.PARTIAL_LINK_TEXT,
    "name": By.NAME,
    "tag": By.TAG_NAME,
    "class": By.CLASS_NAME,
    "css": By.CSS_SELECTOR
}

if appium_installed:
    from appium.webdriver.common.mobileby import MobileBy

    mobile_locator_to_by_map = {
        "ios_uiautomation": MobileBy.IOS_UIAUTOMATION,
        "android_uiautomation": MobileBy.ANDROID_UIAUTOMATOR,
        "accessibility_id": MobileBy.ACCESSIBILITY_ID
    }

    locator_to_by_map.update(mobile_locator_to_by_map)


def locator_to_by_value(locator):
    separator_index = locator.find("=")
    by = locator[:separator_index]
    value = locator[separator_index + 1:]
    try:
        by = locator_to_by_map[by]
    except KeyError:
        raise InvalidLocatorException("The by <%s> of locator <%s> is not a valid By." % (by, locator))
    return by, value