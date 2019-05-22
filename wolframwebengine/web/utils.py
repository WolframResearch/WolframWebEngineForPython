# -*- coding: utf-8 -*-

import inspect
from wolframclient.utils.asyncio import get_event_loop

is_coroutine_function = getattr(inspect, "iscoroutinefunction", lambda: False)
is_coroutine = getattr(inspect, "iscoroutine", lambda: False)


def auto_wait(obj, loop=None):
    if is_coroutine(obj):
        return get_event_loop(loop).run_until_complete(obj)
    return obj
