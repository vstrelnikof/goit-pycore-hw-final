import logging

from decorators.log_action import WRAPPED_FUNCNAME_KEY, WRAPPED_MODULE_KEY


class WrappedFuncNameFormatter(logging.Formatter):
    """Formatter, який підставляє wrapped_funcName/wrapped_module з extra замість кадру декоратора."""

    def format(self, record: logging.LogRecord) -> str:
        wrapped_fn = getattr(record, WRAPPED_FUNCNAME_KEY, None)
        wrapped_mod = getattr(record, WRAPPED_MODULE_KEY, None)
        if wrapped_fn is not None:
            record.funcName = wrapped_fn
        if wrapped_mod is not None:
            record.name = wrapped_mod
        return super().format(record)
