import asyncio
import concurrent.futures
import logging
import functools


def periodic_callback(func, interval, args=None, kwargs=None):
    """
    Run awaitable object periodically
    """
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    async def do():
        while True:
            try:
                await func(*args, **kwargs)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Error in periodic callback {func.__name__}: {str(e)}")
            finally:
                await asyncio.sleep(interval)

    return asyncio.ensure_future(do())


def run_in_thread(f):
    """
    decorator to run any function in a separate thread
    """

    @functools.wraps(f)
    async def wrapper(*args):
        await asyncio.get_event_loop().run_in_executor(
            None, functools.partial(f, *args)
        )

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
