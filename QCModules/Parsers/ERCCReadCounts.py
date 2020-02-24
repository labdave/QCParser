from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException
import logging
import pandas as pd

class ERCCReadCounts(BaseParser):

    DESCRIPTION     = "Parse a file containing ERCC counts"
    INPUT_FILE_DESC = "GetERCCReadCounts generated read counts file"

    def __init__(self, sys_args):
        super(ERCCReadCounts, self).__init__(sys_args)

        self.ercc_baits = self.args.ercc_baits

    def configure_arg_parser(self, base_parser):
        base_parser = super(ERCCReadCounts, self).configure_arg_parser(base_parser)

        # Add sample name argument
        base_parser.add_argument("--ercc-baits",
                                 nargs="+",
                                 action='store',
                                 dest='ercc_baits',
                                 default=[],
                                 help="List of ercc baits.")

        return base_parser

    def parse_input(self):

        # parse the input
        try:
            # Get input table as pandas data frame
            input_table = pd.read_csv(self.input_file, sep=' ', header=None)
        except BaseException, e:
            logging.error("Unable to ercc read counts!")
            if e.message != "":
                logging.error("Received the following error msg:\n%s" % e.message)
            raise

        # add read counts to the db

        for bait in self.ercc_baits:
            if bait in input_table.values:
                self.add_entry(bait, input_table.loc[input_table[0] == bait].iat[0,1])
            else:
                self.add_entry(bait, 0)

    def define_required_colnames(self):
        return [bait for bait in self.ercc_baits]
