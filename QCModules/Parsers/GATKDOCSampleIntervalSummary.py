import logging
import pandas as pd

from BaseParser import BaseParser
class GATKDOCSampleIntervalSummary(BaseParser):

    DESCRIPTION     = "Parse the sample interval summary stats from GATK DepthOfCoverage tool."
    INPUT_FILE_DESC = "GATK DepthOfCoverage Sample Interval Summary Statistics TSV output"

    def __init__(self, sys_args):
        super(GATKDOCSampleIntervalSummary, self).__init__(sys_args)

        # Get intervals
        self.intervals           = self.args.intervals

    def configure_arg_parser(self, base_parser):
        base_parser = super(GATKDOCSampleIntervalSummary, self).configure_arg_parser(base_parser)

        # Add sample name argument
        base_parser.add_argument("--int",
                                 nargs="+",
                                 action='store',
                                 dest='intervals',
                                 default=[],
                                 help="List of intervals.")

        return base_parser

    def parse_input(self):

        try:
            # Get input table as pandas data frame
            input_table = pd.read_csv(self.input_file, sep='\t')

        except BaseException, e:
            logging.error("Unable to parse GATK DepthOfCoverage sample interval summary output!")
            if e.message != "":
                logging.error("Received the following error msg:\n%s" % e.message)
            raise

        for interval in self.intervals:
            self.add_entry(interval,
                           input_table[input_table.Target.str.contains('^{0}'.format(interval))][['total_coverage']].iat[0,0]
                           )

    def define_required_colnames(self):
        return [i for i in self.intervals]
