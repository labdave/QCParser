from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException

class TNADemuxReport(BaseParser):

    DESCRIPTION     = "Parse RNA/DNA report from TNA demux script"
    INPUT_FILE_DESC = "CSV output from TNA demux script (all_barcode_stats.csv)"

    def __init__(self, sys_args):
        super(TNADemuxReport, self).__init__(sys_args)

    def parse_input(self):

        # Parse TNADemux stat output
        first_line      = True

        with open(self.input_file, "r") as fh:

            # Parse summary file and store results
            for line in fh:
                # Strip newlines
                line = line.strip().split(",")

                # Check to make sure file is actually the correct filetype
                if first_line:
                    if "total_percent_rna" not in line:
                        raise QCParseException("TNADemux file '%s' does not contain 'total_percent_rna' in first line. "
                                           "Make sure it's the all_barcode_stats.txt!")
                    elif len(line) != 8:
                        raise QCParseException("TNADemux file '%s' does not have exactly four columns! Expected\n"
                                               "columns: sample,barcode,read1_percent,read2_percent,",
                                               "total_percent_rna,total_reads,rna_reads,nonrna_reads\n"
                                               "Make sure it's the all_barcode_stats.txt!")
                    first_line = False
                else:
                    self.add_entry("R1_Percent", float(line[2]), note = line[1])
                    self.add_entry("R2_Percent", float(line[3]), note = line[1])
                    self.add_entry("Total_RNA_Percent", float(line[4]), note = line[1])
                    self.add_entry("Total_reads", int(float(line[5])), note = line[1])
                    self.add_entry("RNA_reads", int(float(line[6])), note = line[1])
                    self.add_entry("NON_RNA_reads", int(float(line[7])), note = line[1])

    def define_required_colnames(self):
        return ["R1_Percent", "R2_Percent", "Total_RNA_Percent", "Total_reads", "RNA_reads", "NON_RNA_reads"]