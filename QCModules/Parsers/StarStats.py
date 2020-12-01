from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException

class StarStats(BaseParser):

    DESCRIPTION     = "Parse Star generated log file"
    INPUT_FILE_DESC = "Star final log file"

    def __init__(self, sys_args):
        super(StarStats, self).__init__(sys_args)

    def parse_input(self):
        # Parse STAR log file
        with open(self.input_file, "r") as fh:
            for line in fh:
                # remove the trailing new line character
                line = line.rstrip()

                data = line.split('|')

                if len(data) > 1:
                    stat_value = data[1].split('\t')[1]
                    if "Number of splices: Total" in data[0]:
                        self.add_entry("Total_Number_of_Splices", stat_value)
                    elif "Number of splices: Annotated (sjdb)" in data[0]:
                        self.add_entry("Number_of_Splices_Annotated_SJDB", stat_value)
                    elif "Number of splices: GT/AG" in data[0]:
                        self.add_entry("Number_of_Splices_GT_AG", stat_value)
                    elif "Number of splices: GC/AG" in data[0]:
                        self.add_entry("Number_of_Splices_GC_AG", stat_value)
                    elif "Number of splices: AT/AC" in data[0]:
                        self.add_entry("Number_of_Splices_AT_AC", stat_value)
                    elif "Number of splices: Non-canonical" in data[0]:
                        self.add_entry("Number_of_Splices_Non_canonical", stat_value)
                    else:
                        continue

    def define_required_colnames(self):
        return ["Total_Number_of_Splices","Number_of_Splices_Annotated_SJDB","Number_of_Splices_GT_AG",
                "Number_of_Splices_GC_AG","Number_of_Splices_AT_AC","Number_of_Splices_Non_canonical"]
