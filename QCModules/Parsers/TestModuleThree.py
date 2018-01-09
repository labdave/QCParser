import argparse

import QCModules.BaseModule

class TestModuleThree(QCModules.BaseModule):

    DESCRIPTION = "Dis a testin' tool THREE"

    def __init__(self, command_line_args):
        super(TestModuleThree, self).__init__(command_line_args)

    def configure_arg_parser(self, base_parser):
        base_parser.add_argument('--derp', action='store', dest="derp", help='tools to run')
        return base_parser

    def run(self):
        pass