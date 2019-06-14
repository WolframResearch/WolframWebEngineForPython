from __future__ import absolute_import, print_function, unicode_literals

import os

from wolframclient.utils.importutils import module_path
from wolframclient.utils.tests import TestCase as BaseTestCase
from wolframwebengine.server.explorer import get_wl_handler_path_from_folder


class TestCase(BaseTestCase):
    def test_sample_explorer(self):

        folder = module_path("wolframwebengine", "examples", "sampleapp")

        for path, resolved in (
            ("/", "index.wl"),
            ("/random.wl", "random.wl"),
            ("/foo/bar/", "foo/bar/index.wl"),
            ("/foo/", "foo/index.wl"),
            ("/foo/bar/index.wl", "foo/bar/index.wl"),
            ("/foo/bar/something.wl", "foo/bar/something.wl"),
        ):

            self.assertEqual(
                get_wl_handler_path_from_folder(folder, path), os.path.join(folder, resolved)
            )
