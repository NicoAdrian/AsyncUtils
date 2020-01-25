# AsyncUtils
Small set of asynchronous functions I use in personnal projects or work

## Examples

* `do_sp(cmd: str)`: Simply executes the given command and returns stdout, stderr if any.
* `periodic_callback(f: function, interval: int, *args, **kwargs)`: Schedule the given function to be called and awaited every `interval` seconds with the given args and kwargs
* `run_in_thread`: Decorate a blocking function with it to run it in a separate thread, hence awaiting it like a non-blocking function

Use python3.6 or higher
