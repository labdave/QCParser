import logging
import argparse
import os

from QCModules import BaseModule, QCParseException
from QCReport import QCReportHelper

class PrintTable(BaseModule):

    DESCRIPTION = "Print QCReport to tab-delimited table."

    def __init__(self, sys_args):
        super(PrintTable, self).__init__(sys_args)

        # Get input file
        self.input_file     = self.args.input_file

        # Get alt-colnames
        self.alt_colnames   = self.args.alt_colnames

        # Get visible columns
        self.col_order      = self.args.col_order

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
                                 dest='col_order',
                                 nargs='*',
                                 default=[],
                                 type=int,
                                 help="Space-delimited list that specifies column order. Columns included by index (Starting from 0)."
                                      "Columns can be ommitted and/or jumbled but all indices must be smaller than the total number of columns.")

        return base_parser

    def make_qc_report(self):

        # Load QCReport from input file
        self.report = QCReportHelper.load(self.input_file)

        # Set order of columns as they will appear in the table
        self.col_order = range(self.report.n_columns()) if len(self.col_order) == 0 else self.col_order

        # Check column order
        self.__check_col_order()
        logging.debug("Col order is fine!")

        # Check that alt-colnames is equal to the number of columns in col_order
        self.__check_colnames()
        logging.debug("Col names are fine!")

        final_col_names = ["Sample"] + self.__get_colnames()

        # Loop through samples and get values for each column requested
        self.report_string = "\t".join(final_col_names) + "\n"

        # Loop through samples and subset
        for sample in self.report.get_sample_names():
            # Get sample data values in order requested and format as tab-delimited string
            sample_data = [sample] + [str(self.report.get_entry(sample, i)["Value"]) for i in self.col_order]
            self.report_string += "\t".join(sample_data) + "\n"

    def output_qc_report(self):
        # Print table string instead of
        print self.report_string

    def __get_colnames(self):
        # Determine the list of column names as they will appear in the report

        # Get complete list of current colnames
        curr_colnames   = self.report.get_colnames(self.report.get_sample_names()[0])

        # Default column names ordered as they'll appear in the table
        final_colnames  = [curr_colnames[i] for i in self.col_order]

        # Replace default colnames with any alternative colnames
        for i in range(len(self.alt_colnames)):
            final_colnames[i] = self.alt_colnames[i] if self.alt_colnames[i] != "-" else final_colnames[i]

        return final_colnames

    def __check_col_order(self):
        # Check to make sure all values of col-order are within range [0, n_col]
        if max(self.col_order) >= self.report.n_columns():
            logging.error("Invalid col order! Col-order contains column indices greater than number of columns in input report (%s)!"
                          % self.report.n_columns())
            raise QCParseException("Invalid col-order!")
        if min(self.col_order) < 0:
            logging.error("Invalid col order! All column indices must be >= 0!")
            raise QCParseException("Invalid col-order!")

    def __check_colnames(self):
        # Check to make sure num colnames and num columns is same
        if len(self.alt_colnames) > 0 and len(self.alt_colnames) != len(self.col_order):
            logging.error("Must provide same number of alternative colnames (%s) as columns (%s)!" % (
                len(self.alt_colnames), len(self.col_order)))
            raise QCParseException("Alternative colnames provided don't match number of columns that will appear in table!")

