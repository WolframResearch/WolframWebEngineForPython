# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import os


def get_wl_handler_path_from_folder(folder, path, index='index.m'):

    absolute = os.path.join(folder, *filter(None, path.split('/')))

    if os.path.isdir(absolute):
        absolute = os.path.join(absolute, index)

    if os.path.exists(absolute):
        return absolute
