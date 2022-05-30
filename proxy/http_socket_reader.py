import socket

from http_parser.pyparser import HttpParser

import proxy.config as config

__all__ = ["HttpSocketReader"]


class HttpSocketReader:
    def __init__(self, sock: socket.socket, buffer_size: int = config.BUFFER_SIZE):
        self.sock = sock
        self.buffer_size = buffer_size

    def recv_data(self, size: int = config.BUFFER_SIZE):
        data = self.sock.recv(size)
        return data

    def recv_all_data(self, sock: socket.socket):
        data = sock.recv(self.buffer_size)

        parser = HttpParser()
        parser.execute(data, len(data))

        headers = parser.get_headers()
        content_length = headers.get('Content-Length')

        if parser.is_chunked():
            while not data.endswith(b"0\r\n\r\n"):
                data += sock.recv(self.buffer_size)
        elif content_length:
            while len(data) < int(content_length):
                data += sock.recv(self.buffer_size)

        return data
