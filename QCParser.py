#!/usr/bin/env python
import argparse
import sys

import QCModules
from Utils import import_submodules

def import_qc_parser_modules():
    # Dynamically import and return all QCParser classes contained in the QCModules package

    # Import all modules in the QCModules folder
    qc_modules = import_submodules(QCModules)

    # Initialize new dictionary to hold class objects contained in modules
    classes = {}

    # Loop through modules to get any classes that inherit from BaseModule
    for module_name, module_obj in qc_modules.iteritems():
        # Exclude any base classes
        if "Base" not in module_name:
            # Get name of QCParser class contained within the module
            module_class_name = module_name.split(".")[-1]
            # Get only modules which contain a class inheriting from BaseModule
            if module_class_name in module_obj.__dict__:
                module_class = module_obj.__dict__[module_class_name]
                #if module_class in QCModules.BaseModule.__subclasses__():
                classes[module_class_name] = module_class
    return classes

def configure_base_arg_parser(available_modules, module_descriptions):

    # Build usage string based on descriptions of available modules detected
    usage_string = '''qcparser <tool> [tool_args]\nTools:\n'''
    for i in range(len(available_modules)):
        usage_string += "\t%s\t\t%s\n" %( available_modules[i], module_descriptions[i])
    usage_string += "\nFurther tool level options can be found for each module."

    # Create base arg parser
    parser = argparse.ArgumentParser(prog="QCParser",
                                     description="Tools for parsing output from several commonly available bioinformatic tools",
                                     usage = '''%s''' % usage_string)

    # Add argument for name of QCModule
    parser.add_argument('module',
                        choices=available_modules,
                        help='QCParser module to run.')
    return parser

def main():

    # Dynamically import QCParser modules in the QCModules directory
    qc_parser_modules = import_qc_parser_modules()

    # Get names and descriptions of each parser
    module_names        = qc_parser_modules.keys()
    module_descriptions = [qc_parser_module.DESCRIPTION for qc_parser_module in qc_parser_modules.values()]

    # Dynamically create arg parser with names and descriptions of available QCParser modules
    parser  = configure_base_arg_parser(module_names, module_descriptions)
    args    = parser.parse_args(sys.argv[1:2])

    # Try to initialize QCParser Module class and parse remaining command line arguments
    qc_module = qc_parser_modules[args.module](sys.argv[2:])

    # Configure logging levels
    qc_module.run()

if __name__=='__main__':
    main()