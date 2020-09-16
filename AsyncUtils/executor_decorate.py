import asyncio
import functools


def run_in_executor(f):
    """
    decorator to run any blocking function in an executor
    """

    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        return await asyncio.get_event_loop().run_in_executor(
            None, functools.partial(f, *args, **kwargs)
        )

    return wrapper
