import asyncio
import time
import unittest

from test_sync import setup

from pyappbase import Appbase


async def hello_world(d, data):
    while d[0]:
        await asyncio.sleep(0.1)
        data.append("Hello")


class AsnycTests(unittest.TestCase):
    def setUp(self):
        self.appbase = setup(Appbase)
        self.appbase.set_async()

    def test_async_sync_ping_comparison(self):
        # number of simultaneous calls
        call_counts = 4

        self.sync_appbase = setup(Appbase)
        self.sync_appbase.set_async(False)

        t = time.time()
        for i in range(call_counts):
            print(self.sync_appbase.ping())
        sync_difference = time.time() - t
        print()
        print("Syncronous method took ", sync_difference, "s")

        async def get_data():
            return await self.appbase.ping()

        t = time.time()
        loop = asyncio.get_event_loop()

        async def get_data_gathered():
            answer = await asyncio.gather(*[get_data() for _ in range(call_counts)], loop=loop)
            return answer

        print("".join(loop.run_until_complete(get_data_gathered())))
        async_difference = time.time() - t
        print("Asnycronous method took ", async_difference, "s")
        print()

        # the async is more than twice as fast
        self.assertGreater(sync_difference / 2, async_difference)

    def test_async_two_methods(self):
        async def get_data():
            return await self.appbase.ping()

        # some thing multable
        wait = [True]
        data = []
        asyncio.get_event_loop().create_task(hello_world(wait, data))
        results = asyncio.get_event_loop().run_until_complete(get_data())
        wait[0] = False

        async def temp():
            await asyncio.sleep(1)

        asyncio.get_event_loop().run_until_complete(temp())
        print(results)
        self.assertNotEquals(len(data), 0)
