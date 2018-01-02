#!/usr/bin/env python

import argparse
import asyncio
import collections
import functools
import logging
import subprocess
from itsdangerous import Signer, BadSignature

parser = argparse.ArgumentParser()
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', default=8888, type=int)
parser.add_argument('key')
parser.add_argument('target_dir')
parser.add_argument('rsync_host')
args = parser.parse_args()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

signer = Signer(args.key)


def run_rsync(remote_path):
    source = '{}:{}'.format(args.rsync_host, remote_path)
    cmd = ['/bin/rsync', '-a', '--partial', '-r', source, args.target_dir]
    logger.debug('Running rsync: %s', ' '.join(cmd))
    subprocess.run(cmd)


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
        path = await queue.get()
        run_rsync(path)


def run():
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop)
    srv_coro = asyncio.start_server(functools.partial(handle_message, queue=queue),
                                    args.host, args.port, loop=loop)
    fetch_coro = fetch_queue(queue)

    loop.run_until_complete(asyncio.gather(srv_coro, fetch_coro))


if __name__ == "__main__":
    run()
