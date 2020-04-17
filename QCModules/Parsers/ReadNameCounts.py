from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException

class ReadNameCounts(BaseParser):

    DESCRIPTION     = "Count the readnames present into a given file"
    INPUT_FILE_DESC = "Read names produced from the utils get read names"

    def __init__(self, sys_args):
        super(ReadNameCounts, self).__init__(sys_args)

    def parse_input(self):

        # intialize the read counts place holder
        read_counts = 0

        # Parse samtools view output for overlapping read counts
        with open(self.input_file) as inp:
            for line in inp:
                # increas the read counts is in int format
                read_counts += 1

        # Add entries
        self.add_entry("read_counts", read_counts)

    def define_required_colnames(self):
        return ["read_counts"]
