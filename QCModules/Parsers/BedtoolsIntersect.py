from BaseParser import BaseParser

class BedtoolsIntersect(BaseParser):

    DESCRIPTION     = "Summarize overlap percentage from Bedtools Intersect output."
    INPUT_FILE_DESC = "Bedtools intersect output (produced with -c, -wa flags)"

    def __init__(self, sys_args):
        super(BaseParser, self).__init__(sys_args)

    def define_required_columns(self):
        # Define colnames required to be present in qc_report after parsing
        pass

    def parse_input(self):
        # Parse input and get
        pass