from BaseParser import BaseParser

class Trimmomatic(BaseParser):

    DESCRIPTION     = "Parse Trimmomatic stderr log."
    INPUT_FILE_DESC = "Trimmomatic stderr log"

    def __init__(self, sys_args):
        super(BaseParser, self).__init__(sys_args)

    def define_required_columns(self):
        # Define colnames required to be present in qc_report after parsing
        pass

    def parse_input(self):
        # Parse input and get
        pass