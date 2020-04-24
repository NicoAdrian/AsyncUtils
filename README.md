# AsyncUtils
Small set of asynchronous functions I use in personnal projects or work

## Examples

* `run_sp(cmd: str)`: Simply executes the given command and returns stdout, stderr if any.
* `class Periodic(cb: Callable, interval: int)`: Schedule the given function to be called and awaited if needed every `interval` seconds.
  - `start()`: Starts the periodic callback
  - `stop()`: Stops the periodic callback
  - `is_running() -> bool`: Returns `True` if the periodic callback has been started and is not stopped.
* `run_in_executor`: Decorate a blocking function with it to run it in a separate executor, hence awaiting it like a non-blocking function

Use python3.6 or higher
