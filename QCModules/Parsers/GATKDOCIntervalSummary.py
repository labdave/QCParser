import logging
import pandas as pd
import numpy as np

from BaseParser import BaseParser
class GATKDOCIntervalSummary(BaseParser):

    DESCRIPTION     = "Parse the interval summary stats from GATK DepthOfCoverage tool."
    INPUT_FILE_DESC = "GATK DepthOfCoverage Interval Summary Statistics TSV output"

    def __init__(self, sys_args):
        super(GATKDOCIntervalSummary, self).__init__(sys_args)

    def parse_input(self):

        try:
            # Get input table as pandas data frame
            input_table = pd.read_table(self.input_file)

        except BaseException, e:
            logging.error("Unable to parse GATK DepthOfCoverage interval summary output!")
            if e.message != "":
                logging.error("Received the following error msg:\n%s" % e.message)
            raise

        total_regions                   = input_table['depth>=0']
        regions_above_hundreadX_depth    = input_table['depth>=100']

        pct_regions_above_hundreadX_depth = round((regions_above_hundreadX_depth/total_regions)*100, 2)

        self.add_entry("pct_regions_above_hundreadX_depth", pct_regions_above_hundreadX_depth)

    def define_required_colnames(self):
        return ["pct_regions_above_hundreadX_depth"]
