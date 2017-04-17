class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


class MissingFastqcZipFileError(Exception):
    def __init__(self, fastqc_zip):
        self.fastqc_zip = fastqc_zip

    def __str__(self):
        return ("Fastcq zip file not found: %s" % (self.fastqc_zip))


class MissingFastqcSummaryFileError(Exception):
    def __init__(self, fastqc_summary):
        self.fastqc_summary = fastqc_summary

    def __str__(self):
        return ("Fastcq summary file not found: %s" % (self.fastqc_summary))


class MissingSummaryFileError(Exception):
    def __init__(self, summary_type, summary_file):
        self.type = summary_type
        self.file = summary_file

    def __str__(self):
        return ("%s summary file not found: %s" % (self.type, self.file))


class SummaryParseError(Exception):
    def __init__(self, summary_type, summary_file, msg):
        self.type = summary_type
        self.file = summary_file
        self.msg = msg

    def __str__(self):
        return ("Error parsing %s summary file: %s\n%s" % (self.type, self.file, self.msg))