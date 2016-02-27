import functools

from .exceptions import UnsupportedOperationException


def SupportedBy(*web_driver_types):
    def handle_func(func):
        @functools.wraps(func)
        def handle_args(*args, **kwargs):
            wd_types = []
            for wd_type in web_driver_types:
                if isinstance(wd_type, list):
                    wd_types += wd_type
                else:
                    wd_types += [wd_type]

            from .element import Element
            from .webdriver import WebDriver
            from .waiter import ElementWaitFor, WebDriverWaitFor

            if isinstance(args[0], Element):
                current_web_driver_type = args[0].get_web_driver_type()
                if current_web_driver_type not in wd_types:
                    raise UnsupportedOperationException(
                        "Operation [element.%s()] is not supported by web driver [%s]." % (func.__name__, current_web_driver_type))
            elif isinstance(args[0], WebDriver):
                current_web_driver_type = args[0].get_web_driver_type()
                if current_web_driver_type not in wd_types:
                    raise UnsupportedOperationException(
                        "Operation [webdriver.%s()] is not supported by web driver [%s]." % (func.__name__, current_web_driver_type))
            elif isinstance(args[0], ElementWaitFor):
                current_web_driver_type = args[0].__element__.get_web_driver_type()
                if current_web_driver_type not in wd_types:
                    raise UnsupportedOperationException(
                        "Operation [element.wait_for().%s()] is not supported by web driver [%s]." % (func.__name__, current_web_driver_type))
            elif isinstance(args[0], WebDriverWaitFor):
                current_web_driver_type = args[0].__web_driver__.get_web_driver_type()
                if current_web_driver_type not in wd_types:
                    raise UnsupportedOperationException(
                        "Operation [webdriver.wait_for().%s()] is not supported by web driver [%s]." % (func.__name__, current_web_driver_type))

            return func(*args, **kwargs)

        return handle_args

    return handle_func
