import logging

from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException

class SamtoolsIdxstats(BaseParser):

    DESCRIPTION     = "Parse Samtools idxstats output (v1.3 and later)"
    INPUT_FILE_DESC = "Samtools idxstats output"

    def __init__(self, sys_args):
        super(SamtoolsIdxstats, self).__init__(sys_args)

    def parse_input(self):

        # Initialize idxstats information
        ref_length = []
        aligned = []
        unaligned = []

        # Parse samtools idxstats output
        with open(self.input_file) as inp:
            for line in inp:

                # Get information from the line
                info = line.strip().split("\t")

                # Get the reference name
                ref_name = info[0]

                # Add information for the reference name
                ref_length.append("%s:%s" % (ref_name, info[1]))
                aligned.append("%s:%s" % (ref_name, info[2]))
                unaligned.append("%s:%s" % (ref_name, info[3]))

        # Add entries
        self.add_entry("Ref_length", ";".join(ref_length))
        self.add_entry("Aligned", ";".join(aligned))
        self.add_entry("Unaligned", ";".join(unaligned))

    def define_required_colnames(self):
        return ["Ref_length", "Aligned", "Unaligned"]
