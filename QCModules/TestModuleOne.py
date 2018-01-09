import argparse

import QCModules.BaseModule

class TestModuleOne(QCModules.BaseModule):

    DESCRIPTION = "Dis a testin' tool ONE"

    def __init__(self, command_line_args):
        super(TestModuleOne, self).__init__(command_line_args)

    def configure_arg_parser(self, base_parser):
        base_parser.add_argument('--derp', action='store', dest="derp", help='tools to run')
        return base_parser

    def make_qc_report(self):
        pass