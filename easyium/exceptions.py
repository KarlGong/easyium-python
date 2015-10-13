__author__ = 'karl.gong'


class EasyiumException(Exception):
    pass


class TimeoutException(EasyiumException):
    pass


class NoSuchElementException(EasyiumException):
    pass


class NotPersistException(EasyiumException):
    pass


class LatePersistException(EasyiumException):
    pass


class UnsupportedWebDriverTypeException(EasyiumException):
    pass


class InvalidByException(EasyiumException):
    pass


class UnsupportedOperationException(EasyiumException):
    pass