from BaseParser import BaseParser

class PicardInsertSize(BaseParser):

    DESCRIPTION     = "Parse Picard InsertSize Metrics output."
    INPUT_FILE_DESC = "Picard InsertSize Metrics log file"

    def __init__(self, sys_args):
        super(PicardInsertSize, self).__init__(sys_args)

    def parse_input(self):
        in_histogram = False
        ins_size_counts = []
        with open(self.input_file, "r") as fh:
            for line in fh:

                # Find line with number of reads input and surviving trimming
                if "FR" in line:
                    line = line.strip().split()

                    median_insert_size  = float(line[0])
                    mean_insert_size    = float(line[4])
                    sd_insert_size      = float(line[5])
                    min_insert_size     = int(line[2])
                    max_insert_size     = int(line[3])

                    # Add information to report
                    self.add_entry("Mean_Insert_Size",      mean_insert_size)
                    self.add_entry("Median_Insert_Size",    median_insert_size)
                    self.add_entry("Insert_Size_SD",        sd_insert_size)
                    self.add_entry("Min_Insert_Size",       min_insert_size)
                    self.add_entry("Max_Insert_Size",       max_insert_size)

                elif "## HISTOGRAM" in line:
                    in_histogram = True

                elif in_histogram and "insert_size" not in line:
                    # Get histogram count
                    data = line.strip().split()
                    if len(data) == 2:
                        ins_size_counts.append(data[1])

            # Add insert size distribution information
            self.add_entry("Ins_Size_Dist", ";".join(ins_size_counts))


    def define_required_colnames(self):
        return ["Mean_Insert_Size", "Median_Insert_Size", "Insert_Size_SD", "Min_Insert_Size", "Max_Insert_Size"]