from selenium.webdriver.common.alert import Alert as SeleniumAlert


class Alert:
    def __init__(self, selenium_alert: SeleniumAlert):
        self.__selenium_alert = selenium_alert

    def get_text(self) -> str:
        """
            Gets the text of the Alert.
        """
        return self.__selenium_alert.text

    def dismiss(self):
        """
            Dismisses the alert available.
        """
        self.__selenium_alert.dismiss()

    def accept(self):
        """
            Accepts the alert available.
        """
        self.__selenium_alert.accept()

    def send_keys(self, keys: str):
        """
            Send Keys to the Alert.

        :param keys: The text to be sent to Alert.
        """
        self.__selenium_alert.send_keys(keys)
