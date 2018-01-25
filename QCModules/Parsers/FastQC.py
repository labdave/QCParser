from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException

class FastQC(BaseParser):

    DESCRIPTION     = "Parse Fastqc text output"
    INPUT_FILE_DESC = "FastQC output file (fastqc_data.txt)"

    def __init__(self, sys_args):
        super(FastQC, self).__init__(sys_args)

    def parse_input(self):

        # Parse Fastqc data
        first_line      = True
        test_results    = []
        colname         = None
        value           = None
        in_base_quality_section = False
        qual_scores = []

        with open(self.input_file, "r") as fh:

            # Parse summary file and store results
            for line in fh:
                # Strip newlines
                line = line.strip()

                # Check to make sure file is actually the correct filetype
                if first_line and "FastQC" not in line:
                    raise QCParseException("FastQC file '%s' does not contain 'FastQC' in first line. Make sure it's the fastq_data.txt.")
                first_line = False

                if "Total Sequences" in line:
                    # Get read count
                    colname     = "Total_Reads"
                    value   = int(line.split()[2])

                elif "flagged as poor quality" in line:
                    # Get num low quality reads
                    colname     = "LQ_Reads"
                    value   = int(line.split()[5]) * 2

                elif "Sequence length" in line:
                    # Get sequence length
                    colname     = "Read_Len"
                    value   = line.split()[2]

                elif "%GC" in line:
                    # Get GC percent
                    colname = "GC"
                    value = float(line.split()[1])

                elif ">>" in line and "END_MODULE" not in line:
                    # Record results from test (e.g. PASS/WARN/FAIL)
                    line = line[2:]
                    test_results.append(line.split()[-1])

                    # Check to see if we're in the per base sequence quality section
                    test_name = " ".join(line.split()[:-1])
                    if test_name == "Per base sequence quality":
                        # Set flag
                        in_base_quality_section = True
                    else:
                        in_base_quality_section = False

                elif in_base_quality_section:
                    if "#" not in line and ">>" not in line:
                        # Get next quality score
                        qual_scores.append(line.split()[1])

                else:
                    colname = None
                    value = None

                # add to summary summary if necessary
                if colname is not None and value is not None:
                    self.add_entry(colname, value)

        # Add FastQC test results
        self.add_entry(colname="FastQC_Tests", value=";".join(test_results))

        # Add BaseQuality scores
        self.add_entry(colname="AvgQualScores", value=";".join(qual_scores))

    def define_required_colnames(self):
        return ["FastQC_Tests", "Total_Reads", "LQ_Reads", "Read_Len", "GC"]


