import os
import logging
import argparse
import abc

from QCModules import BaseModule, QCParseException

class BaseParser(BaseModule):

    __metaclass__ = abc.ABCMeta

    # Description of input file that will be parsed
    # Should be overridden by inheriting classes to be more specific
    INPUT_FILE_DESC = "input file"

    def __init__(self, sys_args):
        super(BaseParser, self).__init__(sys_args)

        # Get input file
        self.input_file     = self.args.input_file

        # Get sample name
        self.sample_name    = self.args.sample_name

        # Define colnames that must be present in QCReport after parsing
        self.required_cols  = self.define_required_columns()

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
                                 help="Path to %s." % self.INPUT_FILE_DESC)

        # Add sample name argument
        base_parser.add_argument('-s', "--sample",
                                 action='store',
                                 dest='sample_name',
                                 required=True,
                                 help="Sample name.")

        return base_parser

    def make_qc_report(self):

        # Parse input file and get data members
        self.parse_input()

        # Check to make sure all required fields were found
        valid_report    = True
        report_cols     = self.report.get_colnames()
        for required_col in self.required_cols:
            if not required_col in report_cols:
                logging.error("Required colnames missing from final QCReport: %s" % required_col)
                valid_report = False

        # Throw exception if not all columns in report
        if not valid_report:
            raise QCParseException("One or more required columns missing from QCReport. See log for details.")

    def add_entry(self, colname, value):
        # Wrapper method for class
        self.report.add_entry(sample=self.sample_name,
                              module=self.__class__.__name__,
                              source_file=self.input_file,
                              colname=colname,
                              value=value)

    @abc.abstractmethod
    def define_required_columns(self):
        # Define colnames required to be present in qc_report after parsing
        pass

    @abc.abstractmethod
    def parse_input(self):
        # Parse input and get
        pass


