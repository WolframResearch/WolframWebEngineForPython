from __future__ import absolute_import, print_function, unicode_literals

import logging
import os
import sys

from aiohttp import web
from aiohttp.abc import AbstractAccessLogger

from wolframclient.cli.utils import SimpleCommand
from wolframclient.exception import WolframKernelException
from wolframclient.utils.api import asyncio
from wolframclient.utils.decorators import cached_property, to_dict
from wolframclient.utils.functional import first
from wolframclient.utils.importutils import module_path
from wolframwebengine.server.app import create_session, create_view, is_wl_code


class AccessLogger(AbstractAccessLogger):
    def log(self, request, response, time):
        self.logger.info(
            "%s %s done in %.4fs: %s" % (request.method, request.path, time, response.status)
        )


class Command(SimpleCommand):
    """ Run test suites from the tests modules.
    A list of patterns can be provided to specify the tests to run.
    """

    ServerRunner = web.ServerRunner
    Server = web.Server
    TCPSite = web.TCPSite
    AccessLogger = AccessLogger

    def add_arguments(self, parser):
        parser.add_argument("path", default=".", nargs="?")
        parser.add_argument("--port", default=18000, help="Insert the port.")
        parser.add_argument("--domain", default="localhost", help="Insert the domain.")
        parser.add_argument("--kernel", default=None, help="Insert the kernel path.")
        parser.add_argument(
            "--poolsize", default=1, help="Insert the kernel pool size.", type=int
        )
        parser.add_argument(
            "--cached",
            default=False,
            help="The server will cache the WL input expression.",
            action="store_true",
        )
        parser.add_argument(
            "--lazy",
            default=False,
            help="The server will start the kernels on the first request.",
            action="store_true",
        )
        parser.add_argument(
            "--index", default="index.wl", help="The file name to search for folder index."
        )

        parser.add_argument(
            "--demo",
            nargs="?",
            default=False,
            help="Run a demo application",
            choices=tuple(self.demo_choices.keys()),
        )

    def print_line(self, f="", s=""):
        self.print(f.ljust(15), s)

    def print_separator(self):
        self.print("-" * 70)

    @cached_property
    @to_dict
    def demo_choices(self):

        yield None, "form.wl"

        for path in os.listdir(self.demo_path()):

            if os.path.isdir(path):
                yield path, path

            if is_wl_code(path):
                yield first(os.path.splitext(path)), path

    def demo_path(self, *args):
        return module_path("wolframwebengine", "examples", "demo", *args)

    def handle(self, domain, port, path, kernel, poolsize, lazy, index, demo, **opts):

        if demo is None or demo:
            path = self.demo_path(self.demo_choices[demo])

        path = os.path.abspath(os.path.expanduser(path))

        try:
            session = create_session(kernel, poolsize=poolsize)

        except WolframKernelException as e:
            self.print(e)
            self.print("Use --help to display all available options.")
            sys.exit(1)

        async def main():

            view = create_view(session, path, index=index, **opts)

            runner = self.ServerRunner(self.Server(view, access_log_class=self.AccessLogger))
            await runner.setup()
            await self.TCPSite(runner, domain, port).start()

            self.print_separator()

            isdir = os.path.isdir(path)

            for args in (
                ("Address", "http://%s:%s/" % (domain, port)),
                (isdir and "Folder" or "File", path),
            ):
                self.print_line(*args)

            if isdir:

                if index:
                    self.print_line("Index", index)

                if not os.path.exists(os.path.join(path, index)):
                    self.print_separator()
                    self.print_line(
                        "Warning", "The folder %s doesn't contain an %s file." % (path, index)
                    )
                    self.print_line("", "No content will be served for the homepage.")

            self.print_separator()

            if sys.platform == 'win32':
                self.print_line("(Press CTRL+BREAK to quit)")
            else:
                self.print_line("(Press CTRL+C to quit)")

            self.print_line()

            logging.basicConfig(level=logging.INFO, format="%(message)s")

            if not lazy:
                await session.start()

            while True:
                await asyncio.sleep(3600)

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            if session.started:
                self.print("Requested server shutdown, closing session...")
                loop.run_until_complete(session.stop())

        loop.close()
