import asyncio
import time


class Periodic:
    def __init__(self, cb, interval):
        self.cb = cb
        self.interval = interval
        self._fut = None

    def start(self):
        if not self.is_running():
            self._fut = asyncio.ensure_future(self._run())

    def stop(self):
        if self.is_running():
            asyncio.ensure_future(self._stop_fut())

    def is_running(self):
        return self._fut is not None

    async def _stop_fut(self):
        self._fut.cancel()
        try:
            await self._fut
        except asyncio.CancelledError:
            pass
        finally:
            self._fut = None

    async def _run(self):
        to_wait = self.interval
        is_coro = asyncio.iscoroutinefunction(self.cb)
        while True:
            if to_wait > 0:
                await asyncio.sleep(to_wait)
            t0 = time.time()
            if is_coro:
                await self.cb()
            else:
                self.cb()
            to_wait = self.interval - (time.time() - t0)
