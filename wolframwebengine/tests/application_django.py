# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from wolframclient.utils.tests import TestCase as BaseTestCase
from django.urls import reverse
from django.test import Client
from wolframwebengine.web.utils import auto_wait
from wolframclient.utils.functional import first


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

        resp = self.client.get(reverse("home"))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, b"hello from django")

        resp = self.client.get(reverse("form"))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(first(resp["content-type"].split(";")), "text/html")

        resp = self.client.get(reverse("api"))

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp["content-type"], "application/json")

    def tearDown(self):
        if self.session.started:
            auto_wait(self.session.stop())
        super().tearDown()
