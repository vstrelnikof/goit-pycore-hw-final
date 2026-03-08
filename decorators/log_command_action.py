import logging
from decorators.log_action import log_action


def log_command_action(level: int = logging.INFO, log_time: bool = True):
    """Спеціалізований декоратор для команд з увімкненим таймером за дефолтом"""
    return log_action(level=level, log_time=log_time, prefix="Command")
