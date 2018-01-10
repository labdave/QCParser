import logging
import os
import argparse

from QCModules import BaseModule

class Rbind(BaseModule):

    DESCRIPTION = "Concatenate Two or more QCReports by ROW (e.g. merging across samples)"

    def __init__(self, sys_args):
        super(Rbind, self).__init__(sys_args)

        # Get input file
        self.input_files     = self.args.input_files

    def configure_arg_parser(self, base_parser):

        # Add input file arg parser
        def file_type(arg_string):
            """
            This function check both the existance of input file and the file size
            :param arg_string: file name as string
            :return: file name as string
            """
            if not os.path.exists(arg_string):
                err_msg = "%s does not exist!! " \
                          "Please provide a correct file!!" % arg_string
                raise argparse.ArgumentTypeError(err_msg)
            return arg_string

        # Add input file arguments
        base_parser.add_argument('-i', "--inputs",
                                 action='store',
                                 nargs='+',
                                 dest='input_files',
                                 type=file_type,
                                 required=True,
                                 help="Space-delimited list of QCReport file paths.")

        return base_parser

    def make_qc_report(self):
        pass