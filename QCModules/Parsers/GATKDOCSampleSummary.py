import logging
import pandas as pd
import numpy as np

from BaseParser import BaseParser
class GATKDOCSampleSummary(BaseParser):

    DESCRIPTION     = "Parse the sample summary stats from GATK DepthOfCoverage tool."
    INPUT_FILE_DESC = "GATK DepthOfCoverage Sample Summary Statistics TSV output"

    def __init__(self, sys_args):
        super(GATKDOCSampleSummary, self).__init__(sys_args)

    def parse_input(self):

        # Names to associated with input columns
        input_column_names = ["sample_id", "total", "mean_coverage", "granular_third_quartile", "granular_median",
                              "granular_first_quartile", "oneX", "tenX", "twintyFiveX", "fiftyX", "seventyFiveX",
                              "hundreadX", "hundreadAndFiftyX", "twoHundreadX", "twoHundreadAndFiftyX", "fivehundreadX"]

        try:
            # Get input table as pandas data frame
            input_table = pd.read_table(self.input_file,
                                        header=0,
                                        names=input_column_names,
                                        skipfooter=1,
                                        engine='python'
                                        )

        except BaseException, e:
            logging.error("Unable to parse GATK DepthOfCoverage sample summary output!")
            logging.error("Columns should be the following: %s" % "\t".join(input_column_names))
            if e.message != "":
                logging.error("Received the following error msg:\n%s" % e.message)
            raise

        mean_coverage                           = float(input_table.mean_coverage)            # mean coverage value
        pct_bases_above_onex                    = float(input_table.oneX)                     # percentage of bases covered by atleast 1X
        pct_bases_above_tenX                    = float(input_table.tenX)                     # percentage of bases covered by atleast 10X
        pct_bases_above_twintyFiveX             = float(input_table.twintyFiveX)              # percentage of bases covered by atleast 25X
        pct_bases_above_fiftyX                  = float(input_table.fiftyX)                   # percentage of bases covered by atleast 50X
        pct_bases_above_seventyFiveX            = float(input_table.seventyFiveX)             # percentage of bases covered by atleast 75X
        pct_bases_above_hundreadX               = float(input_table.hundreadX)                # percentage of bases covered by atleast 100X
        pct_bases_above_hundreadAndFiftyX       = float(input_table.hundreadAndFiftyX)        # percentage of bases covered by atleast 150X
        pct_bases_above_twoHundreadX            = float(input_table.twoHundreadX)             # percentage of bases covered by atleast 200X
        pct_bases_above_twoHundreadAndFiftyX    = float(input_table.twoHundreadAndFiftyX)     # percentage of bases covered by atleast 250X
        pct_bases_above_fivehundreadX           = float(input_table.fivehundreadX)            # percentage of bases covered by atleast 500X

        self.add_entry("mean_coverage",                         mean_coverage)
        self.add_entry("pct_bases_above_onex",                  pct_bases_above_onex)
        self.add_entry("pct_bases_above_tenX",                  pct_bases_above_tenX)
        self.add_entry("pct_bases_above_twintyFiveX",           pct_bases_above_twintyFiveX)
        self.add_entry("pct_bases_above_fiftyX",                pct_bases_above_fiftyX)
        self.add_entry("pct_bases_above_seventyFiveX",          pct_bases_above_seventyFiveX)
        self.add_entry("pct_bases_above_hundreadX",             pct_bases_above_hundreadX)
        self.add_entry("pct_bases_above_hundreadAndFiftyX",     pct_bases_above_hundreadAndFiftyX)
        self.add_entry("pct_bases_above_twoHundreadX",          pct_bases_above_twoHundreadX)
        self.add_entry("pct_bases_above_twoHundreadAndFiftyX",  pct_bases_above_twoHundreadAndFiftyX)
        self.add_entry("pct_bases_above_fivehundreadX",         pct_bases_above_fivehundreadX)

    def define_required_colnames(self):
        return ["mean_coverage", "pct_bases_above_onex", "pct_bases_above_tenX", "pct_bases_above_twintyFiveX",
                "pct_bases_above_fiftyX", "pct_bases_above_seventyFiveX", "pct_bases_above_hundreadX",
                "pct_bases_above_hundreadAndFiftyX", "pct_bases_above_twoHundreadAndFiftyX",
                "pct_bases_above_twoHundreadX", "pct_bases_above_fivehundreadX"]
