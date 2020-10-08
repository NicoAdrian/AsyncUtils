import asyncio
import logging


class PeriodicCallback:
    def __init__(self, callback, interval):
        self.callback = callback
        self.interval = interval
        self._is_coro = asyncio.iscoroutinefunction(self.callback)
        self._running = False
        self._handle = None

    def start(self):
        self._ioloop = asyncio.get_event_loop()
        self._running = True
        self._next_run = self._ioloop.time()
        self._schedule_next()

    def stop(self):
        self._running = False
        if self._handle is not None:
            self._handle.cancel()
            self._handle = None

    def _log_exc(self, ex):
        logging.error("Exception in periodic callback %s: %s", self.callback, ex)

    async def _run_coro(self):
        try:
            await self.callback()
        except Exception as ex:
            self._log_exc(ex)

    def is_running(self):
        return self._running

    def _run(self):
        if not self.is_running():
            return
        try:
            if self._is_coro:
                asyncio.ensure_future(self._run_coro())
            else:
                self.callback()
        except Exception as ex:
            self._log_exc(ex)
        finally:
            self._schedule_next()

    def _schedule_next(self):
        if self.is_running():
            self._handle = self._ioloop.call_at(self._next_run, self._run)
            self._next_run += self.interval
