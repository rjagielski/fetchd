#!/usr/bin/env python

import argparse
import asyncio
import logging
from itsdangerous import TimestampSigner

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', default=8888, type=int)
parser.add_argument('key')
parser.add_argument('path')
args = parser.parse_args()


async def send_path(loop):
    signer = TimestampSigner(args.key)
    message = signer.sign(args.path.encode('utf-8'))
    logger.debug('message: %s', message)

    _, writer = await asyncio.open_connection(args.host, args.port, loop=loop)
    writer.write(message)
    writer.close()


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_path(loop))
    loop.close()


if __name__ == "__main__":
    run()
