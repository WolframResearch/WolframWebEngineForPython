from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from wolframclient.language import wl
from wolframclient.utils.api import aiohttp
from wolframclient.utils.decorators import to_dict
from wolframclient.utils.encoding import force_text
from wolframwebengine.web.utils import (
    make_generate_httpresponse_expression,
    process_generate_httpresponse_expression,
)
from wolframwebengine.web.utils import to_multipart as _to_multipart

to_multipart = partial(
    _to_multipart, namegetter=lambda f: f.filename, filegetter=lambda f: f.file
)


@to_dict
def aiohttp_request_meta(request, post):
    yield "Method", request.method
    yield "Scheme", request.url.scheme
    yield "Domain", request.url.host
    yield "Port", force_text(request.url.port)
    yield "PathString", request.url.path
    yield "QueryString", request.url.query_string
    yield "Headers", tuple(wl.Rule(k, v) for k, v in request.headers.items())
    yield "MultipartElements", tuple(wl.Rule(k, to_multipart(v)) for k, v in post.items())


async def generate_http_response(session, request, expression):
    wl_req = aiohttp_request_meta(request, await request.post())

    response = process_generate_httpresponse_expression(
        await session.evaluate(make_generate_httpresponse_expression(wl_req, expression))
    )

    return aiohttp.Response(
        body=response.get("BodyByteArray", b""),
        status=response.get("StatusCode", 200),
        headers=aiohttp.CIMultiDict(rule.args for rule in response.get("Headers", ())),
    )
