# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import os

from aiohttp import web

from wolframclient.cli.utils import SimpleCommand
from wolframclient.evaluation import (WolframEvaluatorPool,
                                      WolframLanguageAsyncSession)
from wolframclient.language import wl
from wolframclient.utils.api import asyncio
from wolframclient.utils.functional import last
from wolframwebengine.explorer import get_wl_handler_path_from_folder
from wolframwebengine.web import aiohttp_wl_view


class Command(SimpleCommand):
    """ Run test suites from the tests modules.
    A list of patterns can be provided to specify the tests to run.
    """

    ServerRunner = web.ServerRunner
    Server = web.Server
    TCPSite = web.TCPSite

    def add_arguments(self, parser):
        parser.add_argument('path', default='.', nargs='?')
        parser.add_argument('--port', default=18000, help='Insert the port.')
        parser.add_argument(
            '--domain', default='localhost', help='Insert the domain.')
        parser.add_argument(
            '--kernel',
            default=None,
            help='Insert the kernel path.')
        parser.add_argument(
            '--poolsize',
            default=1,
            help='Insert the kernel pool size.',
            type=int)
        parser.add_argument(
            '--cached',
            default=False,
            help='The server will cache the WL input expression.',
            action='store_true')
        parser.add_argument(
            '--lazy',
            default=False,
            help='The server will start the kernels on the first request.',
            action='store_true')
        parser.add_argument(
            '--index',
            default='index.m',
            help='The file name to search for folder index.',
        )

    def create_session(self, path, poolsize=1, **opts):
        if poolsize <= 1:
            return WolframLanguageAsyncSession(path, **opts)
        return WolframEvaluatorPool(path, poolsize=poolsize, **opts)

    EXTENSIONS = {
        '.wxf': wl.Function(wl.Import(wl.Slot(), 'WXF')),
        '.mx': wl.Function(wl.Import(wl.Slot(), 'MX')),
        '.m': wl.Get,
        '.wl': wl.Get,
    }

    def is_wl_code(self, path):
        try:
            return bool(self.get_wl_handler(path))
        except KeyError:
            return False

    def get_wl_handler(self, path):
        return self.EXTENSIONS[last(os.path.splitext(path)).lower()]

    def create_view(self, session, path, cached, index):

        path = os.path.abspath(os.path.expanduser(path))

        @aiohttp_wl_view(session)
        async def get_code(request, location=path):
            expr = self.get_wl_handler(location)(location)
            if cached:
                return wl.Once(expr)
            return expr

        if os.path.isdir(path):

            async def view(request):
                loc = get_wl_handler_path_from_folder(
                    path, request.path, index=index)

                if not loc:
                    return web.Response(body='Page not found', status=404)

                if self.is_wl_code(loc):
                    return await get_code(request, location=loc)
                return web.FileResponse(loc)

            return view

        elif os.path.exists(path):
            if not self.is_wl_code(path):
                raise ValueError('%s must be one of the following formats: %s'
                                 % (path, ', '.join(self.EXTENSIONS.keys())))
            return get_code
        else:
            raise ValueError('%s is not an existing path on disk.' % path)

    def handle(self, domain, port, path, kernel, poolsize, lazy, cached,
               **opts):

        session = self.create_session(
            kernel, poolsize=poolsize, inputform_string_evaluation=False)
        view = self.create_view(session, path, cached=cached, **opts)

        async def main():

            self.print(
                "======= Serving on http://%s:%s/ ======" % (domain, port))

            runner = self.ServerRunner(self.Server(view))
            await runner.setup()
            await self.TCPSite(runner, domain, port).start()

            if not lazy:
                await session.start()

            while True:
                await asyncio.sleep(3600)

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            self.print('Requested server shutdown, closing session...')
            loop.run_until_complete(session.stop())

        loop.close()
