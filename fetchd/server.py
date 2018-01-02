#!/usr/bin/python

from SocketServer import TCPServer, StreamRequestHandler
import socket
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DownloadManger(StreamRequestHandler):

    def handle(self):
        self.data = self.rfile.readline().strip()
        logging.info("From <%s>: %s" % (self.client_address, self.data))
        self.wfile.write(self.data.upper() + "\r\n")


class Server(TCPServer):

    # The constant would be better initialized by a systemd module
    SYSTEMD_FIRST_SOCKET_FD = 3
    HOST = 'localhost'
    PORT = 9999

    def __init__(self, handler_cls):
        # Invoke base but omit bind/listen steps (performed by systemd activation!)
        server_address = (self.HOST, self.PORT)
        super().__init__(self, server_address, handler_cls,
                         bind_and_activate=False)

        # Override socket
        self.socket = socket.fromfd(self.SYSTEMD_FIRST_SOCKET_FD,
                                    self.address_family, self.socket_type)


if __name__ == "__main__":
    handler = DownloadManger()
    server = Server(handler)
    server.serve_forever()
