# -*- coding: utf-8 -*-

import inspect


if hasattr(inspect, "iscoroutinefunction"):
    is_coroutine = inspect.iscoroutinefunction
else:
    is_coroutine = lambda func: False
