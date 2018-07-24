import functools

from .exceptions import UnsupportedOperationException


def SupportedBy(*_platforms):
    def handle_func(func):
        @functools.wraps(func)
        def handle_args(*args, **kwargs):
            platforms = []
            for platform in _platforms:
                if isinstance(platform, list):
                    platforms += platform
                else:
                    platforms += [platform]

            from .element import Element
            from .web_driver import WebDriver
            from .waiter import ElementWaitFor, WebDriverWaitFor

            if isinstance(args[0], Element):
                platform = args[0].get_web_driver_info().platform
                if platform not in platforms:
                    raise UnsupportedOperationException(
                        "Operation [element.%s()] is not supported by platform [%s]." % (func.__name__, platform))
            elif isinstance(args[0], WebDriver):
                platform = args[0].get_web_driver_info().platform
                if platform not in platforms:
                    raise UnsupportedOperationException(
                        "Operation [webdriver.%s()] is not supported by platform [%s]." % (func.__name__, platform))
            elif isinstance(args[0], ElementWaitFor):
                platform = args[0]._get_element().get_web_driver_info().platform
                if platform not in platforms:
                    raise UnsupportedOperationException(
                        "Operation [element.wait_for().%s()] is not supported by platform [%s]." % (
                        func.__name__, platform))
            elif isinstance(args[0], WebDriverWaitFor):
                platform = args[0]._get_web_driver().get_web_driver_info().platform
                if platform not in platforms:
                    raise UnsupportedOperationException(
                        "Operation [webdriver.wait_for().%s()] is not supported by platform [%s]." % (
                        func.__name__, platform))

            return func(*args, **kwargs)

        return handle_args

    return handle_func
