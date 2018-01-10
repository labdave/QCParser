import logging
import argparse
import os

from QCModules import BaseModule, QCParseException

class PrintTable(BaseModule):

    DESCRIPTION = "Print QCReport to tab-delimited table."

    def __init__(self, sys_args):
        super(PrintTable, self).__init__(sys_args)

        # Get input file
        self.input_file     = self.args.input_file

        # Get alt-colnames
        self.alt_colnames   = self.args.alt_colnames

        # Get visible columns
        self.visible_cols   = self.args.visible_cols

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
        base_parser.add_argument('-i', "--input",
                                action='store',
                                dest='input_file',
                                type=file_type,
                                required=True,
                                help="Path to JSON-formatted QCReport.")

        # Add argument to be able to specify colname aliases for each colname
        base_parser.add_argument("--alt-colnames",
                                 action='store',
                                 nargs = '*',
                                 dest='alt_colnames',
                                 default=[],
                                 help="Space-delimited list of alternative column names. '-' character indicates use default colname."
                                      "List must be equal in length to number of column names. Example: Num_Reads - - Total_Reads")

        # Add argument to specify which columns to print and in which order
        base_parser.add_argument("--col-order",
                                 action='store',
                                 dest='visible_cols',
                                 nargs='*',
                                 default=[],
                                 type=int,
                                 help="Space-delimited list that specifies column order. Columns included by index (Starting from 0)."
                                      "Columns can be ommitted and/or jumbled but all indices must be smaller than the total number of columns.")

        return base_parser

    def make_qc_report(self):
        pass
