import logging
import os
import argparse
import json

from QCModules import BaseModule
from QCReport import QCReportHelper

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

        # Parse input files as QCReports
        reports = self.parse_input_reports()

        # Get first report
        self.report = reports.pop(0)

        # Rbind successive reports to next report
        for new_report in reports:
            self.report.rbind(new_report)

    def parse_input_reports(self):
        # Parse input files into JSON format
        return [QCReportHelper.load(input_file) for input_file in self.input_files]
