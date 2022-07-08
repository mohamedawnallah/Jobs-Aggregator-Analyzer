import functools
from this import d
import time
from typing import Callable, Any
from loguru import logger


Decorator = Callable

def timer(func) -> Decorator:
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs) -> Any:
        """Wrapper Timer"""
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        message = f"{func.__name__!r} took {run_time:.4f} seconds"
        logger.debug(message)
        return value

    return wrapper_timer


def slow_down(func) -> Decorator:
    """Sleep 1 second before calling the function"""

    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs) -> Any:
        """Wrapper Slower Down"""
        time.sleep(1)
        value = func(*args, **kwargs)
        return value

    return wrapper_slow_down


def debug(func) -> Decorator:
    """Print the function signature and return the value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs) -> Any:
        """Wrapper Debugger"""
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}= {v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        logger.debug(f"{func.__name__!r} returned {value!r}")
        return value

    return wrapper_debug
