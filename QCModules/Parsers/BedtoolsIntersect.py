import logging
import pandas as pd
import numpy as np

from BaseParser import BaseParser

class BedtoolsIntersect(BaseParser):

    DESCRIPTION     = "Summarize overlap percentage from Bedtools Intersect output."
    INPUT_FILE_DESC = "Bedtools intersect output (produced with -c, -wa flags)"

    def __init__(self, sys_args):
        super(BaseParser, self).__init__(sys_args)

    def make_qc_report(self):

        # Names to associated with input columns
        input_column_names = ["chr", "start", "end", "header", "mq", "strand", "start2", "end2", "color", "passed", "length", "dummy", "mapped"]

        try:
            # Get input table as pandas data frame
            input_table = pd.read_table(self.input_file,
                                        names= input_column_names,
                                        header=None,
                                        usecols=["mapped"])
        except BaseException, e:
            logging.error("Unable to parse BedtoolsIntersect output! Make sure BedtoolsIntersect was run with the -c and -wa flags!")
            logging.error("Columns should be the following: %s" % "\t".join(input_column_names))
            if e.message != "":
                logging.error("Received the following error msg:\n%s" % e.message)

        # Replace '.' with 0 for unmapped reads
        input_table.mapped.replace(".", "0", inplace=True)

        # Convert everything to int
        input_table.mapped = input_table.mapped.apply(np.int16)

        # Get percent of reads that intersected the target
        reads_mapped, pct_mapped = self.__get_pct_reads_mapped(input_table)
        self.add_entry("Num_Mapped_to_Target", reads_mapped)
        self.add_entry("Pct_Mapped_to_Target", pct_mapped)

    def __get_pct_reads_mapped(self, input_table):
        # Determine the percentage of reads in the bedfile that mapped to the target region
        total_bases = len(input_table) * 1.0
        covered_bases = len(input_table[input_table.mapped > 0]) * 1.0
        return int(covered_bases), (covered_bases / total_bases) * 100
