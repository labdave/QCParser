from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException

class BedtoolsCoverage(BaseParser):

    DESCRIPTION     = "Parse Bedtools Coverage Stats Report file"
    INPUT_FILE_DESC = "Coverage Stats file from CoverageStats module"

    def __init__(self, sys_args):
        super(BedtoolsCoverage, self).__init__(sys_args)

    def parse_input(self):

        # Parse CoverageStats module output file
        with open(self.input_file) as inp:

            for line_id, line in enumerate(inp):
                # raise an error if the input file contains more than two rows
                if line_id > 1:
                    raise QCParseException("CoverageStats generated output is not in expected format. The output "
                                           "should only contains two rows including header.")

                # skip the header line
                if line_id == 0:
                    continue

                # split the stats
                stats = line.strip().split(",")

                # Add entries
                self.add_entry("BoC_perc_baits_covered", stats[1])
                self.add_entry("BoC_median", stats[2])
                self.add_entry("DoC_mean", stats[3])
                self.add_entry("DoC_median", stats[4])

    def define_required_colnames(self):
        return ["BoC_perc_baits_covered","BoC_median","DoC_mean","DoC_median"]