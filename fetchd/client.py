#!/usr/bin/python

import argparse
import asyncio


parser = argparse.ArgumentParser()
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', default=8888, type=int)
parser.add_argument('path')
args = parser.parse_args()


async def send_path(loop):
    _, writer = await asyncio.open_connection(args.host, args.port, loop=loop)
    writer.write(args.path.encode())
    writer.close()


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_path(loop))
    loop.close()


if __name__ == "__main__":
    run()
