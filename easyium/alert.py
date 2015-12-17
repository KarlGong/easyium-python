class Alert:
    def __init__(self, selenium_alert):
        self.__selenium_alert = selenium_alert

    def get_text(self):
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

    def send_keys(self, keys):
        """
            Send Keys to the Alert.

        :param keys: The text to be sent to Alert.
        """
        self.__selenium_alert.send_keys(keys)

    def authenticate(self, username, password):
        """
            Send the username / password to an Authenticated dialog (like with Basic HTTP Auth) and click 'OK'.

        :param username: string to be set in the username section of the dialog
        :param password: string to be set in the password section of the dialog
        """
        self.__selenium_alert.authenticate(username, password)
