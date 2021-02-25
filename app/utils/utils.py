# Created by zhouwang on 2020/11/12.
import threading


def lock(func):
    func.__lock__ = threading.Lock()

    def _w(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)
    return _w