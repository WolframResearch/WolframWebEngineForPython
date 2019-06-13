from __future__ import absolute_import, print_function, unicode_literals

from wolframclient.cli.dispatch import DispatchCommand as _DispatchCommand


class DispatchCommand(_DispatchCommand):

    modules = [] + _DispatchCommand.modules + ["wolframwebengine.cli.commands"]


def execute_from_command_line(argv=None, **opts):
    return DispatchCommand(argv).main()
