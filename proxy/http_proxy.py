import socket
from threading import Thread

from proxy.http_request_handler import HTTPRequestHandler

__all__ = ["HttpProxy"]


class HttpProxy:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def run(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.bind((self.host, self.port))
        client_socket.listen()
        print(f"Proxy server is running on {self.host}:{self.port}")
        while True:
            source, addr = client_socket.accept()
            print(f"Request from {addr[0]}:{addr[1]}")
            handler = HTTPRequestHandler(source)
            Thread(target=handler.handle).start()
