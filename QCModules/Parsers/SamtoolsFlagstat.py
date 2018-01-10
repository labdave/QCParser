from BaseParser import BaseParser

class SamtoolsFlagstat(BaseParser):

    DESCRIPTION     = "Parse Samtools flagstat output (v1.3 and later)"
    INPUT_FILE_DESC = "Samtools flagstat output"

    def __init__(self, sys_args):
        super(BaseParser, self).__init__(sys_args)

    def define_required_columns(self):
        # Define colnames required to be present in qc_report after parsing
        pass

    def parse_input(self):
        # Parse input and get
        pass