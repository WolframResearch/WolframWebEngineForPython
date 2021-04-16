from __future__ import absolute_import, print_function, unicode_literals

import sys


def main():
    try:
        from django.conf import settings
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    settings.configure(
        ROOT_URLCONF="wolframwebengine.examples.djangoapp.urls", ALLOWED_HOSTS="*", DEBUG=True
    )

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
