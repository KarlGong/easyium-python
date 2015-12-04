__author__ = 'karl.gong'

# place holder for using default value
DEFAULT = "DEFAULT"


class Config:
    def __init__(self):
        # default configuration for web driver
        self.web_driver_page_load_timeout = 30000
        self.web_driver_script_timeout = 30000
        self.web_driver_pre_wait_time = 0
        self.web_driver_post_wait_time = 0
        self.web_driver_wait_interval = 1000
        self.web_driver_wait_timeout = 30000

        # default configuration for waiter
        self.waiter_pre_wait_time = 0
        self.waiter_post_wait_time = 0
        self.waiter_wait_interval = 1000
        self.waiter_wait_timeout = 30000


default_config = Config()
