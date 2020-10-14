import asyncio
import logging


class Periodic:
    def __init__(self, callback, interval):
        self.callback = asyncio.coroutine(callback)
        self.interval = interval
        self._running = False

    def start(self):
        if not self.is_running():
            self._ioloop = asyncio.get_event_loop()
            self._running = True
            self._run()

    def stop(self):
        if self.is_running():
            self._handle.cancel()
            self._running = False

    async def _run_callback(self):
        try:
            await self.callback()
        except Exception as ex:
            logging.error("Exception in periodic callback '%s': %s", self.callback, ex)

    def is_running(self):
        return self._running

    def _run(self):
        asyncio.ensure_future(self._run_callback())
        self._handle = self._ioloop.call_later(self.interval, self._run)
