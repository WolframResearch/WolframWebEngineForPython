from __future__ import absolute_import, print_function, unicode_literals

import os


def get_wl_handler_path_from_folder(folder, path, index="index.wl"):

    absolute = os.path.join(folder, *filter(None, path.split("/")))

    if os.path.isdir(absolute):
        if index:
            absolute = os.path.join(absolute, index)
        else:
            return

    if os.path.exists(absolute):
        return absolute
