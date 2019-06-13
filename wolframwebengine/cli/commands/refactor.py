from __future__ import absolute_import, print_function, unicode_literals

from wolframclient.cli.commands.refactor import Command as RefactorCommand


class Command(RefactorCommand):

    modules = ["wolframwebengine"]
