import time

from elementattributecontainsall import ElementAttributeContainsAll
from elementattributecontainsone import ElementAttributeContainsOne
from elementexistence import ElementExistence
from elementvisible import ElementVisible
from ..exceptions import TimeoutException
from ..config import DEFAULT, default_wait_interval, default_wait_timeout

__author__ = 'karl.gong'


def wait_for(condition_function, interval=DEFAULT, timeout=DEFAULT, **function_args):
    """
        Wait for the condition to be true.
    :param condition_function: a function which returns bool
    """
    interval = default_wait_interval if interval == DEFAULT else interval
    timeout = default_wait_timeout if timeout == DEFAULT else timeout
    start_time = time.time() * 1000.0

    if condition_function(**function_args):
        return

    while (time.time() * 1000.0 - start_time) <= timeout:
        if condition_function(**function_args):
            return
        else:
            time.sleep(interval / 1000.0)

    raise TimeoutException("Timed out waiting for [%s]." % condition_function.__name__)


class ElementWaiter:
    def __init__(self, element, interval, timeout):
        self.__element = element
        self.__interval = interval
        self.__timeout = timeout
        self.__desired_occurrence = True

    def __wait_for(self, element_condition):
        start_time = time.time() * 1000.0

        if element_condition.occurred() == self.__desired_occurrence:
            return

        while (time.time() * 1000.0 - start_time) <= self.__timeout:
            if element_condition.occurred() == self.__desired_occurrence:
                return
            else:
                time.sleep(self.__interval / 1000.0)

        raise TimeoutException(
            "Timed out waiting for [%s] to be [%s]." % (element_condition, self.__desired_occurrence))

    def not_(self):
        self.__desired_occurrence = not self.__desired_occurrence
        return self

    def exists(self):
        self.__wait_for(ElementExistence(self.__element))

    def visible(self):
        self.__wait_for(ElementVisible(self.__element))

    def attribute_contains_all(self, attribute, *values):
        self.__wait_for(ElementAttributeContainsAll(self.__element, attribute, *values))

    def attribute_contains_one(self, attribute, *values):
        self.__wait_for(ElementAttributeContainsOne(self.__element, attribute, *values))
