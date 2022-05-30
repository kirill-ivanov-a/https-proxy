import socket

from http_parser.pyparser import HttpParser

import proxy.config as config
from proxy.http_socket_reader import HttpSocketReader


class HttpRequest:
    def __init__(
            self,
            sock: socket.socket,
            https_port: int = config.DEFAULT_HTTPS_PORT,
            http_port: int = config.DEFAULT_HTTP_PORT,
            buffer_size: int = config.BUFFER_SIZE,
    ):
        self.https_port = https_port
        self.http_port = http_port
        self.buffer_size = buffer_size
        self.raw_data = HttpSocketReader(sock).recv_data()

        parser = HttpParser()
        parser.execute(self.raw_data, len(self.raw_data))

        self.method = parser.get_method()
        self.headers = parser.get_headers()
        self.secure_connection_required = self.method == "CONNECT"

        if ":" in self.headers["Host"]:
            self.host, port_str = self.headers["Host"].split(":")
            self.port = int(port_str)
        else:
            self.host = self.headers["Host"]
            self.port = https_port if self.secure_connection_required else http_port
