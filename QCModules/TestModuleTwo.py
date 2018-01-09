import argparse

import QCModules.BaseModule

class TestModuleTwo(QCModules.BaseModule):

    DESCRIPTION = "Dis a testin' tool TWO"

    def __init__(self, command_line_args):
        super(TestModuleTwo, self).__init__(command_line_args)

    def configure_arg_parser(self, base_parser):
        parser = argparse.ArgumentParser(description="Tools for parsing output from several commonly available bioinformatic tools")
        parser.add_argument('--nipples', action='store', dest="derp", help='tools to run')

    def make_qc_report(self):
        pass