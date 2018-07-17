import asyncio

from aioblinker import signal


def handler(sender, a, b):
    print('handler')
    print('а:', a, 'b:', b)


async def async_handler(sender, a, b):
    print('async_handler')
    print('а:', a, 'b:', b)


def worker():
    kwargs = {'a': 1, 'b': 2}
    signal('worker_complete').send(**kwargs)


loop = asyncio.get_event_loop()

worker_complete = signal('worker_complete')
worker_complete.connect(handler)
worker_complete.connect(async_handler)
worker()

loop.run_forever()