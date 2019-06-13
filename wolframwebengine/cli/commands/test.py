from __future__ import absolute_import, print_function, unicode_literals

from wolframclient.cli.commands.test import Command as TestCommand
from wolframclient.utils.functional import iterate


class Command(TestCommand):

    modules = ["wolframwebengine.tests"]

    dependencies = tuple(iterate((("django", "2.2.1"),), TestCommand.dependencies))
