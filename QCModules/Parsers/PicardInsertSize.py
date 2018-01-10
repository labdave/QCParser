from BaseParser import BaseParser

class FastQC(BaseParser):

    DESCRIPTION     = "Parse Picard InsertSize Metrics output."
    INPUT_FILE_DESC = "Picard InsertSize Metrics log file"

    def __init__(self, sys_args):
        super(BaseParser, self).__init__(sys_args)

    def define_required_columns(self):
        # Define colnames required to be present in qc_report after parsing
        pass

    def parse_input(self):
        # Parse input and get
        pass