import logging
import time
from typing import Tuple
from functools import cache

from .config import Config

logger = logging.getLogger(__name__)


@cache
def get_unit(exp):
    u = exp/3
    exponent = exp - exp % 3
    unit = "s"
    if u == 1:
        unit = "ms"
    if u == 2:
        unit = "µs"
    if u == 3:
        unit = "ns"
    return unit, exponent


def _call(func):
    def inner(*args, **kwargs):
        ret = None
        time_str = None
        if Config.logTime:
            start = time.time()
            unit, exponent = get_unit(
                Config.logTimeMultiplierExponent)
            ret = func(*args, **kwargs)
            duration = time.time() - start
            duration *= 10 ** exponent
            duration = round(duration, Config.logTimePrecision)
            time_str = f"{duration} {unit}"
        else:
            ret = func(*args, **kwargs)
        return ret, time_str

    return inner


def logMethodCall(func):
    def inner(self, *args, **kwargs):
        objStr = repr(self)
        ret, time_str = _call(func)(self, *args, **kwargs)
        if func.__name__ not in Config.ignoreMethods.get(type(self), set({})):
            Config.log(Config.format(args, kwargs, ret,
                       objStr=objStr, method=func, time=time_str))
        return ret

    return inner


def logFuncCall(func):
    def inner(*args, **kwargs):
        ret, time_str = _call(func)(*args, **kwargs)
        Config.log(Config.format(args, kwargs, ret, func=func, time=time_str))
        return ret

    return inner


class MethodLoggerMeta(type):
    def __new__(cls, name: str, bases: Tuple[type], attrs: dict):
        attrs_copy = attrs.copy()
        for key, value in attrs.items():
            if callable(value) and not key.startswith("__"):
                attrs_copy[key] = logMethodCall(value)
        return type(name, bases, attrs_copy)
