__author__ = 'karl.gong'

from .exceptions import UnsupportedOperationForWebDriver


def SupportedBy(*web_driver_types):
    def handle_func(func):
        def handle_args(*args, **kwargs):
            wd_types = []
            for wd_type in web_driver_types:
                wd_types += wd_type

            current_web_driver_type = args[0].get_web_driver().get_web_driver_type()
            if current_web_driver_type not in wd_types:
                raise UnsupportedOperationForWebDriver(
                    "The operation is not supported in web driver [%s]." % current_web_driver_type)

            func(*args, **kwargs)

        return handle_args

    return handle_func
