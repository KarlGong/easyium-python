import re

__author__ = 'karl.gong'

filter_msg_regex = re.compile(r"\n  \(Session info:.*?\)\n  \(Driver info:.*?\(.*?\).*?\)")


class EasyiumException(Exception):
    def __init__(self, msg=None, context=None):
        # Remove Session info and Driver info of the message.
        self.msg = filter_msg_regex.sub("", msg)
        self.message = self.msg
        self.context = context

    def __str__(self):
        exception_msg = ""
        if self.msg is not None:
            exception_msg = self.msg
        if self.context is not None:
            exception_msg += "\n" + str(self.context)
        return exception_msg


class TimeoutException(EasyiumException):
    pass


class ElementTimeoutException(TimeoutException):
    pass


class WebDriverTimeoutException(TimeoutException):
    pass


class NoSuchElementException(EasyiumException):
    pass


class NotPersistException(EasyiumException):
    pass


class LatePersistException(EasyiumException):
    pass


class UnsupportedWebDriverTypeException(EasyiumException):
    pass


class InvalidLocatorException(EasyiumException):
    pass


class UnsupportedOperationException(EasyiumException):
    pass
