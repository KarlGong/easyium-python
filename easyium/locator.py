from selenium.webdriver.common.by import By

from exceptions import InvalidByException

__author__ = 'karl.gong'

locator_to_by_map = {
    "id": By.ID,
    "xpath": By.XPATH,
    "link": By.LINK_TEXT,
    "name": By.NAME,
    "tag": By.TAG_NAME,
    "class": By.CLASS_NAME,
    "css": By.CSS_SELECTOR
}


def locator_to_by_value(locator):
    separator_index = locator.find("=")
    by = locator[:separator_index]
    value = locator[separator_index + 1:]
    try:
        by = locator_to_by_map[by]
    except KeyError:
        raise InvalidByException("Invalid By: [%s] for locator: [%s]." % (by, locator))
    return by, value