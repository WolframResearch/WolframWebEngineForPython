from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from wolframclient.utils.importutils import API
from wolframwebengine.web.utils import is_coroutine_function

available_backends = API(
    aiohttp="wolframwebengine.web.aiohttp.generate_http_response",
    django="wolframwebengine.web.django.generate_http_response",
)


def get_backend(backend):
    if not backend in available_backends:
        raise ValueError(
            "Invalid backend %s. Choices are: %s"
            % (backend, ", ".join(available_backends.keys()))
        )
    return available_backends[backend]


def generate_http_response(session, backend):
    generator = get_backend(backend)

    def outer(func):

        if is_coroutine_function(func):

            async def inner(request, *args, **opts):
                return await generator(session, request, await func(request, *args, **opts))

        else:

            def inner(request, *args, **opts):
                return generator(session, request, func(request, *args, **opts))

        return inner

    return outer


aiohttp_wl_view = partial(generate_http_response, backend="aiohttp")
django_wl_view = partial(generate_http_response, backend="django")
