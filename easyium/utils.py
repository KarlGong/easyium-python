import socket
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from .config import DEFAULT
from .waiter import Waiter


def wait_for_server_started(server_url, interval=DEFAULT, timeout=DEFAULT, pre_wait_time=DEFAULT, post_wait_time=DEFAULT):
    """
        Wait for the appium server to be started.

    :param server_url: the url of the appium server, e.g.,"http://127.0.0.1:4728/wd/hub"
    :param interval: the wait interval (in milliseconds), default value is from default_config.waiter_wait_interval
    :param timeout: the wait timeout (in milliseconds), default value is from default_config.waiter_wait_timeout
    :param pre_wait_time: the pre wait time (in milliseconds), default value is from default_config.waiter_pre_wait_time
    :param post_wait_time: the post wait time (in milliseconds), default value is from default_config.waiter_post_wait_time
    """
    url_components = urlparse(server_url)
    server_host = url_components.hostname
    server_port = url_components.port

    def server_started():
        socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            socket_.settimeout(1)
            socket_.connect((server_host, server_port))
            return True
        except socket.error:
            return False
        finally:
            socket_.close()

    Waiter(interval, timeout, pre_wait_time, post_wait_time).wait_for(server_started)
