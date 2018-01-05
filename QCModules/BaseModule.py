import abc

class BaseModule(object):
    __metaclass__ = abc.ABCMeta

    # Description to be used by arg parser when building a description string
    DESCRIPTION = None

    # Names of data columns produced by Module
    COLNAMES    = []

    def __init__(self, command_line_args, **kwargs):
        # Parse command line arguments
        self.arg_parser     = self.get_arg_parser()
        self.args           = self.arg_parser.parse_args(command_line_args)
        self.qc_report      = None

    def get_qc_report(self):
        return self.qc_report

    @abc.abstractmethod
    def get_arg_parser(self):
        # Return the module's command line parser
        pass

    @abc.abstractmethod
    def parse(self, **kwargs):
        # Main module code goes here
        pass


