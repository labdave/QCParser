from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException
import logging
import pandas as pd

class StarGeneReadCounts(BaseParser):

    DESCRIPTION     = "Parse Star produced gene read counts (v2.6 and later)"
    INPUT_FILE_DESC = "Star generated gene read counts file"

    def __init__(self, sys_args):
        super(StarGeneReadCounts, self).__init__(sys_args)

        self.ERCC_baits = ["ERCC-00004", "ERCC-00046", "ERCC-00051", "ERCC-00054", "ERCC-00060", "ERCC-00074",
                           "ERCC-00077", "ERCC-00079", "ERCC-00085", "ERCC-00095", "ERCC-00097", "ERCC-00108",
                           "ERCC-00116", "ERCC-00134", "ERCC-00142", "ERCC-00148", "ERCC-00156", "ERCC-00171"]

    def parse_input(self):

        # Parse TNADemux stat output
        first_line      = True

        with open(self.input_file, "r") as fh:

            # Parse summary file and store results
            for line in fh:
                # Strip newlines
                line = line.strip().split("\t")

                # Check to make sure file is actually the correct filetype
                if first_line:
                    if "N_unmapped" not in line:
                        raise QCParseException("Star gene read counts file '%s' does not contain 'N_unmapped' in first line. Make sure the format of the file!")
                    elif len(line) != 4:
                        raise QCParseException("Star gene read counts file '%s' does not have exactly four columns! Expected columns: gene,unstranded counts,forward strand count,reverse strand count. Make sure it's the all_barcode_stats.txt!")

                    break

            # parse the input
            try:
                # Get input table as pandas data frame
                input_table = pd.read_csv(self.input_file, sep='\t', header=None, skiprows=4)
            except BaseException, e:
                logging.error("Unable to parse gene read counts!")
                if e.message != "":
                    logging.error("Received the following error msg:\n%s" % e.message)
                raise

            # add read counts to the db

            for bait in self.ERCC_baits:
                self.add_entry(bait, input_table.loc[input_table[0] == bait].iat[0,1])

    def define_required_colnames(self):
        return [bait for bait in self.ERCC_baits]
