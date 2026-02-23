import logging
from typing import Callable

def log_command_action(func: Callable):
    """Декоратор для логування викликів команд"""
    def wrapper(*args, **kwargs):
        logging.info(f"Executing command: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
