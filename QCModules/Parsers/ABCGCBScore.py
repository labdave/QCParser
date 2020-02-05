from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException

class ABCGCBScore(BaseParser):

    DESCRIPTION     = "Parse ABCGCBScore module output for to get the ABCGCBScore"
    INPUT_FILE_DESC = "ABCGCBScore module output file containing the score"

    def __init__(self, sys_args):
        super(ABCGCBScore, self).__init__(sys_args)

    def parse_input(self):

        # intialize the read counts place holder
        abc_gcb_score = 0

        # Parse samtools view output for overlapping read counts
        with open(self.input_file) as inp:
            for line_id, line in enumerate(inp):
                # raise an error if the input file contains other than the abc/gcb score meaning more than
                # one line in the input file
                if line_id > 0:
                    raise QCParseException("ABCGCBScore generated output is not in expected format. The output "
                                           "should only contains abc/gcb score.")

                # make sure the read counts is in int format
                line = line.rstrip()
                abc_gcb_score = round(float(line.split('\t')[1]),4)


        # Add entries
        self.add_entry("abc_gcb_score", abc_gcb_score)

    def define_required_colnames(self):
        return ["abc_gcb_score"]