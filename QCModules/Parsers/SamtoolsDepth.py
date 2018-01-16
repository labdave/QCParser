import logging
import pandas as pd
import numpy as np

from BaseParser import BaseParser

class SamtoolsDepth(BaseParser):

    DESCRIPTION     = "Summarize coverage depth from Samtool depth output"
    INPUT_FILE_DESC = "Samtools depth output [Chr Pos Depth]"

    def __init__(self, sys_args):
        super(SamtoolsDepth, self).__init__(sys_args)

        # Get cutoffs for determining coverage depth
        self.cutoffs = self.__format_cutoffs(self.args.cutoffs)
        logging.debug("Samtools depth cutoffs: %s" % self.cutoffs)

    def configure_arg_parser(self, base_parser):

        base_parser = super(SamtoolsDepth, self).configure_arg_parser(base_parser)

        # Add additional option to get depth cutoffs
        base_parser.add_argument('--ct',
                                 action='append',
                                 dest='cutoffs',
                                 default=[5],
                                 type=int,
                                 help="Determine percentage of bases covered above this depth (INT). Can be specified multiple times for multiple cutoffs.")
        return base_parser

    def parse_input(self):

        # Get input table as pandas data frame
        try:
            input_table = pd.read_table(self.input_file, names=["chr", "pos", "depth"], header=None, usecols=["depth"])
        except BaseException, e:
            logging.error("Unable to read SamtoolsDepth output. Make sure input file is 3 column, tab-delimited file (chr pos depth)!")
            if e.message != "":
                logging.error("Received the following error:\n%s" % e.message)

        # Summarize depth column
        results = input_table["depth"].describe()

        # Iterate through key/value pairs and store results
        keys        = ['mean', 'std', 'min', '25%', '50%', '75%', 'max']
        colnames    = ['Mean_cov', 'Cov_sd', 'Min_cov', 'Q1_cov', 'Median_cov', 'Q3_cov', 'Max_cov']
        for i in range(len(keys)):
            self.add_entry(colnames[i], results[[keys[i]]][0])

        # Get percent of bases covered above varying depth cutoffs
        for cutoff in self.cutoffs:
            colname = "pct_cov_gt_%d" % cutoff
            value = self.__get_pct_bases_covered_above_cutoff(input_table, cutoff)
            self.add_entry(colname, value)

    def define_required_colnames(self):
        return ["Mean_cov", "Cov_sd", "Min_cov", "Q1_cov", "Median_cov", "Q3_cov", "Max_cov"]

    @staticmethod
    def __format_cutoffs(cutoffs):
        # Make sure cutoffs are a sorted set
        if len(cutoffs) == 0:
            return cutoffs
        # return sorted list of unique cutoffs
        return sorted(list(set(cutoffs)))

    @staticmethod
    def __get_pct_bases_covered_above_cutoff(input_table, cutoff):
        # Helper function to determine the nubmer of reference bases covered at or above some cutoff
        total_bases = len(input_table) * 1.0
        covered_bases = len(input_table[input_table.depth >= cutoff])
        return (covered_bases / total_bases) * 100
