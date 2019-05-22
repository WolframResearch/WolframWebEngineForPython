# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import os
import shutil
import tempfile
import uuid
from wolframwebengine.web.utils import auto_wait
from wolframclient.language import wl
from wolframclient.utils import six
from wolframclient.utils.decorators import to_dict
from wolframclient.utils.encoding import force_text
from django.http import HttpResponse
from wolframclient.utils.functional import iterate, first, last


def to_multipart(v):

    raise NotImplementedError(v)

    if isinstance(v, six.string_types):
        return {"ContentString": v, "InMemory": True}

    destdir = os.path.join(tempfile.gettempdir(), force_text(uuid.uuid4()))
    os.mkdir(destdir)

    with open(os.path.join(destdir, v.filename), "wb") as dest:
        shutil.copyfileobj(v.file, dest)
        return {"FileName": dest.name, "InMemory": False, "OriginalFileName": v.filename}


@to_dict
def django_request_meta(request):
    yield "Method", request.method
    yield "Scheme", request.is_secure() and "https" or "http"
    yield "Domain", request.get_host()
    yield "Port", request.get_port()
    yield "PathString", request.path
    yield "QueryString", request.META["QUERY_STRING"]
    yield "Headers", tuple(wl.Rule(k, v) for k, v in request.headers.items())
    yield "MultipartElements", tuple(
        iterate(
            (wl.Rule(k, v) for k in request.POST.keys() for v in request.POST.getlist(k)),
            (
                wl.Rule(k, to_multipart(v))
                for k in request.FILES.keys()
                for v in request.FILES.getlist(k)
            ),
        )
    )


def generate_http_response(session, request, expression):
    wl_req = django_request_meta(request)

    response = auto_wait(
        session.evaluate(
            wl.GenerateHTTPResponse(expression, wl_req)(
                ("BodyByteArray", "Headers", "StatusCode")
            )
        )
    )

    http = HttpResponse(
        content=response.get("BodyByteArray", b""), status=response.get("StatusCode", 200)
    )

    for rule in response.get("Headers", ()):
        http[first(rule.args)] = last(rule.args)

    return http
