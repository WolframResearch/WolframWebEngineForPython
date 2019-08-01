from __future__ import absolute_import, print_function, unicode_literals

from functools import partial
from operator import attrgetter

from django.http import HttpResponse

from wolframclient.language import wl
from wolframclient.utils.decorators import to_dict
from wolframclient.utils.functional import first, iterate, last
from wolframwebengine.web.utils import (
    auto_wait,
    make_generate_httpresponse_expression,
    process_generate_httpresponse_expression,
)
from wolframwebengine.web.utils import to_multipart as _to_multipart

to_multipart = partial(_to_multipart, namegetter=attrgetter("name"))


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
            (
                wl.Rule(k, to_multipart(v))
                for k in request.POST.keys()
                for v in request.POST.getlist(k)
            ),
            (
                wl.Rule(k, to_multipart(v))
                for k in request.FILES.keys()
                for v in request.FILES.getlist(k)
            ),
        )
    )


def generate_http_response(session, request, expression):
    wl_req = django_request_meta(request)

    response = process_generate_httpresponse_expression(
        auto_wait(session.evaluate(make_generate_httpresponse_expression(wl_req, expression)))
    )

    http = HttpResponse(
        content=response.get("BodyByteArray", b""), status=response.get("StatusCode", 200)
    )

    for rule in response.get("Headers", ()):
        http[first(rule.args)] = last(rule.args)

    return http
