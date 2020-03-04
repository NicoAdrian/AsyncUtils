import asyncio
import logging
from functools import wraps, partial


def periodic_callback(func, interval, *args, **kwargs):
    """
    Run awaitable object periodically
    """

    async def do():
        while True:
            try:
                await asyncio.sleep(interval)
                await func(*args, **kwargs)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Error in periodic_callback '{func.__name__}': {e}")

    return asyncio.ensure_future(do())


def run_in_thread(f):
    """
    decorator to run any blocking function in a separate thread
    """

    @wraps(f)
    async def wrapper(*args):
        return await asyncio.get_event_loop().run_in_executor(None, partial(f, *args))

    return wrapper


async def do_sp(cmd):
    """
    Run subprocess
    """
    sp = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await sp.communicate()
    return stdout, stderr
