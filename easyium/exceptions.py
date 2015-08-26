__author__ = 'karl.gong'


class ESelException(Exception):
    pass


class TimeoutException(ESelException):
    pass


class NoSuchElementException(ESelException):
    pass


class NotPersistException(ESelException):
    pass


class LatePersistException(ESelException):
    pass


class UnsupportedWebDriverTypeException(ESelException):
    pass


class InvalidByException(ESelException):
    pass
