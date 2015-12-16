__author__ = 'karl.gong'


class EasyiumException(Exception):
    pass


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
