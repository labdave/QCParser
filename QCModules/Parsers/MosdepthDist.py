import logging

from QCModules.BaseModule import QCParseException
from BaseParser import BaseParser

class MosdepthDist(BaseParser):

    DESCRIPTION     = "Parse read depth distribution output from Mosdepth"
    INPUT_FILE_DESC = "Mosdepth *dist.txt file"

    def __init__(self, sys_args):
        super(MosdepthDist, self).__init__(sys_args)

    def parse_input(self):

        pct_covered_hist = []
        q1      = None
        median  = None
        q3      = None

        with open(self.input_file, "r") as fh:

            # Parse summary file and store results
            for line in fh:

                # Skip if line doesn't start with 'total'
                if not line.startswith("total"):
                    continue

                # Get next value in cumsum distribution
                line = line.strip().split("\t")
                if len(line) != 3:
                    raise QCParseException(
                        "MosdepthDist file '%s' contains at least one line that doesn't have 3 columns! "
                        "Make sure it's actually output from Mosdepth!" % self.input_file)

                # Depth
                dp = int(line[1])
                # Pct of bases covered >= Depth
                pct_covered = float(line[2])

                # Add to cumsum distribution
                pct_covered_hist.append(str(pct_covered))

                # Determine if
                if q3 is None and pct_covered >= 0.25:
                    q3 = dp

                elif median is None and pct_covered >= 0.5:
                    median = dp

                elif q1 is None and pct_covered >= 0.75:
                    q1 = dp

        q1 = 0 if q1 is None else q1
        median = 0 if median is None else median
        q3 = 0 if q3 is None else q3

        if len(pct_covered_hist) <= 0:
            raise QCParseException(
                "MosdepthDist file '%s' does not contain any lines with 'total' in first column!. "
                "Make sure it's actually output from Mosdepth!" % self.input_file)

        self.add_entry("median_cov",           median)
        self.add_entry("25_pct_cov",    q1)
        self.add_entry("75_pct_cov",    q3)
        self.add_entry("depth_dist",        ";".join(pct_covered_hist))

    def define_required_colnames(self):
        return ["median_cov",
                "25_pct_cov",
                "75_pct_cov",
                "depth_dist"]
