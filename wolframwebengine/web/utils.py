from __future__ import absolute_import, print_function, unicode_literals

import inspect
import os
import shutil
import tempfile
import uuid

from wolframclient.language import wl
from wolframclient.serializers import export
from wolframclient.utils import six
from wolframclient.utils.asyncio import get_event_loop
from wolframclient.utils.encoding import force_text
from wolframclient.utils.functional import identity

is_coroutine_function = getattr(inspect, "iscoroutinefunction", lambda: False)
is_coroutine = getattr(inspect, "iscoroutine", lambda: False)


def auto_wait(obj, loop=None):
    if is_coroutine(obj):
        return get_event_loop(loop).run_until_complete(obj)
    return obj


def make_generate_httpresponse_expression(request, expression):
    return wl.GenerateHTTPResponse(wl.Unevaluated(expression), request)(
        ("BodyByteArray", "Headers", "StatusCode")
    )


def process_generate_httpresponse_expression(response):
    if isinstance(response, dict):
        if not response.get('BodyByteArray', None):
            #empty byte array is returning a an empty list, we need an empty byte array
            response['BodyByteArray'] = b''
        return response
    return {
        "BodyByteArray": export(response, target_format="wl"),
        "Headers": (wl.Rule("content-type", "text/plain;charset=utf-8"),),
        "StatusCode": 500,
    }


def to_multipart(v, namegetter=identity, filegetter=identity):
    if isinstance(v, six.string_types):
        return {"ContentString": v, "InMemory": True}

    destdir = os.path.join(tempfile.gettempdir(), force_text(uuid.uuid4()))
    os.mkdir(destdir)

    with open(os.path.join(destdir, namegetter(v)), "wb") as dest:
        shutil.copyfileobj(filegetter(v), dest)
        return {"FileName": dest.name, "InMemory": False, "OriginalFileName": namegetter(v)}
