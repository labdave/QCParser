from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException

class SamtoolsCountReads(BaseParser):

    DESCRIPTION     = "Parse Samtools view output for overlapping read counts (v1.3 and later)"
    INPUT_FILE_DESC = "Samtools view output with overlapping read counts"

    def __init__(self, sys_args):
        super(SamtoolsCountReads, self).__init__(sys_args)

    def parse_input(self):

        # intialize the read counts place holder
        read_counts = 0

        # Parse samtools view output for overlapping read counts
        with open(self.input_file) as inp:
            for line_id, line in enumerate(inp):
                # raise an error if the input file contains other than the overlapping read counts meaning more than
                # one line in the input file
                if line_id > 0:
                    raise QCParseException("SAMTOOLS view generated output is not in expected format. The output "
                                           "should only contains ovelapping read counts.")

                # make sure the read counts is in int format
                read_counts = int(line)

        # Add entries
        self.add_entry("read_counts", read_counts)

    def define_required_colnames(self):
        return ["read_counts"]