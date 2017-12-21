import abc

class BaseModule(object):
    __metaclass__ = abc.ABCMeta

    # Description to be used by arg parser when building a description string
    DESCRIPTION = "Base Module"

    def __init__(self, command_line_args, **kwargs):
        # Parse command line arguments
        self.arg_parser     = self.get_arg_parser()
        self.args           = self.arg_parser.parse_args(command_line_args)

    @abc.abstractmethod
    def get_arg_parser(self):
        # Return the module's command line parser
        pass

    @abc.abstractmethod
    def run(self, **kwargs):
        # Main module code goes here
        pass


