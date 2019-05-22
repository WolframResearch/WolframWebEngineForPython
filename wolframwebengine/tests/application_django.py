# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from wolframclient.utils.tests import TestCase as BaseTestCase

from django.urls import reverse
from django.test import Client


class DjangoTestCase(BaseTestCase):
    def setUp(self):

        from django.conf import settings

        settings.configure(ROOT_URLCONF="wolframwebengine.examples.djangoapp.urls")

        from wolframwebengine.examples.djangoapp.urls import session

        self.session = session
        self.client = Client()

    def test_django_app(self):

        resp = self.client.get(reverse("home"))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, b"hello from django")

        resp = self.client.get(reverse("form"))

        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(reverse("api"))

        self.assertEqual(resp.status_code, 200)

    def tearDown(self):
        if self.session.started:
            self.loop.run_until_complete(self.session.stop())
        super().tearDown()
