from __future__ import absolute_import, print_function, unicode_literals

from urllib.parse import urlparse

from aiohttp import web
from aiohttp.formdata import FormData
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from wolframclient.language import wl
from wolframclient.utils.functional import first
from wolframclient.utils.importutils import module_path
from wolframwebengine.server.app import create_session, create_view
from wolframwebengine.web import aiohttp_wl_view
from wolframwebengine.web.utils import auto_wait


class WolframEngineTestCase(AioHTTPTestCase):
    async def get_application(self):

        self.session = create_session(poolsize=1)
        routes = web.RouteTableDef()

        @routes.get("/")
        async def hello(request):
            return web.Response(text="Hello from aiohttp")

        @routes.get("/form")
        @routes.post("/form")
        @aiohttp_wl_view(self.session)
        async def form_view(request):
            return wl.FormFunction({"x": "String"}, wl.Identity, "JSON")

        @routes.get("/api")
        @routes.post("/api")
        @aiohttp_wl_view(self.session)
        async def api_view(request):
            return wl.APIFunction({"x": "String"}, wl.Identity, "JSON")

        @routes.get("/request/{name:.*}")
        @routes.post("/request/{name:.*}")
        @aiohttp_wl_view(self.session)
        async def request_view(request):
            return wl.Delayed(
                wl.HTTPRequestData(
                    ["Method", "Scheme", "Domain", "PathString", "QueryString", "FormRules"]
                ),
                "JSON",
            )

        path = module_path("wolframwebengine", "examples", "sampleapp")

        for cached in (True, False):

            root = cached and "/cached" or "/app"
            view = create_view(
                session=self.session,
                path=path,
                cached=cached,
                path_extractor=lambda request, l=len(root): request.path[l:],
                index="index.wl",
            )

            routes.get(root + "{name:.*}")(view)
            routes.post(root + "{name:.*}")(view)

        app = web.Application()
        app.add_routes(routes)

        return app

    @unittest_run_loop
    async def test_aiohttp(self):

        for method, path, data in (
            ("GET", "/request/", []),
            ("GET", "/request/bar/bar?a=2", []),
            ("POST", "/request/some/random/path", {"a": "2"}),
        ):

            parsed = urlparse(path)

            resp = await self.client.request(method, path, data=data or None)

            self.assertEqual(resp.status, 200)
            self.assertEqual(
                await resp.json(),
                [method, "http", "127.0.0.1", parsed.path, parsed.query, data],
            )

        for cached in (True, False):

            root = cached and "/cached" or "/app"

            resp1 = await self.client.request("GET", root + "/random.wl")
            resp2 = await self.client.request("GET", root + "/random.wl")

            self.assertIsInstance(float(await resp1.text()), float)
            (cached and self.assertEqual or self.assertNotEqual)(
                await resp1.text(), await resp2.text()
            )

        for loc, content in (
            ("", '"Hello from / in a folder!"'),
            ("/", '"Hello from / in a folder!"'),
            ("/index.wl", '"Hello from / in a folder!"'),
            ("/foo", '"Hello from foo"'),
            ("/foo/", '"Hello from foo"'),
            ("/foo/index.wl", '"Hello from foo"'),
            ("/foo/bar", '"Hello from foo/bar"'),
            ("/foo/bar", '"Hello from foo/bar"'),
            ("/foo/bar/index.wl", '"Hello from foo/bar"'),
            ("/foo/bar/something.wl", '"Hello from foo/bar/something"'),
        ):
            resp = await self.client.request("GET", root + loc)
            self.assertEqual(resp.status, 200)
            self.assertEqual(await resp.text(), content)

        for loc in ("/some-random-url", "/404", "/some-/nonsense"):
            resp = await self.client.request("GET", root + loc)
            self.assertEqual(resp.status, 404)

        for fmt in ("wxf", "mx", "m", "wl", "json"):

            resp = await self.client.request("GET", root + "some." + fmt)

            self.assertEqual(resp.status, 200)
            self.assertEqual(len(await resp.json()), 4)
            self.assertEqual((await resp.json())[0:3], ["hello", "from", fmt.upper()])
            self.assertIsInstance((await resp.json())[-1], int)

            self.assertEqual(resp.headers["Content-Type"], "application/json")

        resp = await self.client.request("GET", "/")

        self.assertEqual(resp.status, 200)
        self.assertEqual(await resp.text(), "Hello from aiohttp")

        for root in ("", "/app"):

            resp = await self.client.request("GET", root + "/api")

            self.assertEqual(resp.status, 400)
            self.assertEqual((await resp.json())["Success"], False)
            self.assertEqual(resp.headers["Content-Type"], "application/json")

            resp = await self.client.request("GET", root + "/api?x=a")

            self.assertEqual(resp.status, 200)
            self.assertEqual((await resp.json())["x"], "a")
            self.assertEqual(resp.headers["Content-Type"], "application/json")

            resp = await self.client.request("GET", root + "/form")

            self.assertEqual(resp.status, 200)
            self.assertEqual(first(resp.headers["Content-Type"].split(";")), "text/html")

            resp = await self.client.request("POST", root + "/form", data={"x": "foobar"})

            self.assertEqual(resp.status, 200)
            self.assertEqual((await resp.json())["x"], "foobar")
            self.assertEqual(resp.headers["Content-Type"], "application/json")

            data = FormData()
            data.add_field("x", b"foobar", filename="somefile.txt")

            resp = await self.client.request("POST", root + "form", data=data)

            self.assertEqual(resp.status, 200)
            self.assertEqual((await resp.json())["x"], "foobar")
            self.assertEqual(resp.headers["Content-Type"], "application/json")

    def tearDown(self):
        if self.session.started:
            auto_wait(self.session.stop(), loop=self.loop)
        super().tearDown()
