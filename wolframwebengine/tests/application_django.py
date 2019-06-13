from __future__ import absolute_import, print_function, unicode_literals

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

from wolframclient.utils.api import json
from wolframclient.utils.functional import first
from wolframclient.utils.tests import TestCase as BaseTestCase
from wolframwebengine.web.utils import auto_wait


class DjangoTestCase(BaseTestCase):
    def setUp(self):

        from django.conf import settings

        settings.configure(
            ROOT_URLCONF="wolframwebengine.examples.djangoapp.urls",
            ALLOWED_HOSTS="*",
            DEBUG=True,
        )

        import django

        django.setup()

        from wolframwebengine.examples.djangoapp.urls import session

        self.session = session
        self.client = Client()

    def test_django_app(self):

        resp = self.client.get("/")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, b"hello from django")

        resp = self.client.get("/form")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(first(resp["content-type"].split(";")), "text/html")

        resp = self.client.get("/api")

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp["content-type"], "application/json")

        resp = self.client.get("/api?x=2")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["content-type"], "application/json")
        self.assertEqual(json.loads(resp.content), {"x": "2"})

        resp = self.client.post("/api", {"x": SimpleUploadedFile("foo.txt", b"foobar")})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["content-type"], "application/json")
        self.assertEqual(json.loads(resp.content), {"x": "foobar"})

    def tearDown(self):
        if self.session.started:
            auto_wait(self.session.stop())
        super().tearDown()
