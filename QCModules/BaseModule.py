import abc
import argparse

class BaseModule(object):
    __metaclass__ = abc.ABCMeta

    # Description to be used by arg parser when building a description string
    DESCRIPTION = None

    def __init__(self, sys_argv):
        # Sys_argv is designed to be command line arguments (usually sys.argv[2:])

        # Parse command line options
        self.args   = self.parse_args(sys_argv)

        # Initialize empty QCReport
        self.qc_report  = None

    def parse_args(self, sys_argv):

        # Create base parser with verbosity option
        arg_parser = argparse.ArgumentParser(description=self.DESCRIPTION)
        arg_parser.add_argument("-v",
                                action='count',
                                dest='verbosity_level',
                                required=False,
                                default=0,
                                help="Increase verbosity of the program."
                                  "Multiple -v's increase the verbosity level:\n"
                                  "0 = Errors\n"
                                  "1 = Errors + Warnings\n"
                                  "2 = Errors + Warnings + Info\n"
                                  "3 = Errors + Warnings + Info + Debug")

        # Add any additional options
        arg_parser = self.configure_arg_parser(arg_parser)
        return arg_parser.parse_args(sys_argv)

    def get_qc_report(self):
        return self.qc_report

    def get_verbosity_level(self):
        return self.args.verbosity_level

    @abc.abstractmethod
    def configure_arg_parser(self, base_parser):
        # Add additional arg parser options and return arg parser
        pass

    @abc.abstractmethod
    def make_qc_report(self):
        # Main module code goes here
        pass


