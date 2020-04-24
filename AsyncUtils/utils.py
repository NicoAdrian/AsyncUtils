import asyncio
import logging
import time
import functools


class Periodic:
    def __init__(self, cb, interval):
        self.cb = cb
        self.interval = interval
        self._fut = None

    def start(self):
        if self._fut is None:
            self._fut = asyncio.ensure_future(self._run())

    def stop(self):
        if self._fut is not None:
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
            try:
                if is_coro:
                    await self.cb()
                else:
                    self.cb()
            except Exception as ex:
                logging.error(f"[periodic callback] error in {self.cb}: {ex}")

            to_wait = self.interval - (time.time() - t0)


def run_in_thread(f):
    """
    decorator to run any blocking function in an executor
    """

    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        return await asyncio.get_event_loop().run_in_executor(
            None, functools.partial(f, *args, **kwargs)
        )

    return wrapper


async def run_sp(cmd):
    """
    Run subprocess
    """
    sp = await asyncio.create_subprocess_shell(
        *cmd.split(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await sp.communicate()
    return stdout, stderr
