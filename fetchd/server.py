#!/usr/bin/python

import logging
import asyncio
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', default=8888, type=int)
args = parser.parse_args()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def handle_message(reader, writer):
    data = await reader.read()
    message = data.decode()
    logger.debug('Data received: %s', message)


def run():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_message, args.host, args.port, loop=loop)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()


if __name__ == "__main__":
    run()
