import socket

from proxy.http_request import HttpRequest
from proxy.http_socket_reader import HttpSocketReader

__all__ = ["HTTPRequestHandler"]


class HTTPRequestHandler:
    def __init__(self, source: socket.socket):
        self.source = source
        self.request = None
        self.server = None

    def handle(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.request = HttpRequest(self.source)

        if not self.request.raw_data:
            self.source.close()
            return
        if self.request.secure_connection_required:
            self.__handle_https_request()
        else:
            self.__handle_http_request()

    def __handle_http_request(self):
        try:
            self.server.connect((self.request.host, self.request.port))
            self.server.sendall(self.request.raw_data)
            response = HttpSocketReader(self.server).recv_data()
            self.source.sendall(response)
        except socket.error as e:
            print(f"Could not establish http connection with {self.request.host}:{self.request.port}: {e}")
        finally:
            self.server.close()
            self.source.close()

    def __handle_https_request(self):
        try:
            self.server.connect((self.request.host, self.request.port))
            reply = (
                "HTTP/1.1 200 Connection established\r\n"
                "ProxyServer-agent: PyProxy\r\n\r\n"
            )
            self.source.sendall(reply.encode())
            self.source.setblocking(False)
            self.server.setblocking(False)

            while True:
                try:
                    data = HttpSocketReader(self.source).recv_data()
                    if not data:
                        break
                    self.server.sendall(data)
                except socket.error:
                    pass

                try:
                    reply = HttpSocketReader(self.server).recv_data()
                    if not reply:
                        break
                    self.source.sendall(reply)
                except socket.error:
                    pass
        except socket.error as e:
            print(
                f"Could not establish https connection with {self.request.host}:{self.request.port}: {e}"
            )
        finally:
            self.server.close()
            self.source.close()
