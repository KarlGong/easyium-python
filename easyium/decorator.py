__author__ = 'karl.gong'

from .exceptions import UnsupportedOperationException


def SupportedBy(*web_driver_types):
    def handle_func(func):
        def handle_args(*args, **kwargs):
            wd_types = []
            for wd_type in web_driver_types:
                if isinstance(wd_type, list):
                    wd_types += wd_type
                else:
                    wd_types += [wd_type]

            current_web_driver_type = args[0].get_web_driver_type()
            if current_web_driver_type not in wd_types:
                raise UnsupportedOperationException(
                    "This operation is not supported by web driver [%s]." % current_web_driver_type)

            return func(*args, **kwargs)

        return handle_args

    return handle_func
