from typing import Tuple

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By

from .exceptions import InvalidLocatorException

locator_to_by_map = {
    "id": By.ID,
    "xpath": By.XPATH,
    "link": By.LINK_TEXT,
    "partial_link": By.PARTIAL_LINK_TEXT,
    "name": By.NAME,
    "tag": By.TAG_NAME,
    "class": By.CLASS_NAME,
    "css": By.CSS_SELECTOR,
    "ios_pre": MobileBy.IOS_PREDICATE,
    "ios_ui": MobileBy.IOS_UIAUTOMATION,
    "ios_class": MobileBy.IOS_CLASS_CHAIN,
    "android_ui": MobileBy.ANDROID_UIAUTOMATOR,
    "android_tag": MobileBy.ANDROID_VIEWTAG,
    "android_data": MobileBy.ANDROID_DATA_MATCHER,
    "acc_id": MobileBy.ACCESSIBILITY_ID,
    "custom": MobileBy.CUSTOM
}


def locator_to_by_value(locator: str) -> Tuple[By, str]:
    separator_index = locator.find("=")
    if separator_index == -1:
        raise InvalidLocatorException("Separator '=' is not found.")
    by = locator[:separator_index]
    value = locator[separator_index + 1:]
    try:
        by = locator_to_by_map[by]
    except KeyError:
        raise InvalidLocatorException("The by <%s> of locator <%s> is not a valid By." % (by, locator))
    return by, value
