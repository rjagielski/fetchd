#!/usr/bin/env python

import argparse
import asyncio
import collections
import functools
import logging
import time
from itsdangerous import Signer, BadSignature

parser = argparse.ArgumentParser()
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', default=8888, type=int)
parser.add_argument('key')
args = parser.parse_args()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

signer = Signer(args.key)


async def handle_message(reader, writer, queue):
    data = await reader.read()
    try:
        path = signer.unsign(data).decode()
    except BadSignature:
        logger.error('Invalid signature in message: %s', data)
    else:
        queue.put_nowait(path)


async def fetch_queue(queue):
    while True:
        message = await queue.get()
        time.sleep(3)
        logger.info(message)


def run():
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop)
    srv_coro = asyncio.start_server(functools.partial(handle_message, queue=queue),
                                    args.host, args.port, loop=loop)
    fetch_coro = fetch_queue(queue)

    loop.run_until_complete(asyncio.gather(srv_coro, fetch_coro))


if __name__ == "__main__":
    run()
