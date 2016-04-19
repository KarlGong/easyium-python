from easyium import WebDriver, WebDriverType, StaticElement


# This class maps the google page in the browser.
class Google:
    def __init__(self):
        # Create a WebDriver instance for chrome.
        self.__web_driver = WebDriver(WebDriverType.CHROME)

        # The google apps grid button is in the top-right.
        # This button is always in the page, so it is StaticElement.
        self.__google_apps_grid_button = StaticElement(self.__web_driver, "class=gb_b")

        # After clicked the google apps grid button, the google apps list will be shown.
        # This list is always in the page, although it is invisible, it is StaticElement.
        self.__google_apps_list = StaticElement(self.__web_driver, "class=gb_ha")

        # Currently the StaticElement does not refer to WebElement in Browser,
        # so open url here is fine.
        self.__web_driver.open("https://www.google.com")

    def click_google_apps_grid_button(self):
        # It is StaticElement, easyium will wait it to be visible automatically.
        self.__google_apps_grid_button.click()

        # Let's return the GoogleAppsList object.
        return GoogleAppsList(self.__google_apps_list)

    def quit(self):
        self.__web_driver.quit()


# This class maps google apps list in the browser.
class GoogleAppsList:
    def __init__(self, element):
        self.__element = element

    def wait_until_ready(self):
        # Wait for the google apps list visible.
        self.__element.wait_for().visible()

        # In most cases we should wait for the mask not existing here .
        # But in this case, no mask here.
        # self.__loading_mask.wait_for().not_().exists()

    def get_all_apps(self):
        # We should wait this control until ready.
        self.wait_until_ready()

        # Find the elements under google apps list.
        # We do not know how many apps in the list, so use find_elements(locator).
        # The found elements are DynamicElements.
        return [GoogleApp(e) for e in self.__element.find_elements("class=gb_Z")]


# This class maps google app in the browser.
class GoogleApp:
    def __init__(self, element):
        self.__element = element

        # This locator is relative to parent.
        self.__name = StaticElement(self.__element, "class=gb_4")

    def get_name(self):
        # get_text() doesn't work here, so use javascript
        # return self.name.get_text()
        return self.__name.get_web_driver().execute_script('return arguments[0].innerText', self.__name)

if __name__ == '__main__':
    google = Google()
    google_apps_list = google.click_google_apps_grid_button()
    for app in google_apps_list.get_all_apps():
        print(app.get_name())
    google.quit()
