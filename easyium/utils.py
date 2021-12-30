import socket
from urllib.parse import urlparse

from .waiter import Waiter


def wait_for_server_started(server_url: str, interval: int = 1000, timeout: int = 30000):
    """
        Wait for the remote server to be started.

    :param server_url: the url of the remote server, e.g.,"http://127.0.0.1:4728/wd/hub"
    :param interval: the wait interval (in milliseconds)
    :param timeout: the wait timeout (in milliseconds)
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

    Waiter(interval, timeout).wait_for(server_started)
