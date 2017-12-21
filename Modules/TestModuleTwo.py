import argparse

import BaseModule

class TestModuleTwo(BaseModule):

    DESCRIPTION = "Dis a testin' tool"

    def __init__(self, command_line_args, **kwargs):
        super(TestModuleTwo, self).__init__(command_line_args, **kwargs)

    def get_arg_parser(self):
        parser = argparse.ArgumentParser(description="Tools for parsing output from several commonly available bioinformatic tools")
        parser.add_argument('--nipples', action='store', dest="derp", help='tools to run')

    def run(self):
        pass