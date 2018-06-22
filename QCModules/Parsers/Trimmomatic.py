from QCModules.BaseModule import QCParseException
from BaseParser import BaseParser

class Trimmomatic(BaseParser):

    DESCRIPTION     = "Parse Trimmomatic stderr log."
    INPUT_FILE_DESC = "Trimmomatic stderr log"

    def __init__(self, sys_args):
        super(Trimmomatic, self).__init__(sys_args)

    def parse_input(self):
        # open input file
        is_paired   = True
        header_seen = False
        with open(self.input_file, "r") as fh:
            for line in fh:
                # find line with number of reads input and surviving trimming
                if not header_seen and "TrimmomaticSE" in line:
                    is_paired   = False
                    header_seen = True
                elif not header_seen and "TrimmomaticPE" in line:
                    header_seen = True
                elif "Surviving" in line:
                    if is_paired:
                        # paired-end output
                        input_reads = int(line.strip().split()[3]) * 2
                        trimmed_reads = int(line.strip().split()[6]) * 2
                    else:
                        # single-end output
                        input_reads = int(line.strip().split()[2])
                        trimmed_reads = int(line.strip().split()[4])
                    self.add_entry("Input_Reads", input_reads)
                    self.add_entry("Trimmed_Reads", trimmed_reads)
                    break

            # Raise exception if header line never seen
            if not header_seen:
                raise QCParseException("Input file is not output from trimmomatic!")

    def define_required_colnames(self):
        return ["Input_Reads", "Trimmed_Reads"]