# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import os

from wolframclient.cli.utils import SimpleCommand
from wolframclient.evaluation import (WolframEvaluatorPool,
                                      WolframLanguageAsyncSession)
from wolframclient.language import wl
from wolframclient.utils.api import aiohttp, asyncio
from wolframclient.utils.functional import last
from wolframengine.explorer import get_wl_handler_path_from_folder
from wolframengine.web import aiohttp_wl_view


class Command(SimpleCommand):
    """ Run test suites from the tests modules.
    A list of patterns can be provided to specify the tests to run.
    """

    def add_arguments(self, parser):
        parser.add_argument('path', default='.', nargs='?')
        parser.add_argument('--port', default=18000, help='Insert the port.')
        parser.add_argument(
            '--kernel',
            default=
            '/Applications/Mathematica.app/Contents/MacOS/WolframKernel',
            help='Insert the kernel path.')
        parser.add_argument(
            '--poolsize',
            default=1,
            help='Insert the kernel pool size.',
            type=int)
        parser.add_argument(
            '--cached',
            default=False,
            help='Insert the server should cache the WL input expression.',
            action='store_true')
        parser.add_argument(
            '--lazy',
            default=False,
            help=
            'Insert the server should should start the kernels on the first request.',
            action='store_true')

    def create_session(self, path, poolsize=1, **opts):
        if poolsize <= 1:
            return WolframLanguageAsyncSession(path, **opts)
        return WolframEvaluatorPool(path, poolsize=poolsize, **opts)

    EXTENSIONS = {
        '.wxf': wl.Function(wl.Import(wl.Slot(), 'WXF')),
        '.mx':  wl.Function(wl.Import(wl.Slot(), 'MX')),
        '.m':   wl.Get, 
        '.wl':  wl.Get, 
    }

    def is_wl_code(self, path):
        try:
            return bool(self.get_wl_handler(path))
        except KeyError:
            return False

    def get_wl_handler(self, path):
        return self.EXTENSIONS[last(os.path.splitext(path)).lower()]

    def create_view(self, session, path, cached):

        path = os.path.abspath(os.path.expanduser(path))

        @aiohttp_wl_view(session)
        async def get_code(request, location=path):
            expr = self.get_wl_handler(location)(location)
            if cached:
                return wl.Once(expr)
            return expr

        if os.path.isdir(path):

            async def view(request):
                loc = get_wl_handler_path_from_folder(path, request.path)

                if not loc:
                    return aiohttp.Response(body = 'Page not found', status = 404)

                if self.is_wl_code(loc):
                    return await get_code(request, location=loc)
                return aiohttp.FileResponse(loc)

            return view

        elif os.path.exists(path):
            if not self.is_wl_code(path):
                raise ValueError('%s must be one of the following formats: %s' % (path, ', '.join(self.EXTENSIONS.keys())))
            return get_code
        else:
            raise ValueError('%s is not an existing path on disk.' % path)

    def get_web_app(self, path, kernel, poolsize, lazy, cached, **opts):

        session = self.create_session(
            kernel, poolsize=poolsize, inputform_string_evaluation=False)
        view = self.create_view(session, path, cached=cached, **opts)

        routes = aiohttp.RouteTableDef()

        @routes.route('*', '/{tail:.*}')
        async def main(request):
            return await view(request)

        app = aiohttp.Application()
        app.add_routes(routes)

        if not lazy:
            asyncio.ensure_future(session.start())

        return app

    def handle(self, port, **opts):
        aiohttp.run_app(self.get_web_app(**opts), port=port)
