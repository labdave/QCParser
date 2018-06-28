import logging
import pandas as pd
import numpy as np

from BaseParser import BaseParser
class GATKCollectReadCount(BaseParser):

    DESCRIPTION     = "Count total number of reads mapping to genomic features."
    INPUT_FILE_DESC = "GATK CollectReadCount TSV output"

    def __init__(self, sys_args):
        super(GATKCollectReadCount, self).__init__(sys_args)

    def parse_input(self):

        # Determine number of rows to skip (@SQ, @HQ, header lines)
        skip_rows = 0
        with open(self.input_file, 'r') as f:
            for line in f:
                if line.startswith("@") or line.startswith("CONTIG"):
                    skip_rows += 1
                else:
                    break

        # Names to associated with input columns
        input_column_names = ["CONTIG", "START", "END", "COUNT"]

        try:
            # Get input table as pandas data frame
            input_table = pd.read_table(self.input_file,
                                        delim_whitespace=True,
                                        header=None,
                                        names=input_column_names,
                                        skiprows=skip_rows)

        except BaseException, e:
            logging.error("Unable to parse GATK CollectReadCount output!")
            logging.error("Columns should be the following: %s" % "\t".join(input_column_names))
            if e.message != "":
                logging.error("Received the following error msg:\n%s" % e.message)
            raise

        on_target_reads     = int(input_table.COUNT.sum())                  # Num reads map to a target region
        num_targets         = len(input_table)                              # Total number of targets
        missed_targets      = len(input_table[input_table.COUNT <= 0])      # Number of targets not hit by any reads
        pct_missing         = (missed_targets*1.0 / num_targets*1.0) * 100  # Percentage of targets missed by sequencing
        self.add_entry("Reads_Mapped_to_Target",        on_target_reads)
        self.add_entry("Target_Regions",                num_targets)
        self.add_entry("Target_Regions_Missed",         missed_targets)
        self.add_entry("Pct_Target_Regions_Missed",     pct_missing)

    def define_required_colnames(self):
        return ["Reads_Mapped_to_Target",
                "Target_Regions",
                "Target_Regions_Missed",
                "Pct_Target_Regions_Missed"]
