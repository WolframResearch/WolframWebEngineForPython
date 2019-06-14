from __future__ import absolute_import, print_function, unicode_literals

import os

from aiohttp import web

from wolframclient.evaluation import WolframEvaluatorPool, WolframLanguageAsyncSession
from wolframclient.language import wl
from wolframclient.utils.functional import last
from wolframwebengine.server.explorer import get_wl_handler_path_from_folder
from wolframwebengine.web import aiohttp_wl_view

EXTENSIONS = {
    ".wxf": wl.Composition(wl.BinaryDeserialize, wl.ReadByteArray),
    ".mx": wl.Function(wl.Import(wl.Slot(), "MX")),
    ".m": wl.Get,
    ".wl": wl.Get,
}


def is_wl_code(path):
    try:
        return bool(get_wl_handler(path))
    except KeyError:
        return False


def get_wl_handler(path):
    return EXTENSIONS[last(os.path.splitext(path)).lower()]


def create_session(path=None, poolsize=1, inputform_string_evaluation=False, **opts):
    if poolsize <= 1:
        return WolframLanguageAsyncSession(
            path, inputform_string_evaluation=inputform_string_evaluation, **opts
        )
    return WolframEvaluatorPool(
        path,
        poolsize=poolsize,
        inputform_string_evaluation=inputform_string_evaluation,
        **opts
    )


def create_view(
    session, path, cached=False, index="index.wl", path_extractor=lambda request: request.path
):

    path = os.path.abspath(os.path.expanduser(path))

    @aiohttp_wl_view(session)
    async def get_code(request, location=path):
        expr = get_wl_handler(location)(location)
        if cached:
            return wl.Once(expr)
        return expr

    if os.path.isdir(path):

        async def view(request):
            loc = get_wl_handler_path_from_folder(path, path_extractor(request), index=index)

            if not loc:
                return web.Response(body="Page not found", status=404)

            if is_wl_code(loc):
                return await get_code(request, location=loc)
            return web.FileResponse(loc)

        return view

    elif os.path.exists(path):
        if not is_wl_code(path):
            raise ValueError(
                "%s must be one of the following formats: %s"
                % (path, ", ".join(EXTENSIONS.keys()))
            )
        return get_code
    else:
        raise ValueError("%s is not an existing path on disk." % path)
