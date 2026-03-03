import inspect
import logging
import time
from functools import wraps
from typing import Callable

logger = logging.getLogger(__name__)

def log_action(level: int = logging.INFO, log_time: bool = False, prefix: str = "Action"):
    """Фабрика декораторів для логування"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.log(level, f"{prefix}: {func.__name__} started")
            start: float | None = time.perf_counter() if log_time else None
            # Перевірка на асинхронність
            if inspect.iscoroutinefunction(func):
                async def async_wrapper():
                    res = await func(*args, **kwargs)
                    _finish(start)
                    return res
                return async_wrapper()
            result = func(*args, **kwargs)
            _finish(start)
            return result

        def _finish(start_time) -> None:
            msg = f"{prefix}: {func.__name__} finished"
            if start_time:
                duration = time.perf_counter() - start_time
                msg += f" in {duration:.4f}s"
            logger.log(level, msg)

        return wrapper
    return decorator
