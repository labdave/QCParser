#!/usr/bin/env python
import argparse
import sys


def configure_arg_parser():
    parser = argparse.ArgumentParser(description="Tools for parsing output from several commonly available bioinformatic tools",
                                     usage = '''qcparser <tool> [<args>]
                                     Tools:
                                        fastqc      parse fastqc text output
                                        flagstat    parse samtools flagstat output
                                        capture     parse/summarize output from bedtools intersect
                                        coverage    parse/summarize output from samtools depth
                                        trimmomatic parse output from trimmomatic
                                        insertsize  parse output from Picard CollectInsertSizeMetrics
                                        merge       merge parsed output files from multiple tools (column-wise) or across multiple samples (row-wise)''')

    parser.add_argument('module', help='QCParser module to run.')
    parser.add_argument()

def main():
    # Configure arg parser



if __name__=='__main__':
    try:
        QCParser()
    except Exception:
        sys.exit(1)