import sys
import logging

def configure_logging(verbosity):
    # Setting the format of the logs
    FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"

    # Configuring the logging system to the lowest level
    logging.basicConfig(level=logging.DEBUG, format=FORMAT, stream=sys.stderr)

    # Defining the ANSI Escape characters
    BOLD = '\033[1m'
    DEBUG = '\033[92m'
    INFO = '\033[94m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'

    # Coloring the log levels
    if sys.stderr.isatty():
        logging.addLevelName(logging.ERROR, "%s%s%s%s%s" % (BOLD, ERROR, "GAP_DAEMON_ERROR", END, END))
        logging.addLevelName(logging.WARNING, "%s%s%s%s%s" % (BOLD, WARNING, "GAP_DAEMON_WARNING", END, END))
        logging.addLevelName(logging.INFO, "%s%s%s%s%s" % (BOLD, INFO, "GAP_DAEMON_INFO", END, END))
        logging.addLevelName(logging.DEBUG, "%s%s%s%s%s" % (BOLD, DEBUG, "GAP_DAEMON_DEBUG", END, END))
    else:
        logging.addLevelName(logging.ERROR, "GAP_DAEMON_ERROR")
        logging.addLevelName(logging.WARNING, "GAP_DAEMON_WARNING")
        logging.addLevelName(logging.INFO, "GAP_DAEMON_INFO")
        logging.addLevelName(logging.DEBUG, "GAP_DAEMON_DEBUG")

    # Setting the level of the logs
    level = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG][verbosity]
    logging.getLogger().setLevel(level)

def configure_argparser(argparser_obj):

    def file_type(arg_string):
        """
        This function check both the existance of input file and the file size
        :param arg_string: file name as string
        :return: file name as string
        """
        if not os.path.exists(arg_string):
            err_msg = "%s does not exist! " \
                      "Please provide a valid file!" % arg_string
            raise argparse.ArgumentTypeError(err_msg)

        return arg_string

    # Path to VCF input file
    argparser_obj.add_argument("--vcf",
                               action="store",
                               type=file_type,
                               dest="vcf_file",
                               required=True,
                               help="Path to vcf file to recode.")

    # Path to VCF input file
    argparser_obj.add_argument("--output",
                               action="store",
                               type=str,
                               dest="out_file",
                               required=True,
                               help="Path to recoded output file.")

    argparser_obj.add_argument("--info-columns",
                               action="store",
                               type=str,
                               dest="info_columns",
                               required=False,
                               default=None,
                               help="Column-delimited list of INFO columns to include in output. NO SPACES ALLOWED or list will not be parsed!")

    # Path to recoded output file
    argparser_obj.add_argument("--min-call-depth",
                               action="store",
                               type=int,
                               dest="min_call_depth",
                               required=False,
                               default=10,
                               help="Minimum read depth required to call variant genotype.")

    # Character used to denote missing variant information
    argparser_obj.add_argument("--missing-data-char",
                               action="store",
                               type=str,
                               dest="missing_data_char",
                               required=False,
                               default='.',
                               help="Character used as placeholder for missing VCF info.")

    # Character used to denote missing genotypes
    argparser_obj.add_argument("--missing-gt-char",
                               action="store",
                               type=str,
                               dest="missing_gt_char",
                               required=False,
                               default='NA',
                               help="Character used as placeholder for missing genotypes.")

    # Flag to allow VCF records with >1 alternate allele. Default is to not use this and throw errors.
    # You really shouldn't ever use this flag because parsing multiple alternate alleles with multiple annotations can fuck shit up.
    argparser_obj.add_argument("--multiallelic",
                               action="store_true",
                               dest="multiallelic",
                               required=False,
                               help="Flag allowing variant records to contain more than one alternate allele. This flag shouldn't really be used.")

    # Verbosity level
    argparser_obj.add_argument("-v",
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