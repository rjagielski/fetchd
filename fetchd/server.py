#!/usr/bin/env python

import argparse
import asyncio
import collections
import functools
import logging
import os
import subprocess
from itsdangerous import TimestampSigner, BadSignature

parser = argparse.ArgumentParser()
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', default=8888, type=int)
parser.add_argument('key')
parser.add_argument('target_dir')
parser.add_argument('rsync_host')
args = parser.parse_args()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


signer = TimestampSigner(args.key)


async def run_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')


def run_rsync(remote_path):
    source = '{}:{}'.format(args.rsync_host, remote_path)
    cmd = ['/bin/rsync', '-a', '--partial', '-r', source, args.target_dir]
    logger.debug('Running rsync: %s', ' '.join(cmd))
    await run_cmd(cmd)
    logger.info('Fetching complete %s', os.path.basename(remote_path))


async def handle_message(reader, writer, queue):
    data = await reader.read()
    try:
        path = signer.unsign(data, max_age=5).decode()
    except BadSignature:
        logger.error('Invalid signature in message: %s', data)
    else:
        queue.put_nowait(path)
        logger.info('Added to queue: %s', path)


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
