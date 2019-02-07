# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from wolframclient.cli.commands.test import Command as TestCommand


class Command(TestCommand):

    modules = ['wolframevaluate.tests']

    dependencies = [
        ("zmq", None),
    ]
