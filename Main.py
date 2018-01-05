#!/usr/bin/env python
import argparse

import QCModules
from Utils import import_submodules

def get_qc_parser_classes(qc_modules):
    # Takes a dict of modules found in the QCMOdules folder
    # Returns all class objects within these modules that extend the BaseModule class
    classes = {}
    for module_name, module_obj in qc_modules.iteritems():
        # Exclude any base classes
        if "Base" not in module_name:
            module_class_name = module_name.split(".")[-1]
            # Get only modules which contain a class inheriting from BaseModule
            if module_class_name in module_obj.__dict__:
                module_class = module_obj.__dict__[module_class_name]
                if module_class in QCModules.BaseModule.__subclasses__():
                    classes[module_class_name] = module_class
    return classes

def configure_arg_parser(available_modules, module_descriptions):

    # Build usage string
    usage_string = '''qcparser <tool> [<args>]\nTools:\n'''
    for i in range(len(available_modules)):
        usage_string += "\t%s\t%s\n" %( available_modules[i], module_descriptions[i])
    usage_string += "\nFurther tool level options can be found for each module."

    # Create arg parser
    parser = argparse.ArgumentParser(description="Tools for parsing output from several commonly available bioinformatic tools",
                                     usage = '''%s''' % usage_string)

    # QCParser module to select
    parser.add_argument('module',
                        choices=available_modules,
                        help='QCParser module to run.')

    # Verbosity level
    parser.add_argument("-v", action='count',
                        dest='verbosity_level',
                        required=False,
                        default=0,
                        help="Increase verbosity of the program. Multiple -v's increase the verbosity level:\n"
                            "0 = Errors\n"
                            "1 = Errors + Warnings\n"
                            "2 = Errors + Warnings + Info\n"
                            "3 = Errors + Warnings + Info + Debug")
    return parser

def main():

    # Import all available modules within the QCModules directory
    qc_parser_modules = import_submodules(QCModules)

    # Get any class objects within these modules that inherit from BaseModule
    qc_parser_classes = get_qc_parser_classes(qc_parser_modules)

    # Get names and descriptions of each parser
    qc_parser_class_names   = [x.__name__ for x in qc_parser_classes.values()]
    qc_parser_descriptions  = [x.DESCRIPTION for x in qc_parser_classes.values()]

    parser = configure_arg_parser(qc_parser_class_names, qc_parser_descriptions)
    args = parser.parse_args()

    # Initialize QCParser Module class
    #cmd_line_args =
    #qc_module = qc_parser_classes[args.module]

if __name__=='__main__':
    main()