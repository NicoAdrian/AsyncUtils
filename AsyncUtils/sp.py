import asyncio

async def run_sp(cmd):
    sp = await asyncio.create_subprocess_exec(
        *cmd.split(), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await sp.communicate()
    return stdout, stderr
