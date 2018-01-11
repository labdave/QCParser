from BaseParser import BaseParser

class FastQC(BaseParser):

    DESCRIPTION     = "Parse Picard InsertSize Metrics output."
    INPUT_FILE_DESC = "Picard InsertSize Metrics log file"

    def __init__(self, sys_args):
        super(BaseParser, self).__init__(sys_args)

    def make_qc_report(self):
        with open(self.input_file, "r") as fh:
            for line in fh:

                # Find line with number of reads input and surviving trimming
                if "FR" in line:
                    line = line.strip().split()

                    median_insert_size  = float(line[0])
                    mean_insert_size    = float(line[4])
                    sd_insert_size      = float(line[5])
                    min_insert_size     = float(line[2])
                    max_insert_size     = float(line[3])

                    # Add information to report
                    self.add_entry("Mean_Insert_Size",      mean_insert_size)
                    self.add_entry("Median_Insert_Size",    median_insert_size)
                    self.add_entry("Insert_Size_SD",        sd_insert_size)
                    self.add_entry("Min_Insert_Size",       min_insert_size)
                    self.add_entry("Max_Insert_Size",       max_insert_size)