#!/usr/bin/python

import socket
import logging


HOST = ''
PORT = 50007
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)

        try:
            while True:
                conn, addr = s.accept()
                with conn:
                    logging.info('Connection from %s', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data: break
                        conn.sendall(data)
        finally:
            connection.close()


if __name__ == "__main__":
    run()
